"""Catálogo de indicadores para las gráficas de los informes.

Cada indicador recibe el periodo del informe (julio a junio) y cuántos periodos mostrar, y devuelve sus datos en una
forma común que cualquier tipo de gráfica compatible sabe dibujar:

    {'total': 36, 'total_etiqueta': 'académic@s',
     'paneles': [{'titulo': 'Investigadores', 'total': 23, 'partes': [{'nombre': 'F', 'valor': 39}, ...],
                  'categorias': ['Asociado C', ...], 'series': [{'nombre': '…', 'valores': [5, ...]}]}],
     'jerarquia': [{'nombre': '…', 'valor': 16, 'hijos': [...]}],      # para anillos
     'grupos': [{'nombre': '…', 'items': [{'nombre': '…', 'valor': 19}]}],  # para el semicírculo
     'colores_categorias': ['#E5243B', ...], 'extra': {...}}

Los cálculos son los de `nucleo.cifras_informe`, que reproducen el informe anual oficial.
"""

from collections import Counter, OrderedDict
from dataclasses import dataclass, field
from statistics import mean
from typing import Callable

TIPOS = [
    ('columnas', 'Columnas'),
    ('barras', 'Barras horizontales'),
    ('rango', 'Rango y promedio'),
    ('pastillas', 'Comparación por periodos'),
    ('dona', 'Dona'),
    ('anillos', 'Anillos (jerarquía)'),
    ('rosa', 'Rosa polar'),
    ('semicirculo', 'Semicírculo por grupos'),
    ('tabla', 'Tabla'),
]

#: Colores oficiales de los 17 Objetivos de Desarrollo Sostenible.
COLORES_ODS = ['#E5243B', '#DDA63A', '#4C9F38', '#C5192D', '#FF3A21', '#26BDE2', '#FCC30B', '#A21942', '#FD6925',
               '#DD1367', '#FD9D24', '#BF8B2E', '#3F7E44', '#0A97D9', '#56C02B', '#00689D', '#19486A']


@dataclass
class Indicador:
    clave: str
    nombre: str
    descripcion: str
    tipos: list
    funcion: Callable
    historico: bool = False  # Usa varios periodos (los de la gráfica).
    tipo_inicial: str = ''
    etiquetas: dict = field(default_factory=dict)


def _periodo(texto):
    from nucleo.cifras_informe import Periodo

    return Periodo.de(texto)


def periodos_hasta(periodo, n):
    """Los `n` periodos que terminan en `periodo`, del más antiguo al más reciente."""
    from nucleo.cifras_informe import Periodo

    return [Periodo.de(f'{a}-{a + 1}') for a in range(periodo.inicio.year - max(n, 1) + 1, periodo.inicio.year + 1)]


def _panel(titulo, categorias, series, total=None, partes=None):
    return {'titulo': titulo, 'total': total, 'partes': partes or [], 'categorias': list(categorias),
            'series': [{'nombre': n, 'valores': list(v)} for n, v in series]}


def _situaciones(anio):
    from nucleo.models import SituacionAcademica

    return SituacionAcademica.objects.filter(anio=anio, nombramiento__isnull=False).select_related('usuario',
                                                                                                    'nombramiento')


def _grupo(nombramiento):
    from nucleo.cifras_informe import _es_investigador

    return 'Investigadores' if _es_investigador(nombramiento) else 'Técnicos'


NIVELES = ['Asociado A', 'Asociado B', 'Asociado C', 'Titular A', 'Titular B', 'Titular C']


# --------------------------------------------------------------------------------------------------- planta
def planta(periodo, n=1):
    from nucleo.cifras_informe import _nivel_corto
    from nucleo.models import User

    situaciones = list(_situaciones(periodo.anio_corte))
    paneles = []
    for grupo in ('Investigadores', 'Técnicos'):
        del_grupo = [s for s in situaciones if _grupo(s.nombramiento) == grupo]
        cuenta = Counter(_nivel_corto(s.nombramiento) for s in del_grupo)
        niveles = [nv for nv in NIVELES if cuenta[nv]]
        mujeres = round(100 * sum(s.usuario.genero == User.Genero.FEMENINO for s in del_grupo) / len(del_grupo)) \
            if del_grupo else 0
        paneles.append(_panel(grupo, niveles, [(grupo, [cuenta[nv] for nv in niveles])], len(del_grupo),
                              [{'nombre': 'F', 'valor': mujeres}, {'nombre': 'M', 'valor': 100 - mujeres}]))
    return {'total': len(situaciones), 'total_etiqueta': 'académic@s', 'paneles': paneles}


