from django.conf.urls import url
from . views import *

urlpatterns = [

    url(r'^invitados/json/', InvitadoJSON.as_view(), name='invitado_lista__json'),
    url(r'^invitados/$', MovilidadLista.as_view(), name='invitado_lista'),
    url(r'^invitados/(?P<pk>[\w\-]+)/$', MovilidadDetalle.as_view(), name='invitado_detalle'),

]