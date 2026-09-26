"""Bitácora de cambios con django-simple-history."""

from django.db import models
from simple_history import register

EXCLUIDOS = {'User'}  # El historial de cuentas guardaría hashes de contraseña.


def registrar_historial(espacio):
    """Registra el historial de todos los modelos concretos definidos en el módulo `espacio` (su `globals()`)."""
    for objeto in list(espacio.values()):
        if (isinstance(objeto, type) and issubclass(objeto, models.Model) and not objeto._meta.abstract
                and objeto.__module__ == espacio['__name__'] and objeto.__name__ not in EXCLUIDOS):
            register(objeto)
