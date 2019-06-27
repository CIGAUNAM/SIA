from django.db import models
from django.conf import settings
from nucleo.models import User, Evento, TipoEvento, Pais, Libro, Revista, InstitucionSimple, RevistaDivulgacion, Indice, MedioDivulgacion, Financiamiento
from investigacion.models import ProyectoInvestigacion
from django.urls import reverse
from sortedm2m.fields import SortedManyToManyField

EVENTO__AMBITO = getattr(settings, 'EVENTO__AMBITO', (('NACIONAL', 'Nacional'), ('INTERNACIONAL', 'Internacional')))
STATUS_PUBLICACION_LIBRO = getattr(settings, 'STATUS_PUBLICACION_LIBRO', (('', '-------'), ('ENVIADO', 'Enviado'), ('ACEPTADO', 'Aceptado'), ('EN_PRENSA', 'En prensa'), ('PUBLICADO', 'Publicado')))

STATUS_PUBLICACION = (('', '-------'), ('ENVIADO', 'Enviado'), ('ACEPTADO', 'Aceptado'), ('EN_PRENSA', 'En prensa'), ('PUBLICADO', 'Publicado'))


# Create your models here.

class ArticuloDivulgacion(models.Model):
    titulo = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_PUBLICACION)
    autores = SortedManyToManyField(User, related_name='articulo_divulgacion_autores', verbose_name='Autores')
    autores_todos = models.TextField()
    agradecimientos = models.ManyToManyField(User, related_name='articulo_divulgacion_agradecimientos', blank=True)
    url = models.URLField(blank=True)
    solo_electronico = models.BooleanField(default=False)
    revista_divulgacion = models.ForeignKey(RevistaDivulgacion, related_name='articulodivulgacion_revistadivulgacion', on_delete=models.DO_NOTHING)
    fecha = models.DateField(null=True, blank=True)
    fecha_enviado = models.DateField(null=True, blank=True)
    fecha_aceptado = models.DateField(null=True, blank=True)
    fecha_enprensa = models.DateField(null=True, blank=True)
    fecha_publicado = models.DateField(null=True, blank=True)
    pagina_inicio = models.PositiveIntegerField()
    pagina_fin = models.PositiveIntegerField()
    numero = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return "{} : {}".format(self.titulo, self.revista_divulgacion)

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


class EventoDivulgacion(models.Model):
    eventodivulgacion_nombre = models.CharField(max_length=255)
    eventodivulgacion_tipo = models.ForeignKey(TipoEvento, on_delete=models.PROTECT)
    eventodivulgacion_fecha_inicio = models.DateField()
    eventodivulgacion_fecha_fin = models.DateField()
    eventodivulgacion_pais = models.ForeignKey(Pais, on_delete=models.PROTECT)
    eventodivulgacion_ciudad = models.CharField(max_length=255)
    eventodivulgacion_ambito = models.CharField(max_length=20, choices=EVENTO__AMBITO)
    eventodivulgacion_numeroponentes = models.PositiveIntegerField()
    eventodivulgacion_numeroasistentes = models.PositiveIntegerField()

    def __str__(self):
        return self.eventodivulgacion_nombre

    def natural_key(self):
        return self.eventodivulgacion_nombre

    def get_absolute_url(self):
        return reverse('eventodivulgacion_detalle', kwargs={'pk': self.pk})

    class Meta:
        unique_together = ['eventodivulgacion_fecha_inicio', 'eventodivulgacion_nombre']




class OrganizacionEventoDivulgacion(models.Model):
    evento2 = models.ForeignKey(Evento, on_delete=models.DO_NOTHING)
    evento = models.ForeignKey(EventoDivulgacion, blank=True, null=True, related_name='OrganizacionEventoAcademico_evento', on_delete=models.DO_NOTHING)

    tipo_participacion = models.CharField(
        max_length=50,
        choices=(('', '-------'), ('COORDINADOR', 'Coordinador general'), ('COMITE_ORGANIZADOR', 'Comité organizador'),
                 ('APOYO_TECNICO', 'Apoyo técnico'), ('OTRO', 'Otro tipo de participaciòn')))
    tipo_participacion_otro = models.CharField(max_length=254, blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    coordinador_general = models.ForeignKey(User, blank=True, null=True, related_name='organizacion_evento_divulgacion_coordinador_general', on_delete=models.DO_NOTHING, verbose_name='Coordinador general')
    comite_organizador = SortedManyToManyField(User, blank=True, related_name='organizacion_evento_divulgacion_comite_organizador', verbose_name='Comite organizador')
    apoyo_tecnico = SortedManyToManyField(User, blank=True, related_name='organizacion_evento_divulgacion_apoyo_tecnico', verbose_name='Apoyo técnico')

    def __str__(self):
        return "{}, {}".format(self.evento2, self.tipo_participacion)

    def get_absolute_url(self):
        return reverse('organizacion_evento_divulgacion_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Organización de evento de divulgación'
        verbose_name_plural = 'Organización de eventos de divulgación'


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
    tema = models.CharField(max_length=254)
    fecha = models.DateField()
    descripcion = models.TextField(blank=True)
    actividad = models.CharField(max_length=20, choices=(
        ('PRODUCCION', 'Producción'), ('PARTICIPACION', 'Participación'), ('ENTREVISTA', 'Entrevista'),
        ('OTRA', 'Otra')))
    medio_divulgacion = models.ForeignKey(MedioDivulgacion, blank=True, null=True, on_delete=models.DO_NOTHING)
    medio_divulgacion_text = models.CharField(max_length=254, blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{} : {} : {}".format(self.medio_divulgacion.nombre_medio, self.tema, self.fecha)

    def get_absolute_url(self):
        return reverse('programa_radio_television_internet_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['fecha', 'tema']
        verbose_name = 'Programa de radio, televisión, internet o medios impresos'
        verbose_name_plural = 'Programas de radio, televisión, internet o medios impresos'
