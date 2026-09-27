from django.apps import apps
from django.contrib.auth.management import create_permissions
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

from .models import Persona, User
from .permisos import sincronizar_grupo_investigadores


@receiver(post_save, sender=User)
def sincronizar_persona(sender, instance, raw, **kwargs):
    """Toda cuenta tiene una Persona con el mismo nombre, para figurar como autor, tutor, etc."""
    if raw:
        return
    Persona.objects.update_or_create(
        usuario=instance,
        defaults={'nombre': instance.first_name or instance.email.split('@')[0], 'apellidos': instance.last_name,
                  'email': '' if instance.sin_correo else instance.email, 'verificado': True},
    )


@receiver(post_migrate, sender=apps.get_app_config('nucleo'))
def configurar_permisos(sender, using, **kwargs):
    # post_migrate se emite app por app: se crean primero los permisos de todas para poder asignarlos.
    for app_config in apps.get_app_configs():
        create_permissions(app_config, verbosity=0, using=using)
    sincronizar_grupo_investigadores()
