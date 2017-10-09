# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-09 21:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('investigacion', '0001_initial'),
        ('desarrollo_tecnologico', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='desarrollotecnologico',
            name='autores',
            field=models.ManyToManyField(related_name='desarrollo_tecnologico_autores', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='desarrollotecnologico',
            name='licencia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='desarrollo_tecnologico.Licencia'),
        ),
        migrations.AddField(
            model_name='desarrollotecnologico',
            name='proyecto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='investigacion.ProyectoInvestigacion'),
        ),
    ]
