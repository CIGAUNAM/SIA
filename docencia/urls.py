from django.conf.urls import url
from . views import *


urlpatterns = [
    url(r'^cursos-escolarizados/json/', CursoDocenciaEscolarizadoJSON.as_view(), name='curso_docencia_escolarizado_lista__json'),
    url(r'^cursos-escolarizados/json-otros/', CursoDocenciaEscolarizadoJSON.as_view(otros=True), name='curso_docencia_escolarizado_lista__json'),
    url(r'^cursos-escolarizados/$', CursoDocenciaEscolarizadoLista.as_view(), name='curso_docencia_escolarizado_lista'),
    url(r'^cursos-escolarizados/(?P<pk>[\w\-]+)/$', CursoDocenciaEscolarizadoDetalle.as_view(), name='curso_docencia_escolarizado_detalle'),

    url(r'^cursos-extracurriculares/json/', CursoDocenciaExtracurricularJSON.as_view(), name='curso_docencia_extracurriculares_lista__json'),
    url(r'^cursos-extracurriculares/json-otros/', CursoDocenciaExtracurricularJSON.as_view(otros=True), name='curso_docencia_extracurriculares_lista__json'),
    url(r'^cursos-extracurriculares/$', CursoDocenciaExtracurricularLista.as_view(), name='curso_docencia_extracurriculares_lista'),
    url(r'^cursos-extracurriculares/(?P<pk>[\w\-]+)/$', CursoDocenciaExtracurricularDetalle.as_view(), name='curso_docencia_extracurriculares_detalle'),
]