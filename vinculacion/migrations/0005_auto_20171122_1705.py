# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-22 23:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vinculacion', '0004_remove_arbitrajepublicacionacademica_capitulo_libro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arbitrajepublicacionacademica',
            name='tipo',
            field=models.CharField(choices=[('', '-------'), ('ARTICULO', 'Artículo en revista'), ('LIBRO', 'Libro')], max_length=20),
        ),
    ]
