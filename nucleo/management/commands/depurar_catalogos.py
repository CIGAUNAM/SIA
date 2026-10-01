"""Depura los catálogos Comisión, Cargo, Beca y Distinción según el mapeo revisado (datos/depuracion/mapeo_catalogos.py).

El catálogo queda con el TIPO de cosa; lo específico (programa, convocatoria, nivel, clave del proyecto) pasa al
registro (`función`, `detalle`, `institución`, `modalidad`). Los registros que no corresponden a la sección se
mueven a la suya (arbitrajes, cursos, sociedades, labores directivas).

Sin --aplicar todo corre en una transacción que se revierte al final (simulacro). Cada cambio deja su motivo en el
historial.
"""

import importlib.util
from collections import Counter
from datetime import date
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from compromiso_institucional.models import Comision, ComisionInstitucional, LaborDirectivaCoordinacion
from distinciones.models import DistincionAcademico, DistincionAlumno, SociedadCientifica
from formacion_recursos_humanos.models import AsesoriaEstudiante, DireccionTesis, SupervisionPostdoctoral
from nucleo.models import Beca, Cargo, Distincion, Institucion, ModalidadBeca, Revista
from vinculacion.models import ArbitrajePublicacion, OtraComision, ServicioAsesoriaExterna, TipoComision

MOTIVO = 'Depuración de catálogos'
F = ComisionInstitucional.Funcion
FUNCIONES = {f.label.lower(): f.value for f in F} | {k.lower(): v for k, v in {
    'Representante': F.TITULAR, 'Representante del personal académico': F.TITULAR,
    'Representante titular de los investigadores': F.TITULAR, 'Representante de los investigadores': F.TITULAR,
    'Representante suplente de los investigadores': F.SUPLENTE, 'Representante de los tutores': F.TITULAR,
    'Organizador': F.COORDINADOR, 'Presidente': F.PRESIDENTE, 'Integrante': F.INTEGRANTE, 'Moderador(a)': F.COMENTARISTA,
}.items()}
#: Instituciones que otorgan becas y distinciones: etiqueta del mapeo → pk existente o datos para crearla.
INSTITUCIONES = {
    'SECIHTI': {'nombre': 'Secretaría de Ciencia, Humanidades, Tecnología e Innovación (SECIHTI)', 'pais': 'México',
                'clasificacion': 'FEDERAL'},
    'CONACyT (hoy SECIHTI)': 65,
    'UNAM': 1, 'UNAM, DGAPA': 31, 'UNAM, Instituto de Geografía': 16,
    'UNAM, Coordinación General de Estudios de Posgrado': {'nombre': 'Coordinación General de Estudios de Posgrado',
                                                          'padre': 1, 'pais': 'México', 'pertenece_unam': True},
    'UNAM, ENES Morelia': 10,
    'Universidad de Twente (proyecto KTGAL)': 127,
    'Nuffic (Países Bajos)': {'nombre': 'Nuffic', 'pais': 'Países Bajos / Holanda'},
    'Gobierno de Australia': {'nombre': 'Gobierno de Australia', 'pais': 'Australia', 'clasificacion': 'FEDERAL'},
    'Secretaría de Relaciones Exteriores (AMEXCID)': 75,
    'GeoForAll Iberoamérica': 942,
    'Progress in Development Studies (revista, SAGE)': {'nombre': 'Progress in Development Studies (SAGE)',
                                                        'pais': 'Reino Unido'},
    'Ashden (Reino Unido)': {'nombre': 'Ashden', 'pais': 'Reino Unido', 'clasificacion': 'NO_LUCRATIVA'},
    'Universidad de Cambridge': 669,
    'Sociedad Científica Latinoamericana de Agroecología (SOCLA)': 288,
    'Consejo General del Val-de-Marne (Francia)': {'nombre': 'Consejo General del Val-de-Marne', 'pais': 'Francia',
                                                   'clasificacion': 'ESTATAL'},
    'Universidad de La Habana (Cuba)': 387,
    'Buró Sindical, Universidad de La Habana (Cuba)': {'nombre': 'Buró Sindical', 'padre': 387, 'pais': 'Cuba'},
    'Gobierno de Cuba': {'nombre': 'Gobierno de Cuba', 'pais': 'Cuba', 'clasificacion': 'FEDERAL'},
    'Universidad Autónoma de Baja California Sur': 214,
    'Instituto Nacional para el Federalismo y el Desarrollo Municipal (INAFED)': 145,
    'Instituto de Materiales y Reactivos (Cuba)': {'nombre': 'Instituto de Materiales y Reactivos', 'padre': 387,
                                                   'pais': 'Cuba'},
    'Comisión Europea': {'nombre': 'Comisión Europea', 'pais': 'Bélgica'},
    'Academia Mexicana de Ciencias': 293,
    'American Chemical Society': 941,
    'Consejo Nacional de Investigaciones Científicas y Técnicas (CONICET), Argentina': 252,
    'Environment for Development Initiative (EfD)': 943,
    'Sociedad Mexicana de Geografía y Estadística (SMGE)': 162,
    'Conference of Latin Americanist Geographers (CLAG)': 349,
    'Gobierno de México': {'nombre': 'Gobierno de México', 'pais': 'México', 'clasificacion': 'FEDERAL'},
    'Generalitat de Catalunya': 287, 'Universidad Complutense de Madrid': 64, 'FAO': 483,
}
#: Etiquetas de institución que significan «no se toca» o «vacía».
CONSERVAR, VACIA = 'conservar', None
INSTITUCION_ESPECIAL = {
    '(en cada registro)': VACIA, 'por confirmar': VACIA, 'por confirmar (Cuba)': VACIA,
    'por confirmar (el SIA anterior dice UNAM)': CONSERVAR,
}
CLASES_BECA = {'SECIHTI': 'SECIHTI', 'PAPIIT': 'PAPIIT', 'PAPIME': 'PAPIME', 'UNAM': 'UNAM',
               'IE_NAC': 'IE_NACIONAL', 'IE_INT': 'IE_INTERNACIONAL'}


