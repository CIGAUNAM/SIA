# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-13 17:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MemoriaInExtenso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255, unique=True, verbose_name='Título de memoria in extenso')),
                ('descripcion', models.TextField(blank=True)),
                ('fecha', models.DateField()),
                ('pagina_inicio', models.PositiveIntegerField()),
                ('pagina_fin', models.PositiveIntegerField()),
                ('issn', models.SlugField(blank=True, max_length=20)),
                ('url', models.URLField(blank=True)),
            ],
            options={
                'verbose_name': 'Memoria in extenso',
                'verbose_name_plural': 'Memorias in extenso',
            },
        ),
        migrations.CreateModel(
            name='OrganizacionEventoAcademico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField(blank=True)),
                ('responsabilidad', models.CharField(choices=[('COORDINADOR', 'Coordinador general'), ('COMITE', 'Comité organizador'), ('AYUDANTE', 'Ayudante'), ('TECNICO', 'Apoyo técnico'), ('OTRO', 'Otro')], max_length=30)),
                ('numero_ponentes', models.PositiveIntegerField()),
                ('numero_asistentes', models.PositiveIntegerField()),
                ('ambito', models.CharField(choices=[('', '-------'), ('INSTITUCIONAL', 'Institucional'), ('REGIONAL', 'Regional'), ('NACIONAL', 'Nacional'), ('INTERNACIONAL', 'Internacional'), ('OTRO', 'Otro')], max_length=20)),
            ],
            options={
                'verbose_name': 'Organización de evento académico',
                'verbose_name_plural': 'Organización de eventos académicos',
            },
        ),
        migrations.CreateModel(
            name='ParticipacionEventoAcademico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('descripcion', models.TextField(blank=True)),
                ('ambito', models.CharField(choices=[('', '-------'), ('INSTITUCIONAL', 'Institucional'), ('REGIONAL', 'Regional'), ('NACIONAL', 'Nacional'), ('INTERNACIONAL', 'Internacional'), ('OTRO', 'Otro')], max_length=20)),
                ('resumen_publicado', models.BooleanField(default=False)),
                ('por_invitacion', models.BooleanField(default=False)),
                ('ponencia_magistral', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Participación en evento académico',
                'verbose_name_plural': 'Participación en eventos académicos',
            },
        ),
        migrations.CreateModel(
            name='PrologoLibro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField(blank=True)),
                ('pagina_inicio', models.PositiveIntegerField()),
                ('pagina_fin', models.PositiveIntegerField()),
                ('url', models.URLField(blank=True)),
            ],
            options={
                'verbose_name': 'Prólogo de libro',
                'verbose_name_plural': 'Prólogos de libros',
            },
        ),
        migrations.CreateModel(
            name='Resena',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255, unique=True)),
                ('tipo', models.CharField(choices=[('LIBRO', 'Libro'), ('REVISTA', 'Revista')], max_length=10)),
                ('descripcion', models.TextField(blank=True)),
                ('pagina_inicio', models.PositiveIntegerField()),
                ('pagina_fin', models.PositiveIntegerField()),
                ('url', models.URLField(blank=True)),
            ],
            options={
                'verbose_name': 'Reseña de libro',
                'verbose_name_plural': 'Reseñas de libros',
            },
        ),
    ]
