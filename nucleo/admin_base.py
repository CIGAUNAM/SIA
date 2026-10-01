"""Clases base del admin del SIA.

Cada `ModelAdmin` declara en `permisos_investigador` qué acciones concede al grupo
"Académicos"; `nucleo.permisos.sincronizar_grupos` lee esos valores (ver ahí los demás grupos).

- `PropietarioAdmin`: registros de producción académica. Un académico solo ve los
  registros en los que participa (según `propietarios`); los administradores ven todo.
  Los registros de un periodo de informe cerrado quedan en solo lectura para los académicos.
- `CompartidoAdmin`: catálogos que cualquier académico puede ampliar; quién los modifica depende de
  cuántas cuentas los usan (ver `nucleo.uso`).
- `CatalogoAdmin`: catálogos que solo mantienen los administradores.

Las tres bases incluyen bitácora de cambios, validación de fechas, aviso de posibles
duplicados y la acción "Fusionar" para administradores.
"""

import copy
from datetime import date

from django import forms
from django.contrib import admin, messages
from django.contrib.admin import helpers
from django.core.exceptions import PermissionDenied
from django.db.models import DateField, Max, Q
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.html import format_html, format_html_join
from django.utils.http import url_has_allowed_host_and_scheme
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import GenericTabularInline, ModelAdmin, TabularInline
from unfold.decorators import action
from unfold.forms import PaginationInlineFormSet

from .fusion import ErrorFusion, fusionar, resumen_referencias
from .informe import anio_cierre
from .models import SIN_FECHA, EstadoPublicacion, Evidencia, PeriodoInforme, Persona, es_sin_fecha
from .permisos import es_sysadmin
from .utils import personas_ordenadas

TODAS_LAS_ACCIONES = ('add', 'change', 'delete', 'view')
#: Apps de trayectoria (no producción regular): se capturan desde "Mi perfil" y no aparecen en el menú de los académicos.
SECCIONES_PERFIL = ('formacion_academica', 'experiencia_profesional')
ANIOS_A_FUTURO = 2


def es_administrador(user):
    return user.is_active and (user.is_superuser or user.has_perm('nucleo.ver_todo'))


def persona_de(user):
    """Persona con la que figura la cuenta en la producción académica."""
    return user.persona


def lista_personas(obj, campo, maximo=3):
    """Resumen de una relación de personas para `list_display` (usa `prefetch_personas` si existe)."""
    personas = personas_ordenadas(obj, campo)
    texto = ', '.join(str(p) for p in personas[:maximo])
    return f'{texto}…' if len(personas) > maximo else texto


def _es_autocomplete(request):
    return getattr(request.resolver_match, 'url_name', None) == 'autocomplete'


def enlace_admin(obj):
    url = reverse(f'admin:{obj._meta.app_label}_{obj._meta.model_name}_change', args=[obj.pk])
    return format_html('<a href="{}" target="_blank">{}</a>', url, obj)


def filtro_anio(*campos):
    """Filtro de lista por año sobre uno o varios campos de fecha (se combinan con OR)."""

    class FiltroAnio(admin.SimpleListFilter):
        title = 'año'
        parameter_name = 'anio'

        def lookups(self, request, model_admin):
            anios = set()
            qs = model_admin.get_queryset(request).order_by()
            for campo in campos:
                anios.update(fecha.year for fecha in qs.dates(campo, 'year'))
            return [(anio, anio) for anio in sorted(anios, reverse=True)]

        def queryset(self, request, queryset):
            if not self.value():
                return queryset
            filtro = Q()
            for campo in campos:
                filtro |= Q(**{f'{campo}__year': self.value()})
            return queryset.filter(filtro)

    return FiltroAnio


# ---------------------------------------------------------------------------
# Comportamiento común
# ---------------------------------------------------------------------------

def adscripcion(persona):
    """'actual', 'ex' o 'externa': si la persona tiene cuenta en la entidad y sigue adscrita.

    Solo se usa para distinguirla (con color) en los selectores de los formularios; `str(persona)` no cambia, así que
    informes, PDF y exportaciones no la muestran.
    """
    usuario = getattr(persona, 'usuario', None)
    if usuario is None:
        return 'externa'
    return 'ex' if usuario.egreso_entidad and usuario.egreso_entidad < date.today() else 'actual'


