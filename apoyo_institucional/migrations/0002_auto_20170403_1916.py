# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-04 00:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('nucleo', '0001_initial'),
        ('apoyo_institucional', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='representanteanteorganocolegiado',
            name='ante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Departamento'),
        ),
        migrations.AddField(
            model_name='representanteanteorganocolegiado',
            name='representacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apoyo_institucional.Representacion'),
        ),
        migrations.AddField(
            model_name='representanteanteorganocolegiado',
            name='representante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='representanteanteorganocolegiado',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='representante_ante_organo_colegiado_tags', to='nucleo.Tag'),
        ),
        migrations.AddField(
            model_name='comisionacademica',
            name='comision_academica',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apoyo_institucional.Comision'),
        ),
        migrations.AddField(
            model_name='comisionacademica',
            name='dependencias',
            field=models.ManyToManyField(to='nucleo.Dependencia'),
        ),
        migrations.AddField(
            model_name='comisionacademica',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='comision_academica_tags', to='nucleo.Tag'),
        ),
        migrations.AddField(
            model_name='comisionacademica',
            name='ubicacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Ubicacion'),
        ),
        migrations.AddField(
            model_name='comisionacademica',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cargoacademicoadministrativo',
            name='cargo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Cargo'),
        ),
        migrations.AddField(
            model_name='cargoacademicoadministrativo',
            name='dependencia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Dependencia'),
        ),
        migrations.AddField(
            model_name='cargoacademicoadministrativo',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='cargo_academico_administrativo_tags', to='nucleo.Tag'),
        ),
        migrations.AddField(
            model_name='cargoacademicoadministrativo',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='apoyotecnico',
            name='apoyo_tecnico',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apoyo_institucional.Actividad'),
        ),
        migrations.AddField(
            model_name='apoyotecnico',
            name='dependencia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Dependencia'),
        ),
        migrations.AddField(
            model_name='apoyotecnico',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='apoyo_tecnico_tags', to='nucleo.Tag'),
        ),
        migrations.AddField(
            model_name='apoyotecnico',
            name='ubicacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Ubicacion'),
        ),
        migrations.AddField(
            model_name='apoyotecnico',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='apoyootraactividad',
            name='apoyo_actividad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apoyo_institucional.Actividad'),
        ),
        migrations.AddField(
            model_name='apoyootraactividad',
            name='dependencia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Dependencia'),
        ),
        migrations.AddField(
            model_name='apoyootraactividad',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='apoyo_otra_actividad_tags', to='nucleo.Tag'),
        ),
        migrations.AddField(
            model_name='apoyootraactividad',
            name='ubicacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Ubicacion'),
        ),
        migrations.AddField(
            model_name='apoyootraactividad',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='representanteanteorganocolegiado',
            unique_together=set([('representante', 'representacion', 'cargo_inicio')]),
        ),
        migrations.AlterUniqueTogether(
            name='comisionacademica',
            unique_together=set([('comision_academica', 'user', 'fecha_inicio')]),
        ),
        migrations.AlterUniqueTogether(
            name='cargoacademicoadministrativo',
            unique_together=set([('cargo', 'user', 'dependencia', 'cargo_inicio')]),
        ),
        migrations.AlterUniqueTogether(
            name='apoyotecnico',
            unique_together=set([('apoyo_tecnico', 'user', 'dependencia', 'apoyo_inicio')]),
        ),
        migrations.AlterUniqueTogether(
            name='apoyootraactividad',
            unique_together=set([('apoyo_actividad', 'user', 'dependencia', 'apoyo_inicio')]),
        ),
    ]
