# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-21 03:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nucleo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='genero',
            field=models.CharField(choices=[('', '-------'), ('M', 'Masculino'), ('F', 'Femenino')], default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='tipo',
            field=models.CharField(choices=[('', '-------'), ('INVESTIGADOR', 'Investigador'), ('ADMINISTRATIVO', 'Administrativo'), ('TECNICO', 'Técnico'), ('POSTDOCTORADO', 'Postdoctorado'), ('OTRO', 'Otro')], default='OTRO', max_length=30),
        ),
    ]
