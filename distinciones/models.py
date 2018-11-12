from django.db import models
from django.urls import reverse
from nucleo.models import User, Institucion, Dependencia, Distincion, Libro
from investigacion.models import ArticuloCientifico, CapituloLibroInvestigacion

NIVEL_ACADEMICO = (('', '-------'), ('LICENCIATURA', 'Licenciatura'), ('MAESTRIA', 'Maestría'), ('DOCTORADO', 'Doctorado'))


# Create your models here.


class DistincionAcademico(models.Model):
    distincion = models.ForeignKey(Distincion, on_delete=models.DO_NOTHING)
    fecha = models.DateField()
    usuario = models.ForeignKey(User, related_name='distincion_academico_usuario', on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{} : {}".format(self.distincion, self.fecha)

    def get_absolute_url(self):
        return reverse('distincion_academico_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Distinción recibida por académico'
        verbose_name_plural = 'Distinciones recibidas por académicos'


class DistincionAlumno(models.Model):
    distincion = models.ForeignKey(Distincion, on_delete=models.DO_NOTHING)
    alumno = models.ForeignKey(User, related_name='distincion_alumno_alumno', on_delete=models.DO_NOTHING)
    nivel_academico = models.CharField(max_length=20, choices=NIVEL_ACADEMICO)
    tutores = models.ManyToManyField(User, related_name='distincion_alumno_tutores')
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
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    institucion = models.ForeignKey(Institucion, on_delete=models.DO_NOTHING)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.DO_NOTHING)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('comision_expertos_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'Participación en comisión de expertos'
        verbose_name_plural = 'Participaciones en comisiones de expertos'


class ParticipacionSociedadCientifica(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=20, choices=(('', '-------'), ('INVITACION', 'Por invitación'),
                                                    ('ELECCION', 'Por elección')))
    ambito = models.CharField(max_length=20, choices=(('', '-------'), ('NACIONAL', 'Nacional'),
                                                    ('INTERNACIONAL', 'Internacional')))

    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('sociedad_cientifica_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'Participación en sociedad científica'
        verbose_name_plural = 'Participaciones en sociedades científicas'


class CitaPublicacion(models.Model):
    tipo_trabajo_citado = models.CharField(max_length=20, choices=(('', '-------'), ('ARTICULO', 'Artículo'),
                                                                   ('LIBRO', 'Libro'),
                                                                   ('CAPITULO_LIBRO', 'Capítulo de libro')))
    articulo_citado = models.ForeignKey(ArticuloCientifico, blank=True, null=True,
                                        related_name='cita_publicacion_articulo_citado', on_delete=models.DO_NOTHING)
    libro_citado = models.ForeignKey(Libro, blank=True, null=True, related_name='cita_publicacion_libro_citado',
                                     on_delete=models.DO_NOTHING)
    capitulo_libro_citado = models.ForeignKey(CapituloLibroInvestigacion, blank=True, null=True,
                                              on_delete=models.DO_NOTHING)
    citado_en_articulos = models.ManyToManyField(ArticuloCientifico, blank=True,
                                                 related_name='cita_publicacion_citado_en_articulos')
    citado_en_libros = models.ManyToManyField(Libro, blank=True, related_name='cita_publicacion_citado_en_libros')
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
