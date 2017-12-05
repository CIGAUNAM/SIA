from django.db import models

from django.conf import settings
# from django.contrib.auth.models import User
from autoslug import AutoSlugField
from nucleo.models import User, Pais, Ciudad, TipoEvento, Evento, Libro, Revista, Indice, MedioDivulgacion, Financiamiento
from investigacion.models import ProyectoInvestigacion
from django.core.urlresolvers import reverse
from sortedm2m.fields import SortedManyToManyField

EVENTO__AMBITO = getattr(settings, 'EVENTO__AMBITO', (
    ('INSTITUCIONAL', 'Institucional'), ('REGIONAL', 'Regional'), ('NACIONAL', 'Nacional'),
    ('INTERNACIONAL', 'Internacional'), ('OTRO', 'Otro')))
EVENTO__RESPONSABILIDAD = getattr(settings, 'EVENTO__RESPONSABILIDAD', (
    ('COORDINADOR', 'Coordinador general'), ('COMITE', 'Comité organizador'), ('AYUDANTE', 'Ayudante'),
    ('TECNICO', 'Apoyo técnico'), ('OTRO', 'Otro')))
STATUS_PUBLICACION = getattr(settings, 'STATUS_PUBLICACION', (
    ('PUBLICADO', 'Publicado'), ('EN_PRENSA', 'En prensa'), ('ACEPTADO', 'Aceptado'), ('ENVIADO', 'Enviado'),
    ('OTRO', 'Otro')))


# Create your models here.

class ArticuloDivulgacion(models.Model):
    titulo = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=16, choices=(('', '-------'), ('ARTICULO', 'Artículo'), ('ACTA', 'Acta'), ('CARTA', 'Carta'), ('RESENA', 'Reseña'), ('OTRO', 'Otro')))
    status = models.CharField(max_length=20, choices=STATUS_PUBLICACION)
    indizado = models.BooleanField(default=False)
    usuarios = SortedManyToManyField(User, related_name='articulo_divulgacion_autores', verbose_name='Autores')
    alumnos = models.ManyToManyField(User, related_name='articulo_divulgacion_alumnos', blank=True)
    indices = models.ManyToManyField(Indice, related_name='articulo_divulgacion_indices', blank=True)
    url = models.URLField(blank=True)
    solo_electronico = models.BooleanField(default=False)
    revista = models.ForeignKey(Revista)
    fecha = models.DateField()
    volumen = models.CharField(max_length=100, blank=True)
    numero = models.CharField(max_length=100, blank=True)
    issn = models.CharField(max_length=30, blank=True)
    pagina_inicio = models.PositiveIntegerField()
    pagina_fin = models.PositiveIntegerField()
    id_doi = models.CharField(max_length=100, blank=True)
    proyecto = models.ForeignKey(ProyectoInvestigacion, blank=True, null=True)

    def __str__(self):
        return "{} : {} : {}".format(self.titulo, self.tipo.title(), self.revista)

    def get_absolute_url(self):
        return reverse('articulo_divulgacion_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Artículo de divulgación"
        verbose_name_plural = "Artículos de divulgación"
        ordering = ['fecha', 'titulo']



class CapituloLibroDivulgacion(models.Model):
    titulo = models.CharField(max_length=255, unique=True)

    descripcion = models.TextField(blank=True)
    libro = models.ForeignKey(Libro)

    pagina_inicio = models.PositiveIntegerField()
    pagina_fin = models.PositiveIntegerField()
    proyecto = models.ForeignKey(ProyectoInvestigacion, blank=True, null=True)
    # proyectos = models.ManyToManyField(Proyecto, related_name='capitulo_libro_divulgracion_proyectos', blank=True)
    usuario = models.ForeignKey(User)

    # tags = models.ManyToManyField(Tag, related_name='capitulo_libro_divulgacion_tags', blank=True)

    def __str__(self):
        return "{} : {}".format(self.titulo, self.libro)

    def get_absolute_url(self):
        return reverse('capitulo_libro_divulgacion_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Capítulo en libro de divulgación"
        verbose_name_plural = "Capítulos en libros de divulgración"
        ordering = ['titulo']
        unique_together = ['titulo', 'libro', 'usuario']


class OrganizacionEventoDivulgacion(models.Model):
    evento = models.ForeignKey(Evento)
    descripcion = models.TextField(blank=True)
    responsabilidad = models.CharField(max_length=30, choices=EVENTO__RESPONSABILIDAD)
    numero_ponentes = models.PositiveIntegerField()
    numero_asistentes = models.PositiveIntegerField()
    ambito = models.CharField(max_length=20, choices=EVENTO__AMBITO)
    financiamiento = models.ForeignKey(Financiamiento, blank=True, null=True)
    usuario = models.ForeignKey(User)

    # tags = models.ManyToManyField(Tag, related_name='organizacion_evento_tags', blank=True)

    def __str__(self):
        return str(self.evento)

    def get_absolute_url(self):
        return reverse('organizacion_evento_divulgacion_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Organización de evento académico'
        verbose_name_plural = 'Organización de eventos académicos'


class ParticipacionEventoDivulgacion(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    evento = models.ForeignKey(Evento)
    resumen_publicado = models.BooleanField(default=False)
    ambito = models.CharField(max_length=20, choices=EVENTO__AMBITO)
    por_invitacion = models.BooleanField(default=False)
    ponencia_magistral = models.BooleanField(default=False)
    usuario = models.ForeignKey(User)

    # tags = models.ManyToManyField(Tag, related_name='participacion_evento_tags', blank=True)

    def __str__(self):
        return "{} : {}".format(self.titulo, self.evento)

    def get_absolute_url(self):
        return reverse('participacion_evento_divulgacion_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Participación en evento académico'
        verbose_name_plural = 'Participación en eventos académicos'


class ProgramaRadioTelevisionInternet(models.Model):
    tema = models.CharField(max_length=255)
    fecha = models.DateField()
    descripcion = models.TextField(blank=True)
    actividad = models.CharField(max_length=20, choices=(
        ('PRODUCCION', 'Producciòn'), ('PARTICIPACION', 'Participaciòn'), ('ENTREVISTA', 'Entrevista'),
        ('OTRA', 'Otra')))
    medio_divulgacion = models.ForeignKey(MedioDivulgacion)
    usuario = models.ForeignKey(User)

    def __str__(self):
        return "{} : {} : {}".format(self.nombre_medio, self.tema, self.fecha)

    def get_absolute_url(self):
        return reverse('programa_radio_television_internet_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['fecha', 'tema']
        verbose_name = 'Programa de radio, televisión o internet'
        verbose_name_plural = 'Programas de radio, televisión o internet'


