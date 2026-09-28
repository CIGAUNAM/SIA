"""Grupos de acceso. Sus permisos se definen aquí y se sincronizan en cada `migrate`.

- **Académicos** (investigadores, técnicos académicos, posdoctorantes): capturan su propia producción; cada
  ModelAdmin declara en `permisos_investigador` qué acciones les concede.
- **Administración** (personal administrativo): ve y edita la producción de todos (con motivo obligatorio al
  editar un registro ajeno, que queda en el historial), mantiene catálogos, el informe anual, la configuración de
  la entidad y las cuentas. No borra producción ajena ni gestiona superusuarios, grupos o permisos.
- **Sysadmin**: el superusuario de Django (sin grupo).

El `tipo` de la cuenta (investigador, técnico...) describe a la persona, no su acceso.
"""

from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

GRUPO_ACADEMICOS = 'Académicos'
GRUPO_ADMINISTRACION = 'Administración'

#: Apps cuyos modelos no gestiona Administración (grupos y permisos: solo el superusuario).
APPS_SOLO_SYSADMIN = {'auth'}


def es_sysadmin(user):
    return user.is_active and user.is_superuser


def _acciones_por_modelo(obtener_acciones):
    """{modelo: acciones} para cada ModelAdmin registrado; los inlines heredan las acciones de su ModelAdmin."""
    resultado = {}
    for modelo, model_admin in admin.site._registry.items():
        acciones = set(obtener_acciones(modelo, model_admin))
        resultado.setdefault(modelo, set()).update(acciones)
        for inline in model_admin.inlines:
            resultado.setdefault(inline.model, set()).update(acciones)
    return resultado


def _permisos(acciones_por_modelo):
    permisos = []
    for modelo, acciones in acciones_por_modelo.items():
        content_type = ContentType.objects.get_for_model(modelo)
        codenames = [f'{accion}_{modelo._meta.model_name}' for accion in acciones]
        permisos.extend(Permission.objects.filter(content_type=content_type, codename__in=codenames))
    return permisos


def _acciones_administracion(modelo, model_admin):
    from .admin_base import CatalogoAdmin, VerificableAdmin

    if modelo._meta.app_label in APPS_SOLO_SYSADMIN:
        return ()
    if isinstance(model_admin, (VerificableAdmin, CatalogoAdmin)):
        return ('view', 'add', 'change', 'delete')  # Borrar catálogos es parte de fusionar duplicados.
    return ('view', 'add', 'change')  # Producción y cuentas: sin borrar.


def sincronizar_grupos():
    academicos, _ = Group.objects.get_or_create(name=GRUPO_ACADEMICOS)
    academicos.permissions.set(_permisos(_acciones_por_modelo(
        lambda modelo, model_admin: getattr(model_admin, 'permisos_investigador', ()))))

    administracion, _ = Group.objects.get_or_create(name=GRUPO_ADMINISTRACION)
    permisos = _permisos(_acciones_por_modelo(_acciones_administracion))
    permisos.append(Permission.objects.get(content_type__app_label='nucleo', codename='ver_todo'))
    administracion.permissions.set(permisos)
    return academicos, administracion
