from django.conf.urls import url

from . views import *

urlpatterns = [
    url(r'^mov-invitados/json/', MovilidadJSON.as_view(tipo='INVITACION'), name='invitado1_lista__json'),
    url(r'^mov-invitados/$', MovilidadLista.as_view(tipo='INVITACION', obj='invitado', objs='invitados', Objs='Invitados', url_seccion='invitados'), name='invitado1_lista'),
    url(r'^mov-invitados/(?P<pk>[\w\-]+)/eliminar$', MovilidadAcademicaEliminar.as_view()),
    url(r'^mov-invitados/(?P<pk>[\w\-]+)/$', MovilidadDetalle.as_view(tipo='INVITACION', url_seccion='invitados'), name='invitado1_detalle'),

    url(r'^mov-estancias/json/', MovilidadJSON.as_view(tipo='ESTANCIA'), name='estancia_lista1__json'),
    url(r'^mov-estancias/$', MovilidadLista.as_view(tipo='ESTANCIA', obj='estancia de colaboración', objs='estancias de colaboración', Objs='Estancias de colaboración', url_seccion='estancias'), name='estancia1_lista'),
    url(r'^mov-estancias/(?P<pk>[\w\-]+)/eliminar$', MovilidadAcademicaEliminar.as_view()),
    url(r'^mov-estancias/(?P<pk>[\w\-]+)/$', MovilidadDetalle.as_view(tipo='ESTANCIA'), name='estancia1_detalle'),

    url(r'^mov-sabaticos/json/', MovilidadJSON.as_view(tipo='SABATICO'), name='sabatico_lista1__json'),
    url(r'^mov-sabaticos/$', MovilidadLista.as_view(tipo='SABATICO', obj='sabático', objs='sabáticos', Objs='Sabáticos', url_seccion='sabaticos'), name='sabatico1_lista'),
    url(r'^mov-sabaticos/(?P<pk>[\w\-]+)/eliminar$', MovilidadAcademicaEliminar.as_view()),
    url(r'^mov-sabaticos/(?P<pk>[\w\-]+)/$', MovilidadDetalle.as_view(tipo='SABATICO'), name='sabatico1_detalle'),

    url(r'^invitados/json/', InvitadoMovilidadJSON.as_view(), name='invitado_lista__json'),
    url(r'^invitados/$', InvitadoMovilidadLista.as_view(), name='invitado_lista'),
    url(r'^invitados/(?P<pk>[\w\-]+)/eliminar$', InvitadoMovilidadEliminar.as_view(), name='invitado_eliminar'),
    url(r'^invitados/(?P<pk>[\w\-]+)/$', InvitadoMovilidadDetalle.as_view(), name='invitado_detalle'),

    url(r'^estancias/json/', EstanciaMovilidadJSON.as_view(), name='estancia_lista__json'),
    url(r'^estancias/$', EstanciaMovilidadLista.as_view(), name='estancia_lista'),
    url(r'^estancias/(?P<pk>[\w\-]+)/eliminar$', EstanciaMovilidadEliminar.as_view(), name='estancia_eliminar'),
    url(r'^estancias/(?P<pk>[\w\-]+)/$', EstanciaMovilidadDetalle.as_view(), name='estancia_detalle'),

    url(r'^sabaticos/json/', SabaticoMovilidadJSON.as_view(), name='sabatico_lista__json'),
    url(r'^sabaticos/$', SabaticoMovilidadLista.as_view(), name='sabatico_lista'),
    url(r'^sabaticos/(?P<pk>[\w\-]+)/eliminar$', SabaticoMovilidadEliminar.as_view(), name='sabatico_eliminar'),
    url(r'^sabaticos/(?P<pk>[\w\-]+)/$', SabaticoMovilidadDetalle.as_view(), name='sabatico_detalle'),
]