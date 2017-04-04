from django.db import models

from django.conf import settings
#from django.contrib.auth.models import User
from autoslug import AutoSlugField
from nucleo.models import User, Tag, Pais, Ciudad, Ubicacion, Proyecto, TipoEvento, Evento, Libro, Revista, Indice
from django.core.urlresolvers import reverse

EVENTO__AMBITO = getattr(settings, 'EVENTO__AMBITO', (('INSTITUCIONAL', 'Institucional'), ('REGIONAL', 'Regional'), ('NACIONAL', 'Nacional'), ('INTERNACIONAL', 'Internacional'), ('OTRO', 'Otro')))
EVENTO__RESPONSABILIDAD = getattr(settings, 'EVENTO__RESPONSABILIDAD', (('COORDINADOR', 'Coordinador general'), ('COMITE', 'Comité organizador'), ('AYUDANTE', 'Ayudante'), ('TECNICO', 'Apoyo técnico'), ('OTRO', 'Otro')))
STATUS_PUBLICACION = getattr(settings, 'STATUS_PUBLICACION', (('PUBLICADO', 'Publicado'), ('EN_PRENSA', 'En prensa'), ('ACEPTADO', 'Aceptado'), ('ENVIADO', 'Enviado'), ('OTRO', 'Otro')))

# Create your models here.

