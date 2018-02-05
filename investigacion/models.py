from django.db import models
from django.conf import settings
from django.urls import reverse
from nucleo.models import User, Pais, Estado, Ciudad, Institucion, Dependencia, \
    Revista, Indice, Libro, Editorial, Coleccion, ProblemaNacionalConacyt, Financiamiento, Metodologia, \
    AreaEspecialidad, ImpactoSocial 
from sortedm2m.fields import SortedManyToManyField


STATUS_PUBLICACION = getattr(settings, 'STATUS_PUBLICACION', (('PUBLICADO', 'Publicado'), ('EN_PRENSA', 'En prensa'),
                                                              ('ACEPTADO', 'Aceptado'), ('ENVIADO', 'Enviado'),
                                                              ('OTRO', 'Otro')))
STATUS_PROYECTO = getattr(settings, 'STATUS_PROYECTO', (('NUEVO', 'Nuevo'), ('EN_PROCESO', 'En proceso'),
                                                        ('CONCLUIDO', 'Concluído'), ('OTRO', 'Otro')))
CLASIFICACION_PROYECTO = getattr(settings,
                                 'CLASIFICACION_PROYECTO', (('BASICO', 'Ciencia Básica'),
                                                            ('APLICADO', 'Investigaciòn Aplicada'),
                                                            ('DESARROLLO_TECNOLOGICO', 'Desarrollo tecnológico'),
                                                            ('INNOVACION', 'Innovación'),
                                                            ('INVESTIGACION_FRONTERA', 'Investigación de frontera'),
                                                            ('OTRO', 'Otro')))
ORGANIZACION_PROYECTO = getattr(settings, 'ORGANIZACION_PROYECTO', (('INDIVIDUAL', 'Individual'),
                                                                    ('COLECTIVO', 'Colectivo')))
MODALIDAD_PROYECTO = getattr(settings, 'MODALIDAD_PROYECTO', (('DISCIPLINARIO', 'Disciplinario'),
                                                              ('MULTIDISCIPLINARIO', 'Multidisciplinario'),
                                                              ('INTERDISCIPLINARIO', 'Interisciplinario'),
                                                              ('TRANSDISCIPLINARIO', 'Transdisciplinario')))
FINANCIAMIENTO_UNAM = getattr(settings,
                              'FINANCIAMIENTO_UNAM', (('ASIGNADO', 'Presupuesto asignado a la entidad'),
                                                      ('CONCURSADO', 'Presupuesto concursado por la entidad'),
                                                      ('AUTOGENERADO', 'Recursos autogenerados (extraordinarios)'),
                                                      ('OTRO', 'Otro')))
FINANCIAMIENTO_EXTERNO = getattr(settings, 'FINANCIAMIENTO_UNAM', (('ESTATAL', 'Gubernamental Estatal'),
                                                                   ('FEDERAL', 'Gubernamental Federal'),
                                                                   ('LUCRATIVO', 'Privado lucrativo'),
                                                                   ('NO_LUCRATIVO', 'Privado no lucrativo'),
                                                                   ('EXTRANJERO', 'Recursos del extranjero'),
                                                                   ('OTRO', 'Otro')))
FINANCIAMIENTO_TIPO = getattr(settings, 'FINANCIAMIENTO_TIPO',
                              (('UNAM', FINANCIAMIENTO_UNAM), ('Externo', FINANCIAMIENTO_EXTERNO)))


# Create your models here.


