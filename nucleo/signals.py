from django.apps import apps
from django.contrib.auth.management import create_permissions
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .permisos import sincronizar_grupos


@receiver(post_migrate, sender=apps.get_app_config('nucleo'))
def configurar_permisos(sender, using, **kwargs):
    # post_migrate se emite app por app: se crean primero los permisos de todas para poder asignarlos.
    for app_config in apps.get_app_configs():
        create_permissions(app_config, verbosity=0, using=using)
    sincronizar_grupos()
