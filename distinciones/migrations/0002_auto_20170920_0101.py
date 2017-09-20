# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-20 06:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('distinciones', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('nucleo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='distincionalumno',
            name='alumno',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='distincion_alumno_alumno', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='distincionalumno',
            name='dependencia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Dependencia'),
        ),
        migrations.AddField(
            model_name='distincionalumno',
            name='distincion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Distincion'),
        ),
        migrations.AddField(
            model_name='distincionalumno',
            name='tutores',
            field=models.ManyToManyField(related_name='distincion_alumno_tutores', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='distincionacademico',
            name='condecorados',
            field=models.ManyToManyField(related_name='distincion_academico_condecorados', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='distincionacademico',
            name='dependencia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Dependencia'),
        ),
        migrations.AddField(
            model_name='distincionacademico',
            name='distincion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Distincion'),
        ),
    ]
