from django.db import models

from django.conf import settings
from django.core.urlresolvers import reverse
from nucleo.models import User, Dependencia, Distincion

DISTINCION__AMBITO = getattr(settings, 'EVENTO__AMBITO', (('INSTITUCIONAL', 'Institucional'), ('REGIONAL', 'Regional'), ('NACIONAL', 'Nacional'), ('INTERNACIONAL', 'Internacional'), ('OTRO', 'Otro')))
GRADO_ACADEMICO = getattr(settings, 'GRADO_ACADEMICO', (('LICENCIATURA', 'Licenciatura'), ('MAESTRIA', 'Maestría'), ('DOCTORADO', 'Doctorado')))

# Create your models here.

class DistincionAcademico(models.Model):
    distincion = models.ForeignKey(Distincion)
    condecorados = models.ManyToManyField(User, related_name='distincion_academico_condecorados')
    otorga = models.ForeignKey(Dependencia)
    ambito = models.CharField(max_length=20, choices=DISTINCION__AMBITO)
    fecha = models.DateField()

    def __str__(self):
        return "{} : {}".format(self.distincion, self.fecha)

    def get_absolute_url(self):
        return reverse('distincion_academico_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Distinción recibida'
        verbose_name_plural = 'Distinciones recibidas'



class DistincionAlumno(models.Model):
    distincion = models.ForeignKey(Distincion)
    alumno = models.ForeignKey(User, related_name='distincion_alumno_alumno')
    grado_academico = models.CharField(max_length=20, choices=GRADO_ACADEMICO)
    tutores = models.ManyToManyField(User, related_name='distincion_alumno_tutores')
    otorga = models.ForeignKey(Dependencia)
    ambito = models.CharField(max_length=20, choices=DISTINCION__AMBITO)
    fecha = models.DateField()

    def __str__(self):
        return "{} : {}".format(self.distincion, self.fecha)

    def get_absolute_url(self):
        return reverse('distincion_alumno_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Distinción recibida'
        verbose_name_plural = 'Distinciones recibidas'