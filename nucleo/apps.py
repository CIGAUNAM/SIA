from django.apps import AppConfig


class NucleoConfig(AppConfig):
    name = 'nucleo'
    verbose_name = 'Catálogos y personas'

    def ready(self):
        from . import signals  # noqa: F401