class ProyectoInvestigacion(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)
    es_permanente = models.BooleanField(default=False)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    institucion = models.ForeignKey(Institucion, on_delete=models.DO_NOTHING)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.DO_NOTHING)
    usuarios = SortedManyToManyField(User, related_name='proyecto_investigacion_responsables',
                                     verbose_name='Responsables')
    participantes = models.ManyToManyField(User, related_name='proyecto_investigacion_participantes', blank=True)
    status = models.CharField(max_length=30, choices=STATUS_PROYECTO)
    clasificacion = models.CharField(max_length=30, choices=CLASIFICACION_PROYECTO)
    organizacion = models.CharField(max_length=30, choices=ORGANIZACION_PROYECTO)
    modalidad = models.CharField(max_length=30, choices=MODALIDAD_PROYECTO)
    tematica_genero = models.BooleanField(default=False)
    problema_nacional_conacyt = models.ForeignKey(ProblemaNacionalConacyt, blank=True, null=True,
                                                  on_delete=models.DO_NOTHING)
    descripcion_problema_nacional_conacyt = models.TextField(blank=True)

    financiamientos = models.ManyToManyField(Financiamiento, blank=True)
    financiamiento_conacyt = models.CharField(max_length=20, unique=True, null=True, blank=True)
    financiamiento_papiit = models.CharField(max_length=20, unique=True, null=True, blank=True)

    metodologias = models.ManyToManyField(Metodologia, related_name='proyecto_investigacion_metodologias', blank=True)
    especialidades = models.ManyToManyField(AreaEspecialidad, related_name='proyecto_investigacion_especialidades',
                                            blank=True)
    impactos_sociales = models.ManyToManyField(ImpactoSocial, related_name='proyecto_investigacion_impactos_sociales',
                                               blank=True)
    tecnicos = models.ManyToManyField(User, related_name='proyecto_investigacion_impactos_tecnicos', blank=True)
    alumnos_doctorado = models.ManyToManyField(User, related_name='proyecto_investigacion_alumnos_doctorado',
                                               blank=True)
    alumnos_maestria = models.ManyToManyField(User, related_name='proyecto_investigacion_alumnos_maestria',
                                              blank=True)
    alumnos_licenciatura = models.ManyToManyField(User, related_name='proyecto_investigacion_alumnos_licenciatura',
                                                  blank=True)

    def __str__(self):
        if self.nombre == 'Ninguno':
            return 'Ninguno'
        else:
            return "{} : {}".format(self.nombre, self.fecha_inicio)

    def natural_key(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('proyecto_investigacion_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['nombre']
        unique_together = ['financiamiento_conacyt', 'financiamiento_papiit']


class ArticuloCientifico(models.Model):
    titulo = models.CharField(max_length=255, unique=True)
    # slug = AutoSlugField(populate_from='titulo', unique=True)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=16, choices=(('ARTICULO', 'Artículo'), ('ACTA', 'Acta'), ('CARTA', 'Carta'),
                                                    ('RESENA', 'Reseña'), ('OTRO', 'Otro')))
    revista = models.ForeignKey(Revista, on_delete=models.DO_NOTHING)
    volumen = models.CharField(max_length=100, null=True, blank=True)
    numero = models.CharField(max_length=100, null=True, blank=True)
    fecha = models.DateField(auto_now=False)
    issn_impreso = models.CharField(max_length=40, blank=True, verbose_name='ISSN Impreso')
    issn_online = models.CharField(max_length=40, blank=True, verbose_name='ISSN Online')
    status = models.CharField(max_length=20, choices=STATUS_PUBLICACION)
    solo_electronico = models.BooleanField(default=False)
    usuarios = SortedManyToManyField(User, related_name='articulo_cientifico_autores', verbose_name='Autores')
    alumnos = models.ManyToManyField(User, related_name='articulo_cientifico_alumnos', blank=True)
    indices = models.ManyToManyField(Indice, related_name='articulo_cientifico_indices', blank=True)
    url = models.URLField(blank=True)
    pagina_inicio = models.PositiveIntegerField()
    pagina_fin = models.PositiveIntegerField()
    id_doi = models.CharField(max_length=100, null=True, blank=True)
    id_wos = models.CharField(max_length=100, null=True, blank=True)
    proyecto = models.ForeignKey(ProyectoInvestigacion, blank=True, null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{} : {} : {}".format(self.titulo, self.tipo.title(), self.revista)

    def get_absolute_url(self):
        return reverse('articulo_cientifico_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Artículo científico"
        verbose_name_plural = "Artículos científicos"
        ordering = ['fecha', 'titulo']


class CapituloLibroInvestigacion(models.Model):
    titulo = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)
    libro = models.ForeignKey(Libro, on_delete=models.DO_NOTHING)
    pagina_inicio = models.PositiveIntegerField()
    pagina_fin = models.PositiveIntegerField()
    usuarios = SortedManyToManyField(User, related_name='capitulo_libro_investigacion_autores', verbose_name='Autores')

    def __str__(self):
        return "{} : {}".format(self.titulo, self.libro)

    def get_absolute_url(self):
        return reverse('capitulo_libro_investigacion_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Capítulo en libro"
        verbose_name_plural = "Capítulos en libros"
        ordering = ['titulo']


class MapaArbitrado(models.Model):
    titulo = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)
    escala = models.CharField(max_length=30)
    usuarios = SortedManyToManyField(User, related_name='mapa_arbitrado_autores', verbose_name='Autores')
    editores = models.ManyToManyField(User, related_name='mapa_arbitrado_editores', blank=True)
    coordinadores = models.ManyToManyField(User, related_name='mapa_arbitrado_coordinadores', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_PUBLICACION)
    pais = models.ForeignKey(Pais, on_delete=models.DO_NOTHING)
    estado = models.ForeignKey(Estado, on_delete=models.DO_NOTHING)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.DO_NOTHING)
    editorial = models.ForeignKey(Editorial, on_delete=models.DO_NOTHING)
    fecha = models.DateField(auto_now=False)
    numero_edicion = models.PositiveIntegerField(default=1)
    numero_paginas = models.PositiveIntegerField(default=1)
    coleccion = models.ForeignKey(Coleccion, blank=True, null=True, on_delete=models.DO_NOTHING)
    volumen = models.CharField(max_length=255, blank=True)
    isbn = models.SlugField(max_length=30, blank=True)
    url = models.URLField(blank=True)
    proyecto = models.ForeignKey(ProyectoInvestigacion, blank=True, null=True, on_delete=models.DO_NOTHING)
    # proyectos = models.ManyToManyField(Proyecto, related_name='mapa_arbitrado_proyectos', blank=True)
    # tags = models.ManyToManyField(Tag, related_name='mapa_arbitrado_tags', blank=True)

    def __str__(self):
        return "{} : ({}) : {}".format(self.titulo, self.escala, self.fecha)

    def get_absolute_url(self):
        return reverse('mapa_arbitrado_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Mapa arbitrado"
        verbose_name_plural = "Mapas arbitrados"
        ordering = ['fecha', 'titulo']


class InformeTecnico(models.Model):
    titulo = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)
    usuarios = SortedManyToManyField(User, related_name='informe_tecnico_autores', verbose_name='Autores')
    fecha = models.DateField(auto_now=False)
    numero_paginas = models.PositiveIntegerField(default=1)
    proyecto = models.ForeignKey(ProyectoInvestigacion, on_delete=models.DO_NOTHING)
    es_publico = models.BooleanField(default=False)
    url = models.URLField(blank=True)

    def __str__(self):
        return "{} : {}".format(self.titulo, self.fecha)

    def get_absolute_url(self):
        return reverse('informe_tecnico_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Informe técnico de acceso público"
        verbose_name_plural = "Informes técnicos de acceso público"
        ordering = ['fecha', 'titulo']
