"""Indicadores de producción académica para la página de inicio del admin.

Cada indicador compara, año por año, el valor del académico con el promedio y el
máximo entre los académicos adscritos a la entidad en ese año.
"""

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, timedelta

from django.apps import apps
from django.db.models import Count, F, Q, Sum
from django.db.models.functions import ExtractYear
from django.urls import reverse

from nucleo.models import StatusPublicacion, User

MIN_INDICADORES = 3
TIPOS_ACADEMICOS = [User.Tipo.INVESTIGADOR, User.Tipo.TECNICO, User.Tipo.POSTDOCTORADO]


@dataclass(frozen=True)
class Indicador:
    titulo: str
    modelo: str
    fecha: str
    usuario: str
    filtro: dict = field(default_factory=dict)
    suma: str | None = None

    @property
    def model(self):
        return apps.get_model(self.modelo)


PUBLICADO = {'status': StatusPublicacion.PUBLICADO}

INDICADORES = [
    Indicador('Artículos científicos publicados', 'investigacion.ArticuloCientifico', 'fecha_publicado',
              'autores__usuario', PUBLICADO),
    Indicador('Capítulos en libros de investigación', 'investigacion.CapituloLibroInvestigacion',
              'libro__fecha_publicado', 'autores__usuario', {'libro__status': StatusPublicacion.PUBLICADO}),
    Indicador('Libros publicados', 'nucleo.Libro', 'fecha_publicado', 'participantes__usuario', PUBLICADO),
    Indicador('Proyectos de investigación iniciados', 'investigacion.ProyectoInvestigacion', 'fecha_inicio',
              'responsables__usuario'),
    Indicador('Ponencias en eventos académicos', 'difusion_cientifica.ParticipacionEventoAcademico', 'fecha',
              'autores__usuario'),
    Indicador('Artículos de divulgación publicados', 'divulgacion_cientifica.ArticuloDivulgacion', 'fecha_publicado',
              'autores__usuario', PUBLICADO),
    Indicador('Tesis dirigidas concluidas', 'formacion_recursos_humanos.DireccionTesis', 'fecha_examen',
              'director__usuario'),
    Indicador('Horas de docencia escolarizada', 'docencia.CursoEscolarizado', 'fecha_inicio', 'usuario',
              suma='total_horas'),
    Indicador('Horas en cursos de especialización', 'formacion_academica.CursoEspecializacion', 'fecha_inicio',
              'usuario', suma='horas'),
]


def academicos_activos(anios):
    """Por año, los ids de los académicos adscritos a la entidad."""
    academicos = User.objects.filter(tipo__in=TIPOS_ACADEMICOS).values_list('pk', 'ingreso_entidad', 'egreso_entidad')
    activos = {}
    for anio in anios:
        activos[anio] = [
            pk for pk, ingreso, egreso in academicos
            if (ingreso is None or ingreso.year <= anio) and (egreso is None or egreso.year >= anio)
        ]
    return activos


def _serie(indicador, anios, activos, usuario, ver_total):
    modelo = indicador.model
    qs = modelo.objects.filter(**indicador.filtro, **{f'{indicador.fecha}__year__gte': anios[0],
                                                      f'{indicador.fecha}__year__lte': anios[-1]})
    agregado = Sum(indicador.suma) if indicador.suma else Count('pk', distinct=True)
    por_usuario = defaultdict(int)
    filas = qs.values(anio=ExtractYear(indicador.fecha), cuenta=F(indicador.usuario)).annotate(valor=agregado)
    for fila in filas:
        # Las filas sin cuenta corresponden a coautores externos; no se filtran en SQL porque en relaciones
        # M2M excluirían registros completos que también tienen autores de la entidad.
        if fila['cuenta'] is not None:
            por_usuario[(fila['anio'], fila['cuenta'])] = fila['valor'] or 0

    serie = {'titulo': indicador.titulo, 'anios': anios, 'mios': [], 'promedio': [], 'maximo': []}
    for anio in anios:
        valores = [por_usuario[(anio, pk)] for pk in activos[anio]]
        serie['mios'].append(por_usuario[(anio, usuario.pk)])
        serie['promedio'].append(round(sum(valores) / len(valores), 2) if valores else 0)
        serie['maximo'].append(max(valores, default=0))
    if ver_total:
        totales = (qs.values(anio=ExtractYear(indicador.fecha))
                   .annotate(valor=Sum(indicador.suma) if indicador.suma else Count('pk', distinct=True)))
        por_anio = {fila['anio']: fila['valor'] or 0 for fila in totales}
        serie['total'] = [por_anio.get(anio, 0) for anio in anios]
    return serie


def anios_con_datos():
    """Primer año con datos y último año "representativo": el más reciente (sin pasar del año en curso)
    con registros en al menos `MIN_INDICADORES` indicadores, para no anclar el tablero a fechas mal capturadas."""
    hoy = date.today().year
    indicadores_por_anio = defaultdict(int)
    primero = hoy
    for indicador in INDICADORES:
        anios = (indicador.model.objects.filter(**indicador.filtro, **{f'{indicador.fecha}__year__lte': hoy})
                 .annotate(anio=ExtractYear(indicador.fecha)).values_list('anio', flat=True).distinct())
        for anio in set(anios) - {None}:
            indicadores_por_anio[anio] += 1
            primero = min(primero, anio)
    representativos = [anio for anio, n in indicadores_por_anio.items() if n >= MIN_INDICADORES]
    return primero, max(representativos, default=hoy)


