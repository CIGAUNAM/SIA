from django.db import models

from django.conf import settings
from django.core.urlresolvers import reverse
from nucleo.models import User, Dependencia, Distincion

DISTINCION__AMBITO = getattr(settings, 'EVENTO__AMBITO', (('INSTITUCIONAL', 'Institucional'), ('REGIONAL', 'Regional'), ('NACIONAL', 'Nacional'), ('INTERNACIONAL', 'Internacional'), ('OTRO', 'Otro')))
GRADO_ACADEMICO = getattr(settings, 'GRADO_ACADEMICO', (('LICENCIATURA', 'Licenciatura'), ('MAESTRIA', 'Maestría'), ('DOCTORADO', 'Doctorado')))

# Create your models here.

class DistincionAcademico(models.Model):
    tipo = models.CharField(max_length=20, choices=(('ESCOLARIZADO', 'Escolarizado'), ('EXTRACURRICULAR', 'Extracurricular')))
    fecha = models.DateField()
    distincion = models.ForeignKey(Distincion)
    descripcion = models.TextField(blank=True)
    condecorados = models.ManyToManyField(User, related_name='distincion_academico_condecorados')
    otorga = models.ForeignKey(Dependencia)
    ambito = models.CharField(max_length=20, choices=DISTINCION__AMBITO)

    def __str__(self):
        return "{} : {}".format(self.distincion, self.fecha)

    def get_absolute_url(self):
        return reverse('distincion_academico_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Distinción recibida'
        verbose_name_plural = 'Distinciones recibidas'



class DistincionAlumno(models.Model):
    tipo = models.CharField(max_length=20, choices=(('ESCOLARIZADO', 'Escolarizado'), ('EXTRACURRICULAR', 'Extracurricular')))
    fecha = models.DateField()
    alumno = models.ForeignKey(User, related_name='distincion_alumno_alumno')
    grado_academico = models.CharField(max_length=20, choices=GRADO_ACADEMICO)
    distincion = models.ForeignKey(Distincion)
    descripcion = models.TextField(blank=True)
    tutores = models.ManyToManyField(User, related_name='distincion_alumno_tutores')
    otorga = models.ForeignKey(Dependencia)
    ambito = models.CharField(max_length=20, choices=DISTINCION__AMBITO)

    def __str__(self):
        return "{} : {}".format(self.distincion, self.fecha)

    def get_absolute_url(self):
        return reverse('distincion_alumno_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Distinción recibida'
        verbose_name_plural = 'Distinciones recibidas'