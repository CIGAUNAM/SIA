from django.db import models

from django.conf import settings
#from autoslug import AutoSlugField
from nucleo.models import User, Pais, Estado, Ciudad, Proyecto, TipoEvento, Evento, Libro, Revista, Indice
from django.core.urlresolvers import reverse

EVENTO__AMBITO = getattr(settings, 'EVENTO__AMBITO', (('INSTITUCIONAL', 'Institucional'), ('REGIONAL', 'Regional'), ('NACIONAL', 'Nacional'), ('INTERNACIONAL', 'Internacional'), ('OTRO', 'Otro')))
EVENTO__RESPONSABILIDAD = getattr(settings, 'EVENTO__RESPONSABILIDAD', (('COORDINADOR', 'Coordinador general'), ('COMITE', 'Comité organizador'), ('AYUDANTE', 'Ayudante'), ('TECNICO', 'Apoyo técnico'), ('OTRO', 'Otro')))
RESENA__TIPO = getattr(settings, 'RESENA__TIPO', (('LIBRO', 'Libro'), ('REVISTA', 'Revista')))

# Create your models here.


class MemoriaInExtenso(models.Model):
    nombre = models.CharField(max_length=255, unique=True, verbose_name='Título de memoria in extenso')
    #slug = AutoSlugField(populate_from='titulo', unique=True)
    descripcion = models.TextField(blank=True)
    pais = models.ForeignKey(Pais)
    estado = models.ForeignKey(Estado)
    ciudad = models.ForeignKey(Ciudad)
    fecha = models.DateField()
    evento = models.ForeignKey(Evento)
    usuarios = models.ManyToManyField(User, related_name='memoria_in_extenso_autores_externos', verbose_name='Autores')
    editores = models.ManyToManyField(User, related_name='memoria_in_extenso_editores', blank=True)
    indices = models.ManyToManyField(Indice, related_name='memoria_in_extenso_indices', blank=True)
    agradecimientos = models.ManyToManyField(User, related_name='memoria_in_extenso_agradecimientos', blank=True)
    #pais_origen = models.ForeignKey(Pais)
    pagina_inicio = models.PositiveIntegerField()
    pagina_fin = models.PositiveIntegerField()
    issn = models.SlugField(max_length=20, blank=True)
    proyecto = models.ForeignKey(Proyecto, blank=True, null=True)
    #proyectos = models.ManyToManyField(Proyecto, blank=True)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.nombre
    
    def get_absolute_url(self):
        return reverse('memoria_in_extenso_detalle', kwargs={'pk': self.pk})
    
    class Meta:
        verbose_name = 'Memoria in extenso'
        verbose_name_plural = 'Memorias in extenso'


class PrologoLibro(models.Model):
    descripcion = models.TextField(blank=True)
    libro = models.ForeignKey(Libro, related_name='prologo_libro_libro')
    pagina_inicio = models.PositiveIntegerField()
    pagina_fin = models.PositiveIntegerField()
    url = models.URLField(blank=True)
    usuario = models.ForeignKey(User)
    #tags = models.ManyToManyField(Tag, related_name='prologo_libro_tags', blank=True)

    def __str__(self):
        return '{} : {}'.format(self.usuario, self.libro)

    def get_absolute_url(self):
        return reverse('prologo_libro_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Prólogo de libro'
        verbose_name_plural = 'Prólogos de libros'
        unique_together = ['usuario', 'libro']


class Resena(models.Model):
    titulo = models.CharField(max_length=255, unique=True)
    tipo = models.CharField(max_length=10, choices=RESENA__TIPO)
    libro_resenado = models.ForeignKey(Libro, blank=True, null=True, related_name='resena_libro_resenado')
    revista_resenada = models.ForeignKey(Revista, blank=True, null=True, related_name='resena_revista_resenada')
    #slug = AutoSlugField(populate_from='titulo_resena', unique=True)
    descripcion = models.TextField(blank=True)
    #libro_publica = models.ForeignKey(Libro, related_name='resena_libro_publica', blank=True, null=True)
    revista_publica = models.ForeignKey(Revista, related_name='resena_revista_publica')
    pagina_inicio = models.PositiveIntegerField()
    pagina_fin = models.PositiveIntegerField()
    url = models.URLField(blank=True)
    usuario = models.ForeignKey(User)
    #tags = models.ManyToManyField(Tag, related_name='resena_tags', blank=True)

    def __str__(self):
        return '{} : {}'.format(self.usuario, self.titulo)

    def get_absolute_url(self):
        return reverse('resena_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Reseña de libro'
        verbose_name_plural = 'Reseñas de libros'


class OrganizacionEventoAcademico(models.Model):
    evento = models.ForeignKey(Evento)
    descripcion = models.TextField(blank=True)
    responsabilidad = models.CharField(max_length=30, choices=EVENTO__RESPONSABILIDAD)
    numero_ponentes = models.PositiveIntegerField()
    numero_asistentes = models.PositiveIntegerField()
    ambito = models.CharField(max_length=20, choices=EVENTO__AMBITO)
    usuario = models.ForeignKey(User)
    #tags = models.ManyToManyField(Tag, related_name='organizacion_evento_academico_tags', blank=True)

    def __str__(self):
        return str(self.evento)

    def get_absolute_url(self):
        return reverse('organizacion_evento_academico_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Organización de evento académico'
        verbose_name_plural= 'Organización de eventos académicos'


class ParticipacionEventoAcademico(models.Model):
    titulo = models.CharField(max_length=255)
    #slug = AutoSlugField(populate_from='titulo', unique=True)
    descripcion = models.TextField(blank=True)
    evento = models.ForeignKey(Evento)
    #autores = models.ManyToManyField(User, related_name='participacion_evento_academico_autores')
    ambito = models.CharField(max_length=20, choices=EVENTO__AMBITO)
    resumen_publicado = models.BooleanField(default=False)
    por_invitacion = models.BooleanField(default=False)
    ponencia_magistral = models.BooleanField(default=False)
    usuario = models.ForeignKey(User)
    #tags = models.ManyToManyField(Tag, related_name='participacion_evento_academico_tags', blank=True)

    def __str__(self):
        return "{} : {}".format(self.titulo, self.evento)

    def get_absolute_url(self):
        return reverse('participacion_evento_academico_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Participación en evento académico'
        verbose_name_plural= 'Participación en eventos académicos'

