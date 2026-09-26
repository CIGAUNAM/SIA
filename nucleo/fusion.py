"""Fusión de registros duplicados: reasigna todas las referencias al registro que se conserva."""

from collections import Counter

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError, transaction


class ErrorFusion(Exception):
    pass


def _es_historico(modelo):
    return hasattr(modelo, 'instance_type')  # Tablas de django-simple-history: no se reescriben.


def relaciones_hacia(modelo):
    """(modelo, campo) de cada llave foránea que apunta a `modelo`, incluidas las tablas intermedias M2M."""
    resultado = []
    for otro in apps.get_models(include_auto_created=True):
        if _es_historico(otro):
            continue
        for campo in otro._meta.get_fields():
            if (getattr(campo, 'concrete', False) and campo.is_relation and (campo.many_to_one or campo.one_to_one)
                    and campo.related_model is modelo):
                resultado.append((otro, campo))
    return resultado


def resumen_referencias(obj):
    """Cuántos registros de cada tipo apuntan a `obj` (para mostrarlo antes de fusionar)."""
    from .models import Evidencia

    conteo = Counter()
    for otro, campo in relaciones_hacia(type(obj)):
        total = otro._default_manager.filter(**{campo.name: obj}).count()
        if total:
            conteo[str(otro._meta.verbose_name_plural)] += total
    evidencias = Evidencia.objects.filter(content_type=ContentType.objects.get_for_model(obj), object_id=obj.pk)
    if evidencias.exists():
        conteo['evidencias'] += evidencias.count()
    return dict(conteo)


@transaction.atomic
def fusionar(conservar, duplicados):
    """Mueve las referencias de cada duplicado a `conservar` y elimina los duplicados.

    Si una referencia ya existía hacia `conservar` (p. ej. la misma persona como autora dos veces del mismo
    artículo), se elimina la repetida.
    """
    from .models import Evidencia, Persona

    modelo = type(conservar)
    relaciones = relaciones_hacia(modelo)
    tipo = ContentType.objects.get_for_model(modelo)
    for duplicado in duplicados:
        if duplicado.pk == conservar.pk:
            continue
        if type(duplicado) is not modelo:
            raise ErrorFusion('Solo se pueden fusionar registros del mismo tipo.')
        if isinstance(conservar, Persona) and duplicado.usuario_id:
            if conservar.usuario_id:
                raise ErrorFusion(f'"{conservar}" y "{duplicado}" tienen cuenta propia; no se pueden fusionar.')
            usuario = duplicado.usuario
            duplicado.usuario = None
            duplicado.save(update_fields=['usuario'])
            conservar.usuario = usuario
            conservar.save(update_fields=['usuario'])

        for otro, campo in relaciones:
            for fila in otro._default_manager.filter(**{campo.name: duplicado}):
                if otro is modelo and fila.pk == conservar.pk:
                    setattr(fila, campo.attname, None)  # Evita que el registro conservado apunte a sí mismo.
                else:
                    setattr(fila, campo.attname, conservar.pk)
                try:
                    with transaction.atomic():
                        fila.save(update_fields=[campo.attname])
                except IntegrityError:
                    fila.delete()
        Evidencia.objects.filter(content_type=tipo, object_id=duplicado.pk).update(object_id=conservar.pk)
        duplicado.delete()
