"""Fechas sospechosas (1900-01-01 del SIA anterior, años imposibles) y su corrección, de la más a la menos segura:

1. Publicaciones: la fecha en Crossref (DOI igual, o título casi idéntico con un autor en común).
2. Año con un dígito mal tecleado (2916 → 2016), si el candidato es único o el más cercano a la otra fecha.
3. Evento con término imposible: término = inicio (evento de un día).
4. Lo demás: "sin fecha" (vacío); en el formulario la fecha sigue siendo obligatoria, así que se completa al editar.

Sin --aplicar solo informa. Con --aplicar guarda, con el motivo en el historial de cada registro.
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


PLACEHOLDER = date(1900, 1, 1)  # "Sin fecha" en el SIA anterior.


def por_digito(fecha, antes_de=None, despues_de=None):
    """Año con un dígito mal tecleado (2916 → 2016): el único año válido que resulta de cambiar un dígito, o el más
    cercano a la otra fecha del registro, respetando el orden inicio ≤ fin. None si no hay uno claro."""
    if fecha == PLACEHOLDER:
        return None
    anio, hoy = str(fecha.year), date.today()
    candidatos = set()
    for posicion in range(len(anio)):
        for digito in '0123456789':
            try:
                otra = fecha.replace(year=int(anio[:posicion] + digito + anio[posicion + 1:]))
            except ValueError:
                continue
            if (otra != fecha and date(ANIO_MINIMO, 1, 1) <= otra <= hoy and (antes_de is None or otra <= antes_de)
                    and (despues_de is None or otra >= despues_de)):
                candidatos.add(otra)
    if len(candidatos) == 1:
        return candidatos.pop()
    referencia = antes_de or despues_de
    if referencia and candidatos:
        orden = sorted(candidatos, key=lambda c: abs((c - referencia).days))
        if len(orden) == 1 or abs((orden[0] - referencia).days) < abs((orden[1] - referencia).days):
            return orden[0]
    return None


def _valida(fecha):
    return fecha is not None and date(ANIO_MINIMO, 1, 1) <= fecha <= date(date.today().year + 2, 12, 31)


def correcciones(obj, campos):
    """{campo: (valor, motivo)} para las fechas sospechosas de `obj` que no se resolvieron con Crossref."""
    from nucleo.models import Evento

    resultado = {}
    for campo in campos:
        valor = getattr(obj, campo)
        inicio_valido = getattr(obj, 'fecha_inicio', None) if _valida(getattr(obj, 'fecha_inicio', None)) else None
        fin_valido = getattr(obj, 'fecha_fin', None) if _valida(getattr(obj, 'fecha_fin', None)) else None
        despues = inicio_valido if campo == 'fecha_fin' else None
        antes = fin_valido if campo == 'fecha_inicio' else None
        if (nueva := por_digito(valor, antes_de=antes, despues_de=despues)) is not None:
            resultado[campo] = (nueva, f'año mal tecleado ({valor.year} → {nueva.year})')
        elif isinstance(obj, Evento) and campo == 'fecha_fin' and inicio_valido:
            resultado[campo] = (inicio_valido, 'evento de un día: término = inicio')
        elif type(obj)._meta.get_field(campo).null:
            resultado[campo] = (None, 'sin fecha conocida')
    return resultado


class Command(BaseCommand):
    help = 'Lista fechas sospechosas y busca en Crossref la fecha de las publicaciones. --aplicar guarda solo esas.'

    def add_arguments(self, parser):
        parser.add_argument('--aplicar', action='store_true', help='Guarda las fechas encontradas en Crossref.')

    def handle(self, *args, aplicar=False, **options):
        total = con_crossref = deducidas = sin_fecha = 0
        for obj, campos in list(sospechosas()):
            total += 1
            texto = ', '.join(f'{c}={getattr(obj, c)}' for c in campos)
            self.stdout.write(f'{obj._meta.verbose_name} #{obj.pk} «{str(obj)[:70]}» — {texto}')
            if hasattr(obj, 'titulo') and hasattr(obj, 'autores') and (encontrado := en_crossref(obj)):
                fecha, doi, titulo = encontrado
                con_crossref += 1
                self.stdout.write(self.style.SUCCESS(f'    Crossref: {fecha} · DOI {doi} · «{titulo[:70]}»'))
                if aplicar:
                    self._aplicar(obj, campos, fecha, doi)
                continue
            cambios = correcciones(obj, campos)
            for campo, (valor, motivo) in cambios.items():
                self.stdout.write(f'    {campo} → {valor or "sin fecha"} ({motivo})')
                if valor is None:
                    sin_fecha += 1
                else:
                    deducidas += 1
            if aplicar and cambios:
                with transaction.atomic():
                    for campo, (valor, _) in cambios.items():
                        setattr(obj, campo, valor)
                    motivo = 'Fecha revisada: ' + '; '.join(f'{c}: {m}' for c, (_, m) in cambios.items())
                    obj._change_reason = motivo[:100]  # Límite del historial.
                    obj.save()
        estado = 'aplicadas' if aplicar else 'propuestas (usa --aplicar)'
        self.stdout.write(self.style.WARNING(
            f'{total} registros con fechas sospechosas. Correcciones {estado}: {con_crossref} con Crossref, '
            f'{deducidas} fechas deducidas, {sin_fecha} fechas a "sin fecha".'))

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
