from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from nucleo.normalizacion import normalizar


class Command(BaseCommand):
    help = 'Normaliza datos existentes (jerarquía de instituciones, ámbitos, DOIs, métricas). Es idempotente.'

    def handle(self, **options):
        with transaction.atomic():
            resultado = normalizar(apps.get_model, settings.PAIS_SEDE)
        for concepto, total in resultado.items():
            self.stdout.write(f'  {concepto}: {total}')
