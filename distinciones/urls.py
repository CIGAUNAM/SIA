from django.conf.urls import url
from . views import *


urlpatterns = [
    url(r'^academicos/json/', DistincionAcademicoJSON.as_view(), name='distincion_academico_lista__json'),
    url(r'^academicos/$', DistincionAcademicoLista.as_view(), name='distincion_academico_lista'),
    url(r'^academicos/(?P<pk>[\w\-]+)/eliminar$', DistincionAcademicoEliminar.as_view(), name='distincion_academico_eliminar'),
    url(r'^academicos/(?P<pk>[\w\-]+)/$', DistincionAcademicoDetalle.as_view(), name='distincion_academico_detalle'),

    url(r'^alumnos/json/', DistincionAlumnoJSON.as_view(), name='distincion_alumno_lista__json'),
    url(r'^alumnos/json-otros/', DistincionAlumnoJSON.as_view(otros=True), name='distincion_alumno_lista__json_otros'),
    url(r'^alumnos/$', DistincionAlumnoLista.as_view(), name='distincion_alumno_lista'),
    url(r'^alumnos/(?P<pk>[\w\-]+)/eliminar$', DistincionAlumnoEliminar.as_view(), name='distincion_alumno_eliminar'),
    url(r'^alumnos/(?P<pk>[\w\-]+)/$', DistincionAlumnoDetalle.as_view(), name='distincion_alumno_detalle'),

    url(r'^comisiones-expertos/json/', ParticipacionComisionExpertosJSON.as_view(), name='comision_expertos_lista__json'),
    url(r'^comisiones-expertos/$', ParticipacionComisionExpertosLista.as_view(), name='comision_expertos_lista'),
    url(r'^comisiones-expertos/(?P<pk>[\w\-]+)/eliminar$', ParticipacionComisionExpertosEliminar.as_view(), name='comision_expertos_eliminar'),
    url(r'^comisiones-expertos/(?P<pk>[\w\-]+)/$', ParticipacionComisionExpertosDetalle.as_view(), name='comision_expertos_detalle'),

    url(r'^sociedades-cientificas/json/', ParticipacionSociedadCientificaJSON.as_view(), name='sociedad_cientifica_lista__json'),
    url(r'^sociedades-cientificas/$', ParticipacionSociedadCientificaLista.as_view(), name='sociedad_cientifica_lista'),
    url(r'^sociedades-cientificas/(?P<pk>[\w\-]+)/eliminar$', ParticipacionSociedadCientificaEliminar.as_view(), name='sociedad_cientifica_eliminar'),
    url(r'^sociedades-cientificas/(?P<pk>[\w\-]+)/$', ParticipacionSociedadCientificaDetalle.as_view(), name='sociedad_cientifica_detalle'),

    url(r'^citas-publicaciones/json/', CitaPublicacionJSON.as_view(), name='cita_publicacion_lista__json'),
    url(r'^citas-publicaciones/json-otros/', CitaPublicacionJSON.as_view(otros=True), name='cita_publicacion_lista__json_otros'),
    url(r'^citas-publicaciones/$', CitaPublicacionLista.as_view(), name='cita_publicacion_lista'),
    url(r'^citas-publicaciones/(?P<pk>[\w\-]+)/eliminar$', CitaPublicacionEliminar.as_view(), name='cita_publicacion_eliminar'),
    url(r'^citas-publicaciones/(?P<pk>[\w\-]+)/$', CitaPublicacionDetalle.as_view(), name='cita_publicacion_detalle'),

]
