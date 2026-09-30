from cities_light.models import Country
from django.conf import settings
from django.db import models

from nucleo.models import (Ambito, Evento, Institucion, Participante, Persona, requerido_si,
                           validar_paginas)


class TipoParticipacionOrganizacion(models.TextChoices):
    COORDINADOR = 'COORDINADOR', 'Coordinador general'
    COMITE_ORGANIZADOR = 'COMITE_ORGANIZADOR', 'Comité organizador'
    APOYO_TECNICO = 'APOYO_TECNICO', 'Apoyo técnico'
    OTRO = 'OTRO', 'Otro'


class MemoriaInExtenso(models.Model):
    titulo = models.CharField('título', max_length=254)
    evento = models.CharField('nombre del evento', max_length=254)
    lugar = models.CharField('lugar del evento', max_length=254, blank=True)
    fecha = models.DateField()
    pais = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name='país')
    ciudad = models.CharField(max_length=254, blank=True)
    institucion = models.ForeignKey(Institucion, on_delete=models.PROTECT, null=True, blank=True,
                                    verbose_name='institución organizadora')
    pagina_inicio = models.PositiveIntegerField('página inicial', null=True, blank=True)
    pagina_fin = models.PositiveIntegerField('página final', null=True, blank=True)
    isbn = models.CharField('ISBN', max_length=30, blank=True)
    autores = models.ManyToManyField(Persona, through='MemoriaInExtensoAutor', related_name='memorias_in_extenso')

    class Meta:
        ordering = ['-fecha', 'titulo']
        verbose_name = 'memoria in extenso'
        verbose_name_plural = 'memorias in extenso'

    def __str__(self):
        return self.titulo

    def clean(self):
        super().clean()
        validar_paginas(self)


class MemoriaInExtensoAutor(Participante):
    memoria = models.ForeignKey(MemoriaInExtenso, on_delete=models.CASCADE)

    class Meta(Participante.Meta):
        verbose_name = 'autor'
        verbose_name_plural = 'autores'
        constraints = [models.UniqueConstraint(fields=['memoria', 'persona'], name='memoria_autor_unico')]


class OrganizacionEventoAcademico(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.PROTECT)
    tipo_participacion = models.CharField('tipo de participación', max_length=30,
                                          choices=TipoParticipacionOrganizacion.choices)
    tipo_participacion_otro = models.CharField('otro tipo de participación', max_length=254, blank=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                related_name='organizaciones_eventos_academicos')

    class Meta:
        ordering = ['-evento__fecha_inicio']
        verbose_name = 'organización de evento académico'
        verbose_name_plural = 'organización de eventos académicos'

    def __str__(self):
        return f'{self.evento} ({self.get_tipo_participacion_display()})'

    def clean(self):
        super().clean()
        requerido_si(self.tipo_participacion == TipoParticipacionOrganizacion.OTRO, self, 'tipo_participacion_otro')


class ParticipacionEventoAcademico(models.Model):
    class Tipo(models.TextChoices):
        PONENCIA = 'PONENCIA', 'Ponencia'
        POSTER = 'POSTER', 'Póster'

    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    titulo = models.CharField('título', max_length=255)
    evento = models.CharField('nombre del evento', max_length=254)
    lugar = models.CharField('lugar del evento', max_length=254, blank=True)
    ciudad = models.CharField(max_length=255, blank=True)
    pais = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name='país')
    institucion = models.ForeignKey(Institucion, on_delete=models.PROTECT, null=True, blank=True,
                                    verbose_name='institución organizadora')
    fecha = models.DateField(null=True)
    ambito = models.CharField('ámbito', max_length=20, choices=Ambito.choices)
    por_invitacion = models.BooleanField('por invitación', default=False,
                                         help_text='La ponencia fue por invitación expresa de los organizadores.')
    ponencia_magistral = models.BooleanField('conferencia magistral', default=False,
                                             help_text='Conferencia magistral o plenaria.')
    autores = models.ManyToManyField(Persona, through='ParticipacionEventoAcademicoAutor',
                                     related_name='participaciones_eventos_academicos')

    class Meta:
        ordering = ['-fecha', 'titulo']
        verbose_name = 'participación en evento académico'
        verbose_name_plural = 'participación en eventos académicos'

    def __str__(self):
        return f'{self.titulo} — {self.evento}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class ParticipacionEventoAcademicoAutor(Participante):
    participacion = models.ForeignKey(ParticipacionEventoAcademico, on_delete=models.CASCADE)

    class Meta(Participante.Meta):
        verbose_name = 'autor'
        verbose_name_plural = 'autores'
        constraints = [models.UniqueConstraint(fields=['participacion', 'persona'], name='participacion_academica_autor_unico')]


from nucleo.historial import registrar_historial  # noqa: E402

registrar_historial(globals())
