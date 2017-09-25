from django.db import models

from django.conf import settings
from autoslug import AutoSlugField
from django.core.urlresolvers import reverse
#from table.tests.test_utils import Article

from nucleo.models import User, Pais, Estado, Ciudad, Institucion, Dependencia, Cargo, Proyecto, Revista, Indice, Libro, Editorial, Coleccion
from sortedm2m.fields import SortedManyToManyField
from sia_stats.models import SIAYearModelCounter


STATUS_PUBLICACION = getattr(settings, 'STATUS_PUBLICACION', (('PUBLICADO', 'Publicado'), ('EN_PRENSA', 'En prensa'), ('ACEPTADO', 'Aceptado'), ('ENVIADO', 'Enviado'), ('OTRO', 'Otro')))

# Create your models here.


class ArticuloCientifico(models.Model):
    titulo = models.CharField(max_length=255, unique=True)
    # slug = AutoSlugField(populate_from='titulo', unique=True)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=16, choices=(('ARTICULO', 'Artículo'), ('ACTA', 'Acta'), ('CARTA', 'Carta'), ('RESENA', 'Reseña'), ('OTRO', 'Otro')))
    revista = models.ForeignKey(Revista)
    volumen = models.CharField(max_length=100, null=True, blank=True)
    numero = models.CharField(max_length=100, null=True, blank=True)
    fecha = models.DateField(auto_now=False)
    issn_impreso = models.CharField(max_length=40, blank=True, verbose_name='ISSN Impreso')
    issn_online = models.CharField(max_length=40, blank=True, verbose_name='ISSN Online')
    status = models.CharField(max_length=20, choices=STATUS_PUBLICACION)
    solo_electronico = models.BooleanField(default=False)
    usuarios = SortedManyToManyField(User, related_name='articulo_cientifico_autores', verbose_name='Autores')
    alumnos = models.ManyToManyField(User, related_name='articulo_cientifico_alumnos', blank=True)
    indices = models.ManyToManyField(Indice, related_name='articulo_cientifico_indices', blank=True)
    #nombre_abreviado_wos = models.CharField(max_length=255, blank=True)
    url = models.URLField(blank=True)
    pagina_inicio = models.PositiveIntegerField()
    pagina_fin = models.PositiveIntegerField()
    id_doi = models.CharField(max_length=100, null=True, blank=True)
    id_wos = models.CharField(max_length=100, null=True, blank=True)
    proyecto = models.ForeignKey(Proyecto, blank=True, null=True)

    def __str__(self):
        return "{} : {} : {}".format(self.titulo, self.tipo.title(), self.revista)

    def get_absolute_url(self):
        return reverse('articulo_cientifico_detalle', kwargs={'pk': self.pk})

    def save1(self, *args, **kwargs):
        nuevo_item = None

        if self.pk is None:
            nuevo_item = True
        else:
            old_year = self.objects.get(pk=self.pk).fecha.year
            nuevo_item = False

        # guardar el nuevo elemento y despues de guardar hacer los calculos de horas
        super(ArticuloCientifico, self).save(*args, **kwargs)

        try:
            year_data = SIAYearModelCounter.objects.get(year=self.fecha.year, model='ArticuloCientifico')
            # si el registro es nuevo
            if nuevo_item:
                year_data.counter = year_data.counter + 1
                year_data.save()
                for user in self.usuarios:
                    year_data.users.add(self.user)
            # si el registro no es nuevo (si se está editando)
            else:
                # si el año cambia
                if old_year != self.fecha.year:
                    # quitar el curso del año viejo
                    old_year_data = SIAYearModelCounter.objects.get(year=old_year, model='ArticuloCientifico')
                    old_year_data.counter = old_year_data.counter - 1
                    old_year_data.save()
                    # quitar usuario si no hay otros cursos en el mismo año
                    if User.objects.filter(articulo_cientifico_autores__usuarios=self.usuario,
                                           cursos_especializacion__fecha_inicio__year=old_year).count() == 0:
                        old_year_data.users.remove(self.usuario)
                    # poner horas nuevas al año nuevo
                    year_data.counter = year_data.counter + self.horas
                    year_data.save()
                    year_data.users.add(self.usuario)
        except SIAYearModelCounter.DoesNotExist:
            if nuevo_item:
                y = SIAYearModelCounter(model='ArticuloCientifico', year=self.fecha.year, counter=self.horas)
                y.save()
                y.users.add(self.usuario)
            else:
                # quitar horas del año viejo
                old_year_data = SIAYearModelCounter.objects.get(year=old_year, model='ArticuloCientifico')
                old_year_data.counter = old_year_data.counter - 1
                old_year_data.save()
                if User.objects.filter(cursos_especializacion__usuario=self.usuario,
                                       cursos_especializacion__fecha_inicio__year=old_year).count() == 0:
                    old_year_data.users.remove(self.usuario)
                y = SIAYearModelCounter(model='CursoEspecializacion', year=self.fecha.year, counter=self.horas)
                y.save()
                y.users.add(self.usuario)

    def delete1(self, *args, **kwargs):
        year_data = SIAYearModelCounter.objects.get(year=self.fecha.year, model='ArticuloCientifico')
        year_data.counter = year_data.counter - 1
        year_data.save()
        print(self.usuarios)
        super(ArticuloCientifico, self).delete(*args, **kwargs)
        for usuario in self.usuarios:
            if User.objects.filter(articulo_cientifico_autores__usuarios=usuario, articulo_cientifico__fecha__year=self.fecha.year).count() == 0:
                year_data.users.remove(usuario)

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
    proyecto = models.ForeignKey(Proyecto, blank=True, null=True)
    #proyectos = models.ManyToManyField(Proyecto, related_name='capitulo_libro_investigacion_proyectos', blank=True)
    usuario = models.ForeignKey(User, related_name='capitulo_libro_investigacion_usuario')
    #tags = models.ManyToManyField(Tag, related_name='capitulo_libro_investigacion_tags', blank=True)

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
    usuarios = SortedManyToManyField(User, related_name='mapa_arbitrado_autores', verbose_name='Autores')
    editores = models.ManyToManyField(User, related_name='mapa_arbitrado_editores', blank=True)
    coordinadores = models.ManyToManyField(User, related_name='mapa_arbitrado_coordinadores', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_PUBLICACION)
    pais = models.ForeignKey(Pais)
    estado = models.ForeignKey(Estado)
    ciudad = models.ForeignKey(Ciudad)
    editorial = models.ForeignKey(Editorial)
    fecha = models.DateField(auto_now=False)
    numero_edicion = models.PositiveIntegerField(default=1)
    numero_paginas = models.PositiveIntegerField(default=1)
    coleccion = models.ForeignKey(Coleccion, blank=True, null=True)
    volumen = models.CharField(max_length=255, blank=True)
    isbn = models.SlugField(max_length=30, blank=True)
    url = models.URLField(blank=True)
    proyecto = models.ForeignKey(Proyecto, blank=True, null=True)
    #proyectos = models.ManyToManyField(Proyecto, related_name='mapa_arbitrado_proyectos', blank=True)
    #tags = models.ManyToManyField(Tag, related_name='mapa_arbitrado_tags', blank=True)

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
    usuarios = SortedManyToManyField(User, related_name='informe_tecnico_autores', verbose_name='Autores')
    fecha = models.DateField(auto_now=False)
    numero_paginas = models.PositiveIntegerField(default=1)
    proyecto = models.ForeignKey(Proyecto, blank=True, null=True)
    #proyectos = models.ManyToManyField(Proyecto, related_name='informe_tecnico_proyectos', blank=True)
    url = models.URLField(blank=True)
    #tags = models.ManyToManyField(Tag, related_name='informe_tecnico_tags', blank=True)

    def __str__(self):
        return "{} : {}".format(self.titulo, self.fecha)

    def get_absolute_url(self):
        return reverse('informe_tecnico_publico_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Informe técnico de acceso público"
        verbose_name_plural = "Informes técnicos de acceso público"
        ordering = ['fecha', 'titulo']
