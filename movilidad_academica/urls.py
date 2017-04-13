from django.conf.urls import url
from . views import *

urlpatterns = [

    url(r'^invitados/json/', MovilidadJSON.as_view(tipo='INVITACION'), name='invitado_lista__json'),
    url(r'^invitados/$', MovilidadLista.as_view(tipo='INVITACION'), name='invitado_lista'),
    url(r'^invitados/(?P<pk>[\w\-]+)/$', MovilidadDetalle.as_view(), name='invitado_detalle'),

    url(r'^estancias/json/', MovilidadJSON.as_view(tipo='ESTANCIA'), name='estancia_lista__json'),
    url(r'^estancias/$', MovilidadLista.as_view(tipo='ESTANCIA'), name='estancia_lista'),
    url(r'^estancias/(?P<pk>[\w\-]+)/$', MovilidadDetalle.as_view(), name='estancia_detalle'),

    url(r'^sabaticos/json/', MovilidadJSON.as_view(tipo='SABATICO'), name='sabatico_lista__json'),
    url(r'^sabaticos/$', MovilidadLista.as_view(tipo='SABATICO'), name='sabatico_lista'),
    url(r'^sabaticos/(?P<pk>[\w\-]+)/$', MovilidadDetalle.as_view(), name='sabatico_detalle'),

]