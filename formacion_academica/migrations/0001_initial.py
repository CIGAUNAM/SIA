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
            name='CursoEspecializacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(help_text='Nombre del curso texto de ayuda', max_length=255, verbose_name='Nombre del curso')),
                ('descripcion', models.TextField(blank=True, verbose_name='Descripción')),
                ('tipo', models.CharField(choices=[('', '-------'), ('CURSO', 'Curso'), ('DIPLOMADO', 'Diplomado'), ('CERTIFICACION', 'Certificación'), ('OTRO', 'Otro')], max_length=20, verbose_name='Tipo de curso')),
                ('horas', models.PositiveIntegerField(verbose_name='Número de horas')),
                ('fecha_inicio', models.DateField(verbose_name='Fecha de inicio')),
                ('fecha_fin', models.DateField(blank=True, null=True, verbose_name='Fecha de finalización')),
                ('modalidad', models.CharField(choices=[('', '-------'), ('PRESENCIAL', 'Presencial'), ('EN_LINEA', 'En línea'), ('MIXTO', 'Mixto'), ('OTRO', 'Otro')], max_length=20)),
            ],
            options={
                'verbose_name': 'Curso de especialización',
                'verbose_name_plural': 'Cursos de especialización',
                'ordering': ['fecha_inicio'],
            },
        ),
        migrations.CreateModel(
            name='Doctorado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField(blank=True, verbose_name='Descripición')),
                ('titulo_tesis', models.CharField(max_length=255)),
                ('tesis_doc', models.FileField(blank=True, upload_to='')),
                ('tesis_url', models.URLField(blank=True)),
                ('fecha_inicio', models.DateField(verbose_name='Fecha de inicio de doctorado')),
                ('fecha_fin', models.DateField(blank=True, null=True, verbose_name='Fecha de terminación de doctorado')),
                ('fecha_grado', models.DateField(blank=True, null=True, verbose_name='Fecha de obtención de grado de doctorado')),
            ],
            options={
                'ordering': ['fecha_grado', 'dependencia', 'titulo_tesis'],
            },
        ),
        migrations.CreateModel(
            name='Licenciatura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField(blank=True, verbose_name='Descripición')),
                ('titulo_tesis', models.CharField(max_length=255)),
                ('tesis_url', models.URLField(blank=True)),
                ('fecha_inicio', models.DateField(verbose_name='Fecha de inicio de licenciatura')),
                ('fecha_fin', models.DateField(verbose_name='Fecha de terminación de licenciatura')),
                ('fecha_grado', models.DateField(verbose_name='Fecha de obtención de grado de licenciatura')),
            ],
            options={
                'ordering': ['dependencia', 'carrera', 'titulo_tesis'],
            },
        ),
        migrations.CreateModel(
            name='Maestria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField(blank=True, verbose_name='Descripición')),
                ('titulo_tesis', models.CharField(max_length=255)),
                ('tesis_doc', models.FileField(blank=True, upload_to='')),
                ('tesis_url', models.URLField(blank=True)),
                ('fecha_inicio', models.DateField(verbose_name='Fecha de inicio de maestría')),
                ('fecha_fin', models.DateField(blank=True, null=True, verbose_name='Fecha de terminación de maestría')),
                ('fecha_grado', models.DateField(blank=True, null=True, verbose_name='Fecha de obtención de grado de maestría')),
            ],
            options={
                'ordering': ['dependencia', 'programa', 'titulo_tesis'],
            },
        ),
        migrations.CreateModel(
            name='PostDoctorado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('descripcion', models.TextField(blank=True, verbose_name='Descripición')),
                ('fecha_inicio', models.DateField(verbose_name='Fecha de inicio de postdoctorado')),
                ('fecha_fin', models.DateField(blank=True, null=True, verbose_name='Fecha de terminación de postdoctorado')),
            ],
            options={
                'ordering': ['fecha_fin', 'dependencia'],
            },
        ),
    ]