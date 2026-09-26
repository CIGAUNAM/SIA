from django.contrib import admin

from nucleo.admin_base import PropietarioAdmin

from .models import MovilidadAcademica


@admin.register(MovilidadAcademica)
class MovilidadAcademicaAdmin(PropietarioAdmin):
    list_display = ['academico', 'tipo', 'institucion', 'fecha_inicio', 'fecha_fin']
    list_filter = ['tipo', 'financiamiento', 'intercambio_unam']
    search_fields = ['academico', 'institucion__nombre', 'actividades']
    autocomplete_fields = ['institucion', 'redes_academicas', 'proyecto']
    date_hierarchy = 'fecha_inicio'
