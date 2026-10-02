"""Cifras de las gráficas del informe anual, calculadas con los registros del SIA.

Cada función recibe el periodo del informe (julio a junio, p. ej. 2025-2026) y devuelve {etiqueta: valor}. Con ellas
se arman las gráficas y se comparan con las que se hicieron a mano (`REFERENCIA_2025_2026`).
"""

from collections import Counter, OrderedDict
from dataclasses import dataclass
from datetime import date
from statistics import mean

from django.db.models import Q

from .similitud import normalizar


@dataclass(frozen=True)
class Periodo:
    inicio: date
    fin: date
    anio_corte: int  # Año de la situación académica (corte de agosto) que corresponde al periodo.

    @classmethod
    def de(cls, texto):
        """'2025-2026' → del 1 de julio de 2025 al 30 de junio de 2026."""
        a, b = (int(x) for x in texto.split('-'))
        return cls(date(a, 7, 1), date(b, 6, 30), b)

    @property
    def nombre(self):
        return f'{self.inicio.year}-{self.fin.year}'

    def contiene(self, campo):
        return Q(**{f'{campo}__gte': self.inicio, f'{campo}__lte': self.fin})

    def vigente(self, inicio='fecha_inicio', fin='fecha_fin'):
        """Registros activos en algún momento del periodo."""
        return Q(**{f'{inicio}__lte': self.fin}) & (Q(**{f'{fin}__isnull': True}) | Q(**{f'{fin}__gte': self.inicio}))


def _nivel_corto(nombramiento):
    """'Investigador Titular B, Tiempo Completo' → 'Titular B'."""
    partes = nombramiento.nombre.split(',')[0].split()
    return ' '.join(partes[-2:])


def _es_investigador(nombramiento):
    return nombramiento.nombre.startswith('Investigador')


# --------------------------------------------------------------------------------------------------- planta
def planta(periodo):
    """Figura 6: planta académica por categoría, nivel y género (corte de agosto)."""
    from .models import SituacionAcademica, User

    situaciones = SituacionAcademica.objects.filter(anio=periodo.anio_corte, nombramiento__isnull=False) \
        .select_related('usuario', 'nombramiento')
    r = OrderedDict(total=0)
    for grupo, es_inv in (('Investigadores', True), ('Técnicos', False)):
        del_grupo = [s for s in situaciones if _es_investigador(s.nombramiento) == es_inv]
        r[grupo] = len(del_grupo)
        r['total'] += len(del_grupo)
        mujeres = sum(s.usuario.genero == User.Genero.FEMENINO for s in del_grupo)
        r[f'{grupo} · mujeres %'] = round(100 * mujeres / len(del_grupo)) if del_grupo else 0
        for nivel, n in sorted(Counter(_nivel_corto(s.nombramiento) for s in del_grupo).items()):
            r[f'{grupo} · {nivel}'] = n
    return r


def antiguedad(periodo):
    """Figura 7: años promedio en la entidad por categoría y nivel."""
    from .models import SituacionAcademica

    grupos = {}
    for s in SituacionAcademica.objects.filter(anio=periodo.anio_corte, nombramiento__isnull=False) \
            .select_related('usuario', 'nombramiento'):
        ingreso = s.usuario.ingreso_unam or s.usuario.ingreso_entidad  # Antigüedad académica en la UNAM.
        if ingreso is None:
            continue
        grupo = 'Investigadores' if _es_investigador(s.nombramiento) else 'Técnicos'
        grupos.setdefault(f'{grupo} · {_nivel_corto(s.nombramiento)}', []).append(periodo.anio_corte - ingreso.year)
    return OrderedDict((k, round(mean(v), 1)) for k, v in sorted(grupos.items()))


