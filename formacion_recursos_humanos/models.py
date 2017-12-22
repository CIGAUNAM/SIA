from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from nucleo.models import User, Institucion, Dependencia, Beca, Reconocimiento, ProgramaLicenciatura, ProgramaMaestria, \
    ProgramaDoctorado, Pais, Estado, Ciudad
from investigacion.models import ProyectoInvestigacion, ArticuloCientifico, Libro, CapituloLibroInvestigacion
from sortedm2m.fields import SortedManyToManyField


NIVEL_ACADEMICO = getattr(settings, 'NIVEL_ACADEMICO', (('', '-------'), ('LICENCIATURA', 'Licenciatura'), ('MAESTRIA', 'Maestría'), ('DOCTORADO', 'Doctorado')))

# Create your models here.

class AsesoriaEstudiante(models.Model):
    asesorado = models.ForeignKey(User, related_name='asesoria_estudiante_asesorado')
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=30, choices=(('', 'Seleccionar tipo de Asesoría'), ('RESIDENCIA', 'Residencia'), ('PRACTICA', 'Prácticas profesionales'), ('ESTANCIA', 'Estancia de investigación'), ('BECARIO', 'Becario de proyecto de investigación'), ('SERVICIO_SOCIAL', 'Servicio Social')))
    nivel_academico = models.CharField(max_length=20, choices=NIVEL_ACADEMICO)
    programa_licenciatura = models.ForeignKey(ProgramaLicenciatura, null=True, blank=True)
    programa_maestria = models.ForeignKey(ProgramaMaestria, null=True, blank=True)
    programa_doctorado = models.ForeignKey(ProgramaDoctorado, null=True, blank=True)
    beca = models.ForeignKey(Beca, null=True, blank=True)
    proyecto = models.ForeignKey(ProyectoInvestigacion, null=True, blank=True)
    institucion = models.ForeignKey(Institucion)
    dependencia = models.ForeignKey(Dependencia)
    periodo_academico = models.CharField(max_length=200)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    usuario = models.ForeignKey(User, related_name='asesoria_estudiante_usuario')

    def __str__(self):
        return "{} : {}".format(str(self.asesorado), self.fecha_inicio)

    def get_absolute_url(self):
        return reverse('asesoria_estudiante_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha_inicio', '-fecha_fin']
        verbose_name = 'Asesoría en residencias / prácticas / estancias / servicio social'
        verbose_name_plural = 'Asesorías en residencias / prácticas / estancias / servicio social'
        unique_together = ['usuario', 'asesorado', 'nivel_academico']


class SupervisionInvestigadorPostDoctoral(models.Model):
    investigador = models.ForeignKey(User, related_name='supervision_investigador_postdoctoral_investigador')
    disciplina = models.CharField(max_length=200)
    institucion = models.ForeignKey(Institucion)
    dependencia = models.ForeignKey(Dependencia)
    proyecto = models.ForeignKey(ProyectoInvestigacion)
    beca = models.ForeignKey(Beca)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    articulos = models.ManyToManyField(ArticuloCientifico, blank=True)
    libros = models.ManyToManyField(Libro, blank=True)
    capitulos_libros = models.ManyToManyField(CapituloLibroInvestigacion, blank=True)
    usuario = models.ForeignKey(User, related_name='supervision_investigador_postdoctoral_usuario')
    def __str__(self):
        return "{} : {} : {}".format(self.investigador, self.usuario, self.fecha_inicio)

    def get_absolute_url(self):
        return reverse('supervision_investigador_postdoctoral_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha_inicio', '-fecha_fin']
        verbose_name = 'Supervisión de investigador postdoctoral'
        verbose_name_plural = 'Supervisiones de investigadores postdoctorales'


