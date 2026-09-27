"""Convierte un volcado (`dumpdata`) del SIA legacy (Django 2.0) a un fixture del esquema actual.

    python manage.py convertir_legacy datos/legacy/sia_legacy.json datos/fixtures/sia.json
    python manage.py loaddata datos/fixtures/sia.json

El volcado de entrada puede combinar varios archivos de `dumpdata`; si un modelo aparece más de
una vez, se usa su última aparición.
"""

import json
import re
from collections import Counter, defaultdict
from itertools import count
from pathlib import Path

from django.core.management.base import BaseCommand

from nucleo.models import correo_provisional

REGISTRO_LEGACY = '2019-06-27T00:00:00Z'
TIPOS_CUENTA = {'INVESTIGADOR', 'TECNICO', 'POSTDOCTORADO', 'ADMINISTRATIVO'}
STATUS_PUBLICACION = ['ENVIADO', 'ACEPTADO', 'EN_PRENSA', 'PUBLICADO']
FECHA_STATUS = {'ENVIADO': 'fecha_enviado', 'ACEPTADO': 'fecha_aceptado', 'EN_PRENSA': 'fecha_enprensa',
                'PUBLICADO': 'fecha_publicado'}


def txt(valor):
    return '' if valor is None else str(valor).strip()


def clave(texto):
    return re.sub(r'\s+', ' ', txt(texto)).lower()


def opcion(valor, validas, defecto=''):
    return valor if valor in validas else defecto


def fecha_hora(valor):
    if not valor:
        return REGISTRO_LEGACY
    return valor if 'T' in valor else f'{valor}T00:00:00Z'


