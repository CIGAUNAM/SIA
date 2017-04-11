from django.conf.urls import url
from . views import *

urlpatterns = [

    url(r'^invitados/json/', InvitadoJSON.as_view(), name='invitado_lista__json'),
    #url(r'^articulos-cientificos/json-otros/', ArticuloCientificoJSON.as_view(otros=True), name='articulo_cientifico_lista_otros__json'),
    url(r'^invitados/$', InvitadoLista.as_view(), name='invitado_lista'),
    url(r'^invitados/(?P<pk>[\w\-]+)/$', InvitadoDetalle.as_view(), name='invitado_detalle'),

]