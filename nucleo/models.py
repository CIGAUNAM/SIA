import re
import uuid
from pathlib import Path

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, RegexValidator
from django.db import models
from django.db.models import Q
from django.db.models.functions import Coalesce


# ---------------------------------------------------------------------------
# Opciones compartidas
# ---------------------------------------------------------------------------

class NivelAcademico(models.TextChoices):
    LICENCIATURA = 'LICENCIATURA', 'Licenciatura'
    MAESTRIA = 'MAESTRIA', 'Maestría'
    DOCTORADO = 'DOCTORADO', 'Doctorado'


class StatusPublicacion(models.TextChoices):
    ENVIADO = 'ENVIADO', 'Enviado'
    ACEPTADO = 'ACEPTADO', 'Aceptado'
    EN_PRENSA = 'EN_PRENSA', 'En prensa'
    PUBLICADO = 'PUBLICADO', 'Publicado'


class Ambito(models.TextChoices):
    LOCAL = 'LOCAL', 'Local'
    INSTITUCIONAL = 'INSTITUCIONAL', 'Institucional'
    REGIONAL = 'REGIONAL', 'Regional'
    NACIONAL = 'NACIONAL', 'Nacional'
    INTERNACIONAL = 'INTERNACIONAL', 'Internacional'


def ambito_por_pais(pais):
    """Ámbito de un evento o participación según el país donde ocurre y el país sede de la entidad."""
    if pais is None:
        return ''
    return Ambito.NACIONAL if pais.pk == ConfiguracionEntidad.actual().pais_sede_id else Ambito.INTERNACIONAL


class Modalidad(models.TextChoices):
    PRESENCIAL = 'PRESENCIAL', 'Presencial'
    EN_LINEA = 'EN_LINEA', 'En línea'
    MIXTO = 'MIXTO', 'Mixto'
    OTRO = 'OTRO', 'Otro'


class SubsistemaUNAM(models.TextChoices):
    DIFUSION_CULTURAL = 'DIFUSION_CULTURAL', 'Subsistema de Difusión Cultural'
    ESTUDIOS_POSGRADO = 'ESTUDIOS_POSGRADO', 'Subsistema de Estudios de Posgrado'
    HUMANIDADES = 'HUMANIDADES', 'Subsistema de Humanidades'
    INVESTIGACION_CIENTIFICA = 'INVESTIGACION_CIENTIFICA', 'Subsistema de Investigación Científica'
    ESCUELAS = 'ESCUELAS', 'Facultades y Escuelas'
    DESARROLLO_INSTITUCIONAL = 'DESARROLLO_INSTITUCIONAL', 'Desarrollo Institucional'


# ---------------------------------------------------------------------------
# Validadores y normalizadores
# ---------------------------------------------------------------------------

validar_orcid = RegexValidator(r'^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$', 'El ORCID debe tener el formato 0000-0000-0000-000X.')
validar_issn = RegexValidator(r'^\d{4}-\d{3}[\dX]$', 'El ISSN debe tener el formato 1234-567X.')


def normalizar_issn(valor):
    limpio = re.sub(r'[^0-9Xx]', '', valor or '').upper()
    return f'{limpio[:4]}-{limpio[4:]}' if len(limpio) == 8 else (valor or '').strip()


def normalizar_doi(valor):
    """Quita prefijos (https://doi.org/, doi:) y deja el DOI en minúsculas."""
    valor = (valor or '').strip()
    valor = re.sub(r'^(https?://)?(dx\.)?doi\.org/', '', valor, flags=re.IGNORECASE)
    valor = re.sub(r'^doi:\s*', '', valor, flags=re.IGNORECASE)
    return valor.lower()


def validar_periodo(inicio, fin, campo_fin='fecha_fin'):
    if inicio and fin and fin < inicio:
        raise ValidationError({campo_fin: 'La fecha de término no puede ser anterior a la de inicio.'})


def validar_paginas(obj):
    if obj.pagina_inicio and obj.pagina_fin and obj.pagina_fin < obj.pagina_inicio:
        raise ValidationError({'pagina_fin': 'La página final no puede ser menor que la inicial.'})


