from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from nucleo.models import (Beca, Distincion, Institucion, NivelAcademico, Pais, Participante, Periodo, Persona,
                           ProgramaAcademico, requerido_si, validar_programa)


class AsesoriaEstudiante(Periodo):
    class Tipo(models.TextChoices):
        RESIDENCIA = 'RESIDENCIA', 'Residencia'
        PRACTICA = 'PRACTICA', 'Prácticas profesionales'
        ESTANCIA = 'ESTANCIA', 'Estancia de investigación'
        ASESORIA_TECNICA = 'ASESORIA_TECNICA', 'Asesoría técnica'
        SERVICIO_SOCIAL = 'SERVICIO_SOCIAL', 'Servicio social'

    asesorado = models.ForeignKey(Persona, on_delete=models.PROTECT, related_name='asesorias_recibidas')
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    nivel = models.CharField(max_length=20, choices=NivelAcademico.choices)
    programa = models.ForeignKey(ProgramaAcademico, on_delete=models.PROTECT, null=True, blank=True)
    beca = models.ForeignKey(Beca, on_delete=models.PROTECT, null=True, blank=True)
    proyecto = models.ForeignKey('investigacion.ProyectoInvestigacion', on_delete=models.SET_NULL, null=True, blank=True)
    institucion = models.ForeignKey(Institucion, on_delete=models.PROTECT, verbose_name='institución')
    periodo_academico = models.CharField('periodo académico', max_length=200, blank=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='asesorias')

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'asesoría de estudiante'
        verbose_name_plural = 'asesorías de estudiantes (residencias, prácticas, estancias, servicio social)'

    def __str__(self):
        return f'{self.asesorado} — {self.get_tipo_display()}'

    def clean(self):
        super().clean()
        validar_programa(self)


class SupervisionPostdoctoral(Periodo):
    investigador = models.ForeignKey(Persona, on_delete=models.PROTECT, related_name='supervisiones_recibidas')
    titulo_proyecto = models.CharField('título del proyecto', max_length=200)
    institucion = models.ForeignKey(Institucion, on_delete=models.PROTECT, verbose_name='institución')
    proyecto = models.ForeignKey('investigacion.ProyectoInvestigacion', on_delete=models.SET_NULL, null=True, blank=True)
    beca = models.ForeignKey(Beca, on_delete=models.PROTECT, null=True, blank=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='supervisiones')

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'supervisión de investigador postdoctoral'
        verbose_name_plural = 'supervisiones de investigadores postdoctorales'

    def __str__(self):
        return f'{self.investigador} — {self.titulo_proyecto}'


class GrupoInvestigacionInterno(Periodo):
    nombre = models.CharField(max_length=255)
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT, verbose_name='país')
    integrantes = models.ManyToManyField(Persona, related_name='grupos_investigacion')

    class Meta:
        ordering = ['nombre']
        verbose_name = 'área o grupo de investigación interno'
        verbose_name_plural = 'áreas o grupos de investigación internos'

    def __str__(self):
        return self.nombre


class DireccionTesis(Periodo):
    class Status(models.TextChoices):
        EN_PROCESO = 'EN_PROCESO', 'En proceso'
        TERMINADA = 'TERMINADA', 'Terminada'

    titulo_tesis = models.CharField('título de la tesis', max_length=255, unique=True)
    nivel = models.CharField(max_length=20, choices=NivelAcademico.choices)
    programa = models.ForeignKey(ProgramaAcademico, on_delete=models.PROTECT, null=True, blank=True)
    asesorado = models.ForeignKey(Persona, on_delete=models.PROTECT, related_name='tesis')
    status = models.CharField('estado', max_length=20, choices=Status.choices)
    fecha_examen = models.DateField('fecha del examen', null=True, blank=True)
    institucion = models.ForeignKey(Institucion, on_delete=models.PROTECT, verbose_name='institución')
    beca = models.ForeignKey(Beca, on_delete=models.PROTECT, null=True, blank=True)
    reconocimiento = models.ForeignKey(Distincion, on_delete=models.PROTECT, null=True, blank=True)
    director = models.ForeignKey(Persona, on_delete=models.PROTECT, null=True, blank=True,
                                 related_name='tesis_dirigidas')
    codirector = models.ForeignKey(Persona, on_delete=models.PROTECT, null=True, blank=True,
                                   related_name='tesis_codirigidas')
    tutores = models.ManyToManyField(Persona, through='DireccionTesisTutor', related_name='tesis_tutoradas')

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'dirección de tesis'
        verbose_name_plural = 'direcciones de tesis'

    def __str__(self):
        return self.titulo_tesis

    def clean(self):
        super().clean()
        validar_programa(self)
        requerido_si(self.status == self.Status.TERMINADA, self, 'fecha_examen',
                     'Una tesis terminada debe tener la fecha del examen.')