def construir_tablero(usuario, hasta=None, ver_total=False):
    """Series de los indicadores para los años (configurables) que terminan en `hasta` o en el último año con datos."""
    from nucleo.models import ConfiguracionEntidad

    primero, ultimo = anios_con_datos()
    hasta = hasta if hasta and primero <= hasta <= date.today().year else ultimo
    num_anios = max(ConfiguracionEntidad.actual().anios_tablero, 1)
    anios = list(range(hasta - num_anios + 1, hasta + 1))
    activos = academicos_activos(anios)
    series = [_serie(indicador, anios, activos, usuario, ver_total) for indicador in INDICADORES]
    return {'series': series, 'hasta': hasta,
            'anios_disponibles': list(range(date.today().year, min(primero, hasta) - 1, -1))}


def _url_cambio(obj):
    return reverse(f'admin:{obj._meta.app_label}_{obj._meta.model_name}_change', args=[obj.pk])


def pendientes(usuario):
    """Cosas que el académico debería revisar: publicaciones estancadas, tesis vencidas, perfil incompleto."""
    from nucleo.admin_base import persona_de
    from nucleo.models import ConfiguracionEntidad, ConfirmacionInforme, PeriodoInforme

    persona = persona_de(usuario)
    hoy = date.today()
    meses = ConfiguracionEntidad.actual().meses_publicacion_pendiente
    limite = hoy - timedelta(days=round(meses * 30.4))
    publicaciones = []
    for etiqueta in ('investigacion.ArticuloCientifico', 'divulgacion_cientifica.ArticuloDivulgacion',
                     'docencia.ArticuloDocencia', 'investigacion.MapaArbitrado', 'investigacion.PublicacionTecnica',
                     'nucleo.Libro'):
        modelo = apps.get_model(etiqueta)
        campo = 'participantes' if etiqueta == 'nucleo.Libro' else 'autores'
        qs = (modelo.objects.filter(**{campo: persona}).exclude(status=StatusPublicacion.PUBLICADO).con_fecha()
              .filter(fecha_orden__lt=limite).distinct())
        publicaciones += [{'texto': f'{obj} — {obj.get_status_display().lower()} desde {obj.fecha_orden:%m/%Y}',
                           'url': _url_cambio(obj)} for obj in qs[:10]]

    DireccionTesis = apps.get_model('formacion_recursos_humanos', 'DireccionTesis')
    tesis = (DireccionTesis.objects.filter(Q(director=persona) | Q(codirector=persona) | Q(tutores=persona),
                                           status=DireccionTesis.Status.EN_PROCESO, fecha_fin__lt=hoy).distinct())
    faltantes = [etiqueta for campo, etiqueta in (('grado', 'grado'), ('semblanza', 'semblanza'), ('email', 'correo'),
                                                 ('ingreso_entidad', 'fecha de ingreso')) if not getattr(usuario, campo)]
    if not persona.orcid:
        faltantes.append('ORCID')

    periodo = PeriodoInforme.abierto_actual()
    return {
        'publicaciones': publicaciones,
        'meses_publicacion_pendiente': meses,
        'tesis': [{'texto': f'{t} — debía terminar en {t.fecha_fin:%m/%Y}', 'url': _url_cambio(t)} for t in tesis[:10]],
        'perfil_faltante': faltantes,
        'perfil_url': reverse('admin:nucleo_user_change', args=[usuario.pk]),
        'periodo': periodo,
        'periodo_confirmado': periodo is not None and ConfirmacionInforme.objects.filter(
            periodo=periodo, usuario=usuario).exists(),
        'dias_restantes': (periodo.fecha_limite - hoy).days if periodo else None,
    }


ALTAS_RAPIDAS = [
    ('Artículo científico', 'investigacion', 'articulocientifico', 'article'),
    ('Ponencia en evento', 'difusion_cientifica', 'participacioneventoacademico', 'campaign'),
    ('Curso impartido', 'docencia', 'cursoescolarizado', 'co_present'),
    ('Dirección de tesis', 'formacion_recursos_humanos', 'direcciontesis', 'school'),
    ('Proyecto', 'investigacion', 'proyectoinvestigacion', 'science'),
]


def contexto_tablero(request, context):
    """`DASHBOARD_CALLBACK` de Unfold: agrega el tablero al contexto del inicio del admin."""
    from nucleo.admin_base import es_administrador

    administrador = es_administrador(request.user)
    try:
        hasta = int(request.GET.get('hasta', ''))
    except ValueError:
        hasta = None
    context.update({
        'tablero': construir_tablero(request.user, hasta=hasta, ver_total=administrador),
        'es_administrador': administrador,
        'pendientes': pendientes(request.user),
        'altas_rapidas': [{'texto': texto, 'icono': icono,
                           'url': reverse(f'admin:{app}_{modelo}_add')} for texto, app, modelo, icono in ALTAS_RAPIDAS],
    })
    return context
