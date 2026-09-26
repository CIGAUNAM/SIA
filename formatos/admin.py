from django.contrib import admin, messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse
from unfold.decorators import action

from nucleo.admin_base import PropietarioAdmin
from nucleo.documentos import ErrorDocumento, respuesta_documento
from nucleo.models import ConfiguracionEntidad

from .models import LicenciaGoceSueldo, PagoViaticos, ServicioTransporte


class FormatoAdmin(PropietarioAdmin):
    """Formato con botón para descargar la solicitud en PDF (en el detalle y en cada fila)."""
    readonly_fields = ['fecha']
    sujeto_a_cierre = False
    actions_detail = ['descargar_pdf']
    actions_row = ['descargar_pdf']

    @action(description='Descargar PDF', icon='picture_as_pdf', url_path='pdf')
    def descargar_pdf(self, request, object_id):
        obj = self.get_object(request, object_id)
        if obj is None or not self.has_view_permission(request, obj):
            raise PermissionDenied
        contexto = {'formato': obj, 'entidad': ConfiguracionEntidad.actual(request)}
        try:
            return respuesta_documento(request, obj.plantilla_pdf, contexto, f'{self.opts.model_name}-{obj.pk}',
                                       request.GET.get('formato', 'pdf'))
        except ErrorDocumento as error:
            messages.error(request, str(error))
            return redirect(reverse(f'admin:{self.opts.app_label}_{self.opts.model_name}_change', args=[obj.pk]))


@admin.register(ServicioTransporte)
class ServicioTransporteAdmin(FormatoAdmin):
    list_display = ['pk', 'fecha', 'uso', 'tipo', 'fecha_inicio', 'fecha_fin']
    list_filter = ['uso', 'tipo']


@admin.register(LicenciaGoceSueldo)
class LicenciaGoceSueldoAdmin(FormatoAdmin):
    list_display = ['pk', 'fecha', 'evento', 'fecha_inicio', 'fecha_fin']
    autocomplete_fields = ['evento', 'proyecto']
    search_fields = ['evento__nombre']


@admin.register(PagoViaticos)
class PagoViaticosAdmin(FormatoAdmin):
    list_display = ['pk', 'fecha', 'evento', 'fecha_salida', 'importe']
    autocomplete_fields = ['evento', 'proyecto']
    search_fields = ['evento__nombre', 'beneficiario']
