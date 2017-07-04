from django.db import models

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.conf import settings
from autoslug import AutoSlugField


STATUS_PROYECTO = getattr(settings, 'STATUS_PROYECTO', (('NUEVO', 'Nuevo'), ('EN_PROCESO', 'En proceso'), ('CONCLUIDO', 'Concluído'), ('OTRO', 'Otro')))
CLASIFICACION_PROYECTO = getattr(settings, 'CLASIFICACION_PROYECTO', (('BASICO', 'Básico'), ('APLICADO', 'Aplicado'), ('DESARROLLO_TECNOLOGICO', 'Desarrollo tecnológico'), ('INNOVACION', 'Innovación'), ('INVESTIGACION_FRONTERA', 'Investigación de frontera'), ('OTRO', 'Otro')))
ORGANIZACION_PROYECTO = getattr(settings, 'ORGANIZACION_PROYECTO', (('INDIVIDUAL', 'Individual'), ('COLECTIVO', 'Colectivo')))
MODALIDAD_PROYECTO = getattr(settings, 'MODALIDAD_PROYECTO', (('DISCIPLINARIO', 'Disciplinario'), ('MULTIDISCIPLINARIO', 'Multidisciplinario'), ('INTERDISCIPLINARIO', 'Interisciplinario'), ('TRANSDISCIPLINARIO', 'Transdisciplinario'), ('OTRA', 'Otra')))
FINANCIAMIENTO_UNAM = getattr(settings, 'FINANCIAMIENTO_UNAM', (('ASIGNADO', 'Presupuesto asignado a la entidad'), ('CONCURSADO', 'Presupuesto concursado por la entidad'), ('AUTOGENERADO', 'Recursos autogenerados (extraordinarios)'), ('OTRO', 'Otro')))
FINANCIAMIENTO_EXTERNO = getattr(settings, 'FINANCIAMIENTO_UNAM', (('ESTATAL', 'Gubernamental Estatal'), ('FEDERAL', 'Gubernamental Federal'), ('LUCRATIVO', 'Privado lucrativo'), ('NO_LUCRATIVO', 'Privado no lucrativo'), ('EXTRANJERO', 'Recursos del extranjero'), ('OTRO', 'Otro')))
FINANCIAMIENTO_TIPO = getattr(settings, 'FINANCIAMIENTO_TIPO', (('UNAM', FINANCIAMIENTO_UNAM), ('Externo', FINANCIAMIENTO_EXTERNO)))
CARGO__TIPO_CARGO  = getattr(settings, 'CARGO__TIPO_CARGO', (('ACADEMICO', 'Académico'), ('ADMINISTRATIVO', 'Administrativo')))
GRADO_ACADEMICO = getattr(settings, 'GRADO_ACADEMICO', (('LICENCIATURA', 'licenciatura'), ('MAESTRIA', 'Maestría'), ('DOCTORADO', 'Doctorado')))

STATUS_PUBLICACION = getattr(settings, 'STATUS_PUBLICACION', (('PUBLICADO', 'Publicado'), ('EN_PRENSA', 'En prensa'), ('ACEPTADO', 'Aceptado'), ('ENVIADO', 'Enviado'), ('OTRO', 'Otro')))

# Create your models here.

"""
class Tag(models.Model):
    tag = models.CharField(max_length=50, unique=True, help_text='Etiqueta para categorizar objetos.')
    #slug = AutoSlugField(populate_from='tag')

    def __str__(self):
        return self.tag

    def natural_key(self):
        return (self.tag)

    class Meta:
        ordering = ['tag']
"""

class ZonaPais(models.Model):
    nombre = models.CharField(max_length=60, unique=True)
    #slug = AutoSlugField(populate_from='zona')

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return (self.nombre)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Zona de paises'
        verbose_name_plural = 'Zonas de paises'


