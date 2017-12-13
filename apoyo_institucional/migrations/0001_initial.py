# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-13 19:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActividadApoyo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255, unique=True)),
                ('descripcion', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Actividad de apoyo',
                'verbose_name_plural': 'Actividades de apoyo',
            },
        ),
        migrations.CreateModel(
            name='ApoyoOtraActividad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField()),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
            ],
            options={
                'verbose_name_plural': 'Apoyos en Otras Actividades',
                'ordering': ['-fecha_inicio'],
                'get_latest_by': ['usuario', 'actividad_apoyo'],
            },
        ),
        migrations.CreateModel(
            name='ApoyoTecnico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField()),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
            ],
            options={
                'verbose_name_plural': 'Apoyos de Técnicos',
                'ordering': ['-fecha_inicio'],
                'get_latest_by': ['usuario', 'actividad_apoyo'],
            },
        ),
        migrations.CreateModel(
            name='CargoAcademicoAdministrativo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField(blank=True)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
            ],
            options={
                'verbose_name_plural': 'Cargos Académico-Administrativos',
                'ordering': ['-fecha_inicio'],
                'get_latest_by': ['user', 'cargo'],
            },
        ),
        migrations.CreateModel(
            name='Comision',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comision', models.CharField(max_length=255, unique=True)),
                ('descripcion', models.TextField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'Comisiones',
            },
        ),
        migrations.CreateModel(
            name='ComisionAcademica',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField(blank=True)),
                ('es_evaluacion', models.BooleanField(default=False)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
            ],
            options={
                'verbose_name_plural': 'Comisiones Académicas',
                'ordering': ['fecha_inicio'],
                'get_latest_by': ['user', 'comision_academica'],
            },
        ),
        migrations.CreateModel(
            name='Representacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255, unique=True)),
                ('descripcion', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Representación',
                'verbose_name_plural': 'Representaciones',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='RepresentacionOrganoColegiado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField(blank=True)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
            ],
            options={
                'verbose_name_plural': 'Representantes Ante Organos Colegiados',
                'ordering': ['-fecha_inicio'],
            },
        ),
    ]
