from django.db import models
from django.conf import settings
from django.urls import reverse
from nucleo.models import User, Pais, Ciudad, Institucion, InstitucionSimple, Dependencia, \
    Revista, Indice, Libro as LibroInvestigacion, Editorial, Coleccion, ProblemaNacionalConacyt, Financiamiento, Metodologia, \
    AreaEspecialidad, ImpactoSocial, AreaConocimiento
from sortedm2m.fields import SortedManyToManyField


STATUS_PUBLICACION_ARTICULO = getattr(settings, 'STATUS_PUBLICACION_ARTICULO',
                                      (('PUBLICADO', 'Publicado'), ('EN_PRENSA', 'En prensa'), ('ACEPTADO', 'Aceptado'),
                                       ('ENVIADO', 'Enviado')))

STATUS_PUBLICACION = getattr(settings, 'STATUS_PUBLICACION', (('PUBLICADO', 'Publicado'), ('EN_PRENSA', 'En prensa'),
                                                              ('ACEPTADO', 'Aceptado'), ('ENVIADO', 'Enviado')))

STATUS_PROYECTO = getattr(settings, 'STATUS_PROYECTO', (('NUEVO', 'Nuevo'), ('EN_PROCESO', 'En proceso'),
                                                        ('CONCLUIDO', 'Concluído')))
CLASIFICACION_PROYECTO = getattr(settings,
                                 'CLASIFICACION_PROYECTO', (('BASICO', 'Ciencia Básica'),
                                                            ('APLICADO', 'Investigaciòn Aplicada'),
                                                            ('DESARROLLO_TECNOLOGICO', 'Desarrollo tecnológico'),
                                                            ('INNOVACION', 'Innovación'),
                                                            ('INVESTIGACION_FRONTERA', 'Investigación de frontera')))
ORGANIZACION_PROYECTO = getattr(settings, 'ORGANIZACION_PROYECTO', (('INDIVIDUAL', 'Individual'),
                                                                    ('COLECTIVO', 'Colectivo')))
MODALIDAD_PROYECTO = getattr(settings, 'MODALIDAD_PROYECTO', (('DISCIPLINARIO', 'Disciplinario'),
                                                              ('MULTIDISCIPLINARIO', 'Multidisciplinario'),
                                                              ('INTERDISCIPLINARIO', 'Interisciplinario'),
                                                              ('TRANSDISCIPLINARIO', 'Transdisciplinario')))
FINANCIAMIENTO_UNAM = getattr(settings,
                              'FINANCIAMIENTO_UNAM', (('ASIGNADO', 'Presupuesto asignado a la entidad'),
                                                      ('CONCURSADO', 'Presupuesto concursado por la entidad'),
                                                      ('AUTOGENERADO', 'Recursos autogenerados (extraordinarios)'),
                                                      ('OTRO', 'Otro')))
FINANCIAMIENTO_EXTERNO = getattr(settings, 'FINANCIAMIENTO_UNAM', (('ESTATAL', 'Gubernamental Estatal'),
                                                                   ('FEDERAL', 'Gubernamental Federal'),
                                                                   ('LUCRATIVO', 'Privado lucrativo'),
                                                                   ('NO_LUCRATIVO', 'Privado no lucrativo'),
                                                                   ('EXTRANJERO', 'Recursos del extranjero'),
                                                                   ('OTRO', 'Otro')))
FINANCIAMIENTO_TIPO = getattr(settings, 'FINANCIAMIENTO_TIPO',
                              (('UNAM', FINANCIAMIENTO_UNAM), ('Externo', FINANCIAMIENTO_EXTERNO)))


# Create your models here.


class ObjetivoDesarrolloSostenible(models.Model):
    objetivodesarrollosostenible_nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.pk) + ".- " + self.objetivodesarrollosostenible_nombre

    class Meta:
        ordering = ['pk']



