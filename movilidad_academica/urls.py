from django.conf.urls import url
from . views import *

urlpatterns = [
    url(r'^mov-invitados/json/', MovilidadJSON.as_view(tipo='INVITACION'), name='invitado_lista__json'),
    url(r'^mov-invitados/$', MovilidadLista.as_view(tipo='INVITACION', obj='invitado', objs='invitados', Objs='Invitados', url_seccion='invitados'), name='invitado_lista'),
    url(r'^mov-invitados/(?P<pk>[\w\-]+)/eliminar$', MovilidadAcademicaEliminar.as_view()),
    url(r'^mov-invitados/(?P<pk>[\w\-]+)/$', MovilidadDetalle.as_view(tipo='INVITACION', url_seccion='invitados'), name='invitado_detalle'),

    url(r'^mov-estancias/json/', MovilidadJSON.as_view(tipo='ESTANCIA'), name='estancia_lista__json'),
    url(r'^mov-estancias/$', MovilidadLista.as_view(tipo='ESTANCIA', obj='estancia de colaboración', objs='estancias de colaboración', Objs='Estancias de colaboración', url_seccion='estancias'), name='estancia_lista'),
    url(r'^mov-estancias/(?P<pk>[\w\-]+)/eliminar$', MovilidadAcademicaEliminar.as_view()),
    url(r'^mov-estancias/(?P<pk>[\w\-]+)/$', MovilidadDetalle.as_view(tipo='ESTANCIA'), name='estancia_detalle'),

    url(r'^mov-sabaticos/json/', MovilidadJSON.as_view(tipo='SABATICO'), name='sabatico_lista__json'),
    url(r'^mov-sabaticos/$', MovilidadLista.as_view(tipo='SABATICO', obj='sabático', objs='sabáticos', Objs='Sabáticos', url_seccion='sabaticos'), name='sabatico_lista'),
    url(r'^mov-sabaticos/(?P<pk>[\w\-]+)/eliminar$', MovilidadAcademicaEliminar.as_view()),
    url(r'^mov-sabaticos/(?P<pk>[\w\-]+)/$', MovilidadDetalle.as_view(tipo='SABATICO'), name='sabatico_detalle'),

]