from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
#from autoslug import AutoSlugField
from nucleo.models import User, Dependencia, AreaConocimiento, ProgramaLicenciatura, ProgramaMaestria, ProgramaDoctorado, Proyecto

CURSO_ESPECIALIZACION_TIPO = getattr(settings, 'CURSO_ESPECIALIZACION_TIPO', (('', ''), ('', ''), ('CURSO', 'Curso'), ('DIPLOMADO', 'Diplomado'), ('CERTIFICACION', 'Certificación'), ('OTRO', 'Otro')))
CURSO_ESPECIALIZACION_MODALIDAD = getattr(settings, 'CURSO_ESPECIALIZACION_MODALIDAD', (('PRESENCIAL', 'Presencial'), ('EN_LINEA', 'En línea'), ('MIXTO', 'Mixto'), ('OTRO', 'Otro')))

# Create your models here.




class CursoEspecializacion(models.Model):
    nombre = models.CharField(max_length=255, verbose_name='Nombre del curso', help_text='Nombre del curso texto de ayuda')
    #slug = AutoSlugField(populate_from='nombre', max_length=150, unique=True)
    descripcion = models.TextField(verbose_name='Descripción', blank=True)
    tipo = models.CharField(max_length=20, choices=CURSO_ESPECIALIZACION_TIPO, verbose_name='Tipo de curso')
    horas = models.PositiveIntegerField(verbose_name='Número de horas')
    fecha_inicio = models.DateField('Fecha de inicio')
    fecha_fin = models.DateField('Fecha de finalización', blank=True, null=True)
    modalidad = models.CharField(max_length=20, choices=CURSO_ESPECIALIZACION_MODALIDAD)
    area_conocimiento = models.ForeignKey(AreaConocimiento, verbose_name='Área de conocimiento')
    dependencia = models.ForeignKey(Dependencia)
    usuario = models.ForeignKey(User, related_name='cursos_especializacion')
    #tags = models.ManyToManyField(Tag, related_name='curso_especializacion_tags', blank=True)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('curso_especializacion_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['fecha_inicio']
        verbose_name = 'Curso de especialización'
        verbose_name_plural = 'Cursos de especialización'
        unique_together = ['nombre', 'usuario', 'fecha_fin']



class Licenciatura(models.Model):
    carrera = models.ForeignKey(ProgramaLicenciatura)
    descripcion = models.TextField(verbose_name='Descripición', blank=True)
    dependencia = models.ForeignKey(Dependencia)
    titulo_tesis = models.CharField(max_length=255)
    #slug = AutoSlugField(populate_from='titulo_tesis', unique=True)
    #tesis_doc = models.FileField(blank=True)
    tesis_url = models.URLField(blank=True)
    fecha_inicio = models.DateField('Fecha de inicio de licenciatura')
    fecha_fin = models.DateField('Fecha de terminación de licenciatura')
    fecha_grado = models.DateField('Fecha de obtención de grado de licenciatura')
    usuario = models.ForeignKey(User, related_name='licenciaturas')
    #tags = models.ManyToManyField(Tag, related_name='licenciatura_tags', blank=True)

    def __str__(self):
        return "{} : {} : {}".format(self.dependencia, str(self.carrera.nombre), self.titulo_tesis)

    def get_absolute_url(self):
        return reverse('licenciatura_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['dependencia', 'carrera', 'titulo_tesis']
        unique_together = ['carrera', 'usuario']


class Maestria(models.Model):
    programa = models.ForeignKey(ProgramaMaestria)
    descripcion = models.TextField(verbose_name='Descripición', blank=True)
    dependencia = models.ForeignKey(Dependencia)
    titulo_tesis = models.CharField(max_length=255)
    #slug = AutoSlugField(populate_from='titulo_tesis', unique=True)
    tesis_doc = models.FileField(blank=True)
    tesis_url = models.URLField(blank=True)
    fecha_inicio = models.DateField('Fecha de inicio de maestría')
    fecha_fin = models.DateField('Fecha de terminación de maestría', blank=True, null=True)
    fecha_grado = models.DateField('Fecha de obtención de grado de maestría', blank=True, null=True)
    usuario = models.ForeignKey(User, related_name='maestrias')
    #tags = models.ManyToManyField(Tag, related_name='maestria_tags', blank=True)

    def __str__(self):
        return "{} : {} : {}".format(self.dependencia, self.programa.nombre, self.titulo_tesis)

    def get_absolute_url(self):
        return reverse('maestria_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['dependencia', 'programa', 'titulo_tesis']
        unique_together = ['programa', 'usuario']


class Doctorado(models.Model):
    programa = models.ForeignKey(ProgramaDoctorado)
    descripcion = models.TextField(verbose_name='Descripición', blank=True)
    dependencia = models.ForeignKey(Dependencia)
    titulo_tesis = models.CharField(max_length=255)
    #slug = AutoSlugField(populate_from='titulo_tesis', unique=True)
    tesis_doc = models.FileField(blank=True)
    tesis_url = models.URLField(blank=True)
    fecha_inicio = models.DateField('Fecha de inicio de doctorado')
    fecha_fin = models.DateField('Fecha de terminación de doctorado', blank=True, null=True)
    fecha_grado = models.DateField('Fecha de obtención de grado de doctorado', blank=True, null=True)
    usuario = models.ForeignKey(User, related_name='doctorados')
    #tags = models.ManyToManyField(Tag, related_name='doctorado_tags', blank=True)

    def __str__(self):
        return "{} : {} : {}".format(self.dependencia, self.programa.nombre, self.titulo_tesis)

    def get_absolute_url(self):
        return reverse('doctorado_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['fecha_grado', 'dependencia', 'titulo_tesis']
        unique_together = ['programa', 'usuario']


proyectos = [
    ('Ninguno', 1900, 1, 1, 2900, 1, 1, 'OTRO', 'OTRO', 'INDIVIDUAL', 'OTRO', )
]


class PostDoctorado(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(verbose_name='Descripición', blank=True)
    area_conocimiento = models.ForeignKey(AreaConocimiento, related_name='postdoctorado_area_conocimiento', verbose_name='Área de conocimiento')
    dependencia = models.ForeignKey(Dependencia)
    proyecto = models.ForeignKey(Proyecto)
    fecha_inicio = models.DateField('Fecha de inicio de postdoctorado')
    fecha_fin = models.DateField('Fecha de terminación de postdoctorado', blank=True, null=True)
    usuario = models.ForeignKey(User, related_name='postdoctorados')
    #tags = models.ManyToManyField(Tag, related_name='post_doctorado_tags', blank=True)

    def __str__(self):
        return "{} : {} : {}".format(self.nombre, self.dependencia, self.area_conocimiento)

    def get_absolute_url(self):
        return reverse('postdoctorado_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['fecha_fin', 'dependencia']
        unique_together = ['nombre', 'usuario']