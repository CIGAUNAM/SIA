# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-04 00:16
from __future__ import unicode_literals

import autoslug.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asignatura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asignatura', models.CharField(max_length=255, unique=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='asignatura', unique=True)),
                ('descripcion', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nivel', models.CharField(choices=[('LICENCIATURA', 'Licenciatura'), ('MAESTRIA', 'Maestría'), ('DOCTORADO', 'Doctorado')], max_length=30)),
                ('tipo', models.CharField(choices=[('PRESENCIAL', 'Presencial'), ('EN_LINEA', 'En línea')], max_length=30)),
                ('nivel_participacion', models.CharField(choices=[('TITULAR', 'Titular / Responsable'), ('COLABORADOR', 'Colaborador / Invitado')], max_length=30)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('total_horas', models.PositiveIntegerField()),
                ('asignatura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='docencia.Asignatura')),
            ],
            options={
                'ordering': ['-fecha_inicio'],
                'verbose_name': 'Curso',
                'verbose_name_plural': 'Cursos',
            },
        ),
    ]
