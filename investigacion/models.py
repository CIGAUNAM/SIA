from cities_light.models import Country
from django.conf import settings
from django.db import models

from nucleo.models import (anio_o_sf, EstadoPublicacion, Institucion, Participante, Periodo, Persona,
                           Revista, normalizar_doi, requerido_si, validar_paginas)


class ObjetivoDesarrolloSostenible(models.Model):
    numero = models.PositiveSmallIntegerField('número', unique=True)
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['numero']
        verbose_name = 'objetivo de desarrollo sostenible'
        verbose_name_plural = 'objetivos de desarrollo sostenible'

    def __str__(self):
        return f'{self.numero}. {self.nombre}'


class ProyectoInvestigacion(Periodo):
    class Status(models.TextChoices):
        NUEVO = 'NUEVO', 'Nuevo'
        EN_PROCESO = 'EN_PROCESO', 'En proceso'
        CONCLUIDO = 'CONCLUIDO', 'Concluido'

    class Clasificacion(models.TextChoices):
        BASICO = 'BASICO', 'Ciencia básica'
        APLICADO = 'APLICADO', 'Investigación aplicada'
        DESARROLLO_TECNOLOGICO = 'DESARROLLO_TECNOLOGICO', 'Desarrollo tecnológico'
        INNOVACION = 'INNOVACION', 'Innovación'
        INVESTIGACION_FRONTERA = 'INVESTIGACION_FRONTERA', 'Investigación de frontera'

    class Organizacion(models.TextChoices):
        INDIVIDUAL = 'INDIVIDUAL', 'Individual'
        COLECTIVO = 'COLECTIVO', 'Colectivo'

    class ModalidadProyecto(models.TextChoices):
        DISCIPLINARIO = 'DISCIPLINARIO', 'Disciplinario'
        MULTIDISCIPLINARIO = 'MULTIDISCIPLINARIO', 'Multidisciplinario'
        INTERDISCIPLINARIO = 'INTERDISCIPLINARIO', 'Interdisciplinario'
        TRANSDISCIPLINARIO = 'TRANSDISCIPLINARIO', 'Transdisciplinario'

    class Financiamiento(models.TextChoices):
        CONACYT = 'CONACYT', 'SECIHTI (antes CONAHCYT)'
        PAPIIT = 'PAPIIT', 'DGAPA-PAPIIT'
        PAPIME = 'PAPIME', 'DGAPA-PAPIME'
        EXTRAORDINARIOS = 'EXTRAORDINARIOS', 'Ingresos extraordinarios'
        SIN_RECURSOS = 'SIN_RECURSOS', 'Sin recursos propios (en colaboración con otras dependencias)'

    class FinanciamientoUNAM(models.TextChoices):
        CONCURSADO = 'CONCURSADO', 'Presupuesto concursado por la entidad'
        FUERA = 'FUERA', 'Gestionado fuera de la entidad'
        AUTOGENERADOS = 'AUTOGENERADOS', 'Recursos autogenerados (extraordinarios)'

    class FinanciamientoExterno(models.TextChoices):
        FEDERAL = 'FEDERAL', 'Gubernamental federal'
        ESTATAL = 'ESTATAL', 'Gubernamental estatal'
        MUNICIPAL = 'MUNICIPAL', 'Gubernamental municipal'
        EXTRANJERO = 'EXTRANJERO', 'Recursos del extranjero'
        PRIVADO = 'PRIVADO', 'Privado'
        PRIVADO_NO_LUCRATIVO = 'PRIVADO_NO_LUCRATIVO', 'Privado no lucrativo'

    class Prioridad(models.TextChoices):
        """Programas Nacionales Estratégicos de SECIHTI (problemas nacionales prioritarios)."""
        AGENTES_TOXICOS = 'AGENTES_TOXICOS', 'Agentes tóxicos y procesos contaminantes'
        AGUA = 'AGUA', 'Agua'
        CULTURA = 'CULTURA', 'Cultura'
        EDUCACION = 'EDUCACION', 'Educación'
        ENERGIA = 'ENERGIA', 'Energía y cambio climático'
        SALUD = 'SALUD', 'Salud'
        SEGURIDAD = 'SEGURIDAD', 'Seguridad humana'
        SOCIOECOLOGICOS = 'SOCIOECOLOGICOS', 'Sistemas socioecológicos y sustentabilidad'
        SOBERANIA_ALIMENTARIA = 'SOBERANIA_ALIMENTARIA', 'Soberanía alimentaria'
        VIVIENDA = 'VIVIENDA', 'Vivienda'

    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField('descripción', blank=True)
    es_permanente = models.BooleanField('es permanente', default=False,
                                        help_text='Proyecto sin término previsto (p. ej. un observatorio o laboratorio).')
    institucion = models.ForeignKey(Institucion, on_delete=models.PROTECT, null=True, blank=True,
                                    verbose_name='institución')
    responsables = models.ManyToManyField(Persona, through='ProyectoResponsable', related_name='proyectos_responsable')
    participantes = models.ManyToManyField(Persona, blank=True, related_name='proyectos_participante')
    participantes_externos = models.TextField(blank=True, help_text='Participantes que no están registrados como personas.')
    status = models.CharField('estado', max_length=20, choices=Status.choices)
    clasificacion = models.CharField('clasificación', max_length=30, choices=Clasificacion.choices)
    organizacion = models.CharField('organización', max_length=20, choices=Organizacion.choices)
    modalidad = models.CharField(max_length=20, choices=ModalidadProyecto.choices)
    tematica_genero = models.BooleanField('temática de género', default=False,
                                          help_text='El proyecto aborda la perspectiva o la temática de género.')
    objetivos_ods = models.ManyToManyField(ObjetivoDesarrolloSostenible, blank=True,
                                           verbose_name='objetivos de desarrollo sostenible')
    impacto_social = models.CharField(max_length=255, blank=True)
    financiamiento = models.CharField(max_length=20, choices=Financiamiento.choices, blank=True)
    financiamiento_unam = models.CharField('financiamiento UNAM', max_length=20, choices=FinanciamientoUNAM.choices,
                                           blank=True)
    financiamiento_externo = models.CharField(max_length=30, choices=FinanciamientoExterno.choices, blank=True)
    prioridad = models.CharField('prioridad estratégica nacional', max_length=30, choices=Prioridad.choices,
                                 blank=True)
    financiamiento_clave = models.CharField('clave del financiamiento', max_length=30, blank=True,
                                           help_text='Obligatoria para proyectos CONAHCYT, PAPIIT y PAPIME.')
    financiamiento_convocatoria = models.CharField('convocatoria', max_length=160, blank=True)
    financiamiento_institucion = models.ForeignKey(
        Institucion, on_delete=models.PROTECT, null=True, blank=True, related_name='proyectos_financiados',
        verbose_name='institución que financia o colabora')
    num_alumnos_licenciatura = models.PositiveIntegerField('alumnos de licenciatura', default=0)
    num_alumnos_maestria = models.PositiveIntegerField('alumnos de maestría', default=0)
    num_alumnos_doctorado = models.PositiveIntegerField('alumnos de doctorado', default=0)

    class Meta:
        ordering = ['-fecha_inicio', 'nombre']
        verbose_name = 'proyecto de investigación'
        verbose_name_plural = 'proyectos de investigación'

    def __str__(self):
        return self.nombre

    def clean(self):
        super().clean()
        F = self.Financiamiento
        requerido_si(self.financiamiento in (F.CONACYT, F.PAPIIT, F.PAPIME), self, 'financiamiento_clave',
                     'Indica la clave del proyecto en la convocatoria.')
        requerido_si(self.financiamiento in (F.EXTRAORDINARIOS, F.SIN_RECURSOS), self, 'financiamiento_institucion',
                     'Indica la institución que financia o con la que se colabora.')


