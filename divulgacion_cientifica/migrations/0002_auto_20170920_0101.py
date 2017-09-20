# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-20 06:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import sortedm2m.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('divulgacion_cientifica', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('nucleo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='programaradiotelevisioninternet',
            name='medio_divulgacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.MedioDivulgacion'),
        ),
        migrations.AddField(
            model_name='programaradiotelevisioninternet',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='participacioneventodivulgacion',
            name='evento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Evento'),
        ),
        migrations.AddField(
            model_name='participacioneventodivulgacion',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='organizacioneventodivulgacion',
            name='evento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Evento'),
        ),
        migrations.AddField(
            model_name='organizacioneventodivulgacion',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='capitulolibrodivulgacion',
            name='libro',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Libro'),
        ),
        migrations.AddField(
            model_name='capitulolibrodivulgacion',
            name='proyecto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='nucleo.Proyecto'),
        ),
        migrations.AddField(
            model_name='capitulolibrodivulgacion',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='articulodivulgacion',
            name='alumnos',
            field=models.ManyToManyField(blank=True, related_name='articulo_divulgracion_alumnos', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='articulodivulgacion',
            name='indices',
            field=models.ManyToManyField(blank=True, related_name='articulo_divulgracion_indices', to='nucleo.Indice'),
        ),
        migrations.AddField(
            model_name='articulodivulgacion',
            name='proyecto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='nucleo.Proyecto'),
        ),
        migrations.AddField(
            model_name='articulodivulgacion',
            name='revista',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Revista'),
        ),
        migrations.AddField(
            model_name='articulodivulgacion',
            name='usuarios',
            field=sortedm2m.fields.SortedManyToManyField(help_text=None, related_name='articulo_divulgracion_autores', to=settings.AUTH_USER_MODEL, verbose_name='Autores'),
        ),
        migrations.AlterUniqueTogether(
            name='capitulolibrodivulgacion',
            unique_together=set([('titulo', 'libro', 'usuario')]),
        ),
    ]
