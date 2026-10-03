"""Menú lateral y enlaces de cuenta del admin (Unfold).

El menú sigue el orden de las secciones del informe. A los académicos se les ocultan los
catálogos que solo pueden consultar (países, índices...), que siguen disponibles en los
campos de autocompletado.
"""

from django.contrib import admin
from django.urls import reverse
from django.utils.translation import gettext_lazy

from nucleo.admin_base import SECCIONES_PERFIL, es_administrador

SECCIONES = [
    ('formacion_academica', 'school'),
    ('experiencia_profesional', 'work'),
    ('compromiso_institucional', 'account_balance'),
    ('investigacion', 'science'),
    ('difusion_cientifica', 'campaign'),
    ('divulgacion_cientifica', 'public'),
    ('vinculacion', 'handshake'),
    ('movilidad_academica', 'flight'),
    ('docencia', 'co_present'),
    ('formacion_recursos_humanos', 'groups'),
    ('desarrollo_tecnologico', 'memory'),
    ('distinciones', 'emoji_events'),
    ('formatos', 'description'),
    ('nucleo', 'category'),
    ('auth', 'admin_panel_settings'),
]

# Modelos que se muestran en una sección distinta a la de su app: (app, modelo) → sección.
REUBICADOS = {('nucleo', 'user'): 'auth'}
# Modelos que van en el grupo principal del menú (junto a "Avance de captura"), no en su sección.
EN_PRINCIPAL = [
    ('informes', 'informe', 'Informes', 'bar_chart'),
    ('nucleo', 'periodoinforme', 'Periodos de informe', 'event_available'),
    ('nucleo', 'confirmacioninforme', 'Confirmaciones de informe', 'task_alt'),
    ('nucleo', 'configuracionentidad', 'Configuración de la entidad', 'settings'),
]


def _solo_consulta(model_admin):
    return tuple(getattr(model_admin, 'permisos_investigador', ())) == ('view',)


def menu(request):
    administrador = es_administrador(request.user)
    apps = {app['app_label']: app for app in admin.site.get_app_list(request)}
    principales = [
        {'title': 'Inicio', 'icon': 'dashboard', 'link': reverse('admin:index')},
        {'title': 'Mi informe', 'icon': 'fact_check', 'link': reverse('admin:informe')},
        {'title': 'Mi currículum', 'icon': 'article', 'link': reverse('admin:cv')},
        {'title': 'Mi perfil', 'icon': 'person', 'link': reverse('admin:perfil')},
    ]
    if administrador:
        principales.append({'title': 'Avance de captura', 'icon': 'monitoring', 'link': reverse('admin:informe_avance')})
        principales.append({'title': 'Ver por académico', 'icon': 'person_search',
                            'link': reverse('admin:ver_academico')})
    for app_label, modelo, titulo, icono in EN_PRINCIPAL:
        if administrador and request.user.has_perm(f'{app_label}.view_{modelo}'):
            principales.append({'title': titulo, 'icon': icono,
                                'link': reverse(f'admin:{app_label}_{modelo}_changelist')})
    iconos = dict(SECCIONES)
    items = {app_label: [] for app_label, _ in SECCIONES}
    for app_label, app in apps.items():
        for modelo in app['models']:
            if any((app_label, modelo['object_name'].lower()) == (a, m) for a, m, *_ in EN_PRINCIPAL):
                continue
            seccion = REUBICADOS.get((app_label, modelo['object_name'].lower()), app_label)
            if seccion not in apps:  # Sin acceso a la sección destino: se queda en la de su app.
                seccion = app_label
            if seccion not in items:
                continue
            model_admin = admin.site._registry.get(modelo['model'])
            if not administrador and model_admin is not None and _solo_consulta(model_admin):
                continue
            items[seccion].append({'title': modelo['name'], 'icon': iconos[seccion], 'link': modelo['admin_url']})
    grupos = [{'items': principales}]
    for app_label, _ in SECCIONES:
        if app_label in SECCIONES_PERFIL:
            continue  # Formación y experiencia: "Mi perfil" y, para administradores, "Trayectoria" (abajo).
        if items[app_label] and app_label in apps:
            grupos.append({'title': apps[app_label]['name'], 'separator': True, 'collapsible': True,
                           'items': items[app_label]})
    trayectoria = [item for app_label in SECCIONES_PERFIL for item in items[app_label]]
    if administrador and trayectoria:
        # Las de todos los académicos, al final y separadas de la producción.
        grupos.append({'title': 'Trayectoria', 'separator': True, 'collapsible': True, 'items': trayectoria})
    return grupos


def enlaces_cuenta(request):
    return [
        {'title': gettext_lazy('Mi perfil'), 'link': reverse('admin:perfil')},
        {'title': gettext_lazy('Mi currículum'), 'link': reverse('admin:cv')},
    ]
