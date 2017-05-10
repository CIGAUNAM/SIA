from django.db import models

from django.conf import settings
from autoslug import AutoSlugField
from django.core.urlresolvers import reverse
from nucleo.models import User, Tag, Pais, Estado, Ciudad, Institucion, Dependencia, Cargo, Proyecto, TipoDocumento, Revista, Indice, Libro, Editorial, Coleccion

STATUS_PUBLICACION = getattr(settings, 'STATUS_PUBLICACION', (('PUBLICADO', 'Publicado'), ('EN_PRENSA', 'En prensa'), ('ACEPTADO', 'Aceptado'), ('ENVIADO', 'Enviado'), ('OTRO', 'Otro')))

# Create your models here.

class ArticuloCientifico(models.Model):
    titulo = models.CharField(max_length=255, unique=True)
    #slug = AutoSlugField(populate_from='titulo', unique=True)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=16, choices=(('ARTICULO', 'Artículo'), ('ACTA', 'Acta'), ('CARTA', 'Carta'), ('RESENA', 'Reseña'), ('OTRO', 'Otro')))
    revista = models.ForeignKey(Revista)
    status = models.CharField(max_length=20, choices=STATUS_PUBLICACION)
    solo_electronico = models.BooleanField(default=False)
    usuarios = models.ManyToManyField(User, related_name='articulo_cientifico_autores', verbose_name='Autores')
    alumnos = models.ManyToManyField(User, related_name='articulo_cientifico_alumnos', blank=True)
    indices = models.ManyToManyField(Indice, related_name='articulo_cientifico_indices', blank=True)
    nombre_abreviado_wos = models.CharField(max_length=255, blank=True)
    url = models.URLField(blank=True)
    fecha = models.DateField(auto_now=False)
    volumen = models.CharField(max_length=100, blank=True)
    numero = models.CharField(max_length=100, blank=True)
    issn_impreso = models.CharField(max_length=40, blank=True, verbose_name='ISSN Impreso')
    issn_online = models.CharField(max_length=40, blank=True, verbose_name='ISSN Online')
    pagina_inicio = models.PositiveIntegerField()
    pagina_fin = models.PositiveIntegerField()
    id_doi = models.CharField(max_length=100, blank=True)
    id_wos = models.CharField(max_length=100, blank=True)
    proyectos = models.ManyToManyField(Proyecto, related_name='articulo_cientifico_proyectos')
    #usuario = models.ForeignKey(User)
    tags = models.ManyToManyField(Tag, related_name='articulo_cientifico_tags', blank=True)

    def __str__(self):
        return "{} : {} : {}".format(self.titulo, self.tipo.title(), self.revista)

    def get_absolute_url(self):
        return reverse('articulo_cientifico_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Artículo científico"
        verbose_name_plural = "Artículos científicos"
        ordering = ['fecha', 'titulo']


class CapituloLibroInvestigacion(models.Model):
    titulo = models.CharField(max_length=255, unique=True)
    #slug = AutoSlugField(populate_from='titulo', unique=True)
    descripcion = models.TextField(blank=True)
    libro = models.ForeignKey(Libro)
    #status = models.CharField(max_length=20, choices=STATUS_PUBLICACION)
    pagina_inicio = models.PositiveIntegerField()
    pagina_fin = models.PositiveIntegerField()
    proyectos = models.ManyToManyField(Proyecto, related_name='capitulo_libro_investigacion_proyectos', blank=True)
    usuario = models.ForeignKey(User, related_name='capitulo_libro_investigacion_usuario')
    tags = models.ManyToManyField(Tag, related_name='capitulo_libro_investigacion_tags', blank=True)

    def __str__(self):
        return "{} : {}".format(self.titulo, self.libro)

    def get_absolute_url(self):
        return reverse('capitulo_libro_investigacion_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Capítulo en libro"
        verbose_name_plural = "Capítulos en libros"
        ordering = ['titulo']


class MapaArbitrado(models.Model):
    titulo = models.CharField(max_length=255, unique=True)
    #slug = AutoSlugField(populate_from='titulo', unique=True)
    descripcion = models.TextField(blank=True)
    escala = models.CharField(max_length=30)
    usuarios = models.ManyToManyField(User, related_name='mapa_arbitrado_autores', verbose_name='Autores')
    editores = models.ManyToManyField(User, related_name='mapa_arbitrado_editores', blank=True)
    coordinadores = models.ManyToManyField(User, related_name='mapa_arbitrado_coordinadores', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_PUBLICACION)
    ciudad = models.ForeignKey(Ciudad)
    editorial = models.ForeignKey(Editorial)
    fecha = models.DateField(auto_now=False)
    numero_edicion = models.PositiveIntegerField(default=1)
    numero_paginas = models.PositiveIntegerField(default=1)
    coleccion = models.ForeignKey(Coleccion, blank=True, null=True)
    volumen = models.CharField(max_length=255, blank=True)
    isbn = models.SlugField(max_length=30, blank=True)
    url = models.URLField(blank=True)
    proyectos = models.ManyToManyField(Proyecto, related_name='mapa_arbitrado_proyectos')
    tags = models.ManyToManyField(Tag, related_name='mapa_arbitrado_tags', blank=True)

    def __str__(self):
        return "{} : ({}) : {}".format(self.titulo, self.escala, self.fecha)

    def get_absolute_url(self):
        return reverse('mapa_arbitrado_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Mapa arbitrado"
        verbose_name_plural = "Mapas arbitrados"
        ordering = ['fecha', 'titulo']



class InformeTecnico(models.Model):
    titulo = models.CharField(max_length=255, unique=True)
    #slug = AutoSlugField(populate_from='titulo', unique=True)
    descripcion = models.TextField(blank=True)
    usuarios = models.ManyToManyField(User, related_name='informe_tecnico_autores', verbose_name='Autores')
    fecha = models.DateField(auto_now=False)
    numero_paginas = models.PositiveIntegerField(default=1)
    proyectos = models.ManyToManyField(Proyecto, related_name='informe_tecnico_proyectos')
    url = models.URLField(blank=True)
    tags = models.ManyToManyField(Tag, related_name='informe_tecnico_tags', blank=True)

    def __str__(self):
        return "{} : {}".format(self.titulo, self.fecha)

    def get_absolute_url(self):
        return reverse('informe_tecnico__publico_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Informe técnico de acceso público"
        verbose_name_plural = "Informes técnicos de acceso público"
        ordering = ['fecha', 'titulo']
