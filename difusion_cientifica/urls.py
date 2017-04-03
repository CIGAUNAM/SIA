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

    url(r'^resenas/json/', ResenaJSON.as_view(), name='resena_lista__json'),
    url(r'^resenas/$', ResenaLista.as_view(), name='resena_lista'),
    url(r'^resenas/(?P<pk>[\w\-]+)/$', ResenaDetalle.as_view(), name='resena_detalle'),

    url(r'^organizacion-eventos-academicos/json/', OrganizacionEventoAcademicoJSON.as_view(), name='organizacion_evento_academico_lista__json'),
    url(r'^organizacion-eventos-academicos/$', OrganizacionEventoAcademicoLista.as_view(), name='organizacion_evento_academico_lista'),
    url(r'^organizacion-eventos-academicos/(?P<pk>[\w\-]+)/$', OrganizacionEventoAcademicoDetalle.as_view(), name='organizacion_evento_academico_detalle'),

    url(r'^participacion-eventos-academicos/json/', ParticipacionEventoAcademicoJSON.as_view(), name='participacion_evento_academico_lista__json'),
    url(r'^participacion-eventos-academicos/$', ParticipacionEventoAcademicoLista.as_view(), name='participacion_evento_academico_lista'),
    url(r'^participacion-eventos-academicos/(?P<pk>[\w\-]+)/$', ParticipacionEventoAcademicoDetalle.as_view(), name='participacion_evento_academico_detalle'),

]