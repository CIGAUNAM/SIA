from django.db import models
from django.conf import settings
from nucleo.models import User, Evento, Libro, Revista, InstitucionSimple, RevistaDivulgacion, Indice, MedioDivulgacion, Financiamiento
from investigacion.models import ProyectoInvestigacion
from django.urls import reverse
from sortedm2m.fields import SortedManyToManyField

EVENTO__AMBITO = getattr(settings, 'EVENTO__AMBITO', (('NACIONAL', 'Nacional'), ('INTERNACIONAL', 'Internacional')))
EVENTO__RESPONSABILIDAD = getattr(settings, 'EVENTO__RESPONSABILIDAD', (
    ('COORDINADOR', 'Coordinador general'), ('COMITE', 'Comité organizador'), ('AYUDANTE', 'Ayudante'),
    ('TECNICO', 'Apoyo técnico'), ('OTRO', 'Otro')))
STATUS_PUBLICACION_ARTICULO = getattr(settings, 'STATUS_PUBLICACION_ARTICULO', (
    ('PUBLICADO', 'Publicado'), ('ACEPTADO', 'Aceptado'), ('ENVIADO', 'Enviado'),
    ('OTRO', 'Otro')))
STATUS_PUBLICACION_LIBRO = getattr(settings, 'STATUS_PUBLICACION_LIBRO', (
    ('PUBLICADO', 'Publicado'), ('EN_PRENSA', 'En prensa'), ('ACEPTADO', 'Aceptado'), ('ENVIADO', 'Enviado'),
    ('OTRO', 'Otro')))


# Create your models here.

class ArticuloDivulgacion(models.Model):
    titulo = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_PUBLICACION_ARTICULO)
    autores = SortedManyToManyField(User, related_name='articulo_divulgacion_autores', verbose_name='Autores')
    autores_todos = models.TextField(blank=True, null=True)
    agradecimientos = models.ManyToManyField(User, related_name='articulo_divulgacion_agradecimientos', blank=True)
    url = models.URLField(blank=True)
    solo_electronico = models.BooleanField(default=False)
    revista = models.ForeignKey(RevistaDivulgacion, related_name='articulodivulgacion_revista', blank=True, null=True, on_delete=models.DO_NOTHING)
    revista_divulgacion = models.ForeignKey(RevistaDivulgacion, related_name='articulodivulgacion_revistadivulgacion', blank=True, null=True, on_delete=models.DO_NOTHING)
    fecha = models.DateField(null=True, blank=True)
    fecha_enviado = models.DateField(null=True, blank=True)
    fecha_aceptado = models.DateField(null=True, blank=True)
    fecha_enprensa = models.DateField(null=True, blank=True)
    fecha_publicado = models.DateField(null=True, blank=True)
    pagina_inicio = models.PositiveIntegerField()
    pagina_fin = models.PositiveIntegerField()

    volumen = models.CharField(max_length=100, blank=True)
    numero = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return "{} : {} : {}".format(self.titulo, self.tipo.title(), self.revista)

    def get_absolute_url(self):
        return reverse('articulo_divulgacion_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Artículo de divulgación"
        verbose_name_plural = "Artículos de divulgación"
        ordering = ['fecha', 'titulo']


class CapituloLibroDivulgacion(models.Model):
    titulo = models.CharField(max_length=255)
    libro = models.ForeignKey(Libro, on_delete=models.DO_NOTHING)
    pagina_inicio = models.PositiveIntegerField()
    pagina_fin = models.PositiveIntegerField()
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    autores = SortedManyToManyField(User, related_name='capitulo_libro_divulgacion_autores', verbose_name='Autores')
    autores_todos = models.TextField(blank=True, null=True)

    def __str__(self):
        return "{} : {}".format(self.titulo, self.libro)

    def get_absolute_url(self):
        return reverse('capitulo_libro_divulgacion_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Capítulo en libro de divulgación"
        verbose_name_plural = "Capítulos en libros de divulgración"
        ordering = ['titulo']
        unique_together = ['titulo', 'libro']


class OrganizacionEventoDivulgacion(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.DO_NOTHING)
    descripcion = models.TextField(blank=True)
    numero_ponentes = models.PositiveIntegerField()
    numero_asistentes = models.PositiveIntegerField()
    ambito = models.CharField(max_length=20, choices=EVENTO__AMBITO)
    coordinador_general = models.ForeignKey(User, blank=True, null=True, related_name='organizacion_evento_divulgacion_coordinador_general', on_delete=models.DO_NOTHING, verbose_name='Coordinador general')
    comite_organizador = SortedManyToManyField(User, blank=True, related_name='organizacion_evento_divulgacion_comite_organizador', verbose_name='Comite organizador')
    ayudantes = SortedManyToManyField(User, blank=True, related_name='organizacion_evento_divulgacion_ayudantes', verbose_name='Ayudantes')
    apoyo_tecnico = SortedManyToManyField(User, blank=True, related_name='organizacion_evento_divulgacion_apoyo_tecnico', verbose_name='Apoyo técnico')

    def __str__(self):
        return "{}, {}, {}, {}, {}".format(self.evento.tipo, self.evento, self.evento.fecha_inicio,
                                               self.evento.ciudad, self.evento.pais.nombre)

    def get_absolute_url(self):
        return reverse('organizacion_evento_divulgacion_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Organización de evento académico'
        verbose_name_plural = 'Organización de eventos académicos'


class ParticipacionEventoDivulgacion(models.Model):
    tipo = models.CharField(max_length=30, choices=(('', '------'), ('PONENCIA', 'Ponencia'), ('POSTER', 'Poster')))
    titulo = models.CharField(max_length=255)
    evento = models.ForeignKey(Evento, on_delete=models.DO_NOTHING)

    evento_text = models.CharField(max_length=254, blank=True, null=True, verbose_name='Nombre del evento')
    lugar_evento = models.CharField(max_length=254, blank=True, null=True, verbose_name='Lugar del evento')
    institucion = models.ForeignKey(InstitucionSimple, on_delete=models.DO_NOTHING, null=True, blank=True)
    fecha = models.DateField()

    ambito = models.CharField(max_length=20, choices=EVENTO__AMBITO)
    por_invitacion = models.BooleanField(default=False)
    ponencia_magistral = models.BooleanField(default=False)
    autores = models.ManyToManyField(User, related_name='participacion_evento_divulgacion_autores')

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
        ('PRODUCCION', 'Producción'), ('PARTICIPACION', 'Participación'), ('ENTREVISTA', 'Entrevista'),
        ('OTRA', 'Otra')))
    medio_divulgacion = models.ForeignKey(MedioDivulgacion, on_delete=models.DO_NOTHING)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{} : {} : {}".format(self.medio_divulgacion.nombre_medio, self.tema, self.fecha)

    def get_absolute_url(self):
        return reverse('programa_radio_television_internet_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['fecha', 'tema']
        verbose_name = 'Programa de radio, televisión o internet'
        verbose_name_plural = 'Programas de radio, televisión o internet'
