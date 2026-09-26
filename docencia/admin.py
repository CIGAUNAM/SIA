from django.contrib import admin

from nucleo.admin_base import ParticipanteInline, PropietarioAdmin

from .models import ArticuloDocencia, ArticuloDocenciaAutor, CursoEscolarizado, CursoExtracurricular, ProgramaEstudio


@admin.register(CursoEscolarizado)
class CursoEscolarizadoAdmin(PropietarioAdmin):
    list_display = ['asignatura', 'nivel', 'programa', 'periodo_academico', 'nombramiento', 'total_horas']
    list_filter = ['nivel', 'nombramiento', 'modalidad']
    search_fields = ['asignatura__nombre', 'programa__nombre', 'periodo_academico']
    autocomplete_fields = ['programa', 'asignatura', 'institucion']
    date_hierarchy = 'fecha_inicio'


@admin.register(CursoExtracurricular)
class CursoExtracurricularAdmin(PropietarioAdmin):
    list_display = ['asignatura', 'tipo', 'institucion', 'fecha_inicio', 'total_horas']
    list_filter = ['tipo', 'clasificacion', 'modalidad']
    search_fields = ['asignatura__nombre', 'institucion__nombre']
    autocomplete_fields = ['asignatura', 'institucion']
    date_hierarchy = 'fecha_inicio'


class ArticuloDocenciaAutorInline(ParticipanteInline):
    model = ArticuloDocenciaAutor


@admin.register(ArticuloDocencia)
class ArticuloDocenciaAdmin(PropietarioAdmin):
    propietarios = ('autores__usuario', 'alumnos__usuario', 'agradecimientos__usuario')
    autoria = 'autores'
    list_display = ['titulo', 'status', 'fecha']
    list_filter = ['status']
    search_fields = ['titulo']
    campos_similitud = ('titulo',)
    autocomplete_fields = ['alumnos', 'agradecimientos']
    inlines = [ArticuloDocenciaAutorInline]


@admin.register(ProgramaEstudio)
class ProgramaEstudioAdmin(PropietarioAdmin):
    list_display = ['nombre', 'nivel', 'institucion', 'fecha']
    list_filter = ['nivel']
    search_fields = ['nombre']
    campo_fecha = 'fecha'
    autocomplete_fields = ['institucion']
