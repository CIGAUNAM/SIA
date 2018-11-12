from django.db import models
from django.urls import reverse
from nucleo.models import User
from investigacion.models import ProyectoInvestigacion


# Create your models here.


class TipoDesarrollo(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('tipo_desarrollo_tecnologico_detalle', kwargs={'pk': self.pk})

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

    def natural_key(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('licencia_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['nombre']


class DesarrolloTecnologico(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    proyecto = models.ForeignKey(ProyectoInvestigacion, blank=True, null=True, on_delete=models.DO_NOTHING)
    descripcion = models.TextField()
    version = models.CharField(max_length=100, blank=True, null=True)
    patente = models.CharField(max_length=255, blank=True, null=True)
    licencia = models.ForeignKey(Licencia, on_delete=models.DO_NOTHING, blank=True, null=True)
    url = models.URLField(blank=True)
    autores = models.ManyToManyField(User, related_name='desarrollo_tecnologico_autores')
    fecha = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('desarrollo_tecnologico_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['nombre']
        get_latest_by = ['fecha', 'nombre']
        verbose_name_plural = 'Desarrollos Tecnológicos'