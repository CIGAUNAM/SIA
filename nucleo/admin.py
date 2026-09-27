from django.contrib import admin, messages
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import action
from unfold.forms import AdminPasswordChangeForm
from unfold.widgets import UnfoldAdminTextareaWidget

from .admin_base import CatalogoAdmin, FormularioSIA, ParticipanteInline, VerificableAdmin, es_administrador
from .externos import ErrorServicio, nombre_orcid, orcid_por_correo
from .formularios import UserChangeForm, UserCreationForm, registros_de
from .nombres import normalizar_orcid
from .models import (AreaConocimiento, Asignatura, Beca, Cargo, ConfiguracionEntidad, ConfirmacionInforme, Distincion,
                     Evento, Indice, Institucion, Libro, LibroParticipante, MedioDivulgacion, MetricaRevista,
                     Nombramiento, Pais, PeriodoInforme, Persona, ProgramaAcademico, Revista, TipoEvento, User)
from .permisos import GRUPO_INVESTIGADORES

DATOS_PERSONALES = ('Datos personales', {'fields': (
    'grado', 'first_name', 'last_name', 'fecha_nacimiento', 'genero', 'pais_origen', 'rfc', 'curp', 'telefono', 'avatar',
)})
PUBLICACIONES = ('Nombre en publicaciones', {'fields': ('figura_como', 'orcid', 'nombre_persona')})
PERFIL = ('Perfil académico', {'fields': ('tipo', 'semblanza', 'domicilio', 'url', 'sni', 'pride')})
ADSCRIPCION = ('Adscripción', {'fields': ('ingreso_unam', 'ingreso_entidad', 'egreso_entidad', 'ultimo_contrato')})


admin.site.unregister(Group)


