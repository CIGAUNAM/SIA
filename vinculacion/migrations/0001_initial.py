# Generated by Django 2.0.2 on 2018-02-07 06:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('investigacion', '0001_initial'),
        ('nucleo', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ArbitrajeOtraActividad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actividad', models.CharField(max_length=255)),
                ('descripcion', models.TextField(blank=True)),
                ('fecha', models.DateField()),
                ('dependencia', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='nucleo.Dependencia')),
                ('institucion', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='nucleo.Institucion')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Arbitraje en otras actividades',
                'verbose_name_plural': 'Arbitraje en otras actividades',
                'ordering': ['-fecha'],
            },
        ),
        migrations.CreateModel(
            name='ArbitrajeProyectoInvestigacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('descripcion', models.TextField(blank=True)),
                ('proyecto', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='investigacion.ProyectoInvestigacion')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Arbitraje de proyectos de investigación',
                'verbose_name_plural': 'Arbitrajes de proyectos de investigación',
                'ordering': ['-fecha'],
            },
        ),
        migrations.CreateModel(
            name='ArbitrajePublicacionAcademica',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField(blank=True)),
                ('tipo', models.CharField(choices=[('', '-------'), ('ARTICULO', 'Artículo en revista'), ('LIBRO', 'Libro')], max_length=20)),
                ('fecha_dictamen', models.DateField()),
                ('articulo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='investigacion.ArticuloCientifico')),
                ('indices', models.ManyToManyField(blank=True, related_name='arbitraje_publicacion_indices', to='nucleo.Indice')),
                ('libro', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='nucleo.Libro')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Arbitraje en publicaciones académicas',
                'verbose_name_plural': 'Arbitrajes en publicaciones académicas',
                'ordering': ['-fecha_dictamen'],
            },
        ),
        migrations.CreateModel(
            name='ClasificacionServicio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255, unique=True)),
                ('descripcion', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Clasificación de servicio',
                'verbose_name_plural': 'Clasificaciones de servicios',
            },
        ),
        migrations.CreateModel(
            name='ConvenioEntidadExterna',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255, unique=True)),
                ('descripcion', models.TextField(blank=True)),
                ('es_agradecimiento', models.BooleanField()),
                ('objetivos', models.TextField()),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField(blank=True, null=True)),
                ('es_renovacion', models.BooleanField(default=False)),
                ('entidades', models.ManyToManyField(to='nucleo.Dependencia')),
                ('financiamientos', models.ManyToManyField(blank=True, to='nucleo.Financiamiento')),
                ('usuarios', models.ManyToManyField(related_name='convenio_entidad_no_academica_usuarios', to=settings.AUTH_USER_MODEL, verbose_name='Académicos participantes')),
            ],
            options={
                'verbose_name': 'Convenio con entidade externa',
                'verbose_name_plural': 'Convenios con entidades externas',
                'ordering': ['-fecha_inicio'],
            },
        ),
        migrations.CreateModel(
            name='OtroProgramaVinculacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('fecha', models.DateField()),
                ('tipo', models.CharField(choices=[('VINCULACION', 'Vinculación'), ('COLABORACION', 'Colaboración'), ('COOPERACION', 'Cooperación'), ('OTRO', 'Otro')], max_length=20)),
                ('descripcion', models.TextField()),
                ('resultados', models.TextField(blank=True)),
                ('dependencia', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='nucleo.Dependencia')),
                ('institucion', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='nucleo.Institucion')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Otro programa o acción de vinculación, colaboración y/o cooperación',
                'verbose_name_plural': 'Otros programas o acciones de vinculación, colaboración y/o cooperación',
                'ordering': ['-fecha', 'nombre'],
            },
        ),
        migrations.CreateModel(
            name='RedAcademica',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255, unique=True)),
                ('descripcion', models.TextField(blank=True)),
                ('ambito', models.CharField(choices=[('', '-------'), ('LOCAL', 'Local'), ('REGIONAL', 'Regional'), ('NACIONAL', 'Nacional'), ('INTERNACIONAL', 'Internacional'), ('OTRO', 'Otro')], max_length=20)),
                ('objetivos', models.TextField()),
                ('fecha_constitucion', models.DateField()),
                ('vigente', models.BooleanField(default=False)),
                ('entidades', models.ManyToManyField(related_name='red_academica_entidades', to='nucleo.Dependencia')),
                ('proyecto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='investigacion.ProyectoInvestigacion')),
                ('usuarios', models.ManyToManyField(related_name='red_academica_usuarios', to=settings.AUTH_USER_MODEL, verbose_name='Académicos participantes')),
            ],
            options={
                'verbose_name': 'Red académica',
                'verbose_name_plural': 'Redes académicas',
                'ordering': ['-fecha_constitucion'],
            },
        ),
        migrations.CreateModel(
            name='ServicioExternoEntidadNoAcademica',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_servicio', models.CharField(max_length=255)),
                ('descripcion', models.TextField(blank=True)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField(blank=True, null=True)),
                ('clasificacion_servicio', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='vinculacion.ClasificacionServicio')),
                ('entidades', models.ManyToManyField(to='nucleo.Dependencia')),
                ('financiamientos', models.ManyToManyField(blank=True, to='nucleo.Financiamiento')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Servicio o asesoria externa a entidades no académicas',
                'verbose_name_plural': 'Servicios o asesorias externas a entidades no académicas',
                'ordering': ['-fecha_inicio'],
            },
        ),
    ]
