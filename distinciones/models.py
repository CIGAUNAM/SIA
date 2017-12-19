from django.db import models

from django.conf import settings
from django.core.urlresolvers import reverse
from nucleo.models import User, Institucion, Distincion

GRADO_ACADEMICO = getattr(settings, 'GRADO_ACADEMICO', (('LICENCIATURA', 'Licenciatura'), ('MAESTRIA', 'Maestría'), ('DOCTORADO', 'Doctorado')))

# Create your models here.

class DistincionAcademico(models.Model):
    distincion = models.ForeignKey(Distincion)
    institucion = models.ForeignKey(Institucion)
    fecha = models.DateField()
    usuario = models.ForeignKey(User, related_name='distincion_academico_usuario')

    def __str__(self):
        return "{} : {}".format(self.distincion, self.fecha)

    def get_absolute_url(self):
        return reverse('distincion_academico_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Distinción recibida por académico'
        verbose_name_plural = 'Distinciones recibidas por académicos'



class DistincionAlumno(models.Model):
    distincion = models.ForeignKey(Distincion)
    alumno = models.ForeignKey(User, related_name='distincion_alumno_alumno')
    grado_academico = models.CharField(max_length=20, choices=GRADO_ACADEMICO)
    tutores = models.ManyToManyField(User, related_name='distincion_alumno_tutores')
    institucion = models.ForeignKey(Institucion)
    fecha = models.DateField()

    def __str__(self):
        return "{} : {}".format(self.distincion, self.fecha)

    def get_absolute_url(self):
        return reverse('distincion_alumno_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Distinción recibida por alumno'
        verbose_name_plural = 'Distinciones recibidas por alumnos'


class ParticipacionComisionExpertos(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)
    institucion = models.ForeignKey(Institucion)
    fecha = models.DateField()
    usuario = models.ForeignKey(User)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('participacion_comision_expertos_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Participación en comisión de expertos'
        verbose_name_plural = 'Participaciones en comisiones de expertos'

