from django.db import models
from django.conf import settings
from nucleo.models import User, Institucion, Dependencia, Indice, Libro, Financiamiento, ProyectoInsvestigacionArbitrado
from investigacion.models import ProyectoInvestigacion, ArticuloCientifico
from django.urls import reverse
from sortedm2m.fields import SortedManyToManyField


RED_ACADEMICA__CLASIFICACION = getattr(settings, 'RED_ACADEMICA__CLASIFICACION',
                                       (('', '-------'), ('LOCAL', 'Local'), ('REGIONAL', 'Regional'),
                                        ('NACIONAL', 'Nacional'), ('INTERNACIONAL', 'Internacional'), ('OTRO', 'Otro')))
CONVENIO_ENTIDAD_EXTERNA__CLASIFICACION = getattr(settings, 'CONVENIO_ENTIDAD_EXTERNA__CLASIFICACION',
                                                  (('', '-------'), ('FEDERAL', 'Gubernamental federal'),
                                                   ('ESTATAL', 'Gubernamental estatal'),
                                                   ('MUNICIPAL', 'Gubernamental municipal'),
                                                   ('PRIVADA', 'Sector privado'),
                                                   ('NO_LUCRATIVA', 'Sector privado no lucrativo'),
                                                   ('EXTRANJERA', 'Extranjero')))
ARBITRAJE_ACADEMICA__TIPO = getattr(settings, 'ARBITRAJE_ACADEMICA__TIPO',
                                    (('', '-------'), ('ARTICULO', 'Artículo en revista'), ('LIBRO', 'Libro')))

STATUS_PROYECTO = getattr(settings, 'STATUS_PROYECTO', (('NUEVO', 'Nuevo'), ('EN_PROCESO', 'En proceso'),
                                                        ('CONCLUIDO', 'Concluído'), ('OTRO', 'Otro')))

# Create your models here.


class ArbitrajePublicacionAcademica(models.Model):
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=20, choices=ARBITRAJE_ACADEMICA__TIPO)
    articulo = models.ForeignKey(ArticuloCientifico, blank=True, null=True, on_delete=models.DO_NOTHING)
    libro = models.ForeignKey(Libro, blank=True, null=True, on_delete=models.DO_NOTHING)
    fecha_dictamen = models.DateField()
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        lista_titulos = [self.articulo, self.libro]
        titulo = [x for x in lista_titulos if x != 'n/a']
        titulo = titulo[0]
        return "{} : {}".format(self.tipo.title(), titulo, self.fecha_dictamen)

    def get_absolute_url(self):
        return reverse('arbitraje_publicacion_academica_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha_dictamen']
        verbose_name = 'Arbitraje en publicaciones académicas'
        verbose_name_plural = 'Arbitrajes en publicaciones académicas'


class ArbitrajeProyectoInvestigacion(models.Model):
    fecha = models.DateField()
    descripcion = models.TextField(blank=True)
    proyecto = models.ForeignKey(ProyectoInsvestigacionArbitrado, on_delete=models.DO_NOTHING)
    convocatoria = models.CharField(max_length=200)
    institucion = models.ForeignKey(Institucion, on_delete=models.DO_NOTHING)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.DO_NOTHING)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{} : {}".format(str(self.proyecto), self.fecha)

    def get_absolute_url(self):
        return reverse('arbitraje_proyecto_investigacion_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Arbitraje de proyectos de investigación'
        verbose_name_plural = 'Arbitrajes de proyectos de investigación'


class ArbitrajeOtraActividad(models.Model):
    actividad = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    institucion = models.ForeignKey(Institucion, on_delete=models.DO_NOTHING)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.DO_NOTHING)
    fecha = models.DateField()
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{} : {}".format(self.actividad, self.dependencia)

    def get_absolute_url(self):
        return reverse('arbitraje_otra_actividad_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Arbitraje en otras actividades'
        verbose_name_plural = 'Arbitraje en otras actividades'


class RedAcademica(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)
    ambito = models.CharField(max_length=20, choices=RED_ACADEMICA__CLASIFICACION)
    objetivos = models.TextField()
    fecha_constitucion = models.DateField()
    vigente = models.BooleanField(default=False)
    entidades = models.ManyToManyField(Dependencia, related_name='red_academica_entidades')
    proyecto = models.ForeignKey(ProyectoInvestigacion, blank=True, null=True, on_delete=models.DO_NOTHING)
    participantes = models.ManyToManyField(User, related_name='red_academica_usuarios',
                                      verbose_name='Académicos participantes')

    def __str__(self):
        return "{} : {}".format(self.nombre, self.fecha_constitucion)

    def get_absolute_url(self):
        return reverse('red_academica_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha_constitucion']
        verbose_name = 'Red académica'
        verbose_name_plural = 'Redes académicas'


class ConvenioEntidadExterna(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)
    entidades = models.ManyToManyField(Dependencia)
    objetivos = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    es_renovacion = models.BooleanField(blank=True, default=False)
    financiamientos = models.ManyToManyField(Financiamiento, blank=True)
    participantes = models.ManyToManyField(User, related_name='convenio_entidad_no_academica_usuarios',
                                           verbose_name='Académicos participantes')

    def __str__(self):
        return "{} : {}".format(self.nombre, self.fecha_inicio)

    def get_absolute_url(self):
        return reverse('convenio_entidad_no_academica_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'Convenio con entidade externa'
        verbose_name_plural = 'Convenios con entidades externas'


class ClasificacionServicio(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('clasificacion_servicio_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Clasificación de servicio'
        verbose_name_plural = 'Clasificaciones de servicios'


class ServicioExternoEntidadNoAcademica(models.Model):
    nombre_servicio = models.CharField(max_length=255)
    clasificacion_servicio = models.ForeignKey(ClasificacionServicio, on_delete=models.DO_NOTHING)
    descripcion = models.TextField(blank=True)
    entidades = models.ManyToManyField(Dependencia)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    financiamientos = models.ManyToManyField(Financiamiento, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{} : {}".format(self.nombre_servicio, self.fecha_inicio)

    def get_absolute_url(self):
        return reverse('servicio_externo_entidad_no_academica_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'Servicio o asesoria externa a entidades no académicas'
        verbose_name_plural = 'Servicios o asesorias externas a entidades no académicas'


class OtroProgramaVinculacion(models.Model):
    nombre = models.CharField(max_length=255)
    fecha = models.DateField()
    tipo = models.CharField(max_length=20, choices=(('VINCULACION', 'Vinculación'), ('COLABORACION', 'Colaboración'),
                                                    ('COOPERACION', 'Cooperación'), ('OTRO', 'Otro')))
    descripcion = models.TextField()
    resultados = models.TextField(blank=True)
    institucion = models.ForeignKey(Institucion, on_delete=models.DO_NOTHING)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.DO_NOTHING)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{} : {}".format(self.nombre, self.fecha)

    def get_absolute_url(self):
        return reverse('otro_programa_vinculacion_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha', 'nombre']
        verbose_name = 'Otro programa o acción de vinculación, colaboración y/o cooperación'
        verbose_name_plural = 'Otros programas o acciones de vinculación, colaboración y/o cooperación'