def contratos(periodo):
    """Figura 8: personal por tipo de contrato."""
    from .models import SituacionAcademica

    r = Counter()
    for s in SituacionAcademica.objects.filter(anio=periodo.anio_corte, nombramiento__isnull=False) \
            .select_related('nombramiento'):
        grupo = 'Investigadores' if _es_investigador(s.nombramiento) else 'Técnicos'
        r[f'{grupo} · {s.get_contrato_display() or "sin dato"}'] += 1
    return OrderedDict(sorted(r.items()))


def pride(periodo):
    """Figura 21: distribución por nivel PRIDE («B» incluye las equivalencias y PAIPA)."""
    from .models import SituacionAcademica as S

    r = Counter()
    for s in S.objects.filter(anio=periodo.anio_corte, nombramiento__isnull=False).select_related('nombramiento'):
        grupo = 'Investigadores' if _es_investigador(s.nombramiento) else 'Técnicos'
        nivel = 'B o equivalencia' if s.pride in ('A', 'B', S.Pride.EQUIVALENCIA) else s.pride or 'sin PRIDE'
        r[f'{grupo} · {nivel}'] += 1
    return OrderedDict(sorted(r.items()))


def snii(periodo):
    """Figura 22: académicos por nivel del SNII."""
    from .models import SituacionAcademica

    nombres = {'C': 'Candidato', 'I': 'Nivel I', 'II': 'Nivel II', 'III': 'Nivel III', 'E': 'Emérito'}
    r = Counter(nombres[s] for s in SituacionAcademica.objects.filter(anio=periodo.anio_corte)
                .exclude(sni='').values_list('sni', flat=True))
    return OrderedDict((n, r.get(n, 0)) for n in nombres.values())


# --------------------------------------------------------------------------------------------------- proyectos
def _proyectos(periodo):
    from investigacion.models import ProyectoInvestigacion as P

    # Los proyectos del SIA anterior sin fecha de término no cuentan como vigentes: solo los reportados desde 2023.
    return P.objects.filter(periodo.vigente()).filter(Q(fecha_fin__isnull=False) | Q(financiamiento_unam__gt='')
                                                      | Q(fecha_inicio__year__gte=2023))


def proyectos_financiamiento(periodo):
    """Figura 11: proyectos por instancia financiadora (solo los que administra la entidad)."""
    from investigacion.models import ProyectoInvestigacion as P

    r = Counter()
    for p in _proyectos(periodo).exclude(financiamiento_unam=P.FinanciamientoUNAM.FUERA).select_related(
            'financiamiento_institucion__pais'):
        if p.financiamiento == P.Financiamiento.EXTRAORDINARIOS:
            pais = getattr(getattr(p.financiamiento_institucion, 'pais', None), 'code2', 'MX')
            r['Ingr. Extr. Nac.' if pais == 'MX' else 'Ingr. Extr. Inter.'] += 1
        elif p.financiamiento != P.Financiamiento.SIN_RECURSOS:
            r[{'CONACYT': 'SECIHTI'}.get(p.financiamiento, p.financiamiento)] += 1
    return OrderedDict((k, r.get(k, 0)) for k in ('SECIHTI', 'PAPIIT', 'PAPIME', 'Ingr. Extr. Nac.', 'Ingr. Extr. Inter.'))


def proyectos_tipos(periodo):
    """Figura 12: proyectos por modalidad."""
    qs = _proyectos(periodo)
    r = OrderedDict(total=qs.count())
    for m, n in Counter(qs.values_list('modalidad', flat=True)).most_common():
        r[m.capitalize()] = n
    return r


def ods(periodo):
    """Figura 13: proyectos por objetivo de desarrollo sostenible."""
    from investigacion.models import ObjetivoDesarrolloSostenible

    ids = list(_proyectos(periodo).values_list('pk', flat=True))
    return OrderedDict((f'{o.numero}', o.proyectoinvestigacion_set.filter(pk__in=ids).count())
                       for o in ObjetivoDesarrolloSostenible.objects.all())


