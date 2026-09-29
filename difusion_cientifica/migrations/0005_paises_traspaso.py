"""Países → cities_light (1/2): quita la restricción de las llaves de país y traduce sus valores."""

import django.db.models.deletion
from django.db import migrations, models
from django.db.models import F

CAMPOS = [
    ('difusion_cientifica', 'historicalmemoriainextenso', 'pais'),
    ('difusion_cientifica', 'historicalparticipacioneventoacademico', 'pais'),
    ('difusion_cientifica', 'memoriainextenso', 'pais'),
    ('difusion_cientifica', 'participacioneventoacademico', 'pais'),
]


def remapear(apps, schema_editor):
    """Traduce cada llave de país del catálogo anterior (nucleo.Pais) a su equivalente en cities_light.Country.

    En dos pasos (a negativo y de vuelta) porque los ids de ambos catálogos se traslapan.
    """
    Pais = apps.get_model('nucleo', 'Pais')
    equivalente = dict(Pais.objects.values_list('pk', 'equivalente_id'))
    for app_label, modelo, campo in CAMPOS:
        Modelo = apps.get_model(app_label, modelo)
        columna = f'{campo}_id'
        for anterior, nuevo in equivalente.items():
            Modelo.objects.filter(**{columna: anterior}).update(**{columna: -nuevo})
        Modelo.objects.filter(**{f'{columna}__lt': 0}).update(**{columna: F(columna) * -1})


class Migration(migrations.Migration):

    dependencies = [
        ('difusion_cientifica', '0004_ambito_manual'),
        ('nucleo', '0012_paises_catalogo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memoriainextenso',
            name='pais',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.PROTECT, to='nucleo.pais', verbose_name='país'),
        ),
        migrations.AlterField(
            model_name='participacioneventoacademico',
            name='pais',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.PROTECT, to='nucleo.pais', verbose_name='país'),
        ),
        migrations.RunPython(remapear, migrations.RunPython.noop),
    ]
