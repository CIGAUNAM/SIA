"""Países → cities_light (2/2): las llaves de país apuntan a cities_light.Country."""

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('difusion_cientifica', '0005_paises_traspaso'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalmemoriainextenso',
            name='pais',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='cities_light.country', verbose_name='país'),
        ),
        migrations.AlterField(
            model_name='historicalparticipacioneventoacademico',
            name='pais',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='cities_light.country', verbose_name='país'),
        ),
        migrations.AlterField(
            model_name='memoriainextenso',
            name='pais',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cities_light.country', verbose_name='país'),
        ),
        migrations.AlterField(
            model_name='participacioneventoacademico',
            name='pais',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cities_light.country', verbose_name='país'),
        ),
    ]