class DesarrolloGrupoInvestigacionInterno(models.Model):
    nombre = models.CharField(max_length=255)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    grado_consolidacion = models.CharField(max_length=255)
    pais = models.ForeignKey(Pais)
    usuarios = models.ManyToManyField(User)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('desarrollo_grupo_investigacion_detalle', kwargs={'pk': self.pk})

    def natural_key(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Área o grupo de investigación interno'
        verbose_name_plural = 'Áreas o grupos de investigación internos'


class DireccionTesis(models.Model):
    titulo = models.CharField(max_length=255, unique=True)
    especialidad = models.CharField(max_length=255)
    asesorado = models.ForeignKey(User, related_name='direccion_tesis_asesorado')
    descripcion = models.TextField(blank=True)
    grado_academico = models.CharField(max_length=20, choices=NIVEL_ACADEMICO)
    documento_tesis = models.FileField(null=True, blank=True)
    institucion = models.ForeignKey(Institucion)
    dependencia = models.ForeignKey(Dependencia)
    beca = models.ForeignKey(Beca, null=True, blank=True)
    fecha_examen = models.DateField(null=True, blank=True)
    usuarios = SortedManyToManyField(User, related_name='direccion_tesis_usuarios', verbose_name='Tutores')

    def __str__(self):
        return "{} : {}".format(self.titulo, self.asesorado, self.grado_academico)

    def get_absolute_url(self):
        return reverse('direccion_tesis_detalle', kwargs={'pk': self.pk})

    def natural_key(self):
        return self.titulo

    class Meta:
        ordering = ['-fecha_examen']
        verbose_name = 'Dirección de tesis'
        verbose_name_plural = 'Direcciones de tesis'


class ComiteTutoral(models.Model):
    estudiante = models.ForeignKey(User, related_name='comite_tutoral_estudiante')
    grado_academico = models.CharField(max_length=20, choices=(('', '-------'), ('LICENCIATURA', 'Licenciatura'), ('MAESTRIA', 'Maestría'), ('DOCTORADO', 'Doctorado')))
    programa_licenciatura = models.ForeignKey(ProgramaLicenciatura, null=True, blank=True)
    programa_maestria = models.ForeignKey(ProgramaMaestria, null=True, blank=True)
    programa_doctorado = models.ForeignKey(ProgramaDoctorado, null=True, blank=True)
    institucion = models.ForeignKey(Institucion)
    dependencia = models.ForeignKey(Dependencia)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    fecha_examen = models.DateField(null=True, blank=True)
    asesores = SortedManyToManyField(User, related_name='comite_tutoral_asesores', verbose_name='Asesores', blank=True)
    sinodales = SortedManyToManyField(User, related_name='comite_tutoral_sinodales', verbose_name='Sinodales', blank=True)
    proyecto = models.ForeignKey(ProyectoInvestigacion, null=True, blank=True)

    def __str__(self):
        return "{} : {}".format(str(self.estudiante), self.fecha_inicio)

    def get_absolute_url(self):
        return reverse('comite_tutoral_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'Comité tutoral'
        verbose_name_plural = 'Comités tutorales'


class ComiteCandidaturaDoctoral(models.Model):
    asesorado = models.ForeignKey(User, related_name='comite_candidatura_doctoral_asesorado')
    asesores = SortedManyToManyField(User, related_name='comite_candidatura_doctoral_asesores', blank=True)
    sinodales = SortedManyToManyField(User, related_name='comite_candidatura_doctoral_sinodales', blank=True)
    proyecto = models.ForeignKey(ProyectoInvestigacion, null=True, blank=True)
    programa_doctorado = models.ForeignKey(ProgramaDoctorado)
    institucion = models.ForeignKey(Institucion)
    dependencia = models.ForeignKey(Dependencia)
    fecha_defensa = models.DateField()

    def __str__(self):
        return "{} : {}".format(str(self.asesorado), self.fecha_defensa)

    def get_absolute_url(self):
        return reverse('comite_candidatura_doctoral_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha_defensa']
        verbose_name = 'Comité de examen de candidatura doctoral'
        verbose_name_plural = 'Comités de exámenes de candidatura doctoral'

