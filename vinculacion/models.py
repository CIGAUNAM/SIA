from django.db import models

from django.conf import settings
from autoslug import AutoSlugField
from nucleo.models import User, Pais, Estado, Ciudad, Institucion, Dependencia, Cargo, Proyecto, Revista, Indice, Libro, Editorial, Coleccion
from investigacion.models import CapituloLibroInvestigacion
from django.core.urlresolvers import reverse

RED_ACADEMICA__CLASIFICACION = getattr (settings, 'RED_ACADEMICA__CLASIFICACION', (('LOCAL', 'Local'), ('REGIONAL', 'Regional'), ('NACIONAL', 'Nacional'), ('INTERNACIONAL', 'Internacional'), ('OTRO', 'Otro')))
ENTIDAD_NO_ACADEMICA__CLASIFICACION = getattr (settings, 'ENTIDAD_NO_ACADEMICA__CLASIFICACION', (('FEDERAL', 'Gubernamental federal'), ('ESTATAL', 'Gubernamental estatal'), ('PRIVADO', 'Sector privado'), ('NO_LUCRATIVO', 'Sector privado no lucrativo'), ('EXTRANJERO', 'Extranjero'), ('OTRO', 'Otro')))

# Create your models here.

class ArbitrajePublicacionAcademica(models.Model):
    descripcion = models.TextField(blank=True)
    #tipo_publicacion = models.CharField(max_length=20, choices=(('REVISTA', 'Revista'), ('LIBRO', 'Libro'), ('CAPITULO_LIBRO', 'Capitulo en libro')))
    indices = models.ManyToManyField(Indice, related_name='arbitraje_publicacion_indices', blank=True)
    revista = models.ForeignKey(Revista, blank=True, null=True)
    libro = models.ForeignKey(Libro, blank=True, null=True)
    capitulo_libro = models.ForeignKey(CapituloLibroInvestigacion, blank=True, null=True)
    fecha_dictamen = models.DateField()
    usuario = models.ForeignKey(User)
    #tags = models.ManyToManyField(Tag, related_name='arbitraje_publicacion_academica_tags', blank=True)

    def __str__(self):
        lista_titulos = [self.revista, self.libro, self.capitulo_libro]
        titulo = [x for x in lista_titulos if x != 'n/a']
        titulo = titulo[0]
        return "{} : {}".format(self.tipo_publicacion.title(), titulo, self.fecha_dictamen)

    def get_absolute_url(self):
        return reverse('arbitraje_publicacion_academica_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha_dictamen']
        verbose_name = 'Arbitraje en publicaciones académicas'
        verbose_name_plural = 'Arbitrajes en publicaciones académicas'
        unique_together = ['usuario', 'fecha_dictamen']


