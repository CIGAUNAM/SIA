# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-26 22:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArticuloDocencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255, unique=True)),
                ('descripcion', models.TextField(blank=True)),
                ('volumen', models.CharField(blank=True, max_length=100, null=True)),
                ('numero', models.CharField(blank=True, max_length=100, null=True)),
                ('fecha', models.DateField()),
                ('issn_impreso', models.CharField(blank=True, max_length=40, verbose_name='ISSN Impreso')),
                ('issn_online', models.CharField(blank=True, max_length=40, verbose_name='ISSN Online')),
                ('status', models.CharField(choices=[('', '-------'), ('ENVIADO', 'Enviado'), ('ACEPTADO', 'Aceptado'), ('EN_PRENSA', 'En prensa'), ('PUBLICADO', 'Publicado'), ('OTRO', 'Otro')], max_length=20)),
                ('solo_electronico', models.BooleanField(default=False)),
                ('url', models.URLField(blank=True)),
                ('pagina_inicio', models.PositiveIntegerField()),
                ('pagina_fin', models.PositiveIntegerField()),
                ('id_doi', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name': 'Artículo para docencia',
                'verbose_name_plural': 'Artículos para docencia',
                'ordering': ['-fecha', 'titulo'],
            },
        ),
        migrations.CreateModel(
            name='CursoDocencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nivel', models.CharField(choices=[('OTRO', 'Otro'), ('LICENCIATURA', 'Licenciatura'), ('MAESTRIA', 'Maestría'), ('DOCTORADO', 'Doctorado')], max_length=30)),
                ('tipo', models.CharField(choices=[('ESCOLARIZADO', 'Escolarizado'), ('EXTRACURRICULAR', 'Extracurricular')], max_length=20)),
                ('modalidad', models.CharField(choices=[('PRESENCIAL', 'Presencial'), ('EN_LINEA', 'En línea')], max_length=30)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('total_horas', models.PositiveIntegerField()),
            ],
            options={
                'verbose_name': 'Curso',
                'verbose_name_plural': 'Cursos',
                'ordering': ['-fecha_inicio'],
            },
        ),
        migrations.CreateModel(
            name='ProgramaEstudio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=254, unique=True)),
                ('descripcion', models.TextField(blank=True)),
                ('nivel', models.CharField(choices=[('', '-------'), ('LICENCIATURA', 'Licenciatura'), ('MAESTRIA', 'Maestría'), ('DOCTORADO', 'Doctorado'), ('OTRO', 'Otro')], max_length=20)),
                ('fecha', models.DateField()),
            ],
            options={
                'verbose_name': 'Programa de estudio',
                'verbose_name_plural': 'Programas de estudio',
                'ordering': ['-fecha', 'nombre'],
            },
        ),
    ]
