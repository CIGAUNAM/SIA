from django.conf import settings
from django.db import models

from difusion_cientifica.models import TipoParticipacionOrganizacion
from nucleo.models import (Ambito, CapituloLibro, EstadoPublicacion, Evento, Institucion, MedioDivulgacion,
                           Participante, Persona, Revista, requerido_si, validar_paginas)


class ArticuloDivulgacion(EstadoPublicacion):
    titulo = models.CharField('título', max_length=255, unique=True)
    revista = models.ForeignKey(Revista, on_delete=models.PROTECT)
    volumen = models.CharField(max_length=100, blank=True)
    numero = models.CharField('número', max_length=100, blank=True)
    pagina_inicio = models.PositiveIntegerField('página inicial', null=True, blank=True)
    pagina_fin = models.PositiveIntegerField('página final', null=True, blank=True)
    url = models.URLField('URL', blank=True)
    solo_electronico = models.BooleanField('solo electrónico', default=False)
    autores = models.ManyToManyField(Persona, through='ArticuloDivulgacionAutor', related_name='articulos_divulgacion')
    agradecimientos = models.ManyToManyField(Persona, blank=True, related_name='articulos_divulgacion_agradecimiento')

    class Meta:
        ordering = ['-fecha_publicado', '-fecha_enprensa', '-fecha_aceptado', '-fecha_enviado', 'titulo']
        verbose_name = 'artículo de divulgación'
        verbose_name_plural = 'artículos de divulgación'

    def __str__(self):
        return self.titulo

    def clean(self):
        super().clean()
        validar_paginas(self)


class ArticuloDivulgacionAutor(Participante):
    articulo = models.ForeignKey(ArticuloDivulgacion, on_delete=models.CASCADE)

    class Meta(Participante.Meta):
        verbose_name = 'autor'
        verbose_name_plural = 'autores'
        constraints = [models.UniqueConstraint(fields=['articulo', 'persona'], name='articulo_divulgacion_autor_unico')]


class CapituloLibroDivulgacion(CapituloLibro):
    autores = models.ManyToManyField(Persona, through='CapituloLibroDivulgacionAutor',
                                     related_name='capitulos_divulgacion')

    class Meta(CapituloLibro.Meta):
        verbose_name = 'capítulo en libro de divulgación'
        verbose_name_plural = 'capítulos en libros de divulgación'
        constraints = [models.UniqueConstraint(fields=['titulo', 'libro'], name='capitulo_divulgacion_unico')]


class CapituloLibroDivulgacionAutor(Participante):
    capitulo = models.ForeignKey(CapituloLibroDivulgacion, on_delete=models.CASCADE)

    class Meta(Participante.Meta):
        verbose_name = 'autor'
        verbose_name_plural = 'autores'
        constraints = [models.UniqueConstraint(fields=['capitulo', 'persona'], name='capitulo_divulgacion_autor_unico')]


class OrganizacionEventoDivulgacion(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.PROTECT)
    tipo_participacion = models.CharField('tipo de participación', max_length=30,
                                          choices=TipoParticipacionOrganizacion.choices)
    tipo_participacion_otro = models.CharField('otro tipo de participación', max_length=254, blank=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                related_name='organizaciones_eventos_divulgacion')

    class Meta:
        ordering = ['-evento__fecha_inicio']
        verbose_name = 'organización de evento de divulgación'
        verbose_name_plural = 'organización de eventos de divulgación'

    def __str__(self):
        return f'{self.evento} ({self.get_tipo_participacion_display()})'

    def clean(self):
        super().clean()
        requerido_si(self.tipo_participacion == TipoParticipacionOrganizacion.OTRO, self, 'tipo_participacion_otro')


class ParticipacionEventoDivulgacion(models.Model):
    class Tipo(models.TextChoices):
        PONENCIA = 'PONENCIA', 'Ponencia'
        POSTER = 'POSTER', 'Póster'

    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    titulo = models.CharField('título', max_length=255)
    evento = models.ForeignKey(Evento, on_delete=models.PROTECT)
    institucion = models.ForeignKey(Institucion, on_delete=models.PROTECT, null=True, blank=True,
                                    verbose_name='institución organizadora')
    fecha = models.DateField()
    ambito = models.CharField('ámbito', max_length=20, choices=Ambito.choices)
    por_invitacion = models.BooleanField('por invitación', default=False,
                                         help_text='La participación fue por invitación expresa de los organizadores.')
    ponencia_magistral = models.BooleanField('conferencia magistral', default=False,
                                             help_text='Conferencia magistral o plenaria.')
    autores = models.ManyToManyField(Persona, through='ParticipacionEventoDivulgacionAutor',
                                     related_name='participaciones_eventos_divulgacion')

    class Meta:
        ordering = ['-fecha', 'titulo']
        verbose_name = 'participación en evento de divulgación'
        verbose_name_plural = 'participación en eventos de divulgación'

    def __str__(self):
        return f'{self.titulo} — {self.evento}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class ParticipacionEventoDivulgacionAutor(Participante):
    participacion = models.ForeignKey(ParticipacionEventoDivulgacion, on_delete=models.CASCADE)

    class Meta(Participante.Meta):
        verbose_name = 'autor'
        verbose_name_plural = 'autores'
        constraints = [models.UniqueConstraint(fields=['participacion', 'persona'], name='participacion_divulgacion_autor_unico')]


class ProgramaMedio(models.Model):
    """Participación en programas de radio, televisión, internet o medios impresos."""

    class Actividad(models.TextChoices):
        PRODUCCION = 'PRODUCCION', 'Producción'
        PARTICIPACION = 'PARTICIPACION', 'Participación'
        ENTREVISTA = 'ENTREVISTA', 'Entrevista'
        OTRA = 'OTRA', 'Otra'

    tema = models.CharField(max_length=254)
    fecha = models.DateField(null=True)
    descripcion = models.TextField('descripción', blank=True)
    actividad = models.CharField(max_length=20, choices=Actividad.choices)
    medio = models.ForeignKey(MedioDivulgacion, on_delete=models.PROTECT)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='programas_medios')

    class Meta:
        ordering = ['-fecha', 'tema']
        verbose_name = 'programa en medios de comunicación'
        verbose_name_plural = 'programas en medios de comunicación'

    def __str__(self):
        return f'{self.tema} ({self.medio})'


from nucleo.historial import registrar_historial  # noqa: E402

registrar_historial(globals())