def antiguedad(periodo, n=1):
    from nucleo.cifras_informe import _nivel_corto

    anios = {}
    for s in _situaciones(periodo.anio_corte):
        ingreso = s.usuario.ingreso_unam or s.usuario.ingreso_entidad
        if ingreso:
            anios.setdefault(_grupo(s.nombramiento), {}).setdefault(_nivel_corto(s.nombramiento), []).append(
                periodo.anio_corte - ingreso.year)
    paneles = []
    for grupo in ('Investigadores', 'Técnicos'):
        por_nivel = anios.get(grupo, {})
        niveles = [nv for nv in NIVELES if nv in por_nivel]
        paneles.append(_panel(grupo, niveles, [
            ('Promedio', [round(mean(por_nivel[nv]), 1) for nv in niveles]),
            ('Mínimo', [min(por_nivel[nv]) for nv in niveles]),
            ('Máximo', [max(por_nivel[nv]) for nv in niveles])]))
    return {'paneles': paneles, 'extra': {'unidad': 'años'}}


def contratos(periodo, n=4):
    anios = [p.anio_corte for p in periodos_hasta(periodo, n)]
    tipos = ['Obra determinada', 'Definitivo', 'Interino', 'IxM', 'Sin dato']
    paneles = []
    for grupo in ('Investigadores', 'Técnicos'):
        cuenta = {a: Counter() for a in anios}
        for a in anios:
            for s in _situaciones(a):
                if _grupo(s.nombramiento) == grupo:
                    etiqueta = s.get_contrato_display() or 'Sin dato'
                    cuenta[a]['IxM' if 'IxM' in etiqueta or 'México' in etiqueta else etiqueta] += 1
        series = [(t, [cuenta[a][t] for a in anios]) for t in tipos if any(cuenta[a][t] for a in anios)]
        paneles.append(_panel(grupo, [str(a) for a in anios], series))
    return {'paneles': paneles}


def _hay_situaciones(anio):
    from nucleo.models import SituacionAcademica

    return SituacionAcademica.objects.filter(anio=anio, nombramiento__isnull=False).exists()


def _de_historico(indicador, anio, anio_informe, panel=''):
    """Cifras de un año anterior al del informe tomadas de las históricas (las oficiales de ese año), o None si no hay
    y hay que calcularlas. El año del informe siempre se calcula con los datos actuales."""
    if anio == anio_informe:
        return None
    cifras = _historica(indicador, anio, panel)
    return Counter(cifras) if cifras else None


def _historica(indicador, anio, panel=''):
    from .models import CifraHistorica

    return CifraHistorica.de(indicador, anio, panel)


def pride(periodo, n=4):
    """Por nivel del PRIDE; los años anteriores al del informe, de las cifras históricas cuando las hay."""
    from nucleo.models import SituacionAcademica as S

    periodos = periodos_hasta(periodo, n)
    niveles = ['PRIDE B o equivalencia', 'PRIDE C', 'PRIDE D']
    paneles = []
    for grupo in ('Investigadores', 'Técnicos'):
        cuenta = {}
        for p in periodos:
            historico = _de_historico('pride', p.anio_corte, periodo.anio_corte, grupo)
            if historico is not None:
                cuenta[p.nombre] = historico
                continue
            c = Counter()
            for s in _situaciones(p.anio_corte):
                if _grupo(s.nombramiento) == grupo and s.pride:
                    c[niveles[0] if s.pride in ('A', 'B', S.Pride.EQUIVALENCIA) else f'PRIDE {s.pride}'] += 1
            cuenta[p.nombre] = c
        paneles.append(_panel(grupo, [p.nombre for p in periodos],
                              [(nv, [cuenta[p.nombre][nv] for p in periodos]) for nv in niveles]))
    return {'paneles': paneles}