def guardar(obj, motivo=MOTIVO):
    obj._change_reason = motivo[:100]
    obj.save()


def borrar(obj, motivo=MOTIVO):
    obj._change_reason = motivo[:100]
    obj.delete()


def tipo_distincion(nombre, actual):
    n = nombre.lower()
    T = Distincion.Tipo
    if n.startswith('programa de') or n.startswith('pei') or 'estímulos' in n:
        return T.ESTIMULO
    if n.startswith(('beca', 'james p.', 'carolyn')) or 'fellowship' in n or 'scholarship' in n:
        return T.BECA
    if n.startswith('medalla'):
        return T.MEDALLA
    if n.startswith(('diploma', 'certificado')):
        return T.DIPLOMA
    if n.startswith(('premio', 'concurso', 'best paper', 'ashden')):
        return T.PREMIO
    if n.startswith(('mención', 'reconocimiento', 'declaración', 'proyecto de éxito', 'profesor')):
        return T.RECONOCIMIENTO
    if n.startswith(('sistema', 'ingreso', 'investigador', 'international', 'distinción')):
        return T.DISTINCION
    return actual if actual in T.values else T.RECONOCIMIENTO


class Command(BaseCommand):
    help = 'Depura los catálogos Comisión, Cargo, Beca y Distinción. Sin --aplicar es un simulacro.'

    def add_arguments(self, parser):
        parser.add_argument('--mapeo', default='datos/depuracion/mapeo_catalogos.py')
        parser.add_argument('--aplicar', action='store_true', help='Guarda los cambios (si no, se revierten).')

    def handle(self, mapeo, aplicar=False, **options):
        if not Path(mapeo).exists():
            raise CommandError(f'No existe el mapeo {mapeo}')
        spec = importlib.util.spec_from_file_location('mapeo_catalogos', mapeo)
        self.m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.m)
        self.cuenta = Counter()
        self._instituciones = {}
        try:
            with transaction.atomic():
                self.preparar_comisiones()
                self.preparar_cargos()
                self.comisiones()
                self.cargos()
                self.becas()
                self.distinciones()
                self.ambitos()
                if not aplicar:
                    raise _Simulacro
        except _Simulacro:
            pass
        for clave, n in sorted(self.cuenta.items()):
            self.stdout.write(f'  {clave}: {n}')
        estado = 'aplicada' if aplicar else 'simulada (nada se guardó; usa --aplicar)'
        self.stdout.write(self.style.SUCCESS(f'Depuración {estado}.'))

    # ----------------------------------------------------------------------------------------------- utilidades
    def institucion(self, etiqueta):
        """Institucion de una etiqueta del mapeo (la crea si hace falta), o None."""
        from cities_light.models import Country

        if etiqueta in self._instituciones:
            return self._instituciones[etiqueta]
        spec = INSTITUCIONES[etiqueta]
        if isinstance(spec, int):
            obj = Institucion.objects.get(pk=spec)
        else:
            datos = dict(spec)
            pais = Country.objects.get(name=datos.pop('pais'))
            padre = datos.pop('padre', None)
            obj = Institucion.objects.filter(nombre=datos['nombre'], pais=pais, padre_id=padre).first()
            if obj is None:
                obj = Institucion(pais=pais, padre_id=padre, **datos)
                guardar(obj)
                self.cuenta['instituciones creadas'] += 1
        self._instituciones[etiqueta] = obj
        return obj

    def funcion(self, etiqueta):
        if not etiqueta:
            return F.INTEGRANTE
        etiqueta = etiqueta.removeprefix('Función: ')
        try:
            return FUNCIONES[etiqueta.lower()]
        except KeyError:
            raise CommandError(f'Función desconocida en el mapeo: {etiqueta!r}')

    @staticmethod
    def unir(*partes):
        return '; '.join(p for p in partes if p)[:255]

    # ----------------------------------------------------------------------------------------------- comisiones
    def comision(self, nombre):
        obj = Comision.objects.filter(nombre=nombre).first()
        seccion = self.m.CATALOGO_COMISION[nombre]
        ayuda = self.m.AYUDA.get(nombre, '')
        if obj is None:
            obj = Comision(nombre=nombre, seccion=seccion, ayuda=ayuda)
            guardar(obj)
            self.cuenta['comisiones: altas'] += 1
        elif (obj.seccion, obj.ayuda) != (seccion, ayuda):
            obj.seccion, obj.ayuda = seccion, ayuda
            guardar(obj)
        return obj

    def nueva_comision_institucional(self, origen, nombre, funcion, detalle, institucion, inicio, fin, usuario):
        comision = self.comision(nombre)
        obj = ComisionInstitucional(comision=comision, funcion=funcion, detalle=detalle, institucion=institucion,
                                    ambito=comision.ambito_sugerido, fecha_inicio=inicio, fecha_fin=fin,
                                    usuario=usuario)
        guardar(obj, f'{MOTIVO}: viene de {origen}')
        return obj

    def preparar_comisiones(self):
        m = self.m
        renombrar = {pk: v for pk, v in m.COMISION.items() if v[0] == 'renombrar'}
        for pk, (_, nombre, *_r) in renombrar.items():
            obj = Comision.objects.get(pk=pk)
            obj.nombre = f'__depuracion_{pk}'  # Evita choques de nombre único mientras se renombra.
            guardar(obj)
        for pk, (_, nombre, *_r) in renombrar.items():
            obj = Comision.objects.get(pk=pk)
            obj.nombre, obj.seccion, obj.ayuda = nombre, m.CATALOGO_COMISION[nombre], m.AYUDA.get(nombre, '')
            guardar(obj)
            self.cuenta['comisiones: renombradas'] += 1
        for nombre in m.CATALOGO_COMISION:
            self.comision(nombre)

    def comisiones(self):
        m = self.m
        for pk, (accion, destino, funcion, detalle, _nota) in m.COMISION.items():
            registros = list(ComisionInstitucional.objects.filter(comision_id=pk))
            if accion in ('renombrar', 'fusionar'):
                comision = self.comision(destino)
                for r in registros:
                    r.comision, r.funcion = comision, self.funcion(funcion)
                    r.detalle = self.unir(r.detalle, detalle)
                    guardar(r)
                    self.cuenta['comisiones: registros actualizados'] += 1
            elif accion == 'mover':
                for r in registros:
                    self.mover_comision(r, destino, detalle)
            elif accion == 'reclasificar':
                for r in registros:
                    self.reclasificar(r)
            if accion != 'renombrar':
                obj = Comision.objects.filter(pk=pk).first()
                if obj and not ComisionInstitucional.objects.filter(comision=obj).exists():
                    borrar(obj)
                    self.cuenta[f'comisiones: entradas quitadas ({accion})'] += 1

    def mover_comision(self, r, destino, detalle):
        m = self.m
        if destino == m.PUBLICACIONES:
            self.a_arbitraje_publicacion(r, detalle)
        elif destino == m.PROYECTOS:
            self.a_otra_comision(r, 5, detalle or 'Arbitraje de proyecto de investigación')
        elif destino.startswith('Labores directivas'):
            cargo_nombre = destino[destino.index('(') + 1:-1]
            cargo = self.cargo(cargo_nombre)
            nuevo = LaborDirectivaCoordinacion(cargo=cargo, detalle=detalle, institucion=r.institucion,
                                               fecha_inicio=r.fecha_inicio, fecha_fin=r.fecha_fin, usuario=r.usuario)
            guardar(nuevo, f'{MOTIVO}: era la comisión «{r.comision.nombre[:40]}»')
            borrar(r, f'{MOTIVO}: pasó a labores directivas')
            self.cuenta['comisiones → labores directivas'] += 1
        else:
            raise CommandError(f'Destino desconocido: {destino}')

    def a_arbitraje_publicacion(self, r, detalle):
        T = ArbitrajePublicacion.Tipo
        if detalle.startswith('Libro: '):
            tipo, revista, obra = T.LIBRO, None, detalle.removeprefix('Libro: ')
        else:
            nombre = detalle.removeprefix('Revista ').removeprefix('Artículo: ')
            revista = self.revista(nombre, r) if detalle.startswith('Revista ') else self.revista_de(r)
            tipo, obra = T.ARTICULO, '' if detalle.startswith('Revista ') else nombre
        nuevo = ArbitrajePublicacion(tipo=tipo, revista=revista, obra=obra, fecha_dictamen=r.fecha_inicio,
                                     institucion=None if revista else r.institucion, usuario=r.usuario)
        guardar(nuevo, f'{MOTIVO}: era la comisión «{r.comision.nombre[:40]}»')
        borrar(r, f'{MOTIVO}: pasó a arbitraje de publicaciones')
        self.cuenta['comisiones → arbitraje de publicaciones'] += 1

    REVISTAS = {'Geografía y Desarrollo': 165, 'Investigaciones Geográficas': 196,
                'International Forestry Review': 80}

    def revista(self, nombre, r):
        if nombre in self.REVISTAS:
            return Revista.objects.get(pk=self.REVISTAS[nombre])
        obj = Revista.objects.filter(nombre__iexact=nombre).first()
        if obj is None:
            obj = Revista(nombre=nombre, pais=r.institucion.pais)
            guardar(obj)
            self.cuenta['revistas creadas'] += 1
        return obj

    def revista_de(self, r):
        """La revista que el SIA anterior capturó como institución («Revista Geomorphology (Elsevier…)»)."""
        nombre = r.institucion.nombre if r.institucion else ''
        for prefijo in ('Revista ',):
            nombre = nombre.removeprefix(prefijo)
        nombre = nombre.split(' (')[0].strip()
        return self.revista(nombre, r) if nombre else None

    def a_otra_comision(self, r, tipo_pk, descripcion):
        nuevo = OtraComision(tipo=TipoComision.objects.get(pk=tipo_pk), descripcion=descripcion[:255],
                             institucion=r.institucion, fecha_inicio=r.fecha_inicio, fecha_fin=r.fecha_fin,
                             usuario=r.usuario)
        guardar(nuevo, f'{MOTIVO}: era la comisión «{r.comision.nombre[:40]}»')
        borrar(r, f'{MOTIVO}: pasó a otras comisiones de arbitraje')
        self.cuenta['comisiones → arbitraje de proyectos y otros'] += 1

    def reclasificar(self, r):
        m = self.m
        destino, funcion, detalle, _certeza, motivo = m.COMISION_REGISTROS[r.pk]
        if destino == m.ARB_PROY:
            self.a_otra_comision(r, 5, self.unir('Arbitraje de proyecto', detalle))
        elif destino == m.ARB_PUB:
            if detalle.startswith('Revista '):
                self.a_arbitraje_publicacion(r, detalle)
            else:  # Sin revista identificada: queda como arbitraje sin precisar.
                self.a_otra_comision(r, 1, self.unir('Arbitraje (sin precisar si artículo, tesis o proyecto)', detalle))
        elif destino == m.EVENTO:
            # Moderar en un evento no es ponencia ni póster: queda en el comité del evento, como moderador.
            r.comision, r.funcion, r.detalle = self.comision(m.COMITE_CIENTIFICO), F.COMENTARISTA, detalle
            guardar(r, f'{MOTIVO}: {motivo}')
            self.cuenta['comisiones: registros reclasificados'] += 1
        else:
            r.comision, r.funcion = self.comision(destino), self.funcion(funcion)
            r.detalle = self.unir(r.detalle, detalle)
            guardar(r, f'{MOTIVO}: {motivo}')
            self.cuenta['comisiones: registros reclasificados'] += 1

    def ambitos(self):
        for r in ComisionInstitucional.objects.select_related('comision'):
            if r.ambito != r.comision.ambito_sugerido:
                r.ambito = r.comision.ambito_sugerido
                guardar(r, f'{MOTIVO}: ámbito según la sección de la comisión')
                self.cuenta['comisiones: ámbito corregido'] += 1

    # ----------------------------------------------------------------------------------------------- cargos
    def cargo(self, nombre):
        tipo = self.m.CATALOGO_CARGO[nombre]
        obj = Cargo.objects.filter(nombre=nombre, tipo=tipo).first()
        if obj is None:
            obj = Cargo(nombre=nombre, tipo=tipo)
            guardar(obj)
            self.cuenta['cargos: altas'] += 1
        return obj

    def preparar_cargos(self):
        m = self.m
        renombrar = {pk: v for pk, v in m.CARGO.items() if v[0] == 'renombrar'}
        for pk in renombrar:
            obj = Cargo.objects.get(pk=pk)
            obj.nombre = f'__depuracion_{pk}'
            guardar(obj)
        for pk, (_, nombre, *_r) in renombrar.items():
            obj = Cargo.objects.get(pk=pk)
            obj.nombre, obj.tipo = nombre, m.CATALOGO_CARGO[nombre]
            guardar(obj)
            self.cuenta['cargos: renombrados'] += 1
        for nombre in m.CATALOGO_CARGO:
            self.cargo(nombre)

    def cargos(self):
        m = self.m
        for pk, (accion, destino, _f, detalle, nota) in m.CARGO.items():
            registros = list(LaborDirectivaCoordinacion.objects.filter(cargo_id=pk))
            if accion in ('renombrar', 'fusionar'):
                cargo = self.cargo(destino)
                for r in registros:
                    r.cargo, r.detalle = cargo, self.unir(r.detalle, detalle)
                    guardar(r)
                    self.cuenta['cargos: registros actualizados'] += 1
            elif accion == 'mover' and destino == m.COMISIONES:
                nombre, _, especifico = detalle.partition(': ')
                for r in registros:
                    self.nueva_comision_institucional(f'cargo «{r.cargo.nombre[:40]}»', nombre,
                                                      self.funcion(nota if nota.startswith('Función') else ''),
                                                      especifico, r.institucion, r.fecha_inicio, r.fecha_fin,
                                                      r.usuario)
                    borrar(r, f'{MOTIVO}: pasó a comisiones institucionales')
                    self.cuenta['cargos → comisiones institucionales'] += 1
            elif accion == 'mover' and destino == 'Servicios y asesorías externas':
                for r in registros:
                    nuevo = ServicioAsesoriaExterna(nombre=detalle, institucion=r.institucion,
                                                    fecha_inicio=r.fecha_inicio, fecha_fin=r.fecha_fin,
                                                    usuario=r.usuario)
                    guardar(nuevo, f'{MOTIVO}: era el cargo «{r.cargo.nombre[:40]}»')
                    borrar(r, f'{MOTIVO}: pasó a servicios y asesorías externas')
                    self.cuenta['cargos → servicios externos'] += 1
            elif accion == 'mover':  # «Catálogo de comisiones (X)»: sin registros; la comisión ya existe.
                if registros:
                    raise CommandError(f'El cargo {pk} tiene registros y el mapeo lo manda al catálogo de comisiones')
            elif accion == 'eliminar' and registros:
                raise CommandError(f'El cargo {pk} tiene registros: no se puede eliminar')
            if accion != 'renombrar':
                obj = Cargo.objects.filter(pk=pk).first()
                if obj and not LaborDirectivaCoordinacion.objects.filter(cargo=obj).exists():
                    borrar(obj)
                    self.cuenta[f'cargos: entradas quitadas ({accion})'] += 1

    # ----------------------------------------------------------------------------------------------- becas
    def beca(self, nombre, etiqueta):
        institucion = self.institucion(etiqueta)
        obj = Beca.objects.filter(nombre=nombre, institucion=institucion).first()
        if obj is None:
            obj = Beca(nombre=nombre, institucion=institucion)
            self.cuenta['becas: altas'] += 1
        obj.clase = CLASES_BECA[self.m.CATALOGO_BECA[(nombre, etiqueta)]]
        obj.ayuda = self.m.AYUDA_BECA.get(nombre, '')
        guardar(obj)
        return obj

    @staticmethod
    def modalidad(r, beca):
        M = ModalidadBeca
        if isinstance(r, SupervisionPostdoctoral):
            return M.POSDOCTORAL
        if beca.nombre == 'Beca Mixta':
            return M.MOVILIDAD
        if isinstance(r, AsesoriaEstudiante) and r.tipo == AsesoriaEstudiante.Tipo.SERVICIO_SOCIAL:
            return M.SERVICIO_SOCIAL
        return {'LICENCIATURA': M.LICENCIATURA, 'MAESTRIA': M.MAESTRIA, 'DOCTORADO': M.DOCTORADO}.get(r.nivel, '')

    def registros_beca(self, pk):
        for modelo in (AsesoriaEstudiante, DireccionTesis, SupervisionPostdoctoral):
            yield from modelo.objects.filter(beca_id=pk)

    def destino_dividido(self, r):
        m = self.m
        if isinstance(r, SupervisionPostdoctoral):
            return m.B_POSDOC_SECIHTI
        if isinstance(r, AsesoriaEstudiante) and r.nivel == 'LICENCIATURA':
            return m.B_PROYECTO
        return m.B_NACIONAL

    def becas(self):
        m = self.m
        for pk, (accion, destino, _f, _d, _n) in m.BECA.items():  # Renombrar primero (nombre + institución únicos).
            if accion == 'renombrar':
                obj = Beca.objects.get(pk=pk)
                obj.nombre = f'__depuracion_{pk}'
                guardar(obj)
        for pk, (accion, destino, _f, _d, _n) in m.BECA.items():
            if accion == 'renombrar':
                nombre, etiqueta = destino
                obj = Beca.objects.get(pk=pk)
                obj.nombre, obj.institucion = nombre, self.institucion(etiqueta)
                guardar(obj)
                self.cuenta['becas: renombradas'] += 1
        for nombre, etiqueta in m.CATALOGO_BECA:
            self.beca(nombre, etiqueta)

        for pk, (accion, destino, _f, detalle, _n) in m.BECA.items():
            for r in list(self.registros_beca(pk)):
                if accion == 'dividir':
                    beca = self.beca(self.destino_dividido(r), 'SECIHTI')
                else:
                    beca = self.beca(*destino)
                r.beca = beca
                r.detalle_beca = self.unir(r.detalle_beca, detalle)
                r.modalidad_beca = r.modalidad_beca or self.modalidad(r, beca)
                guardar(r)
                self.cuenta['becas: registros actualizados'] += 1
            if accion != 'renombrar':
                obj = Beca.objects.filter(pk=pk).first()
                if obj and not any(True for _ in self.registros_beca(pk)):
                    borrar(obj)
                    self.cuenta['becas: entradas fusionadas'] += 1

    # ----------------------------------------------------------------------------------------------- distinciones
    def institucion_distincion(self, obj, nombre):
        etiqueta = self.m.INSTITUCION_DISTINCION[nombre]
        especial = INSTITUCION_ESPECIAL.get(etiqueta, etiqueta)
        if especial == CONSERVAR:
            return obj.institucion if obj else None
        return self.institucion(especial) if especial else None

    def distincion(self, nombre):
        obj = Distincion.objects.filter(nombre=nombre).first()
        if obj is None:
            obj = Distincion(nombre=nombre, tipo=tipo_distincion(nombre, ''))
            self.cuenta['distinciones: altas'] += 1
        obj.institucion = self.institucion_distincion(obj, nombre)
        obj.tipo = tipo_distincion(nombre, obj.tipo)
        obj.ayuda = self.m.AYUDA_DISTINCION.get(nombre, '')
        guardar(obj)
        return obj

    def registros_distincion(self, pk):
        yield from DistincionAcademico.objects.filter(distincion_id=pk)
        yield from DistincionAlumno.objects.filter(distincion_id=pk)
        yield from DireccionTesis.objects.filter(reconocimiento_id=pk)

    def distinciones(self):
        m = self.m
        for pk, (accion, *_r) in m.DISTINCION.items():
            if accion == 'renombrar':
                obj = Distincion.objects.get(pk=pk)
                obj.nombre = f'__depuracion_{pk}'
                guardar(obj)
        for pk, (accion, nombre, *_r) in m.DISTINCION.items():
            if accion in ('renombrar', 'conservar'):
                obj = Distincion.objects.get(pk=pk)
                obj.nombre = nombre
                obj.institucion = self.institucion_distincion(obj, nombre)
                obj.tipo, obj.ayuda = tipo_distincion(nombre, obj.tipo), m.AYUDA_DISTINCION.get(nombre, '')
                guardar(obj)
                self.cuenta['distinciones: renombradas o conservadas'] += 1
        for nombre in m.ALTAS_DISTINCION:
            self.distincion(nombre)

        for pk, (accion, destino, _f, detalle, nota) in m.DISTINCION.items():
            registros = list(self.registros_distincion(pk))
            if accion in ('renombrar', 'fusionar', 'conservar'):
                distincion = Distincion.objects.get(nombre=destino)
                institucion = self.institucion(nota.removeprefix('Institución: ').split(';')[0]) \
                    if nota.startswith('Institución: ') else None
                for r in registros:
                    if isinstance(r, DireccionTesis):
                        r.reconocimiento = distincion
                        r.detalle_reconocimiento = self.unir(r.detalle_reconocimiento, detalle)
                    else:
                        r.distincion, r.detalle = distincion, self.unir(r.detalle, detalle)
                        r.institucion = r.institucion or institucion
                    guardar(r)
                    self.cuenta['distinciones: registros actualizados'] += 1
            elif accion == 'mover':
                for r in registros:
                    self.mover_distincion(r, destino, detalle)
            elif accion == 'revisar':
                obj = Distincion.objects.get(pk=pk)
                if obj.tipo not in Distincion.Tipo.values:
                    obj.tipo = Distincion.Tipo.RECONOCIMIENTO
                    guardar(obj)
                continue
            if accion == 'fusionar' or accion == 'mover':
                obj = Distincion.objects.filter(pk=pk).first()
                if obj and not any(True for _ in self.registros_distincion(pk)):
                    borrar(obj)
                    self.cuenta[f'distinciones: entradas quitadas ({accion})'] += 1

    def mover_distincion(self, r, destino, detalle):
        m = self.m
        if destino == 'Cursos de especialización':
            # Los tres cursos ya están capturados como cursos de especialización: la distinción era un duplicado.
            borrar(r, f'{MOTIVO}: duplicado de un curso de especialización ya capturado')
            self.cuenta['distinciones: duplicados de cursos borrados'] += 1
        elif destino == 'Sociedades científicas':
            local = 'Grospierres' in detalle
            nuevo = SociedadCientifica(nombre=detalle, tipo=SociedadCientifica.Tipo.INVITACION,
                                       ambito='LOCAL' if local else 'INTERNACIONAL', fecha_inicio=r.fecha,
                                       usuario=r.usuario)
            guardar(nuevo, f'{MOTIVO}: era la distinción «{r.distincion.nombre[:40]}»')
            borrar(r, f'{MOTIVO}: pasó a sociedades científicas')
            self.cuenta['distinciones → sociedades científicas'] += 1
        elif destino.startswith('Comisiones institucionales ('):
            nombre = destino[len('Comisiones institucionales ('):-1]
            funcion = F.EVALUADOR if nombre == m.JURADO_PREMIO else F.VOCAL
            self.nueva_comision_institucional(f'distinción «{r.distincion.nombre[:40]}»', nombre, funcion, detalle,
                                              None, r.fecha, r.fecha, r.usuario)
            borrar(r, f'{MOTIVO}: pasó a comisiones institucionales')
            self.cuenta['distinciones → comisiones institucionales'] += 1
        else:
            raise CommandError(f'Destino desconocido: {destino}')


class _Simulacro(Exception):
    pass
