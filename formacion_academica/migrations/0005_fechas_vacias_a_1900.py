"""Fechas a 1900 ("sin fecha") antes de volver a hacerlas obligatorias (migración siguiente).

Va aparte porque PostgreSQL no permite alterar una tabla en la misma transacción en que se actualizaron sus filas.
"""

import datetime

from django.db import migrations

CAMPOS = [
    ('cursoespecializacion', 'fecha_inicio'),
    ('historicalcursoespecializacion', 'fecha_inicio'),
    ('historicalpostdoctorado', 'fecha_inicio'),
    ('postdoctorado', 'fecha_inicio'),
]


def vacias_a_1900(apps, schema_editor):
    """"Sin fecha" se guarda como 01/01/1900 (se muestra «s.f.»)."""
    for modelo, campo in CAMPOS:
        apps.get_model('formacion_academica', modelo).objects.filter(**{campo: None}).update(**{campo: datetime.date(1900, 1, 1)})


class Migration(migrations.Migration):

    dependencies = [
        ('formacion_academica', '0004_fechas_sin_dato'),
    ]

    operations = [migrations.RunPython(vacias_a_1900, migrations.RunPython.noop)]
