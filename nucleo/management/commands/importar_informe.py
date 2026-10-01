"""Carga a la base las hojas de cálculo con que se armó el informe anual (Eje 2, 3 y 4, planta académica…).

Sirve para comprobar que el modelo del SIA admite todo lo que pide el informe y para arrancar una base con esos
datos. Por cada hoja informa qué se creó, qué ya existía y qué no se pudo cargar (y por qué). Sin --aplicar todo
corre en una transacción que se revierte (simulacro).
"""

import importlib
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from nucleo.importacion.base import Contexto

#: Módulos de `nucleo.importacion`, en orden: primero las personas, de las que dependen los demás.
MODULOS = ['personal', 'produccion', 'vinculacion_academica', 'docencia', 'sociedad']


class _Simulacro(Exception):
    pass


class Command(BaseCommand):
    help = 'Importa las hojas de cálculo del informe anual. Sin --aplicar es un simulacro.'

    def add_arguments(self, parser):
        parser.add_argument('carpeta', help='Carpeta con los archivos .xlsx del informe.')
        parser.add_argument('--aplicar', action='store_true', help='Guarda los cambios (si no, se revierten).')
        parser.add_argument('--solo', nargs='*', choices=MODULOS, help='Importa solo estos módulos.')
        parser.add_argument('--detalle', type=int, default=8, help='Rechazos y avisos a mostrar por hoja.')

    def handle(self, carpeta, aplicar=False, solo=None, detalle=8, **options):
        carpeta = Path(carpeta)
        if not carpeta.is_dir():
            raise CommandError(f'No existe la carpeta {carpeta}')
        ctx = Contexto('Importado de las hojas del informe anual', carpeta)
        try:
            with transaction.atomic():
                for nombre in solo or MODULOS:
                    modulo = importlib.import_module(f'nucleo.importacion.{nombre}')
                    modulo.importar(ctx, ctx.libro(modulo.ARCHIVO))
                if not aplicar:
                    raise _Simulacro
        except _Simulacro:
            pass
        self.reporte(ctx, detalle)
        estado = 'aplicada' if aplicar else 'simulada (nada se guardó; usa --aplicar)'
        self.stdout.write(self.style.SUCCESS(f'Importación {estado}.'))

    def reporte(self, ctx, detalle):
        for hoja in ctx.hojas:
            self.stdout.write(self.style.MIGRATE_HEADING(f'\n{hoja.nombre} ({hoja.filas} filas)'))
            for etiqueta, conteo in (('creados', hoja.creados), ('ya existían', hoja.existentes)):
                if conteo:
                    self.stdout.write(f'  {etiqueta}: ' + ', '.join(f'{n} {m}' for m, n in conteo.items()))
            for etiqueta, lista, estilo in (('no cargados', hoja.rechazados, self.style.ERROR),
                                            ('avisos', hoja.avisos, self.style.WARNING)):
                if lista:
                    self.stdout.write(estilo(f'  {etiqueta}: {len(lista)}'))
                    for fila, motivo in lista[:detalle]:
                        self.stdout.write(f'    fila {fila}: {motivo}')
        self.stdout.write(f'\nPersonas nuevas: {ctx.personas_creadas}; instituciones nuevas: '
                          f'{getattr(ctx, "_creadas_instituciones", 0)}; revistas nuevas: '
                          f'{getattr(ctx, "_creadas_revistas", 0)}')
