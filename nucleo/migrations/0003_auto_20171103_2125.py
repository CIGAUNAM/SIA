# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-04 03:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nucleo', '0002_user_titulo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='titulo',
            field=models.CharField(blank=True, choices=[('', '-------'), ('Dr', 'Doctor'), ('Dra', 'Doctora')], max_length=10, null=True),
        ),
    ]