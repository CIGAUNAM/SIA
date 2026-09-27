from django.contrib import admin

from nucleo.admin_base import PropietarioAdmin

from .models import ComisionExpertos, DistincionAcademico, DistincionAlumno, SociedadCientifica


@admin.register(DistincionAcademico)
class DistincionAcademicoAdmin(PropietarioAdmin):
    list_display = ['distincion', 'fecha']
    campo_fecha = 'fecha'
    list_filter = ['distincion__tipo', 'distincion__ambito']
    search_fields = ['distincion__nombre']
    autocomplete_fields = ['distincion']
    date_hierarchy = 'fecha'


@admin.register(DistincionAlumno)
class DistincionAlumnoAdmin(PropietarioAdmin):
    propietarios = ('tutores__usuario',)
    autoria = 'tutores'
    list_display = ['distincion', 'alumno', 'nivel', 'fecha']
    campo_fecha = 'fecha'
    list_filter = ['nivel']
    search_fields = ['distincion__nombre', 'alumno__nombre']
    autocomplete_fields = ['distincion', 'alumno', 'tutores']


@admin.register(ComisionExpertos)
class ComisionExpertosAdmin(PropietarioAdmin):
    list_display = ['nombre', 'institucion', 'fecha_inicio', 'fecha_fin']
    search_fields = ['nombre', 'institucion__nombre']
    autocomplete_fields = ['institucion']


@admin.register(SociedadCientifica)
class SociedadCientificaAdmin(PropietarioAdmin):
    list_display = ['nombre', 'tipo', 'ambito', 'fecha_inicio', 'fecha_fin']
    list_filter = ['tipo', 'ambito']
    search_fields = ['nombre']