def validar_programa(obj):
    """El programa académico debe corresponder al nivel del registro."""
    if obj.programa_id and obj.nivel and obj.programa.nivel != obj.nivel:
        raise ValidationError({'programa': f'El programa es de {obj.programa.get_nivel_display().lower()}, '
                                           f'pero el registro es de {obj.get_nivel_display().lower()}.'})


def requerido_si(condicion, obj, campo, mensaje='Este campo es obligatorio en este caso.'):
    if condicion and not getattr(obj, campo):
        raise ValidationError({campo: mensaje})


# ---------------------------------------------------------------------------
# Bases abstractas
# ---------------------------------------------------------------------------

class Verificable(models.Model):
    """Catálogo que cualquier académico puede ampliar y que los administradores validan.

    Un registro verificado solo puede modificarlo un administrador; uno no verificado,
    además, quien lo creó.
    """
    verificado = models.BooleanField(
        default=False, help_text='Los registros verificados solo pueden modificarlos los administradores.')
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, editable=False,
        related_name='+')
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Periodo(models.Model):
    fecha_inicio = models.DateField('fecha de inicio')
    fecha_fin = models.DateField('fecha de término', null=True, blank=True,
                                 help_text='Déjala vacía si sigue vigente.')

    class Meta:
        abstract = True

    def clean(self):
        super().clean()
        validar_periodo(self.fecha_inicio, self.fecha_fin)


class PublicacionQuerySet(models.QuerySet):
    def con_fecha(self):
        """Anota `fecha_orden`: la fecha más avanzada registrada en el proceso editorial."""
        return self.annotate(fecha_orden=Coalesce('fecha_publicado', 'fecha_enprensa', 'fecha_aceptado', 'fecha_enviado'))


class EstadoPublicacion(models.Model):
    """Estado editorial de una publicación y las fechas de cada etapa."""
    status = models.CharField('estado', max_length=20, choices=StatusPublicacion.choices)
    fecha_enviado = models.DateField(null=True, blank=True)
    fecha_aceptado = models.DateField(null=True, blank=True)
    fecha_enprensa = models.DateField('fecha en prensa', null=True, blank=True)
    fecha_publicado = models.DateField(null=True, blank=True)

    objects = PublicacionQuerySet.as_manager()

    FECHA_POR_STATUS = {
        StatusPublicacion.ENVIADO: 'fecha_enviado',
        StatusPublicacion.ACEPTADO: 'fecha_aceptado',
        StatusPublicacion.EN_PRENSA: 'fecha_enprensa',
        StatusPublicacion.PUBLICADO: 'fecha_publicado',
    }

    class Meta:
        abstract = True

    @property
    def fecha(self):
        return self.fecha_publicado or self.fecha_enprensa or self.fecha_aceptado or self.fecha_enviado

    def clean(self):
        super().clean()
        campo = self.FECHA_POR_STATUS.get(self.status)
        if campo and not getattr(self, campo):
            raise ValidationError({campo: 'Indica la fecha correspondiente al estado "%s".' % self.get_status_display()})


class Participante(models.Model):
    """Base de las tablas intermedias que guardan personas en un orden (autores, tutores...)."""
    persona = models.ForeignKey('nucleo.Persona', on_delete=models.PROTECT)
    orden = models.PositiveSmallIntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ['orden', 'pk']

    def __str__(self):
        return str(self.persona)


# ---------------------------------------------------------------------------
# Personas y usuarios
# ---------------------------------------------------------------------------

