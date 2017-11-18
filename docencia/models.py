from django.db import models

from django.conf import settings

from autoslug import AutoSlugField
from nucleo.models import User, Institucion, Dependencia, ProgramaLicenciatura, ProgramaMaestria, ProgramaDoctorado, \
    Asignatura, Revista, Indice
from investigacion.models import ProyectoInvestigacion
from vinculacion.models import RedAcademica
from django.core.urlresolvers import reverse
from sortedm2m.fields import SortedManyToManyField


STATUS_PUBLICACION = getattr(settings, 'STATUS_PUBLICACION', (('PUBLICADO', 'Publicado'), ('EN_PRENSA', 'En prensa'), ('ACEPTADO', 'Aceptado'), ('ENVIADO', 'Enviado'), ('OTRO', 'Otro')))


# Create your models here.

class CursoDocencia(models.Model):
    nivel = models.CharField(max_length=30, choices=(('OTRO', 'Otro'), ('LICENCIATURA', 'Licenciatura'), ('MAESTRIA', 'Maestría'), ('DOCTORADO', 'Doctorado')))
    tipo = models.CharField(max_length=20, choices=(('ESCOLARIZADO', 'Escolarizado'), ('EXTRACURRICULAR', 'Extracurricular')))
    licenciatura = models.ForeignKey(ProgramaLicenciatura, blank=True, null=True)
    maestria = models.ForeignKey(ProgramaMaestria, blank=True, null=True)
    doctorado = models.ForeignKey(ProgramaDoctorado, blank=True, null=True)
    asignatura = models.ForeignKey(Asignatura)
    modalidad = models.CharField(max_length=30, choices=(('PRESENCIAL', 'Presencial'), ('EN_LINEA', 'En línea')))
    institucion = models.ForeignKey(Institucion)
    dependencia = models.ForeignKey(Dependencia)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    total_horas = models.PositiveIntegerField()
    usuario = models.ForeignKey(User, related_name='cursodocencia_usuario')
    academicos_participantes = models.ManyToManyField(User, related_name='cursodocencia_academicos_participantes', blank=True, verbose_name='Académicos participantes')
    otras_dependencias_participantes = models.ManyToManyField(Dependencia, related_name='curso_escolarizado_otras_dependencias_participantes', blank=True)

    def __str__(self):
        return "{} : {} : {}".format(self.asignatura, str(self.dependencia.nombre), self.fecha_inicio)

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'


class ArticuloDocencia(models.Model):
    titulo = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)
    revista = models.ForeignKey(Revista)
    volumen = models.CharField(max_length=100, null=True, blank=True)
    numero = models.CharField(max_length=100, null=True, blank=True)
    fecha = models.DateField(auto_now=False)
    issn_impreso = models.CharField(max_length=40, blank=True, verbose_name='ISSN Impreso')
    issn_online = models.CharField(max_length=40, blank=True, verbose_name='ISSN Online')
    status = models.CharField(max_length=20, choices=STATUS_PUBLICACION)
    solo_electronico = models.BooleanField(default=False)
    usuarios = SortedManyToManyField(User, related_name='articulo_docencia_autores', verbose_name='Autores')
    alumnos = models.ManyToManyField(User, related_name='articulo_docencia_alumnos', blank=True)
    indices = models.ManyToManyField(Indice, related_name='articulo_docencia_indices', blank=True)
    url = models.URLField(blank=True)
    pagina_inicio = models.PositiveIntegerField()
    pagina_fin = models.PositiveIntegerField()
    id_doi = models.CharField(max_length=100, null=True, blank=True)
    proyecto = models.ForeignKey(ProyectoInvestigacion, blank=True, null=True)

    def __str__(self):
        return "{} : {} : {}".format(self.titulo, self.tipo.title(), self.revista)

    def get_absolute_url(self):
        return reverse('articulo_docencia_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Artículo para docencia"
        verbose_name_plural = "Artículos para docencia"
        ordering = ['-fecha', 'titulo']


class ProgramaEstudio(models.Model):
    nombre = models.CharField(max_length=254, unique=True)
    descripcion = models.TextField(blank=True)
    nivel = models.CharField(max_length=20, choices=(('', '-------'),
                                                     ('LICENCIATURA', 'Licenciatura'),
                                                     ('MAESTRIA', 'Maestría'), ('DOCTORADO', 'Doctorado'),
                                                     ('OTRO', 'Otro')))
    fecha = models.DateField(auto_now=False)
    usuario = models.ForeignKey(User)


    def __str__(self):
        return "{} : {}".format(self.nombre, self.nivel.title())

    def get_absolute_url(self):
        return reverse('programa_estudio_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Programa de estudio"
        verbose_name_plural = "Programas de estudio"
        ordering = ['-fecha', 'nombre']
