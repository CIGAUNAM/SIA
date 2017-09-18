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
            name='AsesorEstancia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField(blank=True)),
                ('tipo', models.CharField(choices=[('RESIDENCIA', 'Residencia'), ('PRACTICA', 'Práctica'), ('ESTANCIA', 'Estancia'), ('SERVICIO_SOCIAL', 'Servicio Social'), ('OTRO', 'Otro')], max_length=30)),
                ('grado_academico', models.CharField(choices=[('OTRO', 'Otro'), ('LICENCIATURA', 'Licenciatura'), ('MAESTRIA', 'Maestría'), ('DOCTORADO', 'Doctorado')], max_length=20)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
            ],
            options={
                'verbose_name': 'Asesor en residencias / prácticas / estancias / servicio social',
                'verbose_name_plural': 'Asesores en residencias / prácticas / estancias / servicio social',
                'ordering': ['-fecha_inicio', '-fecha_fin'],
            },
        ),
        migrations.CreateModel(
            name='ComiteCandidaturaDoctoral',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_defensa', models.DateField()),
            ],
            options={
                'verbose_name': 'Comité de examen de candidatura doctoral',
                'verbose_name_plural': 'Comités de exámenes de candidatura doctoral',
                'ordering': ['-fecha_defensa'],
            },
        ),
        migrations.CreateModel(
            name='ComiteTutoral',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grado_academico', models.CharField(choices=[('MAESTRIA', 'Maestría'), ('DOCTORADO', 'Doctorado')], max_length=20)),
                ('status', models.CharField(choices=[('EN_PROCESO', 'En proceso'), ('CONCLUIDO', 'Concluído')], max_length=20)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Comité tutoral',
                'verbose_name_plural': 'Comités tutorales',
                'ordering': ['-fecha_inicio'],
            },
        ),
        migrations.CreateModel(
            name='DireccionTesis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255, unique=True)),
                ('descripcion', models.TextField(blank=True)),
                ('grado_academico', models.CharField(choices=[('OTRO', 'Otro'), ('LICENCIATURA', 'Licenciatura'), ('MAESTRIA', 'Maestría'), ('DOCTORADO', 'Doctorado')], max_length=20)),
                ('documento_tesis', models.FileField(blank=True, null=True, upload_to='')),
                ('fecha_examen', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Tesis',
                'verbose_name_plural': 'Tesis',
                'ordering': ['-fecha_examen'],
            },
        ),
    ]