def prioridades(periodo):
    """Figura 14: proyectos por problema nacional prioritario."""
    from investigacion.models import ProyectoInvestigacion as P

    r = Counter(_proyectos(periodo).exclude(prioridad='').values_list('prioridad', flat=True))
    return OrderedDict((P.Prioridad(k).label, n) for k, n in r.most_common())


# --------------------------------------------------------------------------------------------------- publicaciones
def publicaciones(periodo):
    """Figura 15: productos publicados por tipo y origen (i: internacional, n: nacional)."""
    from investigacion.models import ArticuloCientifico, CapituloLibroInvestigacion
    from .models import Libro

    def origen(pais):
        return 'n' if pais.code2 == 'MX' else 'i'

    r = Counter()
    articulos = ArticuloCientifico.objects.filter(periodo.contiene('fecha_publicado')).select_related('revista__pais') \
        .prefetch_related('revista__indices')
    for a in articulos:
        indices = {i.nombre for i in a.revista.indices.all()}
        tipo = 'WOS/Scopus' if indices & {'Scopus', 'Web of Science: SCI/SSCI/SCI-EX'} else 'Otros índices'
        r[f'{tipo} ({origen(a.revista.pais)})'] += 1
    # Solo libros de la entidad: los que contienen un capítulo de alguien de la entidad no cuentan como libro.
    for libro in Libro.objects.filter(periodo.contiene('fecha_publicado'), tipo=Libro.Tipo.INVESTIGACION,
                                      libroparticipante__persona__usuario__isnull=False).distinct().select_related('pais'):
        r[f'Libros ({origen(libro.pais)})'] += 1
    for c in CapituloLibroInvestigacion.objects.filter(periodo.contiene('libro__fecha_publicado')) \
            .select_related('libro__pais'):
        r[f'Capítulos ({origen(c.libro.pais)})'] += 1
    resultado = OrderedDict(total=sum(r.values()))
    for tipo in ('WOS/Scopus', 'Otros índices', 'Libros', 'Capítulos'):
        resultado[tipo] = r[f'{tipo} (i)'] + r[f'{tipo} (n)']
        resultado[f'{tipo} · i'] = r[f'{tipo} (i)']
        resultado[f'{tipo} · n'] = r[f'{tipo} (n)']
    return resultado


def cuartiles(periodo):
    """Figura 20: artículos por cuartil de la revista (%), sobre todos los del periodo; sin cuartil, «n/d»."""
    from investigacion.models import ArticuloCientifico

    r = Counter()
    for a in ArticuloCientifico.objects.filter(periodo.contiene('fecha_publicado')).select_related('revista'):
        metrica = a.revista.metricas.filter(anio=a.fecha_publicado.year).first()
        r[metrica.cuartil if metrica and metrica.cuartil else 'n/d'] += 1
    total = sum(r.values())
    return OrderedDict((q, round(100 * r[q] / total, 1) if total else 0) for q in ('Q1', 'Q2', 'Q3', 'Q4', 'n/d'))