class Conversor:
    def __init__(self, objetos):
        self.legacy = defaultdict(dict)
        for obj in objetos:
            self.legacy[obj['model']][obj['pk']] = obj['fields']
        self.salida = []
        self.pks = defaultdict(set)
        self.contadores = {}
        self.avisos = Counter()
        self.convertidos = set()
        # Índices para reutilizar registros creados a partir de texto libre.
        self.por_nombre = defaultdict(dict)

    # -- utilidades ---------------------------------------------------------

    def fuente(self, modelo):
        self.convertidos.add(modelo)
        return self.legacy.get(modelo, {})

    def agregar(self, modelo, pk, campos):
        if pk in self.pks[modelo]:
            raise ValueError(f'pk duplicada {modelo}:{pk}')
        self.pks[modelo].add(pk)
        self.salida.append({'model': modelo, 'pk': pk, 'fields': campos})
        return pk

    def nuevo_pk(self, modelo):
        if modelo not in self.contadores:
            self.contadores[modelo] = count(max(self.pks[modelo], default=0) + 1)
        pk = next(self.contadores[modelo])
        while pk in self.pks[modelo]:
            pk = next(self.contadores[modelo])
        return pk

    def aviso(self, mensaje):
        self.avisos[mensaje] += 1

    def verificable(self, verificado=True, usuario=None, creado=None, actualizado=None):
        return {'verificado': bool(verificado), 'creado_por': usuario if usuario in self.cuentas else None,
                'creado': fecha_hora(creado), 'actualizado': fecha_hora(actualizado or creado)}

    def persona(self, pk):
        return pk if pk in self.pks['nucleo.persona'] else None

    def cuenta(self, pk):
        return pk if pk in self.cuentas else None

    def participantes(self, modelo, campo_padre, padre, personas, extra=None):
        vistos = set()
        for orden, persona in enumerate(personas, start=1):
            if persona in vistos or self.persona(persona) is None:
                continue
            vistos.add(persona)
            self.agregar(modelo, self.nuevo_pk(modelo),
                         {campo_padre: padre, 'persona': persona, 'orden': orden, **(extra or {})})

    def publicacion(self, f):
        """Estado editorial y fechas; la `fecha` genérica legacy se asigna a la etapa del estado."""
        fechas = {campo: f.get(campo) for campo in FECHA_STATUS.values()}
        status = f.get('status')
        if status not in STATUS_PUBLICACION:
            status = next((s for s in reversed(STATUS_PUBLICACION) if fechas[FECHA_STATUS[s]]), 'PUBLICADO')
        if f.get('fecha') and not fechas[FECHA_STATUS[status]]:
            fechas[FECHA_STATUS[status]] = f['fecha']
        return {'status': status, **fechas}

    def catalogo_por_nombre(self, modelo, nombre, llave=(), **campos):
        """Busca por nombre (sin distinguir mayúsculas) o crea el registro en el catálogo."""
        indice = self.por_nombre[modelo]
        llave = (clave(nombre), llave)
        if llave not in indice:
            pk = self.nuevo_pk(modelo)
            self.agregar(modelo, pk, {'nombre': re.sub(r'\s+', ' ', txt(nombre)), **campos,
                                      **self.verificable(False)})
            indice[llave] = pk
        return indice[llave]

    def indexar(self, modelo, pk, nombre, llave=()):
        self.por_nombre[modelo].setdefault((clave(nombre), llave), pk)

    def institucion(self, f):
        """Institución del registro: la nueva (`institucion`) o la derivada de `institucion2`/`dependencia`."""
        if f.get('institucion') in self.pks['nucleo.institucion']:
            return f['institucion']
        dependencia = self.legacy['nucleo.dependencia'].get(f.get('dependencia'))
        pk_institucion = f.get('institucion2') or (dependencia or {}).get('institucion_dependencia')
        institucion = self.legacy['nucleo.institucion'].get(pk_institucion)
        if not institucion:
            return None
        nombre = institucion['nombre_institucion']
        if dependencia and clave(dependencia['nombre_dependencia']) != clave(nombre):
            nombre = f"{dependencia['nombre_dependencia']}, {nombre}"
        ciudad = txt((dependencia or {}).get('ciudad_text_dependencia'))
        llave = (clave(nombre), institucion['pais_institucion'], clave(ciudad))
        indice = self.por_nombre['institucion']
        if llave not in indice:
            pk = self.nuevo_pk('nucleo.institucion')
            self.agregar('nucleo.institucion', pk, {
                'nombre': nombre[:255], 'pais': institucion['pais_institucion'], 'ciudad': ciudad,
                'clasificacion': opcion(institucion['clasificacion_institucion'], self.CLASIFICACIONES),
                'pertenece_unam': 'UNAM' in nombre.upper(), 'subsistema_unam': '',
                **self.verificable(False)})
            indice[llave] = pk
        return indice[llave]

    CLASIFICACIONES = {'ACADEMICA', 'FEDERAL', 'ESTATAL', 'MUNICIPAL', 'PRIVADA', 'NO_LUCRATIVA'}

    def programa(self, f, nivel):
        for campo, modelo in (('programa_licenciatura', 'lic'), ('licenciatura', 'lic'),
                              ('programa_maestria', 'mae'), ('maestria', 'mae'),
                              ('programa_doctorado', 'doc'), ('doctorado', 'doc')):
            if f.get(campo) in self.mapa_programas[modelo]:
                return self.mapa_programas[modelo][f[campo]]
        if txt(f.get('programa')) and nivel:
            return self.catalogo_por_nombre('nucleo.programaacademico', f['programa'], llave=(nivel,), nivel=nivel,
                                            area_conocimiento=None)
        return None

    def proyecto(self, pk):
        return pk if pk in self.pks['investigacion.proyectoinvestigacion'] else None

    # -- conversión ---------------------------------------------------------

    def convertir(self):
        self.personas_y_usuarios()
        self.catalogos()
        self.investigacion()
        self.formacion_academica()
        self.experiencia_profesional()
        self.compromiso_institucional()
        self.difusion_cientifica()
        self.divulgacion_cientifica()
        self.vinculacion()
        self.movilidad_academica()
        self.docencia()
        self.formacion_recursos_humanos()
        self.desarrollo_tecnologico()
        self.distinciones()
        for modelo in sorted(set(self.legacy) - self.convertidos):
            self.aviso(f'Modelo legacy sin equivalente, se omitió: {modelo} ({len(self.legacy[modelo])})')
        return self.salida

    def personas_y_usuarios(self):
        for pk, f in self.fuente('nucleo.pais').items():
            self.agregar('nucleo.pais', pk, {
                'nombre': f['pais_nombre'], 'nombre_extendido': txt(f['pais_nombre_extendido']),
                'codigo': f['pais_codigo'].upper(),
                'zona': opcion(f.get('pais_zona'), {'AMERICA_NORTE', 'AMERICA_CENTRAL', 'AMERICA_SUR', 'ANTILLAS',
                                                    'EUROPA', 'ASIA', 'EURASIA', 'AFRICA', 'OCEANIA'})})

        usuarios = self.fuente('nucleo.user')
        # Son cuentas quienes entraron al sistema, el personal académico y los dueños de algún registro.
        duenos = {f['usuario'] for modelo, objs in self.legacy.items() for f in objs.values()
                  if not modelo.startswith('nucleo.') and isinstance(f.get('usuario'), int)}
        self.cuentas = {pk for pk, f in usuarios.items()
                        if f['last_login'] or f['is_staff'] or f['is_superuser'] or f['tipo'] in TIPOS_CUENTA
                        or pk in duenos}
        ciudades = self.fuente('nucleo.ciudad')
        correos_usados = set()
        for pk, f in usuarios.items():
            if pk in self.cuentas:
                password = f['password'] if re.match(r'^[a-z0-9_]+\$', f['password'] or '') else '!'
                if password == '!':
                    self.aviso('Cuenta sin contraseña válida (deberá restablecerla)')
                domicilio = '\n'.join(x for x in (txt(f['direccion']), txt(f['direccion_continuacion']),
                                                  txt(ciudades.get(f['ciudad'], {}).get('nombre'))) if x)
                correo = txt(f['email']).lower()
                if not correo or correo in correos_usados:
                    self.aviso('Cuenta sin correo o con correo repetido (se le asignó uno provisional)')
                    correo = correo_provisional(f['username'])
                correos_usados.add(correo)
                self.agregar('nucleo.user', pk, {
                    'email': correo, 'password': password, 'first_name': txt(f['first_name']),
                    'last_name': txt(f['last_name']), 'is_active': f['is_active'],
                    'is_staff': True, 'is_superuser': f['is_superuser'], 'last_login': f['last_login'],
                    'date_joined': fecha_hora(f['date_joined']),
                    'groups': [] if f['is_superuser'] else [['Investigadores']], 'user_permissions': [],
                    'tipo': opcion(f['tipo'], TIPOS_CUENTA | {'OTRO'}, 'OTRO'), 'grado': '',
                    'semblanza': txt(f['descripcion']), 'fecha_nacimiento': f['fecha_nacimiento'],
                    'genero': opcion(f['genero'], {'M', 'F'}), 'pais_origen': f['pais_origen'],
                    'rfc': txt(f['rfc'])[:13], 'curp': txt(f['curp'])[:18], 'domicilio': domicilio,
                    'telefono': txt(f['telefono']) or txt(f['celular']), 'url': txt(f['url']),
                    'sni': str(f['sni']) if f.get('sni') in (1, 2, 3) else '', 'pride': opcion(f['pride'], {'A', 'B', 'C', 'D'}),
                    'ingreso_unam': f['ingreso_unam'], 'ingreso_entidad': f['ingreso_entidad'],
                    'egreso_entidad': f['egreso_entidad'], 'ultimo_contrato': f['ultimo_contrato'],
                    'avatar': txt(f['avatar'])})
            self.agregar('nucleo.persona', pk, {
                'nombre': txt(f['first_name']) or f['username'], 'apellidos': txt(f['last_name']),
                'email': txt(f['email']), 'usuario': pk if pk in self.cuentas else None,
                **self.verificable(True, creado=f['date_joined'])})

    def catalogos(self):
        for pk, f in self.fuente('nucleo.institucionsimple').items():
            self.agregar('nucleo.institucion', pk, {
                'nombre': f['institucion_nombre'], 'pais': f['institucion_pais'],
                'ciudad': txt(f['institucion_ciudad']),
                'clasificacion': opcion(f['institucion_clasificacion'], self.CLASIFICACIONES),
                'pertenece_unam': f['institucion_perteneceunam'],
                'subsistema_unam': txt(f['institucion_subsistemaunam']),
                **self.verificable(f['institucion_regverificado'], f['institucion_regusuario'],
                                   f['institucion_regfechacreado'], f['institucion_regfechaactualizado'])})
            self.por_nombre['institucion'][(clave(f['institucion_nombre']), f['institucion_pais'],
                                            clave(f['institucion_ciudad']))] = pk
        self.fuente('nucleo.institucion')
        self.fuente('nucleo.dependencia')

        for pk, f in self.fuente('nucleo.areaconocimiento').items():
            self.agregar('nucleo.areaconocimiento', pk, {
                'nombre': f['areaconocimiento_nombre'],
                'categoria': opcion(f['areaconocimiento_categoria'], {'LSBM', 'PHYS', 'TECH', 'ARTH', 'SS'}, 'OTRA')})

        self.mapa_programas = {}
        for sufijo, nivel in (('lic', 'LICENCIATURA'), ('mae', 'MAESTRIA'), ('doc', 'DOCTORADO')):
            nombre_legacy = {'lic': 'licenciatura', 'mae': 'maestria', 'doc': 'doctorado'}[sufijo]
            prefijo = f'programa{nombre_legacy}_'
            self.mapa_programas[sufijo] = {}
            for pk_legacy, f in self.fuente(f'nucleo.programa{nombre_legacy}').items():
                pk = self.catalogo_existente('nucleo.programaacademico', f[prefijo + 'nombre'], {
                    'nombre': txt(f[prefijo + 'nombre']), 'nivel': nivel,
                    'area_conocimiento': f[prefijo + 'areaconocimiento'],
                    **self.verificable(f[prefijo + 'regverificado'], f[prefijo + 'regusuario'],
                                       f[prefijo + 'regfechacreado'], f[prefijo + 'regfechaactualizado'])},
                    llave=(nivel,))
                self.mapa_programas[sufijo][pk_legacy] = pk

        for modelo_legacy, modelo in (('nucleo.asignatura', 'nucleo.asignatura'), ('nucleo.beca', 'nucleo.beca')):
            for pk, f in self.fuente(modelo_legacy).items():
                self.agregar(modelo, pk, {'nombre': txt(f['nombre']), **self.verificable()})
                self.indexar(modelo, pk, f['nombre'])

        for pk, f in self.fuente('nucleo.cargo').items():
            self.agregar('nucleo.cargo', pk, {
                'nombre': txt(f['nombre']),
                'tipo': opcion(f['tipo_cargo'], {'ACADEMICO', 'ADMINISTRATIVO', 'DIRECTIVO'}, 'OTRO'),
                **self.verificable()})
            self.indexar('nucleo.cargo', pk, f['nombre'])

        for pk, f in self.fuente('nucleo.nombramiento').items():
            self.agregar('nucleo.nombramiento', pk, {'nombre': f['nombre'], 'clave': f['clave'],
                                                     'descripcion': txt(f['descripcion'])})

        for pk, f in self.fuente('nucleo.distincion').items():
            self.agregar('nucleo.distincion', pk, {
                'nombre': txt(f['nombre']), 'tipo': f['tipo'], 'institucion': self.institucion(f),
                'ambito': opcion(f['ambito'], {'INSTITUCIONAL', 'REGIONAL', 'NACIONAL', 'INTERNACIONAL'}),
                **self.verificable()})
            self.indexar('nucleo.distincion', pk, f['nombre'])

        for pk, f in self.fuente('nucleo.tipoevento').items():
            self.agregar('nucleo.tipoevento', pk, {'nombre': f['tipoevento_nombre']})

        self.eventos()

        for pk, f in self.fuente('nucleo.indice').items():
            self.agregar('nucleo.indice', pk, {'nombre': f['nombre']})

        self.revistas()

        ciudades = self.legacy['nucleo.ciudad']
        for pk, f in self.fuente('nucleo.mediodivulgacion').items():
            self.agregar('nucleo.mediodivulgacion', pk, {
                'nombre': f['nombre_medio'], 'tipo': opcion(f['tipo'], {'PERIODICO', 'RADIO', 'TV', 'INTERNET'}, 'OTRO'),
                'canal': txt(f['canal']), 'pais': f['pais'], 'ciudad': txt(ciudades.get(f['ciudad'], {}).get('nombre')),
                **self.verificable()})

        self.libros()

        for modelo in ('nucleo.zonapais', 'nucleo.estado', 'nucleo.financiamiento', 'nucleo.tipocurso',
                       'nucleo.editorial', 'nucleo.coleccion', 'nucleo.areaespecialidad', 'nucleo.impactosocial',
                       'nucleo.metodologia', 'nucleo.reconocimiento', 'nucleo.problemanacionalconacyt'):
            # Catálogos sin uso en el esquema actual; algunos se consultan durante la conversión.
            self.convertidos.add(modelo)

    def catalogo_existente(self, modelo, nombre, campos, llave=()):
        """Agrega un registro de catálogo legacy fusionando duplicados por nombre."""
        indice = self.por_nombre[modelo]
        k = (clave(nombre), llave)
        if k in indice:
            return indice[k]
        pk = self.nuevo_pk(modelo)
        self.agregar(modelo, pk, campos)
        indice[k] = pk
        return pk

    def eventos(self):
        ciudades = self.legacy['nucleo.ciudad']
        self.mapa_eventos = {'nucleo': {}, 'difusion': {}, 'divulgacion': {}}
        indice = {}

        def agregar_evento(origen, pk_legacy, campos):
            llave = (clave(campos['nombre']), campos['fecha_inicio'])
            verificado = campos.pop('_verificado', True)
            if llave not in indice:
                pk = pk_legacy if origen == 'nucleo' else self.nuevo_pk('nucleo.evento')
                self.agregar('nucleo.evento', pk, {**campos, **self.verificable(verificado)})
                indice[llave] = pk
            self.mapa_eventos[origen][pk_legacy] = indice[llave]

        for pk, f in self.fuente('nucleo.evento').items():
            agregar_evento('nucleo', pk, {
                'nombre': txt(f['nombre']), 'tipo': f['tipo'], 'descripcion': txt(f['descripcion']),
                'fecha_inicio': f['fecha_inicio'], 'fecha_fin': f['fecha_fin'], 'pais': f['pais'],
                'ciudad': txt(ciudades.get(f['ciudad'], {}).get('nombre')), 'ambito': '',
                'numero_ponentes': None, 'numero_asistentes': None})
        for origen, prefijo in (('difusion', 'eventodifusion_'), ('divulgacion', 'eventodivulgacion_')):
            for pk, f in self.fuente(f'{origen}_cientifica.evento{origen}').items():
                agregar_evento(origen, pk, {
                    'nombre': txt(f[prefijo + 'nombre']), 'tipo': f[prefijo + 'tipo'], 'descripcion': '',
                    'fecha_inicio': f[prefijo + 'fecha_inicio'], 'fecha_fin': f[prefijo + 'fecha_fin'],
                    'pais': f[prefijo + 'pais'], 'ciudad': txt(f[prefijo + 'ciudad']),
                    'ambito': opcion(f[prefijo + 'ambito'], {'NACIONAL', 'INTERNACIONAL'}),
                    'numero_ponentes': f[prefijo + 'numeroponentes'],
                    'numero_asistentes': f[prefijo + 'numeroasistentes'],
                    '_verificado': f.get(prefijo + 'regverificado', True)})

    def revistas(self):
        self.mapa_revistas_divulgacion = {}
        nombres = {}
        for pk, f in self.fuente('nucleo.revista').items():
            self.agregar('nucleo.revista', pk, {
                'nombre': txt(f['revista_nombre']), 'nombre_abreviado': txt(f['revista_nombreabreviadowos']),
                'tipo': 'CIENTIFICA', 'pais': f['revista_pais'], 'indices': f['revista_indices'],
                'issn_impreso': txt(f['revista_issn_impreso']), 'issn_electronico': txt(f['revista_issn_online']),
                **self.verificable(f['revista_regverificado'], f['revista_regusuario'], f['revista_regfechacreado'],
                                   f['revista_regfechaactualizado'])})
            nombres[clave(f['revista_nombre'])] = pk
        for pk_legacy, f in self.fuente('nucleo.revistadivulgacion').items():
            nombre = clave(f['revistadivulgacion_nombre'])
            if nombre not in nombres:
                nombres[nombre] = self.agregar('nucleo.revista', self.nuevo_pk('nucleo.revista'), {
                    'nombre': txt(f['revistadivulgacion_nombre']), 'nombre_abreviado': '', 'tipo': 'DIVULGACION',
                    'pais': f['revistadivulgacion_pais'], 'indices': [],
                    'issn_impreso': txt(f['revistadivulgacion_issnimpreso']), 'issn_electronico': '',
                    **self.verificable(f['revistadivulgacion_regverificado'], f['revistadivulgacion_regusuario'],
                                       f['revistadivulgacion_regfechacreado'],
                                       f['revistadivulgacion_regfechaactualizado'])})
            self.mapa_revistas_divulgacion[pk_legacy] = nombres[nombre]

    def libros(self):
        for pk, f in self.fuente('nucleo.libro').items():
            self.agregar('nucleo.libro', pk, {
                'titulo': txt(f['nombre']), 'tipo': f['tipo'],
                'agradecimientos': [p for p in f['agradecimientos'] if self.persona(p)],
                'editorial': txt(f['editorial_text']), 'pais': f['pais'], 'ciudad': txt(f['ciudad_text']),
                'coleccion': txt(f['coleccion_text']), 'volumen': txt(f['volumen']),
                'numero_edicion': f['numero_edicion'] or 1, 'numero_paginas': f['numero_paginas'] or None,
                'isbn': txt(f['isbn']), 'url': txt(f['url']), 'arbitrado_pares': f['arbitrado_pares'],
                **self.publicacion(f), **self.verificable(False)})
            orden = 0
            vistos = set()
            for rol, campo in (('AUTOR', 'autores'), ('EDITOR', 'editores'), ('COORDINADOR', 'coordinadores'),
                               ('COMPILADOR', 'compiladores')):
                for persona in f[campo]:
                    if (persona, rol) in vistos or not self.persona(persona):
                        continue
                    vistos.add((persona, rol))
                    orden += 1
                    self.agregar('nucleo.libroparticipante', self.nuevo_pk('nucleo.libroparticipante'),
                                 {'libro': pk, 'persona': persona, 'rol': rol, 'orden': orden})

    def investigacion(self):
        for pk, f in self.fuente('investigacion.objetivodesarrollosostenible').items():
            self.agregar('investigacion.objetivodesarrollosostenible', pk,
                         {'numero': pk, 'nombre': f['objetivodesarrollosostenible_nombre']})

        for pk, f in self.fuente('investigacion.proyectoinvestigacion').items():
            if clave(f['nombre']) == 'ninguno':
                continue  # Marcador legacy para "sin proyecto": las referencias quedan vacías.
            financiamiento = opcion(f['tipo_financiamiento'],
                                    {'CONACYT', 'PAPIIT', 'PAPIME', 'EXTRAORDINARIOS', 'SIN_RECURSOS'})
            self.agregar('investigacion.proyectoinvestigacion', pk, {
                'nombre': txt(f['nombre']), 'descripcion': txt(f['descripcion']),
                'es_permanente': f['es_permanente'], 'fecha_inicio': f['fecha_inicio'], 'fecha_fin': f['fecha_fin'],
                'institucion': self.institucion(f),
                'participantes': [p for p in f['participantes'] if self.persona(p)],
                'participantes_externos': txt(f['participantes_externos_text']),
                'status': opcion(f['status'], {'NUEVO', 'EN_PROCESO', 'CONCLUIDO'}, 'EN_PROCESO'),
                'clasificacion': txt(f['clasificacion']), 'organizacion': txt(f['organizacion']),
                'modalidad': txt(f['modalidad']), 'tematica_genero': f['tematica_genero'],
                'objetivos_ods': f['objetivos2030'], 'impacto_social': txt(f['impacto_social_text']),
                'financiamiento': financiamiento,
                'financiamiento_clave': txt(f['financiamiento_conacyt_clave'] or f['financiamiento_papiit']
                                            or f['financiamiento_papime']),
                'financiamiento_convocatoria': txt(f['financiamiento_conacyt_convocatoria']),
                'financiamiento_institucion': f['financiamiento_extraordinario'] or f['financiamiento_sin_recurso_ciga'],
                'num_alumnos_licenciatura': f['num_alumnos_licenciatura'] or 0,
                'num_alumnos_maestria': f['num_alumnos_maestria'] or 0,
                'num_alumnos_doctorado': f['num_alumnos_doctorado'] or 0})
            self.participantes('investigacion.proyectoresponsable', 'proyecto', pk, f['responsables'])

        for pk, f in self.fuente('investigacion.articulocientifico').items():
            self.agregar('investigacion.articulocientifico', pk, {
                'titulo': txt(f['titulo']), 'revista': f['revista'], 'volumen': txt(f['volumen']),
                'numero': txt(f['numero']), 'pagina_inicio': f['pagina_inicio'], 'pagina_fin': f['pagina_fin'],
                'doi': txt(f['id_doi']), 'url': txt(f['url']), 'solo_electronico': f['solo_electronico'],
                'factor_impacto': f['factor_impacto'], 'proyecto': self.proyecto(f['proyecto']),
                'alumnos': [p for p in f['alumnos'] if self.persona(p)],
                'agradecimientos': [p for p in f['agradecimientos'] if self.persona(p)], **self.publicacion(f)})
            self.participantes('investigacion.articulocientificoautor', 'articulo', pk, f['autores'])

        for pk, f in self.fuente('investigacion.capitulolibroinvestigacion').items():
            self.agregar('investigacion.capitulolibroinvestigacion', pk, {
                'titulo': txt(f['titulo']), 'libro': f['libro'], 'pagina_inicio': f['pagina_inicio'],
                'pagina_fin': f['pagina_fin']})
            self.participantes('investigacion.capitulolibroinvestigacionautor', 'capitulo', pk, f['autores'])

        for pk, f in self.fuente('investigacion.mapaarbitrado').items():
            self.agregar('investigacion.mapaarbitrado', pk, {
                'titulo': txt(f['titulo']), 'publicacion': txt(f['publicacion']), 'pais': f['pais'],
                'ciudad': txt(f['ciudad_text']), 'numero_paginas': f['numero_paginas'] or 1,
                'proyecto': self.proyecto(f['proyecto']),
                'agradecimientos': [p for p in f['agradecimientos'] if self.persona(p)], **self.publicacion(f)})
            self.participantes('investigacion.mapaarbitradoautor', 'mapa', pk, f['autores'])

        mapa_actividades = {}
        for origen, tipo in (('investigacion', 'INVESTIGACION'), ('servicio', 'SERVICIO')):
            for pk_legacy, f in self.fuente(f'investigacion.actividadapoyotecnico{origen}').items():
                pk = self.nuevo_pk('investigacion.actividadapoyotecnico')
                self.agregar('investigacion.actividadapoyotecnico', pk, {
                    'nombre': f[f'actividadapoyotecnico{origen}_nombre'], 'tipo': tipo, 'orden': f['orden']})
                mapa_actividades[(origen, pk_legacy)] = pk
            for f in self.fuente(f'investigacion.apoyotecnico{origen}').values():
                self.agregar('investigacion.apoyotecnico', self.nuevo_pk('investigacion.apoyotecnico'), {
                    'actividad': mapa_actividades[(origen, f['actividad'])],
                    'actividad_otra': txt(f['actividad_otra']), 'fecha_inicio': f['fecha_inicio'],
                    'fecha_fin': f['fecha_fin'], 'proyecto': self.proyecto(f['proyecto']), 'usuario': f['usuario']})

    def formacion_academica(self):
        for pk, f in self.fuente('formacion_academica.cursoespecializacion').items():
            self.agregar('formacion_academica.cursoespecializacion', pk, {
                'nombre': txt(f['nombre']), 'tipo': opcion(f['tipo'], {'CURSO', 'DIPLOMADO', 'CERTIFICACION'}, 'OTRO'),
                'horas': f['horas'], 'modalidad': opcion(f['modalidad'], {'PRESENCIAL', 'EN_LINEA', 'MIXTO'}, 'OTRO'),
                'institucion': f['institucion'], 'fecha_inicio': f['fecha_inicio'], 'fecha_fin': f['fecha_fin'],
                'usuario': f['usuario']})
        for nivel, modelo in (('LICENCIATURA', 'licenciatura'), ('MAESTRIA', 'maestria'), ('DOCTORADO', 'doctorado')):
            for f in self.fuente(f'formacion_academica.{modelo}').values():
                self.agregar('formacion_academica.grado', self.nuevo_pk('formacion_academica.grado'), {
                    'nivel': nivel, 'titulo_obtenido': txt(f['titulo_obtenido']), 'institucion': f['institucion'],
                    'titulo_tesis': txt(f['titulo_tesis']), 'fecha_grado': f['fecha_grado'],
                    'distincion_obtenida': txt(f['distincion_obtenida']), 'usuario': f['usuario']})
        for pk, f in self.fuente('formacion_academica.postdoctorado').items():
            self.agregar('formacion_academica.postdoctorado', pk, {
                'titulo_proyecto': txt(f['titulo_proyecto']), 'tutor': self.persona(f['tutor']),
                'institucion': self.institucion(f), 'proyecto': self.proyecto(f['proyecto']),
                'financiamiento': opcion(f['entidad_financiamiento'], {'CONACYT', 'SRE', 'DGAPA', 'OTRA'}),
                'financiamiento_otro': txt(f['otra_entidad_financiamiento']), 'fecha_inicio': f['fecha_inicio'],
                'fecha_fin': f['fecha_fin'], 'usuario': f['usuario']})

    def experiencia_profesional(self):
        for pk, f in self.fuente('experiencia_profesional.experienciaprofesional').items():
            self.agregar('experiencia_profesional.experienciaprofesional', pk, {
                'cargo': txt(f['cargo_text']) or 'Sin cargo', 'nombramiento': f['nombramiento'],
                'institucion': f['institucion'], 'descripcion': '', 'fecha_inicio': f['fecha_inicio'],
                'fecha_fin': f['fecha_fin'], 'usuario': f['usuario']})
        vistos = set()
        for pk, f in self.fuente('experiencia_profesional.lineainvestigacion').items():
            llave = (f['usuario'], clave(f['linea_investigacion']))
            if llave in vistos:
                self.aviso('Línea de investigación duplicada para el mismo usuario (se omitió)')
                continue
            vistos.add(llave)
            self.agregar('experiencia_profesional.lineainvestigacion', pk, {
                'nombre': txt(f['linea_investigacion']), 'descripcion': txt(f['descripcion']),
                'institucion': f['institucion'], 'fecha_inicio': f['fecha_inicio'], 'usuario': f['usuario']})
        for pk, f in self.fuente('experiencia_profesional.capacidadpotencialidad').items():
            self.agregar('experiencia_profesional.capacidadpotencialidad', pk, {
                'nombre': txt(f['nombre']), 'descripcion': txt(f['descripcion']), 'fecha_inicio': f['fecha_inicio'],
                'usuario': f['usuario']})

    def compromiso_institucional(self):
        for pk, f in self.fuente('compromiso_institucional.comisioninstitucional').items():
            self.agregar('compromiso_institucional.comision', pk,
                         {'nombre': txt(f['comisioninstitucional_nombre']), **self.verificable()})
            self.indexar('compromiso_institucional.comision', pk, f['comisioninstitucional_nombre'])
        for pk, f in self.fuente('compromiso_institucional.actividadapoyo').items():
            self.agregar('compromiso_institucional.actividadapoyo', pk,
                         {'nombre': txt(f['nombre']), 'descripcion': txt(f['descripcion'])})
        self.fuente('compromiso_institucional.representacion')

        for pk, f in self.fuente('compromiso_institucional.labordirectivacoordinacion').items():
            cargo = f['cargo'] or self.catalogo_por_nombre('nucleo.cargo', f['tipo_cargo'], tipo='OTRO')
            self.agregar('compromiso_institucional.labordirectivacoordinacion', pk, {
                'cargo': cargo, 'institucion': f['institucion'], 'fecha_inicio': f['fecha_inicio'],
                'fecha_fin': f['fecha_fin'], 'usuario': f['usuario']})

        for pk, f in self.fuente('compromiso_institucional.representacionorganocolegiadounam').items():
            self.agregar('compromiso_institucional.representacionorganocolegiado', pk, {
                'tipo': opcion(f['tipo_representacion'], {'DENTRO', 'REPRESENTACION'}, 'DENTRO'),
                'organo': opcion(f['representacion_dentro_unam'], {'PRIDE', 'CAACS', 'CONSEJO_INTERNO',
                                                                   'COMISION_DICTAMINADORA', 'COMISION_EVALUADORA',
                                                                   'OTRA'}),
                'organo_descripcion': txt(f['representacion_dentro_unam_otra'] or f['representacion_fuera_unam']),
                'institucion': f['institucion'] or f['institucion_dentro_unam'] or f['institucion_fuera_unam'],
                'fecha_inicio': f['fecha_inicio'], 'fecha_fin': f['fecha_fin'], 'usuario': f['usuario']})

        for pk, f in self.fuente('compromiso_institucional.comisioninstitucionalciga').items():
            comision = f['comision_academica'] or self.catalogo_por_nombre('compromiso_institucional.comision',
                                                                           f['tipo_comision'])
            self.agregar('compromiso_institucional.comisioninstitucional', pk, {
                'comision': comision, 'ambito': opcion(f['tipo_institucion'], {'INTERIOR', 'EXTERIOR'}, 'INTERIOR'),
                'institucion': self.institucion(f), 'fecha_inicio': f['fecha_inicio'], 'fecha_fin': f['fecha_fin'],
                'usuario': f['usuario']})

        for tipo, modelo in (('TECNICO', 'apoyotecnico'), ('OTRA', 'apoyootraactividad')):
            for f in self.fuente(f'compromiso_institucional.{modelo}').values():
                self.agregar('compromiso_institucional.apoyoinstitucional',
                             self.nuevo_pk('compromiso_institucional.apoyoinstitucional'), {
                                 'tipo': tipo, 'actividad': f['actividad_apoyo'], 'descripcion': txt(f['descripcion']),
                                 'institucion': self.institucion(f), 'fecha_inicio': f['fecha_inicio'],
                                 'fecha_fin': f['fecha_fin'], 'usuario': f['usuario']})

    def difusion_cientifica(self):
        for pk, f in self.fuente('difusion_cientifica.memoriainextenso').items():
            self.agregar('difusion_cientifica.memoriainextenso', pk, {
                'titulo': txt(f['nombre']), 'evento': txt(f['evento_text']), 'lugar': txt(f['lugar']),
                'fecha': f['fecha'], 'pais': f['pais'], 'ciudad': txt(f['ciudad']), 'institucion': f['institucion'],
                'pagina_inicio': f['pagina_inicio'], 'pagina_fin': f['pagina_fin'], 'isbn': txt(f['isbn'])})
            self.participantes('difusion_cientifica.memoriainextensoautor', 'memoria', pk, f['autores'])
        for pk, f in self.fuente('difusion_cientifica.organizacioneventoacademico').items():
            self.agregar('difusion_cientifica.organizacioneventoacademico', pk, {
                'evento': self.mapa_eventos['difusion'][f['evento']],
                'tipo_participacion': opcion(f['tipo_participacion'], self.TIPOS_ORGANIZACION, 'OTRO'),
                'tipo_participacion_otro': txt(f['tipo_participacion_otro']), 'usuario': f['usuario']})
        for pk, f in self.fuente('difusion_cientifica.participacioneventoacademico').items():
            self.agregar('difusion_cientifica.participacioneventoacademico', pk, {
                'tipo': opcion(f['tipo'], {'PONENCIA', 'POSTER'}, 'PONENCIA'), 'titulo': txt(f['titulo']),
                'evento': txt(f['evento']), 'lugar': txt(f['lugar_evento']), 'ciudad': txt(f['ciudad']),
                'pais': f['pais'], 'institucion': f['institucion'], 'fecha': f['fecha'],
                'ambito': opcion(f['ambito'], {'NACIONAL', 'INTERNACIONAL'}, 'NACIONAL'),
                'por_invitacion': f['por_invitacion'], 'ponencia_magistral': f['ponencia_magistral']})
            self.participantes('difusion_cientifica.participacioneventoacademicoautor', 'participacion', pk,
                               f['autores'])
        if self.legacy.get('difusion_cientifica.resena'):
            self.convertidos.add('difusion_cientifica.resena')
            self.aviso(f"Reseñas omitidas: el modelo se eliminó del código legacy "
                       f"({len(self.legacy['difusion_cientifica.resena'])})")

    TIPOS_ORGANIZACION = {'COORDINADOR', 'COMITE_ORGANIZADOR', 'APOYO_TECNICO', 'OTRO'}

    def divulgacion_cientifica(self):
        for pk, f in self.fuente('divulgacion_cientifica.articulodivulgacion').items():
            revista = self.mapa_revistas_divulgacion.get(f.get('revista_divulgacion')) or f.get('revista')
            self.agregar('divulgacion_cientifica.articulodivulgacion', pk, {
                'titulo': txt(f['titulo']), 'revista': revista, 'volumen': txt(f.get('volumen')),
                'numero': txt(f['numero']), 'pagina_inicio': f['pagina_inicio'], 'pagina_fin': f['pagina_fin'],
                'url': txt(f['url']), 'solo_electronico': f['solo_electronico'],
                'agradecimientos': [p for p in f['agradecimientos'] if self.persona(p)], **self.publicacion(f)})
            self.participantes('divulgacion_cientifica.articulodivulgacionautor', 'articulo', pk, f['autores'])
        for pk, f in self.fuente('divulgacion_cientifica.capitulolibrodivulgacion').items():
            self.agregar('divulgacion_cientifica.capitulolibrodivulgacion', pk, {
                'titulo': txt(f['titulo']), 'libro': f['libro'], 'pagina_inicio': f['pagina_inicio'],
                'pagina_fin': f['pagina_fin']})
            autores = f['autores'] or ([f['usuario']] if f.get('usuario') else [])
            self.participantes('divulgacion_cientifica.capitulolibrodivulgacionautor', 'capitulo', pk, autores)
        for pk, f in self.fuente('divulgacion_cientifica.organizacioneventodivulgacion').items():
            evento = (self.mapa_eventos['divulgacion'].get(f['evento'])
                      or self.mapa_eventos['nucleo'].get(f['evento2']))
            self.agregar('divulgacion_cientifica.organizacioneventodivulgacion', pk, {
                'evento': evento, 'tipo_participacion': opcion(f['tipo_participacion'], self.TIPOS_ORGANIZACION, 'OTRO'),
                'tipo_participacion_otro': txt(f['tipo_participacion_otro']), 'usuario': f['usuario']})
        for pk, f in self.fuente('divulgacion_cientifica.participacioneventodivulgacion').items():
            self.agregar('divulgacion_cientifica.participacioneventodivulgacion', pk, {
                'tipo': opcion(f['tipo'], {'PONENCIA', 'POSTER'}, 'PONENCIA'), 'titulo': txt(f['titulo']),
                'evento': self.mapa_eventos['nucleo'][f['evento']], 'institucion': f['institucion'],
                'fecha': f['fecha'], 'ambito': opcion(f['ambito'], {'NACIONAL', 'INTERNACIONAL'}, 'NACIONAL'),
                'por_invitacion': f['por_invitacion'], 'ponencia_magistral': f['ponencia_magistral']})
            self.participantes('divulgacion_cientifica.participacioneventodivulgacionautor', 'participacion', pk,
                               f['autores'])
        for pk, f in self.fuente('divulgacion_cientifica.programaradiotelevisioninternet').items():
            self.agregar('divulgacion_cientifica.programamedio', pk, {
                'tema': txt(f['tema']), 'fecha': f['fecha'], 'descripcion': txt(f['descripcion']),
                'actividad': opcion(f['actividad'], {'PRODUCCION', 'PARTICIPACION', 'ENTREVISTA'}, 'OTRA'),
                'medio': f['medio_divulgacion'], 'usuario': f['usuario']})

    def vinculacion(self):
        for pk, f in self.fuente('vinculacion.arbitrajepublicacionacademica').items():
            self.agregar('vinculacion.arbitrajepublicacion', pk, {
                'tipo': opcion(f['tipo'], {'ARTICULO', 'LIBRO', 'CAPITULO_LIBRO'}, 'ARTICULO'),
                'revista': f['revista'], 'obra': txt(f['libro'] or f['capitulo_libro']),
                'fecha_dictamen': f['fecha_dictamen'], 'institucion': f['institucion'], 'usuario': f['usuario']})
        for pk, f in self.fuente('vinculacion.comisionvinculacion').items():
            self.agregar('vinculacion.tipocomision', pk, {'nombre': f['comisionvinculacion_nombre'],
                                                          'orden': f['comisionvinculacion_orden']})
        for pk, f in self.fuente('vinculacion.otracomision').items():
            self.agregar('vinculacion.otracomision', pk, {
                'tipo': f['comision'], 'descripcion': txt(f['comision_otra']), 'institucion': f['institucion'],
                'fecha_inicio': f['fecha_inicio'], 'fecha_fin': f['fecha_fin'], 'usuario': f['usuario']})
        for pk, f in self.fuente('vinculacion.redacademica').items():
            self.agregar('vinculacion.redacademica', pk, {
                'nombre': txt(f['nombre']), 'ambito': opcion(f['ambito'], {'LOCAL', 'REGIONAL', 'NACIONAL',
                                                                           'INTERNACIONAL'}, 'NACIONAL'),
                'objetivos': txt(f['objetivos']), 'fecha_constitucion': f['fecha_constitucion'],
                'fecha_fin': f['fecha_fin'], 'instituciones': f['instituciones'],
                'proyecto': self.proyecto(f['proyecto']),
                'participantes': [p for p in f['participantes'] if self.persona(p)]})
        for pk, f in self.fuente('vinculacion.conveniootraentidad').items():
            self.agregar('vinculacion.convenio', pk, {
                'nombre': txt(f['nombre']), 'ambito': opcion(f['ambito'], {'NACIONAL', 'INTERNACIONAL'}, 'NACIONAL'),
                'objetivos': txt(f['objetivos']), 'instituciones': f['instituciones'],
                'es_renovacion': f['es_renovacion'], 'financiamiento': txt(f['financiamiento_text']),
                'proyecto': self.proyecto(f['proyecto']), 'fecha_inicio': f['fecha_inicio'],
                'fecha_fin': f['fecha_fin'], 'participantes': [p for p in f['participantes'] if self.persona(p)]})
        for pk, f in self.fuente('vinculacion.servicioasesoriaexterna').items():
            self.agregar('vinculacion.servicioasesoriaexterna', pk, {
                'nombre': txt(f['nombre_servicio']), 'descripcion': txt(f['descripcion']),
                'institucion': f['institucion'], 'financiamiento': txt(f['financiamiento_text']),
                'fecha_inicio': f['fecha_inicio'], 'fecha_fin': f['fecha_fin'], 'usuario': f['usuario']})

    def movilidad_academica(self):
        proyectos = {clave(f['nombre']): pk for pk, f in self.legacy['investigacion.proyectoinvestigacion'].items()
                     if pk in self.pks['investigacion.proyectoinvestigacion']}
        financiamientos = self.legacy['nucleo.financiamiento']
        personas = self.legacy['nucleo.user']
        modelo = 'movilidad_academica.movilidadacademica'
        financiamientos_validos = {'PROGRAMAS_UNAM', 'POR_PROYECTO', 'PRESUPUESTO_OPERATIVO'}

        for f in self.fuente('movilidad_academica.movilidadacademica').values():
            academico = personas.get(f['academico'], {})
            actividades = [txt(f['actividades']), txt(f['descripcion'])]
            if f['financiamiento'] in financiamientos:
                actividades.append(f"Financiamiento: {financiamientos[f['financiamiento']]['nombre']}")
            self.agregar(modelo, self.nuevo_pk(modelo), {
                'tipo': opcion(f['tipo'], {'INVITACION', 'ESTANCIA', 'SABATICO'}, 'ESTANCIA'),
                'academico': f"{txt(academico.get('first_name'))} {txt(academico.get('last_name'))}".strip(),
                'institucion': self.institucion(f), 'actividades': '\n\n'.join(a for a in actividades if a),
                'fecha_inicio': f['fecha_inicio'], 'fecha_fin': f['fecha_fin'],
                'intercambio_unam': f['intercambio_unam'], 'financiamiento': '',
                'redes_academicas': f['redes_academicas'], 'proyecto': self.proyecto(f['proyecto_investigacion']),
                'usuario': f['usuario']})

        for tipo, legacy, campo in (('INVITACION', 'invitadomovilidad', 'invitado'),
                                    ('ESTANCIA', 'estanciaacademica', 'anfitrion'),
                                    ('SABATICO', 'sabaticomovilidad', 'anfitrion')):
            for f in self.fuente(f'movilidad_academica.{legacy}').values():
                actividades = txt(f['actividades'])
                proyecto = proyectos.get(clave(f['proyecto']))
                if txt(f['proyecto']) and not proyecto:
                    actividades += f"\n\nProyecto: {txt(f['proyecto'])}"
                self.agregar(modelo, self.nuevo_pk(modelo), {
                    'tipo': tipo, 'academico': txt(f[campo]), 'institucion': self.institucion(f),
                    'actividades': actividades, 'fecha_inicio': f['fecha_inicio'], 'fecha_fin': f['fecha_fin'],
                    'intercambio_unam': f.get('intercambio_unam', False),
                    'financiamiento': opcion(f['financiamiento'], financiamientos_validos),
                    'redes_academicas': f['redes_academicas'], 'proyecto': proyecto, 'usuario': f['usuario']})

    def docencia(self):
        tipos_curso = {pk: clave(f['nombre']) for pk, f in self.legacy['nucleo.tipocurso'].items()}
        modalidades = {'PRESENCIAL', 'EN_LINEA', 'MIXTO'}

        def asignatura(f):
            if f.get('asignatura') in self.pks['nucleo.asignatura']:
                return f['asignatura']
            nombre = txt(f.get('asignatura_text')) or 'Sin nombre'
            return self.catalogo_por_nombre('nucleo.asignatura', nombre)

        for pk, f in self.fuente('docencia.cursodocenciaescolarizado').items():
            self.agregar('docencia.cursoescolarizado', pk, {
                'nivel': f['nivel'], 'programa': self.programa(f, f['nivel']), 'asignatura': asignatura(f),
                'modalidad': opcion(f['modalidad'], modalidades, 'OTRO'),
                'nombramiento': opcion(f['nombramiento'], {'TITULAR', 'COLABORADOR'}, 'TITULAR'),
                'institucion': self.institucion(f), 'periodo_academico': txt(f['periodo_academico']),
                'total_horas': f['total_horas'], 'fecha_inicio': f['fecha_inicio'], 'fecha_fin': f['fecha_fin'],
                'usuario': f['usuario']})

        for pk, f in self.fuente('docencia.cursodocenciaextracurricular').items():
            tipo = f.get('tipo_curso') or ''
            otro = txt(f.get('tipocurso_otro') or f.get('otro_tipo'))
            if tipo not in {'CURSO', 'DIPLOMADO', 'TALLER', 'SEMINARIO'}:
                nombre_tipo = tipos_curso.get(f.get('tipo'), '')
                tipo = next((t for t in ('CURSO', 'DIPLOMADO', 'TALLER', 'SEMINARIO') if t.lower() in nombre_tipo),
                            'OTRO')
                if tipo == 'OTRO' and not otro:
                    otro = nombre_tipo
            self.agregar('docencia.cursoextracurricular', pk, {
                'asignatura': asignatura(f), 'tipo': tipo, 'tipo_otro': otro,
                'clasificacion': opcion(f['clasificacion'], {'APOYO_POSGRADO', 'CAPACITACION'}),
                'modalidad': opcion(f['modalidad'], modalidades, 'OTRO'), 'institucion': self.institucion(f),
                'periodo_academico': txt(f['periodo_academico']), 'total_horas': f['total_horas'],
                'fecha_inicio': f['fecha_inicio'], 'fecha_fin': f['fecha_fin'], 'usuario': f['usuario']})

        for pk, f in self.fuente('docencia.articulodocencia').items():
            self.agregar('docencia.articulodocencia', pk, {
                'titulo': txt(f['titulo']), 'pagina_inicio': f['pagina_inicio'], 'pagina_fin': f['pagina_fin'],
                'url': txt(f['url']), 'solo_electronico': f['solo_electronico'],
                'alumnos': [p for p in f['alumnos'] if self.persona(p)],
                'agradecimientos': [p for p in f['agradecimientos'] if self.persona(p)], **self.publicacion(f)})
            self.participantes('docencia.articulodocenciaautor', 'articulo', pk, f['autores'])

        for pk, f in self.fuente('docencia.programaestudio').items():
            self.agregar('docencia.programaestudio', pk, {
                'nombre': txt(f['nombre']), 'descripcion': txt(f['descripcion']),
                'nivel': opcion(f['nivel'], {'LICENCIATURA', 'MAESTRIA', 'DOCTORADO'}, 'OTRO'), 'fecha': f['fecha'],
                'institucion': self.institucion(f), 'usuario': f['usuario']})

    def formacion_recursos_humanos(self):
        niveles = {'LICENCIATURA', 'MAESTRIA', 'DOCTORADO'}
        for pk, f in self.fuente('formacion_recursos_humanos.asesoriaestudiante').items():
            nivel = opcion(f['nivel_academico'], niveles, 'LICENCIATURA')
            self.agregar('formacion_recursos_humanos.asesoriaestudiante', pk, {
                'asesorado': f['asesorado'], 'tipo': f['tipo'], 'nivel': nivel, 'programa': self.programa(f, nivel),
                'beca': f['beca'], 'proyecto': self.proyecto(f['proyecto']), 'institucion': self.institucion(f),
                'periodo_academico': txt(f['periodo_academico']), 'fecha_inicio': f['fecha_inicio'],
                'fecha_fin': f['fecha_fin'], 'usuario': f['usuario']})
        for pk, f in self.fuente('formacion_recursos_humanos.supervisioninvestigadorpostdoctoral').items():
            self.agregar('formacion_recursos_humanos.supervisionpostdoctoral', pk, {
                'investigador': f['investigador'], 'titulo_proyecto': txt(f['titulo_proyecto']),
                'institucion': self.institucion(f), 'proyecto': self.proyecto(f['proyecto']), 'beca': f['beca'],
                'fecha_inicio': f['fecha_inicio'], 'fecha_fin': f['fecha_fin'], 'usuario': f['usuario']})
        for pk, f in self.fuente('formacion_recursos_humanos.desarrollogrupoinvestigacioninterno').items():
            self.agregar('formacion_recursos_humanos.grupoinvestigacioninterno', pk, {
                'nombre': txt(f['nombre']), 'pais': f['pais'], 'fecha_inicio': f['fecha_inicio'],
                'fecha_fin': f['fecha_fin'], 'integrantes': [p for p in f['usuarios'] if self.persona(p)]})
        titulos = set()
        for pk, f in self.fuente('formacion_recursos_humanos.direcciontesis').items():
            if clave(f['titulo_tesis']) in titulos:
                self.aviso('Tesis con título duplicado (se omitió)')
                continue
            titulos.add(clave(f['titulo_tesis']))
            nivel = opcion(f['nivel_academico'], niveles, 'LICENCIATURA')
            self.agregar('formacion_recursos_humanos.direcciontesis', pk, {
                'titulo_tesis': txt(f['titulo_tesis']), 'nivel': nivel, 'programa': self.programa(f, nivel),
                'asesorado': f['asesorado'], 'status': opcion(f['status'], {'EN_PROCESO', 'TERMINADA'},
                                                              'TERMINADA' if f['fecha_examen'] else 'EN_PROCESO'),
                'fecha_inicio': f['fecha_inicio'], 'fecha_fin': f['fecha_fin'], 'fecha_examen': f['fecha_examen'],
                'institucion': self.institucion(f), 'beca': f['beca'], 'reconocimiento': f['reconocimiento'],
                'director': self.persona(f['director']), 'codirector': self.persona(f['codirector'])})
            self.participantes('formacion_recursos_humanos.direcciontesistutor', 'tesis', pk, f['tutores'])
        for pk, f in self.fuente('formacion_recursos_humanos.comitetutoral').items():
            nivel = opcion(f['nivel_academico'], niveles, 'DOCTORADO')
            self.agregar('formacion_recursos_humanos.comitetutoral', pk, {
                'estudiante': f['estudiante'], 'nivel': nivel, 'programa': self.programa(f, nivel),
                'titulo_tesis': txt(f['titulo_tesis']), 'institucion': self.institucion(f),
                'fecha_inicio': f['fecha_inicio'], 'fecha_fin': f['fecha_fin'], 'fecha_examen': f['fecha_examen']})
            self.participantes('formacion_recursos_humanos.comitetutoralmiembro', 'comite', pk, f['miembros_comite'])
        for pk, f in self.fuente('formacion_recursos_humanos.comitecandidaturadoctoral').items():
            self.agregar('formacion_recursos_humanos.comitecandidaturadoctoral', pk, {
                'candidato': f['candidato'], 'titulo_tesis': txt(f['titulo_tesis']),
                'programa': self.programa(f, 'DOCTORADO'), 'especialidad': txt(f['especialidad']),
                'institucion': self.institucion(f), 'fecha_defensa': f['fecha_defensa'],
                'director': self.persona(f['director']), 'codirector': self.persona(f['codirector']),
                'asesores': [p for p in f['asesores'] if self.persona(p)]})
            self.participantes('formacion_recursos_humanos.comitecandidaturamiembro', 'comite', pk,
                               f['miembros_comite'])

    def desarrollo_tecnologico(self):
        self.fuente('desarrollo_tecnologico.licencia')
        self.fuente('desarrollo_tecnologico.tipodesarrollo')
        for pk, f in self.fuente('desarrollo_tecnologico.desarrollotecnologico').items():
            self.agregar('desarrollo_tecnologico.desarrollotecnologico', pk, {
                'nombre': txt(f['nombre']), 'descripcion': txt(f['descripcion']), 'version': txt(f['version']),
                'patente': txt(f['patente']), 'licencia': txt(f['licencia_text']), 'url': txt(f['url']),
                'fecha': f['fecha'], 'proyecto': self.proyecto(f['proyecto'])})
            self.participantes('desarrollo_tecnologico.desarrollotecnologicoautor', 'desarrollo', pk, f['autores'])

    def distinciones(self):
        catalogo = {o['pk']: o['fields'] for o in self.salida if o['model'] == 'nucleo.distincion'}

        def distincion(f):
            pk = f['distincion'] or self.catalogo_por_nombre('nucleo.distincion', f['distincion_text'],
                                                             tipo=opcion(f['tipo'], self.TIPOS_DISTINCION, 'OTRO'))
            campos = catalogo.get(pk)
            if campos is not None:  # Completa el catálogo con los datos capturados en el registro.
                campos['institucion'] = campos['institucion'] or f.get('institucion')
                campos['ambito'] = campos['ambito'] or opcion(f.get('ambito'), {'INSTITUCIONAL', 'REGIONAL',
                                                                               'NACIONAL', 'INTERNACIONAL'})
            return pk

        for pk, f in self.fuente('distinciones.distincionacademico').items():
            self.agregar('distinciones.distincionacademico', pk,
                         {'distincion': distincion(f), 'fecha': f['fecha'], 'usuario': f['usuario']})
        for pk, f in self.fuente('distinciones.distincionalumno').items():
            self.agregar('distinciones.distincionalumno', pk, {
                'distincion': distincion(f), 'alumno': f['alumno'],
                'nivel': opcion(f['nivel_academico'], {'LICENCIATURA', 'MAESTRIA', 'DOCTORADO'}, 'LICENCIATURA'),
                'tutores': [p for p in f['tutores'] if self.persona(p)], 'fecha': f['fecha']})
        for pk, f in self.fuente('distinciones.participacioncomisionexpertos').items():
            self.agregar('distinciones.comisionexpertos', pk, {
                'nombre': txt(f['nombre']), 'descripcion': txt(f['descripcion']), 'institucion': self.institucion(f),
                'fecha_inicio': f['fecha_inicio'], 'fecha_fin': f['fecha_fin'], 'usuario': f['usuario']})
        for pk, f in self.fuente('distinciones.participacionsociedadcientifica').items():
            self.agregar('distinciones.sociedadcientifica', pk, {
                'nombre': txt(f['nombre']), 'descripcion': txt(f['descripcion']),
                'tipo': opcion(f['tipo'], {'INVITACION', 'ELECCION'}, 'INVITACION'),
                'ambito': opcion(f['ambito'], {'NACIONAL', 'INTERNACIONAL'}, 'NACIONAL'),
                'fecha_inicio': f['fecha_inicio'], 'fecha_fin': f['fecha_fin'], 'usuario': f['usuario']})
        self.fuente('distinciones.citapublicacion')

    TIPOS_DISTINCION = {'PREMIO', 'DISTINCION', 'RECONOCIMIENTO', 'MEDALLA', 'DIPLOMA', 'GUGGENHEIM',
                        'HONORIS_CAUSA', 'OTRO'}


class Command(BaseCommand):
    help = 'Convierte un volcado JSON del SIA legacy a un fixture del esquema actual.'

    def add_arguments(self, parser):
        parser.add_argument('entrada', nargs='?', default='datos/legacy/sia_legacy.json')
        parser.add_argument('salida', nargs='?', default='datos/fixtures/sia.json')

    def handle(self, entrada, salida, **options):
        objetos = json.loads(Path(entrada).read_text(encoding='utf-8'))
        conversor = Conversor(objetos)
        fixture = conversor.convertir()
        Path(salida).parent.mkdir(parents=True, exist_ok=True)
        Path(salida).write_text(json.dumps(fixture, ensure_ascii=False, indent=1), encoding='utf-8')

        conteo = Counter(obj['model'] for obj in fixture)
        for modelo, total in sorted(conteo.items()):
            self.stdout.write(f'  {modelo}: {total}')
        for aviso, veces in conversor.avisos.items():
            self.stdout.write(self.style.WARNING(f'  Aviso: {aviso} [{veces}]'))
        self.stdout.write(self.style.SUCCESS(f'{len(fixture)} objetos escritos en {salida}'))