def _marcar_opciones(widget):
    """Agrega `data-adscripcion` a las opciones de personas ya elegidas (el script `sia/personas.js` las colorea)."""
    original = widget.create_option

    def create_option(name, value, label, selected, index, subindex=None, attrs=None):
        opcion = original(name, value, label, selected, index, subindex, attrs)
        pk = getattr(value, 'value', value)
        if pk not in (None, ''):
            persona = Persona.objects.select_related('usuario').filter(pk=pk).first()
            if persona is not None:
                opcion['attrs']['data-adscripcion'] = adscripcion(persona)
        return opcion

    widget.create_option = create_option


def tiene_ayuda(modelo):
    """Catálogos con texto de ayuda para quien captura (comisiones, cargos, becas, distinciones)."""
    return any(f.name == 'ayuda' for f in modelo._meta.get_fields())


def _marcar_ayuda(widget, modelo):
    """Agrega `data-ayuda` a la opción ya elegida (el script `sia/personas.js` la muestra bajo el campo)."""
    original = widget.create_option

    def create_option(name, value, label, selected, index, subindex=None, attrs=None):
        opcion = original(name, value, label, selected, index, subindex, attrs)
        pk = getattr(value, 'value', value)
        if pk not in (None, ''):
            ayuda = modelo._default_manager.filter(pk=pk).values_list('ayuda', flat=True).first()
            if ayuda:
                opcion['attrs']['data-ayuda'] = ayuda
        return opcion

    widget.create_option = create_option


class EtiquetaPersonaMixin:
    """Los campos que eligen personas distinguen (por color) a quienes están adscritos a la entidad; los que eligen
    un catálogo con ayuda la muestran bajo el campo."""

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        campo = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if campo is not None and db_field.related_model is Persona:
            _marcar_opciones(campo.widget)
        elif campo is not None and tiene_ayuda(db_field.related_model):
            _marcar_ayuda(campo.widget, db_field.related_model)
        return campo

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        campo = super().formfield_for_manytomany(db_field, request, **kwargs)
        if campo is not None and db_field.related_model is Persona:
            _marcar_opciones(campo.widget)
        return campo


class FormularioSIA(forms.ModelForm):
    """Valida el rango de las fechas capturadas, aplica las reglas del admin y avisa de posibles duplicados."""
    confirmar_no_duplicado = forms.BooleanField(
        required=False, widget=forms.HiddenInput, label='Confirmo que no es un duplicado de los registros señalados')
    motivo_cambio = forms.CharField(
        label='Motivo del cambio', required=False, max_length=100,
        help_text='Este registro es de otro académico: el motivo queda en su historial junto con quién y qué cambió.')

    _model_admin = None
    _request = None

    NOTA_SIN_FECHA = ' Si no se conoce, escribe 01/01/1900 (o una fecha anterior): se mostrará como «s.f.» (sin fecha).'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            if isinstance(campo, forms.DateField) and campo.required:
                campo.help_text = (campo.help_text or '') + self.NOTA_SIN_FECHA

    def clean(self):
        datos = super().clean()
        hoy = date.today()
        for nombre, valor in list(datos.items()):
            campo = self.fields.get(nombre)
            if not (isinstance(valor, date) and isinstance(campo, forms.DateField) and nombre in self.changed_data):
                continue
            if es_sin_fecha(valor):
                datos[nombre] = SIN_FECHA  # 1900 o antes: "sin fecha", se guarda siempre igual.
            elif valor.year > hoy.year + ANIOS_A_FUTURO:
                self.add_error(nombre, f'Revisa el año: no puede ser posterior a {hoy.year + ANIOS_A_FUTURO} '
                                       '(si no se conoce, escribe 01/01/1900).')
        return datos

    def _post_clean(self):
        super()._post_clean()
        if self.errors or self._model_admin is None:
            return
        self._model_admin.validar_instancia(self._request, self)
        if self.instance.pk is None and not self.cleaned_data.get('confirmar_no_duplicado'):
            similares = self._model_admin.posibles_duplicados(self._request, self.instance)
            if similares:
                self.fields['confirmar_no_duplicado'].widget = forms.CheckboxInput()
                visibles = set(self._model_admin.get_queryset(self._request).filter(
                    pk__in=[s.pk for s in similares]).values_list('pk', flat=True))
                elementos = [(enlace_admin(s) if s.pk in visibles
                              else format_html('«{}» (registrado por otro académico)', s),) for s in similares]
                self.add_error(None, format_html(
                    'Ya existen registros parecidos: {}. Si es el mismo, no lo dupliques: si lo registró otra persona, '
                    'pídele que te agregue como participante. Si no es el mismo, marca la casilla de confirmación al '
                    'final del formulario y guarda de nuevo.',
                    format_html_join('; ', '{}', elementos)))