class Pais(models.Model):
    class Zona(models.TextChoices):
        AMERICA_NORTE = 'AMERICA_NORTE', 'América del Norte'
        AMERICA_CENTRAL = 'AMERICA_CENTRAL', 'América Central'
        AMERICA_SUR = 'AMERICA_SUR', 'América del Sur'
        ANTILLAS = 'ANTILLAS', 'Antillas'
        EUROPA = 'EUROPA', 'Europa'
        ASIA = 'ASIA', 'Asia'
        EURASIA = 'EURASIA', 'Europa-Asia'
        AFRICA = 'AFRICA', 'África'
        OCEANIA = 'OCEANIA', 'Oceanía'

    nombre = models.CharField(max_length=60, unique=True)
    nombre_extendido = models.CharField(max_length=200, blank=True)
    codigo = models.CharField('código ISO', max_length=2, unique=True)
    zona = models.CharField(max_length=20, choices=Zona.choices, blank=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'país'
        verbose_name_plural = 'países'

    def __str__(self):
        return self.nombre


class User(AbstractUser):
    """Cuenta de acceso al sistema con el perfil del académico.

    Las personas sin cuenta (coautores, estudiantes, invitados) viven en `Persona`.
    """

    class Tipo(models.TextChoices):
        INVESTIGADOR = 'INVESTIGADOR', 'Investigador'
        TECNICO = 'TECNICO', 'Técnico académico'
        POSTDOCTORADO = 'POSTDOCTORADO', 'Postdoctorado'
        ADMINISTRATIVO = 'ADMINISTRATIVO', 'Administrativo'
        OTRO = 'OTRO', 'Otro'

    class Genero(models.TextChoices):
        FEMENINO = 'F', 'Femenino'
        MASCULINO = 'M', 'Masculino'
        OTRO = 'O', 'Otro'

    class SNI(models.TextChoices):
        CANDIDATO = 'C', 'Candidato'
        NIVEL_1 = '1', 'Nivel I'
        NIVEL_2 = '2', 'Nivel II'
        NIVEL_3 = '3', 'Nivel III'
        EMERITO = 'E', 'Emérito'

    class Pride(models.TextChoices):
        A = 'A', 'A'
        B = 'B', 'B'
        C = 'C', 'C'
        D = 'D', 'D'

    tipo = models.CharField(max_length=20, choices=Tipo.choices, default=Tipo.OTRO)
    grado = models.CharField('grado (abreviatura)', max_length=20, blank=True, help_text='Por ejemplo: Dr., Mtra., Lic.')
    semblanza = models.TextField(blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    genero = models.CharField('género', max_length=1, choices=Genero.choices, blank=True)
    pais_origen = models.ForeignKey(Pais, on_delete=models.PROTECT, null=True, blank=True, verbose_name='país de origen')
    rfc = models.CharField('RFC', max_length=13, blank=True)
    curp = models.CharField('CURP', max_length=18, blank=True)
    direccion = models.TextField('dirección', blank=True)
    telefono = models.CharField('teléfono', max_length=20, blank=True)
    celular = models.CharField(max_length=20, blank=True)
    url = models.URLField('página web', blank=True)
    sni = models.CharField('nivel SNII', max_length=1, choices=SNI.choices, blank=True)
    pride = models.CharField('nivel PRIDE', max_length=1, choices=Pride.choices, blank=True)
    ingreso_unam = models.DateField('ingreso a la UNAM', null=True, blank=True)
    ingreso_entidad = models.DateField('ingreso a la entidad', null=True, blank=True)
    egreso_entidad = models.DateField('egreso de la entidad', null=True, blank=True)
    ultimo_contrato = models.DateField('último contrato', null=True, blank=True)
    avatar = models.ImageField(upload_to='avatares', null=True, blank=True)

    class Meta:
        ordering = ['first_name', 'last_name']
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'
        permissions = [('ver_todo', 'Puede ver y editar los registros de todos los académicos')]

    def __str__(self):
        return self.get_full_name() or self.username

    @property
    def es_administrador(self):
        return self.is_superuser or self.has_perm('nucleo.ver_todo')

    def activo_en(self, anio):
        """Indica si el académico estaba adscrito a la entidad durante el año dado."""
        return (self.ingreso_entidad is not None and self.ingreso_entidad.year <= anio
                and (self.egreso_entidad is None or self.egreso_entidad.year >= anio))


class Persona(Verificable):
    """Cualquier persona que aparece en la producción académica, tenga o no cuenta."""
    nombre = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    orcid = models.CharField('ORCID', max_length=19, blank=True, validators=[validar_orcid],
                             help_text='Formato 0000-0002-1825-0097.')
    usuario = models.OneToOneField(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='persona',
        help_text='Cuenta del sistema asociada, si la persona es académica de la entidad.')

    class Meta:
        ordering = ['apellidos', 'nombre']

    def __str__(self):
        return f'{self.nombre} {self.apellidos}'.strip()

    @property
    def nombre_cita(self):
        """Nombre en formato bibliográfico: `Apellido-Apellido, N. M.`"""
        iniciales = ' '.join(f'{n[0]}.' for n in self.nombre.split())
        apellidos = '-'.join(self.apellidos.split())
        return f'{apellidos}, {iniciales}' if iniciales else apellidos


# ---------------------------------------------------------------------------
# Catálogos
# ---------------------------------------------------------------------------

class Institucion(Verificable):
    class Clasificacion(models.TextChoices):
        ACADEMICA = 'ACADEMICA', 'Académica'
        FEDERAL = 'FEDERAL', 'Gubernamental federal'
        ESTATAL = 'ESTATAL', 'Gubernamental estatal'
        MUNICIPAL = 'MUNICIPAL', 'Gubernamental municipal'
        PRIVADA = 'PRIVADA', 'Sector privado'
        NO_LUCRATIVA = 'NO_LUCRATIVA', 'Sector privado no lucrativo'

    nombre = models.CharField(max_length=255)
    padre = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='dependencias',
                              verbose_name='pertenece a',
                              help_text='Institución de la que depende (p. ej. una facultad pertenece a su universidad).')
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT, verbose_name='país')
    ciudad = models.CharField(max_length=255, blank=True)
    clasificacion = models.CharField('clasificación', max_length=20, choices=Clasificacion.choices, blank=True)
    pertenece_unam = models.BooleanField('pertenece a la UNAM', default=False)
    subsistema_unam = models.CharField('subsistema UNAM', max_length=30, choices=SubsistemaUNAM.choices, blank=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'institución'
        verbose_name_plural = 'instituciones'
        constraints = [
            models.UniqueConstraint(fields=['nombre', 'pais', 'ciudad'], condition=Q(padre__isnull=True),
                                    name='institucion_unica'),
            models.UniqueConstraint(fields=['nombre', 'padre', 'pais', 'ciudad'], condition=Q(padre__isnull=False),
                                    name='dependencia_unica'),
        ]

    def __str__(self):
        nombre = f'{self.nombre}, {self.padre.nombre}' if self.padre_id else self.nombre
        unam = ' [UNAM]' if self.pertenece_unam else ''
        return f'{nombre}{unam} ({self.pais})'

    def clean(self):
        super().clean()
        ancestro = self.padre
        while ancestro is not None:
            if ancestro.pk == self.pk:
                raise ValidationError({'padre': 'Una institución no puede depender de sí misma.'})
            ancestro = ancestro.padre


class AreaConocimiento(models.Model):
    class Categoria(models.TextChoices):
        LSBM = 'LSBM', 'Life Sciences and Biomedicine'
        PHYS = 'PHYS', 'Physical Sciences'
        TECH = 'TECH', 'Technology'
        ARTH = 'ARTH', 'Arts and Humanities'
        SS = 'SS', 'Social Sciences'
        OTRA = 'OTRA', 'Otra'

    nombre = models.CharField(max_length=255, unique=True)
    categoria = models.CharField('categoría', max_length=4, choices=Categoria.choices)

    class Meta:
        ordering = ['categoria', 'nombre']
        verbose_name = 'área de conocimiento'
        verbose_name_plural = 'áreas de conocimiento'

    def __str__(self):
        return self.nombre


class ProgramaAcademico(Verificable):
    nombre = models.CharField(max_length=255)
    nivel = models.CharField(max_length=20, choices=NivelAcademico.choices)
    area_conocimiento = models.ForeignKey(AreaConocimiento, on_delete=models.PROTECT, null=True, blank=True,
                                          verbose_name='área de conocimiento')

    class Meta:
        ordering = ['nivel', 'nombre']
        verbose_name = 'programa académico'
        verbose_name_plural = 'programas académicos'
        constraints = [models.UniqueConstraint(fields=['nombre', 'nivel'], name='programa_unico')]

    def __str__(self):
        return f'{self.nombre} ({self.get_nivel_display()})'


class Asignatura(Verificable):
    nombre = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Beca(Verificable):
    nombre = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Cargo(Verificable):
    class Tipo(models.TextChoices):
        ACADEMICO = 'ACADEMICO', 'Académico'
        ADMINISTRATIVO = 'ADMINISTRATIVO', 'Administrativo'
        DIRECTIVO = 'DIRECTIVO', 'Directivo'
        OTRO = 'OTRO', 'Otro'

    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=20, choices=Tipo.choices, default=Tipo.OTRO)

    class Meta:
        ordering = ['nombre']
        constraints = [models.UniqueConstraint(fields=['nombre', 'tipo'], name='cargo_unico')]

    def __str__(self):
        return self.nombre


