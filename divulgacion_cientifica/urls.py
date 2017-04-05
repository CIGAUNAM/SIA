from django.conf.urls import url
from . views import *

urlpatterns = [

    url(r'^articulos-divulgacion/json/', ArticuloDivulgacionJSON.as_view(), name='articulo_divulgacion_lista__json'),
    url(r'^articulos-divulgacion/json-otros/', ArticuloDivulgacionJSON.as_view(otros=True), name='articulo_divulgacion_lista_otros__json'),
    url(r'^articulos-divulgacion/$', ArticuloDivulgacionLista.as_view(), name='articulo_divulgacion_lista'),
    url(r'^articulos-divulgacion/(?P<pk>[\w\-]+)/$', ArticuloDivulgacionDetalle.as_view(), name='articulo_divulgacion_detalle'),

    url(r'^capitulos-libros-divulgacion/json/', CapituloLibroDivulgacionJSON.as_view(), name='capitulo_libro_divulgacion_lista__json'),
    url(r'^capitulos-libros-divulgacion/$', CapituloLibroDivulgacionLista.as_view(), name='capitulo_libro_divulgacion_lista'),
    url(r'^capitulos-libros-divulgacion/(?P<pk>[\w\-]+)/$', CapituloLibroDivulgacionDetalle.as_view(), name='capitulo_libro_divulgacion_detalle'),

    url(r'^organizacion-eventos-divulgacion/json/', OrganizacionEventoDivulgacionJSON.as_view(), name='organizacion_evento_divulgacion_lista__json'),
    url(r'^organizacion-eventos-divulgacion/$', OrganizacionEventoDivulgacionLista.as_view(), name='organizacion_evento_divulgacion_lista'),
    url(r'^organizacion-eventos-divulgacion/(?P<pk>[\w\-]+)/$', OrganizacionEventoDivulgacionDetalle.as_view(), name='organizacion_evento_divulgacion_detalle'),

    url(r'^participacion-eventos-divulgacion/json/', ParticipacionEventoDivulgacionJSON.as_view(), name='participacion_evento_divulgacion_lista__json'),
    url(r'^participacion-eventos-divulgacion/json-otros/', ParticipacionEventoDivulgacionJSON.as_view(), name='participacion_evento_divulgacion_lista__json'),
    url(r'^participacion-eventos-divulgacion/$', ParticipacionEventoDivulgacionLista.as_view(), name='participacion_evento_divulgacion_lista'),
    url(r'^participacion-eventos-divulgacion/(?P<pk>[\w\-]+)/$', ParticipacionEventoDivulgacionDetalle.as_view(), name='participacion_evento_divulgacion_detalle'),

    url(r'^medios-divulgacion/json/', ProgramaRadioTelevisionInternetJSON.as_view(), name='programa_radio_television_internet_lista__json'),
    url(r'^medios-divulgacion/$', ProgramaRadioTelevisionInternetLista.as_view(), name='programa_radio_television_internet_lista'),
    url(r'^medios-divulgacion/(?P<pk>[\w\-]+)/$', ProgramaRadioTelevisionInternetDivulgacionDetalle.as_view(), name='programa_radio_television_internet_detalle'),

    url(r'^libros-divulgacion/json/', LibroDivulgacionJSON.as_view(), name='libro_investigacion_lista__json'),
    url(r'^libros-divulgacion/json-otros/', LibroDivulgacionJSON.as_view(otros=True), name='libro_investigacion_lista_otros__json'),
    url(r'^libros-divulgacion/$', LibroDivulgacionLista.as_view(), name='libro_investigacion_lista'),
    url(r'^libros-divulgacion/(?P<pk>[\w\-]+)/$', LibroDivulgacionDetalle.as_view(), name='libro_investigacion_detalle'),

]