from cities_light.models import City, Country, Region, SubRegion
from django.apps import apps
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
from django.utils.http import urlencode
from django.utils.text import capfirst
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import action
from unfold.forms import AdminPasswordChangeForm
from unfold.widgets import UnfoldAdminTextareaWidget

from .admin_base import (CatalogoAdmin, EtiquetaPersonaMixin, FormularioSIA, ParticipanteInline, CompartidoAdmin,
                         es_administrador)
from .externos import ErrorServicio, datos_orcid, orcid_por_correo
from .formularios import UserChangeForm, UserCreationForm, registros_de
from .widgets import BuscarOrcidWidget
from .admin_base import SECCIONES_PERFIL
from .nombres import normalizar_orcid
from .models import (AreaConocimiento, Asignatura, Beca, Cargo, ConfiguracionEntidad, ConfirmacionInforme, Distincion,
                     Evento, Indice, Institucion, Libro, LibroParticipante, MedioDivulgacion, MetricaRevista,
                     Nombramiento, PeriodoInforme, Persona, ProgramaAcademico, Revista, SituacionAcademica, TipoEvento,
                     User, anio_o_sf)
from .permisos import GRUPO_ACADEMICOS, GRUPO_ADMINISTRACION, es_sysadmin

DATOS_PERSONALES = ('Datos personales', {'fields': (
    'grado', 'first_name', 'last_name', 'fecha_nacimiento', 'genero', 'pais_origen', 'rfc', 'curp', 'telefono', 'avatar',
)})
def _periodo(registro):
    """'2015–2019', '2015–actual' o el año de la fecha principal del registro, si la tiene."""
    inicio = getattr(registro, 'fecha_inicio', None)
    if inicio:
        if not hasattr(registro, 'fecha_fin'):
            return f'desde {anio_o_sf(inicio)}'
        return f"{anio_o_sf(inicio)}–{anio_o_sf(registro.fecha_fin) if registro.fecha_fin else 'actual'}"
    fecha = next((getattr(registro, campo) for campo in ('fecha_grado', 'fecha', 'fecha_obtencion')
                  if getattr(registro, campo, None)), None)
    return anio_o_sf(fecha) if fecha else ''