# --------------------------------------------------------------------------------------------------- vinculación
def vinculacion(periodo):
    """Figura 24: acciones de vinculación académica."""
    from distinciones.models import SociedadCientifica
    from movilidad_academica.models import MovilidadAcademica as M
    from vinculacion.models import ArbitrajePublicacion as A, ConsejoEditorial, OtraComision, RedAcademica

    r = OrderedDict()
    arb = A.objects.filter(periodo.contiene('fecha_dictamen')).select_related('revista__pais')
    r['Arbitraje · revistas nacionales'] = sum(1 for a in arb if a.tipo == A.Tipo.ARTICULO and a.revista.pais.code2 == 'MX')
    r['Arbitraje · revistas extranjeras'] = sum(1 for a in arb if a.tipo == A.Tipo.ARTICULO and a.revista.pais.code2 != 'MX')
    r['Arbitraje · libros'] = sum(1 for a in arb if a.tipo == A.Tipo.LIBRO)
    r['Arbitraje · capítulos'] = sum(1 for a in arb if a.tipo == A.Tipo.CAPITULO_LIBRO)
    proyectos = OtraComision.objects.filter(periodo.contiene('fecha_inicio'), tipo_id=5).select_related(
        'institucion__padre')  # Cada registro cuenta tantos proyectos como evaluó.
    nombre = lambda o: (o.institucion.nombre if o.institucion else '').upper() + (
        o.institucion.padre.nombre.upper() if o.institucion and o.institucion.padre_id else '')
    r['Arbitraje de proyectos · DGAPA/UNAM'] = sum(o.cantidad for o in proyectos
                                                   if 'DGAPA' in nombre(o) or 'UNAM' in nombre(o))
    r['Arbitraje de proyectos · SECIHTI'] = sum(o.cantidad for o in proyectos if 'SECIHTI' in nombre(o) or 'CONA' in nombre(o))
    r['Arbitraje de proyectos · otros'] = sum(o.cantidad for o in proyectos) - r['Arbitraje de proyectos · DGAPA/UNAM'] \
        - r['Arbitraje de proyectos · SECIHTI']
    redes = RedAcademica.objects.filter(Q(fecha_fin__isnull=True) | Q(fecha_fin__gte=periodo.inicio),
                                        participantes__usuario__isnull=False).distinct()
    r['Redes · nacionales'] = redes.exclude(ambito='INTERNACIONAL').count()
    r['Redes · internacionales'] = redes.filter(ambito='INTERNACIONAL').count()
    # Sociedades distintas (varios académicos en la misma sociedad cuentan una vez), como en el informe.
    sociedades = {}
    for s in SociedadCientifica.objects.filter(periodo.vigente()).order_by('pk'):
        sociedades.setdefault(normalizar(s.nombre), s.ambito)
    r['Sociedades · nacionales'] = sum(1 for a in sociedades.values() if a != 'INTERNACIONAL')
    r['Sociedades · internacionales'] = sum(1 for a in sociedades.values() if a == 'INTERNACIONAL')
    editoriales = ConsejoEditorial.objects.filter(periodo.vigente())
    r['Comités/consejos editoriales · nacionales'] = editoriales.filter(origen='NACIONAL').count()
    r['Comités/consejos editoriales · extranjeros'] = editoriales.filter(origen='EXTRANJERA').count()
    movilidad = M.objects.filter(periodo.contiene('fecha_inicio'))
    r['Sabáticos y estancias · del personal'] = movilidad.exclude(tipo=M.Tipo.INVITACION).filter(visitante=False).count()
    r['Sabáticos y estancias · visitantes'] = movilidad.filter(Q(tipo=M.Tipo.INVITACION) | Q(visitante=True)).count()
    r['total'] = sum(r.values())
    return r


# --------------------------------------------------------------------------------------------------- docencia
#: Años que puede durar una tesis en proceso; pasado ese plazo deja de contarse (registros que nadie cerró).
PLAZO_TESIS = {'DOCTORADO': 6, 'MAESTRIA': 3, 'LICENCIATURA': 3}


def es_unam(institucion):
    while institucion is not None:
        if institucion.pertenece_unam or 'UNAM' in institucion.nombre or 'Nacional Autónoma de México' in institucion.nombre:
            return True
        institucion = institucion.padre
    return False


