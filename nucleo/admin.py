from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.db.models import Count
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from .admin_base import CatalogoAdmin, ParticipanteInline, VerificableAdmin, es_administrador, persona_de
from .models import (AreaConocimiento, Asignatura, Beca, Cargo, ConfirmacionInforme, Distincion, Evento, Indice,
                     Institucion, Libro, LibroParticipante, MedioDivulgacion, MetricaRevista, Nombramiento, Pais,
                     PeriodoInforme, Persona, ProgramaAcademico, Revista, TipoEvento, User)
from .permisos import GRUPO_INVESTIGADORES

PERFIL = ('Perfil académico', {'fields': (
    'tipo', 'grado', 'semblanza', 'avatar', 'fecha_nacimiento', 'genero', 'pais_origen', 'rfc', 'curp',
    'direccion', 'telefono', 'celular', 'url', 'sni', 'pride',
)})
ADSCRIPCION = ('Adscripción', {'fields': ('ingreso_unam', 'ingreso_entidad', 'egreso_entidad', 'ultimo_contrato')})


admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    """Los administradores gestionan todas las cuentas; cada académico solo edita su propio perfil."""
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    permisos_investigador = ('view', 'change')
    list_display = ['username', 'first_name', 'last_name', 'tipo', 'is_active', 'is_staff', 'cv']
    list_filter = ['tipo', 'is_active', 'is_staff', 'groups']
    autocomplete_fields = ['pais_origen']
    fieldsets = (
        *BaseUserAdmin.fieldsets[:2],
        PERFIL,
        ADSCRIPCION,
        *BaseUserAdmin.fieldsets[2:],
    )
    fieldsets_propios = (
        (None, {'fields': ('username', 'password')}),
        ('Datos personales', {'fields': ('first_name', 'last_name', 'email')}),
        PERFIL,
        ADSCRIPCION,
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs if es_administrador(request.user) else qs.filter(pk=request.user.pk)

    def get_fieldsets(self, request, obj=None):
        if obj is not None and not es_administrador(request.user):
            return self.fieldsets_propios
        return super().get_fieldsets(request, obj)

    def get_readonly_fields(self, request, obj=None):
        if es_administrador(request.user):
            return super().get_readonly_fields(request, obj)
        return ['username', 'ingreso_unam', 'ingreso_entidad', 'egreso_entidad', 'ultimo_contrato']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.is_staff = True  # Todas las cuentas usan el admin como interfaz.
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        if not change and not form.instance.is_superuser:
            form.instance.groups.add(Group.objects.get_or_create(name=GRUPO_INVESTIGADORES)[0])

    def has_add_permission(self, request):
        return es_administrador(request.user) and super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return es_administrador(request.user) and super().has_delete_permission(request, obj)

    @admin.display(description='CV')
    def cv(self, obj):
        return format_html('<a href="{}">PDF</a>', reverse('admin:cv_usuario', args=[obj.pk]))


@admin.register(Persona)
class PersonaAdmin(VerificableAdmin):
    list_display = ['apellidos', 'nombre', 'email', 'usuario', 'verificado']
    search_fields = ['apellidos', 'nombre', 'email', 'orcid', 'usuario__username']
    autocomplete_fields = ['usuario']
    fields = ['nombre', 'apellidos', 'email', 'orcid', 'usuario', 'verificado', 'creado_por', 'creado', 'actualizado']

    def posibles_duplicados(self, request, instancia):
        from .similitud import personas_parecidas
        return personas_parecidas(Persona.objects.all(), instancia.nombre, instancia.apellidos, excluir_pk=instancia.pk)

    def get_readonly_fields(self, request, obj=None):
        campos = super().get_readonly_fields(request, obj)
        return campos if es_administrador(request.user) else [*campos, 'usuario']


@admin.register(Pais)
class PaisAdmin(CatalogoAdmin):
    list_display = ['nombre', 'codigo', 'zona']
    list_filter = ['zona']
    search_fields = ['nombre', 'nombre_extendido', 'codigo']


@admin.register(Institucion)
class InstitucionAdmin(VerificableAdmin):
    list_display = ['nombre', 'padre', 'pais', 'ciudad', 'clasificacion', 'pertenece_unam', 'verificado']
    list_filter = ['clasificacion', 'pertenece_unam', 'subsistema_unam']
    search_fields = ['nombre', 'padre__nombre', 'ciudad', 'pais__nombre']
    autocomplete_fields = ['pais', 'padre']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('padre', 'pais')


@admin.register(AreaConocimiento)
class AreaConocimientoAdmin(CatalogoAdmin):
    list_display = ['nombre', 'categoria']
    list_filter = ['categoria']
    search_fields = ['nombre']


@admin.register(ProgramaAcademico)
class ProgramaAcademicoAdmin(VerificableAdmin):
    list_display = ['nombre', 'nivel', 'area_conocimiento', 'verificado']
    list_filter = ['nivel']
    search_fields = ['nombre']
    autocomplete_fields = ['area_conocimiento']


@admin.register(Asignatura)
class AsignaturaAdmin(VerificableAdmin):
    list_display = ['nombre', 'verificado']
    search_fields = ['nombre']


@admin.register(Beca)
class BecaAdmin(VerificableAdmin):
    list_display = ['nombre', 'verificado']
    search_fields = ['nombre']


@admin.register(Cargo)
class CargoAdmin(VerificableAdmin):
    list_display = ['nombre', 'tipo', 'verificado']
    list_filter = ['tipo']
    search_fields = ['nombre']


@admin.register(Nombramiento)
class NombramientoAdmin(CatalogoAdmin):
    list_display = ['nombre', 'clave']
    search_fields = ['nombre', 'clave']


@admin.register(Distincion)
class DistincionAdmin(VerificableAdmin):
    list_display = ['nombre', 'tipo', 'institucion', 'ambito', 'verificado']
    list_filter = ['tipo', 'ambito']
    search_fields = ['nombre']
    autocomplete_fields = ['institucion']


@admin.register(TipoEvento)
class TipoEventoAdmin(CatalogoAdmin):
    search_fields = ['nombre']


@admin.register(Evento)
class EventoAdmin(VerificableAdmin):
    list_display = ['nombre', 'tipo', 'fecha_inicio', 'pais', 'ciudad', 'ambito', 'verificado']
    list_filter = ['tipo', 'ambito']
    search_fields = ['nombre', 'ciudad']
    autocomplete_fields = ['tipo', 'pais']
    date_hierarchy = 'fecha_inicio'


@admin.register(Indice)
class IndiceAdmin(CatalogoAdmin):
    search_fields = ['nombre']


class MetricaRevistaInline(TabularInline):
    model = MetricaRevista
    fields = ['anio', 'fuente', 'factor_impacto', 'cuartil']
    extra = 0


@admin.register(Revista)
class RevistaAdmin(VerificableAdmin):
    list_display = ['nombre', 'tipo', 'pais', 'issn_impreso', 'issn_electronico', 'verificado']
    list_filter = ['tipo', 'indices']
    search_fields = ['nombre', 'nombre_abreviado', 'issn_impreso', 'issn_electronico']
    autocomplete_fields = ['pais']
    filter_horizontal = ['indices']
    inlines = [MetricaRevistaInline]


@admin.register(MedioDivulgacion)
class MedioDivulgacionAdmin(VerificableAdmin):
    list_display = ['nombre', 'tipo', 'canal', 'pais', 'verificado']
    list_filter = ['tipo']
    search_fields = ['nombre', 'canal']
    autocomplete_fields = ['pais']


class LibroParticipanteInline(ParticipanteInline):
    model = LibroParticipante
    fields = ['persona', 'rol', 'orden']


class MisLibrosFilter(admin.SimpleListFilter):
    title = 'participación'
    parameter_name = 'mios'

    def lookups(self, request, model_admin):
        return [('1', 'Libros en los que participo')]

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(participantes__usuario=request.user).distinct()
        return queryset


@admin.register(Libro)
class LibroAdmin(VerificableAdmin):
    list_display = ['titulo', 'tipo', 'editorial', 'status', 'fecha', 'verificado']
    list_filter = [MisLibrosFilter, 'tipo', 'status']
    search_fields = ['titulo', 'editorial', 'isbn']
    campos_similitud = ('titulo',)
    autocomplete_fields = ['pais', 'agradecimientos']
    inlines = [LibroParticipanteInline]
    fieldsets = (
        (None, {'fields': ('titulo', 'tipo', 'editorial', 'coleccion', 'volumen', 'numero_edicion', 'numero_paginas',
                           'isbn', 'url', 'pais', 'ciudad', 'arbitrado_pares')}),
        ('Estado editorial', {'fields': ('status', 'fecha_enviado', 'fecha_aceptado', 'fecha_enprensa',
                                         'fecha_publicado')}),
        ('Agradecimientos', {'fields': ('agradecimientos',), 'classes': ('collapse',)}),
        ('Registro', {'fields': ('verificado', 'creado_por', 'creado', 'actualizado'), 'classes': ('collapse',)}),
    )

    def puede_modificar(self, request, obj):
        # Un libro no verificado también lo pueden corregir sus autores, editores, coordinadores o compiladores.
        return super().puede_modificar(request, obj) or (
            not obj.verificado and obj.participantes.filter(usuario=request.user).exists())

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        # Quien registra un libro nuevo sin participantes figura como autor.
        libro = form.instance
        if not change and not libro.participantes.exists():
            LibroParticipante.objects.create(libro=libro, persona=persona_de(request.user), orden=1)


@admin.register(PeriodoInforme)
class PeriodoInformeAdmin(CatalogoAdmin):
    list_display = ['anio', 'fecha_limite', 'cerrado', 'confirmados', 'avance', 'excel']
    fields = ['anio', 'fecha_limite', 'cerrado', 'cerrado_en', 'cerrado_por']
    readonly_fields = ['cerrado', 'cerrado_en', 'cerrado_por']
    actions = ['cerrar', 'reabrir']

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(num_confirmaciones=Count('confirmaciones'))

    @admin.display(description='confirmaciones', ordering='num_confirmaciones')
    def confirmados(self, obj):
        return obj.num_confirmaciones

    @admin.display(description='avance')
    def avance(self, obj):
        return format_html('<a href="{}?anio={}">Ver avance</a>', reverse('admin:informe_avance'), obj.anio)

    @admin.display(description='Excel')
    def excel(self, obj):
        return format_html('<a href="{}?anio={}">Descargar</a>', reverse('admin:informe_excel'), obj.anio)

    @admin.action(description='Cerrar los periodos seleccionados')
    def cerrar(self, request, queryset):
        total = queryset.filter(cerrado=False).update(cerrado=True, cerrado_en=timezone.now(), cerrado_por=request.user)
        self.message_user(request, f'{total} periodo(s) cerrados: los académicos ya no pueden modificar esos años.')

    @admin.action(description='Reabrir los periodos seleccionados')
    def reabrir(self, request, queryset):
        total = queryset.filter(cerrado=True).update(cerrado=False, cerrado_en=None, cerrado_por=None)
        self.message_user(request, f'{total} periodo(s) reabiertos.')


@admin.register(ConfirmacionInforme)
class ConfirmacionInformeAdmin(CatalogoAdmin):
    permisos_investigador = ()
    list_display = ['usuario', 'periodo', 'fecha', 'comentario']
    list_filter = ['periodo']
    search_fields = ['usuario__first_name', 'usuario__last_name', 'comentario']

    def has_add_permission(self, request):
        return False