def snii(periodo, n=4):
    """Por nivel del SNII; los años anteriores al del informe, de las cifras históricas cuando las hay."""
    from nucleo.models import SituacionAcademica

    periodos = periodos_hasta(periodo, n)
    nombres = {'C': 'Candidato', 'I': 'Nivel I', 'II': 'Nivel II', 'III': 'Nivel III', 'E': 'Emérito'}
    cuenta = {}
    for p in periodos:
        historico = _de_historico('snii', p.anio_corte, periodo.anio_corte)
        if historico is not None:
            cuenta[p.nombre] = historico
            continue
        c = Counter(SituacionAcademica.objects.filter(anio=p.anio_corte).exclude(sni='').values_list('sni', flat=True))
        cuenta[p.nombre] = Counter({nombres[k]: v for k, v in c.items()})
    series = [(nombre, [cuenta[p.nombre][nombre] for p in periodos]) for nombre in nombres.values()
              if any(cuenta[p.nombre][nombre] for p in periodos)]
    return {'paneles': [_panel('', [p.nombre for p in periodos], series)]}


def evolucion_planta(periodo, n=20):
    """Planta académica por año: investigadores, técnicos y cátedras/IxM (los años anteriores al del informe, de las
    cifras históricas cuando las hay)."""
    anios = [p.anio_corte for p in periodos_hasta(periodo, n)]
    categorias = ['Investigadores', 'Técnicos', 'Cátedras / IxM']
    cuenta = {}
    for anio in anios:
        historico = _de_historico('evolucion_planta', anio, periodo.anio_corte)
        if historico is not None:
            cuenta[anio] = historico
            continue
        c = Counter()
        for s in _situaciones(anio):
            c['Cátedras / IxM' if s.contrato == 'IXM' else _grupo(s.nombramiento)] += 1
        cuenta[anio] = c
    anios = [a for a in anios if sum(cuenta[a].values())]  # Solo los años con datos.
    series = [(c, [cuenta[a][c] for a in anios]) for c in categorias if any(cuenta[a][c] for a in anios)]
    return {'paneles': [_panel('', [str(a) for a in anios], series)]}


# --------------------------------------------------------------------------------------------------- proyectos
def proyectos_financiamiento(periodo, n=3):
    from nucleo.cifras_informe import proyectos_financiamiento as calculo

    periodos = periodos_hasta(periodo, n)
    datos = [calculo(p) for p in periodos]
    instancias = list(datos[-1])
    return {'paneles': [_panel('', instancias, [(p.nombre, [d[i] for i in instancias])
                                                 for p, d in zip(periodos, datos)])]}


def tipos_proyectos(periodo, n=1):
    from investigacion.models import ProyectoInvestigacion as P
    from nucleo.cifras_informe import _proyectos

    alcance = {P.Clasificacion.BASICO: 'Básico', P.Clasificacion.APLICADO: 'Aplicado',
               P.Clasificacion.DESARROLLO_TECNOLOGICO: 'DT', P.Clasificacion.INNOVACION: 'Innovación',
               P.Clasificacion.INVESTIGACION_FRONTERA: 'Frontera'}
    arbol = OrderedDict()
    for p in _proyectos(periodo):
        modalidad = P.ModalidadProyecto(p.modalidad).label if p.modalidad else 'Sin modalidad'
        genero = 'Con temática de género' if p.tematica_genero else 'Sin temática de género'
        arbol.setdefault(modalidad, OrderedDict()).setdefault(alcance.get(p.clasificacion, 'Otro'), Counter())[genero] += 1
    arbol = OrderedDict(sorted(arbol.items(), key=lambda kv: -sum(sum(c.values()) for c in kv[1].values())))
    jerarquia = [{'nombre': m, 'valor': sum(sum(c.values()) for c in hijos.values()),
                  'hijos': [{'nombre': a, 'valor': sum(c.values()),
                             'hijos': [{'nombre': g, 'valor': v} for g, v in sorted(c.items())]}
                            for a, c in hijos.items()]} for m, hijos in arbol.items()]
    total = sum(j['valor'] for j in jerarquia)
    return {'total': total, 'total_etiqueta': 'proyectos', 'jerarquia': jerarquia,
            'paneles': [_panel('', [j['nombre'] for j in jerarquia], [('Proyectos', [j['valor'] for j in jerarquia])])]}


def ods(periodo, n=1):
    from investigacion.models import ObjetivoDesarrolloSostenible
    from nucleo.cifras_informe import ods as calculo

    datos = calculo(periodo)
    nombres = {str(o.numero): f'{o.numero}. {o.nombre}' for o in ObjetivoDesarrolloSostenible.objects.all()}
    return {'paneles': [_panel('', [nombres.get(k, k) for k in datos], [('Proyectos', list(datos.values()))])],
            'colores_categorias': COLORES_ODS[:len(datos)], 'extra': {'centro': 'ODS'}}


