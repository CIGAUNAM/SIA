# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-13 17:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('nucleo', '0001_initial'),
        ('docencia', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='cursodocencia',
            name='academicos_participantes',
            field=models.ManyToManyField(blank=True, related_name='curso_escolarizado_usuarioa', to=settings.AUTH_USER_MODEL, verbose_name='Académicos participantes'),
        ),
        migrations.AddField(
            model_name='cursodocencia',
            name='asignatura',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Asignatura'),
        ),
        migrations.AddField(
            model_name='cursodocencia',
            name='dependencia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Dependencia'),
        ),
        migrations.AddField(
            model_name='cursodocencia',
            name='doctorado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='nucleo.ProgramaDoctorado'),
        ),
        migrations.AddField(
            model_name='cursodocencia',
            name='institucion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Institucion'),
        ),
        migrations.AddField(
            model_name='cursodocencia',
            name='licenciatura',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='nucleo.ProgramaLicenciatura'),
        ),
        migrations.AddField(
            model_name='cursodocencia',
            name='maestria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='nucleo.ProgramaMaestria'),
        ),
        migrations.AddField(
            model_name='cursodocencia',
            name='otras_dependencias_participantes',
            field=models.ManyToManyField(blank=True, related_name='curso_escolarizado_otras_dependencias_participantes', to='nucleo.Dependencia'),
        ),
        migrations.AddField(
            model_name='cursodocencia',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='curso_escolarizado_usuario', to=settings.AUTH_USER_MODEL),
        ),
    ]
