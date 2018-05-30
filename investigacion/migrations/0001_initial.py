# Generated by Django 2.0.5 on 2018-05-03 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArticuloCientifico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255, unique=True)),
                ('descripcion', models.TextField(blank=True)),
                ('tipo', models.CharField(choices=[('ARTICULO', 'Artículo'), ('ACTA', 'Acta'), ('CARTA', 'Carta'), ('RESENA', 'Reseña'), ('OTRO', 'Otro')], max_length=16)),
                ('volumen', models.CharField(blank=True, max_length=100, null=True)),
                ('numero', models.CharField(blank=True, max_length=100, null=True)),
                ('fecha', models.DateField()),
                ('issn_impreso', models.CharField(blank=True, max_length=40, verbose_name='ISSN Impreso')),
                ('issn_online', models.CharField(blank=True, max_length=40, verbose_name='ISSN Online')),
                ('status', models.CharField(choices=[('', '-------'), ('ENVIADO', 'Enviado'), ('ACEPTADO', 'Aceptado'), ('EN_PRENSA', 'En prensa'), ('PUBLICADO', 'Publicado'), ('OTRO', 'Otro')], max_length=20)),
                ('solo_electronico', models.BooleanField(default=False)),
                ('url', models.URLField(blank=True)),
                ('pagina_inicio', models.PositiveIntegerField()),
                ('pagina_fin', models.PositiveIntegerField()),
                ('id_doi', models.CharField(blank=True, max_length=100, null=True)),
                ('id_wos', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name': 'Artículo científico',
                'verbose_name_plural': 'Artículos científicos',
                'ordering': ['fecha', 'titulo'],
            },
        ),
        migrations.CreateModel(
            name='CapituloLibroInvestigacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255, unique=True)),
                ('descripcion', models.TextField(blank=True)),
                ('pagina_inicio', models.PositiveIntegerField()),
                ('pagina_fin', models.PositiveIntegerField()),
            ],
            options={
                'verbose_name': 'Capítulo en libro',
                'verbose_name_plural': 'Capítulos en libros',
                'ordering': ['titulo'],
            },
        ),
        migrations.CreateModel(
            name='InformeTecnico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255, unique=True)),
                ('descripcion', models.TextField(blank=True)),
                ('fecha', models.DateField()),
                ('numero_paginas', models.PositiveIntegerField(default=1)),
                ('es_publico', models.BooleanField(default=False)),
                ('url', models.URLField(blank=True)),
            ],
            options={
                'verbose_name': 'Informe técnico de acceso público',
                'verbose_name_plural': 'Informes técnicos de acceso público',
                'ordering': ['fecha', 'titulo'],
            },
        ),
        migrations.CreateModel(
            name='MapaArbitrado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255, unique=True)),
                ('descripcion', models.TextField(blank=True)),
                ('escala', models.CharField(max_length=30)),
                ('status', models.CharField(choices=[('', '-------'), ('ENVIADO', 'Enviado'), ('ACEPTADO', 'Aceptado'), ('EN_PRENSA', 'En prensa'), ('PUBLICADO', 'Publicado'), ('OTRO', 'Otro')], max_length=20)),
                ('fecha', models.DateField()),
                ('numero_edicion', models.PositiveIntegerField(default=1)),
                ('numero_paginas', models.PositiveIntegerField(default=1)),
                ('volumen', models.CharField(blank=True, max_length=255)),
                ('isbn', models.SlugField(blank=True, max_length=30)),
                ('url', models.URLField(blank=True)),
            ],
            options={
                'verbose_name': 'Mapa arbitrado',
                'verbose_name_plural': 'Mapas arbitrados',
                'ordering': ['fecha', 'titulo'],
            },
        ),
        migrations.CreateModel(
            name='ProyectoInvestigacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255, unique=True)),
                ('descripcion', models.TextField(blank=True)),
                ('es_permanente', models.BooleanField(default=False)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('', '-------'), ('NUEVO', 'Nuevo'), ('EN_PROCESO', 'En proceso'), ('CONCLUIDO', 'Concluído'), ('OTRO', 'Otro')], max_length=30)),
                ('clasificacion', models.CharField(choices=[('', '-------'), ('BASICO', 'Básico'), ('APLICADO', 'Aplicado'), ('DESARROLLO_TECNOLOGICO', 'Desarrollo tecnológico'), ('INNOVACION', 'Innovación'), ('INVESTIGACION_FRONTERA', 'Investigación de frontera'), ('OTRA', 'Otra')], max_length=30)),
                ('organizacion', models.CharField(choices=[('', '-------'), ('INDIVIDUAL', 'Individual'), ('COLECTIVO', 'Colectivo')], max_length=30)),
                ('modalidad', models.CharField(choices=[('', '-------'), ('DISCIPLINARIO', 'Disciplinario'), ('MULTIDISCIPLINARIO', 'Multidisciplinario'), ('INTERDISCIPLINARIO', 'Interisciplinario'), ('TRANSDISCIPLINARIO', 'Transdisciplinario'), ('OTRA', 'Otra')], max_length=30)),
                ('tematica_genero', models.BooleanField(default=False)),
                ('descripcion_problema_nacional_conacyt', models.TextField(blank=True)),
                ('financiamiento_conacyt', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('financiamiento_papiit', models.CharField(blank=True, max_length=20, null=True, unique=True)),
            ],
            options={
                'ordering': ['nombre'],
            },
        ),
    ]
