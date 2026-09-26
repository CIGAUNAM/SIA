from django.conf import settings
from django.db import models

from nucleo.models import Ambito, Distincion, Institucion, NivelAcademico, Periodo, Persona


class DistincionAcademico(models.Model):
    distincion = models.ForeignKey(Distincion, on_delete=models.PROTECT, verbose_name='distinción')
    fecha = models.DateField()
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='distinciones')

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'distinción recibida'
        verbose_name_plural = 'distinciones recibidas'

    def __str__(self):
        return f'{self.distincion} ({self.fecha:%Y})'


class DistincionAlumno(models.Model):
    distincion = models.ForeignKey(Distincion, on_delete=models.PROTECT, verbose_name='distinción')
    alumno = models.ForeignKey(Persona, on_delete=models.PROTECT, related_name='distinciones_alumno')
    nivel = models.CharField(max_length=20, choices=NivelAcademico.choices)
    tutores = models.ManyToManyField(Persona, related_name='distinciones_alumnos_tutorados')
    fecha = models.DateField()

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'distinción recibida por alumno'
        verbose_name_plural = 'distinciones recibidas por alumnos'

    def __str__(self):
        return f'{self.distincion} — {self.alumno}'


class ComisionExpertos(Periodo):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField('descripción', blank=True)
    institucion = models.ForeignKey(Institucion, on_delete=models.PROTECT, null=True, blank=True,
                                    verbose_name='institución')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='comisiones_expertos')

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'participación en comisión de expertos'
        verbose_name_plural = 'participaciones en comisiones de expertos'

    def __str__(self):
        return self.nombre


class SociedadCientifica(Periodo):
    class Tipo(models.TextChoices):
        INVITACION = 'INVITACION', 'Por invitación'
        ELECCION = 'ELECCION', 'Por elección'

    nombre = models.CharField(max_length=255)
    descripcion = models.TextField('descripción', blank=True)
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    ambito = models.CharField('ámbito', max_length=20, choices=Ambito.choices)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='sociedades')

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'participación en sociedad científica'
        verbose_name_plural = 'participaciones en sociedades científicas'

    def __str__(self):
        return self.nombre


from nucleo.historial import registrar_historial  # noqa: E402

registrar_historial(globals())
