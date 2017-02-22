# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-21 18:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EstanciaColaboracion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField(blank=True)),
                ('actividades', models.TextField()),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('intercambio_unam', models.BooleanField(default=False)),
                ('convocatoria_financiamiento_unam', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Estancias de colaboración',
                'verbose_name': 'Estancia de colaboración',
                'ordering': ['-fecha_inicio'],
            },
        ),
        migrations.CreateModel(
            name='Invitado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField(blank=True)),
                ('actividades', models.TextField()),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('intercambio_unam', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Invitados nacionales',
                'verbose_name': 'Invitado nacional',
                'ordering': ['-fecha_inicio'],
            },
        ),
        migrations.CreateModel(
            name='Vinculacion',
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
                'verbose_name_plural': 'Actividades de vinculación',
                'verbose_name': 'Actividad de vinculación',
                'ordering': ['-fecha_inicio'],
            },
        ),
    ]
