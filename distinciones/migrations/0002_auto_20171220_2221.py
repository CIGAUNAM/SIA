# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-21 04:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('investigacion', '0001_initial'),
        ('nucleo', '0001_initial'),
        ('distinciones', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='participacionsociedadcientifica',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='participacioncomisionexpertos',
            name='institucion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Institucion'),
        ),
        migrations.AddField(
            model_name='participacioncomisionexpertos',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='distincionalumno',
            name='alumno',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='distincion_alumno_alumno', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='distincionalumno',
            name='distincion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Distincion'),
        ),
        migrations.AddField(
            model_name='distincionalumno',
            name='institucion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Institucion'),
        ),
        migrations.AddField(
            model_name='distincionalumno',
            name='tutores',
            field=models.ManyToManyField(related_name='distincion_alumno_tutores', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='distincionacademico',
            name='distincion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Distincion'),
        ),
        migrations.AddField(
            model_name='distincionacademico',
            name='institucion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Institucion'),
        ),
        migrations.AddField(
            model_name='distincionacademico',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='distincion_academico_usuario', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='citapublicacion',
            name='articulo_citado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cita_publicacion_articulo_citado', to='investigacion.ArticuloCientifico'),
        ),
        migrations.AddField(
            model_name='citapublicacion',
            name='capitulo_libro_citado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='investigacion.CapituloLibroInvestigacion'),
        ),
        migrations.AddField(
            model_name='citapublicacion',
            name='citado_en_articulos',
            field=models.ManyToManyField(blank=True, related_name='cita_publicacion_citado_en_articulos', to='investigacion.ArticuloCientifico'),
        ),
        migrations.AddField(
            model_name='citapublicacion',
            name='citado_en_libros',
            field=models.ManyToManyField(blank=True, related_name='cita_publicacion_citado_en_libros', to='nucleo.Libro'),
        ),
        migrations.AddField(
            model_name='citapublicacion',
            name='libro_citado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cita_publicacion_libro_citado', to='nucleo.Libro'),
        ),
        migrations.AddField(
            model_name='citapublicacion',
            name='usuarios',
            field=models.ManyToManyField(related_name='cita_publicacion_autores', to=settings.AUTH_USER_MODEL, verbose_name='Autores'),
        ),
    ]
