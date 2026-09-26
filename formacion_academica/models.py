from django.conf import settings
from django.db import models

from nucleo.models import Institucion, Modalidad, NivelAcademico, Periodo, Persona, requerido_si


class CursoEspecializacion(Periodo):
    class Tipo(models.TextChoices):
        CURSO = 'CURSO', 'Curso'
        DIPLOMADO = 'DIPLOMADO', 'Diplomado'
        CERTIFICACION = 'CERTIFICACION', 'Certificación'
        OTRO = 'OTRO', 'Otro'

    nombre = models.CharField('nombre del curso', max_length=255)
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    horas = models.PositiveIntegerField('número de horas')
    modalidad = models.CharField(max_length=20, choices=Modalidad.choices)
    institucion = models.ForeignKey(Institucion, on_delete=models.PROTECT, verbose_name='institución')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='cursos_especializacion')

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'curso de especialización'
        verbose_name_plural = 'cursos de especialización'

    def __str__(self):
        return f'{self.get_tipo_display()}: {self.nombre}'


class Grado(models.Model):
    """Grado académico (licenciatura, maestría o doctorado) obtenido por el académico."""
    nivel = models.CharField(max_length=20, choices=NivelAcademico.choices)
    titulo_obtenido = models.CharField('título obtenido', max_length=255)
    institucion = models.ForeignKey(Institucion, on_delete=models.PROTECT, verbose_name='institución')
    titulo_tesis = models.CharField('título de la tesis', max_length=255, blank=True)
    fecha_grado = models.DateField('fecha de obtención del grado')
    distincion_obtenida = models.CharField('distinción obtenida', max_length=255, blank=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='grados')

    class Meta:
        ordering = ['-fecha_grado']
        verbose_name = 'grado académico'
        verbose_name_plural = 'grados académicos'
        constraints = [models.UniqueConstraint(fields=['usuario', 'nivel', 'titulo_obtenido'], name='grado_unico')]

    def __str__(self):
        return f'{self.titulo_obtenido} ({self.institucion})'


class Postdoctorado(Periodo):
    class Financiamiento(models.TextChoices):
        CONACYT = 'CONACYT', 'CONAHCYT'
        SRE = 'SRE', 'SRE'
        DGAPA = 'DGAPA', 'DGAPA'
        OTRA = 'OTRA', 'Otra'

    titulo_proyecto = models.CharField('título del proyecto', max_length=255)
    tutor = models.ForeignKey(Persona, on_delete=models.PROTECT, null=True, blank=True)
    institucion = models.ForeignKey(Institucion, on_delete=models.PROTECT, verbose_name='institución')
    proyecto = models.ForeignKey('investigacion.ProyectoInvestigacion', on_delete=models.SET_NULL, null=True, blank=True)
    financiamiento = models.CharField(max_length=20, choices=Financiamiento.choices, blank=True)
    financiamiento_otro = models.CharField('otra entidad de financiamiento', max_length=160, blank=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='postdoctorados')

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'postdoctorado'
        verbose_name_plural = 'postdoctorados'

    def __str__(self):
        return self.titulo_proyecto

    def clean(self):
        super().clean()
        requerido_si(self.financiamiento == self.Financiamiento.OTRA, self, 'financiamiento_otro',
                     'Indica la entidad que financió el postdoctorado.')


from nucleo.historial import registrar_historial  # noqa: E402

registrar_historial(globals())
