from django.conf.urls import url
from . views import *

#


urlpatterns = [

    url(r'^desarrollos-tecnologicos/json/', DesarrolloTecnologicoJSON.as_view(), name='desarrollo_tecnologico_lista__json'),
    url(r'^desarrollos-tecnologicos/json-otros/', DesarrolloTecnologicoJSON.as_view(otros=True), name='desarrollo_tecnologico_lista__json_otros'),
    url(r'^desarrollos-tecnologicos/$', DesarrolloTecnologicoLista.as_view(), name='desarrollo_tecnologico_lista'),
    url(r'^desarrollos-tecnologicos/(?P<pk>[\w\-]+)/$', DesarrolloTecnologicoDetalle.as_view(), name='desarrollo_tecnologico_detalle'),
    url(r'^desarrollos-tecnologicos/(?P<pk>[\w\-]+)/eliminar$', DesarrolloTecnologicoEliminar.as_view(), name='desarrollo_tecnologico_eliminar'),

]