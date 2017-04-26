from django.conf.urls import url
from . views import *


urlpatterns = [
    url(r'^arbitrajes-publicaciones/json/', ArbitrajePublicacionAcademicaJSON.as_view(), name='arbitraje_publicacion_academica_lista__json'),
    url(r'^arbitrajes-publicaciones/$', ArbitrajePublicacionAcademicaLista.as_view(), name='arbitraje_publicacion_academica_lista'),
    url(r'^arbitrajes-publicaciones/(?P<pk>[\w\-]+)/eliminar$', ArbitrajePublicacionAcademicaDetalle.as_view(), name='arbitraje_publicacion_academica_eliminar'),
    url(r'^arbitrajes-publicaciones/(?P<pk>[\w\-]+)/$', ArbitrajePublicacionAcademicaDetalle.as_view(), name='arbitraje_publicacion_academica_detalle'),

    url(r'^arbitrajes-proyectos/json/', ArbitrajeProyectoInvestigacionJSON.as_view(), name='arbitraje_proyecto_investigacion_lista__json'),
    url(r'^arbitrajes-proyectos/$', ArbitrajeProyectoInvestigacionLista.as_view(), name='arbitraje_proyecto_investigacion_lista'),
    url(r'^arbitrajes-proyectos/(?P<pk>[\w\-]+)/eliminar$', ArbitrajeProyectoInvestigacionEliminar.as_view(), name='arbitraje_proyecto_investigacion_eliminar'),
    url(r'^arbitrajes-proyectos/(?P<pk>[\w\-]+)/$', ArbitrajeProyectoInvestigacionDetalle.as_view(), name='arbitraje_proyecto_investigacion_detalle'),

    url(r'^otros-arbitrajes/json/', ArbitrajeOtraActividadJSON.as_view(), name='arbitraje_otra_actividad_lista__json'),
    url(r'^otros-arbitrajes/$', ArbitrajeOtraActividadLista.as_view(), name='arbitraje_otra_actividad_lista'),
    url(r'^otros-arbitrajes/(?P<pk>[\w\-]+)/eliminar$', ArbitrajeOtraActividadEliminar.as_view(), name='arbitraje_otra_actividad_eliminar'),
    url(r'^otros-arbitrajes/(?P<pk>[\w\-]+)/$', ArbitrajeOtraActividadDetalle.as_view(), name='arbitraje_otra_actividad_detalle'),

    url(r'^redes-academicas/json/', RedAcademicaJSON.as_view(), name='red_academica_lista__json'),
    url(r'^redes-academicas/json-otros/', RedAcademicaJSON.as_view(otros=True), name='red_academica_lista_otros__json'),
    url(r'^redes-academicas/$', RedAcademicaLista.as_view(), name='red_academica_lista'),
    url(r'^redes-academicas/(?P<pk>[\w\-]+)/eliminar$', RedAcademicaEliminar.as_view(), name='red_academica_eliminar'),
    url(r'^redes-academicas/(?P<pk>[\w\-]+)/$', RedAcademicaDetalle.as_view(), name='red_academica_detalle'),

    url(r'^convenios-entidades-no-academicas/json/', ConvenioEntidadNoAcademicaJSON.as_view(), name='convenio_entidad_no_academica_lista__json'),
    url(r'^convenios-entidades-no-academicas/json-otros/', ConvenioEntidadNoAcademicaJSON.as_view(otros=True), name='convenio_entidad_no_academica_lista_otros__json'),
    url(r'^convenios-entidades-no-academicas/$', ConvenioEntidadNoAcademicaLista.as_view(), name='convenio_entidad_no_academica_lista'),
    url(r'^convenios-entidades-no-academicas/(?P<pk>[\w\-]+)/eliminar$', ConvenioEntidadNoAcademicaEliminar.as_view(), name='convenio_entidad_no_academica_eliminar'),
    url(r'^convenios-entidades-no-academicas/(?P<pk>[\w\-]+)/$', ConvenioEntidadNoAcademicaDetalle.as_view(), name='convenio_entidad_no_academica_detalle'),

    url(r'^servicios-externos-no-academicos/json/', ServicioExternoEntidadNoAcademicaJSON.as_view(), name='servicio_externo_entidad_no_academica_lista__json'),
    url(r'^servicios-externos-no-academicos/$', ServicioExternoEntidadNoAcademicaLista.as_view(), name='servicio_externo_entidad_no_academica_lista'),
    url(r'^servicios-externos-no-academicos/(?P<pk>[\w\-]+)/eliminar$', ServicioExternoEntidadNoAcademicaEliminar.as_view(), name='servicio_externo_entidad_no_academica_eliminar'),
    url(r'^servicios-externos-no-academicos/(?P<pk>[\w\-]+)/$', ServicioExternoEntidadNoAcademicaDetalle.as_view(), name='servicio_externo_entidad_no_academica_detalle'),

    url(r'^otros-programas-vinculacion/json/', OtroProgramaVinculacionJSON.as_view(), name='otro_programa_vinculacion_lista__json'),
    url(r'^otros-programas-vinculacion/$', OtroProgramaVinculacionLista.as_view(), name='otro_programa_vinculacion_lista'),
    url(r'^otros-programas-vinculacion/(?P<pk>[\w\-]+)/eliminar$', OtroProgramaVinculacionEliminar.as_view(), name='otro_programa_vinculacion_eliminar'),
    url(r'^otros-programas-vinculacion/(?P<pk>[\w\-]+)/$', OtroProgramaVinculacionDetalle.as_view(), name='otro_programa_vinculacion_detalle'),

]