from django.conf.urls import url
from . views import *


urlpatterns = [
    url(r'^arbitrajes-publicaciones/json/', ArbitrajePublicacionAcademicaJSON.as_view(), name='arbitraje_publicacion_academica_lista__json'),
    url(r'^arbitrajes-publicaciones/$', ArbitrajePublicacionAcademicaLista.as_view(), name='arbitraje_publicacion_academica_lista'),
    url(r'^arbitrajes-publicaciones/(?P<pk>[\w\-]+)/$', ArbitrajePublicacionAcademicaDetalle.as_view(), name='arbitraje_publicacion_academica_detalle'),

    url(r'^arbitrajes-proyectos/json/', ArbitrajeProyectoInvestigacionJSON.as_view(), name='arbitraje_proyecto_investigacion_lista__json'),
    url(r'^arbitrajes-proyectos/$', ArbitrajeProyectoInvestigacionLista.as_view(), name='arbitraje_proyecto_investigacion_lista'),
    url(r'^arbitrajes-proyectos/(?P<pk>[\w\-]+)/$', ArbitrajeProyectoInvestigacionDetalle.as_view(), name='arbitraje_proyecto_investigacion_detalle'),

    url(r'^otros-arbitrajes/json/', ArbitrajeOtraActividadJSON.as_view(), name='arbitraje_otra_actividad_lista__json'),
    url(r'^otros-arbitrajes/$', ArbitrajeOtraActividadLista.as_view(), name='arbitraje_otra_actividad_lista'),
    url(r'^otros-arbitrajes/(?P<pk>[\w\-]+)/$', ArbitrajeOtraActividadDetalle.as_view(), name='arbitraje_otra_actividad_detalle'),

    url(r'^redes-academicas/json/', RedAcademicaJSON.as_view(), name='red_academica_lista__json'),
    url(r'^redes-academicas/json-otros/', RedAcademicaJSON.as_view(otros=True), name='red_academica_lista_otros__json'),
    url(r'^redes-academicas/$', RedAcademicaLista.as_view(), name='red_academica_lista'),
    url(r'^redes-academicas/(?P<pk>[\w\-]+)/$', RedAcademicaDetalle.as_view(), name='red_academica_detalle'),

    url(r'^convenios-entidades-no-academicas/json/', ConvenioEntidadNoAcademicaJSON.as_view(), name='convenio_entidad_no_academica_lista__json'),
    url(r'^convenios-entidades-no-academicas/json-otros/', ConvenioEntidadNoAcademicaJSON.as_view(otros=True), name='convenio_entidad_no_academica_lista_otros__json'),
    url(r'^convenios-entidades-no-academicas/$', ConvenioEntidadNoAcademicaLista.as_view(), name='convenio_entidad_no_academica_lista'),
    url(r'^convenios-entidades-no-academicas/(?P<pk>[\w\-]+)/$', ConvenioEntidadNoAcademicaDetalle.as_view(), name='convenio_entidad_no_academica_detalle'),

    url(r'^servicios-externos-no-academicos/json/', ServicioExternoEntidadNoAcademicaJSON.as_view(), name='servicio_externo_entidad_no_academica_lista__json'),
    url(r'^servicios-externos-no-academicos/$', ServicioExternoEntidadNoAcademicaLista.as_view(), name='servicio_externo_entidad_no_academica_lista'),
    url(r'^servicios-externos-no-academicos/(?P<pk>[\w\-]+)/$', ServicioExternoEntidadNoAcademicaDetalle.as_view(), name='servicio_externo_entidad_no_academica_detalle'),

    url(r'^otros-programas-vinculacion/json/', OtroProgramaVinculacionJSON.as_view(), name='otro_programa_vinculacion_lista__json'),
    url(r'^otros-programas-vinculacion/$', OtroProgramaVinculacionLista.as_view(), name='otro_programa_vinculacion_lista'),
    url(r'^otros-programas-vinculacion/(?P<pk>[\w\-]+)/$', OtroProgramaVinculacionDetalle.as_view(), name='otro_programa_vinculacion_detalle'),

]
"""
    url(r'^articulos-divulgacion/json/', ArticuloDivulgacionJSON.as_view(), name='articulo_divulgacion_lista__json'),
    url(r'^articulos-divulgacion/json-otros/', ArticuloDivulgacionJSON.as_view(otros=True), name='articulo_divulgacion_lista_otros__json'),
    url(r'^articulos-divulgacion/$', ArticuloDivulgacionLista.as_view(), name='articulo_divulgacion_lista'),
    url(r'^articulos-divulgacion/(?P<pk>[\w\-]+)/$', ArticuloDivulgacionDetalle.as_view(), name='articulo_divulgacion_detalle'),

    url(r'^capitulos-libros-divulgacion/json/', CapituloLibroDivulgacionJSON.as_view(), name='capitulo_libro_divulgacion_lista__json'),
    url(r'^capitulos-libros-divulgacion/$', CapituloLibroDivulgacionLista.as_view(), name='capitulo_libro_divulgacion_lista'),
    url(r'^capitulos-libros-divulgacion/(?P<pk>[\w\-]+)/$', CapituloLibroDivulgacionDetalle.as_view(), name='capitulo_libro_divulgacion_detalle'),
"""