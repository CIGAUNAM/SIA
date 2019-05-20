from django.conf.urls import url
from . views import *

urlpatterns = [

    url(r'^memorias-in-extenso/json/', MemoriaInExtensoJSON.as_view(), name='memoria_in_extenso_lista__json'),
    url(r'^memorias-in-extenso/json-otros/', MemoriaInExtensoJSON.as_view(otros=True), name='memoria_in_extenso_lista_otros__json'),
    url(r'^memorias-in-extenso/$', MemoriaInExtensoLista.as_view(), name='memoria_in_extenso_lista'),
    url(r'^memorias-in-extenso/(?P<pk>[\w\-]+)/eliminar$', MemoriaInExtensoEliminar.as_view(), name='memoria_in_extenso_eliminar'),
    url(r'^memorias-in-extenso/(?P<pk>[\w\-]+)/$', MemoriaInExtensoDetalle.as_view(), name='memoria_in_extenso_detalle'),

    url(r'^organizacion-eventos-academicos/json/', OrganizacionEventoAcademicoJSON.as_view(), name='organizacion_evento_academico_lista__json'),
    #url(r'^organizacion-eventos-academicos/json-otros/', OrganizacionEventoAcademicoJSON.as_view(otros=True), name='organizacion_evento_academico_lista_otros__json'),
    url(r'^organizacion-eventos-academicos/$', OrganizacionEventoAcademicoLista.as_view(), name='organizacion_evento_academico_lista'),
    url(r'^organizacion-eventos-academicos/(?P<pk>[\w\-]+)/eliminar$', OrganizacionEventoAcademicoEliminar.as_view(), name='organizacion_evento_academico_eliminar'),
    url(r'^organizacion-eventos-academicos/(?P<pk>[\w\-]+)/$', OrganizacionEventoAcademicoDetalle.as_view(), name='organizacion_evento_academico_detalle'),

    url(r'^participacion-eventos-academicos/json/', ParticipacionEventoAcademicoJSON.as_view(), name='participacion_evento_academico_lista__json'),
    url(r'^participacion-eventos-academicos/json-otros/', ParticipacionEventoAcademicoJSON.as_view(otros=True), name='participacion_evento_academico_lista_otros__json'),
    url(r'^participacion-eventos-academicos/$', ParticipacionEventoAcademicoLista.as_view(), name='participacion_evento_academico_lista'),
    url(r'^participacion-eventos-academicos/(?P<pk>[\w\-]+)/eliminar$', ParticipacionEventoAcademicoEliminar.as_view(), name='participacion_evento_academico_eliminar'),
    url(r'^participacion-eventos-academicos/(?P<pk>[\w\-]+)/$', ParticipacionEventoAcademicoDetalle.as_view(), name='participacion_evento_academico_detalle'),

    url(r'^rest/eventos-difusion/$', RESTEventoDifusionLista.as_view()),
    url(r'^rest/eventos-difusion/(?P<pk>[0-9]+)/$', RESTEventoDifusionDetalle.as_view()),

    url(r'^eventos-difusion/agregar/$', EventoDifusionAgregar.as_view(), name='eventodifusion_agregar'),
    url(r'^eventos-difusion/(?P<pk>[\w\-]+)/$', EventoDifusionDetalle.as_view(), name='eventodifusion_detalle'),
]