class BaseAdmin(EtiquetaPersonaMixin, SimpleHistoryAdmin, ModelAdmin):
    """Bitácora, validación de fechas, aviso de duplicados y fusión (solo administradores)."""
    form = FormularioSIA
    #: Campos (en orden) cuyo texto se compara para avisar de posibles duplicados al crear.
    campos_similitud = ()
    list_per_page = 50
    save_as = True
    save_as_continue = True
    actions = ['fusionar_registros']

    # -- permisos por objeto -------------------------------------------------

    def puede_modificar(self, request, obj):
        """Regla adicional por objeto; las subclases la especializan."""
        return True

    def has_change_permission(self, request, obj=None):
        return super().has_change_permission(request, obj) and (obj is None or self.puede_modificar(request, obj))

    def has_delete_permission(self, request, obj=None):
        return super().has_delete_permission(request, obj) and (obj is None or self.puede_modificar(request, obj))

    def history_form_view(self, request, object_id, version_id, extra_context=None):
        # simple-history carga la versión sin pasar por get_queryset: se verifica que el registro sea visible.
        if not self.get_queryset(request).filter(pk=object_id).exists():
            raise PermissionDenied
        return super().history_form_view(request, object_id, version_id, extra_context)

    # -- formulario ----------------------------------------------------------

    def posibles_duplicados(self, request, instancia):
        """Registros que podrían ser el mismo que `instancia` (solo se revisa al crear)."""
        from .similitud import candidatos

        if not self.campos_similitud:
            return []
        texto = ' '.join(str(getattr(instancia, campo) or '') for campo in self.campos_similitud)
        return candidatos(self.model._default_manager.all(), self.campos_similitud, texto, excluir_pk=instancia.pk)

    def validar_instancia(self, request, form):
        """Validaciones del admin que necesitan la instancia ya construida (año cerrado, etc.)."""

    def get_form(self, request, obj=None, **kwargs):
        form_class = super().get_form(request, obj, **kwargs)
        return type(form_class.__name__, (form_class,), {'_model_admin': self, '_request': request})

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        campos = [c for _, opciones in fieldsets for c in opciones.get('fields', ())]
        if obj is None and 'confirmar_no_duplicado' not in campos:
            fieldsets = [*fieldsets, (None, {'fields': ['confirmar_no_duplicado']})]
        return fieldsets

    # -- duplicados existentes (administradores) -------------------------------

    def has_revisar_duplicados_permission(self, request):
        return es_administrador(request.user)

    @action(description='Revisar duplicados', icon='join', url_path='duplicados', permissions=['revisar_duplicados'])
    def revisar_duplicados(self, request):
        """Pares de registros probablemente duplicados, con opción de fusionar cada par."""
        if request.method == 'POST':
            conservar = get_object_or_404(self.model, pk=request.POST.get('conservar'))
            eliminar = get_object_or_404(self.model, pk=request.POST.get('eliminar'))
            try:
                fusionar(conservar, [eliminar])
                self.message_user(request, f'Se fusionó "{eliminar}" en "{conservar}".')
            except ErrorFusion as error:
                self.message_user(request, str(error), messages.ERROR)
            return redirect(request.get_full_path())
        pares, vistos = [], set()
        for obj in self.model._default_manager.all():
            for similar in self.posibles_duplicados(request, obj):
                llave = tuple(sorted((obj.pk, similar.pk)))
                if llave not in vistos:
                    vistos.add(llave)
                    pares.append([(x, resumen_referencias(x)) for x in (obj, similar)])
            if len(pares) >= 100:
                break
        contexto = {**self.admin_site.each_context(request), 'opts': self.opts, 'pares': pares,
                    'title': f'Posibles duplicados: {self.opts.verbose_name_plural}'}
        return TemplateResponse(request, 'admin/nucleo/duplicados.html', contexto)

    # -- fusión --------------------------------------------------------------

    def get_actions(self, request):
        acciones = super().get_actions(request)
        if not es_administrador(request.user):
            acciones.pop('fusionar_registros', None)
        return acciones

    @admin.action(description='Fusionar registros duplicados')
    def fusionar_registros(self, request, queryset):
        registros = list(queryset)
        if len(registros) < 2:
            self.message_user(request, 'Selecciona al menos dos registros para fusionar.', messages.WARNING)
            return None
        if 'conservar' in request.POST:
            conservar = next((r for r in registros if str(r.pk) == request.POST['conservar']), None)
            if conservar is None:
                self.message_user(request, 'Elige el registro que se conserva.', messages.ERROR)
                return None
            try:
                fusionar(conservar, [r for r in registros if r.pk != conservar.pk])
            except ErrorFusion as error:
                self.message_user(request, str(error), messages.ERROR)
                return None
            self.message_user(request, f'Se fusionaron {len(registros) - 1} registro(s) en "{conservar}".')
            return None
        contexto = {
            **self.admin_site.each_context(request),
            'title': f'Fusionar {self.opts.verbose_name_plural}',
            'opts': self.opts,
            'registros': [(r, resumen_referencias(r)) for r in registros],
            'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
        }
        return TemplateResponse(request, 'admin/nucleo/fusionar.html', contexto)


