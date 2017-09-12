from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
#from autoslug import AutoSlugField
from nucleo.models import User, Dependencia, Institucion, AreaConocimiento, ProgramaLicenciatura, ProgramaMaestria, ProgramaDoctorado, Proyecto

CURSO_ESPECIALIZACION_TIPO = getattr(settings, 'CURSO_ESPECIALIZACION_TIPO', (('', ''), ('', ''), ('CURSO', 'Curso'), ('DIPLOMADO', 'Diplomado'), ('CERTIFICACION', 'Certificación'), ('OTRO', 'Otro')))
CURSO_ESPECIALIZACION_MODALIDAD = getattr(settings, 'CURSO_ESPECIALIZACION_MODALIDAD', (('PRESENCIAL', 'Presencial'), ('EN_LINEA', 'En línea'), ('MIXTO', 'Mixto'), ('OTRO', 'Otro')))

#from django_stats2.mixins import StatsMixin
#from django_stats2.fields import StatField

from sia_stats.models import SIAYearModelCounter, SIAUserModelCounter
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
    institucion = models.ForeignKey(Institucion)
    dependencia = models.ForeignKey(Dependencia)
    usuario = models.ForeignKey(User, related_name='cursos_especializacion')
    #tags = models.ManyToManyField(Tag, related_name='curso_especializacion_tags', blank=True)



    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('curso_especializacion_detalle', kwargs={'pk': self.pk})


    def save(self, *args, **kwargs):
        old_horas = 0
        old_year = 0

        nuevo_item = None

        if self.pk is None:
            nuevo_item = True
        else:
            old_horas = CursoEspecializacion.objects.get(pk=self.pk).horas
            old_year = CursoEspecializacion.objects.get(pk=self.pk).fecha_inicio.year
            nuevo_item = False
        
        #guardar el nuevo elemento y despues de guardar hacer los calculos de horas
        super(CursoEspecializacion, self).save(*args, **kwargs)

        try:            
            year_data = SIAYearModelCounter.objects.get(year=self.fecha_inicio.year, model='CursoEspecializacion')

            # si el registro es nuevo
            if nuevo_item:
                year_data.counter = year_data.counter + self.horas
                year_data.save()
                year_data.users.add(self.usuario)

            # si el registro no es nuevo (si se está editando)
            else:
                # si el año no cambia
                if old_year == self.fecha_inicio.year:
                    year_data.counter = year_data.counter - old_horas + self.horas
                    year_data.save()
                # si el año cambia
                else:
                    # quitar las horas del año viejo
                    old_year_data = SIAYearModelCounter.objects.get(year=old_year, model='CursoEspecializacion')
                    old_year_data.counter = old_year_data.counter - old_horas
                    old_year_data.save()
                    # quitar usuario si no hay otros cursos en el mismo año
                    if User.objects.filter(cursos_especializacion__usuario=self.usuario, cursos_especializacion__fecha_inicio__year=old_year).count() == 0:
                        old_year_data.users.remove(self.usuario)
                    # poner horas nuevas al año nuevo
                    year_data.counter = year_data.counter + self.horas
                    year_data.save()
                    year_data.users.add(self.usuario)

        except SIAYearModelCounter.DoesNotExist:
            if nuevo_item:
                y = SIAYearModelCounter(model='CursoEspecializacion', year=self.fecha_inicio.year, counter=self.horas)
                y.save()
                y.users.add(self.usuario)
            else:
                # quitar horas del año viejo
                old_year_data = SIAYearModelCounter.objects.get(year=old_year, model='CursoEspecializacion')
                old_year_data.counter = old_year_data.counter - old_horas
                old_year_data.save()

                if User.objects.filter(cursos_especializacion__usuario=self.usuario, cursos_especializacion__fecha_inicio__year=old_year).count() == 0:
                    old_year_data.users.remove(self.usuario)

                y = SIAYearModelCounter(model='CursoEspecializacion', year=self.fecha_inicio.year, counter=self.horas)
                y.save()
                y.users.add(self.usuario)


    class Meta:
        ordering = ['fecha_inicio']
        verbose_name = 'Curso de especialización'
        verbose_name_plural = 'Cursos de especialización'
        unique_together = ['nombre', 'usuario', 'fecha_fin']



class Licenciatura(models.Model):
    carrera = models.ForeignKey(ProgramaLicenciatura)
    descripcion = models.TextField(verbose_name='Descripición', blank=True)
    institucion = models.ForeignKey(Institucion)
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
    institucion = models.ForeignKey(Institucion)
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
    institucion = models.ForeignKey(Institucion)
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
    institucion = models.ForeignKey(Institucion)
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