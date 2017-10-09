# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-09 21:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import sortedm2m.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('investigacion', '0001_initial'),
        ('nucleo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyectoinvestigacion',
            name='alumnos_doctorado',
            field=models.ManyToManyField(blank=True, related_name='proyecto_investigacion_alumnos_doctorado', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='proyectoinvestigacion',
            name='alumnos_licenciatura',
            field=models.ManyToManyField(blank=True, related_name='proyecto_investigacion_alumnos_licenciatura', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='proyectoinvestigacion',
            name='alumnos_maestria',
            field=models.ManyToManyField(blank=True, related_name='proyecto_investigacion_alumnos_maestria', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='proyectoinvestigacion',
            name='dependencia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Dependencia'),
        ),
        migrations.AddField(
            model_name='proyectoinvestigacion',
            name='especialidades',
            field=models.ManyToManyField(blank=True, related_name='proyecto_investigacion_especialidades', to='nucleo.AreaEspecialidad'),
        ),
        migrations.AddField(
            model_name='proyectoinvestigacion',
            name='financiamientos',
            field=models.ManyToManyField(blank=True, to='nucleo.Financiamiento'),
        ),
        migrations.AddField(
            model_name='proyectoinvestigacion',
            name='impactos_sociales',
            field=models.ManyToManyField(blank=True, related_name='proyecto_investigacion_impactos_sociales', to='nucleo.ImpactoSocial'),
        ),
        migrations.AddField(
            model_name='proyectoinvestigacion',
            name='institucion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Institucion'),
        ),
        migrations.AddField(
            model_name='proyectoinvestigacion',
            name='metodologias',
            field=models.ManyToManyField(blank=True, related_name='proyecto_investigacion_metodologias', to='nucleo.Metodologia'),
        ),
        migrations.AddField(
            model_name='proyectoinvestigacion',
            name='participantes',
            field=models.ManyToManyField(blank=True, related_name='proyecto_investigacion_participantes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='proyectoinvestigacion',
            name='problema_nacional_conacyt',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='nucleo.ProblemaNacionalConacyt'),
        ),
        migrations.AddField(
            model_name='proyectoinvestigacion',
            name='tecnicos',
            field=models.ManyToManyField(blank=True, related_name='proyecto_investigacion_impactos_tecnicos', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='proyectoinvestigacion',
            name='usuarios',
            field=sortedm2m.fields.SortedManyToManyField(help_text=None, related_name='proyecto_investigacion_responsables', to=settings.AUTH_USER_MODEL, verbose_name='Responsables'),
        ),
        migrations.AddField(
            model_name='mapaarbitrado',
            name='ciudad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Ciudad'),
        ),
        migrations.AddField(
            model_name='mapaarbitrado',
            name='coleccion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='nucleo.Coleccion'),
        ),
        migrations.AddField(
            model_name='mapaarbitrado',
            name='coordinadores',
            field=models.ManyToManyField(blank=True, related_name='mapa_arbitrado_coordinadores', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='mapaarbitrado',
            name='editores',
            field=models.ManyToManyField(blank=True, related_name='mapa_arbitrado_editores', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='mapaarbitrado',
            name='editorial',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Editorial'),
        ),
        migrations.AddField(
            model_name='mapaarbitrado',
            name='estado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Estado'),
        ),
        migrations.AddField(
            model_name='mapaarbitrado',
            name='pais',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Pais'),
        ),
        migrations.AddField(
            model_name='mapaarbitrado',
            name='proyecto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='investigacion.ProyectoInvestigacion'),
        ),
        migrations.AddField(
            model_name='mapaarbitrado',
            name='usuarios',
            field=sortedm2m.fields.SortedManyToManyField(help_text=None, related_name='mapa_arbitrado_autores', to=settings.AUTH_USER_MODEL, verbose_name='Autores'),
        ),
        migrations.AddField(
            model_name='informetecnico',
            name='proyecto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='investigacion.ProyectoInvestigacion'),
        ),
        migrations.AddField(
            model_name='informetecnico',
            name='usuarios',
            field=sortedm2m.fields.SortedManyToManyField(help_text=None, related_name='informe_tecnico_autores', to=settings.AUTH_USER_MODEL, verbose_name='Autores'),
        ),
        migrations.AddField(
            model_name='capitulolibroinvestigacion',
            name='libro',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Libro'),
        ),
        migrations.AddField(
            model_name='capitulolibroinvestigacion',
            name='proyecto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='investigacion.ProyectoInvestigacion'),
        ),
        migrations.AddField(
            model_name='capitulolibroinvestigacion',
            name='usuarios',
            field=sortedm2m.fields.SortedManyToManyField(help_text=None, related_name='capitulo_libro_investigacion_autores', to=settings.AUTH_USER_MODEL, verbose_name='Autores'),
        ),
        migrations.AddField(
            model_name='articulocientifico',
            name='alumnos',
            field=models.ManyToManyField(blank=True, related_name='articulo_cientifico_alumnos', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='articulocientifico',
            name='indices',
            field=models.ManyToManyField(blank=True, related_name='articulo_cientifico_indices', to='nucleo.Indice'),
        ),
        migrations.AddField(
            model_name='articulocientifico',
            name='proyecto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='investigacion.ProyectoInvestigacion'),
        ),
        migrations.AddField(
            model_name='articulocientifico',
            name='revista',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Revista'),
        ),
        migrations.AddField(
            model_name='articulocientifico',
            name='usuarios',
            field=sortedm2m.fields.SortedManyToManyField(help_text=None, related_name='articulo_cientifico_autores', to=settings.AUTH_USER_MODEL, verbose_name='Autores'),
        ),
    ]
