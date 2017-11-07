# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-03 05:31
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('nucleo', '0001_initial'),
        ('investigacion', '0002_auto_20171102_2331'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vinculacion', '0001_initial'),
        ('movilidad_academica', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movilidadacademica',
            name='academico',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movilidad_academica_academico', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='movilidadacademica',
            name='dependencia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Dependencia'),
        ),
        migrations.AddField(
            model_name='movilidadacademica',
            name='financiamiento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Financiamiento'),
        ),
        migrations.AddField(
            model_name='movilidadacademica',
            name='institucion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Institucion'),
        ),
        migrations.AddField(
            model_name='movilidadacademica',
            name='proyecto_investigacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='investigacion.ProyectoInvestigacion'),
        ),
        migrations.AddField(
            model_name='movilidadacademica',
            name='redes_academicas',
            field=models.ManyToManyField(blank=True, related_name='vinculacion_redes_academicas', to='vinculacion.RedAcademica'),
        ),
        migrations.AddField(
            model_name='movilidadacademica',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movilidad_academica_usuario', to=settings.AUTH_USER_MODEL),
        ),
    ]