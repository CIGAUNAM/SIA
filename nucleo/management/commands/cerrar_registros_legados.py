"""Cierra los registros del SIA anterior que quedaron abiertos (sin fecha de término) y nadie volvió a reportar.

El SIA anterior dejó de capturarse en 2019: una red, una sociedad, una comisión o un proyecto que empezó antes y
sigue sin fecha de término contaría como vigente en todos los informes. Si no aparece en las hojas del informe
(`importar_informe`), se cierra al 31/12/2019 con el motivo en su historial; quien siga ahí lo vuelve a registrar.
Las tesis en proceso no se tocan: se dejan de contar al rebasar su plazo (ver `cifras_informe.PLAZO_TESIS`).

Además, los periodos que cubren las hojas del informe (desde --primer-periodo) son la versión oficial: un registro
anterior que el SIA daba por vigente en ellos (p. ej. con un término previsto en 2025) pero que nadie reportó, se cierra
el día antes del primer periodo reportado.
Sin --aplicar es un simulacro.
"""

from collections import Counter
from datetime import date, timedelta

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from nucleo.models import Periodo

REPORTADO = ('Importado de las hojas del informe anual', 'Reportado de nuevo en las hojas del informe anual')
#: Las tesis se dejan de contar por plazo; la experiencia profesional sin término es el puesto actual.
EXCLUIDOS = {'DireccionTesis', 'ExperienciaProfesional', 'LineaInvestigacion', 'CapacidadPotencialidad'}
MOTIVO = 'Cerrado: abierto desde el SIA anterior y no se volvió a reportar'
MOTIVO_OFICIAL = 'Cerrado: el informe oficial no lo reporta en sus periodos'


def modelos_con_vigencia():
    propias = {c.label for c in apps.get_app_configs()
               if str(c.path).startswith(str(settings.BASE_DIR)) and '.venv' not in str(c.path)}
    for modelo in apps.get_models():
        if (modelo._meta.app_label in propias and not modelo.__name__.startswith('Historical')
                and modelo.__name__ not in EXCLUIDOS):
            if issubclass(modelo, Periodo):
                yield modelo, 'fecha_inicio'
            elif modelo.__name__ == 'RedAcademica':
                yield modelo, 'fecha_constitucion'


class Command(BaseCommand):
    help = 'Cierra al 31/12/2019 los registros abiertos del SIA anterior que no se volvieron a reportar.'

    def add_arguments(self, parser):
        parser.add_argument('--aplicar', action='store_true')
        parser.add_argument('--antes-de', default='2020-01-01', help='Solo registros que empezaron antes de esta fecha.')
        parser.add_argument('--cierre', default='2019-12-31')
        parser.add_argument('--primer-periodo', default='2024-07-01',
                            help='Inicio del primer periodo que cubren las hojas del informe.')

    def handle(self, aplicar=False, antes_de='2020-01-01', cierre='2019-12-31', primer_periodo='2024-07-01', **options):
        corte, fin = date.fromisoformat(antes_de), date.fromisoformat(cierre)
        primero = date.fromisoformat(primer_periodo)
        cuenta = Counter()
        with transaction.atomic():
            for modelo, campo_inicio in modelos_con_vigencia():
                reportados = set(modelo.history.filter(history_change_reason__in=REPORTADO)
                                 .values_list('id', flat=True))
                for obj in modelo.objects.filter(fecha_fin__isnull=True, **{f'{campo_inicio}__lt': corte}) \
                        .exclude(pk__in=reportados):
                    inicio = getattr(obj, campo_inicio)
                    obj.fecha_fin = max(fin, inicio)
                    obj._change_reason = MOTIVO
                    obj.save()
                    cuenta[modelo._meta.verbose_name_plural] += 1
                for obj in modelo.objects.filter(fecha_fin__gte=primero, **{f'{campo_inicio}__lt': primero}) \
                        .exclude(pk__in=reportados):
                    obj.fecha_fin = primero - timedelta(days=1)
                    obj._change_reason = MOTIVO_OFICIAL
                    obj.save()
                    cuenta[f'{modelo._meta.verbose_name_plural} (sin reportar en el informe oficial)'] += 1
            for nombre, n in sorted(cuenta.items()):
                self.stdout.write(f'  {nombre}: {n}')
            if not aplicar:
                transaction.set_rollback(True)
        estado = 'cerrados' if aplicar else 'por cerrar (simulacro; usa --aplicar)'
        self.stdout.write(self.style.SUCCESS(f'{sum(cuenta.values())} registros {estado}.'))
