from django.db import models

#from django.contrib.auth.models import User
from autoslug import AutoSlugField
from nucleo.models import User, Tag, Dependencia, Proyecto
from vinculacion.models import RedAcademica
from formacion_academica.models import Licenciatura, Maestria, Doctorado

# Create your models here.

class Asignatura(models.Model):
    asignatura = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(populate_from='asignatura', unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.asignatura


class CursoDocencia(models.Model):
    nivel = models.CharField(max_length=30, choices=(('LICENCIATURA', 'Licenciatura'), ('MAESTRIA', 'Maestría'), ('DOCTORADO', 'Doctorado')))
    tipo = models.CharField(max_length=20, choices=(('ESCOLARIZADO', 'Escolarizado'), ('EXTRACURRICULAR', 'Extracurricular')))
    licenciatura = models.ForeignKey(Licenciatura)
    maestria = models.ForeignKey(Maestria)
    doctorado = models.ForeignKey(Doctorado)
    asignatura = models.ForeignKey(Asignatura)
    tipo = models.CharField(max_length=30, choices=(('PRESENCIAL', 'Presencial'), ('EN_LINEA', 'En línea')))
    nivel_participacion = models.CharField(max_length=30, choices=(('TITULAR', 'Titular / Responsable'), ('COLABORADOR', 'Colaborador / Invitado')))
    dependencia = models.ForeignKey(Dependencia)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    total_horas = models.PositiveIntegerField()
    usuario = models.ForeignKey(User, related_name='curso_escolarizado_docente')
    otros_academicos = models.ManyToManyField(User, related_name='curso_escolarizado_otros_academicos', blank=True)
    otras_dependencias_participantes = models.ManyToManyField(User, related_name='curso_escolarizado_otras_dependencias_participantes', blank=True)

    def __str__(self):
        return "{} : {} : {}".format(self.asignatura, str(self.dependencia.dependencia), self.fecha_inicio)

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'

