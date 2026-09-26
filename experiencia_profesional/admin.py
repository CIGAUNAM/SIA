from django.contrib import admin

from nucleo.admin_base import PropietarioAdmin

from .models import CapacidadPotencialidad, ExperienciaProfesional, LineaInvestigacion


@admin.register(ExperienciaProfesional)
class ExperienciaProfesionalAdmin(PropietarioAdmin):
    list_display = ['cargo', 'nombramiento', 'institucion', 'fecha_inicio', 'fecha_fin']
    search_fields = ['cargo', 'institucion__nombre']
    autocomplete_fields = ['nombramiento', 'institucion']


@admin.register(LineaInvestigacion)
class LineaInvestigacionAdmin(PropietarioAdmin):
    list_display = ['nombre', 'institucion', 'fecha_inicio']
    search_fields = ['nombre']
    autocomplete_fields = ['institucion']
    sujeto_a_cierre = False


@admin.register(CapacidadPotencialidad)
class CapacidadPotencialidadAdmin(PropietarioAdmin):
    list_display = ['nombre', 'fecha_inicio']
    search_fields = ['nombre']
    sujeto_a_cierre = False
