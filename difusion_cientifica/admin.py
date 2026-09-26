from django.contrib import admin

from nucleo.admin_base import ParticipanteInline, PropietarioAdmin, lista_personas
from nucleo.utils import prefetch_personas

from .models import (MemoriaInExtenso, MemoriaInExtensoAutor, OrganizacionEventoAcademico,
                     ParticipacionEventoAcademico, ParticipacionEventoAcademicoAutor)


class MemoriaInExtensoAutorInline(ParticipanteInline):
    model = MemoriaInExtensoAutor


@admin.register(MemoriaInExtenso)
class MemoriaInExtensoAdmin(PropietarioAdmin):
    propietarios = ('autores__usuario',)
    autoria = 'autores'
    list_display = ['titulo', 'evento', 'fecha', 'pais']
    search_fields = ['titulo', 'evento']
    campo_fecha = 'fecha'
    campos_similitud = ('titulo',)
    autocomplete_fields = ['pais', 'institucion']
    date_hierarchy = 'fecha'
    inlines = [MemoriaInExtensoAutorInline]


@admin.register(OrganizacionEventoAcademico)
class OrganizacionEventoAcademicoAdmin(PropietarioAdmin):
    list_display = ['evento', 'tipo_participacion']
    list_filter = ['tipo_participacion']
    search_fields = ['evento__nombre']
    campo_fecha = 'evento__fecha_inicio'
    autocomplete_fields = ['evento']


class ParticipacionEventoAcademicoAutorInline(ParticipanteInline):
    model = ParticipacionEventoAcademicoAutor


@admin.register(ParticipacionEventoAcademico)
class ParticipacionEventoAcademicoAdmin(PropietarioAdmin):
    propietarios = ('autores__usuario',)
    autoria = 'autores'
    list_display = ['titulo', 'tipo', 'evento', 'fecha', 'ambito', 'autores_']
    list_filter = ['tipo', 'ambito', 'por_invitacion', 'ponencia_magistral']
    search_fields = ['titulo', 'evento']
    campo_fecha = 'fecha'
    campos_similitud = ('titulo',)
    autocomplete_fields = ['pais', 'institucion']
    date_hierarchy = 'fecha'
    inlines = [ParticipacionEventoAcademicoAutorInline]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(prefetch_personas(self.model, 'autores'))

    @admin.display(description='autores')
    def autores_(self, obj):
        return lista_personas(obj, 'autores')
