from django.contrib import admin

from nucleo.admin_base import CatalogoAdmin, PropietarioAdmin, CompartidoAdmin

from .models import (ActividadApoyo, ApoyoInstitucional, Comision, ComisionInstitucional, LaborDirectivaCoordinacion,
                     RepresentacionOrganoColegiado)


@admin.register(Comision)
class ComisionAdmin(CompartidoAdmin):
    permisos_investigador = ('view',)  # Lo mantiene Administración; el académico solo elige.
    list_display = ['nombre', 'seccion']
    list_filter = ['seccion']
    search_fields = ['nombre']


@admin.register(ActividadApoyo)
class ActividadApoyoAdmin(CatalogoAdmin):
    search_fields = ['nombre']


@admin.register(LaborDirectivaCoordinacion)
class LaborDirectivaCoordinacionAdmin(PropietarioAdmin):
    list_display = ['cargo', 'detalle', 'institucion', 'fecha_inicio', 'fecha_fin']
    search_fields = ['cargo__nombre', 'detalle', 'institucion__nombre']
    autocomplete_fields = ['cargo', 'institucion']


@admin.register(RepresentacionOrganoColegiado)
class RepresentacionOrganoColegiadoAdmin(PropietarioAdmin):
    list_display = ['__str__', 'tipo', 'institucion', 'fecha_inicio', 'fecha_fin']
    list_filter = ['tipo', 'organo']
    search_fields = ['organo_descripcion', 'institucion__nombre']
    autocomplete_fields = ['institucion']


@admin.register(ComisionInstitucional)
class ComisionInstitucionalAdmin(PropietarioAdmin):
    list_display = ['comision', 'funcion', 'detalle', 'institucion', 'fecha_inicio', 'fecha_fin']
    list_filter = ['comision__seccion', 'funcion', 'ambito']
    search_fields = ['comision__nombre', 'detalle', 'institucion__nombre']
    autocomplete_fields = ['comision', 'institucion']


@admin.register(ApoyoInstitucional)
class ApoyoInstitucionalAdmin(PropietarioAdmin):
    list_display = ['actividad', 'tipo', 'institucion', 'fecha_inicio', 'fecha_fin']
    list_filter = ['tipo']
    search_fields = ['actividad__nombre', 'descripcion']
    autocomplete_fields = ['actividad', 'institucion']
