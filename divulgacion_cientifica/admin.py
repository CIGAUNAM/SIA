from django.contrib import admin

from nucleo.admin_base import ParticipanteInline, PropietarioAdmin, lista_personas
from nucleo.utils import prefetch_personas

from .models import (ArticuloDivulgacion, ArticuloDivulgacionAutor, OrganizacionEventoDivulgacion,
                     ParticipacionEventoDivulgacion,
                     ParticipacionEventoDivulgacionAutor, ProgramaMedio)


class ArticuloDivulgacionAutorInline(ParticipanteInline):
    model = ArticuloDivulgacionAutor


@admin.register(ArticuloDivulgacion)
class ArticuloDivulgacionAdmin(PropietarioAdmin):
    propietarios = ('autores__usuario', 'agradecimientos__usuario')
    autoria = 'autores'
    list_display = ['titulo', 'revista', 'status', 'fecha', 'autores_']
    list_filter = ['status', 'solo_electronico']
    search_fields = ['titulo', 'revista__nombre']
    campos_similitud = ('titulo',)
    autocomplete_fields = ['revista', 'agradecimientos']
    inlines = [ArticuloDivulgacionAutorInline]
    fieldsets = (
        (None, {'fields': ('titulo', 'revista', 'volumen', 'numero', 'pagina_inicio', 'pagina_fin', 'url',
                           'solo_electronico')}),
        ('Estado editorial', {'fields': ('status', 'fecha_enviado', 'fecha_aceptado', 'fecha_enprensa',
                                         'fecha_publicado')}),
        ('Agradecimientos', {'fields': ('agradecimientos',)}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('revista').prefetch_related(prefetch_personas(self.model, 'autores'))

    @admin.display(description='autores')
    def autores_(self, obj):
        return lista_personas(obj, 'autores')


@admin.register(OrganizacionEventoDivulgacion)
class OrganizacionEventoDivulgacionAdmin(PropietarioAdmin):
    list_display = ['evento', 'tipo_participacion']
    list_filter = ['tipo_participacion']
    search_fields = ['evento__nombre']
    campo_fecha = 'evento__fecha_inicio'
    autocomplete_fields = ['evento']


class ParticipacionEventoDivulgacionAutorInline(ParticipanteInline):
    model = ParticipacionEventoDivulgacionAutor


@admin.register(ParticipacionEventoDivulgacion)
class ParticipacionEventoDivulgacionAdmin(PropietarioAdmin):
    propietarios = ('autores__usuario',)
    autoria = 'autores'
    list_display = ['titulo', 'tipo', 'evento', 'fecha', 'ambito']
    list_filter = ['tipo', 'ambito', 'por_invitacion']
    search_fields = ['titulo', 'evento__nombre']
    campo_fecha = 'fecha'
    campos_similitud = ('titulo',)
    autocomplete_fields = ['evento', 'institucion']
    date_hierarchy = 'fecha'
    inlines = [ParticipacionEventoDivulgacionAutorInline]


@admin.register(ProgramaMedio)
class ProgramaMedioAdmin(PropietarioAdmin):
    list_display = ['tema', 'medio', 'actividad', 'fecha']
    list_filter = ['actividad', 'medio__tipo']
    search_fields = ['tema', 'medio__nombre']
    campo_fecha = 'fecha'
    autocomplete_fields = ['medio']
    date_hierarchy = 'fecha'
