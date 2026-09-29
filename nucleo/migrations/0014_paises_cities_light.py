"""Países → cities_light (2/2): las llaves de país apuntan a cities_light.Country."""

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nucleo', '0013_paises_traspaso'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libro',
            name='pais',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cities_light.country', verbose_name='país'),
        ),
        migrations.AlterField(
            model_name='evento',
            name='pais',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cities_light.country', verbose_name='país'),
        ),
        migrations.AlterField(
            model_name='historicalrevista',
            name='pais',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='cities_light.country', verbose_name='país'),
        ),
        migrations.AlterField(
            model_name='configuracionentidad',
            name='pais_sede',
            field=models.ForeignKey(blank=True, help_text='Define si un evento o participación es nacional o internacional.', null=True, on_delete=django.db.models.deletion.PROTECT, to='cities_light.country', verbose_name='país sede'),
        ),
        migrations.AlterField(
            model_name='mediodivulgacion',
            name='pais',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cities_light.country', verbose_name='país'),
        ),
        migrations.AlterField(
            model_name='historicalevento',
            name='pais',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='cities_light.country', verbose_name='país'),
        ),
        migrations.AlterField(
            model_name='user',
            name='pais_origen',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='cities_light.country', verbose_name='país de origen'),
        ),
        migrations.AlterField(
            model_name='institucion',
            name='pais',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cities_light.country', verbose_name='país'),
        ),
        migrations.AlterField(
            model_name='historicalconfiguracionentidad',
            name='pais_sede',
            field=models.ForeignKey(blank=True, db_constraint=False, help_text='Define si un evento o participación es nacional o internacional.', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='cities_light.country', verbose_name='país sede'),
        ),
        migrations.AlterField(
            model_name='historicalinstitucion',
            name='pais',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='cities_light.country', verbose_name='país'),
        ),
        migrations.AlterField(
            model_name='historicallibro',
            name='pais',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='cities_light.country', verbose_name='país'),
        ),
        migrations.AlterField(
            model_name='revista',
            name='pais',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cities_light.country', verbose_name='país'),
        ),
        migrations.AlterField(
            model_name='historicalmediodivulgacion',
            name='pais',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='cities_light.country', verbose_name='país'),
        ),
    ]
