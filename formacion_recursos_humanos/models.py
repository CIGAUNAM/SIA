from django.db import models
from django.urls import reverse
from django.conf import settings
from nucleo.models import User, Institucion, Dependencia, Beca, ProgramaLicenciatura, ProgramaMaestria, \
    ProgramaDoctorado, Pais, Distincion, Libro as LibroInvestigacion
from investigacion.models import ProyectoInvestigacion, ArticuloCientifico, CapituloLibroInvestigacion
from sortedm2m.fields import SortedManyToManyField

NIVEL_ACADEMICO = getattr(settings, 'NIVEL_ACADEMICO', (('', '-------'), ('LICENCIATURA', 'Licenciatura'),
                                                        ('MAESTRIA', 'Maestría'), ('DOCTORADO', 'Doctorado')))


# Create your models here.


class AsesoriaEstudiante(models.Model):
    asesorado = models.ForeignKey(User, related_name='asesoria_estudiante_asesorado', on_delete=models.DO_NOTHING)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=30, choices=(('', 'Seleccionar tipo de Asesoría'), ('RESIDENCIA', 'Residencia'),
                                                    ('PRACTICA', 'Prácticas profesionales'),
                                                    ('ESTANCIA', 'Estancia de investigación'),
                                                    ('BECARIO', 'Becario de proyecto de investigación'),
                                                    ('SERVICIO_SOCIAL', 'Servicio Social')))
    nivel_academico = models.CharField(max_length=20, choices=NIVEL_ACADEMICO)
    programa_licenciatura = models.ForeignKey(ProgramaLicenciatura, null=True, blank=True, on_delete=models.DO_NOTHING)
    programa_maestria = models.ForeignKey(ProgramaMaestria, null=True, blank=True, on_delete=models.DO_NOTHING)
    programa_doctorado = models.ForeignKey(ProgramaDoctorado, null=True, blank=True, on_delete=models.DO_NOTHING)
    beca = models.ForeignKey(Beca, null=True, blank=True, on_delete=models.DO_NOTHING)
    proyecto_externo = models.CharField(max_length=254, null=True, blank=True)
    proyecto = models.ForeignKey(ProyectoInvestigacion, null=True, blank=True, on_delete=models.DO_NOTHING)
    institucion = models.ForeignKey(Institucion, on_delete=models.DO_NOTHING)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.DO_NOTHING)
    periodo_academico = models.CharField(max_length=200)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    usuario = models.ForeignKey(User, related_name='asesoria_estudiante_usuario', on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{} : {}".format(str(self.asesorado), self.fecha_inicio)

    def get_absolute_url(self):
        return reverse('asesor_estancia_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha_inicio', '-fecha_fin']
        verbose_name = 'Asesoría en residencias / prácticas / estancias / servicio social'
        verbose_name_plural = 'Asesorías en residencias / prácticas / estancias / servicio social'
        unique_together = ['usuario', 'asesorado', 'nivel_academico', 'periodo_academico']


class SupervisionInvestigadorPostDoctoral(models.Model):
    investigador = models.ForeignKey(User, related_name='supervision_investigador_postdoctoral_investigador',
                                     on_delete=models.DO_NOTHING)
    disciplina = models.CharField(max_length=200)
    institucion = models.ForeignKey(Institucion, on_delete=models.DO_NOTHING)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.DO_NOTHING)
    proyecto = models.ForeignKey(ProyectoInvestigacion, on_delete=models.DO_NOTHING)
    beca = models.ForeignKey(Beca, on_delete=models.DO_NOTHING)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    articulos = models.ManyToManyField(ArticuloCientifico, blank=True)
    libros = models.ManyToManyField(LibroInvestigacion, blank=True)
    capitulos_libros = models.ManyToManyField(CapituloLibroInvestigacion, blank=True)
    usuario = models.ForeignKey(User, related_name='supervision_investigador_postdoctoral_usuario',
                                on_delete=models.DO_NOTHING)

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
    pais = models.ForeignKey(Pais, on_delete=models.DO_NOTHING)
    usuarios = models.ManyToManyField(User)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('grupo_investigacion_interno_detalle', kwargs={'pk': self.pk})

    def natural_key(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Área o grupo de investigación interno'
        verbose_name_plural = 'Áreas o grupos de investigación internos'


class DireccionTesis(models.Model):
    titulo_tesis = models.CharField(max_length=255, unique=True)
    nivel_academico = models.CharField(max_length=20, choices=NIVEL_ACADEMICO)
    programa = models.CharField(max_length=255)
    asesorado = models.ForeignKey(User, related_name='direccion_tesis_asesorado', on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=255, choices=(
        ('', '-------'), ('EN_PROCESO', 'Tesis en proceso'), ('TERMINADA', 'Tesis terminada')))
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    fecha_examen = models.DateField(null=True, blank=True)
    institucion2 = models.ForeignKey(Institucion, on_delete=models.DO_NOTHING)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.DO_NOTHING)
    beca = models.ForeignKey(Beca, null=True, blank=True, on_delete=models.DO_NOTHING)
    reconocimiento = models.ForeignKey(Distincion, null=True, blank=True, on_delete=models.DO_NOTHING)
    reconocimiento_text = models.CharField(max_length=255, null=True, blank=True,)
    director = models.ForeignKey(User, null=True, blank=True, related_name='direccion_tesis_director', on_delete=models.DO_NOTHING)
    codirector = models.ForeignKey(User, null=True, blank=True, related_name='direccion_tesis_codirector', on_delete=models.DO_NOTHING)
    tutores = SortedManyToManyField(User, null=True, blank=True, related_name='direccion_tesis_usuarios', verbose_name='Tutores')


    def __str__(self):
        return "{} : {}".format(self.titulo_tesis, self.asesorado, self.nivel_academico)

    def get_absolute_url(self):
        return reverse('direccion_tesis_detalle', kwargs={'pk': self.pk})

    def natural_key(self):
        return self.titulo_tesis

    class Meta:
        ordering = ['-fecha_examen']
        verbose_name = 'Dirección de tesis'
        verbose_name_plural = 'Direcciones de tesis'


