"""Fechas sospechosas (1900-01-01 del SIA anterior, años imposibles) y, para publicaciones, la fecha en Crossref.

Crossref solo se acepta si el DOI coincide o si el título es prácticamente el mismo y comparte al menos un autor.
Sin --aplicar solo informa; con --aplicar guarda únicamente esas correcciones de Crossref (fecha de publicación,
DOI y estado "publicado"). Las demás fechas las debe corregir quien conoce el dato.
"""

import urllib.parse
from datetime import date
from difflib import SequenceMatcher

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import models, transaction
from django.db.models import Q

from nucleo import externos
from nucleo.externos import ErrorServicio
from nucleo.models import EstadoPublicacion, StatusPublicacion
from nucleo.nombres import partes_cita
from nucleo.similitud import normalizar

ANIO_MINIMO = 1950
EXCLUIDOS = {'fecha_nacimiento'}
SIMILITUD_TITULO = 0.95


def campos_fecha(modelo):
    return [f.name for f in modelo._meta.concrete_fields
            if type(f) is models.DateField and f.name not in EXCLUIDOS and not (f.auto_now or f.auto_now_add)]


def sospechosas():
    """[(registro, [campos con fecha sospechosa])] de los modelos del SIA (sin historial)."""
    limite = date(date.today().year + 2, 12, 31)
    propias = {c.label for c in apps.get_app_configs() if str(c.path).startswith(str(settings.BASE_DIR))
               and '.venv' not in str(c.path)}
    for modelo in apps.get_models():
        if modelo.__name__.startswith('Historical') or modelo._meta.app_label not in propias:
            continue
        campos = campos_fecha(modelo)
        filtro = Q()
        for campo in campos:
            filtro |= Q(**{f'{campo}__lt': date(ANIO_MINIMO, 1, 1)}) | Q(**{f'{campo}__gt': limite})
        if not campos:
            continue
        for obj in modelo._default_manager.filter(filtro):
            malos = [c for c in campos if getattr(obj, c) and not date(ANIO_MINIMO, 1, 1) <= getattr(obj, c) <= limite]
            yield obj, malos


def _fecha_crossref(item):
    for clave in ('published-print', 'published-online', 'published', 'issued'):
        partes = (item.get(clave) or {}).get('date-parts', [[None]])[0]
        if partes and partes[0]:
            anio, mes, dia = (list(partes) + [1, 1])[:3]
            return date(anio, mes or 1, dia or 1)
    return None


def en_crossref(obj):
    """(fecha, DOI, título) de la publicación en Crossref, o None si no hay una coincidencia segura."""
    autores = next((getattr(obj, rel) for rel in ('autores', 'participantes') if hasattr(obj, rel)), None)
    apellidos = {normalizar(partes_cita(p.nombre)[0]).split()[0]
                 for p in (autores.all() if autores is not None else []) if normalizar(partes_cita(p.nombre)[0])}
    doi = getattr(obj, 'doi', '')
    try:
        if doi:
            items = [externos.obtener_json(f'https://api.crossref.org/works/{urllib.parse.quote(doi)}')['message']]
        else:
            consulta = urllib.parse.urlencode({'query.bibliographic': obj.titulo, 'query.author': ' '.join(sorted(apellidos)),
                                               'rows': 5})
            items = externos.obtener_json(f'https://api.crossref.org/works?{consulta}')['message']['items']
    except ErrorServicio:
        return None
    for item in items:
        titulo = (item.get('title') or [''])[0]
        suyos = {normalizar(a.get('family', '')).split()[0] for a in item.get('author', []) if a.get('family')}
        if doi or (SequenceMatcher(None, normalizar(obj.titulo), normalizar(titulo)).ratio() >= SIMILITUD_TITULO
                   and apellidos & suyos):
            fecha = _fecha_crossref(item)
            if fecha:
                return fecha, item.get('DOI', ''), titulo
    return None


class Command(BaseCommand):
    help = 'Lista fechas sospechosas y busca en Crossref la fecha de las publicaciones. --aplicar guarda solo esas.'

    def add_arguments(self, parser):
        parser.add_argument('--aplicar', action='store_true', help='Guarda las fechas encontradas en Crossref.')

    def handle(self, *args, aplicar=False, **options):
        total = corregibles = 0
        for obj, campos in sospechosas():
            total += 1
            texto = ', '.join(f'{c}={getattr(obj, c)}' for c in campos)
            linea = f'{obj._meta.verbose_name} #{obj.pk} «{str(obj)[:70]}» — {texto}'
            if isinstance(obj, EstadoPublicacion) or hasattr(obj, 'titulo') and hasattr(obj, 'autores'):
                encontrado = en_crossref(obj)
                if encontrado:
                    fecha, doi, titulo = encontrado
                    corregibles += 1
                    self.stdout.write(self.style.SUCCESS(f'{linea}\n    Crossref: {fecha} · DOI {doi} · «{titulo[:70]}»'))
                    if aplicar:
                        self._aplicar(obj, campos, fecha, doi)
                    continue
            self.stdout.write(f'{linea}\n    Sin dato en línea: debe corregirlo quien lo capturó.')
        accion = 'corregidas' if aplicar else 'corregibles con Crossref (usa --aplicar)'
        self.stdout.write(self.style.WARNING(f'{total} registros con fechas sospechosas; {corregibles} {accion}.'))

    @transaction.atomic
    def _aplicar(self, obj, campos, fecha, doi):
        cambios = {}
        if isinstance(obj, EstadoPublicacion):
            for campo in campos:  # Las fechas imposibles de etapas anteriores se vacían; la de publicación es la real.
                if campo != 'fecha_publicado':
                    cambios[campo] = None
            cambios.update(fecha_publicado=fecha, status=StatusPublicacion.PUBLICADO)
        else:
            cambios.update({campo: fecha for campo in campos})
        if doi and hasattr(obj, 'doi') and not obj.doi:
            cambios['doi'] = doi.lower()
        for campo, valor in cambios.items():
            setattr(obj, campo, valor)
        obj._change_reason = 'Fecha corregida con Crossref (revisar_fechas)'
        obj.save()
