# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-04 01:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations
import sortedm2m.fields


class Migration(migrations.Migration):

    dependencies = [
        ('difusion_cientifica', '0002_auto_20170925_0048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memoriainextenso',
            name='usuarios',
            field=sortedm2m.fields.SortedManyToManyField(help_text=None, related_name='memoria_in_extenso_autores', to=settings.AUTH_USER_MODEL, verbose_name='Autores'),
        ),
    ]
