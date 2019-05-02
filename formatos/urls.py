from django.conf.urls import url
from . views import *


urlpatterns = [
    url(r'^servicio-transporte/json/', FormatoServicioTransporteJSON.as_view(), name='formato_servicio_transporte_lista__json'),
    url(r'^servicio-transporte/$', FormatoServicioTransporteLista.as_view(), name='formato_servicio_transporte_lista'),
    url(r'^servicio-transporte/(?P<pk>[\w\-]+)/eliminar$', FormatoServicioTransporteEliminar.as_view(), name='formato_servicio_transporte_eliminar'),
    url(r'^servicio-transporte/(?P<pk>[\w\-]+)/$', FormatoServicioTransporteDetalle.as_view(), name='formato_servicio_transporte_detalle'),

    url(r'^licencia-goce-sueldo/json/', FormatoLicenciaGoceSueldoJSON.as_view(), name='formato_licencia_goce_sueldo__json'),
    url(r'^licencia-goce-sueldo/$', FormatoLicenciaGoceSueldoLista.as_view(), name='formato_licencia_goce_sueldo_lista'),
    url(r'^licencia-goce-sueldo/(?P<pk>[\w\-]+)/eliminar$', FormatoLicenciaGoceSueldoEliminar.as_view(), name='formato_licencia_goce_sueldo_eliminar'),
    url(r'^licencia-goce-sueldo/(?P<pk>[\w\-]+)/$', FormatoLicenciaGoceSueldoDetalle.as_view(), name='formato_licencia_goce_sueldo_detalle'),

    url(r'^pago-viaticos/json/', FormatoPagoViaticoJSON.as_view(), name='formato_pago_viatico_lista__json'),
    url(r'^pago-viaticos/$', FormatoPagoViaticoLista.as_view(), name='formato_pago_viatico_lista'),
    url(r'^pago-viaticos/(?P<pk>[\w\-]+)/eliminar$', FormatoPagoViaticoEliminar.as_view(), name='formato_pago_viatico_eliminar'),
    url(r'^pago-viaticos/(?P<pk>[\w\-]+)/$', FormatoPagoViaticoDetalle.as_view(), name='formato_pago_viatico_detalle'),
    url(r'^pago-viaticos/(?P<pk>[\w\-]+)/pdf$', FormatoPagoViaticoPDF.as_view(), name='formato_pago_viatico_pdf'),



]