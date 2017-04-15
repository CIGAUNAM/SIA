from django.conf.urls import url
from . views import *




urlpatterns = [

    url(r'^asesorias/json/', AsesorEstanciaJSON.as_view(), name='asesor_estancia_lista__json'),
    url(r'^asesorias/$', AsesorEstanciaLista.as_view(), name='asesor_estancia_lista'),
    url(r'^asesorias/(?P<pk>[\w\-]+)/$', AsesorEstanciaDetalle.as_view(), name='asesor_estancia_detalle'),

    url(r'^direccion-tesis/json/', DireccionTesisJSON.as_view(), name='direccion_tesis_lista__json'),
    url(r'^direccion-tesis/$', DireccionTesisLista.as_view(), name='direccion_tesis_lista'),
    url(r'^direccion-tesis/(?P<pk>[\w\-]+)/$', DireccionTesisDetalle.as_view(), name='direccion_tesis_detalle'),

]