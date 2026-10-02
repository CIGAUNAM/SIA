"""Calcula las cifras de las gráficas del informe anual con los registros del SIA y las compara con la referencia."""

from django.core.management.base import BaseCommand

from nucleo.cifras_informe import FIGURAS, REFERENCIA_2025_2026, Periodo


class Command(BaseCommand):
    help = 'Cifras de las gráficas del informe anual (julio-junio) y comparación con las hechas a mano.'

    def add_arguments(self, parser):
        parser.add_argument('--periodo', default='2025-2026')

    def handle(self, periodo, **options):
        p = Periodo.de(periodo)
        referencia = REFERENCIA_2025_2026 if p.nombre == '2025-2026' else {}
        iguales = distintas = 0
        for figura, funcion in FIGURAS.items():
            calculado = funcion(p)
            esperado = referencia.get(figura, {})
            self.stdout.write(self.style.MIGRATE_HEADING(f'\n{figura}'))
            for clave in list(dict.fromkeys([*esperado, *calculado])):
                c, e = calculado.get(clave, 0), esperado.get(clave)
                if e is None:
                    self.stdout.write(f'  {clave:55} {c}')
                elif c == e:
                    iguales += 1
                    self.stdout.write(self.style.SUCCESS(f'  {clave:55} {c}'))
                else:
                    distintas += 1
                    self.stdout.write(self.style.ERROR(f'  {clave:55} {c}  (informe: {e})'))
        self.stdout.write(f'\nCifras iguales al informe: {iguales}; distintas: {distintas}')
