from urllib.parse import urlencode

from django.contrib import admin, messages
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from unfold.decorators import action

from nucleo.admin_base import CatalogoAdmin, ParticipanteInline, PropietarioAdmin, lista_personas
from nucleo.models import normalizar_doi
from nucleo.utils import prefetch_personas

from .models import (ActividadApoyoTecnico, ApoyoTecnico, ArticuloCientifico, ArticuloCientificoAutor,
                     CapituloLibroInvestigacion, CapituloLibroInvestigacionAutor, MapaArbitrado, MapaArbitradoAutor,
                     ObjetivoDesarrolloSostenible, ProyectoInvestigacion, ProyectoResponsable, PublicacionTecnica,
                     PublicacionTecnicaAutor)

ESTADO_EDITORIAL = ('Estado editorial', {'fields': (
    'status', 'fecha_enviado', 'fecha_aceptado', 'fecha_enprensa', 'fecha_publicado')})


@admin.register(ObjetivoDesarrolloSostenible)
class ObjetivoDesarrolloSostenibleAdmin(CatalogoAdmin):
    solo_sysadmin = True
    search_fields = ['nombre']


class ProyectoResponsableInline(ParticipanteInline):
    model = ProyectoResponsable


@admin.register(ProyectoInvestigacion)
class ProyectoInvestigacionAdmin(PropietarioAdmin):
    propietarios = ('responsables__usuario', 'participantes__usuario')
    autoria = 'responsables'
    compartido = True
    list_display = ['nombre', 'status', 'financiamiento', 'fecha_inicio', 'fecha_fin', 'responsables_']
    list_filter = ['status', 'financiamiento', 'clasificacion', 'es_permanente']
    search_fields = ['nombre', 'financiamiento_clave']
    campos_similitud = ('nombre',)
    date_hierarchy = 'fecha_inicio'
    autocomplete_fields = ['institucion', 'participantes', 'financiamiento_institucion']
    filter_horizontal = ['objetivos_ods']
    inlines = [ProyectoResponsableInline]
    fieldsets = (
        (None, {'fields': ('nombre', 'descripcion', 'institucion', 'status', 'fecha_inicio', 'fecha_fin',
                           'es_permanente')}),
        ('Clasificación', {'fields': ('clasificacion', 'organizacion', 'modalidad', 'tematica_genero',
                                      'objetivos_ods', 'impacto_social')}),
        ('Financiamiento', {'fields': ('financiamiento', 'financiamiento_clave', 'financiamiento_convocatoria',
                                       'financiamiento_institucion')}),
        ('Participantes', {'fields': ('participantes', 'participantes_externos', 'num_alumnos_licenciatura',
                                      'num_alumnos_maestria', 'num_alumnos_doctorado')}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(prefetch_personas(self.model, 'responsables'))

    @admin.display(description='responsables')
    def responsables_(self, obj):
        return lista_personas(obj, 'responsables')


class ArticuloCientificoAutorInline(ParticipanteInline):
    model = ArticuloCientificoAutor

    def get_extra(self, request, obj=None, **kwargs):
        # Al importar, se muestran tantas filas como autores traiga el registro.
        autores = request.GET.get('_autores')
        return len(autores.split(',')) if obj is None and autores else super().get_extra(request, obj, **kwargs)


@admin.register(ArticuloCientifico)
class ArticuloCientificoAdmin(PropietarioAdmin):
    propietarios = ('autores__usuario', 'alumnos__usuario', 'agradecimientos__usuario')
    autoria = 'autores'
    list_display = ['titulo', 'revista', 'status', 'fecha', 'autores_']
    list_filter = ['status', 'solo_electronico', 'revista__indices']
    search_fields = ['titulo', 'revista__nombre', 'doi']
    campos_similitud = ('titulo',)
    autocomplete_fields = ['revista', 'proyecto', 'alumnos', 'agradecimientos']
    inlines = [ArticuloCientificoAutorInline]
    fieldsets = (
        (None, {'fields': ('titulo', 'revista', 'volumen', 'numero', 'pagina_inicio', 'pagina_fin', 'doi', 'url',
                           'solo_electronico', 'factor_impacto', 'proyecto')}),
        ESTADO_EDITORIAL,
        ('Alumnos y agradecimientos', {'fields': ('alumnos', 'agradecimientos')}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('revista').prefetch_related(prefetch_personas(self.model, 'autores'))

    @admin.display(description='autores')
    def autores_(self, obj):
        return lista_personas(obj, 'autores')

    actions_list = ['importar', 'revisar_duplicados']

    def get_formset_kwargs(self, request, obj, inline, prefix):
        kwargs = super().get_formset_kwargs(request, obj, inline, prefix)
        autores = request.GET.get('_autores', '')
        if obj.pk is None and request.method == 'GET' and isinstance(inline, ArticuloCientificoAutorInline) and autores:
            kwargs['initial'] = [{'persona': pk, 'orden': orden} for orden, pk in enumerate(autores.split(','))
                                 if pk.isdigit()]
        return kwargs

    @action(description='Importar (DOI, BibTeX u ORCID)', icon='download', url_path='importar',
            permissions=['add'])
    def importar(self, request):
        from .importacion import (ErrorImportacion, desde_bibtex, desde_crossref, obras_orcid, parametros_alta)

        def abrir_alta(datos):
            parametros, avisos = parametros_alta(datos, request.user)
            for aviso in avisos:
                messages.info(request, aviso)
            return redirect(f"{reverse('admin:investigacion_articulocientifico_add')}?{urlencode(parametros)}")

        contexto = {**self.admin_site.each_context(request), 'title': 'Importar artículo científico', 'opts': self.opts}
        origen = request.POST if request.method == 'POST' else request.GET
        if request.method == 'GET':
            origen = {'orcid': origen.get('orcid', '')}  # Por GET solo se consulta; importar crea personas.
        try:
            if origen.get('doi'):
                return abrir_alta(desde_crossref(origen['doi']))
            if origen.get('bibtex'):
                entradas = desde_bibtex(origen['bibtex'])
                indice = origen.get('entrada')
                if len(entradas) == 1 or (indice or '').isdigit():
                    return abrir_alta(entradas[int(indice or 0)])
                contexto.update({'entradas': entradas, 'bibtex': origen['bibtex']})
            if origen.get('orcid'):
                obras = obras_orcid(origen['orcid'])
                registrados = set(ArticuloCientifico.objects.filter(
                    doi__in=[doi for _, _, doi in obras if doi]).values_list('doi', flat=True))
                contexto.update({'orcid': origen['orcid'],
                                 'obras': [(t, a, d, d in registrados) for t, a, d in obras]})
        except ErrorImportacion as error:
            messages.error(request, str(error))
        return TemplateResponse(request, 'admin/investigacion/importar.html', contexto)

    def posibles_duplicados(self, request, instancia):
        mismo_doi = []
        if instancia.doi:
            mismo_doi = list(ArticuloCientifico.objects.filter(doi=normalizar_doi(instancia.doi)).exclude(pk=instancia.pk))
        return mismo_doi or super().posibles_duplicados(request, instancia)


class CapituloLibroInvestigacionAutorInline(ParticipanteInline):
    model = CapituloLibroInvestigacionAutor


@admin.register(CapituloLibroInvestigacion)
class CapituloLibroInvestigacionAdmin(PropietarioAdmin):
    propietarios = ('autores__usuario',)
    autoria = 'autores'
    list_display = ['titulo', 'libro', 'autores_']
    search_fields = ['titulo', 'libro__titulo']
    campo_fecha = 'libro__fecha_publicado'
    campos_similitud = ('titulo',)
    autocomplete_fields = ['libro']
    inlines = [CapituloLibroInvestigacionAutorInline]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('libro').prefetch_related(prefetch_personas(self.model, 'autores'))

    @admin.display(description='autores')
    def autores_(self, obj):
        return lista_personas(obj, 'autores')


class MapaArbitradoAutorInline(ParticipanteInline):
    model = MapaArbitradoAutor


@admin.register(MapaArbitrado)
class MapaArbitradoAdmin(PropietarioAdmin):
    propietarios = ('autores__usuario', 'agradecimientos__usuario')
    autoria = 'autores'
    list_display = ['titulo', 'publicacion', 'status', 'fecha']
    list_filter = ['status']
    search_fields = ['titulo', 'publicacion']
    autocomplete_fields = ['pais', 'proyecto', 'agradecimientos']
    inlines = [MapaArbitradoAutorInline]
    fieldsets = (
        (None, {'fields': ('titulo', 'publicacion', 'pais', 'ciudad', 'numero_paginas', 'proyecto')}),
        ESTADO_EDITORIAL,
        ('Agradecimientos', {'fields': ('agradecimientos',)}),
    )


class PublicacionTecnicaAutorInline(ParticipanteInline):
    model = PublicacionTecnicaAutor


@admin.register(PublicacionTecnica)
class PublicacionTecnicaAdmin(PropietarioAdmin):
    propietarios = ('autores__usuario',)
    autoria = 'autores'
    list_display = ['titulo', 'tipo', 'status', 'fecha', 'es_publico']
    list_filter = ['tipo', 'status', 'es_publico']
    search_fields = ['titulo']
    autocomplete_fields = ['institucion', 'proyecto']
    inlines = [PublicacionTecnicaAutorInline]
    fieldsets = (
        (None, {'fields': ('titulo', 'tipo', 'descripcion', 'institucion', 'proyecto', 'es_publico', 'url', 'cita')}),
        ESTADO_EDITORIAL,
    )


@admin.register(ActividadApoyoTecnico)
class ActividadApoyoTecnicoAdmin(CatalogoAdmin):
    list_display = ['nombre', 'tipo', 'orden']
    list_filter = ['tipo']
    list_editable = ['orden']
    search_fields = ['nombre']


@admin.register(ApoyoTecnico)
class ApoyoTecnicoAdmin(PropietarioAdmin):
    list_display = ['__str__', 'actividad', 'proyecto', 'fecha_inicio', 'fecha_fin']
    list_filter = ['actividad__tipo']
    search_fields = ['actividad__nombre', 'actividad_otra', 'proyecto__nombre']
    autocomplete_fields = ['actividad', 'proyecto']