PUBLICACIONES = ('Nombre en publicaciones', {'fields': ('orcid', 'nombre_persona', 'figura_como')})
PERFIL = ('Perfil académico', {'fields': ('tipo', 'semblanza', 'domicilio', 'url', 'sni', 'pride')})
ADSCRIPCION = ('Adscripción', {'fields': ('numero_trabajador', 'ingreso_unam', 'ingreso_entidad', 'egreso_entidad',
                                           'ultimo_contrato')})




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
class UserAdmin(EtiquetaPersonaMixin, BaseUserAdmin, ModelAdmin):
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
        (None, {'fields': ('email', 'contrasena')}),
        DATOS_PERSONALES,
        PUBLICACIONES,
        PERFIL,
        ADSCRIPCION,
    )
    #: Debajo del formulario: formación académica y experiencia profesional de la cuenta.
    change_form_after_template = 'admin/nucleo/perfil_trayectoria.html'

    def es_mi_perfil(self, request, obj):
        """La propia cuenta se edita como "Mi perfil", sin controles administrativos (aun siendo administrador).

        Un superusuario puede ver la versión completa de su cuenta con `?completo=1`.
        """
        return (obj is not None and obj.pk == request.user.pk
                and not (es_sysadmin(request.user) and request.GET.get('completo')))

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
        if obj is not None and (not es_administrador(request.user) or self.es_mi_perfil(request, obj)):
            return self.fieldsets_propios
        fieldsets = super().get_fieldsets(request, obj)
        if obj is not None and not es_sysadmin(request.user):
            # Administración no asigna grupos, permisos ni superusuarios: solo activa o desactiva cuentas.
            fieldsets = [('Acceso', {'fields': ('is_active', 'grupos'), 'description': (
                'Los grupos y permisos los asigna un superusuario.')}) if 'is_superuser' in opciones.get('fields', ())
                         else (nombre, opciones) for nombre, opciones in fieldsets]
        return fieldsets

    def has_change_permission(self, request, obj=None):
        # Administración no edita superusuarios ni a otros miembros de Administración (p. ej. su contraseña).
        if (obj is not None and obj != request.user and not es_sysadmin(request.user)
                and (obj.is_superuser or obj.groups.filter(name=GRUPO_ADMINISTRACION).exists())):
            return False
        return super().has_change_permission(request, obj)

    @admin.display(description='grupos')
    def grupos(self, obj):
        return ', '.join(obj.groups.values_list('name', flat=True)) or '—'

    def get_readonly_fields(self, request, obj=None):
        if es_administrador(request.user) and not self.es_mi_perfil(request, obj):
            return [*super().get_readonly_fields(request, obj), 'figura_como', 'grupos']
        campos = ['email', 'contrasena', 'figura_como']
        if not es_administrador(request.user):
            campos.append('tipo')  # El tipo (investigador, técnico...) lo asigna un administrador.
        return campos

    def trayectoria(self, request, obj):
        """Secciones de formación y experiencia de la cuenta, con enlaces para agregar y editar que vuelven aquí."""
        volver = request.get_full_path()
        secciones = []
        for app_label in SECCIONES_PERFIL:
            modelos = []
            for modelo, model_admin in admin.site._registry.items():
                if modelo._meta.app_label != app_label or not model_admin.has_view_or_change_permission(request):
                    continue
                opts = modelo._meta
                parametros = {'volver': volver, **({} if obj.pk == request.user.pk else {'usuario': obj.pk})}
                registros = [{
                    'texto': str(r), 'periodo': _periodo(r),
                    'url': f"{reverse(f'admin:{opts.app_label}_{opts.model_name}_change', args=[r.pk])}?"
                           f"{urlencode({'volver': volver})}",
                } for r in modelo._default_manager.filter(usuario=obj)]
                modelos.append({
                    'titulo': capfirst(opts.verbose_name_plural), 'registros': registros,
                    'agregar': (f"{reverse(f'admin:{opts.app_label}_{opts.model_name}_add')}?{urlencode(parametros)}"
                                if model_admin.has_add_permission(request) else None),
                })
            secciones.append({'titulo': apps.get_app_config(app_label).verbose_name, 'modelos': modelos})
        return secciones

    def response_change(self, request, obj):
        if obj.pk == request.user.pk and not any(b in request.POST for b in ('_continue', '_addanother', '_saveasnew')):
            super().response_change(request, obj)  # Deja el mensaje de "se guardó".
            return redirect(request.get_full_path())  # En "Mi perfil", guardar deja en la misma página.
        return super().response_change(request, obj)

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        if obj is not None:
            context['trayectoria'] = self.trayectoria(request, obj)
            if self.es_mi_perfil(request, obj):
                context.update(title='Mi perfil', subtitle=None, es_mi_perfil=True, show_save_and_add_another=False,
                               version_completa=es_sysadmin(request.user))
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
            form.instance.groups.add(Group.objects.get_or_create(name=GRUPO_ACADEMICOS)[0])

    def has_add_permission(self, request):
        return es_administrador(request.user) and super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.pk == request.user.pk:
            return False  # Nadie borra su propia cuenta desde "Mi perfil".
        return es_administrador(request.user) and super().has_delete_permission(request, obj)

    @admin.display(description='contraseña')
    def contrasena(self, obj):
        return format_html('<a href="{}" class="text-primary-600">Cambiar mi contraseña</a>',
                           reverse('admin:password_change'))

    @admin.display(description='CV')
    def cv(self, obj):
        return format_html('<a href="{}">PDF</a>', reverse('admin:cv_usuario', args=[obj.pk]))


