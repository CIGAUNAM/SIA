from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.conf import settings
from sortedm2m.fields import SortedManyToManyField

from django.contrib.auth.models import UnicodeUsernameValidator

from django.utils.translation import gettext_lazy


STATUS_PROYECTO = getattr(settings, 'STATUS_PROYECTO', (('NUEVO', 'Nuevo'), ('EN_PROCESO', 'En proceso'),
                                                        ('CONCLUIDO', 'Concluído'), ('OTRO', 'Otro')))
CLASIFICACION_PROYECTO = getattr(settings,
                                 'CLASIFICACION_PROYECTO', (('BASICO', 'Ciencia Básica'),
                                                            ('APLICADO', 'Investigaciòn Aplicada'),
                                                            ('DESARROLLO_TECNOLOGICO', 'Desarrollo tecnológico'),
                                                            ('INNOVACION', 'Innovación'),
                                                            ('INVESTIGACION_FRONTERA', 'Investigación de frontera'),
                                                            ('OTRO', 'Otro')))
ORGANIZACION_PROYECTO = getattr(settings,
                                'ORGANIZACION_PROYECTO', (('INDIVIDUAL', 'Individual'), ('COLECTIVO', 'Colectivo')))
MODALIDAD_PROYECTO = getattr(settings, 'MODALIDAD_PROYECTO', (('DISCIPLINARIO', 'Disciplinario'),
                                                              ('MULTIDISCIPLINARIO', 'Multidisciplinario'),
                                                              ('INTERDISCIPLINARIO', 'Interisciplinario'),
                                                              ('TRANSDISCIPLINARIO', 'Transdisciplinario'),
                                                              ('OTRA', 'Otra')))
FINANCIAMIENTO_UNAM = getattr(settings,
                              'FINANCIAMIENTO_UNAM', (('ASIGNADO', 'Presupuesto asignado a la entidad'),
                                                      ('CONCURSADO', 'Presupuesto concursado por la entidad'),
                                                      ('AUTOGENERADO', 'Recursos autogenerados (extraordinarios)'),
                                                      ('OTRO', 'Otro')))
FINANCIAMIENTO_EXTERNO = getattr(settings, 'FINANCIAMIENTO_EXTERNO', (('ESTATAL', 'Gubernamental Estatal'),
                                                                      ('FEDERAL', 'Gubernamental Federal'),
                                                                      ('LUCRATIVO', 'Privado lucrativo'),
                                                                      ('NO_LUCRATIVO', 'Privado no lucrativo'),
                                                                      ('EXTRANJERO', 'Recursos del extranjero'),
                                                                      ('OTRO', 'Otro')))
FINANCIAMIENTO_TIPO = getattr(settings, 'FINANCIAMIENTO_TIPO', (('UNAM', FINANCIAMIENTO_UNAM),
                                                                ('Externo', FINANCIAMIENTO_EXTERNO)))
CARGO__TIPO_CARGO = getattr(settings, 'CARGO__TIPO_CARGO',
                            (('ACADEMICO', 'Académico'), ('ADMINISTRATIVO', 'Administrativo')))
NIVEL_ACADEMICO = getattr(settings, 'NIVEL_ACADEMICO',
                          (('LICENCIATURA', 'licenciatura'), ('MAESTRIA', 'Maestría'), ('DOCTORADO', 'Doctorado')))
STATUS_PUBLICACION = getattr(settings, 'STATUS_PUBLICACION', (('PUBLICADO', 'Publicado'), ('EN_PRENSA', 'En prensa'),
                                                              ('ACEPTADO', 'Aceptado'), ('ENVIADO', 'Enviado'),
                                                              ('OTRO', 'Otro')))
ENTIDAD_CLASIFICACION = getattr(settings, 'ENTIDAD_CLASIFICACION', (('', '-------'),
                                                                    ('ACADEMICA', 'Académica'),
                                                                    ('FEDERAL', 'Gubernamental federal'),
                                                                    ('ESTATAL', 'Gubernamental estatal'),
                                                                    ('MUNICIPAL', 'Gubernamental municipal'),
                                                                    ('PRIVADA', 'Sector privado'),
                                                                    ('NO_LUCRATIVA', 'Sector privado no lucrativo')))


# Create your models here.


class ZonaPais(models.Model):
    nombre = models.CharField(max_length=60, unique=True)
    # slug = AutoSlugField(populate_from='zona')

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Zona de paises'
        verbose_name_plural = 'Zonas de paises'