class Nombramiento(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    clave = models.CharField(max_length=20, unique=True)
    descripcion = models.TextField('descripción', blank=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Distincion(Verificable):
    class Tipo(models.TextChoices):
        PREMIO = 'PREMIO', 'Premio'
        DISTINCION = 'DISTINCION', 'Distinción'
        RECONOCIMIENTO = 'RECONOCIMIENTO', 'Reconocimiento'
        MEDALLA = 'MEDALLA', 'Medalla'
        DIPLOMA = 'DIPLOMA', 'Diploma'
        GUGGENHEIM = 'GUGGENHEIM', 'Beca Guggenheim'
        HONORIS_CAUSA = 'HONORIS_CAUSA', 'Doctorado Honoris Causa'
        OTRO = 'OTRO', 'Otro'

    nombre = models.CharField(max_length=255, unique=True)
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    institucion = models.ForeignKey(Institucion, on_delete=models.PROTECT, null=True, blank=True,
                                    verbose_name='institución que la otorga')
    ambito = models.CharField('ámbito', max_length=20, choices=Ambito.choices, blank=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'distinción'
        verbose_name_plural = 'distinciones'

    def __str__(self):
        return self.nombre


class TipoEvento(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'tipo de evento'
        verbose_name_plural = 'tipos de evento'

    def __str__(self):
        return self.nombre


class Evento(Verificable):
    nombre = models.CharField(max_length=255)
    tipo = models.ForeignKey(TipoEvento, on_delete=models.PROTECT)
    descripcion = models.TextField('descripción', blank=True)
    fecha_inicio = models.DateField('fecha de inicio')
    fecha_fin = models.DateField('fecha de término')
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT, verbose_name='país')
    ciudad = models.CharField(max_length=255, blank=True)
    ambito = models.CharField('ámbito', max_length=20, choices=Ambito.choices, blank=True, editable=False,
                              help_text='Se calcula a partir del país.')
    numero_ponentes = models.PositiveIntegerField('número de ponentes', null=True, blank=True)
    numero_asistentes = models.PositiveIntegerField('número de asistentes', null=True, blank=True)

    class Meta:
        ordering = ['-fecha_inicio', 'nombre']
        constraints = [models.UniqueConstraint(fields=['nombre', 'fecha_inicio'], name='evento_unico')]

    def __str__(self):
        return f'{self.nombre} ({self.fecha_inicio:%Y})'

    def clean(self):
        super().clean()
        validar_periodo(self.fecha_inicio, self.fecha_fin)

    def save(self, *args, **kwargs):
        self.ambito = ambito_por_pais(self.pais) if self.pais_id else ''
        super().save(*args, **kwargs)


class Indice(models.Model):
    nombre = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'índice'
        verbose_name_plural = 'índices'

    def __str__(self):
        return self.nombre


class Revista(Verificable):
    class Tipo(models.TextChoices):
        CIENTIFICA = 'CIENTIFICA', 'Científica'
        DIVULGACION = 'DIVULGACION', 'Divulgación'

    nombre = models.CharField(max_length=255, unique=True)
    nombre_abreviado = models.CharField('nombre abreviado (WoS)', max_length=255, blank=True)
    tipo = models.CharField(max_length=20, choices=Tipo.choices, default=Tipo.CIENTIFICA)
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT, verbose_name='país')
    indices = models.ManyToManyField(Indice, blank=True, verbose_name='índices')
    issn_impreso = models.CharField('ISSN impreso', max_length=9, blank=True, validators=[validar_issn])
    issn_electronico = models.CharField('ISSN electrónico', max_length=9, blank=True, validators=[validar_issn])

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return f'{self.nombre} ({self.pais})'

    def save(self, *args, **kwargs):
        self.issn_impreso = normalizar_issn(self.issn_impreso)
        self.issn_electronico = normalizar_issn(self.issn_electronico)
        super().save(*args, **kwargs)

    def factor_impacto(self, anio):
        """Factor de impacto del año indicado (o del más reciente anterior), si está registrado."""
        metrica = self.metricas.filter(anio__lte=anio).order_by('-anio').first()
        return metrica.factor_impacto if metrica else None


class MetricaRevista(models.Model):
    class Fuente(models.TextChoices):
        JCR = 'JCR', 'Journal Citation Reports (JIF)'
        SJR = 'SJR', 'Scimago Journal Rank'
        OTRA = 'OTRA', 'Otra'

    class Cuartil(models.TextChoices):
        Q1 = 'Q1', 'Q1'
        Q2 = 'Q2', 'Q2'
        Q3 = 'Q3', 'Q3'
        Q4 = 'Q4', 'Q4'

    revista = models.ForeignKey(Revista, on_delete=models.CASCADE, related_name='metricas')
    anio = models.PositiveSmallIntegerField('año')
    fuente = models.CharField(max_length=10, choices=Fuente.choices, default=Fuente.JCR)
    factor_impacto = models.DecimalField('factor de impacto', max_digits=7, decimal_places=3)
    cuartil = models.CharField(max_length=2, choices=Cuartil.choices, blank=True)

    class Meta:
        ordering = ['-anio']
        verbose_name = 'métrica de la revista'
        verbose_name_plural = 'métricas de la revista'
        constraints = [models.UniqueConstraint(fields=['revista', 'anio', 'fuente'], name='metrica_unica')]

    def __str__(self):
        return f'{self.revista.nombre} {self.anio}: {self.factor_impacto}'


class MedioDivulgacion(Verificable):
    class Tipo(models.TextChoices):
        PERIODICO = 'PERIODICO', 'Periódico'
        RADIO = 'RADIO', 'Radio'
        TV = 'TV', 'Televisión'
        INTERNET = 'INTERNET', 'Internet'
        OTRO = 'OTRO', 'Otro'

    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    canal = models.CharField(max_length=255, blank=True)
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT, verbose_name='país')
    ciudad = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'medio de divulgación'
        verbose_name_plural = 'medios de divulgación'
        constraints = [models.UniqueConstraint(fields=['nombre', 'canal'], name='medio_unico')]

    def __str__(self):
        return f'{self.nombre} ({self.canal})' if self.canal else self.nombre


class Libro(Verificable, EstadoPublicacion):
    class Tipo(models.TextChoices):
        INVESTIGACION = 'INVESTIGACION', 'Investigación'
        DIVULGACION = 'DIVULGACION', 'Divulgación'
        DOCENCIA = 'DOCENCIA', 'Docencia'

    titulo = models.CharField('título', max_length=255, unique=True)
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    participantes = models.ManyToManyField('Persona', through='LibroParticipante', related_name='libros')
    agradecimientos = models.ManyToManyField('Persona', blank=True, related_name='libros_agradecimientos')
    editorial = models.CharField(max_length=255, blank=True)
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT, verbose_name='país')
    ciudad = models.CharField(max_length=255, blank=True)
    coleccion = models.CharField('colección', max_length=255, blank=True)
    volumen = models.CharField(max_length=255, blank=True)
    numero_edicion = models.PositiveIntegerField('número de edición', default=1)
    numero_paginas = models.PositiveIntegerField('número de páginas', null=True, blank=True)
    isbn = models.CharField('ISBN', max_length=30, blank=True)
    url = models.URLField('URL', blank=True)
    arbitrado_pares = models.BooleanField('arbitrado por pares', default=False,
                                          help_text='El libro pasó por dictamen de pares académicos antes de publicarse.')

    class Meta:
        ordering = ['titulo']

    def __str__(self):
        return self.titulo


