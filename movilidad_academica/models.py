from django.db import models

from autoslug import AutoSlugField
from nucleo.models import User, Institucion, Dependencia, Financiamiento
from investigacion.models import ProyectoInvestigacion
from vinculacion.models import RedAcademica


# Create your models here.


class MovilidadAcademica(models.Model):
    tipo = models.CharField(max_length=30, choices=(('INVITACION', 'Invitación'), ('ESTANCIA', 'Estancia de colaboración'), ('SABATICO', 'Sabático')))
    academico = models.ForeignKey(User, related_name='movilidad_academica_academico')
    descripcion = models.TextField(blank=True)
    institucion = models.ForeignKey(Institucion)
    dependencia = models.ForeignKey(Dependencia)
    actividades = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    intercambio_unam = models.BooleanField(default=False)
    financiamiento = models.ForeignKey(Financiamiento)
    redes_academicas = models.ManyToManyField(RedAcademica, related_name='vinculacion_redes_academicas', blank=True)
    proyecto_investigacion = models.ForeignKey(ProyectoInvestigacion, blank=True, null=True)
    usuario = models.ForeignKey(User, related_name='movilidad_academica_usuario')
    #tags = models.ManyToManyField(Tag, related_name='vinculacion_tags', blank=True)

    def __str__(self):
        return "{} : {}".format(str(self.academico), str(self.dependencia))

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'Actividad de vinculación'
        verbose_name_plural = 'Actividades de vinculación'


"""
class Invitado(models.Model):
    invitado = models.ForeignKey(User)
    descripcion = models.TextField(blank=True)
    dependencia_procedencia = models.ForeignKey(Dependencia)
    actividades = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    intercambio_unam = models.BooleanField(default=False)
    financiamiento = models.ForeignKey(Financiamiento)
    redes_academicas = models.ManyToManyField(RedAcademica, related_name='invitado_redes_academicas', blank=True)
    proyecto_investigacion = models.ForeignKey(Proyecto, blank=True, null=True)
    usuario = models.ForeignKey(User)
    #tags = models.ForeignKey(Tag, related_name='invitado_tags')

    def __str__(self):
        return "{} : {}".format(str(self.invitado), str(self.dependencia_procedencia))

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'Invitado nacional'
        verbose_name_plural = 'Invitados nacionales'


class EstanciaColaboracion(models.Model):
    academico = models.ForeignKey(User)
    descripcion = models.TextField(blank=True)
    dependencia_visitada = models.ForeignKey(Dependencia)
    actividades = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    intercambio_unam = models.BooleanField(default=False)
    financiamiento = models.ForeignKey(Financiamiento)
    convocatoria_financiamiento_unam = models.CharField(max_length=255, blank=True)
    redes_academicas = models.ManyToManyField(RedAcademica, related_name='estancia_colaboracion_academicas', blank=True)
    proyectos_investigacion = models.ManyToManyField(Proyecto, related_name='estancia_colaboracion_investigacion', blank=True)
    usuario = models.ForeignKey(User)
    #tags = models.ForeignKey(Tag, related_name='estancia_tags')

    def __str__(self):
        return "{} : {}".format(str(self.academico), str(self.dependencia_visitada))

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'Estancia de colaboración'
        verbose_name_plural = 'Estancias de colaboración'
"""