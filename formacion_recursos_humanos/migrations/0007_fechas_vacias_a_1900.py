"""Fechas a 1900 ("sin fecha") antes de volver a hacerlas obligatorias (migración siguiente).

Va aparte porque PostgreSQL no permite alterar una tabla en la misma transacción en que se actualizaron sus filas.
"""

import datetime

from django.db import migrations

CAMPOS = [
    ('asesoriaestudiante', 'fecha_inicio'),
    ('comitetutoral', 'fecha_inicio'),
    ('direcciontesis', 'fecha_inicio'),
    ('grupoinvestigacioninterno', 'fecha_inicio'),
    ('historicalasesoriaestudiante', 'fecha_inicio'),
    ('historicalcomitetutoral', 'fecha_inicio'),
    ('historicaldirecciontesis', 'fecha_inicio'),
    ('historicalgrupoinvestigacioninterno', 'fecha_inicio'),
    ('historicalsupervisionpostdoctoral', 'fecha_inicio'),
    ('supervisionpostdoctoral', 'fecha_inicio'),
]


def vacias_a_1900(apps, schema_editor):
    """"Sin fecha" se guarda como 01/01/1900 (se muestra «s.f.»)."""
    for modelo, campo in CAMPOS:
        apps.get_model('formacion_recursos_humanos', modelo).objects.filter(**{campo: None}).update(**{campo: datetime.date(1900, 1, 1)})


class Migration(migrations.Migration):

    dependencies = [
        ('formacion_recursos_humanos', '0006_fechas_sin_dato'),
    ]

    operations = [migrations.RunPython(vacias_a_1900, migrations.RunPython.noop)]