class DireccionTesisTutor(Participante):
    tesis = models.ForeignKey(DireccionTesis, on_delete=models.CASCADE)

    class Meta(Participante.Meta):
        verbose_name = 'tutor'
        verbose_name_plural = 'tutores'
        constraints = [models.UniqueConstraint(fields=['tesis', 'persona'], name='tesis_tutor_unico')]


class ComiteTutoral(Periodo):
    estudiante = models.ForeignKey(Persona, on_delete=models.PROTECT, related_name='comites_tutorales_estudiante')
    nivel = models.CharField(max_length=20, choices=NivelAcademico.choices)
    programa = models.ForeignKey(ProgramaAcademico, on_delete=models.PROTECT, null=True, blank=True)
    titulo_tesis = models.CharField('título de la tesis', max_length=255, blank=True)
    institucion = models.ForeignKey(Institucion, on_delete=models.PROTECT, verbose_name='institución')
    fecha_examen = models.DateField('fecha del examen', null=True, blank=True)
    miembros = models.ManyToManyField(Persona, through='ComiteTutoralMiembro', related_name='comites_tutorales')

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'comité tutoral'
        verbose_name_plural = 'comités tutorales'

    def __str__(self):
        return f'{self.estudiante} ({self.fecha_inicio:%Y})'

    def clean(self):
        super().clean()
        validar_programa(self)


class ComiteTutoralMiembro(Participante):
    comite = models.ForeignKey(ComiteTutoral, on_delete=models.CASCADE)

    class Meta(Participante.Meta):
        verbose_name = 'miembro'
        verbose_name_plural = 'miembros'
        constraints = [models.UniqueConstraint(fields=['comite', 'persona'], name='comite_tutoral_miembro_unico')]


class ComiteCandidaturaDoctoral(models.Model):
    candidato = models.ForeignKey(Persona, on_delete=models.PROTECT, related_name='candidaturas')
    titulo_tesis = models.CharField('título de la tesis', max_length=255, blank=True)
    programa = models.ForeignKey(ProgramaAcademico, on_delete=models.PROTECT, null=True, blank=True)
    especialidad = models.CharField(max_length=255, blank=True)
    institucion = models.ForeignKey(Institucion, on_delete=models.PROTECT, null=True, blank=True,
                                    verbose_name='institución')
    fecha_defensa = models.DateField('fecha de la defensa')
    director = models.ForeignKey(Persona, on_delete=models.PROTECT, null=True, blank=True,
                                 related_name='candidaturas_dirigidas')
    codirector = models.ForeignKey(Persona, on_delete=models.PROTECT, null=True, blank=True,
                                   related_name='candidaturas_codirigidas')
    asesores = models.ManyToManyField(Persona, blank=True, related_name='candidaturas_asesoradas')
    miembros = models.ManyToManyField(Persona, through='ComiteCandidaturaMiembro', related_name='candidaturas_sinodal')

    class Meta:
        ordering = ['-fecha_defensa']
        verbose_name = 'comité de candidatura doctoral'
        verbose_name_plural = 'comités de candidatura doctoral'

    def __str__(self):
        return f'{self.candidato} ({self.fecha_defensa:%Y})'

    def clean(self):
        super().clean()
        if self.programa_id and self.programa.nivel != NivelAcademico.DOCTORADO:
            raise ValidationError({'programa': 'Elige un programa de doctorado.'})


class ComiteCandidaturaMiembro(Participante):
    comite = models.ForeignKey(ComiteCandidaturaDoctoral, on_delete=models.CASCADE)

    class Meta(Participante.Meta):
        verbose_name = 'sinodal'
        verbose_name_plural = 'sinodales'
        constraints = [models.UniqueConstraint(fields=['comite', 'persona'], name='comite_candidatura_miembro_unico')]


from nucleo.historial import registrar_historial  # noqa: E402

registrar_historial(globals())
