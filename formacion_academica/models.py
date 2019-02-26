from django.db import models
from django.conf import settings
from django.urls import reverse
from nucleo.models import User, Dependencia, Institucion, AreaConocimiento, ProgramaLicenciatura, ProgramaMaestria, ProgramaDoctorado
from investigacion.models import ProyectoInvestigacion

CURSO_ESPECIALIZACION_TIPO = getattr(settings, 'CURSO_ESPECIALIZACION_TIPO', (('', ''), ('', ''), ('CURSO', 'Curso'),
                                                                              ('DIPLOMADO', 'Diplomado'),
                                                                              ('CERTIFICACION', 'Certificación'),
                                                                              ('OTRO', 'Otro')))
CURSO_ESPECIALIZACION_MODALIDAD = getattr(settings, 'CURSO_ESPECIALIZACION_MODALIDAD', (('PRESENCIAL', 'Presencial'),
                                                                                        ('EN_LINEA', 'En línea'),
                                                                                        ('MIXTO', 'Mixto'),
                                                                                        ('OTRO', 'Otro')))


# Create your models here.


class CursoEspecializacion(models.Model):
    nombre = models.CharField(max_length=255, verbose_name='Nombre del curso',
                              help_text='Nombre del curso texto de ayuda')
    descripcion = models.TextField(verbose_name='Descripción', blank=True)
    tipo = models.CharField(max_length=20, choices=CURSO_ESPECIALIZACION_TIPO, verbose_name='Tipo de curso')
    horas = models.PositiveIntegerField(verbose_name='Número de horas')
    fecha_inicio = models.DateField('Fecha de inicio')
    fecha_fin = models.DateField('Fecha de finalización', blank=True, null=True)
    modalidad = models.CharField(max_length=20, choices=CURSO_ESPECIALIZACION_MODALIDAD)
    area_conocimiento = models.ForeignKey(AreaConocimiento, verbose_name='Área de conocimiento',
                                          on_delete=models.DO_NOTHING)
    # institucion = models.ForeignKey(Institucion, on_delete=models.DO_NOTHING)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.DO_NOTHING)
    usuario = models.ForeignKey(User, related_name='cursos_especializacion', on_delete=models.DO_NOTHING)
    # tags = models.ManyToManyField(Tag, related_name='curso_especializacion_tags', blank=True)

    def __str__(self):
        return "{} de {}".format(self.tipo, self.nombre)

    def get_absolute_url(self):
        return reverse('curso_especializacion_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['fecha_inicio']
        verbose_name = 'Curso de especialización'
        verbose_name_plural = 'Cursos de especialización'
        unique_together = ['nombre', 'usuario', 'fecha_fin']


class Licenciatura(models.Model):
    carrera = models.ForeignKey(ProgramaLicenciatura, on_delete=models.DO_NOTHING)
    descripcion = models.TextField(verbose_name='Descripición', blank=True)
    institucion = models.ForeignKey(Institucion, on_delete=models.DO_NOTHING)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.DO_NOTHING)
    titulo_tesis = models.CharField(max_length=255)
    tesis_url = models.URLField(blank=True)
    fecha_inicio = models.DateField('Fecha de inicio de licenciatura')
    fecha_fin = models.DateField('Fecha de terminación de licenciatura')
    fecha_grado = models.DateField('Fecha de obtención de grado de licenciatura')
    usuario = models.ForeignKey(User, related_name='licenciaturas', on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{}, {}, {}".format(str(self.carrera.nombre), self.dependencia, self.titulo_tesis)

    def get_absolute_url(self):
        return reverse('licenciatura_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['dependencia', 'carrera', 'titulo_tesis']
        unique_together = ['carrera', 'usuario']


class Maestria(models.Model):
    programa = models.ForeignKey(ProgramaMaestria, on_delete=models.DO_NOTHING)
    descripcion = models.TextField(verbose_name='Descripición', blank=True)
    institucion = models.ForeignKey(Institucion, on_delete=models.DO_NOTHING)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.DO_NOTHING)
    titulo_tesis = models.CharField(max_length=255)
    tesis_doc = models.FileField(blank=True)
    tesis_url = models.URLField(blank=True)
    fecha_inicio = models.DateField('Fecha de inicio de maestría')
    fecha_fin = models.DateField('Fecha de terminación de maestría', blank=True, null=True)
    fecha_grado = models.DateField('Fecha de obtención de grado de maestría', blank=True, null=True)
    usuario = models.ForeignKey(User, related_name='maestrias', on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{}, {}, {}".format(self.programa.nombre, self.dependencia, self.titulo_tesis)

    def get_absolute_url(self):
        return reverse('maestria_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['dependencia', 'programa', 'titulo_tesis']
        unique_together = ['programa', 'usuario']


class Doctorado(models.Model):
    programa = models.ForeignKey(ProgramaDoctorado, on_delete=models.DO_NOTHING)
    descripcion = models.TextField(verbose_name='Descripición', blank=True)
    institucion = models.ForeignKey(Institucion, on_delete=models.DO_NOTHING)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.DO_NOTHING)
    titulo_tesis = models.CharField(max_length=255)
    tesis_doc = models.FileField(blank=True)
    tesis_url = models.URLField(blank=True)
    fecha_inicio = models.DateField('Fecha de inicio de doctorado')
    fecha_fin = models.DateField('Fecha de terminación de doctorado', blank=True, null=True)
    fecha_grado = models.DateField('Fecha de obtención de grado de doctorado', blank=True, null=True)
    usuario = models.ForeignKey(User, related_name='doctorados', on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{}, {}, {}".format(self.programa.nombre, self.dependencia,  self.titulo_tesis)

    def get_absolute_url(self):
        return reverse('doctorado_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['fecha_grado', 'dependencia', 'titulo_tesis']
        unique_together = ['programa', 'usuario']


class PostDoctorado(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(verbose_name='Descripición', blank=True)
    area_conocimiento = models.ForeignKey(AreaConocimiento, related_name='postdoctorado_area_conocimiento',
                                          verbose_name='Área de conocimiento', on_delete=models.DO_NOTHING)
    institucion = models.ForeignKey(Institucion, on_delete=models.DO_NOTHING)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.DO_NOTHING)
    proyecto = models.ForeignKey(ProyectoInvestigacion, on_delete=models.DO_NOTHING)
    fecha_inicio = models.DateField('Fecha de inicio de postdoctorado')
    fecha_fin = models.DateField('Fecha de terminación de postdoctorado', blank=True, null=True)
    usuario = models.ForeignKey(User, related_name='postdoctorados', on_delete=models.DO_NOTHING)
    # tags = models.ManyToManyField(Tag, related_name='post_doctorado_tags', blank=True)

    def __str__(self):
        return "{} : {} : {}".format(self.nombre, self.dependencia, self.area_conocimiento)

    def get_absolute_url(self):
        return reverse('postdoctorado_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['fecha_fin', 'dependencia']
        unique_together = ['nombre', 'usuario']
