from django.db import models
from django.conf import settings
from django.urls import reverse
from nucleo.models import User, Dependencia, Institucion, InstitucionSimple, AreaConocimiento, ProgramaLicenciatura, ProgramaMaestria, ProgramaDoctorado
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
    tipo = models.CharField(max_length=20, choices=CURSO_ESPECIALIZACION_TIPO, verbose_name='Tipo de curso')
    horas = models.PositiveIntegerField(verbose_name='Número de horas')
    fecha_inicio = models.DateField('Fecha de inicio')
    fecha_fin = models.DateField('Fecha de finalización', blank=True, null=True)
    modalidad = models.CharField(max_length=20, choices=CURSO_ESPECIALIZACION_MODALIDAD)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.DO_NOTHING, null=True, blank=True)
    institucion = models.ForeignKey(InstitucionSimple, on_delete=models.DO_NOTHING, null=True, blank=True)
    usuario = models.ForeignKey(User, related_name='cursos_especializacion', on_delete=models.DO_NOTHING)

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
    titulo_obtenido = models.CharField(max_length=255)
    carrera = models.ForeignKey(ProgramaLicenciatura, on_delete=models.DO_NOTHING, null=True, blank=True)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.DO_NOTHING, null=True, blank=True)
    institucion = models.ForeignKey(InstitucionSimple, on_delete=models.DO_NOTHING, null=True, blank=True)
    titulo_tesis = models.CharField(max_length=255)
    #fecha_inicio = models.DateField('Fecha de inicio de licenciatura')
    #fecha_fin = models.DateField('Fecha de terminación de licenciatura')
    fecha_grado = models.DateField('Fecha de obtención de grado de licenciatura')
    distincion_obtenida = models.CharField(max_length=255, null=True, blank=True)
    usuario = models.ForeignKey(User, related_name='licenciaturas', on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{}, {}, {}".format(str(self.carrera.nombre), self.dependencia, self.titulo_tesis)

    def get_absolute_url(self):
        return reverse('licenciatura_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['titulo_obtenido', 'titulo_tesis']
        unique_together = ['titulo_obtenido', 'usuario']




class Maestria(models.Model):
    titulo_obtenido = models.CharField(max_length=255)
    programa = models.ForeignKey(ProgramaMaestria, on_delete=models.DO_NOTHING, null=True, blank=True)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.DO_NOTHING, null=True, blank=True)
    institucion = models.ForeignKey(InstitucionSimple, on_delete=models.DO_NOTHING, null=True, blank=True)
    titulo_tesis = models.CharField(max_length=255)
    #tesis_doc = models.FileField(blank=True)
    #tesis_url = models.URLField(blank=True)
    #fecha_inicio = models.DateField('Fecha de inicio de maestría')
    #fecha_fin = models.DateField('Fecha de terminación de maestría', blank=True, null=True)
    fecha_grado = models.DateField('Fecha de obtención de grado de maestría', blank=True, null=True)
    distincion_obtenida = models.CharField(max_length=255, null=True, blank=True)
    usuario = models.ForeignKey(User, related_name='maestrias', on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{}, {}, {}".format(self.programa.nombre, self.dependencia, self.titulo_tesis)

    def get_absolute_url(self):
        return reverse('maestria_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['titulo_obtenido', 'titulo_tesis']
        unique_together = ['titulo_obtenido', 'usuario']


class Doctorado(models.Model):
    titulo_obtenido = models.CharField(max_length=255)
    programa = models.ForeignKey(ProgramaDoctorado, on_delete=models.DO_NOTHING, null=True, blank=True)
    #descripcion = models.TextField(verbose_name='Descripición', blank=True)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.DO_NOTHING)
    institucion = models.ForeignKey(InstitucionSimple, on_delete=models.DO_NOTHING, null=True, blank=True)
    titulo_tesis = models.CharField(max_length=255)
    #tesis_doc = models.FileField(blank=True)
    #tesis_url = models.URLField(blank=True)
    #fecha_inicio = models.DateField('Fecha de inicio de doctorado')
    #fecha_fin = models.DateField('Fecha de terminación de doctorado', blank=True, null=True)
    fecha_grado = models.DateField('Fecha de obtención de grado de doctorado', blank=True, null=True)
    distincion_obtenida = models.CharField(max_length=255, null=True, blank=True)
    usuario = models.ForeignKey(User, related_name='doctorados', on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{}, {}, {}".format(self.programa.nombre, self.dependencia,  self.titulo_tesis)

    def get_absolute_url(self):
        return reverse('doctorado_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['fecha_grado', 'dependencia', 'titulo_tesis']
        unique_together = ['programa', 'usuario']



class PostDoctorado(models.Model):
    titulo_proyecto = models.CharField(max_length=255)
    tutor = models.ForeignKey(User, related_name='postdoctorado_tutor', on_delete=models.DO_NOTHING)

    #descripcion = models.TextField(verbose_name='Descripición', blank=True)
    #area_conocimiento = models.ForeignKey(AreaConocimiento, related_name='postdoctorado_area_conocimiento', verbose_name='Área de conocimiento', on_delete=models.DO_NOTHING)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.DO_NOTHING, blank=True, null=True)
    institucion = models.ForeignKey(InstitucionSimple, on_delete=models.DO_NOTHING, null=True, blank=True)
    proyecto = models.ForeignKey(ProyectoInvestigacion, on_delete=models.DO_NOTHING, blank=True, null=True)
    entidad_financiamiento = models.CharField(max_length=20, blank=True, null=True, choices=(('', '-------'), ('CONACYT', 'CONACYT'), ('SRE', 'SRE'), ('DGAPA', 'DGAPA'), ('OTRA', 'Otra')))
    otra_entidad_financiamiento = models.CharField(max_length=160, blank=True, null=True)
    fecha_inicio = models.DateField('Fecha de inicio de postdoctorado')
    fecha_fin = models.DateField('Fecha de terminación de postdoctorado')
    usuario = models.ForeignKey(User, related_name='postdoctorado_usuario', on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{} : {} : {}".format(self.titulo_proyecto, self.dependencia, self.area_conocimiento)

    def get_absolute_url(self):
        return reverse('postdoctorado_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['fecha_fin', ]
        unique_together = ['titulo_proyecto', 'usuario']
