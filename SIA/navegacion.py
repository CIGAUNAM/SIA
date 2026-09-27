"""Menú lateral y enlaces de cuenta del admin (Unfold).

El menú sigue el orden de las secciones del informe. A los académicos se les ocultan los
catálogos que solo pueden consultar (países, índices...), que siguen disponibles en los
campos de autocompletado.
"""

from django.contrib import admin
from django.urls import reverse
from django.utils.translation import gettext_lazy

from nucleo.admin_base import VerificableAdmin, es_administrador

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


def _funcion_contador(modelo):
    """Unfold solo acepta insignias como ruta importable: se registra una función por catálogo en este módulo."""
    nombre = f'contador_{modelo._meta.app_label}_{modelo._meta.model_name}'
    if nombre not in globals():
        def contador(request):
            return modelo.objects.filter(verificado=False).count() or None
        globals()[nombre] = contador
    return f'{__name__}.{nombre}'


def _solo_consulta(model_admin):
    return tuple(getattr(model_admin, 'permisos_investigador', ())) == ('view',)


def menu(request):
    administrador = es_administrador(request.user)
    apps = {app['app_label']: app for app in admin.site.get_app_list(request)}
    principales = [
        {'title': 'Inicio', 'icon': 'dashboard', 'link': reverse('admin:index')},
        {'title': 'Mi informe', 'icon': 'fact_check', 'link': reverse('admin:informe')},
        {'title': 'Mi currículum', 'icon': 'article', 'link': reverse('admin:cv')},
    ]
    if administrador:
        principales.append({'title': 'Avance de captura', 'icon': 'monitoring', 'link': reverse('admin:informe_avance')})
    if request.user.has_perm('nucleo.change_configuracionentidad'):
        principales.append({'title': 'Configuración de la entidad', 'icon': 'settings',
                            'link': reverse('admin:nucleo_configuracionentidad_changelist')})
    iconos = dict(SECCIONES)
    items = {app_label: [] for app_label, _ in SECCIONES}
    for app_label, app in apps.items():
        for modelo in app['models']:
            seccion = REUBICADOS.get((app_label, modelo['object_name'].lower()), app_label)
            if seccion not in apps:  # Sin acceso a la sección destino: se queda en la de su app.
                seccion = app_label
            if seccion not in items:
                continue
            model_admin = admin.site._registry.get(modelo['model'])
            if not administrador and model_admin is not None and _solo_consulta(model_admin):
                continue
            item = {'title': modelo['name'], 'icon': iconos[seccion], 'link': modelo['admin_url']}
            if administrador and isinstance(model_admin, VerificableAdmin):
                item['badge'] = _funcion_contador(modelo['model'])
            items[seccion].append(item)
    grupos = [{'items': principales}]
    for app_label, _ in SECCIONES:
        if items[app_label] and app_label in apps:
            grupos.append({'title': apps[app_label]['name'], 'separator': True, 'collapsible': True,
                           'items': items[app_label]})
    return grupos


def enlaces_cuenta(request):
    return [
        {'title': gettext_lazy('Mi perfil'), 'link': reverse('admin:nucleo_user_change', args=[request.user.pk])},
        {'title': gettext_lazy('Mi currículum'), 'link': reverse('admin:cv')},
    ]
