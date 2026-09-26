from django.contrib import admin

from nucleo.admin_base import ParticipanteInline, PropietarioAdmin

from .models import (AsesoriaEstudiante, ComiteCandidaturaDoctoral, ComiteCandidaturaMiembro, ComiteTutoral,
                     ComiteTutoralMiembro, DireccionTesis, DireccionTesisTutor, GrupoInvestigacionInterno,
                     SupervisionPostdoctoral)


@admin.register(AsesoriaEstudiante)
class AsesoriaEstudianteAdmin(PropietarioAdmin):
    list_display = ['asesorado', 'tipo', 'nivel', 'programa', 'fecha_inicio', 'fecha_fin']
    list_filter = ['tipo', 'nivel']
    search_fields = ['asesorado__nombre', 'asesorado__apellidos', 'programa__nombre']
    autocomplete_fields = ['asesorado', 'programa', 'beca', 'proyecto', 'institucion']


@admin.register(SupervisionPostdoctoral)
class SupervisionPostdoctoralAdmin(PropietarioAdmin):
    list_display = ['investigador', 'titulo_proyecto', 'fecha_inicio', 'fecha_fin']
    search_fields = ['investigador__nombre', 'investigador__apellidos', 'titulo_proyecto']
    autocomplete_fields = ['investigador', 'institucion', 'proyecto', 'beca']


@admin.register(GrupoInvestigacionInterno)
class GrupoInvestigacionInternoAdmin(PropietarioAdmin):
    propietarios = ('integrantes__usuario',)
    autoria = 'integrantes'
    list_display = ['nombre', 'fecha_inicio', 'fecha_fin']
    search_fields = ['nombre']
    autocomplete_fields = ['pais', 'integrantes']


class DireccionTesisTutorInline(ParticipanteInline):
    model = DireccionTesisTutor
    extra = 0


@admin.register(DireccionTesis)
class DireccionTesisAdmin(PropietarioAdmin):
    propietarios = ('director__usuario', 'codirector__usuario', 'tutores__usuario')
    autoria = 'tutores'
    list_display = ['titulo_tesis', 'asesorado', 'nivel', 'status', 'fecha_examen']
    list_filter = ['nivel', 'status']
    search_fields = ['titulo_tesis', 'asesorado__nombre', 'asesorado__apellidos']
    campos_similitud = ('titulo_tesis',)
    autocomplete_fields = ['programa', 'asesorado', 'institucion', 'beca', 'reconocimiento', 'director', 'codirector']
    inlines = [DireccionTesisTutorInline]


class ComiteTutoralMiembroInline(ParticipanteInline):
    model = ComiteTutoralMiembro


@admin.register(ComiteTutoral)
class ComiteTutoralAdmin(PropietarioAdmin):
    propietarios = ('miembros__usuario',)
    autoria = 'miembros'
    list_display = ['estudiante', 'nivel', 'programa', 'fecha_inicio', 'fecha_examen']
    list_filter = ['nivel']
    search_fields = ['estudiante__nombre', 'estudiante__apellidos', 'titulo_tesis']
    autocomplete_fields = ['estudiante', 'programa', 'institucion']
    inlines = [ComiteTutoralMiembroInline]


class ComiteCandidaturaMiembroInline(ParticipanteInline):
    model = ComiteCandidaturaMiembro


@admin.register(ComiteCandidaturaDoctoral)
class ComiteCandidaturaDoctoralAdmin(PropietarioAdmin):
    propietarios = ('director__usuario', 'codirector__usuario', 'asesores__usuario', 'miembros__usuario')
    autoria = 'miembros'
    list_display = ['candidato', 'programa', 'fecha_defensa']
    search_fields = ['candidato__nombre', 'candidato__apellidos', 'titulo_tesis']
    campo_fecha = 'fecha_defensa'
    autocomplete_fields = ['candidato', 'programa', 'institucion', 'director', 'codirector', 'asesores']
    date_hierarchy = 'fecha_defensa'
    inlines = [ComiteCandidaturaMiembroInline]