class LibroParticipante(Participante):
    class Rol(models.TextChoices):
        AUTOR = 'AUTOR', 'Autor'
        EDITOR = 'EDITOR', 'Editor'
        COORDINADOR = 'COORDINADOR', 'Coordinador'
        COMPILADOR = 'COMPILADOR', 'Compilador'

    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=Rol.choices, default=Rol.AUTOR)

    class Meta(Participante.Meta):
        verbose_name = 'participante'
        verbose_name_plural = 'participantes'
        constraints = [models.UniqueConstraint(fields=['libro', 'persona', 'rol'], name='libro_participante_unico')]


class CapituloLibro(models.Model):
    """Base de los capítulos en libros (investigación y divulgación)."""
    titulo = models.CharField('título', max_length=255)
    libro = models.ForeignKey(Libro, on_delete=models.PROTECT)
    pagina_inicio = models.PositiveIntegerField('página inicial', null=True, blank=True)
    pagina_fin = models.PositiveIntegerField('página final', null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ['titulo']

    def __str__(self):
        return f'{self.titulo} — {self.libro}'

    def clean(self):
        super().clean()
        validar_paginas(self)


# ---------------------------------------------------------------------------
# Configuración de la entidad
# ---------------------------------------------------------------------------

class ConfiguracionEntidad(models.Model):
    """Datos y parámetros propios de la entidad académica.

    Hoy hay un solo registro. Cuando el sistema sea multi-entidad (multitenant), cada entidad
    tendrá el suyo: el resto del código solo debe leerla con `ConfiguracionEntidad.actual(request)`.
    """
    CLAVE_CACHE = 'nucleo:configuracion_entidad'

    # Identidad
    nombre = models.CharField('nombre de la entidad', max_length=255)
    siglas = models.CharField(max_length=30, blank=True)
    institucion_madre = models.CharField('institución a la que pertenece', max_length=255, blank=True,
                                         default='Universidad Nacional Autónoma de México')
    institucion_madre_siglas = models.CharField('siglas de la institución', max_length=30, blank=True, default='UNAM')
    logo = models.ImageField(upload_to='configuracion', null=True, blank=True,
                             help_text='Aparece en el CV y en los formatos impresos.')
    # Dirección y contacto
    titular = models.CharField('nombre de quien dirige', max_length=255, blank=True,
                               help_text='Firma el visto bueno de los formatos.')
    cargo_titular = models.CharField('cargo de quien dirige', max_length=100, default='Director(a)')
    ciudad = models.CharField(max_length=255, blank=True)
    direccion = models.TextField('dirección', blank=True)
    telefono = models.CharField('teléfono', max_length=100, blank=True)
    correo = models.EmailField('correo de contacto', blank=True)
    sitio_web = models.URLField('sitio web', blank=True)
    # Documentos
    consejo_tecnico = models.CharField(
        'consejo técnico', max_length=255, blank=True, default='Consejo Técnico de la Investigación Científica',
        help_text='Órgano ante el que se tramitan las licencias con goce de sueldo.')
    # Operación
    pais_sede = models.ForeignKey(Pais, on_delete=models.PROTECT, null=True, blank=True, verbose_name='país sede',
                                  help_text='Define si un evento o participación es nacional o internacional.')
    remitente = models.EmailField('remitente de los correos', blank=True,
                                  help_text='Si se deja vacío se usa el configurado en el servidor.')
    anios_tablero = models.PositiveSmallIntegerField('años en el tablero', default=6)
    meses_publicacion_pendiente = models.PositiveSmallIntegerField(
        'meses para marcar una publicación como pendiente', default=6,
        help_text='Una publicación no publicada que no cambia de estado en este tiempo aparece en los pendientes.')

    class Meta:
        verbose_name = 'configuración de la entidad'
        verbose_name_plural = 'configuración de la entidad'

    def __str__(self):
        return self.siglas or self.nombre

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(self.CLAVE_CACHE)

    @classmethod
    def actual(cls, request=None):
        """Configuración vigente. Punto único de acceso: con multitenant se resolverá a partir de `request`."""
        configuracion = cache.get(cls.CLAVE_CACHE)
        if configuracion is None:
            configuracion = cls.objects.select_related('pais_sede').first() or cls(nombre='Entidad académica')
            cache.set(cls.CLAVE_CACHE, configuracion, 60)
        return configuracion

    @property
    def nombre_completo(self):
        """"Centro de ..., UNAM"."""
        return f'{self.nombre}, {self.institucion_madre_siglas}' if self.institucion_madre_siglas else self.nombre

    @property
    def remitente_correos(self):
        return self.remitente or settings.DEFAULT_FROM_EMAIL


# ---------------------------------------------------------------------------
# Evidencias
# ---------------------------------------------------------------------------

def almacenamiento_evidencias():
    from .almacenamiento import AlmacenamientoProtegido
    return AlmacenamientoProtegido()


def ruta_evidencia(instancia, nombre_archivo):
    return f'evidencias/{uuid.uuid4().hex}/{Path(nombre_archivo).name}'


EXTENSIONES_EVIDENCIA = ['pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx', 'xls', 'xlsx', 'odt', 'ods']
TAMANO_MAXIMO_EVIDENCIA = 15 * 1024 * 1024


def validar_tamano_evidencia(archivo):
    if archivo.size > TAMANO_MAXIMO_EVIDENCIA:
        raise ValidationError('El archivo no puede pesar más de 15 MB.')


class Evidencia(models.Model):
    """Documento probatorio (constancia, carta, PDF de la publicación) adjunto a cualquier registro."""
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField()
    objeto = GenericForeignKey('content_type', 'object_id')
    archivo = models.FileField(
        upload_to=ruta_evidencia, storage=almacenamiento_evidencias, max_length=255,
        validators=[FileExtensionValidator(EXTENSIONES_EVIDENCIA), validar_tamano_evidencia],
        help_text='PDF, imagen u hoja de cálculo; máximo 15 MB.')
    descripcion = models.CharField('descripción', max_length=255, blank=True)
    subido_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, editable=False,
                                   related_name='+')
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['creado']
        verbose_name = 'evidencia'
        verbose_name_plural = 'evidencias'
        indexes = [models.Index(fields=['content_type', 'object_id'])]

    def __str__(self):
        return self.descripcion or Path(self.archivo.name).name


