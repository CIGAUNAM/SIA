from django.conf import settings
from django.db import models

from nucleo.models import (Asignatura, EstadoPublicacion, Institucion, Modalidad, NivelAcademico, Participante, Periodo,
                           Persona, ProgramaAcademico, requerido_si, validar_paginas, validar_programa)


class CursoEscolarizado(Periodo):
    class Nombramiento(models.TextChoices):
        TITULAR = 'TITULAR', 'Titular o coordinador'
        COLABORADOR = 'COLABORADOR', 'Colaborador o invitado'

    nivel = models.CharField(max_length=20, choices=NivelAcademico.choices)
    programa = models.ForeignKey(ProgramaAcademico, on_delete=models.PROTECT, null=True, blank=True)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.PROTECT)
    modalidad = models.CharField(max_length=20, choices=Modalidad.choices)
    nombramiento = models.CharField(max_length=20, choices=Nombramiento.choices)
    institucion = models.ForeignKey(Institucion, on_delete=models.PROTECT, verbose_name='institución')
    periodo_academico = models.CharField('periodo académico', max_length=20)
    total_horas = models.PositiveIntegerField('total de horas')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='cursos_escolarizados')

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'curso escolarizado'
        verbose_name_plural = 'cursos escolarizados'

    def __str__(self):
        return f'{self.asignatura} ({self.periodo_academico})'

    def clean(self):
        super().clean()
        validar_programa(self)


class CursoExtracurricular(Periodo):
    class Tipo(models.TextChoices):
        CURSO = 'CURSO', 'Curso'
        DIPLOMADO = 'DIPLOMADO', 'Diplomado'
        TALLER = 'TALLER', 'Taller'
        SEMINARIO = 'SEMINARIO', 'Seminario'
        OTRO = 'OTRO', 'Otro'

    class Clasificacion(models.TextChoices):
        APOYO_POSGRADO = 'APOYO_POSGRADO', 'En apoyo al posgrado'
        CAPACITACION = 'CAPACITACION', 'Curso de capacitación'

    asignatura = models.ForeignKey(Asignatura, on_delete=models.PROTECT, verbose_name='nombre del curso')
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    tipo_otro = models.CharField('otro tipo', max_length=254, blank=True)
    clasificacion = models.CharField('clasificación', max_length=20, choices=Clasificacion.choices, blank=True)
    modalidad = models.CharField(max_length=20, choices=Modalidad.choices)
    institucion = models.ForeignKey(Institucion, on_delete=models.PROTECT, verbose_name='institución')
    periodo_academico = models.CharField('periodo académico', max_length=20, blank=True)
    total_horas = models.PositiveIntegerField('total de horas')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                related_name='cursos_extracurriculares')

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'curso extracurricular'
        verbose_name_plural = 'cursos extracurriculares'

    def __str__(self):
        return f'{self.asignatura} ({self.fecha_inicio:%Y})'

    def clean(self):
        super().clean()
        requerido_si(self.tipo == self.Tipo.OTRO, self, 'tipo_otro', 'Describe el tipo de curso.')


class ArticuloDocencia(EstadoPublicacion):
    titulo = models.CharField('título', max_length=255, unique=True)
    pagina_inicio = models.PositiveIntegerField('página inicial', null=True, blank=True)
    pagina_fin = models.PositiveIntegerField('página final', null=True, blank=True)
    url = models.URLField('URL', blank=True)
    solo_electronico = models.BooleanField('solo electrónico', default=False)
    autores = models.ManyToManyField(Persona, through='ArticuloDocenciaAutor', related_name='articulos_docencia')
    alumnos = models.ManyToManyField(Persona, blank=True, related_name='articulos_docencia_alumno')
    agradecimientos = models.ManyToManyField(Persona, blank=True, related_name='articulos_docencia_agradecimiento')

    class Meta:
        ordering = ['-fecha_publicado', '-fecha_enprensa', '-fecha_aceptado', '-fecha_enviado', 'titulo']
        verbose_name = 'artículo para docencia'
        verbose_name_plural = 'artículos para docencia'

    def __str__(self):
        return self.titulo

    def clean(self):
        super().clean()
        validar_paginas(self)


class ArticuloDocenciaAutor(Participante):
    articulo = models.ForeignKey(ArticuloDocencia, on_delete=models.CASCADE)

    class Meta(Participante.Meta):
        verbose_name = 'autor'
        verbose_name_plural = 'autores'
        constraints = [models.UniqueConstraint(fields=['articulo', 'persona'], name='articulo_docencia_autor_unico')]


class ProgramaEstudio(models.Model):
    class Nivel(models.TextChoices):
        LICENCIATURA = 'LICENCIATURA', 'Licenciatura'
        MAESTRIA = 'MAESTRIA', 'Maestría'
        DOCTORADO = 'DOCTORADO', 'Doctorado'
        OTRO = 'OTRO', 'Otro'

    nombre = models.CharField(max_length=254)
    descripcion = models.TextField('descripción', blank=True)
    nivel = models.CharField(max_length=20, choices=Nivel.choices)
    fecha = models.DateField()
    institucion = models.ForeignKey(Institucion, on_delete=models.PROTECT, verbose_name='institución')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='programas_estudio')

    class Meta:
        ordering = ['-fecha', 'nombre']
        verbose_name = 'programa de estudio'
        verbose_name_plural = 'programas de estudio'

    def __str__(self):
        return f'{self.nombre} ({self.get_nivel_display()})'


from nucleo.historial import registrar_historial  # noqa: E402

registrar_historial(globals())
