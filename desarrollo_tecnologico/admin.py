from django.contrib import admin

from nucleo.admin_base import ParticipanteInline, PropietarioAdmin

from .models import DesarrolloTecnologico, DesarrolloTecnologicoAutor


class DesarrolloTecnologicoAutorInline(ParticipanteInline):
    model = DesarrolloTecnologicoAutor


@admin.register(DesarrolloTecnologico)
class DesarrolloTecnologicoAdmin(PropietarioAdmin):
    propietarios = ('autores__usuario',)
    autoria = 'autores'
    list_display = ['nombre', 'version', 'licencia', 'fecha']
    search_fields = ['nombre', 'descripcion']
    campo_fecha = 'fecha'
    campos_similitud = ('nombre',)
    autocomplete_fields = ['proyecto']
    inlines = [DesarrolloTecnologicoAutorInline]