# ---------------------------------------------------------------------------
# Informe anual
# ---------------------------------------------------------------------------

class PeriodoInforme(models.Model):
    """Año de informe. Al cerrarse, los académicos ya no pueden modificar los registros de ese año."""
    anio = models.PositiveSmallIntegerField('año', unique=True)
    fecha_limite = models.DateField('fecha límite de captura')
    cerrado = models.BooleanField(default=False)
    cerrado_en = models.DateTimeField(null=True, blank=True, editable=False)
    cerrado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                    editable=False, related_name='+')

    class Meta:
        ordering = ['-anio']
        verbose_name = 'periodo de informe'
        verbose_name_plural = 'periodos de informe'

    def __str__(self):
        return f'Informe {self.anio}'

    @classmethod
    def anios_cerrados(cls):
        return set(cls.objects.filter(cerrado=True).values_list('anio', flat=True))

    @classmethod
    def abierto_actual(cls):
        """El periodo abierto más antiguo: el que los académicos deberían estar capturando."""
        return cls.objects.filter(cerrado=False).order_by('anio').first()


class ConfirmacionInforme(models.Model):
    periodo = models.ForeignKey(PeriodoInforme, on_delete=models.CASCADE, related_name='confirmaciones')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='confirmaciones')
    fecha = models.DateTimeField(auto_now_add=True)
    comentario = models.TextField(blank=True)

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'confirmación de informe'
        verbose_name_plural = 'confirmaciones de informe'
        constraints = [models.UniqueConstraint(fields=['periodo', 'usuario'], name='confirmacion_unica')]

    def __str__(self):
        return f'{self.usuario} — {self.periodo}'


from nucleo.historial import registrar_historial  # noqa: E402

registrar_historial(globals())
