# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-18 17:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import sortedm2m.fields


class Migration(migrations.Migration):

    dependencies = [
        ('nucleo', '0006_auto_20171117_0923'),
        ('docencia', '0004_auto_20171117_1912'),
    ]

    operations = [
        migrations.AddField(
            model_name='articulodocencia',
            name='indices',
            field=models.ManyToManyField(blank=True, related_name='articulo_docencia_indices', to='nucleo.Indice'),
        ),
        migrations.AlterField(
            model_name='articulodocencia',
            name='usuarios',
            field=sortedm2m.fields.SortedManyToManyField(help_text=None, related_name='articulo_docencia_autores', to=settings.AUTH_USER_MODEL, verbose_name='Autores'),
        ),
    ]