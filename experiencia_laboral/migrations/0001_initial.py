# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-09 21:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CapacidadPotencialidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255, verbose_name='Capacidad o potencialidad')),
                ('descripcion', models.TextField(blank=True)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Capacidad y potencialid',
                'verbose_name_plural': 'Capacidades y potencialidades',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='ExperienciaLaboral',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('es_nombramiento_definitivo', models.BooleanField(default=False)),
                ('descripcion', models.TextField(blank=True)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Experiencia Laboral',
                'verbose_name_plural': 'Experiencias Laborales',
                'ordering': ['fecha_inicio', 'dependencia'],
            },
        ),
        migrations.CreateModel(
            name='LineaInvestigacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('linea_investigacion', models.CharField(max_length=255)),
                ('descripcion', models.TextField(blank=True)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Línea de investigación',
                'verbose_name_plural': 'Líneas de investigación',
                'ordering': ['fecha_inicio', 'linea_investigacion'],
            },
        ),
    ]