class EvidenciaInline(GenericTabularInline):
    model = Evidencia
    fields = ['archivo', 'descripcion']
    extra = 0
    tab = True
    verbose_name_plural = 'evidencias (constancias, cartas, PDF)'

    def _permiso_padre(self, request, obj):
        padre = self.admin_site._registry.get(self.parent_model)
        if padre is None:
            return False
        return padre.has_change_permission(request, obj) if obj else padre.has_add_permission(request)

    def has_add_permission(self, request, obj=None):
        return self._permiso_padre(request, obj)

    def has_change_permission(self, request, obj=None):
        return self._permiso_padre(request, obj)

    def has_delete_permission(self, request, obj=None):
        return self._permiso_padre(request, obj)

    def has_view_permission(self, request, obj=None):
        return True  # El registro padre ya solo es visible para quien puede verlo.


# ---------------------------------------------------------------------------
# Inlines de personas ordenadas (autores, responsables, tutores...)
# ---------------------------------------------------------------------------

class ParticipanteForm(forms.ModelForm):
    # Unfold lo llena al arrastrar las filas (0, 1, 2...); vacío en filas nuevas = al final.
    orden = forms.IntegerField(required=False, min_value=0)

    def _post_clean(self):
        super()._post_clean()
        if self.instance.orden is None:
            self.instance.orden = 0


class ParticipanteFormSet(PaginationInlineFormSet):
    def save(self, commit=True):
        guardados = super().save(commit)
        if commit:
            self._renumerar()
        return guardados

    def _renumerar(self):
        """Reasigna `orden` como 1..n respetando el orden indicado; los vacíos van al final."""
        filas = []
        for posicion, form in enumerate(self.forms):
            if form.instance.pk is None or self._should_delete_form(form):
                continue
            orden = getattr(form, 'cleaned_data', {}).get('orden', form.instance.orden)
            filas.append((float('inf') if orden is None else orden, posicion, form.instance))
        for numero, (_, _, instancia) in enumerate(sorted(filas, key=lambda f: f[:2]), start=1):
            if instancia.orden != numero:
                instancia.orden = numero
                instancia.save(update_fields=['orden'])


