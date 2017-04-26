from django.conf.urls import url
from . views import *




urlpatterns = [

    url(r'^asesorias/json/', AsesorEstanciaJSON.as_view(), name='asesor_estancia_lista__json'),
    url(r'^asesorias/$', AsesorEstanciaLista.as_view(), name='asesor_estancia_lista'),
    url(r'^asesorias/(?P<pk>[\w\-]+)/eliminar$', AsesorEstanciaEliminar.as_view(), name='asesor_estancia_eliminar'),
    url(r'^asesorias/(?P<pk>[\w\-]+)/$', AsesorEstanciaDetalle.as_view(), name='asesor_estancia_detalle'),

    url(r'^direccion-tesis/json/', DireccionTesisJSON.as_view(), name='direccion_tesis_lista__json'),
    url(r'^direccion-tesis/$', DireccionTesisLista.as_view(), name='direccion_tesis_lista'),
    url(r'^direccion-tesis/(?P<pk>[\w\-]+)/eliminar$', DireccionTesisEliminar.as_view(), name='direccion_tesis_eliminar'),
    url(r'^direccion-tesis/(?P<pk>[\w\-]+)/$', DireccionTesisDetalle.as_view(), name='direccion_tesis_detalle'),

    url(r'^comites-tutorales/json/', ComiteTutoralJSON.as_view(), name='comite_tutoral_lista__json'),
    url(r'^comites-tutorales/json-otros/', ComiteTutoralJSON.as_view(otros=True), name='comite_tutoral_lista__json_otros'),
    url(r'^comites-tutorales/$', ComiteTutoralLista.as_view(), name='comite_tutoral_lista'),
    url(r'^comites-tutorales/(?P<pk>[\w\-]+)/eliminar$', ComiteTutoralEliminar.as_view(), name='comite_tutoral_eliminar'),
    url(r'^comites-tutorales/(?P<pk>[\w\-]+)/$', ComiteTutoralDetalle.as_view(), name='comite_tutoral_detalle'),

    url(r'^comites-candidatura-doctoral/json/', ComiteCandidaturaDoctoralJSON.as_view(), name='comite_candidatura_doctoral_lista__json'),
    url(r'^comites-candidatura-doctoral/json-otros/', ComiteCandidaturaDoctoralJSON.as_view(otros=True), name='comite_candidatura_doctoral_lista__json_otros'),
    url(r'^comites-candidatura-doctoral/$', ComiteCandidaturaDoctoralLista.as_view(), name='comite_candidatura_doctoral_lista'),
    url(r'^comites-candidatura-doctoral/(?P<pk>[\w\-]+)/eliminar$', ComiteCandidaturaDoctoralEliminar.as_view(), name='comite_candidatura_doctoral_eliminar'),
    url(r'^comites-candidatura-doctoral/(?P<pk>[\w\-]+)/$', ComiteCandidaturaDoctoralDetalle.as_view(), name='comite_candidatura_doctoral_detalle'),

]