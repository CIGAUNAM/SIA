from django.conf.urls import url
from . views import *

urlpatterns = [
    url(r'^articulos-cientificos/json2/', ArticuloCientificoJSON.as_view(), name='articulo_cientifico_lista__json'),
    url(r'^articulos-cientificos/json2-otros/', ArticuloCientificoJSON.as_view(otros=True), name='articulo_cientifico_lista_otros__json'),
    url(r'^articulos-cientificos/$', ArticuloCientificoLista.as_view(), name='articulo_cientifico_lista'),
    url(r'^articulos-cientificos/(?P<pk>[\w\-]+)/eliminar$', ArticuloCientificoEliminar.as_view(), name='articulo_cientifico_eliminar'),
    url(r'^articulos-cientificos/(?P<pk>[\w\-]+)/$', ArticuloCientificoDetalle.as_view(), name='articulo_cientifico_detalle'),

    url(r'^libros-investigacion/json2/', LibroInvestigacionJSON.as_view(), name='libro_investigacion_lista__json'), url(r'^libros-investigacion/json2-otros/', LibroInvestigacionJSON.as_view(otros=True), name='libro_investigacion_lista_otros__json'),
    url(r'^libros-investigacion/$', LibroInvestigacionLista.as_view(), name='libro_investigacion_lista'),
    url(r'^libros-investigacion/(?P<pk>[\w\-]+)/eliminar$', LibroInvestigacionEliminar.as_view(), name='libro_investigacion_eliminar'),
    url(r'^libros-investigacion/(?P<pk>[\w\-]+)/$', LibroInvestigacionDetalle.as_view(), name='libro_investigacion_detalle'),

    url(r'^capitulos-libros-investigacion/json2/', CapituloLibroInvestigacionJSON.as_view(), name='capitulo_libro_investigacion_lista__json'),
    url(r'^capitulos-libros-investigacion/json2-otros/', CapituloLibroInvestigacionJSON.as_view(otros=True), name='capitulo_libro_investigacion_lista__json'),
    url(r'^capitulos-libros-investigacion/$', CapituloLibroInvestigacionLista.as_view(), name='capitulo_libro_investigacion_lista'),
    url(r'^capitulos-libros-investigacion/(?P<pk>[\w\-]+)/eliminar$', CapituloLibroInvestigacionEliminar.as_view(), name='capitulo_libro_investigacion_eliminar'),
    url(r'^capitulos-libros-investigacion/(?P<pk>[\w\-]+)/$', CapituloLibroInvestigacionDetalle.as_view(), name='capitulo_libro_investigacion_detalle'),

    url(r'^mapas-arbitrados/json2/', MapaArbitradoJSON.as_view(), name='mapa_arbitrado_lista__json'),
    url(r'^mapas-arbitrados/json2-otros/', MapaArbitradoJSON.as_view(otros=True), name='mapa_arbitrado_lista_otros__json'),
    url(r'^mapas-arbitrados/$', MapaArbitradoLista.as_view(), name='mapa_arbitrado_lista'),
    url(r'^mapas-arbitrados/(?P<pk>[\w\-]+)/eliminar$', MapaArbitradoEliminar.as_view(), name='mapa_arbitrado_eliminar'),
    url(r'^mapas-arbitrados/(?P<pk>[\w\-]+)/$', MapaArbitradoDetalle.as_view(), name='mapa_arbitrado_detalle'),

    url(r'^publicaciones-tecnicas/json2/', PublicacionTecnicaJSON.as_view(), name='publicacion_tecnica_lista__json'),
    url(r'^publicaciones-tecnicas/json2-otros/', PublicacionTecnicaJSON.as_view(otros=True), name='publicacion_tecnica_lista_otros__json'),
    url(r'^publicaciones-tecnicas/$', PublicacionTecnicaLista.as_view(), name='publicacion_tecnica_lista'),
    url(r'^publicaciones-tecnicas/(?P<pk>[\w\-]+)/eliminar$', PublicacionTecnicaEliminar.as_view(), name='publicacion_tecnica_eliminar'),
    url(r'^publicaciones-tecnicas/(?P<pk>[\w\-]+)/$', PublicacionTecnicaDetalle.as_view(), name='publicacion_tecnica_detalle'),

    url(r'^proyectos/json2/', ProyectoInvestigacionJSON.as_view(), name='proyecto_investigacion_lista__json'),
    url(r'^proyectos/json2-otros/', ProyectoInvestigacionJSON.as_view(otros=True), name='proyecto_investigacion_lista_otros__json'),
    url(r'^proyectos/$', ProyectoInvestigacionLista.as_view(), name='proyecto_investigacion_lista'),
    url(r'^proyectos/(?P<pk>[\w\-]+)/eliminar$', ProyectoInvestigacionEliminar.as_view(), name='proyecto_investigacion_eliminar'),
    url(r'^proyectos/(?P<pk>[\w\-]+)/$', ProyectoInvestigacionDetalle.as_view(), name='proyecto_investigacion_detalle'),

    url(r'^apoyo-tecnico-investigacion/json2/', ApoyoTecnicoInvestigacionJSON.as_view(), name='apoyo_tecnico_investigacion_lista__json'),
    url(r'^apoyo-tecnico-investigacion/$', ApoyoTecnicoInvestigacionLista.as_view(), name='apoyo_tecnico_investigacion_lista'),
    url(r'^apoyo-tecnico-investigacion/(?P<pk>[\w\-]+)/eliminar$', ApoyoTecnicoInvestigacionEliminar.as_view(), name='apoyo_tecnico_investigacion_eliminar'),
    url(r'^apoyo-tecnico-investigacion/(?P<pk>[\w\-]+)/$', ApoyoTecnicoInvestigacionDetalle.as_view(), name='apoyo_tecnico_investigacion_detalle'),

    url(r'^apoyo-tecnico-servicios/json2/', ApoyoTecnicoServicioJSON.as_view(), name='apoyo_tecnico_servicio_lista__json'),
    url(r'^apoyo-tecnico-servicios/$', ApoyoTecnicoServicioLista.as_view(), name='apoyo_tecnico_servicio_lista'),
    url(r'^apoyo-tecnico-servicios/(?P<pk>[\w\-]+)/eliminar$', ApoyoTecnicoServicioEliminar.as_view(), name='apoyo_tecnico_servicio_eliminar'),
    url(r'^apoyo-tecnico-servicios/(?P<pk>[\w\-]+)/$', ApoyoTecnicoServicioDetalle.as_view(), name='apoyo_tecnico_servicio_detalle'),

]

