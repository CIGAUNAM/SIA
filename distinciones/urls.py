from django.conf.urls import url
from . views import *


urlpatterns = [
    url(r'^academicos/json/', DistincionAcademicoJSON.as_view(), name='distincion_academico_lista__json'),
    url(r'^academicos/json-otros/', DistincionAcademicoJSON.as_view(otros=True), name='distincion_academico_lista__json_otros'),
    url(r'^academicos/$', DistincionAcademicoLista.as_view(), name='distincion_academico_lista'),
    url(r'^academicos/(?P<pk>[\w\-]+)/eliminar$', DistincionAcademicoEliminar.as_view(), name='distincion_academico_eliminar'),
    url(r'^academicos/(?P<pk>[\w\-]+)/$', DistincionAcademicoDetalle.as_view(), name='distincion_academico_detalle'),

    url(r'^alumnos/json/', DistincionAlumnoJSON.as_view(), name='distincion_alumno_lista__json'),
    url(r'^alumnos/json-otros/', DistincionAlumnoJSON.as_view(otros=True), name='distincion_alumno_lista__json_otros'),
    url(r'^alumnos/$', DistincionAlumnoLista.as_view(), name='distincion_alumno_lista'),
    url(r'^alumnos/(?P<pk>[\w\-]+)/eliminar$', DistincionAlumnoEliminar.as_view(), name='distincion_alumno_eliminar'),
    url(r'^alumnos/(?P<pk>[\w\-]+)/$', DistincionAlumnoDetalle.as_view(), name='distincion_alumno_detalle'),

]
