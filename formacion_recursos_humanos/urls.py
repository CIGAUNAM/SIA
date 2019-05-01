from django.conf.urls import url
from . views import *




urlpatterns = [

    url(r'^asesorias/json2/', AsesoriaEstudianteJSON.as_view(), name='asesor_estancia_lista__json'),
    url(r'^asesorias/$', AsesoriaEstudianteLista.as_view(), name='asesor_estancia_lista'),
    url(r'^asesorias/(?P<pk>[\w\-]+)/eliminar$', AsesoriaEstudianteEliminar.as_view(), name='asesor_estancia_eliminar'),
    url(r'^asesorias/(?P<pk>[\w\-]+)/$', AsesoriaEstudianteDetalle.as_view(), name='asesor_estancia_detalle'),

    url(r'^supervision-investigadores-postdoctorales/json2/', SupervisionInvestigadorPostDoctoralJSON.as_view(), name='supervision_investigador_postdoctoral_lista__json'),
    url(r'^supervision-investigadores-postdoctorales/$', SupervisionInvestigadorPostDoctoralLista.as_view(), name='supervision_investigador_postdoctoral_lista'),
    url(r'^supervision-investigadores-postdoctorales/(?P<pk>[\w\-]+)/eliminar$', SupervisionInvestigadorPostDoctoralEliminar.as_view(), name='supervision_investigador_postdoctoral_eliminar'),
    url(r'^supervision-investigadores-postdoctorales/(?P<pk>[\w\-]+)/$', SupervisionInvestigadorPostDoctoralDetalle.as_view(), name='supervision_investigador_postdoctoral_detalle'),

    url(r'^grupos-investigacion-internos/json2/', DesarrolloGrupoInvestigacionInternoJSON.as_view(), name='grupo_investigacion_interno_lista__json'),
    url(r'^grupos-investigacion-internos/json2-otros/', DesarrolloGrupoInvestigacionInternoJSON.as_view(otros=True), name='grupo_investigacion_interno_lista__json_otros'),
    url(r'^grupos-investigacion-internos/$', DesarrolloGrupoInvestigacionInternoLista.as_view(), name='grupo_investigacion_interno_lista'),
    url(r'^grupos-investigacion-internos/(?P<pk>[\w\-]+)/eliminar$', DesarrolloGrupoInvestigacionInternoEliminar.as_view(), name='grupo_investigacion_interno_eliminar'),
    url(r'^grupos-investigacion-internos/(?P<pk>[\w\-]+)/$', DesarrolloGrupoInvestigacionInternoDetalle.as_view(), name='grupo_investigacion_interno_detalle'),

    url(r'^direccion-tesis/json2/', DireccionTesisJSON.as_view(), name='direccion_tesis_lista__json'),
    url(r'^direccion-tesis/json2-otros/', DireccionTesisJSON.as_view(otros=True), name='direccion_tesis_lista__json_otros'),
    url(r'^direccion-tesis/$', DireccionTesisLista.as_view(), name='direccion_tesis_lista'),
    url(r'^direccion-tesis/(?P<pk>[\w\-]+)/eliminar$', DireccionTesisEliminar.as_view(), name='direccion_tesis_eliminar'),
    url(r'^direccion-tesis/(?P<pk>[\w\-]+)/$', DireccionTesisDetalle.as_view(), name='direccion_tesis_detalle'),

    url(r'^comites-tutorales/json2/', ComiteTutoralJSON.as_view(), name='comite_tutoral_lista__json'),
    url(r'^comites-tutorales/json2-otros/', ComiteTutoralJSON.as_view(otros=True), name='comite_tutoral_lista__json_otros'),
    url(r'^comites-tutorales/$', ComiteTutoralLista.as_view(), name='comite_tutoral_lista'),
    url(r'^comites-tutorales/(?P<pk>[\w\-]+)/eliminar$', ComiteTutoralEliminar.as_view(), name='comite_tutoral_eliminar'),
    url(r'^comites-tutorales/(?P<pk>[\w\-]+)/$', ComiteTutoralDetalle.as_view(), name='comite_tutoral_detalle'),

    url(r'^comites-candidatura-doctoral/json2/', ComiteCandidaturaDoctoralJSON.as_view(), name='comite_candidatura_doctoral_lista__json'),
    url(r'^comites-candidatura-doctoral/json2-otros/', ComiteCandidaturaDoctoralJSON.as_view(otros=True), name='comite_candidatura_doctoral_lista__json_otros'),
    url(r'^comites-candidatura-doctoral/$', ComiteCandidaturaDoctoralLista.as_view(), name='comite_candidatura_doctoral_lista'),
    url(r'^comites-candidatura-doctoral/(?P<pk>[\w\-]+)/eliminar$', ComiteCandidaturaDoctoralEliminar.as_view(), name='comite_candidatura_doctoral_eliminar'),
    url(r'^comites-candidatura-doctoral/(?P<pk>[\w\-]+)/$', ComiteCandidaturaDoctoralDetalle.as_view(), name='comite_candidatura_doctoral_detalle'),
]