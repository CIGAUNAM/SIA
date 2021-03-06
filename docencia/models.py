from django.db import models
from django.conf import settings
from nucleo.models import User, Institucion, Dependencia, ProgramaLicenciatura, ProgramaMaestria, ProgramaDoctorado, \
    Asignatura, Revista, Indice, TipoCurso
from investigacion.models import ProyectoInvestigacion
from django.urls import reverse
from sortedm2m.fields import SortedManyToManyField


STATUS_PUBLICACION_ARTICULO = getattr(settings, 'STATUS_PUBLICACION_ARTICULO',
                                      (('PUBLICADO', 'Publicado'), ('ACEPTADO', 'Aceptado'), ('ENVIADO', 'Enviado'),
                                       ('OTRO', 'Otro')))


# Create your models here.


class CursoDocenciaEscolarizado(models.Model):
    nivel = models.CharField(max_length=30, choices=(('', '------'), ('LICENCIATURA', 'Licenciatura'),
                                                     ('MAESTRIA', 'Maestría'), ('DOCTORADO', 'Doctorado')))
    licenciatura = models.ForeignKey(ProgramaLicenciatura, blank=True, null=True, on_delete=models.DO_NOTHING)
    maestria = models.ForeignKey(ProgramaMaestria, blank=True, null=True, on_delete=models.DO_NOTHING)
    doctorado = models.ForeignKey(ProgramaDoctorado, blank=True, null=True, on_delete=models.DO_NOTHING)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.DO_NOTHING)
    modalidad = models.CharField(max_length=30, choices=(('', 'Seleccionar modalidad de curso'),
                                                         ('PRESENCIAL', 'Presencial'), ('EN_LINEA', 'En línea'),
                                                         ('MIXTO', 'Mixto'), ('OTRO', 'Otro')))
    nombramiento = models.CharField(max_length=30, choices=(('', '-------'), ('TITULAR', 'Titular o Coordinador'),
                                                            ('COLABORADOR', 'Colaborador o Invitado')))
    institucion = models.ForeignKey(Institucion, on_delete=models.DO_NOTHING)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.DO_NOTHING)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    total_horas = models.PositiveIntegerField()
    periodo_academico = models.CharField(max_length=20)
    usuario = models.ForeignKey(User, related_name='curso_docencia_escolarizado_usuario', on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{} : {} : {}".format(self.asignatura, str(self.dependencia.nombre), self.fecha_inicio)

    def get_absolute_url(self):
        return reverse('curso_docencia_escolarizado_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'Curso Escolarizado'
        verbose_name_plural = 'Cursos Escolarizados'


class CursoDocenciaExtracurricular(models.Model):
    asignatura = models.ForeignKey(Asignatura, on_delete=models.DO_NOTHING)
    tipo = models.ForeignKey(TipoCurso, on_delete=models.DO_NOTHING)
    modalidad = models.CharField(max_length=30, choices=(('', 'Seleccionar modalidad de curso'),
                                                         ('PRESENCIAL', 'Presencial'), ('EN_LINEA', 'En línea'),
                                                         ('MIXTO', 'Mixto')))
    institucion = models.ForeignKey(Institucion, on_delete=models.DO_NOTHING)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.DO_NOTHING)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    total_horas = models.PositiveIntegerField()
    periodo_academico = models.CharField(max_length=20)
    usuario = models.ForeignKey(User, related_name='curso_docencia_extracurricular_usuario',
                                on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{} : {} : {}".format(self.asignatura, str(self.dependencia.nombre), self.fecha_inicio)

    def get_absolute_url(self):
        return reverse('curso_docencia_extracurricular_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'Curso Extracurricular'
        verbose_name_plural = 'Cursos Extracurriculares'


class ArticuloDocencia(models.Model):
    titulo = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)
    revista = models.ForeignKey(Revista, on_delete=models.DO_NOTHING)
    volumen = models.CharField(max_length=100, null=True, blank=True)
    numero = models.CharField(max_length=100, null=True, blank=True)
    fecha = models.DateField(auto_now=False)
    status = models.CharField(max_length=20, choices=STATUS_PUBLICACION_ARTICULO)
    solo_electronico = models.BooleanField(default=False)
    autores = SortedManyToManyField(User, related_name='articulo_docencia_autores', verbose_name='Autores')
    alumnos = models.ManyToManyField(User, related_name='articulo_docencia_alumnos', blank=True)
    agradecimientos = models.ManyToManyField(User, related_name='articulo_docencia_agradecimientos', blank=True)
    url = models.URLField(blank=True)
    pagina_inicio = models.PositiveIntegerField()
    pagina_fin = models.PositiveIntegerField()

    def __str__(self):
        return "{} : {}".format(self.titulo, self.revista)

    def get_absolute_url(self):
        return reverse('articulo_docencia_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Artículo para docencia"
        verbose_name_plural = "Artículos para docencia"
        ordering = ['-fecha', 'titulo']


class ProgramaEstudio(models.Model):
    nombre = models.CharField(max_length=254)
    descripcion = models.TextField(blank=True)
    nivel = models.CharField(max_length=20, choices=(('', '-------'),
                                                     ('LICENCIATURA', 'Licenciatura'),
                                                     ('MAESTRIA', 'Maestría'), ('DOCTORADO', 'Doctorado'),
                                                     ('OTRO', 'Otro')))
    fecha = models.DateField(auto_now=False)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    institucion = models.ForeignKey(Institucion, on_delete=models.DO_NOTHING)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{} : {}".format(self.nombre, self.nivel.title())

    def get_absolute_url(self):
        return reverse('programa_estudio_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Programa de estudio"
        verbose_name_plural = "Programas de estudio"
        ordering = ['-fecha', 'nombre']
