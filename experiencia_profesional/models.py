from django.conf import settings
from django.db import models

from nucleo.models import Institucion, Nombramiento, Periodo


class ExperienciaProfesional(Periodo):
    cargo = models.CharField(max_length=254)
    nombramiento = models.ForeignKey(Nombramiento, on_delete=models.PROTECT, null=True, blank=True)
    institucion = models.ForeignKey(Institucion, on_delete=models.PROTECT, null=True, blank=True,
                                    verbose_name='institución')
    descripcion = models.TextField('descripción', blank=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='experiencias')

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'experiencia profesional'
        verbose_name_plural = 'experiencias profesionales'

    def __str__(self):
        return f'{self.cargo} — {self.institucion}' if self.institucion else self.cargo


class LineaInvestigacion(models.Model):
    nombre = models.CharField('línea de investigación', max_length=255)
    descripcion = models.TextField('descripción', blank=True)
    institucion = models.ForeignKey(Institucion, on_delete=models.PROTECT, null=True, blank=True,
                                    verbose_name='institución')
    fecha_inicio = models.DateField('fecha de inicio', null=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='lineas_investigacion')

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'línea de investigación'
        verbose_name_plural = 'líneas de investigación'
        constraints = [models.UniqueConstraint(fields=['usuario', 'nombre'], name='linea_investigacion_unica')]

    def __str__(self):
        return self.nombre


class CapacidadPotencialidad(models.Model):
    nombre = models.CharField('capacidad o potencialidad', max_length=255)
    descripcion = models.TextField('descripción', blank=True)
    fecha_inicio = models.DateField('fecha de inicio')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='capacidades')

    class Meta:
        ordering = ['nombre']
        verbose_name = 'capacidad o potencialidad'
        verbose_name_plural = 'capacidades y potencialidades'
        constraints = [models.UniqueConstraint(fields=['usuario', 'nombre'], name='capacidad_unica')]

    def __str__(self):
        return self.nombre


from nucleo.historial import registrar_historial  # noqa: E402

registrar_historial(globals())
