# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-05 01:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArticuloDivulgacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255, unique=True)),
                ('descripcion', models.TextField(blank=True)),
                ('tipo', models.CharField(choices=[('', '-------'), ('ARTICULO', 'Artículo'), ('ACTA', 'Acta'), ('CARTA', 'Carta'), ('RESENA', 'Reseña'), ('OTRO', 'Otro')], max_length=16)),
                ('status', models.CharField(choices=[('', '-------'), ('ENVIADO', 'Enviado'), ('ACEPTADO', 'Aceptado'), ('EN_PRENSA', 'En prensa'), ('PUBLICADO', 'Publicado'), ('OTRO', 'Otro')], max_length=20)),
                ('indizado', models.BooleanField(default=False)),
                ('url', models.URLField(blank=True)),
                ('solo_electronico', models.BooleanField(default=False)),
                ('fecha', models.DateField()),
                ('volumen', models.CharField(blank=True, max_length=100)),
                ('numero', models.CharField(blank=True, max_length=100)),
                ('issn', models.CharField(blank=True, max_length=30)),
                ('pagina_inicio', models.PositiveIntegerField()),
                ('pagina_fin', models.PositiveIntegerField()),
                ('id_doi', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'verbose_name': 'Artículo de divulgación',
                'verbose_name_plural': 'Artículos de divulgación',
                'ordering': ['fecha', 'titulo'],
            },
        ),
        migrations.CreateModel(
            name='CapituloLibroDivulgacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255, unique=True)),
                ('descripcion', models.TextField(blank=True)),
                ('pagina_inicio', models.PositiveIntegerField()),
                ('pagina_fin', models.PositiveIntegerField()),
            ],
            options={
                'verbose_name': 'Capítulo en libro de divulgación',
                'verbose_name_plural': 'Capítulos en libros de divulgración',
                'ordering': ['titulo'],
            },
        ),
        migrations.CreateModel(
            name='OrganizacionEventoDivulgacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField(blank=True)),
                ('responsabilidad', models.CharField(choices=[('', '-------'), ('COORDINADOR', 'Coordinador general'), ('COMITE', 'Comité organizador'), ('AYUDANTE', 'Ayudante'), ('TECNICO', 'Apoyo técnico'), ('OTRO', 'Otro')], max_length=30)),
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
            name='ParticipacionEventoDivulgacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('descripcion', models.TextField(blank=True)),
                ('resumen_publicado', models.BooleanField(default=False)),
                ('ambito', models.CharField(choices=[('', '-------'), ('INSTITUCIONAL', 'Institucional'), ('REGIONAL', 'Regional'), ('NACIONAL', 'Nacional'), ('INTERNACIONAL', 'Internacional'), ('OTRO', 'Otro')], max_length=20)),
                ('por_invitacion', models.BooleanField(default=False)),
                ('ponencia_magistral', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Participación en evento académico',
                'verbose_name_plural': 'Participación en eventos académicos',
            },
        ),
        migrations.CreateModel(
            name='ProgramaRadioTelevisionInternet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tema', models.CharField(max_length=255)),
                ('fecha', models.DateField()),
                ('descripcion', models.TextField(blank=True)),
                ('actividad', models.CharField(choices=[('PRODUCCION', 'Producciòn'), ('PARTICIPACION', 'Participaciòn'), ('ENTREVISTA', 'Entrevista'), ('OTRA', 'Otra')], max_length=20)),
            ],
            options={
                'verbose_name': 'Programa de radio, televisión o internet',
                'verbose_name_plural': 'Programas de radio, televisión o internet',
                'ordering': ['fecha', 'tema'],
            },
        ),
    ]
