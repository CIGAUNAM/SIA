from django.db import models

#from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from nucleo.models import User, Dependencia, ImpactoSocial, Proyecto, Indice

# Create your models here.

class TipoDesarrollo(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Tipo de desarrollo'
        verbose_name_plural = 'Tipos de desarrollo'


class Licencia(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField()
    url = models.URLField()

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']


class DesarrolloTecnologico(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    #tipo_desarrollo_tecnologico = models.ForeignKey(TipoDesarrollo)
    proyectos = models.ManyToManyField(Proyecto, related_name='desarrollo_tecnologico_proyectos')
    descripcion = models.TextField()
    version = models.CharField(max_length=100)
    patente = models.CharField(max_length=255, blank=True)
    licencia = models.ForeignKey(Licencia)
    url = models.URLField(blank=True)
    autores = models.ManyToManyField(User, related_name='desarrollo_tecnologico_autores')
    agradecimientos = models.ManyToManyField(User, related_name='desarrollo_tecnologico_agradecimientos', blank=True)
    fecha = models.DateField()

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('comite_tutoral_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['nombre']
        get_latest_by = ['fecha', 'nombre']
        verbose_name_plural = 'Desarrollos Tecnológicos'
