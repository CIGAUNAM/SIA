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

]