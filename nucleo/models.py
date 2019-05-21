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
                                                              ('ACEPTADO', 'Aceptado'), ('ENVIADO', 'Enviado')))
ENTIDAD_CLASIFICACION = getattr(settings, 'ENTIDAD_CLASIFICACION', (('', '-------'),
                                                                    ('ACADEMICA', 'Académica'),
                                                                    ('FEDERAL', 'Gubernamental federal'),
                                                                    ('ESTATAL', 'Gubernamental estatal'),
                                                                    ('MUNICIPAL', 'Gubernamental municipal'),
                                                                    ('PRIVADA', 'Sector privado'),
                                                                    ('NO_LUCRATIVA', 'Sector privado no lucrativo'),
                                                                    ('INTERNACIONAL', 'Internacional')))


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


class Pais(models.Model):
    pais_nombre = models.CharField(max_length=60, unique=True)
    pais_nombre_extendido = models.CharField(max_length=200, unique=True)
    pais_codigo = models.SlugField(max_length=2, unique=True)
    pais_zona = models.ForeignKey(ZonaPais, on_delete=models.PROTECT)

    def __str__(self):
        return self.pais_nombre

    def natural_key(self):
        return self.pais_nombre

    def get_absolute_url(self):
        return reverse('pais_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['pais_nombre']
        verbose_name_plural = 'Paises'
        verbose_name = 'País'



class Estado(models.Model):
    nombre = models.CharField(max_length=200)
    # slug = AutoSlugField(populate_from='estado')
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT)

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
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT)
    validado = models.BooleanField(default=False)
    fecha_creado = models.DateField(auto_now_add=True, null=True, blank=True)


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