def prioridades(periodo, n=1):
    from nucleo.cifras_informe import prioridades as calculo

    datos = calculo(periodo)
    return {'paneles': [_panel('', list(datos), [('Proyectos', list(datos.values()))])]}


# --------------------------------------------------------------------------------------------------- publicaciones
def publicaciones(periodo, n=1):
    from nucleo.cifras_informe import publicaciones as calculo

    d = calculo(periodo)
    tipos = ['WOS/Scopus', 'Otros índices', 'Libros', 'Capítulos']
    nombres = ['WOS / Scopus', 'Otros índices', 'Libros', 'Capítulos']
    total = d['total']
    internac = sum(d[f'{t} · i'] for t in tipos)
    investigadores = len([s for s in _situaciones(periodo.anio_corte) if _grupo(s.nombramiento) == 'Investigadores'])
    indizados = d['WOS/Scopus'] + d['Otros índices']
    promedio = lambda x: round(x / investigadores, 2) if investigadores else 0
    return {'total': total, 'total_etiqueta': 'productos publicados', 'paneles': [_panel(
        'Producción por tipo de publicación', nombres,
        [('Internacional', [d[f'{t} · i'] for t in tipos]), ('Nacional', [d[f'{t} · n'] for t in tipos])], total,
        [{'nombre': 'Internac.', 'valor': round(100 * internac / total) if total else 0},
         {'nombre': 'Nac.', 'valor': 100 - round(100 * internac / total) if total else 0}])],
            'extra': {'promedios': [
                {'nombre': 'Todas las publicaciones', 'valor': promedio(total), 'base': total},
                {'nombre': 'Artículos indizados', 'valor': promedio(indizados), 'base': indizados},
                {'nombre': 'WOS / Scopus', 'valor': promedio(d['WOS/Scopus']), 'base': d['WOS/Scopus']}],
                'investigadores': investigadores}}


def cuartiles(periodo, n=1):
    from investigacion.models import ArticuloCientifico

    def rango(fi):
        if fi is None or fi == 0:
            return 'NA'
        return 'FI <1.0' if fi < 1 else 'FI 1.0–3.0' if fi <= 3 else 'FI 3.1–5.0' if fi <= 5 else 'FI >5.0'

    arbol = OrderedDict((q, Counter()) for q in ('Q1', 'Q2', 'Q3', 'Q4', 'n/d'))
    for a in ArticuloCientifico.objects.filter(periodo.contiene('fecha_publicado')).select_related('revista'):
        metrica = a.revista.metricas.filter(anio=a.fecha_publicado.year).first()
        q = metrica.cuartil if metrica and metrica.cuartil else 'n/d'
        arbol[q][rango(metrica.factor_impacto if metrica else None)] += 1
    total = sum(sum(c.values()) for c in arbol.values())
    pct = lambda v: round(100 * v / total, 1) if total else 0
    jerarquia = [{'nombre': q, 'valor': sum(c.values()), 'porcentaje': pct(sum(c.values())),
                  'hijos': [{'nombre': r, 'valor': v} for r, v in sorted(c.items())]} for q, c in arbol.items()]
    return {'total': total, 'total_etiqueta': 'artículos', 'jerarquia': jerarquia,
            'paneles': [_panel('', list(arbol), [('% de artículos', [pct(sum(c.values())) for c in arbol.values()])])],
            'extra': {'unidad': '%'}}


# --------------------------------------------------------------------------------------------------- vinculación
GRUPOS_VINCULACION = [
    ('Arbitraje de publicaciones', [('En revistas nacionales', 'Arbitraje · revistas nacionales'),
                                    ('En revistas extranjeras', 'Arbitraje · revistas extranjeras'),
                                    ('Libros', 'Arbitraje · libros'), ('Capítulos de libros', 'Arbitraje · capítulos')]),
    ('Arbitraje de proyectos', [('DGAPA', 'Arbitraje de proyectos · DGAPA/UNAM'),
                                ('SECIHTI', 'Arbitraje de proyectos · SECIHTI'),
                                ('Otros (nac./internac.)', 'Arbitraje de proyectos · otros')]),
    ('Académicos invitados', [('Invitados', 'Académicos invitados')]),
    ('Redes académicas', [('Red nacional', 'Redes · nacionales'), ('Red internacional', 'Redes · internacionales')]),
    ('Sociedades científicas', [('SC nacionales', 'Sociedades · nacionales'),
                                ('SC internacionales', 'Sociedades · internacionales')]),
    ('Estancias', [('Del personal', 'Estancias · del personal'), ('Visitantes', 'Estancias · visitantes')]),
    ('Sabáticos', [('Del personal', 'Sabáticos · del personal'), ('Visitantes', 'Sabáticos · visitantes')]),
    ('Consejos editoriales', [('De revistas nacionales', 'Consejos editoriales · nacionales'),
                              ('De revistas extranjeras', 'Consejos editoriales · extranjeros')]),
    ('Comités editoriales', [('De revistas nacionales', 'Comités editoriales · nacionales'),
                             ('De revistas extranjeras', 'Comités editoriales · extranjeros')]),
]


