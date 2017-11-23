# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-22 20:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('investigacion', '0003_remove_capitulolibroinvestigacion_proyecto'),
        ('vinculacion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='arbitrajepublicacionacademica',
            name='articulo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='investigacion.ArticuloCientifico'),
        ),
    ]