class User(AbstractUser):
    grado = models.ForeignKey(GradoAcademico, blank=True, null=True, on_delete=models.PROTECT)
    descripcion = models.TextField(blank=True, verbose_name='Semblanza')
    tipo = models.CharField(max_length=30, blank=True, null=True, choices=(
        ('', 'Seleccionar tipo de usuario'), ('INVESTIGADOR', 'Investigador'), ('ADMINISTRATIVO', 'Administrativo'),
        ('TECNICO', 'Técnico'), ('POSTDOCTORADO', 'Postdoctorado'), ('OTRO', 'Otro')), default='OTRO')
    fecha_nacimiento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=10, blank=True, null=True, choices=(
        ('', 'Seleccionar género'), ('M', 'Masculino'), ('F', 'Femenino')))
    pais_origen = models.ForeignKey(Pais, default=1, blank=True, null=True, verbose_name='País de origen', related_name='user_pais_origen', on_delete=models.PROTECT)
    rfc = models.SlugField(max_length=20, blank=True)
    curp = models.SlugField(max_length=20, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    direccion_continuacion = models.CharField(max_length=255, blank=True)
    pais = models.ForeignKey(Pais, blank=True, null=True, related_name='user_pais', on_delete=models.PROTECT, default=1)
    estado = models.ForeignKey(Estado, blank=True, null=True, on_delete=models.PROTECT, default=1)
    ciudad = models.ForeignKey(Ciudad, blank=True, null=True, on_delete=models.PROTECT, default=1)
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



class InstitucionSimple(models.Model):
    institucion_nombre = models.CharField(max_length=255, verbose_name='Nombre de la institución')
    institucion_pais = models.ForeignKey(Pais, on_delete=models.PROTECT, verbose_name='País donde se encuentra la institución')
    institucion_ciudad = models.CharField(max_length=255, verbose_name='Ciudad donde se encuentra la institución')

    institucion_clasificacion = models.CharField(
        max_length=20, choices=(('', '-------'), ('ACADEMICA', 'Académica'), ('FEDERAL', 'Gubernamental federal'),
                                ('ESTATAL', 'Gubernamental estatal'), ('MUNICIPAL', 'Gubernamental municipal'),
                                ('PRIVADA', 'Sector privado'), ('NO_LUCRATIVA', 'Sector privado no lucrativo')),
        verbose_name='Clasificación de la institución')
    institucion_perteneceunam = models.BooleanField(default=False, verbose_name='Pertenece a la UNAM')
    institucion_subsistemaunam = models.CharField(max_length=50, choices=(
        ('', '-------'),
        ('DIFUSION_CULTURAL', 'Subsistema de Difusión Cultural'),
        ('ESTUDIOS_POSGRADO', 'Subsistema de Estudios de Posgrado'),
        ('HUMANIDADES', 'Subsistema de Humanidades'),
        ('INVESTIGACION_CIENTIFICA', 'Subsistema de Investigación Científica'),
        ('ESCUELAS', 'Facultades y Escuelas'),
        ('DESARROLLO_INSTITUCIONAL', 'Desarrollo Institucional')), blank=True, null=True, verbose_name='Subsistema UNAM (sólo si la institución pertenece a la UNAM)')
    institucion_regverificado = models.BooleanField(default=False, verbose_name='Este registro se encuentra validado y verificado. Cuando un registro está marcado como verificado ya no es posible editar ni eliminar por otros usuarios')
    institucion_regfechacreado = models.DateField(auto_now_add=True)
    institucion_regfechaactualizado = models.DateField(auto_now=True, blank=True, null=True)
    institucion_regusuario = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Usuario que creó el registro de esta entrada', default=1)

    def __str__(self):
        unam = ""
        if self.institucion_perteneceunam:
            unam = " [UNAM]"
        return "{} {} ({})".format(self.institucion_nombre, unam, self.institucion_pais)

    def natural_key(self):
        return "{} ({})".format(self.institucion_nombre, self.institucion_pais)

    def get_absolute_url(self):
        return reverse('institucion_detalle', kwargs={'pk': self.pk})

    class Meta:
        unique_together = ('institucion_nombre', 'institucion_pais', 'institucion_ciudad')
        ordering = ['pk']
        verbose_name = 'Institución'
        verbose_name_plural = 'Instituciones'


class Institucion(models.Model):
    nombre_institucion = models.CharField(max_length=255, unique=True)
    descripcion_institucion = models.TextField(blank=True)
    clasificacion_institucion = models.CharField(max_length=20, choices=ENTIDAD_CLASIFICACION)
    pais_institucion = models.ForeignKey(Pais, on_delete=models.PROTECT)
    validado = models.BooleanField(default=False)
    fecha_creado = models.DateField(auto_now_add=True, blank=True, null=True)
    fecha_actualizado = models.DateField(auto_now=True, blank=True, null=True)
    usuario_creador = models.ForeignKey(User, on_delete=models.PROTECT, default=1)

    def __str__(self):
        return self.nombre_institucion

    def natural_key(self):
        return self.nombre_institucion

    def get_absolute_url(self):
        return reverse('institucion_detalle_mal', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Institución'
        verbose_name_plural = 'Instituciones'
        ordering = ['-id']


class Dependencia(models.Model):
    nombre_dependencia = models.CharField(max_length=255)
    descripcion_dependencia = models.TextField(blank=True)
    institucion_dependencia = models.ForeignKey(Institucion, on_delete=models.PROTECT)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.PROTECT, blank=True, null=True)
    ciudad_text_dependencia = models.CharField(max_length=255)
    subsistema_unam_dependencia = models.CharField(max_length=50, choices=(
        ('', 'Seleccionar Subsistema UNAM'),
        ('DIFUSION_CULTURAL', 'Subsistema de Difusión Cultural'),
        ('ESTUDIOS_POSGRADO', 'Subsistema de Estudios de Posgrado'),
        ('HUMANIDADES', 'Subsistema de Humanidades'),
        ('INVESTIGACION_CIENTIFICA', 'Subsistema de Investigación Científica'),
        ('ESCUELAS', 'Facultades y Escuelas'),
        ('DESARROLLO_INSTITUCIONAL', 'Desarrollo Institucional')), blank=True, null=True, verbose_name='Subsistema UNAM')
    validado = models.BooleanField(default=False)
    fecha_creado = models.DateField(auto_now_add=True, null=True, blank=True)
    fecha_actualizado = models.DateField(auto_now=True, null=True, blank=True)
    usuario_creador = models.ForeignKey(User, on_delete=models.PROTECT, default=1)

    # clasificacion = models.CharField(max_length=20, choices=ENTIDAD_CLASIFICACION, null=True, blank=True)
    # pais = models.ForeignKey(Pais, on_delete=models.PROTECT, null=True, blank=True)


    def __str__(self):
        return "{} :: {}".format(self.nombre_dependencia, self.institucion_dependencia.nombre_institucion)

    def natural_key(self):
        return self.nombre_dependencia

    def get_absolute_url(self):
        return reverse('dependencia_detalle', kwargs={'pk': self.pk})

    class Meta:
        unique_together = ('nombre_dependencia', 'institucion_dependencia')
        ordering = ['pk']











class Departamento(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.PROTECT)

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
    areaconocimiento_nombre = models.CharField(max_length=255, unique=True)
    areaconocimiento_categoria = models.CharField(max_length=20, choices=(
            ('LSBM', 'Life Sciences and Biomedicine'), ('PHYS', 'Physical Sciences'), ('TECH', 'Technology'),
            ('ARTH', 'Arts and Humanities'), ('SS', 'Social Sciences'), ('ZTRA', 'Otra')))
    # descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.areaconocimiento_nombre

    def natural_key(self):
        return self.areaconocimiento_nombre

    def get_absolute_url(self):
        return reverse('area_conocimiento_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['areaconocimiento_categoria', 'areaconocimiento_nombre']
        verbose_name = 'Área de conocimiento'
        verbose_name_plural = 'Áreas de conocimiento'


class AreaEspecialidad(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)
    area_conocimiento = models.ForeignKey(AreaConocimiento, on_delete=models.PROTECT)

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
    institucion = models.ForeignKey(Institucion, on_delete=models.PROTECT)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.PROTECT)

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
    institucion = models.ForeignKey(Institucion, on_delete=models.PROTECT)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.PROTECT)

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
    programalicenciatura_nombre = models.CharField(max_length=255, unique=True)
    programalicenciatura_areaconocimiento = models.ForeignKey(AreaConocimiento, verbose_name='Área de conocimiento', on_delete=models.PROTECT)
    programalicenciatura_regverificado = models.BooleanField(default=False, verbose_name='Este registro se encuentra validado y verificado. Cuando un registro está marcado como verificado ya no es posible editar ni eliminar por otros usuarios')
    programalicenciatura_regfechacreado = models.DateField(auto_now_add=True, blank=True, null=True)
    programalicenciatura_regfechaactualizado = models.DateField(auto_now=True, blank=True, null=True)
    programalicenciatura_regusuario = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Usuario que creó el registro de esta entrada')

    def __str__(self):
        return self.programalicenciatura_nombre

    def natural_key(self):
        return self.programalicenciatura_nombre

    def get_absolute_url(self):
        return reverse('programa_licenciatura_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['programalicenciatura_nombre']
        verbose_name = 'Programa de licenciatura'
        verbose_name_plural = 'Programas de licenciatura'


class ProgramaMaestria(models.Model):
    programamaestria_nombre = models.CharField(max_length=255, unique=True)
    programamaestria_areaconocimiento = models.ForeignKey(AreaConocimiento, verbose_name='Área de conocimiento', on_delete=models.PROTECT)
    programamaestria_regverificado = models.BooleanField(default=False, verbose_name='Este registro se encuentra validado y verificado. Cuando un registro está marcado como verificado ya no es posible editar ni eliminar por otros usuarios')
    programamaestria_regfechacreado = models.DateField(auto_now_add=True, blank=True, null=True)
    programamaestria_regfechaactualizado = models.DateField(auto_now=True, blank=True, null=True)
    programamaestria_regusuario = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Usuario que creó el registro de esta entrada')

    def __str__(self):
        return self.programamaestria_nombre

    def natural_key(self):
        return self.programamaestria_nombre

    def get_absolute_url(self):
        return reverse('programa_maestria_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['programamaestria_nombre']
        verbose_name = 'Programa de maestria'
        verbose_name_plural = 'Programas de maestria'


class ProgramaDoctorado(models.Model):
    programadoctorado_nombre = models.CharField(max_length=255, unique=True)
    programadoctorado_areaconocimiento = models.ForeignKey(AreaConocimiento, verbose_name='Área de conocimiento', on_delete=models.PROTECT)
    programadoctorado_regverificado = models.BooleanField(default=False, verbose_name='Este registro se encuentra validado y verificado. Cuando un registro está marcado como verificado ya no es posible editar ni eliminar por otros usuarios')
    programadoctorado_regfechacreado = models.DateField(auto_now_add=True, blank=True, null=True)
    programadoctorado_regfechaactualizado = models.DateField(auto_now=True, blank=True, null=True)
    programadoctorado_regusuario = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Usuario que creó el registro de esta entrada')

    def __str__(self):
        return self.programadoctorado_nombre

    def natural_key(self):
        return self.programadoctorado_nombre

    def get_absolute_url(self):
        return reverse('programa_doctorado_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['programadoctorado_nombre']
        verbose_name = 'Programa de doctorado'
        verbose_name_plural = 'Programas de doctorado'


class TipoEvento(models.Model):
    tipoevento_nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.tipoevento_nombre

    def natural_key(self):
        return self.tipoevento_nombre

    def get_absolute_url(self):
        return reverse('tipo_evento_detalle', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Tipo de evento'
        verbose_name_plural = 'Tipos de eventos'


class Evento(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    tipo = models.ForeignKey(TipoEvento, on_delete=models.PROTECT)
    tipo_publico = models.CharField(max_length=255)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    entidades = models.ManyToManyField(Dependencia, related_name='evento_entidades')
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT)
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.PROTECT)
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
    institucion = models.ForeignKey(Institucion, on_delete=models.DO_NOTHING)
    ambito = models.CharField(max_length=50, choices=(('', '-------'), ('INSTITUCIONAL', 'Institucional'), ('REGIONAL', 'Regional'), ('NACIONAL', 'Nacional'), ('INTERNACIONAL', 'Internacional')))
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
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT)
    # estado = models.ForeignKey(Estado, on_delete=models.PROTECT)
    # ciudad = models.ForeignKey(Ciudad, on_delete=models.PROTECT)
    ciudad = models.CharField(max_length=255, blank=True)

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
    tipo_participacion = models.CharField(max_length=50, choices=(('', '-------'), ('AUTORIA', 'Autoría'), ('EDICION', 'Edición'), ('COORDINACION', 'Coordinación'), ('COMPILACION', 'Compilación')))
    autores = SortedManyToManyField(User, related_name='libro_autores', blank=True)
    editores = SortedManyToManyField(User, related_name='libro_editores', blank=True)
    coordinadores = SortedManyToManyField(User, related_name='libro_coordinadores', blank=True)
    compiladores = SortedManyToManyField(User, related_name='libro_compiladores', blank=True)
    autores_todos = models.TextField(blank=True, null=True)
    agradecimientos = models.ManyToManyField(User, related_name='libro_agradecimientos', blank=True)
    # editorial = models.ForeignKey(Editorial, on_delete=models.PROTECT, blank=True, null=True)
    editorial_text = models.CharField(max_length=255, blank=True, null=True)
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT)
    ciudad_text = models.CharField(max_length=255, blank=True, null=True)
    # ciudad = models.ForeignKey(Ciudad, on_delete=models.PROTECT, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_PUBLICACION)
    fecha = models.DateField(blank=True, null=True)
    fecha_enviado = models.DateField(null=True, blank=True)
    fecha_aceptado = models.DateField(null=True, blank=True)
    fecha_enprensa = models.DateField(null=True, blank=True)
    fecha_publicado = models.DateField(null=True, blank=True)
    numero_edicion = models.PositiveIntegerField(default=1)
    numero_paginas = models.PositiveIntegerField(default=0)
    coleccion_text = models.CharField(max_length=255, blank=True, null=True)
    volumen = models.CharField(max_length=255, blank=True)
    isbn = models.SlugField(max_length=30, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    arbitrado_pares = models.BooleanField(default=False)

    def __str__(self):
        return "{} : {} : {}".format(self.nombre, self.editorial_text, self.isbn)

    def natural_key(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('libro_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['nombre']
        get_latest_by = ['fecha', 'nombre_libro', 'editorial']


class Revista(models.Model):
    revista_nombre = models.CharField(max_length=255, unique=True)
    revista_nombreabreviadowos = models.CharField(max_length=255, null=True, blank=True)
    revista_pais = models.ForeignKey(Pais, on_delete=models.PROTECT)
    revista_indices = models.ManyToManyField(Indice, related_name='revista_indices')
    revista_issn_impreso = models.CharField(max_length=40, null=True, blank=True, verbose_name='ISSN Impreso')
    revista_issn_online = models.CharField(max_length=40, null=True, blank=True, verbose_name='ISSN Online')
    revista_regverificado = models.BooleanField(default=False, verbose_name='Este registro se encuentra validado y verificado. Cuando un registro está marcado como verificado ya no es posible editar ni eliminar por otros usuarios')
    revista_regfechacreado = models.DateField(auto_now_add=True, blank=True, null=True)
    revista_regfechaactualizado = models.DateField(auto_now=True, blank=True, null=True)
    revista_regusuario = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Usuario que creó el registro de esta entrada')

    def __str__(self):
        return "{} ({})".format(self.revista_nombre, self.revista_pais)

    def natural_key(self):
        return self.revista_nombre

    def get_absolute_url(self):
        return reverse('revista_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['revista_nombre']
        get_latest_by = ['revista_nombre']


class RevistaDivulgacion(models.Model):
    revistadivulgacion_nombre = models.CharField(max_length=255, unique=True)
    revistadivulgacion_pais = models.ForeignKey(Pais, on_delete=models.PROTECT)
    revistadivulgacion_issnimpreso = models.CharField(max_length=40, null=True, blank=True, verbose_name='ISSN Impreso')
    revistadivulgacion_regverificado = models.BooleanField(default=False, verbose_name='Este registro se encuentra validado y verificado. Cuando un registro está marcado como verificado ya no es posible editar ni eliminar por otros usuarios')
    revistadivulgacion_regfechacreado = models.DateField(auto_now_add=True, blank=True, null=True)
    revistadivulgacion_regfechaactualizado = models.DateField(auto_now=True, blank=True, null=True)
    revistadivulgacion_regusuario = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Usuario que creó el registro de esta entrada')

    def __str__(self):
        return "{} ({})".format(self.revistadivulgacion_nombre, self.revistadivulgacion_pais)

    def natural_key(self):
        return self.revistadivulgacion_nombre

    def get_absolute_url(self):
        return reverse('revistadivulgacion_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['revistadivulgacion_nombre']
        get_latest_by = ['revistadivulgacion_nombre']


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
    tipo = models.CharField(max_length=20, choices=(('', '-------'), ('PERIODICO', 'Periódico'), ('RADIO', 'Radio'),
                                                    ('TV', 'Televisión'), ('INTERNET', 'Internet'), ('OTRO', 'Otro')))
    canal = models.CharField(max_length=255)
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT)
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.PROTECT)

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


class ProyectoInsvestigacionArbitrado(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    institucion = models.ForeignKey(Institucion, on_delete=models.PROTECT)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.PROTECT)
    status = models.CharField(max_length=30, choices=STATUS_PROYECTO)

    def __str__(self):
        return "{} : {}".format(self.nombre, self.fecha_inicio)

    def natural_key(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('proyecto_arbitrado_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['nombre', 'fecha_inicio']


class ConvocatoriaArbitraje(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('convocatoria_atrbitraje_detalle', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Convocatoria'
        verbose_name_plural = 'Convocatorias'


