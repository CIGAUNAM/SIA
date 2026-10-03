"""Informes que Administración arma en el sitio: una lista ordenada de gráficas, cada una con un indicador del
catálogo (`informes.indicadores`), su tipo de gráfica, textos y colores. Cualquier informe sirve de plantilla para
otro (se duplica y se cambia el periodo)."""

import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from .indicadores import OPCIONES_INDICADOR, TIPOS

#: Colores de las gráficas del informe anual (en el orden en que se asignan a las series).
PALETA = ['#7A8B3A', '#4A7C8C', '#B87333', '#C4A85A', '#949A90', '#A5B07A', '#2D3A2E', '#7FA1B0']


def validar_periodo(valor):
    m = re.fullmatch(r'(\d{4})-(\d{4})', valor or '')
    if not m or int(m.group(2)) != int(m.group(1)) + 1:
        raise ValidationError('Escribe el periodo como «2025-2026» (de julio a junio).')


def validar_colores(valor):
    for color in [c.strip() for c in (valor or '').split(',') if c.strip()]:
        if not re.fullmatch(r'#[0-9A-Fa-f]{6}', color):
            raise ValidationError(f'«{color}» no es un color: usa el formato #7A8B3A, separados por comas.')


class Informe(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField('descripción', blank=True)
    periodo = models.CharField(max_length=9, validators=[validar_periodo],
                               help_text='De julio a junio, p. ej. «2025-2026».')
    es_plantilla = models.BooleanField('es plantilla', default=False,
                                       help_text='Aparece como punto de partida para informes nuevos.')
    pie = models.CharField('pie de las gráficas', max_length=255, blank=True,
                           default='{entidad} · {institucion} — Informe Anual {periodo}',
                           help_text='Se puede usar {entidad}, {institucion}, {periodo}, {anio}, {inicio} y {fin}.')
    basado_en = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, editable=False,
                                  related_name='derivados', verbose_name='basado en')
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                   editable=False, related_name='+')
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-es_plantilla', '-periodo', 'nombre']

    def __str__(self):
        return f'{self.nombre} ({self.periodo})'

    def duplicar(self, usuario, nombre=None, periodo=None, es_plantilla=False):
        """Copia del informe con todas sus gráficas (para partir de una plantilla o de un informe anterior)."""
        copia = Informe.objects.create(
            nombre=nombre or f'{self.nombre} (copia)', descripcion=self.descripcion, periodo=periodo or self.periodo,
            es_plantilla=es_plantilla, pie=self.pie, basado_en=self, creado_por=usuario)
        for g in self.graficas.all():
            g.pk, g.informe = None, copia
            g.save()
        return copia


class Grafica(models.Model):
    informe = models.ForeignKey(Informe, on_delete=models.CASCADE, related_name='graficas')
    orden = models.PositiveSmallIntegerField(default=0)
    seccion = models.CharField('sección', max_length=255, blank=True,
                               help_text='Encabezado bajo el que va la gráfica, p. ej. «Eje 2 · Investigación».')
    indicador = models.CharField(max_length=40, choices=OPCIONES_INDICADOR)
    tipo = models.CharField('tipo de gráfica', max_length=20, choices=TIPOS)
    titulo = models.CharField('título', max_length=255,
                              help_text='Se puede usar {entidad}, {periodo}, {anio}, {inicio} y {fin}.')
    subtitulo = models.CharField('subtítulo', max_length=255, blank=True)
    nota = models.TextField(blank=True, help_text='Texto que acompaña a la gráfica en el documento.')
    periodos = models.PositiveSmallIntegerField(
        'periodos a mostrar', default=1, help_text='Para las gráficas históricas: cuántos periodos, hasta el del informe.')
    colores = models.CharField(max_length=255, blank=True, validators=[validar_colores],
                               help_text='Opcional: colores de las series, p. ej. «#7A8B3A, #4A7C8C».')
    mostrar_total = models.BooleanField('mostrar el total', default=True)
    mostrar_valores = models.BooleanField('mostrar los valores', default=True)
    apilado = models.BooleanField('series apiladas', default=True)
    visible = models.BooleanField(default=True)

    class Meta:
        ordering = ['informe', 'orden', 'pk']
        verbose_name = 'gráfica'
        verbose_name_plural = 'gráficas'

    def __str__(self):
        return self.titulo

    def clean(self):
        super().clean()
        from .indicadores import INDICADORES

        indicador = INDICADORES.get(self.indicador)
        if indicador and self.tipo and self.tipo not in indicador.tipos:
            nombres = dict(TIPOS)
            raise ValidationError({'tipo': 'Para este indicador elige: ' +
                                           ', '.join(nombres[t] for t in indicador.tipos) + '.'})

    def paleta(self):
        propios = [c.strip() for c in self.colores.split(',') if c.strip()]
        return propios + [c for c in PALETA if c not in propios]


class CifraHistorica(models.Model):
    """Cifra agregada de un año sin datos por persona en el SIA (p. ej. el PRIDE de 2020 que trae la hoja de
    evolución). Los indicadores la usan solo para los años que el SIA no puede calcular."""
    indicador = models.CharField(max_length=40)
    anio = models.PositiveSmallIntegerField('año', help_text='Año de corte (agosto); el periodo 2020-2021 es 2021.')
    panel = models.CharField(max_length=100, blank=True, help_text='P. ej. «Investigadores»; vacío si no aplica.')
    categoria = models.CharField('categoría', max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    fuente = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['indicador', 'anio', 'panel', 'categoria']
        verbose_name = 'cifra histórica'
        verbose_name_plural = 'cifras históricas'
        constraints = [models.UniqueConstraint(fields=['indicador', 'anio', 'panel', 'categoria'],
                                               name='cifra_historica_unica')]

    def __str__(self):
        return f'{self.indicador} {self.anio} {self.panel} {self.categoria}: {self.valor}'.replace('  ', ' ')

    @classmethod
    def de(cls, indicador, anio, panel=''):
        """{categoría: valor} de un año, o {} si no hay cifras históricas."""
        return {c: int(v) if v == int(v) else float(v) for c, v in
                cls.objects.filter(indicador=indicador, anio=anio, panel=panel).values_list('categoria', 'valor')}


class Emision(models.Model):
    """Versión emitida (oficial) de un informe: sus cifras y textos congelados. No cambia aunque después se capturen
    o corrijan registros; para incorporarlos se emite otra versión, con su motivo."""
    informe = models.ForeignKey(Informe, on_delete=models.PROTECT, related_name='emisiones')
    version = models.PositiveSmallIntegerField('versión')
    periodo = models.CharField(max_length=9)
    emitido_en = models.DateTimeField('emitido el', auto_now_add=True)
    emitido_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                    related_name='+', verbose_name='emitido por')
    motivo = models.TextField(blank=True, help_text='Obligatorio desde la segunda versión: qué cambió y por qué.')
    datos = models.JSONField(editable=False)

    class Meta:
        ordering = ['informe', '-version']
        verbose_name = 'emisión'
        verbose_name_plural = 'emisiones'
        constraints = [models.UniqueConstraint(fields=['informe', 'version'], name='emision_version_unica')]

    def __str__(self):
        return f'{self.informe.nombre} {self.periodo} · versión {self.version}'


from nucleo.historial import registrar_historial  # noqa: E402

registrar_historial(globals())
