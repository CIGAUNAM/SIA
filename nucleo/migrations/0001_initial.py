# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-04 00:16
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('descripcion', models.TextField(blank=True)),
                ('tipo', models.CharField(choices=[('INVESTIGADOR', 'Investigador'), ('ADMINISTRATIVO', 'Administrativo'), ('TECNICO', 'Técnico'), ('OTRO', 'Otro')], default='OTRO', max_length=30)),
                ('fecha_nacimiento', models.DateField(blank=True, null=True)),
                ('rfc', models.SlugField(max_length=20, unique=True)),
                ('direccion1', models.CharField(max_length=255)),
                ('direccion2', models.CharField(blank=True, max_length=255)),
                ('telefono', models.SlugField(blank=True, max_length=20)),
                ('celular', models.SlugField(blank=True, max_length=20)),
                ('url', models.URLField(blank=True, null=True)),
                ('sni', models.PositiveSmallIntegerField(default=0)),
                ('pride', models.CharField(choices=[('-', '-'), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], default='-', max_length=2)),
                ('ingreso_unam', models.DateField(blank=True, null=True)),
                ('ingreso_entidad', models.DateField(blank=True, null=True)),
            ],
            options={
                'ordering': ['last_name'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AreaConocimiento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoria', models.CharField(choices=[('LSBM', 'Life Sciences and Biomedicine'), ('PHYS', 'Physical Sciences'), ('TECH', 'Technology'), ('ARTH', 'Arts and Humanities'), ('SS', 'Social Sciences'), ('ZTRA', 'Otra')], max_length=20)),
                ('area_conocimiento', models.CharField(max_length=255, unique=True)),
                ('descripcion', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['categoria', 'area_conocimiento'],
                'verbose_name': 'Área General de Conocimiento',
                'verbose_name_plural': 'Áreas Generales de Conocimiento',
            },
        ),
        migrations.CreateModel(
            name='AreaEspecialidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('especialidad', models.CharField(max_length=255, unique=True)),
                ('descripcion', models.TextField(blank=True)),
                ('area_conocimiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.AreaConocimiento')),
            ],
            options={
                'ordering': ['especialidad'],
                'verbose_name': 'Área de especialidad de WOS y otras entidades',
                'verbose_name_plural': 'Áreas de especialidades de WOS y otras entidades',
            },
        ),
        migrations.CreateModel(
            name='Beca',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beca', models.CharField(max_length=200, unique=True)),
                ('descripcion', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cargo', models.CharField(max_length=255)),
                ('descripcion', models.TextField(blank=True)),
                ('tipo_cargo', models.CharField(choices=[('ACADEMICO', 'Académico'), ('ADMINISTRATIVO', 'Administrativo'), ('OTRO', 'Otro')], max_length=20)),
            ],
            options={
                'ordering': ['cargo'],
            },
        ),
        migrations.CreateModel(
            name='Ciudad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ciudad', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['estado', 'ciudad'],
                'verbose_name_plural': 'Ciudades',
            },
        ),
        migrations.CreateModel(
            name='Coleccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coleccion', models.CharField(max_length=255, unique=True)),
                ('descripcion', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['coleccion'],
                'verbose_name': 'Colección',
                'verbose_name_plural': 'Colecciones',
            },
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departamento', models.CharField(max_length=255)),
                ('descripcion', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['departamento', 'dependencia'],
            },
        ),
        migrations.CreateModel(
            name='Dependencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dependencia', models.CharField(max_length=255)),
                ('descripcion', models.TextField(blank=True)),
                ('subsistema_unam', models.CharField(choices=[('DIFUSION_CULTURAL', 'Subsistema de Difusión Cultural'), ('ESTUDIOS_POSGRADO', 'Subsistema de Estudios de Posgrado'), ('HUMANIDADES', 'Subsistema de Humanidades'), ('INVESTIGACION_CIENTIFICA', 'Subsistema de Investigación Científica'), ('ESCUELAS', 'Facultades y Escuelas'), ('DESARROLLO_INSTITUCIONAL', 'Desarrollo Institucional'), ('NO', 'No')], default='NO', max_length=50, verbose_name='Subsistema UNAM')),
                ('ciudad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Ciudad')),
            ],
            options={
                'ordering': ['institucion', 'dependencia'],
            },
        ),
        migrations.CreateModel(
            name='Distincion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_distincion', models.CharField(max_length=255, unique=True)),
                ('descripcion', models.TextField(blank=True)),
                ('tipo', models.CharField(choices=[('PREMIO', 'Premio'), ('DISTINCION', 'Distinción'), ('RECONOCIMIENTO', 'Reconocimiento'), ('MEDALLA', 'Medalla'), ('GUGGENHEIM', 'Beca Guggenheim'), ('HONORIS_CAUSA', 'Doctorado Honoris Causa'), ('OTRO', 'Otro')], max_length=30)),
            ],
            options={
                'ordering': ['nombre_distincion'],
                'verbose_name': 'Distinción',
                'verbose_name_plural': 'Distinciones',
            },
        ),
        migrations.CreateModel(
            name='Editorial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('editorial', models.CharField(max_length=255, unique=True)),
                ('descripcion', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['editorial'],
                'verbose_name_plural': 'Editoriales',
            },
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(max_length=200)),
            ],
            options={
                'ordering': ['pais', 'estado'],
            },
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_evento', models.CharField(max_length=255)),
                ('descripcion', models.TextField(blank=True)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('ubicacion', models.TextField(blank=True)),
                ('dependencias', models.ManyToManyField(related_name='evento_dependencias', to='nucleo.Dependencia')),
            ],
            options={
                'ordering': ['fecha_inicio', 'nombre_evento'],
            },
        ),
        migrations.CreateModel(
            name='Financiamiento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_financiamiento', models.CharField(choices=[('UNAM', (('ASIGNADO', 'Presupuesto asignado a la entidad'), ('CONCURSADO', 'Presupuesto concursado por la entidad'), ('AUTOGENERADO', 'Recursos autogenerados (extraordinarios)'), ('OTRO', 'Otro'))), ('Externo', (('ESTATAL', 'Gubernamental Estatal'), ('FEDERAL', 'Gubernamental Federal'), ('LUCRATIVO', 'Privado lucrativo'), ('NO_LUCRATIVO', 'Privado no lucrativo'), ('EXTRANJERO', 'Recursos del extranjero')))], max_length=80)),
                ('descripcion', models.TextField(blank=True)),
                ('clave_proyecto', models.CharField(max_length=255)),
                ('dependencias_financiamiento', models.ManyToManyField(blank=True, related_name='financiamiento_dependencias_financiamiento', to='nucleo.Dependencia')),
            ],
            options={
                'verbose_name': 'Financiamiento',
                'verbose_name_plural': 'Financiamientos',
            },
        ),
        migrations.CreateModel(
            name='ImpactoSocial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('impacto_social', models.CharField(max_length=255, unique=True)),
                ('descripcion', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['impacto_social'],
                'verbose_name': 'Impacto social',
                'verbose_name_plural': 'Impactos sociales',
            },
        ),
        migrations.CreateModel(
            name='Indice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('indice', models.CharField(max_length=255, unique=True)),
                ('descripcion', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Institucion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institucion', models.CharField(max_length=255, unique=True)),
                ('descripcion', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['institucion'],
                'verbose_name': 'Institución',
                'verbose_name_plural': 'Instituciones',
            },
        ),
        migrations.CreateModel(
            name='Libro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_libro', models.CharField(max_length=255, unique=True)),
                ('descripcion', models.TextField(blank=True)),
                ('tipo', models.CharField(choices=[('INVESTIGACION', 'Investigación'), ('DIVULGACION', 'Divulgación')], max_length=50)),
                ('fecha', models.DateField()),
                ('numero_edicion', models.PositiveIntegerField(default=1)),
                ('numero_paginas', models.PositiveIntegerField(default=0)),
                ('volumen', models.CharField(blank=True, max_length=255)),
                ('isbn', models.SlugField(max_length=30)),
                ('url', models.URLField(blank=True)),
                ('status', models.CharField(choices=[('PUBLICADO', 'Publicado'), ('EN_PRENSA', 'En prensa'), ('ACEPTADO', 'Aceptado'), ('ENVIADO', 'Enviado'), ('OTRO', 'Otro')], max_length=20)),
                ('ciudad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Ciudad')),
                ('coleccion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='nucleo.Coleccion')),
                ('coordinadores', models.ManyToManyField(blank=True, related_name='libro_coordinadores', to=settings.AUTH_USER_MODEL)),
                ('editores', models.ManyToManyField(blank=True, related_name='libro_editores', to=settings.AUTH_USER_MODEL)),
                ('editorial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Editorial')),
            ],
            options={
                'ordering': ['nombre_libro'],
                'get_latest_by': ['fecha', 'nombre_libro', 'editorial'],
            },
        ),
        migrations.CreateModel(
            name='Memoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('memoria', models.CharField(max_length=255, unique=True)),
                ('descripcion', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Metodologia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metodologia', models.CharField(max_length=255, unique=True)),
                ('descripcion', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['metodologia'],
            },
        ),
        migrations.CreateModel(
            name='Nombramiento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombramiento', models.CharField(max_length=255, unique=True)),
                ('clave', models.CharField(max_length=20, unique=True)),
                ('descripcion', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pais', models.CharField(max_length=60, unique=True)),
                ('nombre_extendido', models.CharField(max_length=200, unique=True)),
                ('codigo', models.SlugField(max_length=2, unique=True)),
            ],
            options={
                'ordering': ['pais'],
                'verbose_name': 'País',
                'verbose_name_plural': 'Paises',
            },
        ),
        migrations.CreateModel(
            name='ProblemaNacionalConacyt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200, unique=True)),
                ('descripcion', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': ['Problemática Nacional CONACYT'],
                'verbose_name_plural': ['Problemáticas Nacionales CONACYT'],
            },
        ),
        migrations.CreateModel(
            name='ProgramaDoctorado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('programa', models.CharField(max_length=255, unique=True)),
                ('descripcion', models.TextField(blank=True)),
                ('area_conocimiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.AreaConocimiento', verbose_name='Área de conocimiento')),
            ],
            options={
                'ordering': ['programa'],
                'verbose_name': 'Programa de doctorado',
                'verbose_name_plural': 'Programas de doctorado',
            },
        ),
        migrations.CreateModel(
            name='ProgramaFinanciamiento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('programa_financiamiento', models.CharField(max_length=255, unique=True)),
                ('descripcion', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['programa_financiamiento'],
            },
        ),
        migrations.CreateModel(
            name='ProgramaLicenciatura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('programa', models.CharField(max_length=255, unique=True)),
                ('descripcion', models.TextField(blank=True)),
                ('area_conocimiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.AreaConocimiento', verbose_name='Área de conocimiento')),
            ],
            options={
                'ordering': ['programa'],
                'verbose_name': 'Programa de licenciatura',
                'verbose_name_plural': 'Programas de licenciatura',
            },
        ),
        migrations.CreateModel(
            name='ProgramaMaestria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('programa', models.CharField(max_length=255, unique=True)),
                ('descripcion', models.TextField(blank=True)),
                ('area_conocimiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.AreaConocimiento', verbose_name='Área de conocimiento')),
            ],
            options={
                'ordering': ['programa'],
                'verbose_name': 'Programa de maestria',
                'verbose_name_plural': 'Programas de maestria',
            },
        ),
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_proyecto', models.CharField(max_length=255, unique=True)),
                ('descripcion', models.TextField(blank=True)),
                ('tipo', models.CharField(choices=[('INVESTIGACION', 'Investigación'), ('OTRO', 'Otro')], max_length=50)),
                ('es_permanente', models.BooleanField(default=False)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('status', models.CharField(choices=[('NUEVO', 'Nuevo'), ('EN_PROCESO', 'En proceso'), ('CONCLUIDO', 'Concluído'), ('OTRO', 'Otro')], max_length=30)),
                ('clasificacion', models.CharField(choices=[('BASICO', 'Básico'), ('APLICADO', 'Aplicado'), ('DESARROLLO_TECNOLOGICO', 'Desarrollo tecnológico'), ('INNOVACION', 'Innovación'), ('INVESTIGACION_FRONTERA', 'Investigación de frontera'), ('OTRA', 'Otra')], max_length=30)),
                ('organizacion', models.CharField(choices=[('INDIVIDUAL', 'Individual'), ('COLECTIVO', 'Colectivo')], max_length=30)),
                ('modalidad', models.CharField(choices=[('DISCIPLINARIO', 'Disciplinario'), ('MULTIDISCIPLINARIO', 'Multidisciplinario'), ('INTERDISCIPLINARIO', 'Interisciplinario'), ('TRANSDISCIPLINARIO', 'Transdisciplinario'), ('OTRA', 'Otra')], max_length=30)),
                ('tematica_genero', models.BooleanField(default=False)),
                ('descripcion_problema_nacional_conacyt', models.TextField(blank=True)),
                ('alumnos_doctorado', models.ManyToManyField(blank=True, related_name='proyecto_alumnos_doctorado', to=settings.AUTH_USER_MODEL)),
                ('alumnos_licenciatura', models.ManyToManyField(blank=True, related_name='proyecto_alumnos_licenciatura', to=settings.AUTH_USER_MODEL)),
                ('alumnos_maestria', models.ManyToManyField(blank=True, related_name='proyecto_alumnos_maestria', to=settings.AUTH_USER_MODEL)),
                ('dependencias', models.ManyToManyField(blank=True, related_name='proyecto_dependencias', to='nucleo.Dependencia')),
                ('especialidades', models.ManyToManyField(blank=True, related_name='proyecto_especialidades', to='nucleo.AreaEspecialidad')),
                ('financiamientos', models.ManyToManyField(blank=True, to='nucleo.Financiamiento')),
                ('impactos_sociales', models.ManyToManyField(blank=True, related_name='proyecto_impactos_sociales', to='nucleo.ImpactoSocial')),
                ('metodologias', models.ManyToManyField(blank=True, related_name='proyecto_metodologias', to='nucleo.Metodologia')),
                ('participantes', models.ManyToManyField(blank=True, related_name='proyecto_participantes', to=settings.AUTH_USER_MODEL)),
                ('problemas_nacionales_conacyt', models.ManyToManyField(to='nucleo.ProblemaNacionalConacyt')),
                ('tecnicos', models.ManyToManyField(blank=True, related_name='proyecto_impactos_tecnicos', to=settings.AUTH_USER_MODEL)),
                ('usuarios', models.ManyToManyField(related_name='proyecto_responsables', to=settings.AUTH_USER_MODEL, verbose_name='Responsables')),
            ],
            options={
                'ordering': ['fecha_inicio', 'nombre_proyecto'],
            },
        ),
        migrations.CreateModel(
            name='Reconocimiento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reconocimiento', models.CharField(max_length=255, unique=True)),
                ('descripcion', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['reconocimiento'],
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(max_length=200)),
                ('descripcion', models.TextField(blank=True)),
                ('ciudades', models.ManyToManyField(blank=True, related_name='region_ciudades', to='nucleo.Ciudad')),
                ('estados', models.ManyToManyField(blank=True, related_name='region_estados', to='nucleo.Estado')),
                ('paises', models.ManyToManyField(blank=True, related_name='region_paises', to='nucleo.Pais')),
            ],
            options={
                'ordering': ['region'],
                'verbose_name': 'Región',
                'verbose_name_plural': 'Regiones',
            },
        ),
        migrations.CreateModel(
            name='Revista',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_revista', models.CharField(max_length=255, unique=True)),
                ('descripcion', models.TextField(blank=True)),
                ('url', models.URLField(blank=True)),
                ('editorial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Editorial')),
            ],
            options={
                'ordering': ['nombre_revista'],
                'get_latest_by': ['fecha', 'nombre_revista', 'editorial'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(help_text='Etiqueta para categorizar objetos.', max_length=50, unique=True)),
            ],
            options={
                'ordering': ['tag'],
            },
        ),
        migrations.CreateModel(
            name='Tesis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255, unique=True)),
                ('descripcion', models.TextField(blank=True)),
                ('grado_academico', models.CharField(choices=[('LICENCIATURA', 'licenciatura'), ('MAESTRIA', 'Maestría'), ('DOCTORADO', 'Doctorado')], max_length=20)),
                ('documento_tesis', models.FileField(upload_to='')),
                ('fecha_examen', models.DateField()),
                ('alumno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tesis_alumno', to=settings.AUTH_USER_MODEL)),
                ('beca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Beca')),
                ('dependencia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Dependencia')),
                ('reconocimiento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='nucleo.Reconocimiento')),
            ],
            options={
                'ordering': ['-fecha_examen'],
                'verbose_name': 'Tesis',
                'verbose_name_plural': 'Tesis',
            },
        ),
        migrations.CreateModel(
            name='TipoDocumento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=50, unique=True)),
                ('descripcion', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['tipo'],
                'verbose_name': 'Tipo de documento',
                'verbose_name_plural': 'Tipos de documentos',
            },
        ),
        migrations.CreateModel(
            name='TipoEvento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_evento', models.CharField(max_length=100, unique=True)),
                ('descripcion', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Tipo de evento',
                'verbose_name_plural': 'Tipos de eventos',
            },
        ),
        migrations.CreateModel(
            name='Ubicacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direccion1', models.CharField(max_length=255, verbose_name='Dirección')),
                ('direccion2', models.CharField(blank=True, max_length=255, verbose_name='Dirección (continuación)')),
                ('descripcion', models.TextField(blank=True)),
                ('codigo_postal', models.CharField(blank=True, max_length=7)),
                ('telefono', models.SlugField(blank=True, max_length=20)),
                ('ciudad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Ciudad')),
            ],
            options={
                'ordering': ['ciudad', 'direccion1'],
                'verbose_name': 'Ubicación',
                'verbose_name_plural': 'Ubicaciones',
            },
        ),
        migrations.CreateModel(
            name='ZonaPais',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zona', models.CharField(max_length=60, unique=True)),
            ],
            options={
                'ordering': ['zona'],
                'verbose_name': 'Zona de paises',
                'verbose_name_plural': 'Zonas de paises',
            },
        ),
        migrations.AddField(
            model_name='pais',
            name='zona',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.ZonaPais'),
        ),
        migrations.AddField(
            model_name='libro',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='libro_tags', to='nucleo.Tag'),
        ),
        migrations.AddField(
            model_name='libro',
            name='usuarios',
            field=models.ManyToManyField(related_name='libro_autores', to=settings.AUTH_USER_MODEL, verbose_name='Autores'),
        ),
        migrations.AddField(
            model_name='institucion',
            name='pais',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Pais'),
        ),
        migrations.AddField(
            model_name='financiamiento',
            name='programas_financiamiento',
            field=models.ManyToManyField(blank=True, related_name='financiamiento_programas_financiamiento', to='nucleo.ProgramaFinanciamiento'),
        ),
        migrations.AddField(
            model_name='evento',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.TipoEvento'),
        ),
        migrations.AddField(
            model_name='estado',
            name='pais',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Pais'),
        ),
        migrations.AddField(
            model_name='editorial',
            name='pais',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Pais'),
        ),
        migrations.AddField(
            model_name='dependencia',
            name='institucion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Institucion'),
        ),
        migrations.AddField(
            model_name='departamento',
            name='dependencia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Dependencia'),
        ),
        migrations.AddField(
            model_name='ciudad',
            name='estado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Estado'),
        ),
        migrations.AlterUniqueTogether(
            name='cargo',
            unique_together=set([('cargo', 'tipo_cargo')]),
        ),
        migrations.AddField(
            model_name='beca',
            name='institucion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nucleo.Institucion'),
        ),
        migrations.AddField(
            model_name='user',
            name='ciudad',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='nucleo.Ciudad'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='pais_origen',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='nucleo.Pais'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AlterUniqueTogether(
            name='ubicacion',
            unique_together=set([('direccion1', 'direccion2', 'ciudad')]),
        ),
        migrations.AlterUniqueTogether(
            name='evento',
            unique_together=set([('fecha_inicio', 'nombre_evento')]),
        ),
        migrations.AlterUniqueTogether(
            name='estado',
            unique_together=set([('estado', 'pais')]),
        ),
        migrations.AlterUniqueTogether(
            name='dependencia',
            unique_together=set([('dependencia', 'institucion')]),
        ),
        migrations.AlterUniqueTogether(
            name='departamento',
            unique_together=set([('departamento', 'dependencia')]),
        ),
        migrations.AlterUniqueTogether(
            name='ciudad',
            unique_together=set([('ciudad', 'estado')]),
        ),
    ]
