from django.db import models

from django.conf import settings
from nucleo.models import User, Tag, Dependencia, Beca, Proyecto, Tesis, ProgramaLicenciatura, ProgramaMaestria, ProgramaDoctorado

GRADO_ACADEMICO = getattr(settings, 'GRADO_ACADEMICO', (('LICENCIATURA', 'licenciatura'), ('MAESTRIA', 'Maestría'), ('DOCTORADO', 'Doctorado')))

# Create your models here.

class AsesorEstancia(models.Model):
    descripcion = models.TextField(blank=True)
    asesor = models.ForeignKey(User, related_name='asesor_estancia_asesor')
    tipo = models.CharField(max_length=30, choices=(('RESIDENCIA', 'Residencia'), ('PRACTICA', 'Práctica'), ('ESTANCIA', 'Estancia'), ('SERVICIO_SOCIAL', 'Servicio Social'), ('OTRO', 'Otro')))
    asesorado = models.ForeignKey(User, related_name='asesor_estancia_asesorado')
    grado_academico = models.CharField(max_length=20, choices=GRADO_ACADEMICO)
    beca = models.ForeignKey(Beca)
    proyecto = models.ForeignKey(Proyecto)
    programa_licenciatura = models.ForeignKey(ProgramaLicenciatura)
    programa_maestria = models.ForeignKey(ProgramaMaestria)
    programa_doctorado = models.ForeignKey(ProgramaDoctorado)
    dependencia = models.ForeignKey(Dependencia)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return "{} : {} : {}".format(str(self.asesor), str(self.asesorado), self.fecha_inicio)

    class Meta:
        ordering = ['-fecha_inicio', '-fecha_fin']
        verbose_name = 'Asesor en residencias / prácticas / estancias / servicio social'
        verbose_name_plural = 'Asesores en residencias / prácticas / estancias / servicio social'


class DireccionTesis(models.Model):
    asesor = models.ForeignKey(User, related_name='direccion_tesis_asesor')
    fecha_inicio = models.DateField()
    tesis = models.ForeignKey(Tesis)

    def __str__(self):
        return "{} : {} : {}".format(self.tesis, self.asesor, self.fecha_inicio)

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'Dirección de tesis'
        verbose_name_plural = 'Direcciones de tesis'


class ComiteTutoral(models.Model):
    grado_academico = models.CharField(max_length=20, choices=GRADO_ACADEMICO)
    status = models.CharField(max_length=20, choices=(('EN_PROCESO', 'En proceso'), ('CONCLUIDO', 'Concluído')))
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    alumno = models.ForeignKey(User, related_name='comite_tutoral_alumno')
    asesor_principal = models.ForeignKey(User, related_name='comite_tutoral_asesor_principal')
    otros_asesores = models.ManyToManyField(User, related_name='comite_tutoral_otros_asesores', blank=True)
    sinodales = models.ManyToManyField(User, related_name='comite_tutoral_sinodales', blank=True)
    proyecto = models.ForeignKey(Proyecto)
    programa_maestria = models.ForeignKey(ProgramaMaestria)
    programa_doctorado = models.ForeignKey(ProgramaDoctorado)
    dependencia = models.ForeignKey(Dependencia)

    def __str__(self):
        return "{} : {} : {}".format(str(self.alumno), self.fecha_inicio, str(self.asesor_principal))

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'Comité tutoral'
        verbose_name_plural = 'Comités tutorales'


class ComiteCandidaturaDoctoral(models.Model):
    fecha_defensa = models.DateField()
    alumno = models.ForeignKey(User, related_name='comite_candidatura_doctoral_alumno')
    asesor_principal = models.ForeignKey(User, related_name='comite_candidatura_doctoral_asesor_principal')
    otros_asesores = models.ManyToManyField(User, related_name='comite_candidatura_doctoral_otros_asesores', blank=True)
    sinodales = models.ManyToManyField(User, related_name='comite_candidatura_doctoral_sinodales', blank=True)
    proyecto = models.ForeignKey(Proyecto)
    programa_doctorado = models.ForeignKey(ProgramaDoctorado)
    dependencia = models.ForeignKey(Dependencia)

    def __str__(self):
        return "{} : {} : {}".format(str(self.alumno), self.fecha_defensa, str(self.asesor_principal))

    class Meta:
        ordering = ['-fecha_defensa']
        verbose_name = 'Comité de examen de candidatura doctoral'
        verbose_name_plural = 'Comités de exámenes de candidatura doctoral'
