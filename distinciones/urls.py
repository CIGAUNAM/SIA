from django.conf.urls import url
from . views import *


urlpatterns = [
    url(r'^academicos/json/', DistincionAcademicoJSON.as_view(), name='distincio_academico_lista__json'),
    url(r'^academicos/json-otros/', DistincionAcademicoJSON.as_view(otros=True), name='distincio_academico_lista__json_otros'),
    url(r'^academicos/$', DistincionAcademicoLista.as_view(), name='distincio_academico_lista'),
    url(r'^academicos/(?P<pk>[\w\-]+)/$', DistincionAcademicoDetalle.as_view(), name='distincio_academico_detalle'),

    url(r'^alumnos/json-otros/', CursoDocenciaExtracurricularJSON.as_view(otros=True), name='curso_docencia_extracurriculares_lista__json_otros'),
    url(r'^alumnos/$', CursoDocenciaExtracurricularLista.as_view(), name='curso_docencia_extracurriculares_lista'),
    url(r'^alumnos/(?P<pk>[\w\-]+)/$', CursoDocenciaExtracurricularDetalle.as_view(), name='curso_docencia_extracurriculares_detalle'),
    url(r'^alumnos/json/', CursoDocenciaExtracurricularJSON.as_view(), name='curso_docencia_extracurriculares_lista__json'),
]