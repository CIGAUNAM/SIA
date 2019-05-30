from django.db import models
from django.urls import reverse
from nucleo.models import User, Cargo, Nombramiento, Dependencia, Institucion, InstitucionSimple


# Create your models here.


class ExperienciaProfesional(models.Model):
    institucion = models.ForeignKey(InstitucionSimple, on_delete=models.DO_NOTHING, null=True, blank=True)
    cargo_text = models.CharField(max_length=254, blank=True, null=True)
    nombramiento = models.ForeignKey(Nombramiento, blank=True, null=True, on_delete=models.DO_NOTHING)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{} : {} : {}".format(self.usuario, self.institucion, self.cargo_text)

    def get_absolute_url(self):
        return reverse('experiencia_laboral_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['fecha_inicio']
        verbose_name = "Experiencia Laboral"
        verbose_name_plural = "Experiencias Laborales"

class LineaInvestigacion(models.Model):
    linea_investigacion = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    institucion2 = models.ForeignKey(Institucion, on_delete=models.DO_NOTHING)
    institucion = models.ForeignKey(InstitucionSimple, on_delete=models.DO_NOTHING, null=True, blank=True)

    dependencia = models.ForeignKey(Dependencia, on_delete=models.DO_NOTHING)
    fecha_inicio = models.DateField()
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    # tags = models.ManyToManyField(Tag, related_name='linea_investigacion_tags', blank=True)

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
    nombre = models.CharField(max_length=255, verbose_name='Capacidad o potencialidad')
    descripcion = models.TextField(blank=True)
    fecha_inicio = models.DateField()
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{} : {}".format(self.usuario, self.nombre)

    def get_absolute_url(self):
        return reverse('capacidad_potencialidad_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['nombre']
        verbose_name = "Capacidad y potencialid"
        verbose_name_plural = "Capacidades y potencialidades"
        unique_together = ['nombre', 'usuario']
