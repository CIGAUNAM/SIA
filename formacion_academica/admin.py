from django.contrib import admin

from nucleo.admin_base import PropietarioAdmin

from .models import CursoEspecializacion, Grado, Postdoctorado


@admin.register(Grado)
class GradoAdmin(PropietarioAdmin):
    list_display = ['titulo_obtenido', 'nivel', 'institucion', 'fecha_grado']
    campo_fecha = 'fecha_grado'
    list_filter = ['nivel']
    search_fields = ['titulo_obtenido', 'titulo_tesis', 'institucion__nombre']
    autocomplete_fields = ['institucion']


@admin.register(Postdoctorado)
class PostdoctoradoAdmin(PropietarioAdmin):
    list_display = ['titulo_proyecto', 'institucion', 'tutor', 'fecha_inicio', 'fecha_fin']
    search_fields = ['titulo_proyecto', 'institucion__nombre']
    autocomplete_fields = ['institucion', 'tutor', 'proyecto']


@admin.register(CursoEspecializacion)
class CursoEspecializacionAdmin(PropietarioAdmin):
    list_display = ['nombre', 'tipo', 'horas', 'institucion', 'fecha_inicio', 'fecha_fin']
    list_filter = ['tipo', 'modalidad']
    search_fields = ['nombre', 'institucion__nombre']
    autocomplete_fields = ['institucion']
    date_hierarchy = 'fecha_inicio'
