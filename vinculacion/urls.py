from django.conf.urls import url
from . views import *


urlpatterns = [
    url(r'^arbitrajes-publicaciones/json/', ArbitrajePublicacionAcademicaJSON.as_view(), name='arbitraje_publicacion_academica_lista__json'),
    url(r'^arbitrajes-publicaciones/$', ArbitrajePublicacionAcademicaLista.as_view(), name='arbitraje_publicacion_academica_lista'),
    url(r'^arbitrajes-publicaciones/(?P<pk>[\w\-]+)/eliminar$', ArbitrajePublicacionAcademicaEliminar.as_view(), name='arbitraje_publicacion_academica_eliminar'),
    url(r'^arbitrajes-publicaciones/(?P<pk>[\w\-]+)/$', ArbitrajePublicacionAcademicaDetalle.as_view(), name='arbitraje_publicacion_academica_detalle'),

    url(r'^otras-comisiones/json/', OtraComisionJSON.as_view(), name='otra_comision_lista__json'),
    url(r'^otras-comisiones/$', OtraComisionLista.as_view(), name='otra_comision_lista'),
    url(r'^otras-comisiones/(?P<pk>[\w\-]+)/eliminar$', OtraComisionEliminar.as_view(), name='otra_comision_eliminar'),
    url(r'^otras-comisiones/(?P<pk>[\w\-]+)/$', OtraComisionDetalle.as_view(), name='otra_comision_detalle'),

    url(r'^redes-academicas/json/', RedAcademicaJSON.as_view(), name='red_academica_lista__json'),
    url(r'^redes-academicas/json-otros/', RedAcademicaJSON.as_view(otros=True), name='red_academica_lista_otros__json'),
    url(r'^redes-academicas/$', RedAcademicaLista.as_view(), name='red_academica_lista'),
    url(r'^redes-academicas/(?P<pk>[\w\-]+)/eliminar$', RedAcademicaEliminar.as_view(), name='red_academica_eliminar'),
    url(r'^redes-academicas/(?P<pk>[\w\-]+)/$', RedAcademicaDetalle.as_view(), name='red_academica_detalle'),

    url(r'^convenios-entidades-externas/json/', ConvenioEntidadExternaJSON.as_view(), name='convenio_entidad_externa_lista__json'),
    url(r'^convenios-entidades-externas/json-otros/', ConvenioEntidadExternaJSON.as_view(otros=True), name='convenio_entidad_externa_lista_otros__json'),
    url(r'^convenios-entidades-externas/$', ConvenioEntidadExternaLista.as_view(), name='convenio_entidad_externa_lista'),
    url(r'^convenios-entidades-externas/(?P<pk>[\w\-]+)/eliminar$', ConvenioEntidadExternaEliminar.as_view(), name='convenio_entidad_externa_eliminar'),
    url(r'^convenios-entidades-externas/(?P<pk>[\w\-]+)/$', ConvenioEntidadExternaDetalle.as_view(), name='convenio_entidad_externa_detalle'),

    url(r'^servicios-asesorias-externas/json/', ServicioAsesoriaExternaJSON.as_view(), name='servicio_asesoria_exterma_lista__json'),
    url(r'^servicios-asesorias-externas/$', ServicioAsesoriaExternaLista.as_view(), name='servicio_asesoria_exterma_lista'),
    url(r'^servicios-asesorias-externas/(?P<pk>[\w\-]+)/eliminar$', ServicioAsesoriaExternaEliminar.as_view(), name='servicio_asesoria_exterma_eliminar'),
    url(r'^servicios-asesorias-externas/(?P<pk>[\w\-]+)/$', ServicioAsesoriaExternaDetalle.as_view(), name='servicio_asesoria_exterma_detalle'),

    url(r'^otros-programas-vinculacion/json/', OtroProgramaVinculacionJSON.as_view(), name='otro_programa_vinculacion_lista__json'),
    url(r'^otros-programas-vinculacion/$', OtroProgramaVinculacionLista.as_view(), name='otro_programa_vinculacion_lista'),
    url(r'^otros-programas-vinculacion/(?P<pk>[\w\-]+)/eliminar$', OtroProgramaVinculacionEliminar.as_view(), name='otro_programa_vinculacion_eliminar'),
    url(r'^otros-programas-vinculacion/(?P<pk>[\w\-]+)/$', OtroProgramaVinculacionDetalle.as_view(), name='otro_programa_vinculacion_detalle'),

    url(r'^clasificaciones-servicios/json/', ClasificacionServicioJSON.as_view(), name='clasificacion_servicio_lista__json'),
    url(r'^clasificaciones-servicios/$', ClasificacionServicioLista.as_view(), name='clasificacion_servicio_lista'),
    # url(r'^clasificaciones-servicios/(?P<pk>[\w\-]+)/eliminar$', ClasificacionServicioEliminar.as_view(), name='clasificacion_servicio_eliminar'),
    url(r'^clasificaciones-servicios/(?P<pk>[\w\-]+)/$', ClasificacionServicioDetalle.as_view(), name='clasificacion_servicio_detalle'),

]