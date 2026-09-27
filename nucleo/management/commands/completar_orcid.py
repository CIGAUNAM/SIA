"""Toma el nombre para mostrar de las personas con ORCID de su registro público en ORCID."""

from django.core.management.base import BaseCommand

from nucleo.externos import ErrorServicio, nombre_orcid
from nucleo.models import Persona


class Command(BaseCommand):
    help = ('Reemplaza el nombre para mostrar de las personas con ORCID por el de su registro público. '
            'Sin --aplicar solo muestra los cambios.')

    def add_arguments(self, parser):
        parser.add_argument('--aplicar', action='store_true', help='Guarda los cambios.')

    def handle(self, *args, aplicar=False, **options):
        cambios = 0
        for persona in Persona.objects.exclude(orcid='').order_by('nombre'):
            try:
                nombre = nombre_orcid(persona.orcid)
            except ErrorServicio as error:
                self.stderr.write(f'{persona.orcid} ({persona}): {error}')
                continue
            if not nombre or nombre == persona.nombre:
                continue
            self.stdout.write(f'{persona.orcid}: «{persona.nombre}» → «{nombre}»')
            if aplicar:
                persona.nombre = nombre
                persona.save(update_fields=['nombre', 'actualizado'])
            cambios += 1
        accion = 'actualizadas' if aplicar else 'por actualizar (usa --aplicar para guardar)'
        self.stdout.write(self.style.SUCCESS(f'{cambios} personas {accion}.'))
