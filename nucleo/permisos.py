from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

GRUPO_INVESTIGADORES = 'Investigadores'


def sincronizar_grupo_investigadores():
    """Otorga al grupo "Investigadores" los permisos que declara cada ModelAdmin en `permisos_investigador`.

    Los modelos de los inlines reciben los mismos permisos que su ModelAdmin padre.
    """
    grupo, _ = Group.objects.get_or_create(name=GRUPO_INVESTIGADORES)
    acciones_por_modelo = {}
    for modelo, model_admin in admin.site._registry.items():
        acciones = set(getattr(model_admin, 'permisos_investigador', ()))
        acciones_por_modelo.setdefault(modelo, set()).update(acciones)
        for inline in model_admin.inlines:
            acciones_por_modelo.setdefault(inline.model, set()).update(acciones)

    permisos = []
    for modelo, acciones in acciones_por_modelo.items():
        content_type = ContentType.objects.get_for_model(modelo)
        codenames = [f'{accion}_{modelo._meta.model_name}' for accion in acciones]
        permisos.extend(Permission.objects.filter(content_type=content_type, codename__in=codenames))
    grupo.permissions.set(permisos)
    return grupo
