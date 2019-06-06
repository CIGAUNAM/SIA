from django.db import models
from django.conf import settings
from nucleo.models import User, Editorial, Evento, Pais, TipoEvento, Libro, Revista, Indice, InstitucionSimple
from investigacion.models import ProyectoInvestigacion, ArticuloCientifico
from django.urls import reverse
from sortedm2m.fields import SortedManyToManyField


EVENTO__AMBITO = getattr(settings, 'EVENTO__AMBITO', (('', '-------'), ('NACIONAL', 'Nacional'), ('INTERNACIONAL', 'Internacional')))
EVENTO__RESPONSABILIDAD = getattr(settings, 'EVENTO__RESPONSABILIDAD', (('', '-------'), ('COORDINADOR', 'Coordinador general'),
                                                                        ('COMITE', 'Comité organizador'),
                                                                        ('AYUDANTE', 'Ayudante'),
                                                                        ('TECNICO', 'Apoyo técnico'), ('OTRO', 'Otro')))
RESENA__TIPO = getattr(settings, 'RESENA__TIPO', (('', '-------'), ('LIBRO', 'Libro'), ('ARTICULO', 'Artículo')))


# Create your models here.


class MemoriaInExtenso(models.Model):
    nombre = models.CharField(max_length=254, verbose_name='Nombre de memoria in extenso')
    evento_text = models.CharField(max_length=254, verbose_name='Nombre del evento')
    lugar = models.CharField(max_length=254, verbose_name='Lugar del evento')
    fecha = models.DateField()
    pais = models.ForeignKey(Pais, on_delete=models.DO_NOTHING, )
    ciudad = models.CharField(max_length=254)
    autores = SortedManyToManyField(User)
    autores_todos = models.TextField(blank=True, null=True)
    institucion = models.ForeignKey(InstitucionSimple, on_delete=models.DO_NOTHING)
    pagina_inicio = models.PositiveIntegerField()
    pagina_fin = models.PositiveIntegerField()
    isbn = models.SlugField(max_length=20, blank=True)

    def __str__(self):
        return self.nombre
    
    def get_absolute_url(self):
        return reverse('memoria_in_extenso_detalle', kwargs={'pk': self.pk})
    
    class Meta:
        ordering = ['nombre']
        verbose_name = 'Memoria in extenso'
        verbose_name_plural = 'Memorias in extenso'


class EventoDifusion(models.Model):
    eventodifusion_nombre = models.CharField(max_length=255)
    eventodifusion_tipo = models.ForeignKey(TipoEvento, on_delete=models.PROTECT)
    eventodifusion_fecha_inicio = models.DateField()
    eventodifusion_fecha_fin = models.DateField()
    eventodifusion_pais = models.ForeignKey(Pais, on_delete=models.PROTECT)
    eventodifusion_ciudad = models.CharField(max_length=255)
    eventodifusion_ambito = models.CharField(max_length=20, choices=EVENTO__AMBITO)
    eventodifusion_numeroponentes = models.PositiveIntegerField()
    eventodifusion_numeroasistentes = models.PositiveIntegerField()

    eventodifusion_regverificado = models.BooleanField(default=False,
                                                    verbose_name='Este registro se encuentra validado y verificado. Cuando un registro está marcado como verificado ya no es posible editar ni eliminar por otros usuarios')
    eventodifusion_regfechacreado = models.DateField(auto_now_add=True, blank=True, null=True)
    eventodifusion_regfechaactualizado = models.DateField(auto_now=True, blank=True, null=True)
    eventodifusion_regusuario = models.ForeignKey(User, on_delete=models.PROTECT,
                                               verbose_name='Usuario que creó el registro de esta entrada', default=1)

    def __str__(self):
        return self.eventodifusion_nombre

    def natural_key(self):
        return self.eventodifusion_nombre

    def get_absolute_url(self):
        return reverse('eventodifusion_detalle', kwargs={'pk': self.pk})

    class Meta:
        unique_together = ['eventodifusion_fecha_inicio', 'eventodifusion_nombre']


class OrganizacionEventoAcademico(models.Model):
    evento = models.ForeignKey(EventoDifusion, on_delete=models.DO_NOTHING)
    tipo_participacion = models.CharField(
        max_length=50,
        choices=(('', '-------'), ('COORDINADOR', 'Coordinador general'), ('COMITE_ORGANIZADOR', 'Comité organizador'),
                 ('APOYO_TECNICO', 'Apoyo técnico'), ('OTRO', 'Otro tipo de participaciòn')))
    tipo_participacion_otro = models.CharField(max_length=254, blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{} ({})".format(self.evento, self.get_tipo_participacion_display())

    def get_absolute_url(self):
        return reverse('organizacion_evento_academico_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Organización de evento académico'
        verbose_name_plural = 'Organización de eventos académicos'


class ParticipacionEventoAcademico(models.Model):
    tipo = models.CharField(max_length=30, choices=(('', '------'), ('PONENCIA', 'Ponencia'), ('POSTER', 'Poster')))
    titulo = models.CharField(max_length=255)
    evento = models.CharField(max_length=254, verbose_name='Nombre del evento')
    lugar_evento = models.CharField(max_length=254, verbose_name='Lugar del evento')
    ciudad = models.CharField(max_length=255)
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT)
    institucion = models.ForeignKey(InstitucionSimple, on_delete=models.DO_NOTHING)
    fecha = models.DateField()
    ambito = models.CharField(max_length=20, choices=EVENTO__AMBITO)
    por_invitacion = models.BooleanField(default=False)
    ponencia_magistral = models.BooleanField(default=False)
    autores = SortedManyToManyField(User, verbose_name='Autores')
    autores_todos = models.TextField()

    def __str__(self):
        return "{} : {}".format(self.evento, self.titulo)

    def get_absolute_url(self):
        return reverse('participacion_evento_academico_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['evento', 'titulo']
        verbose_name = 'Participación en evento académico'
        verbose_name_plural = 'Participación en eventos académicos'