def vinculacion(periodo, n=1):
    from nucleo.cifras_informe import vinculacion as calculo

    d = calculo(periodo)
    grupos = [{'nombre': g, 'items': [{'nombre': n_, 'valor': d.get(k, 0)} for n_, k in items]}
              for g, items in GRUPOS_VINCULACION]
    totales = [sum(i['valor'] for i in g['items']) for g in grupos]
    return {'total': sum(totales), 'total_etiqueta': 'acciones de vinculación académica', 'grupos': grupos,
            'paneles': [_panel('', [g['nombre'] for g in grupos], [('Acciones', totales)])]}


# --------------------------------------------------------------------------------------------------- docencia
def cursos_posgrado(periodo, n=1):
    from nucleo.cifras_informe import cursos_posgrado as calculo

    d = calculo(periodo)
    categorias = ['INV', 'TEC', 'POSDOC']
    niveles = ['Titular o coordinador', 'Colaborador o invitado']
    paneles = []
    for programa in ('Posgrado en Geografía', 'Otros posgrados'):
        paneles.append(_panel(programa, categorias,
                              [(nv, [d.get(f'{programa} · {c} · {nv}', 0) for c in categorias]) for nv in niveles],
                              d.get(programa, 0)))
    return {'paneles': paneles, 'extra': {'cursos': {p: d.get(f'{p} · cursos impartidos', 0) for p in
                                                     ('Posgrado en Geografía', 'Otros posgrados')}}}


def tesis(periodo, n=1):
    from nucleo.cifras_informe import tesis as calculo

    d = calculo(periodo)
    niveles = ['Doctorado', 'Maestría', 'Licenciatura']
    paneles = []
    for estado in ('Concluidas', 'En proceso'):
        paneles.append(_panel(estado, niveles, [
            ('UNAM (licenciaturas y Posgrado en Geografía)', [d.get(f'{estado} · {nv} · UNAM', 0) for nv in niveles]),
            ('Otras instituciones', [d.get(f'{estado} · {nv} · otras', 0) for nv in niveles])], d.get(estado, 0)))
    return {'paneles': paneles, 'total_etiqueta': 'tesis'}


INDICADORES = OrderedDict((i.clave, i) for i in [
    Indicador('planta', 'Planta académica por categoría, nivel y género',
              'Investigadores y técnicos académicos con nombramiento al corte de agosto.',
              ['columnas', 'barras', 'tabla'], planta),
    Indicador('antiguedad', 'Antigüedad por categoría y nivel', 'Años en la UNAM: mínimo, máximo y promedio.',
              ['rango', 'columnas', 'tabla'], antiguedad),
    Indicador('contratos', 'Personal por tipo de contrato (histórico)', 'Por año de corte.',
              ['columnas', 'barras', 'tabla'], contratos, historico=True),
    Indicador('proyectos_financiamiento', 'Proyectos por instancia financiadora (histórico)',
              'Proyectos administrados por la entidad, por periodo.',
              ['pastillas', 'columnas', 'barras', 'tabla'], proyectos_financiamiento, historico=True),
    Indicador('tipos_proyectos', 'Tipos de proyectos', 'Modalidad, alcance y temática de género.',
              ['anillos', 'dona', 'columnas', 'barras', 'tabla'], tipos_proyectos),
    Indicador('ods', 'Proyectos por Objetivo de Desarrollo Sostenible', 'Un proyecto puede atender varios ODS.',
              ['rosa', 'barras', 'columnas', 'tabla'], ods),
    Indicador('prioridades', 'Problemas nacionales prioritarios', 'Proyectos por prioridad estratégica (SECIHTI).',
              ['barras', 'columnas', 'dona', 'tabla'], prioridades),
    Indicador('publicaciones', 'Productos publicados por tipo y origen',
              'Artículos, libros y capítulos publicados en el periodo.', ['columnas', 'barras', 'tabla'], publicaciones),
    Indicador('cuartiles', 'Cuartil y factor de impacto de las revistas',
              'Todos los artículos del periodo; los que no tienen cuartil, «n/d».',
              ['anillos', 'dona', 'columnas', 'tabla'], cuartiles),
    Indicador('evolucion_planta', 'Evolución de la planta académica (histórico)',
              'Investigadores, técnicos y cátedras/IxM por año.', ['columnas', 'barras', 'tabla'], evolucion_planta,
              historico=True),
    Indicador('pride', 'Planta por nivel del PRIDE (histórico)', 'Por periodo.', ['columnas', 'barras', 'tabla'],
              pride, historico=True),
    Indicador('snii', 'Académicos por nivel del SNII (histórico)', 'Por periodo.', ['columnas', 'barras', 'tabla'],
              snii, historico=True),
    Indicador('vinculacion', 'Acciones de vinculación académica', 'Arbitrajes, redes, sociedades, movilidad y '
              'comités editoriales.', ['semicirculo', 'barras', 'columnas', 'tabla'], vinculacion),
    Indicador('cursos_posgrado', 'Cursos de posgrado por programa, categoría y participación',
              'Cada académico en cada curso.', ['columnas', 'barras', 'tabla'], cursos_posgrado),
    Indicador('tesis', 'Tesis concluidas y en proceso', 'Por grado e institución.', ['barras', 'columnas', 'tabla'],
              tesis),
])