class Pais(models.Model):
    nombre = models.CharField(max_length=60, unique=True)
    #slug = AutoSlugField(populate_from='pais', unique=True)
    nombre_extendido = models.CharField(max_length=200, unique=True)
    codigo = models.SlugField(max_length=2, unique=True)
    zona = models.ForeignKey(ZonaPais)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return (self.nombre)

    def get_absolute_url(self):
        return reverse('pais_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['nombre']
        verbose_name_plural = 'Paises'
        verbose_name = 'País'


class Estado(models.Model):
    nombre = models.CharField(max_length=200)
    #slug = AutoSlugField(populate_from='estado')
    pais = models.ForeignKey(Pais)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('estado_detalle', kwargs={'pk': self.pk})

    class Meta:
        unique_together = ['nombre', 'pais']
        ordering = ['nombre']


class Ciudad(models.Model):
    nombre = models.CharField(max_length=255)
    #slug = AutoSlugField(populate_from='ciudad')
    estado = models.ForeignKey(Estado)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('ciudad_detalle', kwargs={'pk': self.pk})

    class Meta:
        unique_together = ['nombre', 'estado']
        ordering = ['nombre']
        verbose_name_plural = 'Ciudades'

"""
class Region(models.Model):
    region = models.CharField(max_length=200)
    #slug = AutoSlugField(populate_from='region', unique=True)
    descripcion = models.TextField(blank=True)
    paises = models.ManyToManyField(Pais, related_name='region_paises', blank=True)
    estados = models.ManyToManyField(Estado, related_name='region_estados', blank=True)
    ciudades = models.ManyToManyField(Ciudad, related_name='region_ciudades', blank=True)

    def __str__(self):
        return self.region

    def natural_key(self):
        return (self.region)

    class Meta:
        ordering = ['region']
        verbose_name = 'Región'
        verbose_name_plural = 'Regiones'


class Ubicacion(models.Model):
    direccion1 = models.CharField('Dirección', max_length=255)
    direccion2 = models.CharField('Dirección (continuación)', blank=True, max_length=255)
    #slug = AutoSlugField(populate_from='direccion1', unique=True)
    descripcion = models.TextField(blank=True)
    ciudad = models.ForeignKey(Ciudad)
    codigo_postal = models.CharField(max_length=7, blank=True)
    telefono = models.SlugField(max_length=20, blank=True)

    def __str__(self):
        return "{} : {} : {}".format(self.direccion1, self.direccion2, self.ciudad)

    def natural_key(self):
        return (self.direccion1)

    class Meta:
        ordering = ['ciudad', 'direccion1']
        unique_together = ['direccion1', 'direccion2', 'ciudad']
        verbose_name = 'Ubicación'
        verbose_name_plural = 'Ubicaciones'
"""


class User(AbstractUser):
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=30, choices=(('INVESTIGADOR', 'Investigador'), ('ADMINISTRATIVO', 'Administrativo'), ('TECNICO', 'Técnico'), ('OTRO', 'Otro')), default='OTRO')
    fecha_nacimiento = models.DateField(null=True, blank=True)
    pais_origen = models.ForeignKey(Pais, default=1)
    rfc = models.SlugField(max_length=20, blank=True)
    direccion1 = models.CharField(max_length=255, blank=True)
    direccion2 = models.CharField(max_length=255, blank=True)
    ciudad = models.ForeignKey(Ciudad, default=1)
    telefono = models.SlugField(max_length=20, blank=True)
    celular = models.SlugField(max_length=20, blank=True)
    url = models.URLField(blank=True, null=True)
    sni = models.PositiveSmallIntegerField(default=0)
    pride = models.CharField(max_length=2, choices=(('-', '-'), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')), default='-')
    ingreso_unam = models.DateField(null=True, blank=True)
    ingreso_entidad = models.DateField(null=True, blank=True)

    def __str__(self):
        return "{} {} ".format(self.first_name, self.last_name)

    def natural_key(self):
        return "{} {} ".format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('usuario_detalle', kwargs={'pk': self.pk})

    class Meta:
        #ordering = ['first_name', 'last_name']
        pass


class Institucion(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    #slug = AutoSlugField(populate_from='institucion', max_length=255, unique=True)
    descripcion = models.TextField(blank=True)
    pais = models.ForeignKey(Pais)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return (self.nombre)

    def get_absolute_url(self):
        return reverse('institucion_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Institución'
        verbose_name_plural = 'Instituciones'


class Dependencia(models.Model):
    nombre = models.CharField(max_length=255)
    #slug = AutoSlugField(populate_from='dependencia', max_length=255, unique=True)
    descripcion = models.TextField(blank=True)
    institucion = models.ForeignKey(Institucion)
    ciudad = models.ForeignKey(Ciudad)
    subsistema_unam = models.CharField(max_length=50, choices=(('DIFUSION_CULTURAL', 'Subsistema de Difusión Cultural'),
                                                          ('ESTUDIOS_POSGRADO', 'Subsistema de Estudios de Posgrado'),
                                                          ('HUMANIDADES', 'Subsistema de Humanidades'),
                                                          ('INVESTIGACION_CIENTIFICA', 'Subsistema de Investigación Científica'),
                                                          ('ESCUELAS', 'Facultades y Escuelas'),
                                                          ('DESARROLLO_INSTITUCIONAL', 'Desarrollo Institucional'),
                                                          ('NO', 'No')), default='NO', verbose_name='Subsistema UNAM')

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return (self.nombre)

    def get_absolute_url(self):
        return reverse('dependencia_detalle', kwargs={'pk': self.pk})

    class Meta:
        unique_together = ('nombre', 'institucion')
        ordering = ['nombre']


class Departamento(models.Model):
    nombre = models.CharField(max_length=255)
    #slug = AutoSlugField(populate_from='dependencia', unique=True)
    descripcion = models.TextField(blank=True)
    dependencia = models.ForeignKey(Dependencia)


    def __str__(self):
        return self.nombre

    def natural_key(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('departamento_detalle', kwargs={'pk': self.pk})

    class Meta:
        unique_together = ('nombre', 'dependencia')
        ordering = ['nombre', 'dependencia']


class Cargo(models.Model):
    nombre = models.CharField(max_length=255)
    #slug = AutoSlugField(populate_from='nombre', unique=True)
    descripcion = models.TextField(blank=True)
    tipo_cargo = models.CharField(max_length=20, choices=(('ACADEMICO', 'Académico'), ('ADMINISTRATIVO', 'Administrativo'), ('OTRO', 'Otro')))

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return (self.nombre)

    def get_absolute_url(self):
        return reverse('cargo_detalle', kwargs={'pk': self.pk})

    class Meta:
        unique_together = ['nombre', 'tipo_cargo']
        ordering = ['nombre']



class Nombramiento(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    clave = models.CharField(max_length=20, unique=True)
    #slug = AutoSlugField(populate_from='nombramiento', unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return (self.nombre)

    def get_absolute_url(self):
        return reverse('nombramiento_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['id']


class AreaConocimiento(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    categoria = models.CharField(max_length=20, choices=(
            ('LSBM', 'Life Sciences and Biomedicine'), ('PHYS', 'Physical Sciences'), ('TECH', 'Technology'),
            ('ARTH', 'Arts and Humanities'), ('SS', 'Social Sciences'), ('ZTRA', 'Otra')))
    #slug = AutoSlugField(populate_from='area_conocimiento', unique=True)
    descripcion = models.TextField(blank=True)


    def __str__(self):
        return self.nombre

    def natural_key(self):
        return (self.nombre)

    def get_absolute_url(self):
        return reverse('area_conocimiento_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['categoria', 'nombre']
        verbose_name = 'Área General de Conocimiento'
        verbose_name_plural = 'Áreas Generales de Conocimiento'


class AreaEspecialidad(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    #slug = AutoSlugField(populate_from='especialidad', unique=True)
    descripcion = models.TextField(blank=True)
    area_conocimiento = models.ForeignKey(AreaConocimiento)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return (self.nombre)

    def get_absolute_url(self):
        return reverse('area_especialidad_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Área de especialidad de WOS y otras entidades'
        verbose_name_plural = 'Áreas de especialidades de WOS y otras entidades'


class ImpactoSocial(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    #slug = AutoSlugField(populate_from='impacto_social', unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return (self.nombre)

    def get_absolute_url(self):
        return reverse('impacto_social_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Impacto social'
        verbose_name_plural = 'Impactos sociales'

"""
class ProgramaFinanciamiento(models.Model):
    programa_financiamiento = models.CharField(max_length=255, unique=True)
    #slug = AutoSlugField(populate_from='programa_financiamiento', unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.programa_financiamiento

    def natural_key(self):
        return (self.programa_financiamiento)

    class Meta:
        ordering = ['programa_financiamiento']
"""

class Financiamiento(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    tipo_financiamiento = models.CharField(max_length=80, choices=FINANCIAMIENTO_TIPO)
    descripcion = models.TextField(blank=True)
    #programas_financiamiento = models.ManyToManyField(ProgramaFinanciamiento, related_name='financiamiento_programas_financiamiento', blank=True)
    dependencias_financiamiento = models.ManyToManyField(Dependencia, related_name='financiamiento_dependencias_financiamiento')
    #clave_proyecto = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return (self.tipo_financiamiento)

    def get_absolute_url(self):
        return reverse('financiamiento_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Financiamiento'
        verbose_name_plural = 'Financiamientos'


class Metodologia(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    #slug = AutoSlugField(populate_from='metodologia', unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return (self.nombre)

    def get_absolute_url(self):
        return reverse('metodologia_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['nombre']


class Beca(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    #slug = AutoSlugField(populate_from='beca', unique=True)
    descripcion = models.TextField(blank=True)
    #institucion = models.ForeignKey(Institucion)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return (self.nombre)

    def get_absolute_url(self):
        return reverse('beca_detalle', kwargs={'pk': self.pk})


class Reconocimiento(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    #slug = AutoSlugField(populate_from='reconocimiento', unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return (self.nombre)

    def get_absolute_url(self):
        return reverse('reconocimiento_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['nombre']


class ProgramaLicenciatura(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)
    #slug = AutoSlugField(populate_from='programa', unique=True)
    area_conocimiento = models.ForeignKey(AreaConocimiento, verbose_name='Área de conocimiento')

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return (self.nombre)

    def get_absolute_url(self):
        return reverse('programa_licenciatura_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Programa de licenciatura'
        verbose_name_plural = 'Programas de licenciatura'


class ProgramaMaestria(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)
    #slug = AutoSlugField(populate_from='programa', unique=True)
    area_conocimiento = models.ForeignKey(AreaConocimiento, verbose_name='Área de conocimiento')

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return (self.nombre)

    def get_absolute_url(self):
        return reverse('programa_maestria_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Programa de maestria'
        verbose_name_plural = 'Programas de maestria'


class ProgramaDoctorado(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)
    #slug = AutoSlugField(populate_from='programa', unique=True)
    area_conocimiento = models.ForeignKey(AreaConocimiento, verbose_name='Área de conocimiento')

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return (self.nombre)

    def get_absolute_url(self):
        return reverse('programa_doctorado_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Programa de doctorado'
        verbose_name_plural = 'Programas de doctorado'


class TipoEvento(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    #slug = AutoSlugField(populate_from='tipo_evento')
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return (self.nombre)

    def get_absolute_url(self):
        return reverse('tipo_evento_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Tipo de evento'
        verbose_name_plural = 'Tipos de eventos'


class Evento(models.Model):
    nombre = models.CharField(max_length=255)
    #slug = AutoSlugField(populate_from='nombre_evento', unique=True)
    descripcion = models.TextField(blank=True)
    tipo = models.ForeignKey(TipoEvento)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    dependencias = models.ManyToManyField(Dependencia, related_name='evento_dependencias')
    ubicacion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return (self.nombre)

    def get_absolute_url(self):
        return reverse('evento_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['fecha_inicio', 'nombre']
        unique_together = ['fecha_inicio', 'nombre']


class Distincion(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    tipo = models.CharField(max_length=30, choices=(
    ('PREMIO', 'Premio'), ('DISTINCION', 'Distinción'), ('RECONOCIMIENTO', 'Reconocimiento'), ('MEDALLA', 'Medalla'),
    ('GUGGENHEIM', 'Beca Guggenheim'), ('HONORIS_CAUSA', 'Doctorado Honoris Causa'), ('OTRO', 'Otro')))
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return (self.nombre)

    def get_absolute_url(self):
        return reverse('distincion_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Distinción'
        verbose_name_plural = 'Distinciones'


class ProblemaNacionalConacyt(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    #slug = AutoSlugField(populate_from='nombre', unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return (self.nombre)

    def get_absolute_url(self):
        return reverse('problema_nacional_conacyt_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = ['Problemática Nacional CONACYT']
        verbose_name_plural = ['Problemáticas Nacionales CONACYT']


class Proyecto(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    #slug = AutoSlugField(populate_from='nombre_proyecto', unique=True)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=50, choices=(('INVESTIGACION', 'Investigación'), ('OTRO', 'Otro')))
    es_permanente = models.BooleanField(default=False)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    usuarios = models.ManyToManyField(User, related_name='proyecto_responsables', verbose_name='Responsables')
    participantes = models.ManyToManyField(User, related_name='proyecto_participantes', blank=True)
    status = models.CharField(max_length=30, choices=STATUS_PROYECTO)
    clasificacion = models.CharField(max_length=30, choices=CLASIFICACION_PROYECTO)
    organizacion = models.CharField(max_length=30, choices=ORGANIZACION_PROYECTO)
    modalidad = models.CharField(max_length=30, choices=MODALIDAD_PROYECTO)
    tematica_genero = models.BooleanField(default=False)
    problema_nacional_conacyt = models.ForeignKey(ProblemaNacionalConacyt, blank=True, null=True)
    descripcion_problema_nacional_conacyt = models.TextField(blank=True)
    dependencias = models.ManyToManyField(Dependencia, related_name='proyecto_dependencias', blank=True)
    financiamientos = models.ManyToManyField(Financiamiento, blank=True)
    metodologias = models.ManyToManyField(Metodologia, related_name='proyecto_metodologias', blank=True)
    especialidades = models.ManyToManyField(AreaEspecialidad, related_name='proyecto_especialidades', blank=True)
    impactos_sociales = models.ManyToManyField(ImpactoSocial, related_name='proyecto_impactos_sociales', blank=True)
    tecnicos = models.ManyToManyField(User, related_name='proyecto_impactos_tecnicos', blank=True)
    alumnos_doctorado = models.ManyToManyField(User, related_name='proyecto_alumnos_doctorado', blank=True)
    alumnos_maestria = models.ManyToManyField(User, related_name='proyecto_alumnos_maestria', blank=True)
    alumnos_licenciatura = models.ManyToManyField(User, related_name='proyecto_alumnos_licenciatura', blank=True)

    def __str__(self):
        if self.nombre == 'Ninguno':
            return 'Ninguno'
        else:
            return "{} : {}".format(self.nombre, self.fecha_inicio)

    def natural_key(self):
        return (self.nombre)

    def get_absolute_url(self):
        return reverse('proyecto_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['nombre']



###################


"""
class TipoDocumento(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    #slug = AutoSlugField(populate_from='tipo', unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return (self.nombre)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Tipo de documento'
        verbose_name_plural = 'Tipos de documentos'
"""

class Indice(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    #slug = AutoSlugField(populate_from='indice', unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return (self.nombre)

    def get_absolute_url(self):
        return reverse('indice_detalle', kwargs={'pk': self.pk})

    def get_absolute_url(self):
        return reverse('/', kwargs={'pk': self.pk})



class Memoria(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)
    #slug = AutoSlugField(populate_from='memoria')

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return (self.nombre)

    def get_absolute_url(self):
        return reverse('memoria_detalle', kwargs={'pk': self.pk})


class Editorial(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    #slug = AutoSlugField(populate_from='editorial', unique=True)
    descripcion = models.TextField(blank=True)
    pais = models.ForeignKey(Pais)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return (self.nombre)

    def get_absolute_url(self):
        return reverse('editorial_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['nombre']
        verbose_name_plural = 'Editoriales'


class Coleccion(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    #slug = AutoSlugField(populate_from='coleccion', unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return (self.nombre)

    def get_absolute_url(self):
        return reverse('coleccion_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Colección'
        verbose_name_plural = 'Colecciones'


class Libro(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    #slug = AutoSlugField(populate_from='nombre_libro', unique=True)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=50, choices=(('INVESTIGACION', 'Investigación'), ('DIVULGACION', 'Divulgación')))
    usuarios = models.ManyToManyField(User, related_name='libro_autores', verbose_name='Autores')
    editores = models.ManyToManyField(User, related_name='libro_editores', blank=True)
    coordinadores = models.ManyToManyField(User, related_name='libro_coordinadores', blank=True)
    ciudad = models.ForeignKey(Ciudad)
    editorial = models.ForeignKey(Editorial)
    status = models.CharField(max_length=20, choices=STATUS_PUBLICACION)
    fecha = models.DateField(auto_now=False)
    numero_edicion = models.PositiveIntegerField(default=1)
    numero_paginas = models.PositiveIntegerField(default=0)
    coleccion = models.ForeignKey(Coleccion, blank=True, null=True)
    volumen = models.CharField(max_length=255, blank=True)
    isbn = models.SlugField(max_length=30)
    url = models.URLField(blank=True)
    #tags = models.ManyToManyField(Tag, related_name='libro_tags', blank=True)

    def __str__(self):
        return "{} : {} : {}".format(self.nombre, self.editorial, self.isbn)

    def natural_key(self):
        return (self.nombre)

    def get_absolute_url(self):
        return reverse('libro_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['nombre']
        get_latest_by = ['fecha', 'nombre_libro', 'editorial']


class Revista(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    #slug = AutoSlugField(populate_from='nombre_revista', unique=True)
    descripcion = models.TextField(blank=True)
    editorial = models.ForeignKey(Editorial)
    #pais = models.ForeignKey(Pais)
    url = models.URLField(blank=True)

    def __str__(self):
        return "{} : {}".format(self.nombre, self.editorial)

    def natural_key(self):
        return (self.nombre)

    def get_absolute_url(self):
        return reverse('revista_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['nombre']
        get_latest_by = ['fecha', 'nombre_revista', 'editorial']


class Asignatura(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return (self.nombre)

    def get_absolute_url(self):
        return reverse('asignatura_detalle', kwargs={'pk': self.pk})


class MedioDivulgacion(models.Model):
    nombre_medio = models.CharField(max_length=255, unique=True)
    #slug = AutoSlugField(populate_from='nombre_medio', unique=True)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=20, choices=(('PERIODICO', 'Periódico'), ('RADIO', 'Radio'), ('TV', 'Televisión'), ('INTERNET', 'Internet'), ('OTRO', 'Otro')))
    canal = models.CharField(max_length=255)
    ciudad = models.ForeignKey(Ciudad)
    #tags = models.ManyToManyField(Tag, related_name='medio_divulgacion_tags', blank=True)

    def __str__(self):
        return self.nombre_medio

    def get_absolute_url(self):
        return reverse('medio_divulgacion_detalle', kwargs={'pk': self.pk})

    def natural_key(self):
        return (self.nombre_medio)

    def get_absolute_url(self):
        return reverse('medio_divulgacion_detalle', kwargs={'pk': self.pk})

    class Meta:
        unique_together = ['canal', 'nombre_medio']
        ordering = ['nombre_medio']
        verbose_name = "Medio de difusión para divulgación"
        verbose_name_plural = "Medios de difusión para divulgación"