class ProyectoInvestigacion(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)
    es_permanente = models.BooleanField(default=False)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    institucion = models.ForeignKey(InstitucionSimple, on_delete=models.DO_NOTHING, null=True, blank=True)
    responsables = SortedManyToManyField(User, related_name='proyecto_investigacion_responsables',
                                         verbose_name='Responsables')
    participantes = models.ManyToManyField(User, related_name='proyecto_investigacion_participantes', blank=True)
    participantes_externos_text = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=30, choices=STATUS_PROYECTO)
    clasificacion = models.CharField(max_length=30, choices=CLASIFICACION_PROYECTO)
    organizacion = models.CharField(max_length=30, choices=ORGANIZACION_PROYECTO)
    modalidad = models.CharField(max_length=30, choices=MODALIDAD_PROYECTO)
    tematica_genero = models.BooleanField(default=False)
    objetivos2030 = models.ManyToManyField(ObjetivoDesarrolloSostenible, blank=True)

    tipo_financiamiento = models.CharField(max_length=30, choices=(('', '-------'), ('CONACYT', 'CONACYT'), ('PAPIIT', 'DGAPA-PAPIIT'), ('PAPIME', 'DGAPA-PAPIME'), ('EXTRAORDINARIOS', 'Ingresos extraordinarios'), ('SIN_RECURSOS', 'Sin recursos en el CIGA (en colaboración con otras dependencias)')))

    financiamiento_conacyt_clave = models.CharField(max_length=30, unique=True, null=True, blank=True)
    financiamiento_conacyt_convocatoria = models.CharField(max_length=160,  null=True, blank=True)
    financiamiento_papiit = models.CharField(max_length=30, unique=True, null=True, blank=True)
    financiamiento_papime = models.CharField(max_length=30, unique=True, null=True, blank=True)
    financiamiento_extraordinario = models.ForeignKey(InstitucionSimple, null=True, blank=True, on_delete=models.DO_NOTHING, related_name='proyecto_investigacion_financiamiento_extraordinario')
    financiamiento_sin_recurso_ciga = models.ForeignKey(InstitucionSimple, null=True, blank=True, on_delete=models.DO_NOTHING, related_name='proyecto_investigacion_financiamiento_sin_recurso_ciga')
    impacto_social_text = models.CharField(max_length=255, null=True, blank=True)
    num_alumnos_doctorado = models.PositiveIntegerField(null=True, blank=True)
    num_alumnos_maestria = models.PositiveIntegerField(null=True, blank=True)
    num_alumnos_licenciatura = models.PositiveIntegerField(null=True, blank=True)


    def __str__(self):
        if self.nombre == 'Ninguno':
            return 'Ninguno'
        else:
            return "{} : {}".format(self.nombre, self.fecha_inicio)

    def natural_key(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('proyecto_investigacion_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['nombre']


class ArticuloCientifico(models.Model):
    titulo = models.CharField(max_length=255, unique=True)
    revista = models.ForeignKey(Revista, on_delete=models.DO_NOTHING)
    volumen = models.CharField(max_length=100, null=True, blank=True)
    numero = models.CharField(max_length=100, null=True, blank=True)
    fecha_enviado = models.DateField(null=True, blank=True)
    fecha_aceptado = models.DateField(null=True, blank=True)
    fecha_enprensa = models.DateField(null=True, blank=True)
    fecha_publicado = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_PUBLICACION_ARTICULO)
    solo_electronico = models.BooleanField(default=False)
    autores = SortedManyToManyField(User, related_name='articulo_cientifico_autores', verbose_name='Autores')
    autores_todos = models.TextField(blank=True, null=True)
    alumnos = models.ManyToManyField(User, related_name='articulo_cientifico_alumnos', blank=True)
    agradecimientos = models.ManyToManyField(User, related_name='articulo_cientifico_agradecimientos', blank=True)
    factor_impacto = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)
    url = models.URLField(blank=True)
    pagina_inicio = models.PositiveIntegerField(null=True, blank=True)
    pagina_fin = models.PositiveIntegerField(null=True, blank=True)
    id_doi = models.CharField(max_length=100, null=True, blank=True)
    proyecto = models.ForeignKey(ProyectoInvestigacion, blank=True, null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{} : {}".format(self.titulo, self.revista)

    def get_absolute_url(self):
        return reverse('articulo_cientifico_detalle', kwargs={'pk': self.pk})

    def natural_key(self):
        return self.titulo

    class Meta:
        verbose_name = "Artículo científico"
        verbose_name_plural = "Artículos científicos"
        ordering = ['-fecha_publicado', '-fecha_enprensa', '-fecha_aceptado', '-fecha_enviado', 'titulo']


class CapituloLibroInvestigacion(models.Model):
    titulo = models.CharField(max_length=255, unique=True)
    libro = models.ForeignKey(LibroInvestigacion, on_delete=models.DO_NOTHING)
    pagina_inicio = models.PositiveIntegerField()
    pagina_fin = models.PositiveIntegerField()
    autores = SortedManyToManyField(User, related_name='capitulo_libro_investigacion_autores', verbose_name='Autores')
    autores_todos = models.TextField(blank=True, null=True)

    def __str__(self):
        return "{} : {}".format(self.titulo, self.libro)

    def get_absolute_url(self):
        return reverse('capitulo_libro_investigacion_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Capítulo en libro"
        verbose_name_plural = "Capítulos en libros"
        ordering = ['titulo']


class MapaArbitrado(models.Model):
    titulo = models.CharField(max_length=255, unique=True)
    autores = SortedManyToManyField(User, related_name='mapa_arbitrado_autores', verbose_name='Autores', blank=True)
    autores_todos = models.TextField(blank=True, null=True)
    agradecimientos = SortedManyToManyField(User, related_name='mapa_arbitrado_agradecimientos', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_PUBLICACION)
    pais = models.ForeignKey(Pais, on_delete=models.DO_NOTHING)
    ciudad_text = models.CharField(max_length=255, blank=True, null=True)
    publicacion = models.CharField(max_length=255, blank=True, null=True)
    fecha_enviado = models.DateField(null=True, blank=True)
    fecha_aceptado = models.DateField(null=True, blank=True)
    fecha_enprensa = models.DateField(null=True, blank=True)
    fecha_publicado = models.DateField(null=True, blank=True)
    numero_paginas = models.PositiveIntegerField(default=1)
    proyecto = models.ForeignKey(ProyectoInvestigacion, blank=True, null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{} : {}".format(self.titulo, self.publicacion)

    def get_absolute_url(self):
        return reverse('mapa_arbitrado_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Mapa arbitrado"
        verbose_name_plural = "Mapas arbitrados"


class PublicacionTecnica(models.Model):
    titulo = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=255, choices=(
        ('', '-------'), ('DESARROLLO_TECNOLOGICO', 'Desarrollo tecnológico terminado'),
        ('PROGRAMA_COMPUTO', 'Programa de cómputo especializado documentado'),
        ('BASE_DATOS', 'Bases de datos geográficos, arbitradas por expertos, para apliciones Web'),
        ('NORMA_PATENTE', 'Normas y patentes'),
        ('INFORME_TECNICO', 'Informes técnicos finales dirigidos a tomadores de decisiones'),
        ('PLAN_MANEJO', 'Planes de manejo, ordenamiento, y gestión territorial, reconocidos oficialmente'),
        ('CARTA_REVISTA', 'Cartas en revistas de prestigio internacional'),
        ('TRADUCCION', 'Traducción de libros y revisiones técnicas')))
    status = models.CharField(max_length=20, choices=STATUS_PUBLICACION)
    fecha_enviado = models.DateField(null=True, blank=True)
    fecha_aceptado = models.DateField(null=True, blank=True)
    fecha_enprensa = models.DateField(null=True, blank=True)
    fecha_publicado = models.DateField(null=True, blank=True)
    autores = SortedManyToManyField(User, related_name='informe_tecnico_autores', verbose_name='Autores')
    autores_todos = models.TextField(blank=True, null=True)
    institucion = models.ForeignKey(InstitucionSimple, on_delete=models.DO_NOTHING)
    proyecto = models.ForeignKey(ProyectoInvestigacion, on_delete=models.DO_NOTHING)
    es_publico = models.BooleanField(default=False)
    url = models.URLField(blank=True)
    cita = models.TextField(blank=True)

    def __str__(self):
        return "{} : {}".format(self.titulo, self.tipo)

    def get_absolute_url(self):
        return reverse('publicacion_tecnica_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Publicación técnico de acceso público"
        verbose_name_plural = "Publicaciones técnicas de acceso público"
        ordering = ['titulo']


class ActividadApoyoTecnicoInvestigacion(models.Model):
    actividadapoyotecnicoinvestigacion_nombre = models.CharField(max_length=160, unique=True)
    orden = models.IntegerField()

    def __str__(self):
        return self.actividadapoyotecnicoinvestigacion_nombre

    def natural_key(self):
        return self.actividadapoyotecnicoinvestigacion_nombre

    class Meta:
        ordering = ['orden', 'id']


class ActividadApoyoTecnicoServicio(models.Model):
    actividadapoyotecnicoservicio_nombre = models.CharField(max_length=160, unique=True)
    orden = models.IntegerField()

    def __str__(self):
        return self.actividadapoyotecnicoservicio_nombre

    def natural_key(self):
        return self.actividadapoyotecnicoservicio_nombre

    class Meta:
        ordering = ['orden', 'id']


class ApoyoTecnicoInvestigacion(models.Model):
    actividad = models.ForeignKey(ActividadApoyoTecnicoInvestigacion, on_delete=models.DO_NOTHING)
    actividad_otra = models.CharField(max_length=254, blank=True, null=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    proyecto = models.ForeignKey(ProyectoInvestigacion, on_delete=models.DO_NOTHING)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{}, {} ({})".format(self.actividad, self.usuario, self.fecha_inicio)

    def get_absolute_url(self):
        return reverse('apoyo_tecnico_investigacion_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Apoyo técnico en (o, a la) investigacion"
        verbose_name_plural = "Apoyos técnicos en (o, a la) investigacion"
        ordering = ['fecha_inicio', 'actividad']


class ApoyoTecnicoServicio(models.Model):
    actividad = models.ForeignKey(ActividadApoyoTecnicoServicio, on_delete=models.DO_NOTHING)
    actividad_otra = models.CharField(max_length=254, blank=True, null=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    proyecto = models.ForeignKey(ProyectoInvestigacion, on_delete=models.DO_NOTHING)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{}, {} ({})".format(self.actividad, self.usuario, self.fecha_inicio)

    def get_absolute_url(self):
        return reverse('apoyo_tecnico_servicio_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Apoyo técnico en actividades de servicio"
        verbose_name_plural = "Apoyos técnicos en actividades de servicio"
        ordering = ['fecha_inicio', 'actividad']