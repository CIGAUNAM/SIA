from django.conf.urls import url
from . views import *

urlpatterns = [

    url(r'^articulos-cientificos/json/', ArticuloCientificoJSON.as_view(), name='articulo_cientifico_lista__json'),
    url(r'^articulos-cientificos/$', ArticuloCientificoLista.as_view(), name='articulo_cientifico_lista'),
    url(r'^articulos-cientificos/(?P<pk>[\w\-]+)/$', ArticuloCientificoDetalle.as_view(), name='articulo_cientifico_detalle'),

]