from django.db import models

from nucleo.models import User, Tag, Cargo, Nombramiento, Dependencia
# Create your models here.


class ExperienciaLaboral(models.Model):
    dependencia = models.ForeignKey(Dependencia)
    nombramiento = models.ForeignKey(Nombramiento, blank=True, null=True)
    es_nombramiento_definitivo = models.BooleanField(default=False)
    cargo = models.ForeignKey(Cargo)
    descripcion = models.TextField(blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    usuario = models.ForeignKey(User)
    tags = models.ManyToManyField(Tag, related_name='experiencia_laboral_tags', blank=True)

    def __str__(self):
        return "{} : {} : {}".format(self.usuario, self.dependencia, self.cargo)

    class Meta:
        ordering = ['fecha_inicio', 'dependencia']
        verbose_name = "Experiencia Laboral"
        verbose_name_plural = "Experiencias Laborales"


class LineaInvestigacion(models.Model):
    linea_investigacion = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    dependencia = models.ForeignKey(Dependencia)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    usuario = models.ForeignKey(User)
    tags = models.ManyToManyField(Tag, related_name='linea_investigacion_tags', blank=True)

    def __str__(self):
        return "{} : {}".format(self.usuario, self.linea_investigacion)

    class Meta:
        ordering = ['fecha_inicio', 'linea_investigacion']
        verbose_name = "Línea de investigación"
        verbose_name_plural = "Líneas de investigación"


class CapacidadPotencialidad(models.Model):
    competencia = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    usuario = models.ForeignKey(User)
    tags = models.ManyToManyField(Tag, related_name='capacidad_potencialidad_tags', blank=True)

    def __str__(self):
        return "{} : {}".format(self.usuario, self.competencia)

    class Meta:
        ordering = ['competencia']
        verbose_name = "Capacidad y potencialid"
        verbose_name_plural = "Capacidades y potencialidades"