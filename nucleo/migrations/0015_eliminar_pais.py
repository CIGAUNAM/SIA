"""Países → cities_light (final): ya nadie apunta a nucleo.Pais; se elimina con su historial."""

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nucleo', '0014_paises_cities_light'),
        ('difusion_cientifica', '0006_paises_cities_light'),
        ('formacion_recursos_humanos', '0005_paises_cities_light'),
        ('investigacion', '0005_paises_cities_light'),
    ]

    operations = [
        migrations.DeleteModel(name='HistoricalPais'),
        migrations.DeleteModel(name='Pais'),
    ]
