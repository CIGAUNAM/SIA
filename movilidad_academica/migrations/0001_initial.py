# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-04 06:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MovilidadAcademica',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('INVITACION', 'Invitación'), ('ESTANCIA', 'Estancia de colaboración'), ('SABATICO', 'Sabático')], max_length=30)),
                ('descripcion', models.TextField(blank=True)),
                ('actividades', models.TextField()),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('intercambio_unam', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Actividad de vinculación',
                'verbose_name_plural': 'Actividades de vinculación',
                'ordering': ['-fecha_inicio'],
            },
        ),
    ]
