from django.db import models
from django.conf import settings
from nucleo.models import User, Institucion, Dependencia, Revista, Indice, Financiamiento, \
    ProyectoInsvestigacionArbitrado, InstitucionSimple
from investigacion.models import ProyectoInvestigacion, ArticuloCientifico, LibroInvestigacion, CapituloLibroInvestigacion
from django.urls import reverse
from sortedm2m.fields import SortedManyToManyField


RED_ACADEMICA__AMBITO = getattr(settings, 'RED_ACADEMICA__AMBITO',
                                (('', '-------'), ('LOCAL', 'Local'), ('REGIONAL', 'Regional'),
                                        ('NACIONAL', 'Nacional'), ('INTERNACIONAL', 'Internacional'), ('OTRO', 'Otro')))
CONVENIO_ENTIDAD_EXTERNA__CLASIFICACION = getattr(settings, 'CONVENIO_ENTIDAD_EXTERNA__CLASIFICACION',
                                                  (('', '-------'), ('FEDERAL', 'Gubernamental federal'),
                                                   ('ESTATAL', 'Gubernamental estatal'),
                                                   ('MUNICIPAL', 'Gubernamental municipal'),
                                                   ('PRIVADA', 'Sector privado'),
                                                   ('NO_LUCRATIVA', 'Sector privado no lucrativo'),
                                                   ('EXTRANJERA', 'Extranjero')))
ARBITRAJE_ACADEMICO__TIPO = getattr(settings, 'ARBITRAJE_ACADEMICA__TIPO',
                                    (('', '-------'), ('ARTICULO', 'Artículo en revista'), ('LIBRO', 'Libro'), ('CAPITULO_LIBRO', 'Capítulo de libro')))

STATUS_PROYECTO = getattr(settings, 'STATUS_PROYECTO', (('NUEVO', 'Nuevo'), ('EN_PROCESO', 'En proceso'),
                                                        ('CONCLUIDO', 'Concluído'), ('OTRO', 'Otro')))

# Create your models here.


class ArbitrajePublicacionAcademica(models.Model):
    tipo = models.CharField(max_length=20, choices=ARBITRAJE_ACADEMICO__TIPO)
    revista = models.ForeignKey(Revista, blank=True, null=True, on_delete=models.DO_NOTHING)
    libro = models.CharField(max_length=255, blank=True, null=True)
    capitulo_libro = models.CharField(max_length=255, blank=True, null=True)
    fecha_dictamen = models.DateField()
    institucion = models.ForeignKey(InstitucionSimple, blank=True, null=True, on_delete=models.DO_NOTHING)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.fecha_dictamen

    def get_absolute_url(self):
        return reverse('arbitraje_publicacion_academica_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha_dictamen']
        verbose_name = 'Arbitraje en publicaciones académicas'
        verbose_name_plural = 'Arbitrajes en publicaciones académicas'

class ComisionVinculacion(models.Model):
    comisionvinculacion_nombre = models.CharField(max_length=140, unique=True)
    comisionvinculacion_orden = models.IntegerField()

    def __str__(self):
        return self.comisionvinculacion_nombre

    def natural_key(self):
        return self.comisionvinculacion_nombre

    class Meta:
        ordering = ['comisionvinculacion_orden', 'id']


class OtraComision(models.Model):
    comision = models.ForeignKey(ComisionVinculacion, on_delete=models.DO_NOTHING)
    comision_otra = models.CharField(max_length=255, blank=True, null=True)
    institucion = models.ForeignKey(InstitucionSimple, on_delete=models.DO_NOTHING, null=True, blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{} : {}".format(self.comision_otra, self.institucion)

    def get_absolute_url(self):
        return reverse('otra_comision_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'Otra comisión de arbitraje'
        verbose_name_plural = 'Otras comisiones de arbitraje'


class RedAcademica(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    ambito = models.CharField(max_length=20, choices=RED_ACADEMICA__AMBITO)
    objetivos = models.TextField()
    fecha_constitucion = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    instituciones = models.ManyToManyField(InstitucionSimple)
    proyecto = models.ForeignKey(ProyectoInvestigacion, blank=True, null=True, on_delete=models.DO_NOTHING)
    participantes = models.ManyToManyField(User, related_name='red_academica_participantes', verbose_name='Académicos participantes')

    def __str__(self):
        return "{} : {}".format(self.nombre, self.fecha_constitucion)

    def get_absolute_url(self):
        return reverse('red_academica_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha_constitucion']
        verbose_name = 'Red académica'
        verbose_name_plural = 'Redes académicas'


class ConvenioOtraEntidad(models.Model):
    nombre = models.CharField(max_length=254, unique=True)
    instituciones = models.ManyToManyField(InstitucionSimple)
    objetivos = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    es_renovacion = models.BooleanField(blank=True, default=False)
    financiamiento_text = models.CharField(max_length=254, blank=True, null=True)
    proyecto = models.ForeignKey(ProyectoInvestigacion, on_delete=models.DO_NOTHING, blank=True, null=True)
    ambito = models.CharField(max_length=20, choices=(('', '-------'), ('NACIONAL', 'Nacional'), ('INTERNACIONAL', 'INTERNACIONAL')))
    participantes = models.ManyToManyField(User, verbose_name='Académicos participantes')

    def __str__(self):
        return "{} : {}".format(self.nombre, self.fecha_inicio)

    def get_absolute_url(self):
        return reverse('convenio_otra_entidad_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'Convenio con otra entidad'
        verbose_name_plural = 'Convenios con otras entidades'


class ServicioAsesoriaExterna(models.Model):
    nombre_servicio = models.CharField(max_length=254)
    descripcion = models.TextField(blank=True)
    institucion = models.ForeignKey(InstitucionSimple, on_delete=models.DO_NOTHING)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    financiamiento_text = models.CharField(max_length=254)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{} : {}".format(self.nombre_servicio, self.fecha_inicio)

    def get_absolute_url(self):
        return reverse('servicio_asesoria_exterma_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'Servicio o asesoria externa'
        verbose_name_plural = 'Servicios o asesorias externas'