class ArticuloDivulgacion(models.Model):
    titulo = models.CharField(max_length=255, unique=True)
    documento_articulo = models.FileField(blank=True)
    #slug = AutoSlugField(populate_from='titulo', unique=True)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=16, choices=(('ARTICULO', 'Artículo'), ('ACTA', 'Acta'), ('CARTA', 'Carta'), ('RESENA', 'Reseña'), ('OTRO', 'Otro')))
    status = models.CharField(max_length=20, choices=STATUS_PUBLICACION)
    indizado = models.BooleanField(default=False)
    usuarios = models.ManyToManyField(User, related_name='articulo_divulgracion_autores', verbose_name='Autores')
    alumnos = models.ManyToManyField(User, related_name='articulo_divulgracion_alumnos', blank=True)
    indices = models.ManyToManyField(Indice, related_name='articulo_divulgracion_indices', blank=True)
    url = models.URLField(blank=True)
    solo_electronico = models.BooleanField(default=False)
    revista = models.ForeignKey(Revista)
    fecha = models.DateField(auto_now=False)
    volumen = models.CharField(max_length=100, blank=True)
    numero = models.CharField(max_length=100, blank=True)
    issn = models.CharField(max_length=30, blank=True)
    pagina_inicio = models.PositiveIntegerField()
    pagina_fin = models.PositiveIntegerField()
    id_doi = models.CharField(max_length=100, blank=True)
    proyectos = models.ManyToManyField(Proyecto, related_name='articulo_divulgracion_proyectos', blank=True)
    tags = models.ManyToManyField(Tag, related_name='articulo_divulgacion_tags', blank=True)

    def __str__(self):
        return "{} : {} : {}".format(self.titulo, self.tipo.title(), self.revista)

    def get_absolute_url(self):
        return reverse('articulo_divulgacion_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Artículo de divulgación"
        verbose_name_plural = "Artículos de divulgación"
        ordering = ['fecha', 'titulo']

"""
class LibroDivulgacion(models.Model):
    libro = models.ForeignKey(Libro)
    slug = AutoSlugField(populate_from='libro', unique=True)
    descripcion = models.TextField(blank=True)
    #status = models.CharField(max_length=20, choices=STATUS_PUBLICACION)
    proyectos = models.ManyToManyField(Proyecto, related_name='libro_divulgracion_proyectos', blank=True)
    tags = models.ManyToManyField(Tag, related_name='libro_divulgacion_tags', blank=True)

    def __str__(self):
        return str(self.libro)

    class Meta:
        verbose_name = "Libro de divulgación"
        verbose_name_plural = "Libro de divulgación"
        ordering = ['libro']
"""

class CapituloLibroDivulgacion(models.Model):
    titulo = models.CharField(max_length=255, unique=True)
    #slug = AutoSlugField(populate_from='titulo', unique=True)
    descripcion = models.TextField(blank=True)
    libro = models.ForeignKey(Libro)
    #status = models.CharField(max_length=20, choices=STATUS_PUBLICACION)
    pagina_inicio = models.PositiveIntegerField()
    pagina_fin = models.PositiveIntegerField()
    proyectos = models.ManyToManyField(Proyecto, related_name='capitulo_libro_divulgracion_proyectos', blank=True)
    usuario = models.ForeignKey(User)
    tags = models.ManyToManyField(Tag, related_name='capitulo_libro_divulgacion_tags', blank=True)

    def __str__(self):
        return "{} : {}".format(self.titulo, self.libro)

    def get_absolute_url(self):
        return reverse('capitulo_libro_divulgacion', kwargs={'pk': self.pk})

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
    tags = models.ManyToManyField(Tag, related_name='organizacion_evento_tags', blank=True)

    def __str__(self):
        return str(self.evento)

    def get_absolute_url(self):
        return reverse('organizacion_evento_divulgacion', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Organización de evento académico'
        verbose_name_plural= 'Organización de eventos académicos'


class ParticipacionEventoDivulgacion(models.Model):
    titulo = models.CharField(max_length=255)
    #slug = AutoSlugField(populate_from='titulo', unique=True)
    descripcion = models.TextField(blank=True)
    evento = models.ForeignKey(Evento)
    resumen_publicado = models.BooleanField(default=False)
    autores = models.ManyToManyField(User, related_name='participacion_evento_autores')
    ambito = models.CharField(max_length=20, choices=EVENTO__AMBITO)
    por_invitacion = models.BooleanField(default=False)
    ponencia_magistral = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, related_name='participacion_evento_tags', blank=True)

    def __str__(self):
        return "{} : {}".format(self.titulo, self.evento)

    def get_absolute_url(self):
        return reverse('participacion_evento_divulgacion', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Participación en evento académico'
        verbose_name_plural= 'Participación en eventos académicos'


class MedioDivulgacion(models.Model):
    nombre_medio = models.CharField(max_length=255, unique=True)
    #slug = AutoSlugField(populate_from='nombre_medio', unique=True)
    descripcion = models.TextField(blank=True)
    canal = models.CharField(max_length=255)
    ubicacion = models.ForeignKey(Ubicacion)
    tags = models.ManyToManyField(Tag, related_name='medio_divulgacion_tags', blank=True)

    def __str__(self):
        return self.nombre_medio

    def get_absolute_url(self):
        return reverse('medio_divulgacion', kwargs={'pk': self.pk})

    class Meta:
        unique_together = ['canal', 'nombre_medio']
        ordering = ['nombre_medio']
        verbose_name = "Medio de difusión para divulgación"
        verbose_name_plural = "Medios de difusión para divulgación"


class ProgramaRadioTelevisionInternet(models.Model):
    fecha = models.DateField()
    tema = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    actividad = models.CharField(max_length=20, choices=(('PRODUCCION', 'Producciòn'), ('PARTICIPACION', 'Participaciòn'), ('ENTREVISTA', 'Entrevista'), ('OTRA', 'Otra')))
    medio = models.CharField(max_length=20, choices=(('PERIODICO', 'Periódico'), ('RADIO', 'Radio'), ('TV', 'Televisión'), ('INTERNET', 'Internet'), ('OTRO', 'Otro')))
    nombre_medio = models.ForeignKey(MedioDivulgacion)
    partiticipantes = models.ManyToManyField(User, related_name='programa_radio_television_internet_participantes')
    tags = models.ManyToManyField(Tag, related_name='programa_radio_television_internet_tags', blank=True)

    def __str__(self):
        return "{} : {} : {}".format(self.nombre_medio, self.tema, self.fecha)

    def get_absolute_url(self):
        return reverse('programa_radio_television_internet', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['fecha', 'tema']
        verbose_name = 'Programa de radio, televisión o internet'
        verbose_name_plural = 'Programas de radio, televisión o internet'


