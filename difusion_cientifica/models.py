from django.db import models
from django.conf import settings
from nucleo.models import User, Editorial, Evento, Pais, TipoEvento, Libro, Revista, Indice, InstitucionSimple
from investigacion.models import ProyectoInvestigacion, ArticuloCientifico
from django.urls import reverse
from sortedm2m.fields import SortedManyToManyField


EVENTO__AMBITO = getattr(settings, 'EVENTO__AMBITO', (('NACIONAL', 'Nacional'), ('INTERNACIONAL', 'Internacional')))
EVENTO__RESPONSABILIDAD = getattr(settings, 'EVENTO__RESPONSABILIDAD', (('COORDINADOR', 'Coordinador general'),
                                                                        ('COMITE', 'Comité organizador'),
                                                                        ('AYUDANTE', 'Ayudante'),
                                                                        ('TECNICO', 'Apoyo técnico'), ('OTRO', 'Otro')))
RESENA__TIPO = getattr(settings, 'RESENA__TIPO', (('LIBRO', 'Libro'), ('ARTICULO', 'Artículo')))


# Create your models here.


class MemoriaInExtenso(models.Model):
    nombre = models.CharField(max_length=254, verbose_name='Nombre de memoria in extenso')
    evento = models.ForeignKey(Evento, on_delete=models.DO_NOTHING, null=True, blank=True)
    evento_text = models.CharField(max_length=254, blank=True, null=True, verbose_name='Nombre del evento')
    lugar_evento = models.CharField(max_length=254, blank=True, null=True, verbose_name='Lugar del evento')

    autores = SortedManyToManyField(User)
    autores_todos = models.TextField(blank=True, null=True)
    institucion = models.ForeignKey(InstitucionSimple, on_delete=models.DO_NOTHING, null=True, blank=True)

    pagina_inicio = models.PositiveIntegerField(null=True, blank=True)
    pagina_fin = models.PositiveIntegerField(null=True, blank=True)
    isbn = models.SlugField(max_length=20, blank=True)
    url = models.URLField(blank=True)

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
    # usuario = models.ForeignKey(User, related_name='traduccion_autor', on_delete=models.DO_NOTHING)
    autores = SortedManyToManyField(User, verbose_name='Autores')

    def __str__(self):
        return '{} : {}'.format(self.usuario, self.titulo)

    def get_absolute_url(self):
        return reverse('traduccion_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Reseña de libro'
        verbose_name_plural = 'Reseñas de libros'


class EventoDifusion(models.Model):
    evento_nombre = models.CharField(max_length=255)
    evento_tipo = models.ForeignKey(TipoEvento, on_delete=models.PROTECT)
    evento_fecha_inicio = models.DateField()
    evento_fecha_fin = models.DateField()
    evento_pais = models.ForeignKey(Pais, on_delete=models.PROTECT)
    evento_ciudad = models.CharField(max_length=255)
    evento_ambito = models.CharField(max_length=20, choices=EVENTO__AMBITO)
    evento_numeroponentes = models.PositiveIntegerField()
    evento_numeroasistentes = models.PositiveIntegerField()

    def __str__(self):
        return self.evento_nombre

    def natural_key(self):
        return self.evento_nombre

    def get_absolute_url(self):
        return reverse('eventodifusion_detalle', kwargs={'pk': self.pk})

    class Meta:
        unique_together = ['evento_fecha_inicio', 'evento_nombre']


class OrganizacionEventoAcademico(models.Model):
    evento2 = models.ForeignKey(Evento, on_delete=models.DO_NOTHING)
    tipo_participacion = models.CharField(
        max_length=50,
        choices=(('', '-------'), ('COORDINADOR', 'Coordinador general'), ('COMITE_ORGANIZADOR', 'Comité organizador'),
                 ('APOYO_TECNICO', 'Apoyo técnico'), ('OTRO', 'Otro tipo de participaciòn')))
    tipo_participacion_otro = models.CharField(max_length=254, blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    coordinador_general = models.ForeignKey(User, blank=True, null=True, related_name='organizacion_evento_academico_coordinador_general', on_delete=models.DO_NOTHING, verbose_name='Coordinador general')
    comite_organizador = SortedManyToManyField(User, blank=True, related_name='organizacion_evento_academico_comite_organizador', verbose_name='Comite organizador')
    apoyo_tecnico = SortedManyToManyField(User, blank=True, related_name='organizacion_evento_academico_apoyo_tecnico', verbose_name='Apoyo técnico')

    def __str__(self):
        return "{}, {}".format(self.evento2, self.tipo_participacion)

    def get_absolute_url(self):
        return reverse('organizacion_evento_academico_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Organización de evento académico'
        verbose_name_plural = 'Organización de eventos académicos'


class ParticipacionEventoAcademico(models.Model):
    tipo = models.CharField(max_length=30, choices=(('', '------'), ('PONENCIA', 'Ponencia'), ('POSTER', 'Poster')))
    titulo = models.CharField(max_length=255)
    evento = models.ForeignKey(Evento, blank=True, null=True, on_delete=models.DO_NOTHING)

    evento_text = models.CharField(max_length=254, blank=True, null=True, verbose_name='Nombre del evento')
    lugar_evento = models.CharField(max_length=254, blank=True, null=True, verbose_name='Lugar del evento')
    institucion = models.ForeignKey(InstitucionSimple, on_delete=models.DO_NOTHING, null=True, blank=True)
    fecha = models.DateField()

    ambito = models.CharField(max_length=20, choices=EVENTO__AMBITO)
    por_invitacion = models.BooleanField(default=False)
    ponencia_magistral = models.BooleanField(default=False)
    autores = SortedManyToManyField(User, related_name='participacion_evento_academico_autores', verbose_name='Autores')
    autores_todos = models.TextField(blank=True, null=True)

    def __str__(self):
        return "{} : {}".format(self.titulo, self.evento)

    def get_absolute_url(self):
        return reverse('participacion_evento_academico_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Participación en evento académico'
        verbose_name_plural = 'Participación en eventos académicos'
