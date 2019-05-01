from django.conf.urls import url
from . views import *


urlpatterns = [
    url(r'^arbitrajes-publicaciones/json2/', ArbitrajePublicacionAcademicaJSON.as_view(), name='arbitraje_publicacion_academica_lista__json'),
    url(r'^arbitrajes-publicaciones/$', ArbitrajePublicacionAcademicaLista.as_view(), name='arbitraje_publicacion_academica_lista'),
    url(r'^arbitrajes-publicaciones/(?P<pk>[\w\-]+)/eliminar$', ArbitrajePublicacionAcademicaEliminar.as_view(), name='arbitraje_publicacion_academica_eliminar'),
    url(r'^arbitrajes-publicaciones/(?P<pk>[\w\-]+)/$', ArbitrajePublicacionAcademicaDetalle.as_view(), name='arbitraje_publicacion_academica_detalle'),

    url(r'^otras-comisiones/json2/', OtraComisionJSON.as_view(), name='otra_comision_lista__json'),
    url(r'^otras-comisiones/$', OtraComisionLista.as_view(), name='otra_comision_lista'),
    url(r'^otras-comisiones/(?P<pk>[\w\-]+)/eliminar$', OtraComisionEliminar.as_view(), name='otra_comision_eliminar'),
    url(r'^otras-comisiones/(?P<pk>[\w\-]+)/$', OtraComisionDetalle.as_view(), name='otra_comision_detalle'),

    url(r'^redes-academicas/json2/', RedAcademicaJSON.as_view(), name='red_academica_lista__json'),
    url(r'^redes-academicas/json2-otros/', RedAcademicaJSON.as_view(otros=True), name='red_academica_lista_otros__json'),
    url(r'^redes-academicas/$', RedAcademicaLista.as_view(), name='red_academica_lista'),
    url(r'^redes-academicas/(?P<pk>[\w\-]+)/eliminar$', RedAcademicaEliminar.as_view(), name='red_academica_eliminar'),
    url(r'^redes-academicas/(?P<pk>[\w\-]+)/$', RedAcademicaDetalle.as_view(), name='red_academica_detalle'),

    url(r'^convenios-otras-entidades/json2/', ConvenioOtraEntidadJSON.as_view(), name='convenio_otra_entidad_lista__json'),
    url(r'^convenios-otras-entidades/json2-otros/', ConvenioOtraEntidadJSON.as_view(otros=True), name='convenio_otra_entidad_lista_otros__json'),
    url(r'^convenios-otras-entidades/$', ConvenioOtraEntidadLista.as_view(), name='convenio_otra_entidad_lista'),
    url(r'^convenios-otras-entidades/(?P<pk>[\w\-]+)/eliminar$', ConvenioOtraEntidadEliminar.as_view(), name='convenio_otra_entidad_eliminar'),
    url(r'^convenios-otras-entidades/(?P<pk>[\w\-]+)/$', ConvenioOtraEntidadDetalle.as_view(), name='convenio_otra_entidad_detalle'),

    url(r'^servicios-asesorias-externas/json2/', ServicioAsesoriaExternaJSON.as_view(), name='servicio_asesoria_exterma_lista__json'),
    url(r'^servicios-asesorias-externas/$', ServicioAsesoriaExternaLista.as_view(), name='servicio_asesoria_exterma_lista'),
    url(r'^servicios-asesorias-externas/(?P<pk>[\w\-]+)/eliminar$', ServicioAsesoriaExternaEliminar.as_view(), name='servicio_asesoria_exterma_eliminar'),
    url(r'^servicios-asesorias-externas/(?P<pk>[\w\-]+)/$', ServicioAsesoriaExternaDetalle.as_view(), name='servicio_asesoria_exterma_detalle'),

]