class ComiteTutoral(models.Model):
    estudiante = models.ForeignKey(User, related_name='comite_tutoral_estudiante', on_delete=models.DO_NOTHING)
    nivel_academico = models.CharField(max_length=20, choices=NIVEL_ACADEMICO)
    programa_licenciatura = models.ForeignKey(ProgramaLicenciatura, null=True, blank=True, on_delete=models.DO_NOTHING)
    programa_maestria = models.ForeignKey(ProgramaMaestria, null=True, blank=True, on_delete=models.DO_NOTHING)
    programa_doctorado = models.ForeignKey(ProgramaDoctorado, null=True, blank=True, on_delete=models.DO_NOTHING)
    programa = models.CharField(max_length=255, null=True, blank=True)

    titulo_tesis = models.CharField(max_length=255, null=True, blank=True)
    institucion2 = models.ForeignKey(Institucion, on_delete=models.DO_NOTHING)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.DO_NOTHING)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    fecha_examen = models.DateField(null=True, blank=True)
    miembros_comite = SortedManyToManyField(User, related_name='comite_tutoral_miembros_comite', verbose_name='Miembros de comité tutoral')

    def __str__(self):
        return "{} : {}".format(str(self.estudiante), self.fecha_inicio)

    def get_absolute_url(self):
        return reverse('comite_tutoral_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'Comité tutoral'
        verbose_name_plural = 'Comités tutorales'


class ComiteCandidaturaDoctoral(models.Model):
    candidato = models.ForeignKey(User, related_name='comite_candidatura_doctoral_candidato',
                                  on_delete=models.DO_NOTHING)
    titulo_tesis = models.CharField(max_length=255, null=True, blank=True)
    programa = models.CharField(max_length=255, null=True, blank=True)
    especialidad = models.CharField(max_length=255, null=True, blank=True)

    asesores = SortedManyToManyField(User, related_name='comite_candidatura_doctoral_asesores', blank=True)
    programa_doctorado = models.ForeignKey(ProgramaDoctorado, on_delete=models.DO_NOTHING)
    institucion2 = models.ForeignKey(Institucion, on_delete=models.DO_NOTHING)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.DO_NOTHING)
    fecha_defensa = models.DateField()
    miembros_comite = SortedManyToManyField(User, related_name='comite_candidatura_doctoral_sinodales', blank=True)
    director = models.ForeignKey(User, null=True, blank=True, related_name='comite_candidatura_doctoral_director', on_delete=models.DO_NOTHING)
    codirector = models.ForeignKey(User, null=True, blank=True, related_name='comite_candidatura_doctoral_codirector', on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{} : {}".format(str(self.candidato), self.fecha_defensa)

    def get_absolute_url(self):
        return reverse('comite_candidatura_doctoral_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-fecha_defensa']
        verbose_name = 'Comité de examen de candidatura doctoral'
        verbose_name_plural = 'Comités de exámenes de candidatura doctoral'
