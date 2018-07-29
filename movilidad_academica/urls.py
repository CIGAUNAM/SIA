from django.conf.urls import url
from . views import *

urlpatterns = [
    url(r'^invitados/json/', MovilidadJSON.as_view(tipo='INVITACION'), name='invitado_lista__json'),
    url(r'^invitados/$', MovilidadLista.as_view(tipo='INVITACION', obj='invitado', objs='invitados', Objs='Invitados', url_seccion='invitados'), name='invitado_lista'),
    url(r'^invitados/(?P<pk>[\w\-]+)/eliminar$', MovilidadAcademicaEliminar.as_view()),
    url(r'^invitados/(?P<pk>[\w\-]+)/$', MovilidadDetalle.as_view(tipo='INVITACION', url_seccion='invitados'), name='invitado_detalle'),

    url(r'^estancias/json/', MovilidadJSON.as_view(tipo='ESTANCIA'), name='estancia_lista__json'),
    url(r'^estancias/$', MovilidadLista.as_view(tipo='ESTANCIA', obj='estancia de colaboración', objs='estancias de colaboración', Objs='Estancias de colaboración', url_seccion='estancias'), name='estancia_lista'),
    url(r'^estancias/(?P<pk>[\w\-]+)/eliminar$', MovilidadAcademicaEliminar.as_view()),
    url(r'^estancias/(?P<pk>[\w\-]+)/$', MovilidadDetalle.as_view(tipo='ESTANCIA'), name='estancia_detalle'),

    url(r'^sabaticos/json/', MovilidadJSON.as_view(tipo='SABATICO'), name='sabatico_lista__json'),
    url(r'^sabaticos/$', MovilidadLista.as_view(tipo='SABATICO', obj='sabático', objs='sabáticos', Objs='Sabáticos', url_seccion='sabaticos'), name='sabatico_lista'),
    url(r'^sabaticos/(?P<pk>[\w\-]+)/eliminar$', MovilidadAcademicaEliminar.as_view()),
    url(r'^sabaticos/(?P<pk>[\w\-]+)/$', MovilidadDetalle.as_view(tipo='SABATICO'), name='sabatico_detalle'),

]