class DomicilioWidget(UnfoldAdminTextareaWidget):
    """Área de texto con un botón para copiar el domicilio de la entidad."""
    template_name = 'nucleo/widgets/domicilio.html'

    def __init__(self, domicilio_entidad='', attrs=None):
        self.domicilio_entidad = domicilio_entidad
        super().__init__({'rows': 3, **(attrs or {})})

    def get_context(self, name, value, attrs):
        return {**super().get_context(name, value, attrs), 'domicilio_entidad': self.domicilio_entidad}


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
    list_display = ['email', 'first_name', 'last_name', 'nombre_publicaciones', 'orcid', 'tipo', 'is_active', 'cv']
    list_filter = ['tipo', 'is_active', 'is_staff', 'groups']
    search_fields = ['email', 'first_name', 'last_name', 'persona__nombre', 'persona__orcid']
    ordering = ['first_name', 'last_name']
    autocomplete_fields = ['pais_origen', 'persona']
    list_select_related = ['persona']
    actions_list = ['sugerir_orcid']
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email', 'first_name', 'last_name')}),
        ('Nombre en publicaciones', {'fields': ('orcid', 'nombre_persona')}),  # + es_persona si hay parecidas
        ('Contraseña', {'fields': ('usable_password', 'password1', 'password2')}),
    )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        DATOS_PERSONALES,
        PUBLICACIONES,
        ('Persona asociada', {'classes': ['collapse'], 'fields': ('persona',)}),
        PERFIL,
        ADSCRIPCION,
        *BaseUserAdmin.fieldsets[2:],
    )
    fieldsets_propios = (
        (None, {'fields': ('email', 'password')}),
        DATOS_PERSONALES,
        PUBLICACIONES,
        PERFIL,
        ADSCRIPCION,
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs if es_administrador(request.user) else qs.filter(pk=request.user.pk)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'domicilio':
            kwargs['widget'] = DomicilioWidget(ConfiguracionEntidad.actual(request).direccion)
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.administrador = es_administrador(request.user)
        return form

    def get_fieldsets(self, request, obj=None):
        if obj is not None and not es_administrador(request.user):
            return self.fieldsets_propios
        return super().get_fieldsets(request, obj)

    def get_readonly_fields(self, request, obj=None):
        if es_administrador(request.user):
            return [*super().get_readonly_fields(request, obj), 'figura_como']
        return ['email', 'figura_como', 'ingreso_unam', 'ingreso_entidad', 'egreso_entidad', 'ultimo_contrato']

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        adminform = context['adminform']
        if add and 'es_persona' in adminform.form.pregunta:
            # La pregunta "¿Es alguna de estas personas?" solo aparece cuando hay coautores parecidos.
            adminform.fieldsets = [
                (nombre, {**opciones, 'fields': (*opciones['fields'], 'es_persona')})
                if nombre == 'Nombre en publicaciones' else (nombre, opciones)
                for nombre, opciones in adminform.fieldsets]
        return super().render_change_form(request, context, add, change, form_url, obj)

    def has_sugerir_orcid_permission(self, request):
        return es_administrador(request.user)

    @action(description='Sugerir ORCID', icon='fingerprint', url_path='sugerir-orcid',
            permissions=['sugerir_orcid'])
    def sugerir_orcid(self, request):
        """ORCID probables de las cuentas que no lo tienen (por nombre y afiliación); el administrador confirma."""
        from .sugerencias_orcid import asignar_orcid, preseleccion, sugerencias

        if request.method == 'POST':
            guardados = 0
            for clave, valor in request.POST.items():
                orcid = normalizar_orcid(valor)
                if not clave.startswith('cuenta_') or not orcid:
                    continue
                cuenta = get_object_or_404(User.objects.select_related('persona'), pk=clave.removeprefix('cuenta_'))
                try:
                    with transaction.atomic():
                        unida = asignar_orcid(cuenta.persona, orcid)
                except ValueError as error:
                    self.message_user(request, f'{cuenta}: {error}', messages.ERROR)
                    continue
                guardados += 1
                if unida is not None:
                    self.message_user(request, f'{cuenta}: se unió «{unida}», que ya tenía ese ORCID.')
            self.message_user(request, f'Se guardó el ORCID de {guardados} cuenta(s).', messages.SUCCESS)
            return redirect(request.get_full_path())
        filas = [(cuenta, candidatos, preseleccion(candidatos)) for cuenta, candidatos in sugerencias(request)]
        contexto = {**self.admin_site.each_context(request), 'opts': self.opts, 'filas': filas,
                    'sin_orcid': User.objects.filter(is_active=True, persona__orcid='').count(),
                    'afiliacion': '/'.join(x for x in (ConfiguracionEntidad.actual(request).siglas,
                                                        ConfiguracionEntidad.actual(request).institucion_madre_siglas) if x),
                    'title': 'Sugerencias de ORCID'}
        return TemplateResponse(request, 'admin/nucleo/sugerir_orcid.html', contexto)

    @admin.display(description='Figura como')
    def figura_como(self, obj):
        persona = obj.persona
        orcid = (format_html('<a href="https://orcid.org/{0}" target="_blank" rel="noopener">ORCID {0}</a>',
                             persona.orcid) if persona.orcid else 'sin ORCID')
        return format_html('<a href="{}" class="font-semibold text-primary-600">{}</a> · {} · {}',
                           reverse('admin:nucleo_persona_change', args=[persona.pk]), persona, orcid,
                           registros_de(persona))

    @admin.display(description='Nombre en publicaciones', ordering='persona__nombre')
    def nombre_publicaciones(self, obj):
        return obj.persona

    @admin.display(description='ORCID', ordering='persona__orcid')
    def orcid(self, obj):
        return obj.persona.orcid or '—'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.is_staff = True  # Todas las cuentas usan el admin como interfaz.
        super().save_model(request, obj, form, change)
        if getattr(form, 'orcid_encontrado', False):
            messages.info(request, f'Se encontró su ORCID ({obj.persona.orcid}) a partir del correo.')
        if getattr(form, 'resumen_fusion', None):
            messages.info(request, f'El ORCID ya estaba en el catálogo: se unió {form.resumen_fusion} a esta cuenta.')

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


class PersonaForm(FormularioSIA):
    """Sin ORCID pero con correo, el ORCID se busca en ORCID; sin nombre, se toma del registro de ORCID."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'nombre' in self.fields:
            self.fields['nombre'].required = False
            self.fields['nombre'].help_text += ' Si lo dejas vacío, se toma de ORCID.'

    def clean(self):
        datos = super().clean()
        if ('orcid' in self.fields and not datos.get('orcid') and datos.get('email')
                and (self.instance.pk is None or 'email' in self.changed_data)):
            try:
                encontrado = orcid_por_correo(datos['email'])
            except ErrorServicio:
                encontrado = None
            if encontrado and not Persona.objects.filter(orcid=encontrado[0]).exclude(pk=self.instance.pk).exists():
                datos['orcid'] = encontrado[0]
                datos['nombre'] = datos.get('nombre') or encontrado[1]
        if 'nombre' in self.fields and not datos.get('nombre'):
            if not datos.get('orcid'):
                self.add_error('nombre', 'Escribe el nombre para mostrar, un ORCID o un correo público en ORCID.')
            else:
                try:
                    datos['nombre'] = nombre_orcid(datos['orcid'])
                except ErrorServicio as error:
                    self.add_error('nombre', f'No se pudo consultar ORCID ({error}). Escribe el nombre.')
                else:
                    if not datos['nombre']:
                        self.add_error('nombre', 'Ese ORCID no tiene un nombre público. Escribe el nombre.')
        return datos


@admin.register(Persona)
class PersonaAdmin(VerificableAdmin):
    form = PersonaForm
    list_display = ['nombre', 'orcid', 'email', 'cuenta', 'verificado']
    list_select_related = ['usuario']
    search_fields = ['nombre', 'email', 'orcid', 'usuario__email']
    fields = ['nombre', 'orcid', 'email', 'cuenta', 'verificado', 'creado_por', 'creado', 'actualizado']

    @admin.display(description='cuenta', ordering='usuario__email')
    def cuenta(self, obj):
        usuario = getattr(obj, 'usuario', None)
        if usuario is None:
            return '—'
        return format_html('<a href="{}">{}</a>', reverse('admin:nucleo_user_change', args=[usuario.pk]), usuario.email)

    def posibles_duplicados(self, request, instancia):
        from .similitud import personas_parecidas
        return personas_parecidas(Persona.objects.all(), instancia.nombre, excluir_pk=instancia.pk)

    def get_search_results(self, request, queryset, search_term):
        queryset, duplicados = super().get_search_results(request, queryset, search_term)
        if request.GET.get('model_name') == 'user' and request.GET.get('field_name') == 'persona':
            queryset = queryset.filter(usuario__isnull=True)  # Al ligar una cuenta, solo personas sin cuenta.
        return queryset, duplicados

    def get_readonly_fields(self, request, obj=None):
        return [*super().get_readonly_fields(request, obj), 'cuenta']


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
            LibroParticipante.objects.create(libro=libro, persona=request.user.persona, orden=1)


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


@admin.register(ConfiguracionEntidad)
class ConfiguracionEntidadAdmin(SimpleHistoryAdmin, ModelAdmin):
    """Un solo registro por entidad: la lista lleva directo a editarlo."""
    permisos_investigador = ()
    autocomplete_fields = ['pais_sede']
    fieldsets = (
        ('Identidad', {'fields': ('nombre', 'siglas', 'institucion_madre', 'institucion_madre_siglas', 'logo')}),
        ('Dirección y contacto', {'fields': ('titular', 'cargo_titular', 'ciudad', 'direccion', 'telefono', 'correo',
                                             'sitio_web')}),
        ('Documentos', {'fields': ('consejo_tecnico',)}),
        ('Operación', {'fields': ('pais_sede', 'remitente', 'anios_tablero', 'meses_publicacion_pendiente')}),
    )

    def has_add_permission(self, request):
        return super().has_add_permission(request) and not ConfiguracionEntidad.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        if not self.has_view_or_change_permission(request):
            raise PermissionDenied
        configuracion = ConfiguracionEntidad.objects.first()
        if configuracion is None:
            return redirect('admin:nucleo_configuracionentidad_add')
        return redirect('admin:nucleo_configuracionentidad_change', configuracion.pk)
