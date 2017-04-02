from django.conf.urls import url
from . views import *

urlpatterns = [

    url(r'^memorias-in-extenso/json/', MemoriaInExtensoJSON.as_view(), name='memoria_in_extenso_lista__json'),
    url(r'^memorias-in-extenso/json-otros/', MemoriaInExtensoJSON.as_view(otros=True), name='memoria_in_extenso_lista_otros__json'),
    url(r'^memorias-in-extenso/$', MemoriaInExtensoLista.as_view(), name='memoria_in_extenso_lista'),
    url(r'^memorias-in-extenso/(?P<pk>[\w\-]+)/$', MemoriaInExtensoDetalle.as_view(), name='memoria_in_extenso_detalle'),

    url(r'^prologos-libros/json/', PrologoLibroJSON.as_view(), name='prologo_libro_lista__json'),
    #url(r'^prologos-libros/json-otros/', PrologoLibroJSON.as_view(otros=True), name='prologo_libro_lista_otros__json'),
    url(r'^prologos-libros/$', PrologoLibroLista.as_view(), name='prologo_libro_lista'),
    url(r'^prologos-libros/(?P<pk>[\w\-]+)/$', PrologoLibroDetalle.as_view(), name='prologo_libro_detalle'),



]