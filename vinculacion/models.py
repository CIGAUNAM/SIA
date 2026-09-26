from django.conf import settings
from django.db import models

from nucleo.models import Ambito, Institucion, Periodo, Persona, Revista, requerido_si, validar_periodo


class ArbitrajePublicacion(models.Model):
    class Tipo(models.TextChoices):
        ARTICULO = 'ARTICULO', 'Artículo en revista'
        LIBRO = 'LIBRO', 'Libro'
        CAPITULO_LIBRO = 'CAPITULO_LIBRO', 'Capítulo de libro'

    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    revista = models.ForeignKey(Revista, on_delete=models.PROTECT, null=True, blank=True,
                                help_text='Solo para artículos.')
    obra = models.CharField('libro o capítulo', max_length=255, blank=True, help_text='Solo para libros y capítulos.')
    fecha_dictamen = models.DateField('fecha del dictamen')
    institucion = models.ForeignKey(Institucion, on_delete=models.PROTECT, null=True, blank=True,
                                    verbose_name='institución')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='arbitrajes')

    class Meta:
        ordering = ['-fecha_dictamen']
        verbose_name = 'arbitraje de publicación académica'
        verbose_name_plural = 'arbitrajes de publicaciones académicas'

    def __str__(self):
        return f'{self.get_tipo_display()}: {self.revista or self.obra} ({self.fecha_dictamen:%Y})'

    def clean(self):
        super().clean()
        requerido_si(self.tipo == self.Tipo.ARTICULO, self, 'revista', 'Elige la revista del artículo dictaminado.')
        requerido_si(self.tipo != self.Tipo.ARTICULO, self, 'obra', 'Escribe el título del libro o capítulo.')


class TipoComision(models.Model):
    nombre = models.CharField(max_length=140, unique=True)
    orden = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['orden', 'pk']
        verbose_name = 'tipo de comisión de arbitraje'
        verbose_name_plural = 'tipos de comisión de arbitraje'

    def __str__(self):
        return self.nombre


class OtraComision(Periodo):
    tipo = models.ForeignKey(TipoComision, on_delete=models.PROTECT)
    descripcion = models.CharField('descripción', max_length=255, blank=True)
    institucion = models.ForeignKey(Institucion, on_delete=models.PROTECT, null=True, blank=True,
                                    verbose_name='institución')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='otras_comisiones')

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'otra comisión de arbitraje'
        verbose_name_plural = 'otras comisiones de arbitraje'

    def __str__(self):
        return self.descripcion or str(self.tipo)


class RedAcademica(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    ambito = models.CharField('ámbito', max_length=20, choices=Ambito.choices)
    objetivos = models.TextField()
    fecha_constitucion = models.DateField('fecha de constitución')
    fecha_fin = models.DateField('fecha de término', null=True, blank=True)
    instituciones = models.ManyToManyField(Institucion, blank=True)
    proyecto = models.ForeignKey('investigacion.ProyectoInvestigacion', on_delete=models.SET_NULL, null=True, blank=True)
    participantes = models.ManyToManyField(Persona, related_name='redes_academicas')

    class Meta:
        ordering = ['-fecha_constitucion']
        verbose_name = 'red académica'
        verbose_name_plural = 'redes académicas'

    def __str__(self):
        return self.nombre

    def clean(self):
        super().clean()
        validar_periodo(self.fecha_constitucion, self.fecha_fin)


class Convenio(Periodo):
    nombre = models.CharField(max_length=254, unique=True)
    ambito = models.CharField('ámbito', max_length=20, choices=Ambito.choices)
    objetivos = models.TextField()
    instituciones = models.ManyToManyField(Institucion)
    es_renovacion = models.BooleanField('es renovación', default=False)
    financiamiento = models.CharField(max_length=254, blank=True)
    proyecto = models.ForeignKey('investigacion.ProyectoInvestigacion', on_delete=models.SET_NULL, null=True, blank=True)
    participantes = models.ManyToManyField(Persona, related_name='convenios')

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'convenio con otra entidad'
        verbose_name_plural = 'convenios con otras entidades'

    def __str__(self):
        return self.nombre


class ServicioAsesoriaExterna(Periodo):
    nombre = models.CharField('nombre del servicio', max_length=254)
    descripcion = models.TextField('descripción', blank=True)
    institucion = models.ForeignKey(Institucion, on_delete=models.PROTECT, verbose_name='institución')
    financiamiento = models.CharField(max_length=254, blank=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='servicios_externos')

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'servicio o asesoría externa'
        verbose_name_plural = 'servicios o asesorías externas'

    def __str__(self):
        return self.nombre


from nucleo.historial import registrar_historial  # noqa: E402

registrar_historial(globals())
