"""Países → cities_light (preparación): carga el catálogo y relaciona cada país anterior con su equivalente.

- `cities_light.Country` se llena desde `nucleo/fixtures/paises.json` (países ISO de GeoNames con nombre en español
  y, sin código ISO, los que usaba el SIA anterior), con ids fijos.
- `Pais.equivalente` guarda, de forma temporal, el país del catálogo al que corresponde cada país anterior: por
  código ISO, por los alias de abajo o, sin código, por nombre. Si alguno no tiene equivalente, la migración se
  detiene sin cambiar nada.
"""

import json
from pathlib import Path

import django.db.models.deletion
from django.core.management.color import no_style
from django.db import migrations, models

FIXTURE = Path(__file__).resolve().parent.parent / 'fixtures' / 'paises.json'
ALIAS = {'EU': 'US', '1': 'NL', '67': 'KR', '78': 'AE'}  # Mismo país con otro código en el SIA anterior.


def cargar_paises(apps, schema_editor):
    Country = apps.get_model('cities_light', 'Country')
    existentes = set(Country.objects.values_list('pk', flat=True))
    nuevos = [Country(pk=o['pk'], **o['fields']) for o in json.loads(FIXTURE.read_text('utf-8'))
              if o['pk'] not in existentes]
    if existentes and nuevos:
        raise RuntimeError('cities_light.Country ya tiene datos distintos del fixture de países; revísalo antes de '
                           'migrar (no se importa de GeoNames).')
    Country.objects.bulk_create(nuevos)
    conexion = schema_editor.connection
    with conexion.cursor() as cursor:  # Los ids se dieron a mano: la secuencia debe seguir después del último.
        for sql in conexion.ops.sequence_reset_sql(no_style(), [Country]):
            cursor.execute(sql)


def relacionar(apps, schema_editor):
    Pais = apps.get_model('nucleo', 'Pais')
    Country = apps.get_model('cities_light', 'Country')
    por_codigo = dict(Country.objects.exclude(code2=None).values_list('code2', 'pk'))
    por_nombre = dict(Country.objects.filter(code2=None).values_list('name', 'pk'))
    faltan = []
    for pais in Pais.objects.all():
        codigo = (pais.codigo or '').upper()
        pais.equivalente_id = por_codigo.get(ALIAS.get(codigo, codigo)) or por_nombre.get(pais.nombre)
        if pais.equivalente_id is None:
            faltan.append(f'{pais.nombre} ({pais.codigo})')
        pais.save(update_fields=['equivalente'])
    if faltan:
        raise RuntimeError('Países sin equivalente en el catálogo: ' + ', '.join(faltan))


class Migration(migrations.Migration):

    dependencies = [
        ('nucleo', '0011_ambito_manual'),
        ('cities_light', '0013_alter_city_alternate_names_alter_city_country_and_more'),
    ]

    operations = [
        migrations.RunPython(cargar_paises, migrations.RunPython.noop),
        migrations.AddField(
            model_name='pais',
            name='equivalente',
            field=models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING,
                                    related_name='+', to='cities_light.country'),
        ),
        migrations.RunPython(relacionar, migrations.RunPython.noop),
    ]