class ProyectoResponsable(Participante):
    proyecto = models.ForeignKey(ProyectoInvestigacion, on_delete=models.CASCADE)

    class Meta(Participante.Meta):
        verbose_name = 'responsable'
        verbose_name_plural = 'responsables'
        constraints = [models.UniqueConstraint(fields=['proyecto', 'persona'], name='proyecto_responsable_unico')]


class ArticuloCientifico(EstadoPublicacion):
    titulo = models.CharField('título', max_length=255, unique=True)
    revista = models.ForeignKey(Revista, on_delete=models.PROTECT)
    volumen = models.CharField(max_length=100, blank=True)
    numero = models.CharField('número', max_length=100, blank=True)
    pagina_inicio = models.PositiveIntegerField('página inicial', null=True, blank=True)
    pagina_fin = models.PositiveIntegerField('página final', null=True, blank=True)
    doi = models.CharField('DOI', max_length=100, blank=True)
    url = models.URLField('URL', blank=True)
    solo_electronico = models.BooleanField('solo electrónico', default=False,
                                           help_text='El artículo solo se publicó en formato electrónico.')
    factor_impacto = models.DecimalField(
        'factor de impacto', max_digits=6, decimal_places=3, null=True, blank=True,
        help_text='Histórico capturado en el artículo. Si está vacío se usa el registrado en la revista para el año.')
    autores = models.ManyToManyField(Persona, through='ArticuloCientificoAutor', related_name='articulos_cientificos')
    alumnos = models.ManyToManyField(Persona, blank=True, related_name='articulos_cientificos_alumno',
                                     help_text='Coautores que eran estudiantes al momento de publicar.')
    agradecimientos = models.ManyToManyField(Persona, blank=True, related_name='articulos_cientificos_agradecimiento',
                                             help_text='Académicos de la entidad mencionados en los agradecimientos.')
    proyecto = models.ForeignKey(ProyectoInvestigacion, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-fecha_publicado', '-fecha_enprensa', '-fecha_aceptado', '-fecha_enviado', 'titulo']
        verbose_name = 'artículo científico'
        verbose_name_plural = 'artículos científicos'

    def __str__(self):
        return self.titulo

    def clean(self):
        super().clean()
        validar_paginas(self)

    def save(self, *args, **kwargs):
        self.doi = normalizar_doi(self.doi)
        super().save(*args, **kwargs)

    @property
    def factor_impacto_vigente(self):
        if self.factor_impacto is not None:
            return self.factor_impacto
        return self.revista.factor_impacto(self.fecha.year) if self.fecha else None


class ArticuloCientificoAutor(Participante):
    articulo = models.ForeignKey(ArticuloCientifico, on_delete=models.CASCADE)

    class Meta(Participante.Meta):
        verbose_name = 'autor'
        verbose_name_plural = 'autores'
        constraints = [models.UniqueConstraint(fields=['articulo', 'persona'], name='articulo_cientifico_autor_unico')]


class MapaArbitrado(EstadoPublicacion):
    titulo = models.CharField('título', max_length=255, unique=True)
    publicacion = models.CharField('publicación o editorial', max_length=255, blank=True)
    pais = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name='país')
    ciudad = models.CharField(max_length=255, blank=True)
    numero_paginas = models.PositiveIntegerField('número de páginas', default=1)
    autores = models.ManyToManyField(Persona, through='MapaArbitradoAutor', related_name='mapas_arbitrados')
    agradecimientos = models.ManyToManyField(Persona, blank=True, related_name='mapas_arbitrados_agradecimiento')
    proyecto = models.ForeignKey(ProyectoInvestigacion, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['titulo']
        verbose_name = 'mapa arbitrado'
        verbose_name_plural = 'mapas arbitrados'

    def __str__(self):
        return self.titulo


class MapaArbitradoAutor(Participante):
    mapa = models.ForeignKey(MapaArbitrado, on_delete=models.CASCADE)

    class Meta(Participante.Meta):
        verbose_name = 'autor'
        verbose_name_plural = 'autores'
        constraints = [models.UniqueConstraint(fields=['mapa', 'persona'], name='mapa_autor_unico')]


class PublicacionTecnica(EstadoPublicacion):
    class Tipo(models.TextChoices):
        DESARROLLO_TECNOLOGICO = 'DESARROLLO_TECNOLOGICO', 'Desarrollo tecnológico terminado'
        PROGRAMA_COMPUTO = 'PROGRAMA_COMPUTO', 'Programa de cómputo especializado documentado'
        BASE_DATOS = 'BASE_DATOS', 'Base de datos geográficos arbitrada por expertos para aplicaciones web'
        NORMA_PATENTE = 'NORMA_PATENTE', 'Norma o patente'
        INFORME_TECNICO = 'INFORME_TECNICO', 'Informe técnico final dirigido a tomadores de decisiones'
        PLAN_MANEJO = 'PLAN_MANEJO', 'Plan de manejo, ordenamiento o gestión territorial reconocido oficialmente'
        RESENA = 'RESENA', 'Reseña'
        CARTA_REVISTA = 'CARTA_REVISTA', 'Carta en revista de prestigio internacional'
        TRADUCCION = 'TRADUCCION', 'Traducción de libro o revisión técnica'

    titulo = models.CharField('título', max_length=255, unique=True)
    tipo = models.CharField(max_length=30, choices=Tipo.choices)
    descripcion = models.TextField('descripción', blank=True)
    autores = models.ManyToManyField(Persona, through='PublicacionTecnicaAutor', related_name='publicaciones_tecnicas')
    institucion = models.ForeignKey(Institucion, on_delete=models.PROTECT, verbose_name='institución')
    proyecto = models.ForeignKey(ProyectoInvestigacion, on_delete=models.SET_NULL, null=True, blank=True)
    es_publico = models.BooleanField('es de acceso público', default=False,
                                     help_text='Cualquier persona puede consultarla (p. ej. en un repositorio abierto).')
    url = models.URLField('URL', blank=True)
    cita = models.TextField(blank=True)

    class Meta:
        ordering = ['titulo']
        verbose_name = 'publicación técnica'
        verbose_name_plural = 'publicaciones técnicas'

    def __str__(self):
        return self.titulo


class PublicacionTecnicaAutor(Participante):
    publicacion = models.ForeignKey(PublicacionTecnica, on_delete=models.CASCADE)

    class Meta(Participante.Meta):
        verbose_name = 'autor'
        verbose_name_plural = 'autores'
        constraints = [models.UniqueConstraint(fields=['publicacion', 'persona'], name='publicacion_tecnica_autor_unico')]


class ActividadApoyoTecnico(models.Model):
    class Tipo(models.TextChoices):
        INVESTIGACION = 'INVESTIGACION', 'Apoyo a la investigación'
        SERVICIO = 'SERVICIO', 'Apoyo a actividades de servicio'

    nombre = models.CharField(max_length=160)
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    orden = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['tipo', 'orden', 'pk']
        verbose_name = 'actividad de apoyo técnico'
        verbose_name_plural = 'actividades de apoyo técnico'
        constraints = [models.UniqueConstraint(fields=['nombre', 'tipo'], name='actividad_apoyo_tecnico_unica')]

    def __str__(self):
        return self.nombre


class ApoyoTecnico(Periodo):
    actividad = models.ForeignKey(ActividadApoyoTecnico, on_delete=models.PROTECT)
    actividad_otra = models.CharField('otra actividad', max_length=254, blank=True)
    proyecto = models.ForeignKey(ProyectoInvestigacion, on_delete=models.SET_NULL, null=True, blank=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'apoyo técnico'
        verbose_name_plural = 'apoyos técnicos'

    def __str__(self):
        return f'{self.actividad_otra or self.actividad} ({anio_o_sf(self.fecha_inicio)})'


from nucleo.historial import registrar_historial  # noqa: E402

registrar_historial(globals())
