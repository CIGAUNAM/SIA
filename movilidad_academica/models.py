from django.conf import settings
from django.db import models

from nucleo.models import Institucion, Periodo


class MovilidadAcademica(Periodo):
    class Tipo(models.TextChoices):
        INVITACION = 'INVITACION', 'Académico invitado'
        ESTANCIA = 'ESTANCIA', 'Estancia académica'
        SABATICO = 'SABATICO', 'Sabático'

    class Financiamiento(models.TextChoices):
        PROGRAMAS_UNAM = 'PROGRAMAS_UNAM', 'Programas UNAM'
        POR_PROYECTO = 'POR_PROYECTO', 'Por proyecto'
        PRESUPUESTO_OPERATIVO = 'PRESUPUESTO_OPERATIVO', 'Presupuesto operativo'
        OTRO = 'OTRO', 'Otro'

    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    academico = models.CharField('académico invitado o anfitrión', max_length=255)
    institucion = models.ForeignKey(Institucion, on_delete=models.PROTECT, null=True, blank=True,
                                    verbose_name='institución')
    actividades = models.TextField()
    intercambio_unam = models.BooleanField('intercambio UNAM', default=False)
    financiamiento = models.CharField(max_length=30, choices=Financiamiento.choices, blank=True)
    redes_academicas = models.ManyToManyField('vinculacion.RedAcademica', blank=True, verbose_name='redes académicas')
    proyecto = models.ForeignKey('investigacion.ProyectoInvestigacion', on_delete=models.SET_NULL, null=True, blank=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='movilidades')

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'movilidad académica'
        verbose_name_plural = 'movilidad académica'

    def __str__(self):
        return f'{self.get_tipo_display()}: {self.academico}'


from nucleo.historial import registrar_historial  # noqa: E402

registrar_historial(globals())