class ParticipanteInline(EtiquetaPersonaMixin, TabularInline):
    form = ParticipanteForm
    formset = ParticipanteFormSet
    autocomplete_fields = ['persona']
    fields = ['persona', 'orden']
    ordering_field = 'orden'
    hide_ordering_field = True
    extra = 1

    def _permiso_padre(self, request, obj):
        padre = self.admin_site._registry.get(self.parent_model)
        return padre.has_change_permission(request, obj) if obj else padre.has_add_permission(request)

    def has_add_permission(self, request, obj=None):
        return super().has_add_permission(request, obj) and self._permiso_padre(request, obj)

    def has_change_permission(self, request, obj=None):
        return super().has_change_permission(request, obj) and self._permiso_padre(request, obj)

    def has_delete_permission(self, request, obj=None):
        return super().has_delete_permission(request, obj) and self._permiso_padre(request, obj)


# ---------------------------------------------------------------------------
# Registros con dueño
# ---------------------------------------------------------------------------

class PropietarioAdmin(BaseAdmin):
    #: Lookups que, desde el modelo, llegan a la cuenta (`User`) de quien participa en el registro.
    propietarios = ('usuario',)
    #: Relación M2M con `Persona` a la que se agrega el académico si guarda un registro en el que no figura.
    autoria = None
    #: Si otros académicos pueden elegir este registro en campos de autocompletado (p. ej. proyectos).
    compartido = False
    #: Fecha de referencia del registro (filtro por año y cierre de registros de una sola fecha).
    campo_fecha = None
    #: Si los periodos de informe cerrados bloquean el registro (los formatos administrativos no).
    sujeto_a_cierre = True
    permisos_investigador = TODAS_LAS_ACCIONES

    def _tiene_campo_usuario(self):
        return any(f.name == 'usuario' for f in self.model._meta.fields)

    def _campos_fecha_filtro(self):
        if issubclass(self.model, EstadoPublicacion):
            return ('fecha_publicado', 'fecha_enprensa', 'fecha_aceptado', 'fecha_enviado')
        if self.campo_fecha:
            return (self.campo_fecha,)
        if any(isinstance(f, DateField) and f.name == 'fecha_inicio' for f in self.model._meta.fields):
            return ('fecha_inicio',)
        return ()

    def get_queryset(self, request):
        from .acotar import academico_acotado

        qs = super().get_queryset(request)
        academico = academico_acotado(request)  # "Ver por académico" de un administrador.
        if (es_administrador(request.user) and academico is None) or (self.compartido and _es_autocomplete(request)):
            return qs
        dueno = academico or request.user
        filtro = Q()
        for lookup in self.propietarios:
            filtro |= Q(**{lookup: dueno})
        qs = qs.filter(filtro)
        if len(self.propietarios) > 1 or any('__' in lookup for lookup in self.propietarios):
            qs = qs.distinct()
        return qs

    def get_inlines(self, request, obj):
        return [*super().get_inlines(request, obj), EvidenciaInline]

    def get_list_display(self, request):
        list_display = list(super().get_list_display(request))
        if self._tiene_campo_usuario() and es_administrador(request.user) and 'usuario' not in list_display:
            list_display.append('usuario')
        return list_display

    def get_list_filter(self, request):
        list_filter = list(super().get_list_filter(request))
        campos_fecha = self._campos_fecha_filtro()
        if campos_fecha:
            list_filter.insert(0, filtro_anio(*campos_fecha))
        if self._tiene_campo_usuario() and es_administrador(request.user) and 'usuario' not in list_filter:
            list_filter.append(('usuario', admin.RelatedOnlyFieldListFilter))
        return list_filter

    def get_autocomplete_fields(self, request):
        campos = list(super().get_autocomplete_fields(request))
        if self._tiene_campo_usuario() and es_administrador(request.user) and 'usuario' not in campos:
            campos.append('usuario')
        return campos

    def get_changeform_initial_data(self, request):
        inicial = super().get_changeform_initial_data(request)
        if self._tiene_campo_usuario():
            from .acotar import academico_acotado

            inicial.setdefault('usuario', (academico_acotado(request) or request.user).pk)
        return inicial

    def es_propio(self, request, obj):
        """Si el usuario participa en el registro (o sea, si lo vería sin ser administrador)."""
        filtro = Q()
        for lookup in self.propietarios:
            filtro |= Q(**{lookup: request.user})
        return self.model._default_manager.filter(filtro, pk=obj.pk).exists()

    def requiere_motivo(self, request, obj):
        """Administración (no el superusuario) debe justificar cada edición de la producción de otro académico."""
        return (obj is not None and es_administrador(request.user) and not es_sysadmin(request.user)
                and not self.es_propio(request, obj))

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if self.requiere_motivo(request, obj):
            fieldsets = [*fieldsets, ('Trazabilidad', {'fields': ['motivo_cambio']})]
        return fieldsets

    def has_delete_permission(self, request, obj=None):
        # Administración puede corregir la producción ajena, pero no borrarla.
        if obj is not None and not es_sysadmin(request.user) and not self.es_propio(request, obj):
            return False
        return super().has_delete_permission(request, obj)

    def _volver(self, request):
        """Página a la que se regresa al guardar (p. ej. el perfil desde el que se agregó el registro)."""
        destino = request.GET.get('volver', '')
        if destino and url_has_allowed_host_and_scheme(destino, allowed_hosts={request.get_host()}) and not any(
                boton in request.POST for boton in ('_continue', '_addanother', '_saveasnew')):
            return destino
        return None

    def response_add(self, request, obj, post_url_continue=None):
        respuesta = super().response_add(request, obj, post_url_continue)
        destino = self._volver(request)
        return redirect(destino) if destino and respuesta.status_code == 302 else respuesta

    def response_change(self, request, obj):
        respuesta = super().response_change(request, obj)
        destino = self._volver(request)
        return redirect(destino) if destino and respuesta.status_code == 302 else respuesta

    def response_delete(self, request, obj_display, obj_id):
        respuesta = super().response_delete(request, obj_display, obj_id)
        destino = self._volver(request)
        return redirect(destino) if destino and respuesta.status_code == 302 else respuesta

    def save_model(self, request, obj, form, change):
        motivo = form.cleaned_data.get('motivo_cambio')
        if motivo:
            obj._change_reason = motivo  # django-simple-history lo guarda en el historial.
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'motivo_cambio' in form.base_fields:
            # Copia: el campo declarado es el mismo objeto en todas las clases de formulario.
            campo_motivo = copy.deepcopy(form.base_fields['motivo_cambio'])
            campo_motivo.required = self.requiere_motivo(request, obj)
            form.base_fields['motivo_cambio'] = campo_motivo
        campo = form.base_fields.get('usuario')
        if campo is not None and not es_administrador(request.user):
            # El académico no elige el dueño: el campo se envía oculto y se ignora lo que llegue en POST.
            campo.disabled = True
            campo.widget = forms.HiddenInput()
            campo.initial = obj.usuario_id if obj else request.user.pk
        return form

    # -- periodos de informe cerrados --------------------------------------------

    def anio_cierre(self, obj):
        return anio_cierre(obj, self.campo_fecha) if self.sujeto_a_cierre else None

    def puede_modificar(self, request, obj):
        if es_administrador(request.user):
            return True
        anio = self.anio_cierre(obj)
        return anio is None or anio not in PeriodoInforme.anios_cerrados()

    def validar_instancia(self, request, form):
        if es_administrador(request.user):
            return
        anio = self.anio_cierre(form.instance)
        if anio is not None and anio in PeriodoInforme.anios_cerrados():
            form.add_error(None, f'El informe {anio} ya está cerrado: no puedes registrar ni modificar actividades '
                                 f'de ese año. Pide el cambio a un administrador.')

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)
        if obj is not None and not es_administrador(request.user) and not self.puede_modificar(request, obj):
            messages.info(request, f'Este registro pertenece al informe {self.anio_cierre(obj)}, que ya está cerrado; '
                                   'solo puedes consultarlo.')
        return super().change_view(request, object_id, form_url, extra_context)

    # -- autoría ---------------------------------------------------------------

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        for formset in formsets:
            if formset.model is Evidencia:
                for evidencia in formset.new_objects:
                    evidencia.subido_por = request.user
                    evidencia.save(update_fields=['subido_por'])
        from .acotar import academico_acotado

        academico = academico_acotado(request)
        if es_administrador(request.user) and (academico is None or change):
            return
        obj = form.instance
        if self.get_queryset(request).filter(pk=obj.pk).exists():
            return
        dueno = academico or request.user
        if self.autoria:
            relacion = getattr(obj, self.autoria)
            through = relacion.through
            defaults = {}
            if any(f.name == 'orden' for f in through._meta.fields):
                ultimo = through.objects.filter(**{relacion.source_field_name: obj}).aggregate(m=Max('orden'))['m']
                defaults['orden'] = (ultimo or 0) + 1
            relacion.add(persona_de(dueno), through_defaults=defaults)
            lista = obj._meta.get_field(self.autoria).verbose_name
            if dueno == request.user:
                messages.info(request, f'Se te agregó a la lista de {lista} para que el registro aparezca entre los tuyos.')
            else:
                messages.info(request, f'Se agregó a {dueno} a la lista de {lista}: el registro es de su producción.')
        elif dueno == request.user:
            messages.warning(request, 'El registro se guardó, pero no figuras en él, así que no aparecerá en tu lista.')