INDICADORES['personalizado'] = Indicador(
    'personalizado', 'Indicador personalizado', 'Definido en «Indicadores personalizados».',
    ['columnas', 'barras', 'dona', 'pastillas', 'tabla'], None, historico=True)

OPCIONES_INDICADOR = [(clave, i.nombre) for clave, i in INDICADORES.items()]


def calcular(grafica, periodo_texto):
    """Datos de una gráfica para el periodo del informe (o un mensaje si el indicador falla)."""
    indicador = INDICADORES.get(grafica.indicador)
    if indicador is None:
        return {'error': f'Indicador desconocido: {grafica.indicador}'}
    periodo = _periodo(periodo_texto)
    if grafica.indicador == 'personalizado':
        from .personalizados import calcular as calcular_personalizado

        if grafica.personalizado is None:
            return {'error': 'Falta elegir el indicador personalizado.'}
        return calcular_personalizado(grafica.personalizado, periodo, grafica.periodos)
    return indicador.funcion(periodo, grafica.periodos if indicador.historico else 1)


#: Figura del informe anual publicado con que se compara cada indicador (ver `nucleo.cifras_informe`).
FIGURA_DEL_INFORME = {
    'planta': '6. Planta académica', 'antiguedad': '7. Antigüedad promedio', 'contratos': '8. Contratos',
    'proyectos_financiamiento': '11. Proyectos por financiamiento', 'tipos_proyectos': '12. Tipos de proyectos',
    'ods': '13. ODS', 'prioridades': '14. Problemas nacionales', 'publicaciones': '15. Publicaciones',
    'cuartiles': '20. Cuartiles', 'pride': '21. PRIDE', 'snii': '22. SNII', 'vinculacion': '24. Vinculación académica',
    'cursos_posgrado': '26. Cursos de posgrado', 'tesis': '28. Tesis',
}


def comparacion(indicador, periodo_texto):
    """Cifras del SIA frente a las del informe publicado del periodo, con el motivo de cada diferencia; None si no hay
    informe publicado de referencia para ese periodo o indicador."""
    from nucleo.cifras_informe import FIGURAS, REFERENCIA_2025_2026, Periodo, explicacion

    figura = FIGURA_DEL_INFORME.get(indicador)
    if periodo_texto != '2025-2026' or figura not in REFERENCIA_2025_2026:
        return None
    calculado, publicado = FIGURAS[figura](Periodo.de(periodo_texto)), REFERENCIA_2025_2026[figura]
    filas = []
    for clave, valor in publicado.items():
        sia = calculado.get(clave, 0)
        motivo = None if sia == valor else explicacion(figura, clave)
        filas.append({'clave': clave, 'sia': sia, 'informe': valor,
                      'estado': 'igual' if sia == valor else (motivo[0] if motivo else 'sin explicar'),
                      'motivo': motivo[1] if motivo else ''})
    return {'figura': figura, 'filas': filas, 'iguales': sum(f['estado'] == 'igual' for f in filas)}
