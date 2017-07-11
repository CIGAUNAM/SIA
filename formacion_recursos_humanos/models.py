from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from nucleo.models import User, Institucion, Dependencia, Beca, Proyecto, Reconocimiento, ProgramaLicenciatura, ProgramaMaestria, ProgramaDoctorado

GRADO_ACADEMICO = getattr(settings, 'GRADO_ACADEMICO', (('LICENCIATURA', 'Licenciatura'), ('MAESTRIA', 'Maestría'), ('DOCTORADO', 'Doctorado')))

# Create your models here.

class AsesorEstancia(models.Model):
    asesorado = models.ForeignKey(User, related_name='asesor_estancia_asesorado')
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=30, choices=(('RESIDENCIA', 'Residencia'), ('PRACTICA', 'Práctica'), ('ESTANCIA', 'Estancia'), ('SERVICIO_SOCIAL', 'Servicio Social'), ('OTRO', 'Otro')))
    grado_academico = models.CharField(max_length=20, choices=GRADO_ACADEMICO)
    programa_licenciatura = models.ForeignKey(ProgramaLicenciatura, null=True, blank=True)
    programa_maestria = models.ForeignKey(ProgramaMaestria, null=True, blank=True)
    programa_doctorado = models.ForeignKey(ProgramaDoctorado, null=True, blank=True)
    beca = models.ForeignKey(Beca, null=True, blank=True)
    proyecto = models.ForeignKey(Proyecto, null=True, blank=True)
    institucion = models.ForeignKey(Institucion)
    dependencia = models.ForeignKey(Dependencia)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    usuario = models.ForeignKey(User, related_name='asesor_estancia_usuario')

    def __str__(self):
        return "{} : {}".format(str(self.asesorado), self.fecha_inicio)

    def get_absolute_url(self):
        return reverse('asesor_estancia_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha_inicio', '-fecha_fin']
        verbose_name = 'Asesor en residencias / prácticas / estancias / servicio social'
        verbose_name_plural = 'Asesores en residencias / prácticas / estancias / servicio social'
        unique_together = ['usuario', 'asesorado', 'grado_academico']


"""
class DireccionTesis1(models.Model):
    asesor = models.ForeignKey(User, related_name='direccion_tesis_asesor')
    fecha_inicio = models.DateField()
    tesis = models.ForeignKey(DireccionTesis)

    def __str__(self):
        return "{} : {} : {}".format(self.tesis, self.asesor, self.fecha_inicio)

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'Dirección de tesis'
        verbose_name_plural = 'Direcciones de tesis'
"""

class DireccionTesis(models.Model):
    titulo = models.CharField(max_length=255, unique=True)
    #slug = AutoSlugField(populate_from='titulo')
    asesorado = models.ForeignKey(User, related_name='direccion_tesis_asesorado')
    descripcion = models.TextField(blank=True)
    grado_academico = models.CharField(max_length=20, choices=GRADO_ACADEMICO)
    documento_tesis = models.FileField(null=True, blank=True)
    institucion = models.ForeignKey(Institucion)
    dependencia = models.ForeignKey(Dependencia)
    beca = models.ForeignKey(Beca, null=True, blank=True)
    reconocimiento = models.ForeignKey(Reconocimiento, blank=True, null=True)
    fecha_examen = models.DateField(null=True, blank=True)
    usuario = models.ForeignKey(User, related_name='direccion_tesis_usuario')

    def __str__(self):
        return "{} : {}".format(self.titulo, self.asesorado, self.grado_academico)

    def get_absolute_url(self):
        return reverse('direccion_tesis_detalle', kwargs={'pk': self.pk})

    def natural_key(self):
        return (self.titulo)

    class Meta:
        ordering = ['-fecha_examen']
        verbose_name = 'Tesis'
        verbose_name_plural = 'Tesis'

class ComiteTutoral(models.Model):
    grado_academico = models.CharField(max_length=20, choices=(('MAESTRIA', 'Maestría'), ('DOCTORADO', 'Doctorado')))
    programa_maestria = models.ForeignKey(ProgramaMaestria, null=True, blank=True)
    programa_doctorado = models.ForeignKey(ProgramaDoctorado, null=True, blank=True)
    status = models.CharField(max_length=20, choices=(('EN_PROCESO', 'En proceso'), ('CONCLUIDO', 'Concluído')))
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    asesorado = models.ForeignKey(User, related_name='comite_tutoral_asesorado')
    asesor_principal = models.ForeignKey(User, related_name='comite_tutoral_asesor_principal')
    otros_asesores = models.ManyToManyField(User, related_name='comite_tutoral_otros_asesores', blank=True)
    sinodales = models.ManyToManyField(User, related_name='comite_tutoral_sinodales', blank=True)
    proyecto = models.ForeignKey(Proyecto, null=True, blank=True)
    institucion = models.ForeignKey(Institucion)
    dependencia = models.ForeignKey(Dependencia)

    def __str__(self):
        return "{} : {} : {}".format(str(self.asesorado), self.fecha_inicio, str(self.asesor_principal))

    def get_absolute_url(self):
        return reverse('comite_tutoral_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'Comité tutoral'
        verbose_name_plural = 'Comités tutorales'


class ComiteCandidaturaDoctoral(models.Model):
    asesorado = models.ForeignKey(User, related_name='comite_candidatura_doctoral_asesorado')
    asesor_principal = models.ForeignKey(User, related_name='comite_candidatura_doctoral_asesor_principal')
    otros_asesores = models.ManyToManyField(User, related_name='comite_candidatura_doctoral_otros_asesores', blank=True)
    sinodales = models.ManyToManyField(User, related_name='comite_candidatura_doctoral_sinodales', blank=True)
    proyecto = models.ForeignKey(Proyecto, null=True, blank=True)
    programa_doctorado = models.ForeignKey(ProgramaDoctorado)
    institucion = models.ForeignKey(Institucion)
    dependencia = models.ForeignKey(Dependencia)
    fecha_defensa = models.DateField()

    def __str__(self):
        return "{} : {} : {}".format(str(self.asesorado), self.fecha_defensa, str(self.asesor_principal))

    def get_absolute_url(self):
        return reverse('comite_candidatura_doctoral_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha_defensa']
        verbose_name = 'Comité de examen de candidatura doctoral'
        verbose_name_plural = 'Comités de exámenes de candidatura doctoral'
