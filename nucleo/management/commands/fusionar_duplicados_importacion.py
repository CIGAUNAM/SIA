"""Une lo importado de las hojas del informe con lo que ya estaba en el SIA cuando es lo mismo.

Compara cada registro nuevo (importado) con los anteriores por su nombre normalizado (y país, académico o revista
cuando aplica). Si coinciden exactamente, se fusionan y se conserva el más completo: el de más campos llenos y, a
igualdad, el de más registros que lo usan; los datos que solo tenía el otro se copian. Los casos parecidos que no
son idénticos solo se listan para revisarlos a mano. Sin --aplicar es un simulacro.
"""

import re
from difflib import SequenceMatcher

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import transaction

from nucleo.fusion import fusionar, resumen_referencias
from nucleo.similitud import normalizar

IMPORTADO = 'Importado de las hojas del informe anual'
#: modelo → (campo de nombre, campos que también deben coincidir)
MODELOS = [
    ('nucleo.Persona', 'nombre', ()),
    ('nucleo.Institucion', 'nombre', ('pais_id', 'padre_id')),
    ('nucleo.Revista', 'nombre', ()),
    ('nucleo.Evento', 'nombre', ('fecha_inicio',)),
    ('nucleo.Asignatura', 'nombre', ()),
    ('nucleo.ProgramaAcademico', 'nombre', ('nivel',)),
    ('nucleo.MedioDivulgacion', 'nombre', ('tipo',)),
    ('nucleo.Libro', 'titulo', ()),
    ('vinculacion.RedAcademica', 'nombre', ()),
    ('investigacion.ProyectoInvestigacion', 'nombre', ()),
    ('investigacion.ArticuloCientifico', 'titulo', ()),
    ('distinciones.SociedadCientifica', 'nombre', ('usuario_id',)),
]


def clave(texto):
    return re.sub(r'\s+', ' ', normalizar(re.sub(r'\([^)]*\)', ' ', texto or ''))).strip()


def completitud(obj):
    llenos = sum(1 for f in obj._meta.concrete_fields
                 if not f.primary_key and getattr(obj, f.attname) not in (None, '', 0, False))
    return llenos, sum(resumen_referencias(obj).values())


def completar(conservar, otro):
    """Copia al registro que se conserva los datos que solo tenía el otro."""
    cambios = False
    for f in conservar._meta.concrete_fields:
        if f.primary_key or f.name in ('creado', 'actualizado', 'creado_por'):
            continue
        if getattr(conservar, f.attname) in (None, '') and getattr(otro, f.attname) not in (None, ''):
            setattr(conservar, f.attname, getattr(otro, f.attname))
            cambios = True
    return cambios


class Command(BaseCommand):
    help = 'Fusiona lo importado del informe con los registros anteriores idénticos (conserva el más completo).'

    def add_arguments(self, parser):
        parser.add_argument('--aplicar', action='store_true')
        parser.add_argument('--detalle', type=int, default=15)

    def handle(self, aplicar=False, detalle=15, **options):
        with transaction.atomic():
            for etiqueta, campo, extra in MODELOS:
                modelo = apps.get_model(etiqueta)
                nuevos_ids = set(modelo.history.filter(history_change_reason=IMPORTADO, history_type='+')
                                 .values_list('id', flat=True))
                anteriores = {}
                for obj in modelo.objects.exclude(pk__in=nuevos_ids):
                    anteriores.setdefault((clave(getattr(obj, campo)), *(getattr(obj, e) for e in extra)), []).append(obj)
                fusiones, dudosos = [], []
                for nuevo in modelo.objects.filter(pk__in=nuevos_ids):
                    k = (clave(getattr(nuevo, campo)), *(getattr(nuevo, e) for e in extra))
                    if not k[0]:
                        continue
                    iguales = anteriores.get(k)
                    if iguales:
                        fusiones.append((nuevo, iguales[0]))
                    elif len(k[0]) > 15 and modelo.__name__ != 'Persona':
                        candidato = next((o for (n, *resto), lista in anteriores.items() for o in lista
                                          if tuple(resto) == k[1:] and n[:6] == k[0][:6]
                                          and SequenceMatcher(None, n, k[0]).ratio() >= 0.92), None)
                        if candidato:
                            dudosos.append((nuevo, candidato))
                for nuevo, anterior in fusiones:
                    conservar, quitar = (nuevo, anterior) if completitud(nuevo) > completitud(anterior) else (anterior, nuevo)
                    if completar(conservar, quitar):
                        conservar._change_reason = 'Datos completados al fusionar con su duplicado'
                        conservar.save()
                    fusionar(conservar, [quitar])
                titulo = f'{modelo._meta.verbose_name_plural}: {len(fusiones)} fusionados, {len(dudosos)} por revisar'
                self.stdout.write(self.style.MIGRATE_HEADING(titulo))
                for nuevo, anterior in fusiones[:detalle]:
                    self.stdout.write(f'  = «{str(nuevo)[:70]}»')
                for nuevo, anterior in dudosos[:detalle]:
                    self.stdout.write(self.style.WARNING(f'  ? «{str(nuevo)[:60]}»  ~  «{str(anterior)[:60]}»'))
            if not aplicar:
                transaction.set_rollback(True)
        self.stdout.write(self.style.SUCCESS('Fusión aplicada.' if aplicar else 'Simulacro: nada se guardó (usa --aplicar).'))
