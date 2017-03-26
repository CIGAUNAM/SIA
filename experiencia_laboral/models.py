from django.db import models
from django.core.urlresolvers import reverse
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

    def get_absolute_url(self):
        return reverse('experiencia_laboral_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['fecha_inicio', 'dependencia']
        verbose_name = "Experiencia Laboral"
        verbose_name_plural = "Experiencias Laborales"
        unique_together = ['dependencia', 'cargo', 'fecha_fin', 'usuario']


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

    def get_absolute_url(self):
        return reverse('linea_investigacion_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['fecha_inicio', 'linea_investigacion']
        verbose_name = "Línea de investigación"
        verbose_name_plural = "Líneas de investigación"
        unique_together = ['linea_investigacion', 'fecha_inicio', 'usuario']


class CapacidadPotencialidad(models.Model):
    competencia = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    usuario = models.ForeignKey(User)
    tags = models.ManyToManyField(Tag, related_name='capacidad_potencialidad_tags', blank=True)

    def __str__(self):
        return "{} : {}".format(self.usuario, self.competencia)

    def get_absolute_url(self):
        return reverse('capacidad_potencialidad_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['competencia']
        verbose_name = "Capacidad y potencialid"
        verbose_name_plural = "Capacidades y potencialidades"
        unique_together = ['competencia', 'usuario']