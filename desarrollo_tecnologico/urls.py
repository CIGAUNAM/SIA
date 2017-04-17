from django.conf.urls import url
from . views import *

#


urlpatterns = [

    url(r'^desarrollos-tecnologicos/json/', ComiteCandidaturaDoctoralJSON.as_view(), name='comite_candidatura_doctoral_lista__json'),
    url(r'^desarrollos-tecnologicos/json-otros/', ComiteCandidaturaDoctoralJSON.as_view(otros=True), name='comite_candidatura_doctoral_lista__json_otros'),
    url(r'^desarrollos-tecnologicos/$', ComiteCandidaturaDoctoralLista.as_view(), name='comite_candidatura_doctoral_lista'),
    url(r'^desarrollos-tecnologicos/(?P<pk>[\w\-]+)/$', ComiteCandidaturaDoctoralDetalle.as_view(), name='comite_candidatura_doctoral_detalle'),

]