def tesis(periodo):
    """Figura 28: direcciones de tesis concluidas y en proceso; una tesis codirigida por dos académicos cuenta una vez."""
    from formacion_recursos_humanos.models import DireccionTesis as T

    r = Counter()
    vigentes = T.objects.filter(Q(status=T.Status.EN_PROCESO, fecha_inicio__lte=periodo.fin)
                                | Q(status=T.Status.TERMINADA) & periodo.contiene('fecha_examen')) \
        .select_related('institucion__padre', 'programa')
    for t in vigentes:
        if t.status == T.Status.EN_PROCESO and t.fecha_inicio.year < periodo.fin.year - PLAZO_TESIS[t.nivel]:
            continue
        # «UNAM» en el informe: licenciaturas de la UNAM y su Posgrado en Geografía; los demás posgrados, «otras».
        unam = es_unam(t.institucion) and (t.nivel == 'LICENCIATURA' or (
            t.programa is not None and 'geograf' in t.programa.nombre.lower()))
        estado = 'Concluidas' if t.status == T.Status.TERMINADA else 'En proceso'
        r[f'{estado} · {t.get_nivel_display()} · {"UNAM" if unam else "otras"}'] += 1
    resultado = OrderedDict()
    for estado in ('Concluidas', 'En proceso'):
        resultado[estado] = sum(n for k, n in r.items() if k.startswith(estado))
        for k in sorted(k for k in r if k.startswith(estado)):
            resultado[k] = r[k]
    return resultado


def cursos_posgrado(periodo):
    """Figura 26: cursos de posgrado por programa, categoría y nivel de participación."""
    from docencia.models import CursoEscolarizado as C

    r, vistos = Counter(), set()
    for c in C.objects.filter(periodo.contiene('fecha_inicio'), nivel__in=['MAESTRIA', 'DOCTORADO']) \
            .select_related('programa', 'usuario').order_by('pk'):
        clave = (c.asignatura_id, c.fecha_inicio, c.institucion_id, c.nombramiento)
        if clave in vistos:  # Un curso compartido por varios académicos cuenta una vez.
            continue
        vistos.add(clave)
        programa = 'Posgrado en Geografía' if c.programa and 'geograf' in c.programa.nombre.lower() else 'Otros posgrados'
        categoria = {'INVESTIGADOR': 'INV', 'TECNICO': 'TEC', 'POSTDOCTORADO': 'POSDOC'}.get(c.usuario.tipo, 'OTRO')
        r[f'{programa} · {categoria} · {c.get_nombramiento_display()}'] += 1
    resultado = OrderedDict()
    for programa in ('Posgrado en Geografía', 'Otros posgrados'):
        resultado[programa] = sum(n for k, n in r.items() if k.startswith(programa))
        for k in sorted(k for k in r if k.startswith(programa)):
            resultado[k] = r[k]
    return resultado


FIGURAS = OrderedDict([
    ('6. Planta académica', planta), ('7. Antigüedad promedio', antiguedad), ('8. Contratos', contratos),
    ('11. Proyectos por financiamiento', proyectos_financiamiento), ('12. Tipos de proyectos', proyectos_tipos),
    ('13. ODS', ods), ('14. Problemas nacionales', prioridades), ('15. Publicaciones', publicaciones),
    ('20. Cuartiles', cuartiles), ('21. PRIDE', pride), ('22. SNII', snii), ('24. Vinculación académica', vinculacion),
    ('26. Cursos de posgrado', cursos_posgrado), ('28. Tesis', tesis),
])