# ---------------------------------------------------------------------------
# Catálogos
# ---------------------------------------------------------------------------

class CompartidoAdmin(BaseAdmin):
    """Catálogos compartidos que cualquier académico amplía (personas, instituciones, revistas, eventos...).

    Quién puede modificar un registro (`nucleo.uso`):
    - si tiene titulares con cuenta (autores, editores... de un libro; la cuenta de una persona): cualquiera de ellos;
    - si no, según quién lo usa: nadie (huérfano), cualquiera; una sola cuenta (aunque sea en varios registros),
      solo esa; varias cuentas, nadie (queda de solo lectura para los académicos).
    Borrar: solo si ningún otro registro lo usa, y solo sus titulares o, si no tiene, quien lo creó.
    La administración siempre puede, con un aviso de que el cambio se verá en todos los registros que lo usan.
    """
    permisos_investigador = TODAS_LAS_ACCIONES
    campos_similitud = ('nombre',)
    actions = ['fusionar_registros']
    actions_list = ['revisar_duplicados']
    change_form_before_template = 'admin/nucleo/aviso_compartido.html'

    def _uso(self, request, obj):
        """Uso del registro, calculado una vez por solicitud."""
        from .uso import uso

        cache = request.__dict__.setdefault('_uso_compartido', {})
        llave = (type(obj), obj.pk)
        if llave not in cache:
            cache[llave] = uso(obj)
        return cache[llave]

    def puede_modificar(self, request, obj):
        if es_administrador(request.user):
            return True
        registro_uso = self._uso(request, obj)
        if registro_uso.titulares:
            return request.user.pk in registro_uso.titulares
        return not registro_uso.usuarios or registro_uso.usuarios == {request.user.pk}

    def has_delete_permission(self, request, obj=None):
        if obj is not None and not es_administrador(request.user):
            registro_uso = self._uso(request, obj)
            dueno = (request.user.pk in registro_uso.titulares if registro_uso.titulares
                     else obj.creado_por_id == request.user.pk)
            if registro_uso.registros or not dueno:
                return False
        return super().has_delete_permission(request, obj)

    def get_readonly_fields(self, request, obj=None):
        return [*super().get_readonly_fields(request, obj), 'creado_por', 'creado', 'actualizado']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creado_por = request.user
        super().save_model(request, obj, form, change)

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        if obj is not None and obj.pk:
            registro_uso = self._uso(request, obj)
            context['uso_compartido'] = {
                'registros': registro_uso.registros, 'cuentas': len(registro_uso.usuarios),
                'administrador': es_administrador(request.user),
                'propio': registro_uso.usuarios == {request.user.pk},
                'titular': request.user.pk in registro_uso.titulares, 'con_titulares': bool(registro_uso.titulares),
                'editable': self.puede_modificar(request, obj),
            }
        return super().render_change_form(request, context, add, change, form_url, obj)


class CatalogoAdmin(BaseAdmin):
    permisos_investigador = ('view',)
    #: Catálogos normativos (nombramientos, áreas de conocimiento, ODS): solo el Sysadmin los modifica;
    #: Administración y académicos los consultan.
    solo_sysadmin = False
    list_per_page = 100
