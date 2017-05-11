from django.db import models
from autoslug import AutoSlugField
from nucleo.models import User, Pais, Estado, Ciudad, Institucion, Dependencia, Departamento, Cargo
from django.core.urlresolvers import reverse

# Create your models here.

class Comision(models.Model):
    comision = models.CharField(max_length=255, unique=True)
    #slug = AutoSlugField(populate_from='comision', unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.comision

    def natural_key(self):
        return (self.comision)

    class Meta:
        verbose_name_plural = 'Comisiones'


class Actividad(models.Model):
    actividad = models.CharField(max_length=255, unique=True)
    #slug = AutoSlugField(populate_from='actividad', unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.actividad

    def natural_key(self):
        return (self.actividad)

    class Meta:
        verbose_name_plural = 'Actividades'


class Representacion(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    #slug = AutoSlugField(populate_from='nombre', unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return (self.nombre)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Representación'
        verbose_name_plural = 'Representaciones'

"""
class OrganoColegiado(models.Model):
    organo_colegiado = models.CharField(max_length=255, unique=True)
    #slug = AutoSlugField(populate_from='organo_colegiado', unique=True)

    def __str__(self):
        return self.organo_colegiado
    class Meta:
        verbose_name_plural = 'Organos Colegiados'
"""

class CargoAcademicoAdministrativo(models.Model):
    nombre = models.ForeignKey(Cargo)
    descripcion = models.TextField(blank=True)
    dependencia = models.ForeignKey(Dependencia)
    cargo_inicio = models.DateField(auto_now=False)
    cargo_fin = models.DateField(auto_now=False)
    ##slug = AutoSlugField(populate_from='nombre', unique=True)
    usuario = models.ForeignKey(User)
    #tags = models.ManyToManyField(Tag, related_name='cargo_academico_administrativo_tags', blank=True)

    def __str__(self):
        return "[ {} : {} ] : {} : {} : {} : {}".format(self.user, self.nombre, self.dependencia.nombre, self.dependencia.institucion, self.cargo_inicio, self.cargo_fin)

    def get_absolute_url(self):
        return reverse('cargo_academico_administrativo_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name_plural = 'Cargos Académico-Administrativos'
        unique_together = ('nombre', 'usuario', 'dependencia', 'cargo_inicio')
        ordering = ['-cargo_inicio']
        get_latest_by = ['user', 'nombre']


class RepresentacionOrganoColegiado(models.Model):
    representacion = models.ForeignKey(Representacion)
    ante = models.ForeignKey(Dependencia)
    descripcion = models.TextField(blank=True)
    cargo_inicio = models.DateField(auto_now=False)
    cargo_fin = models.DateField(auto_now=False)
    usuario = models.ForeignKey(User)
    #tags = models.ManyToManyField(Tag, related_name='representante_ante_organo_colegiado_tags', blank=True)

    def __str__(self):
        return "{} : {} : {} - {}".format(self.representacion, self.ante, self.cargo_inicio, self.cargo_fin)

    def get_absolute_url(self):
        return reverse('representacion_organo_colegiado_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name_plural = 'Representantes Ante Organos Colegiados'
        unique_together = ('usuario', 'representacion', 'cargo_inicio')
        ordering = ['-cargo_inicio']


class ComisionAcademica(models.Model):
    nombre = models.ForeignKey(Comision)
    #slug = AutoSlugField(populate_from='nombre', unique=True, max_length=255)
    descripcion = models.TextField(blank=True)
    es_evaluacion = models.BooleanField(default=False)
    dependencias = models.ManyToManyField(Dependencia)
    #ubicacion = models.ForeignKey(Ubicacion)
    fecha_inicio = models.DateField(auto_now=False)
    fecha_fin = models.DateField(auto_now=False)
    usuario = models.ForeignKey(User)
    #tags = models.ManyToManyField(Tag, related_name='comision_academica_tags', blank=True)

    def __str__(self):
        return "[{}] : {} : {} : {}".format(self.user, self.nombre, self.fecha_inicio, self.fecha_fin)

    def get_absolute_url(self):
        return reverse('comision_academica_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name_plural = 'Comisiones Académicas'
        unique_together = ('nombre', 'usuario', 'fecha_inicio')
        ordering = ['fecha_inicio']
        get_latest_by = ['user', 'nombre']



class ApoyoTecnico(models.Model):
    nombre = models.ForeignKey(Actividad)
    descripcion = models.TextField()
    dependencia = models.ForeignKey(Dependencia)
    #ubicacion = models.ForeignKey(Ubicacion)
    apoyo_inicio = models.DateField(auto_now=False)
    apoyo_fin = models.DateField(auto_now=False)
    ##slug = AutoSlugField(populate_from='nombre', unique=True)
    usuario = models.ForeignKey(User)
    #tags = models.ManyToManyField(Tag, related_name='apoyo_tecnico_tags', blank=True)

    def __str__(self):
        return "[{}] : {} : {} : {}".format(self.user, self.nombre, self.apoyo_inicio, self.apoyo_fin)

    def get_absolute_url(self):
        return reverse('apoyo_tecnico_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name_plural = 'Apoyos de Técnicos'
        unique_together = ('nombre', 'usuario', 'dependencia', 'apoyo_inicio')
        ordering = ['-apoyo_inicio']
        get_latest_by = ['user', 'nombre']


class ApoyoOtraActividad(models.Model):
    nombre = models.ForeignKey(Actividad)
    descripcion = models.TextField()
    dependencia = models.ForeignKey(Dependencia)
    #ubicacion = models.ForeignKey(Ubicacion)
    apoyo_inicio = models.DateField(auto_now=False)
    apoyo_fin = models.DateField(auto_now=False)
    ##slug = AutoSlugField(populate_from='apoyo_otra_actividad_tags', unique=True)
    usuario = models.ForeignKey(User)
    #tags = models.ManyToManyField(Tag, related_name='apoyo_otra_actividad_tags', blank=True)

    def __str__(self):
        return "[{}] : {} : {} : {}".format(self.user, self.nombre, self.apoyo_inicio, self.apoyo_fin)

    def get_absolute_url(self):
        return reverse('apoyo_otra_actividad_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name_plural = 'Apoyos en Otras Actividades'
        unique_together = ('nombre', 'usuario', 'dependencia', 'apoyo_inicio')
        ordering = ['-apoyo_inicio']
        get_latest_by = ['user', 'nombre']