class PersonaForm(FormularioSIA):
    """Completa lo que falte con el registro público de ORCID: con el ORCID, el nombre y el correo; con el correo
    (si es público en ORCID), el ORCID y el nombre. El botón "Buscar en ORCID" hace lo mismo sin guardar."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'nombre' in self.fields:
            self.fields['nombre'].required = False
            self.fields['nombre'].help_text += ' Si lo dejas vacío, se toma de ORCID.'

    def clean(self):
        datos = super().clean()
        if 'orcid' not in self.fields:
            return datos
        encontrado = {}
        try:
            if datos.get('orcid') and not (datos.get('nombre') and datos.get('email')):
                encontrado = datos_orcid(datos['orcid'])
            elif not datos.get('orcid') and datos.get('email') and (
                    self.instance.pk is None or 'email' in self.changed_data):
                por_correo = orcid_por_correo(datos['email'])
                if por_correo and not Persona.objects.filter(orcid=por_correo[0]).exclude(pk=self.instance.pk).exists():
                    encontrado = {'orcid': por_correo[0], 'nombre': por_correo[1]}
        except ErrorServicio as error:
            if not datos.get('nombre'):
                self.add_error('nombre', f'No se pudo consultar ORCID ({error}). Escribe el nombre.')
                return datos
        for campo in ('orcid', 'nombre', 'email'):
            if not datos.get(campo) and encontrado.get(campo):
                datos[campo] = encontrado[campo]
        if not datos.get('nombre'):
            self.add_error('nombre', 'Escribe el nombre para mostrar, o un ORCID o correo públicos en ORCID.' if not
                           datos.get('orcid') else 'Ese ORCID no tiene un nombre público. Escribe el nombre.')
        return datos


class TieneCuentaFilter(admin.SimpleListFilter):
    title = '¿tiene cuenta?'
    parameter_name = 'cuenta'

    def lookups(self, request, model_admin):
        return [('si', 'Con cuenta'), ('no', 'Sin cuenta')]

    def queryset(self, request, queryset):
        if self.value() in ('si', 'no'):
            return queryset.filter(usuario__isnull=self.value() == 'no')
        return queryset


@admin.register(Persona)
class PersonaAdmin(CompartidoAdmin):
    form = PersonaForm

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('usuario')  # Para la marca de adscripción.

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'orcid':
            kwargs['widget'] = BuscarOrcidWidget({'orcid': 'id_orcid', 'nombre': 'id_nombre', 'email': 'id_email'},
                                                 campo_correo='id_email', en_persona=True)
        return super().formfield_for_dbfield(db_field, request, **kwargs)
    list_display = ['nombre', 'orcid', 'email', 'cuenta']
    list_filter = [TieneCuentaFilter]
    list_select_related = ['usuario']
    search_fields = ['nombre', 'email', 'orcid', 'usuario__email', 'usuario__first_name', 'usuario__last_name']
    fields = ['cuenta', 'nombre', 'orcid', 'email', 'creado_por', 'creado', 'actualizado']

    @admin.display(description='cuenta vinculada', ordering='usuario__email')
    def cuenta(self, obj):
        usuario = getattr(obj, 'usuario', None)
        if usuario is None:
            return 'Sin cuenta (coautor u otra persona externa)'
        return format_html('<a href="{}" class="font-medium text-primary-600">{}</a> ({})',
                           reverse('admin:nucleo_user_change', args=[usuario.pk]),
                           usuario.get_full_name() or usuario.email, usuario.email)

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


# Países: catálogo fijo de django-cities-light (fixture `paises`). No se administra desde el SIA; solo se elige en
# los campos de país. Se quitan las pantallas que registra el paquete y Country queda solo para el autocompletado.
for modelo_geo in (Country, Region, SubRegion, City):
    if admin.site.is_registered(modelo_geo):
        admin.site.unregister(modelo_geo)


@admin.register(Country)
class PaisAdmin(ModelAdmin):
    permisos_investigador = ('view',)
    search_fields = ['name', 'name_ascii', 'alternate_names', 'code2', 'code3']
    ordering = ['name']

    def get_model_perms(self, request):
        return {}  # Fuera del menú y del índice del admin.

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SituacionAcademica)
class SituacionAcademicaAdmin(CatalogoAdmin):
    """Nombramiento, PRIDE, SNII y contrato de cada académico por año (corte de agosto). Lo mantiene Administración."""
    permisos_investigador = ()
    list_display = ['usuario', 'anio', 'nombramiento', 'pride', 'sni', 'contrato']
    list_filter = ['anio', 'pride', 'sni', 'contrato']
    search_fields = ['usuario__first_name', 'usuario__last_name', 'usuario__email']
    autocomplete_fields = ['usuario', 'nombramiento']


@admin.register(Institucion)
class InstitucionAdmin(CompartidoAdmin):
    list_display = ['nombre', 'padre', 'pais', 'ciudad', 'clasificacion', 'pertenece_unam']
    list_filter = ['clasificacion', 'pertenece_unam', 'subsistema_unam']
    search_fields = ['nombre', 'padre__nombre', 'ciudad', 'pais__name']
    autocomplete_fields = ['pais', 'padre']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('padre', 'pais')


@admin.register(AreaConocimiento)
class AreaConocimientoAdmin(CatalogoAdmin):
    solo_sysadmin = True
    list_display = ['nombre', 'categoria']
    list_filter = ['categoria']
    search_fields = ['nombre']


@admin.register(ProgramaAcademico)
class ProgramaAcademicoAdmin(CompartidoAdmin):
    list_display = ['nombre', 'nivel', 'area_conocimiento']
    list_filter = ['nivel']
    search_fields = ['nombre']
    autocomplete_fields = ['area_conocimiento']


@admin.register(Asignatura)
class AsignaturaAdmin(CompartidoAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']


@admin.register(Beca)
class BecaAdmin(CompartidoAdmin):
    permisos_investigador = ('view',)  # Lo mantiene Administración; el académico solo elige.
    list_display = ['nombre', 'institucion', 'clase']
    list_filter = ['clase']
    search_fields = ['nombre', 'institucion__nombre']
    autocomplete_fields = ['institucion']


@admin.register(Cargo)
class CargoAdmin(CompartidoAdmin):
    permisos_investigador = ('view',)  # Lo mantiene Administración; el académico solo elige.
    list_display = ['nombre', 'tipo']
    list_filter = ['tipo']
    search_fields = ['nombre']


@admin.register(Nombramiento)
class NombramientoAdmin(CatalogoAdmin):
    solo_sysadmin = True
    list_display = ['nombre', 'clave']
    search_fields = ['nombre', 'clave']


@admin.register(Distincion)
class DistincionAdmin(CompartidoAdmin):
    permisos_investigador = ('view',)  # Lo mantiene Administración; el académico solo elige.
    list_display = ['nombre', 'tipo', 'institucion', 'ambito']
    list_filter = ['tipo', 'ambito']
    search_fields = ['nombre', 'institucion__nombre']
    autocomplete_fields = ['institucion']


@admin.register(TipoEvento)
class TipoEventoAdmin(CatalogoAdmin):
    search_fields = ['nombre']


@admin.register(Evento)
class EventoAdmin(CompartidoAdmin):
    list_display = ['nombre', 'tipo', 'fecha_inicio', 'pais', 'ciudad', 'ambito']
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
class RevistaAdmin(CompartidoAdmin):
    list_display = ['nombre', 'tipo', 'pais', 'issn_impreso', 'issn_electronico']
    list_filter = ['tipo', 'indices']
    search_fields = ['nombre', 'nombre_abreviado', 'issn_impreso', 'issn_electronico']
    autocomplete_fields = ['pais']
    filter_horizontal = ['indices']
    inlines = [MetricaRevistaInline]


@admin.register(MedioDivulgacion)
class MedioDivulgacionAdmin(CompartidoAdmin):
    list_display = ['nombre', 'tipo', 'canal', 'pais']
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
class LibroAdmin(CompartidoAdmin):
    list_display = ['titulo', 'tipo', 'editorial', 'status', 'fecha']
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
        ('Registro', {'fields': ('creado_por', 'creado', 'actualizado'), 'classes': ('collapse',)}),
    )

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
        ('Operación', {'fields': ('pais_sede', 'remitente', 'anios_tablero', 'meses_publicacion_pendiente'),
                       'description': 'Solo el Sysadmin modifica esta sección.'}),
    )

    #: Ajustes técnicos: solo el Sysadmin los cambia; Administración edita identidad, contacto y documentos.
    campos_operacion = ('pais_sede', 'remitente', 'anios_tablero', 'meses_publicacion_pendiente')

    def get_readonly_fields(self, request, obj=None):
        campos = super().get_readonly_fields(request, obj)
        return campos if es_sysadmin(request.user) else (*campos, *self.campos_operacion)

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
