from django.conf import settings
from django.db import models

from nucleo.models import anio_o_sf, Cargo, Institucion, Periodo, Compartido, requerido_si


class Comision(Compartido):
    class Seccion(models.TextChoices):
        UNAM = 'UNAM', 'Comisiones UNAM'
        ENTIDAD = 'ENTIDAD', 'Comisiones de la entidad'
        COLEGIADO = 'COLEGIADO', 'Cuerpos colegiados UNAM'
        REPRESENTACION = 'REPRESENTACION', 'Representaciones UNAM'
        EXTERNA = 'EXTERNA', 'Comisiones de evaluación académica externas'
        DOCENCIA = 'DOCENCIA', 'Comités de planeación y evaluación docente'
        ARBITRAJE = 'ARBITRAJE', 'Otras actividades de arbitraje'
        NO_ACADEMICA = 'NO_ACADEMICA', 'Vinculación con entidades no académicas'

    nombre = models.CharField(max_length=255, unique=True)
    seccion = models.CharField('sección del informe', max_length=20, choices=Seccion.choices)
    ayuda = models.CharField(max_length=255, blank=True,
                             help_text='Indicación que se muestra al capturar (p. ej. qué escribir en el detalle). No sale en los reportes.')

    class Meta:
        ordering = ['nombre']
        verbose_name = 'comisión (catálogo)'
        verbose_name_plural = 'comisiones (catálogo)'

    def __str__(self):
        return self.nombre

    @property
    def ambito_sugerido(self):
        interior = self.seccion in (self.Seccion.UNAM, self.Seccion.ENTIDAD)
        return ComisionInstitucional.Ambito.INTERIOR if interior else ComisionInstitucional.Ambito.EXTERIOR


class ActividadApoyo(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField('descripción', blank=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'actividad de apoyo'
        verbose_name_plural = 'actividades de apoyo'

    def __str__(self):
        return self.nombre


class LaborDirectivaCoordinacion(Periodo):
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT)
    detalle = models.CharField(max_length=255, blank=True,
                               help_text='Laboratorio, unidad, programa o departamento (p. ej. Laboratorio de Drones).')
    institucion = models.ForeignKey(Institucion, on_delete=models.PROTECT, null=True, blank=True,
                                    verbose_name='institución')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='labores_directivas')

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'labor directiva o de coordinación'
        verbose_name_plural = 'labores directivas y de coordinación'

    def __str__(self):
        return f'{self.cargo} ({anio_o_sf(self.fecha_inicio)})'


class RepresentacionOrganoColegiado(Periodo):
    class Tipo(models.TextChoices):
        DENTRO = 'DENTRO', 'Dentro de la UNAM'
        REPRESENTACION = 'REPRESENTACION', 'Con representación UNAM (solo por designación)'

    class Organo(models.TextChoices):
        PRIDE = 'PRIDE', 'PRIDE'
        CAACS = 'CAACS', 'CAACS'
        CONSEJO_INTERNO = 'CONSEJO_INTERNO', 'Consejo interno'
        COMISION_DICTAMINADORA = 'COMISION_DICTAMINADORA', 'Comisión dictaminadora'
        COMISION_EVALUADORA = 'COMISION_EVALUADORA', 'Comisión evaluadora'
        OTRA = 'OTRA', 'Otra'

    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    organo = models.CharField('órgano colegiado', max_length=30, choices=Organo.choices, blank=True)
    organo_descripcion = models.CharField('descripción del órgano', max_length=250, blank=True,
                                          help_text='Obligatoria si el órgano es "Otra" o está fuera de la UNAM.')
    institucion = models.ForeignKey(Institucion, on_delete=models.PROTECT, null=True, blank=True,
                                    verbose_name='institución')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='representaciones')

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'representación ante órgano colegiado'
        verbose_name_plural = 'representaciones ante órganos colegiados'

    def __str__(self):
        return self.organo_descripcion or self.get_organo_display()

    def clean(self):
        super().clean()
        requerido_si(self.tipo == self.Tipo.DENTRO, self, 'organo', 'Elige el órgano colegiado.')
        requerido_si(self.organo == self.Organo.OTRA or self.tipo == self.Tipo.REPRESENTACION, self,
                     'organo_descripcion', 'Describe el órgano colegiado.')


class ComisionInstitucional(Periodo):
    class Ambito(models.TextChoices):
        INTERIOR = 'INTERIOR', 'Al interior de la entidad'
        EXTERIOR = 'EXTERIOR', 'Al exterior de la entidad'

    class Funcion(models.TextChoices):
        PRESIDENTE = 'PRESIDENTE', 'Presidente(a)'
        COORDINADOR = 'COORDINADOR', 'Coordinador(a)'
        SECRETARIO = 'SECRETARIO', 'Secretario(a)'
        SECRETARIO_TECNICO = 'SECRETARIO_TECNICO', 'Secretario(a) técnico(a)'
        VOCAL = 'VOCAL', 'Vocal'
        INTEGRANTE = 'INTEGRANTE', 'Integrante'
        TITULAR = 'TITULAR', 'Representante propietario(a) / titular'
        SUPLENTE = 'SUPLENTE', 'Representante suplente'
        EVALUADOR = 'EVALUADOR', 'Evaluador(a) / dictaminador(a)'
        JURADO = 'JURADO', 'Jurado'
        COMENTARISTA = 'COMENTARISTA', 'Comentarista / moderador(a)'
        ENLACE = 'ENLACE', 'Enlace institucional'
        ASESOR = 'ASESOR', 'Asesor(a)'

    comision = models.ForeignKey(Comision, on_delete=models.PROTECT, verbose_name='comisión')
    funcion = models.CharField('función', max_length=20, choices=Funcion.choices, default=Funcion.INTEGRANTE)
    detalle = models.CharField(max_length=255, blank=True,
                               help_text='Programa, convocatoria o nombre específico (según indique la comisión).')
    ambito = models.CharField('ámbito', max_length=20, choices=Ambito.choices)
    institucion = models.ForeignKey(Institucion, on_delete=models.PROTECT, null=True, blank=True,
                                    verbose_name='institución')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='comisiones')

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'comisión institucional'
        verbose_name_plural = 'comisiones institucionales'

    def __str__(self):
        return str(self.comision)


class ApoyoInstitucional(Periodo):
    class Tipo(models.TextChoices):
        TECNICO = 'TECNICO', 'Apoyo técnico'
        OTRA = 'OTRA', 'Apoyo en otras actividades'

    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    actividad = models.ForeignKey(ActividadApoyo, on_delete=models.PROTECT)
    descripcion = models.TextField('descripción', blank=True)
    institucion = models.ForeignKey(Institucion, on_delete=models.PROTECT, verbose_name='institución')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='apoyos_institucionales')

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'apoyo institucional'
        verbose_name_plural = 'apoyos institucionales'

    def __str__(self):
        return f'{self.actividad} ({anio_o_sf(self.fecha_inicio)})'


from nucleo.historial import registrar_historial  # noqa: E402

registrar_historial(globals())
