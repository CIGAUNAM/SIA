from django.db import models

from django.conf import settings
from django.core.urlresolvers import reverse
from nucleo.models import User, Institucion, Distincion
from investigacion.models import ArticuloCientifico, Libro, CapituloLibroInvestigacion

GRADO_ACADEMICO = getattr(settings, 'GRADO_ACADEMICO', (('', '-------'), ('LICENCIATURA', 'Licenciatura'), ('MAESTRIA', 'Maestría'), ('DOCTORADO', 'Doctorado')))

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
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    usuario = models.ForeignKey(User)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('comision_expertos_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Participación en comisión de expertos'
        verbose_name_plural = 'Participaciones en comisiones de expertos'


class ParticipacionSociedadCientifica(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=20, choices=(('', '-------'), ('INVITACION', 'Por invitación'), ('ELECCION', 'Por elección')))
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    usuario = models.ForeignKey(User)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('sociedad_cientifica_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Participación en sociedad científica'
        verbose_name_plural = 'Participaciones en sociedades científicas'


class CitaPublicacion(models.Model):
    tipo_trabajo_citado = models.CharField(max_length=20, choices=(('', '-------'), ('ARTICULO', 'Artículo'), ('LIBRO', 'Libro'), ('CAPITULO_LIBRO', 'Capítulo de libro')))
    articulo_citado = models.ForeignKey(ArticuloCientifico, blank=True, null=True)
    libro_citado = models.ForeignKey(Libro, blank=True, null=True)
    capitulo_libro_citado = models.ForeignKey(CapituloLibroInvestigacion, blank=True, null=True)
    citado_en_articulos = models.ManyToManyField(ArticuloCientifico, blank=True)
    citado_en_libros = models.ManyToManyField(Libro, blank=True)
    citado_en_capitulos_libros = models.ManyToManyField(CapituloLibroInvestigacion, blank=True)
    citado_en_tesis = models.TextField(blank=True)
    citado_en_otras_publicaciones = models.TextField(blank=True)
    usuarios = models.ManyToManyField(User, related_name='cita_publicacion_autores', verbose_name='Autores')

    def __str__(self):
        return self.pk

    def get_absolute_url(self):
        return reverse('cita_publicacion_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Cita de publicación'
        verbose_name_plural = 'Citas de publicaciones'



