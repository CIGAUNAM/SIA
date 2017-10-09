from django.db import models

#from django.contrib.auth.models import User
from autoslug import AutoSlugField
from nucleo.models import User, Institucion, Dependencia, ProgramaLicenciatura, ProgramaMaestria, ProgramaDoctorado, Asignatura
from investigacion.models import ProyectoInvestigacion
from vinculacion.models import RedAcademica


# Create your models here.

class CursoDocencia(models.Model):
    nivel = models.CharField(max_length=30, choices=(('OTRO', 'Otro'), ('LICENCIATURA', 'Licenciatura'), ('MAESTRIA', 'Maestría'), ('DOCTORADO', 'Doctorado')))
    tipo = models.CharField(max_length=20, choices=(('ESCOLARIZADO', 'Escolarizado'), ('EXTRACURRICULAR', 'Extracurricular')))
    licenciatura = models.ForeignKey(ProgramaLicenciatura, blank=True, null=True)
    maestria = models.ForeignKey(ProgramaMaestria, blank=True, null=True)
    doctorado = models.ForeignKey(ProgramaDoctorado, blank=True, null=True)
    asignatura = models.ForeignKey(Asignatura)
    modalidad = models.CharField(max_length=30, choices=(('PRESENCIAL', 'Presencial'), ('EN_LINEA', 'En línea')))
    #nivel_participacion = models.CharField(max_length=30, choices=(('TITULAR', 'Titular / Responsable'), ('COLABORADOR', 'Colaborador / Invitado')))
    institucion = models.ForeignKey(Institucion)
    dependencia = models.ForeignKey(Dependencia)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    total_horas = models.PositiveIntegerField()
    usuario = models.ForeignKey(User, related_name='cursodocencia_usuario')
    academicos_participantes = models.ManyToManyField(User, related_name='cursodocencia_academicos_participantes', blank=True, verbose_name='Académicos participantes')
    otras_dependencias_participantes = models.ManyToManyField(Dependencia, related_name='curso_escolarizado_otras_dependencias_participantes', blank=True)

    def __str__(self):
        return "{} : {} : {}".format(self.asignatura, str(self.dependencia.nombre), self.fecha_inicio)

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'




