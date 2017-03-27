from django.conf.urls import url
from . views import *

urlpatterns = [

    url(r'^articulos-cientificos/json/', ArticuloCientificoJSON.as_view(), name='articulo_cientifico_lista__json'),
    url(r'^articulos-cientificos/json-otros/', ArticuloCientificoJSON.as_view(otros=True), name='articulo_cientifico_lista_otros__json'),
    url(r'^articulos-cientificos/$', ArticuloCientificoLista.as_view(), name='articulo_cientifico_lista'),
    url(r'^articulos-cientificos/(?P<pk>[\w\-]+)/$', ArticuloCientificoDetalle.as_view(), name='articulo_cientifico_detalle'),

    url(r'^capitulos-libros-investigacion/json/', CapituloLibroInvestigacionJSON.as_view(), name='capitulo_libro_investigacion_lista__json'),
    #url(r'^capitulos-libros-investigacion/json-otros/', CapituloLibroInvestigacionJSON.as_view(otros=True), name='capitulo_libro_investigacion_lista_otros__json'),
    url(r'^capitulos-libros-investigacion/$', CapituloLibroInvestigacionLista.as_view(), name='capitulo_libro_investigacion_lista'),
    url(r'^capitulos-libros-investigacion/(?P<pk>[\w\-]+)/$', CapituloLibroInvestigacionDetalle.as_view(), name='capitulo_libro_investigacion_detalle'),

    url(r'^mapas-arbitrados/json/', MapaArbitradoJSON.as_view(), name='mapa_arbitrado_lista__json'),
    url(r'^mapas-arbitrados/json-otros/', MapaArbitradoJSON.as_view(otros=True), name='mapa_arbitrado_lista_otros__json'),
    url(r'^mapas-arbitrados/$', MapaArbitradoLista.as_view(), name='mapa_arbitrado_lista'),
    url(r'^mapas-arbitrados/(?P<pk>[\w\-]+)/$', MapaArbitradoDetalle.as_view(), name='mapa_arbitrado_detalle'),

    url(r'^informes-tecnicos-publicos/json/', InformeTecnicoJSON.as_view(), name='informe_tecnico_publico_lista__json'),
    url(r'^informes-tecnicos-publicos/json-otros/', InformeTecnicoJSON.as_view(otros=True), name='informe_tecnico_publico_lista_otros__json'),
    url(r'^informes-tecnicos-publicos/$', InformeTecnicoLista.as_view(), name='informe_tecnico_publico_lista'),
    url(r'^informes-tecnicos-publicos/(?P<pk>[\w\-]+)/$', InformeTecnicoDetalle.as_view(), name='informe_tecnico_publico_detalle'),

]