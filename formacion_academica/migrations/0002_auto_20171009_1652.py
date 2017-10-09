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
        ('nucleo', '0001_initial'),
        ('formacion_academica', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='postdoctorado',
            name='area_conocimiento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postdoctorado_area_conocimiento', to='nucleo.AreaConocimiento', verbose_name='Área de conocimiento'),
        ),
        migrations.AddField(
            model_name='postdoctorado',
            name='dependencia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Dependencia'),
        ),
        migrations.AddField(
            model_name='postdoctorado',
            name='institucion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Institucion'),
        ),
        migrations.AddField(
            model_name='postdoctorado',
            name='proyecto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='investigacion.ProyectoInvestigacion'),
        ),
        migrations.AddField(
            model_name='postdoctorado',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postdoctorados', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='maestria',
            name='dependencia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Dependencia'),
        ),
        migrations.AddField(
            model_name='maestria',
            name='institucion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Institucion'),
        ),
        migrations.AddField(
            model_name='maestria',
            name='programa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.ProgramaMaestria'),
        ),
        migrations.AddField(
            model_name='maestria',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='maestrias', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='licenciatura',
            name='carrera',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.ProgramaLicenciatura'),
        ),
        migrations.AddField(
            model_name='licenciatura',
            name='dependencia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Dependencia'),
        ),
        migrations.AddField(
            model_name='licenciatura',
            name='institucion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Institucion'),
        ),
        migrations.AddField(
            model_name='licenciatura',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='licenciaturas', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='doctorado',
            name='dependencia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Dependencia'),
        ),
        migrations.AddField(
            model_name='doctorado',
            name='institucion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Institucion'),
        ),
        migrations.AddField(
            model_name='doctorado',
            name='programa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.ProgramaDoctorado'),
        ),
        migrations.AddField(
            model_name='doctorado',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctorados', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cursoespecializacion',
            name='area_conocimiento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.AreaConocimiento', verbose_name='Área de conocimiento'),
        ),
        migrations.AddField(
            model_name='cursoespecializacion',
            name='dependencia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Dependencia'),
        ),
        migrations.AddField(
            model_name='cursoespecializacion',
            name='institucion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Institucion'),
        ),
        migrations.AddField(
            model_name='cursoespecializacion',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cursos_especializacion', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='postdoctorado',
            unique_together=set([('nombre', 'usuario')]),
        ),
        migrations.AlterUniqueTogether(
            name='maestria',
            unique_together=set([('programa', 'usuario')]),
        ),
        migrations.AlterUniqueTogether(
            name='licenciatura',
            unique_together=set([('carrera', 'usuario')]),
        ),
        migrations.AlterUniqueTogether(
            name='doctorado',
            unique_together=set([('programa', 'usuario')]),
        ),
        migrations.AlterUniqueTogether(
            name='cursoespecializacion',
            unique_together=set([('nombre', 'usuario', 'fecha_fin')]),
        ),
    ]