class Pais(models.Model):
    nombre = models.CharField(max_length=60, unique=True)
    nombre_extendido = models.CharField(max_length=200, unique=True)
    codigo = models.SlugField(max_length=2, unique=True)
    zona = models.ForeignKey(ZonaPais, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('pais_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['nombre']
        verbose_name_plural = 'Paises'
        verbose_name = 'País'


class Estado(models.Model):
    nombre = models.CharField(max_length=200)
    # slug = AutoSlugField(populate_from='estado')
    pais = models.ForeignKey(Pais, on_delete=models.DO_NOTHING)

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
    # slug = AutoSlugField(populate_from='ciudad')
    estado = models.ForeignKey(Estado, on_delete=models.DO_NOTHING)

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


class GradoAcademico(models.Model):
    grado_abreviacion = models.CharField(max_length=254, unique=True)
    grado = models.CharField(max_length=254, unique=True)

    def __str__(self):
        return self.grado

    def natural_key(self):
        return self.grado

    def get_absolute_url(self):
        return reverse('grado_academico_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['grado']
        verbose_name = 'Grado académico'
        verbose_name_plural = 'Grados académicos'


class User(AbstractUser):



    grado = models.ForeignKey(GradoAcademico, blank=True, null=True, on_delete=models.DO_NOTHING)
    descripcion = models.TextField(blank=True, verbose_name='Semblanza')
    tipo = models.CharField(max_length=30, blank=True, null=True, choices=(
        ('', 'Seleccionar tipo de usuario'), ('INVESTIGADOR', 'Investigador'), ('ADMINISTRATIVO', 'Administrativo'), 
        ('TECNICO', 'Técnico'), ('POSTDOCTORADO', 'Postdoctorado'), ('OTRO', 'Otro')), default='OTRO')
    fecha_nacimiento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=10, blank=True, null=True, choices=(
        ('', 'Seleccionar género'), ('M', 'Masculino'), ('F', 'Femenino')))
    pais_origen = models.ForeignKey(Pais, default=1, blank=True, null=True, verbose_name='País de origen', related_name='user_pais_origen', on_delete=models.DO_NOTHING)
    rfc = models.SlugField(max_length=20, blank=True)
    curp = models.SlugField(max_length=20, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    direccion_continuacion = models.CharField(max_length=255, blank=True)
    pais = models.ForeignKey(Pais, blank=True, null=True, related_name='user_pais', on_delete=models.DO_NOTHING, default=1)
    estado = models.ForeignKey(Estado, blank=True, null=True, on_delete=models.DO_NOTHING, default=1)
    ciudad = models.ForeignKey(Ciudad, blank=True, null=True, on_delete=models.DO_NOTHING, default=1)
    telefono = models.SlugField(max_length=20, blank=True)
    celular = models.SlugField(max_length=20, blank=True)
    url = models.URLField(blank=True, null=True)
    sni = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    pride = models.CharField(max_length=2, blank=True, null=True, choices=(
        ('-', '-'), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')), default='-')
    ingreso_unam = models.DateField(null=True, blank=True)
    ingreso_entidad = models.DateField(null=True, blank=True)
    egreso_entidad = models.DateField(null=True, blank=True)
    ultimo_contrato = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatares', null=True, blank=True)
    date_joined = models.DateField(auto_now_add=True)
    sic = models.BooleanField(default=False)


    def author_name(self):
        names = self.first_name.split()
        initials = ""
        for i in range(len(names)):
            if i == len(names) - 1:
                initials = initials + names[i][0] + "."
            else:
                initials = initials + names[i][0] + ". "

        surnames = self.last_name.title().replace(" ", "-")
        return "{}, {}".format(surnames, initials)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    def natural_key(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('perfil_usuario', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['first_name', 'last_name']
        pass


class InvestigadorConacyt(models.Model):
    investigador = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class InvestigadorUnam(models.Model):
    investigador = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class InvestigadorInvitado(models.Model):
    investigador = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class Institucion(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)
    clasificacion = models.CharField(max_length=20, choices=ENTIDAD_CLASIFICACION)
    pais = models.ForeignKey(Pais, on_delete=models.DO_NOTHING)
    estado = models.ForeignKey(Estado, on_delete=models.DO_NOTHING)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('institucion_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Institución'
        verbose_name_plural = 'Instituciones'


class Dependencia(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    institucion = models.ForeignKey(Institucion, on_delete=models.DO_NOTHING)
    clasificacion = models.CharField(max_length=20, choices=ENTIDAD_CLASIFICACION)
    pais = models.ForeignKey(Pais, on_delete=models.DO_NOTHING)
    estado = models.ForeignKey(Estado, on_delete=models.DO_NOTHING)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.DO_NOTHING)
    subsistema_unam = models.CharField(max_length=50, choices=(
        ('', 'Seleccionar Subsistema UNAM (sólo si se trata de una dependencia perteneciente a la UNAM)'),
        ('DIFUSION_CULTURAL', 'Subsistema de Difusión Cultural'),
        ('ESTUDIOS_POSGRADO', 'Subsistema de Estudios de Posgrado'),
        ('HUMANIDADES', 'Subsistema de Humanidades'),
        ('INVESTIGACION_CIENTIFICA', 'Subsistema de Investigación Científica'),
        ('ESCUELAS', 'Facultades y Escuelas'),
        ('DESARROLLO_INSTITUCIONAL', 'Desarrollo Institucional'),
        ('NO', 'No')), blank=True, null=True, verbose_name='Subsistema UNAM')

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('dependencia_detalle', kwargs={'pk': self.pk})

    class Meta:
        unique_together = ('nombre', 'institucion')
        ordering = ['nombre']


class Departamento(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.DO_NOTHING)

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
    descripcion = models.TextField(blank=True)
    tipo_cargo = models.CharField(max_length=20, choices=(('', '-------'),
        ('ACADEMICO', 'Académico'), ('ADMINISTRATIVO', 'Administrativo'), ('DIRECTIVO', 'Directivo'), ('OTRO', 'Otro')))

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('cargo_detalle', kwargs={'pk': self.pk})

    class Meta:
        unique_together = ['nombre', 'tipo_cargo']
        ordering = ['nombre']


class Nombramiento(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    clave = models.CharField(max_length=20, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('nombramiento_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['id']


class AreaConocimiento(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    categoria = models.CharField(max_length=20, choices=(
            ('LSBM', 'Life Sciences and Biomedicine'), ('PHYS', 'Physical Sciences'), ('TECH', 'Technology'),
            ('ARTH', 'Arts and Humanities'), ('SS', 'Social Sciences'), ('ZTRA', 'Otra')))
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('area_conocimiento_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['categoria', 'nombre']
        verbose_name = 'Área General de Conocimiento'
        verbose_name_plural = 'Áreas Generales de Conocimiento'


class AreaEspecialidad(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)
    area_conocimiento = models.ForeignKey(AreaConocimiento, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('area_especialidad_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Área de especialidad de WOS y otras entidades'
        verbose_name_plural = 'Áreas de especialidades de WOS y otras entidades'


class ImpactoSocial(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('impacto_social_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Impacto social'
        verbose_name_plural = 'Impactos sociales'


class Financiamiento(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)
    tipo_financiamiento = models.CharField(max_length=80, choices=FINANCIAMIENTO_TIPO)
    institucion = models.ForeignKey(Institucion, on_delete=models.DO_NOTHING)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return self.tipo_financiamiento

    def get_absolute_url(self):
        return reverse('financiamiento_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Financiamiento'
        verbose_name_plural = 'Financiamientos'


class Metodologia(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('metodologia_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['nombre']


class Beca(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField(blank=True)
    institucion = models.ForeignKey(Institucion, on_delete=models.DO_NOTHING)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('beca_detalle', kwargs={'pk': self.pk})


class Reconocimiento(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('reconocimiento_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['nombre']


class ProgramaLicenciatura(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)
    area_conocimiento = models.ForeignKey(AreaConocimiento, verbose_name='Área de conocimiento',
                                          on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('programa_licenciatura_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Programa de licenciatura'
        verbose_name_plural = 'Programas de licenciatura'


class ProgramaMaestria(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)
    area_conocimiento = models.ForeignKey(AreaConocimiento, verbose_name='Área de conocimiento',
                                          on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('programa_maestria_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Programa de maestria'
        verbose_name_plural = 'Programas de maestria'


class ProgramaDoctorado(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)
    area_conocimiento = models.ForeignKey(AreaConocimiento, verbose_name='Área de conocimiento',
                                          on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('programa_doctorado_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Programa de doctorado'
        verbose_name_plural = 'Programas de doctorado'


class TipoEvento(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('tipo_evento_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Tipo de evento'
        verbose_name_plural = 'Tipos de eventos'


class Evento(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    tipo = models.ForeignKey(TipoEvento, on_delete=models.DO_NOTHING)
    tipo_publico = models.CharField(max_length=255)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    entidades = models.ManyToManyField(Dependencia, related_name='evento_entidades')
    pais = models.ForeignKey(Pais, on_delete=models.DO_NOTHING)
    estado = models.ForeignKey(Estado, on_delete=models.DO_NOTHING)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.DO_NOTHING)
    ubicacion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('evento_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['fecha_inicio', 'nombre']
        unique_together = ['fecha_inicio', 'nombre']


class Distincion(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    tipo = models.CharField(max_length=30, choices=(('PREMIO', 'Premio'), ('DISTINCION', 'Distinción'),
                                                    ('RECONOCIMIENTO', 'Reconocimiento'), ('MEDALLA', 'Medalla'),
                                                    ('GUGGENHEIM', 'Beca Guggenheim'),
                                                    ('HONORIS_CAUSA', 'Doctorado Honoris Causa'), ('OTRO', 'Otro')))
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('distincion_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Distinción'
        verbose_name_plural = 'Distinciones'


class ProblemaNacionalConacyt(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('problema_nacional_conacyt_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = ['Problemática Nacional CONACYT']
        verbose_name_plural = ['Problemáticas Nacionales CONACYT']


###################


class Indice(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('indice_detalle', kwargs={'pk': self.pk})


class Editorial(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)
    pais = models.ForeignKey(Pais, on_delete=models.DO_NOTHING)
    estado = models.ForeignKey(Estado, on_delete=models.DO_NOTHING)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('editorial_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['nombre']
        verbose_name_plural = 'Editoriales'


class Coleccion(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('coleccion_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Colección'
        verbose_name_plural = 'Colecciones'


class Libro(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=50, choices=(('INVESTIGACION', 'Investigación'), ('DIVULGACION', 'Divulgación'),
                                                    ('DOCENCIA', 'Docencia')))
    usuarios = SortedManyToManyField(User, related_name='libro_autores', blank=True, verbose_name='Autores')
    editores = SortedManyToManyField(User, related_name='libro_editores', blank=True)
    coordinadores = SortedManyToManyField(User, related_name='libro_coordinadores', blank=True)
    prologo = SortedManyToManyField(User, related_name='libro_prologo', blank=True)
    pais = models.ForeignKey(Pais, on_delete=models.DO_NOTHING)
    estado = models.ForeignKey(Estado, on_delete=models.DO_NOTHING)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.DO_NOTHING)
    editorial = models.ForeignKey(Editorial, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=20, choices=STATUS_PUBLICACION)
    fecha = models.DateField(blank=True, null=True)
    numero_edicion = models.PositiveIntegerField(default=1)
    numero_paginas = models.PositiveIntegerField(default=0)
    coleccion = models.ForeignKey(Coleccion, blank=True, null=True, on_delete=models.DO_NOTHING)
    volumen = models.CharField(max_length=255, blank=True)
    isbn = models.SlugField(max_length=30, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    arbitrado_pares = models.BooleanField(default=False)

    def __str__(self):
        return "{} : {} : {}".format(self.nombre, self.editorial, self.isbn)

    def natural_key(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('libro_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['nombre']
        get_latest_by = ['fecha', 'nombre_libro', 'editorial']


class Revista(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    nombre_abreviado_wos = models.CharField(max_length=255, null=True, blank=True)
    descripcion = models.TextField(blank=True)
    pais = models.ForeignKey(Pais, on_delete=models.DO_NOTHING)
    indices = models.ManyToManyField(Indice, related_name='articulo_cientifico_indices', blank=True)
    # factor_impacto = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    url = models.URLField(blank=True)

    def __str__(self):
        return "{} : {}".format(self.nombre, self.pais)

    def natural_key(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('revista_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['nombre']
        get_latest_by = ['nombre_revista']


class Asignatura(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('asignatura_detalle', kwargs={'pk': self.pk})


class MedioDivulgacion(models.Model):
    nombre_medio = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=20, choices=(('PERIODICO', 'Periódico'), ('RADIO', 'Radio'),
                                                    ('TV', 'Televisión'), ('INTERNET', 'Internet'), ('OTRO', 'Otro')))
    canal = models.CharField(max_length=255)
    pais = models.ForeignKey(Pais, on_delete=models.DO_NOTHING)
    estado = models.ForeignKey(Estado, on_delete=models.DO_NOTHING)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nombre_medio

    def natural_key(self):
        return self.nombre_medio

    def get_absolute_url(self):
        return reverse('medio_divulgacion_detalle', kwargs={'pk': self.pk})

    class Meta:
        unique_together = ['canal', 'nombre_medio']
        ordering = ['nombre_medio']
        verbose_name = "Medio de difusión para divulgación"
        verbose_name_plural = "Medios de difusión para divulgación"


class TipoCurso(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('tipo_curso_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['nombre']
        verbose_name = "Tipo de curso"
        verbose_name_plural = "Tipos de curso"