class ArbitrajeProyectoInvestigacion(models.Model):
    fecha = models.DateField()
    descripcion = models.TextField(blank=True)
    proyecto = models.ForeignKey(Proyecto)
    usuario = models.ForeignKey(User)
    #tags = models.ManyToManyField(Tag, related_name='arbitraje_proyecto_investigacion_tags', blank=True)

    def __str__(self):
        return "{} : {}".format(str(self.proyecto), self.fecha)

    def get_absolute_url(self):
        return reverse('arbitraje_proyecto_investigacion_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Arbitraje de proyectos de investigación'
        verbose_name_plural = 'Arbitrajes de proyectos de investigación'


class ArbitrajeOtraActividad(models.Model):
    actividad = models.CharField(max_length=255, unique=True)
    #slug = AutoSlugField(populate_from='actividad', unique=True)
    descripcion = models.TextField(blank=True)
    dependencia = models.ForeignKey(Dependencia)
    fecha = models.DateField()
    usuario = models.ForeignKey(User)
    #tags = models.ManyToManyField(Tag, related_name='arbitraje_otras_actividades_tags', blank=True)

    def __str__(self):
        return "{} : {}".format(self.actividad, self.dependencia)

    def get_absolute_url(self):
        return reverse('arbitraje_otra_actividad_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Arbitraje en otras actividades'
        verbose_name_plural = 'Arbitraje en otras actividades'


class RedAcademica(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    #slug = AutoSlugField(populate_from='nombre', unique=True)
    descripcion = models.TextField(blank=True)
    clasificacion = models.CharField(max_length=20, choices=RED_ACADEMICA__CLASIFICACION)
    #regiones = models.ManyToManyField(Region, related_name='red_academica_regiones', blank=True)
    paises = models.ManyToManyField(Pais, related_name='red_academica_paises')
    objetivos = models.TextField()
    fecha_constitucion = models.DateField()
    vigente = models.BooleanField(default=False)
    proyectos = models.ManyToManyField(Proyecto, related_name='red_academica_proyectos', blank=True)
    usuarios = models.ManyToManyField(User, related_name='red_academica_usuarios', verbose_name='Académicos participantes')
    #tags = models.ManyToManyField(Tag, related_name='red_academica_tags', blank=True)

    def __str__(self):
        return "{} : {}".format(self.nombre, self.fecha_constitucion)

    def get_absolute_url(self):
        return reverse('red_academica_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha_constitucion']
        verbose_name = 'Red académica'
        verbose_name_plural = 'Redes académicas'


class ConvenioEntidadNoAcademica(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    #slug = AutoSlugField(populate_from='nombre', unique=True)
    descripcion = models.TextField(blank=True)
    es_agradecimiento = models.BooleanField(blank=True)
    clasificacion_entidad = models.CharField(max_length=20, choices=ENTIDAD_NO_ACADEMICA__CLASIFICACION)
    dependencias = models.ManyToManyField(Dependencia, related_name='convenio_entidad_no_academica_dependencias')
    objetivos = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    es_renovacion = models.BooleanField(default=False)
    incluye_financiamiento = models.BooleanField(default=False)
    usuarios = models.ManyToManyField(User, related_name='convenio_entidad_no_academica_usuarios', verbose_name='Académicos participantes')
    #tags = models.ManyToManyField(Tag, related_name='convenio_entidad_academica_tags', blank=True)

    def __str__(self):
        return "{} : {}".format(self.nombre, self.fecha_inicio)

    def get_absolute_url(self):
        return reverse('convenio_entidad_no_academica_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'Convenio con entidades no académicas'
        verbose_name_plural = 'Convenios con entidades no académicas'


class ClasificacionServicio(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    #slug = AutoSlugField(populate_from='nombre', unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre
    class Meta:
        verbose_name = 'Clasificación de servicio'
        verbose_name_plural = 'Clasificaciones de servicios'


class ServicioExternoEntidadNoAcademica(models.Model):
    nombre_servicio = models.CharField(max_length=255, unique=True)
    #slug = AutoSlugField(populate_from='nombre_servicio', unique=True)
    clasificacion_servicio = models.ForeignKey(ClasificacionServicio)
    descripcion = models.TextField(blank=True)
    dependencia = models.ForeignKey(Dependencia)
    clasificacion_entidad = models.CharField(max_length=20, choices=ENTIDAD_NO_ACADEMICA__CLASIFICACION)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    incluye_financiamiento = models.BooleanField(default=False)
    usuario = models.ForeignKey(User)
    #tags = models.ManyToManyField(Tag, related_name='servicio_externo_entidad_academica_tags', blank=True)

    def __str__(self):
        return "{} : {}".format(self.nombre_servicio, self.fecha_inicio)

    def get_absolute_url(self):
        return reverse('servicio_externo_entidad_no_academica_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'Servicio o asesoria externa a entidades no académicas'
        verbose_name_plural = 'Servicios o asesorias externas a entidades no académicas'


class OtroProgramaVinculacion(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    #slug = AutoSlugField(populate_from='nombre_servicio', unique=True)
    fecha = models.DateField()
    tipo = models.CharField(max_length=20, choices=(('VINCULACION', 'Vinculación'), ('COLABORACION', 'Colaboración'), ('COOPERACION', 'Cooperación'), ('OTRO', 'Otro')))
    descripcion = models.TextField()
    resultados = models.TextField(blank=True)
    dependencias = models.ManyToManyField(Dependencia)
    usuario = models.ForeignKey(User)
    #tags = models.ManyToManyField(Tag, related_name='otro_programa_vinculacion_tags', blank=True)

    def __str__(self):
        return "{} : {}".format(self.nombre, self.fecha)

    def get_absolute_url(self):
        return reverse('otro_programa_vinculacion_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha', 'nombre']
        verbose_name = 'Otro programa o acción de vinculación, colaboración y/o cooperación'
        verbose_name_plural = 'Otros programas o acciones de vinculación, colaboración y/o cooperación'