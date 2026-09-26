from django.contrib import admin

from nucleo.admin_base import CatalogoAdmin, PropietarioAdmin

from .models import ArbitrajePublicacion, Convenio, OtraComision, RedAcademica, ServicioAsesoriaExterna, TipoComision


@admin.register(ArbitrajePublicacion)
class ArbitrajePublicacionAdmin(PropietarioAdmin):
    list_display = ['__str__', 'tipo', 'fecha_dictamen', 'institucion']
    list_filter = ['tipo']
    search_fields = ['revista__nombre', 'obra']
    campo_fecha = 'fecha_dictamen'
    autocomplete_fields = ['revista', 'institucion']
    date_hierarchy = 'fecha_dictamen'


@admin.register(TipoComision)
class TipoComisionAdmin(CatalogoAdmin):
    list_display = ['nombre', 'orden']
    list_editable = ['orden']
    search_fields = ['nombre']


@admin.register(OtraComision)
class OtraComisionAdmin(PropietarioAdmin):
    list_display = ['__str__', 'tipo', 'institucion', 'fecha_inicio', 'fecha_fin']
    list_filter = ['tipo']
    search_fields = ['descripcion', 'institucion__nombre']
    autocomplete_fields = ['tipo', 'institucion']


@admin.register(RedAcademica)
class RedAcademicaAdmin(PropietarioAdmin):
    propietarios = ('participantes__usuario',)
    autoria = 'participantes'
    compartido = True
    list_display = ['nombre', 'ambito', 'fecha_constitucion', 'fecha_fin']
    list_filter = ['ambito']
    search_fields = ['nombre']
    campo_fecha = 'fecha_constitucion'
    campos_similitud = ('nombre',)
    autocomplete_fields = ['instituciones', 'proyecto', 'participantes']

    def anio_cierre(self, obj):
        return obj.fecha_fin.year if obj.fecha_fin else None


@admin.register(Convenio)
class ConvenioAdmin(PropietarioAdmin):
    propietarios = ('participantes__usuario',)
    autoria = 'participantes'
    list_display = ['nombre', 'ambito', 'fecha_inicio', 'fecha_fin', 'es_renovacion']
    list_filter = ['ambito', 'es_renovacion']
    search_fields = ['nombre']
    autocomplete_fields = ['instituciones', 'proyecto', 'participantes']


@admin.register(ServicioAsesoriaExterna)
class ServicioAsesoriaExternaAdmin(PropietarioAdmin):
    list_display = ['nombre', 'institucion', 'fecha_inicio', 'fecha_fin']
    search_fields = ['nombre', 'institucion__nombre']
    autocomplete_fields = ['institucion']