#: Cifras de las gráficas del informe 2025-2026 hechas a mano (para comparar).
REFERENCIA_2025_2026 = {
    '6. Planta académica': {'total': 36, 'Investigadores': 23, 'Técnicos': 13, 'Investigadores · mujeres %': 39,
                            'Técnicos · mujeres %': 62, 'Investigadores · Asociado C': 5, 'Investigadores · Titular A': 4,
                            'Investigadores · Titular B': 9, 'Investigadores · Titular C': 5, 'Técnicos · Asociado C': 4,
                            'Técnicos · Titular A': 1, 'Técnicos · Titular B': 6, 'Técnicos · Titular C': 2},
    '7. Antigüedad promedio': {'Investigadores · Asociado C': 4.2, 'Investigadores · Titular A': 11.2,
                               'Investigadores · Titular B': 18.2, 'Investigadores · Titular C': 24.5,
                               'Técnicos · Asociado C': 3.8, 'Técnicos · Titular A': 9.0, 'Técnicos · Titular B': 20.3,
                               'Técnicos · Titular C': 23.0},
    '8. Contratos': {'Investigadores · Obra determinada': 3, 'Investigadores · Definitivo': 19,
                     'Investigadores · Interino': 1, 'Técnicos · Obra determinada': 3, 'Técnicos · Definitivo': 9,
                     'Técnicos · Interino': 1},
    '11. Proyectos por financiamiento': {'SECIHTI': 3, 'PAPIIT': 19, 'PAPIME': 3, 'Ingr. Extr. Nac.': 1,
                                         'Ingr. Extr. Inter.': 1},
    '12. Tipos de proyectos': {'total': 46, 'Multidisciplinario': 16, 'Interdisciplinario': 16,
                               'Transdisciplinario': 11, 'Disciplinario': 3},
    '13. ODS': {'1': 3, '2': 5, '3': 2, '4': 4, '5': 0, '6': 8, '7': 1, '8': 3, '9': 2, '10': 6, '11': 13, '12': 6,
                '13': 10, '14': 1, '15': 22, '16': 1, '17': 1},
    '14. Problemas nacionales': {'Sistemas socioecológicos y sustentabilidad': 21, 'Agua': 7,
                                 'Soberanía alimentaria': 5, 'Vivienda': 4, 'Cultura': 4, 'Educación': 3,
                                 'Energía y cambio climático': 2},
    '15. Publicaciones': {'total': 122, 'WOS/Scopus': 70, 'WOS/Scopus · i': 61, 'WOS/Scopus · n': 9,
                          'Otros índices': 8, 'Otros índices · i': 5, 'Otros índices · n': 3, 'Libros': 9,
                          'Libros · i': 1, 'Libros · n': 8, 'Capítulos': 35, 'Capítulos · i': 5, 'Capítulos · n': 30},
    '20. Cuartiles': {'Q1': 43.6, 'Q2': 20.5, 'Q3': 11.5, 'Q4': 12.8, 'n/d': 11.5},
    '21. PRIDE': {'Investigadores · B o equivalencia': 4, 'Investigadores · C': 9, 'Investigadores · D': 10,
                  'Técnicos · B o equivalencia': 2, 'Técnicos · C': 5, 'Técnicos · D': 6},
    '22. SNII': {'Candidato': 0, 'Nivel I': 11, 'Nivel II': 7, 'Nivel III': 5, 'Emérito': 1},
    '24. Vinculación académica': {'Arbitraje · revistas nacionales': 19, 'Arbitraje · revistas extranjeras': 75,
                                  'Arbitraje · libros': 3, 'Arbitraje · capítulos': 6,
                                  'Arbitraje de proyectos · DGAPA/UNAM': 4, 'Arbitraje de proyectos · SECIHTI': 17,
                                  'Arbitraje de proyectos · otros': 6, 'Redes · nacionales': 9,
                                  'Redes · internacionales': 23, 'Sociedades · nacionales': 7,
                                  'Sociedades · internacionales': 17, 'total': 236},
    '26. Cursos de posgrado': {'Posgrado en Geografía': 43, 'Otros posgrados': 6},
    '28. Tesis': {'Concluidas': 32, 'En proceso': 80, 'Concluidas · Doctorado · UNAM': 9,
                  'Concluidas · Doctorado · otras': 3, 'Concluidas · Maestría · UNAM': 7,
                  'Concluidas · Maestría · otras': 4, 'Concluidas · Licenciatura · UNAM': 7,
                  'Concluidas · Licenciatura · otras': 2, 'En proceso · Doctorado · UNAM': 12,
                  'En proceso · Doctorado · otras': 13, 'En proceso · Maestría · UNAM': 27,
                  'En proceso · Maestría · otras': 11, 'En proceso · Licenciatura · UNAM': 14,
                  'En proceso · Licenciatura · otras': 3},
}
