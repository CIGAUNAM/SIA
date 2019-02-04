from django.db import models
from django.conf import settings
from nucleo.models import User, Editorial, Evento, Libro, Revista, Indice
from investigacion.models import ProyectoInvestigacion, ArticuloCientifico
from django.urls import reverse
from sortedm2m.fields import SortedManyToManyField


EVENTO__AMBITO = getattr(settings, 'EVENTO__AMBITO', (('INSTITUCIONAL', 'Institucional'), ('REGIONAL', 'Regional'),
                                                      ('NACIONAL', 'Nacional'), ('INTERNACIONAL', 'Internacional')))
EVENTO__RESPONSABILIDAD = getattr(settings, 'EVENTO__RESPONSABILIDAD', (('COORDINADOR', 'Coordinador general'),
                                                                        ('COMITE', 'Comité organizador'),
                                                                        ('AYUDANTE', 'Ayudante'),
                                                                        ('TECNICO', 'Apoyo técnico'), ('OTRO', 'Otro')))
RESENA__TIPO = getattr(settings, 'RESENA__TIPO', (('LIBRO', 'Libro'), ('ARTICULO', 'Artículo')))


# Create your models here.


class MemoriaInExtenso(models.Model):
    nombre = models.CharField(max_length=255, verbose_name='Nombre de memoria in extenso')
    descripcion = models.TextField(blank=True)
    evento = models.ForeignKey(Evento, on_delete=models.DO_NOTHING)
    autores = SortedManyToManyField(User)
    pagina_inicio = models.PositiveIntegerField(null=True, blank=True)
    pagina_fin = models.PositiveIntegerField(null=True, blank=True)
    editorial_text = models.CharField(max_length=255, verbose_name='Nombre de memoria in extenso')
    indices = models.ManyToManyField(Indice, related_name='memoria_in_extenso_indices', blank=True)
    issn = models.SlugField(max_length=20, blank=True)

    def __str__(self):
        return self.nombre
    
    def get_absolute_url(self):
        return reverse('memoria_in_extenso_detalle', kwargs={'pk': self.pk})
    
    class Meta:
        verbose_name = 'Memoria in extenso'
        verbose_name_plural = 'Memorias in extenso'


class Resena(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=10, choices=RESENA__TIPO)
    libro_resenado = models.ForeignKey(Libro, blank=True, null=True, related_name='resena_libro_resenado',
                                       on_delete=models.DO_NOTHING)
    articulo_resenado = models.ForeignKey(ArticuloCientifico, blank=True, null=True,
                                          related_name='resena_revista_resenada', on_delete=models.DO_NOTHING)
    fecha = models.DateField()
    revista_publica = models.ForeignKey(Revista, related_name='resena_revista_publica', on_delete=models.DO_NOTHING)
    pagina_inicio = models.PositiveIntegerField()
    pagina_fin = models.PositiveIntegerField()
    url = models.URLField(blank=True)
    autores = SortedManyToManyField(User, related_name='resena_autores', verbose_name='Autores')

    def __str__(self):
        return '{} : {}'.format(self.usuario, self.titulo)

    def get_absolute_url(self):
        return reverse('resena_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Reseña de publicación'
        verbose_name_plural = 'Reseñas de publicaciones'


class Traduccion(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=10, choices=RESENA__TIPO)
    libro = models.ForeignKey(Libro, blank=True, null=True, on_delete=models.DO_NOTHING)
    articulo = models.ForeignKey(ArticuloCientifico, blank=True, null=True, on_delete=models.DO_NOTHING)
    fecha = models.DateField()
    url = models.URLField(blank=True)
    autores = SortedManyToManyField(User, verbose_name='Autores')

    def __str__(self):
        return '{} : {}'.format(self.usuario, self.titulo)

    def get_absolute_url(self):
        return reverse('traduccion_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Reseña de libro'
        verbose_name_plural = 'Reseñas de libros'


class OrganizacionEventoAcademico(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.DO_NOTHING)
    descripcion = models.TextField(blank=True)
    numero_ponentes = models.PositiveIntegerField()
    numero_asistentes = models.PositiveIntegerField()
    ambito = models.CharField(max_length=20, choices=EVENTO__AMBITO)
    coordinador_general = models.ForeignKey(User, blank=True, null=True, related_name='organizacion_evento_academico_coordinador_general', on_delete=models.DO_NOTHING, verbose_name='Coordinador general')
    comite_organizador = SortedManyToManyField(User, blank=True, related_name='organizacion_evento_academico_comite_organizador', verbose_name='Comite organizador')
    ayudantes = SortedManyToManyField(User, blank=True, related_name='organizacion_evento_academico_ayudantes', verbose_name='Ayudantes')
    apoyo_tecnico = SortedManyToManyField(User, blank=True, related_name='organizacion_evento_academico_apoyo_tecnico', verbose_name='Apoyo técnico')

    def __str__(self):
        return "{}, {}, {}, {}, {}".format(self.evento.tipo, self.evento, self.evento.fecha_inicio,
                                               self.evento.ciudad, self.evento.pais.nombre)

    def get_absolute_url(self):
        return reverse('organizacion_evento_academico_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Organización de evento académico'
        verbose_name_plural = 'Organización de eventos académicos'


class ParticipacionEventoAcademico(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    evento = models.ForeignKey(Evento, on_delete=models.DO_NOTHING)
    ambito = models.CharField(max_length=20, choices=EVENTO__AMBITO)
    resumen_publicado = models.BooleanField(default=False)
    por_invitacion = models.BooleanField(default=False)
    ponencia_magistral = models.BooleanField(default=False)
    autores = SortedManyToManyField(User, related_name='participacion_evento_academico_autores', verbose_name='Autores')

    def __str__(self):
        return "{} : {}".format(self.titulo, self.evento)

    def get_absolute_url(self):
        return reverse('participacion_evento_academico_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Participación en evento académico'
        verbose_name_plural = 'Participación en eventos académicos'
