"""Inglaterra y Gales (sin código ISO) se unen a Reino Unido.

Para bases ya migradas con `0012`: cada llave hacia esos países (incluido el historial) pasa a Reino Unido, sus
nombres quedan como nombres alternos de Reino Unido y se eliminan. En una instalación nueva no existen (el fixture
ya no los trae) y no hace nada.
"""

from django.db import migrations

UNIR = ('Inglaterra', 'Gales')


def unir(apps, schema_editor):
    Country = apps.get_model('cities_light', 'Country')
    reino_unido = Country.objects.filter(code2='GB').first()
    partes = list(Country.objects.filter(code2=None, name__in=UNIR))
    if reino_unido is None or not partes:
        return
    ids = [p.pk for p in partes]
    for modelo in apps.get_models():
        for campo in modelo._meta.concrete_fields:
            if campo.is_relation and campo.related_model is Country:
                modelo._default_manager.filter(**{f'{campo.attname}__in': ids}).update(
                    **{campo.attname: reino_unido.pk})
    alternos = [x for x in (reino_unido.alternate_names or '').split(';') if x]
    alternos += [p.name for p in partes if p.name not in alternos]
    reino_unido.alternate_names = ';'.join(alternos)
    reino_unido.save(update_fields=['alternate_names'])
    Country.objects.filter(pk__in=ids).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('nucleo', '0015_eliminar_pais'),
    ]

    operations = [migrations.RunPython(unir, migrations.RunPython.noop)]
