from django.db import models

#from django.contrib.auth.models import User
from autoslug import AutoSlugField
from nucleo.models import User, Tag, Ubicacion, Region, Dependencia, ProgramaFinanciamiento, ImpactoSocial, Proyecto, Indice

# Create your models here.

class TipoDesarrollo(models.Model):
    tipo_desarrollo = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField()
    slug = AutoSlugField(populate_from='tipo_desarrollo', unique=True)

    def __str__(self):
        return self.tipo_desarrollo

    class Meta:
        ordering = ['tipo_desarrollo']
        verbose_name = 'Tipo de desarrollo'
        verbose_name_plural = 'Tipos de desarrollo'


class Licencia(models.Model):
    licencia = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(populate_from='licencia', unique=True)
    descripcion = models.TextField()
    url = models.URLField()

    def __str__(self):
        return self.licencia

    class Meta:
        ordering = ['licencia']

"""
class TipoParticipacionProyecto(models.Model):
    tipo = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(populate_from='tipo', unique=True)
    descripcion = models.TextField()

    def __str__(self):
        return self.tipo

    class Meta:
        verbose_name = 'Tipo de participación en proyecto'
        verbose_name_plural = 'Tipos de participación en proyectos'


class StatusProyecto(models.Model):
    status = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(populate_from='status', unique=True)
    descripcion = models.TextField()

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = 'Status de proyecto'
        verbose_name_plural = 'Status de proyectos'

class ClasificacionProyecto(models.Model):
    clasificacion = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(populate_from='clasificacion', unique=True)
    descripcion = models.TextField()

    def __str__(self):
        return self.clasificacion

    class Meta:
        verbose_name = 'Clasificación de proyecto'
        verbose_name_plural = 'Clasificación de proyectos'

class OrganizacionProyecto(models.Model):
    organizacion = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(populate_from='organizacion', unique=True)
    descripcion = models.TextField()

    def __str__(self):
        return self.organizacion

    class Meta:
        verbose_name = 'Organización de proyecto'
        verbose_name_plural = 'Organizaciones de proyectos'

class ModalidadProyecto(models.Model):
    modalidad = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(populate_from='modalidad', unique=True)
    descripcion = models.TextField()

    def __str__(self):
        return self.modalidad

    class Meta:
        verbose_name = 'Organización de proyecto'
        verbose_name_plural = 'Organizaciones de proyectos'
"""


class DesarrolloTecnologico(models.Model):
    nombre_desarrollo_tecnologico = models.CharField(max_length=255, unique=True)
    tipo_desarrollo_tecnologico = models.ForeignKey(TipoDesarrollo)
    proyectos = models.ManyToManyField(Proyecto, related_name='desarrollo_tecnologico_proyectos')
    descripcion = models.TextField()
    version = models.CharField(max_length=100)
    patente = models.CharField(max_length=255, blank=True)
    licencia = models.ForeignKey(Licencia)
    url = models.URLField(blank=True)
    autores = models.ManyToManyField(User, related_name='desarrollo_tecnologico_autores')
    agradecimientos = models.ManyToManyField(User, related_name='desarrollo_tecnologico_agradecimientos')
    tags = models.ManyToManyField(Tag, related_name='desarrollo_tecnologico_tags')
    fecha = models.DateField()
    slug = AutoSlugField(populate_from=nombre_desarrollo_tecnologico, unique=True)

    def __str__(self):
        return self.nombre_desarrollo_tecnologico

    class Meta:
        ordering = ['nombre_desarrollo_tecnologico']
        get_latest_by = ['fecha', 'nombre_desarrollo_tecnologico']
        verbose_name_plural = 'Desarrollos Tecnológicos'
