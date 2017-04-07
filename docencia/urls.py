from django.conf.urls import url
from . views import *


urlpatterns = [
    url(r'^cursos-escolarizados/json/', CursoDocenciaEscolarizadoJSON.as_view(), name='curso_docencia_escolarizado_lista__json'),
    url(r'^cursos-escolarizados/json-otros/', CursoDocenciaEscolarizadoJSON.as_view(otros=True), name='curso_docencia_escolarizado_lista__json'),
    url(r'^cursos-escolarizados/$', CursoDocenciaEscolarizadoLista.as_view(), name='curso_docencia_escolarizado_lista'),
    url(r'^cursos-escolarizados/(?P<pk>[\w\-]+)/$', CursoDocenciaEscolarizadoDetalle.as_view(), name='curso_docencia_escolarizado_detalle'),

    #url(r'^cursos-extracurriculares/json/', CursoDocenciaJSON.as_view(), name='arbitraje_proyecto_investigacion_lista__json'),
    #url(r'^cursos-extracurriculares/$', CursoDocenciaLista.as_view(), name='arbitraje_proyecto_investigacion_lista'),
    #url(r'^cursos-extracurriculares/(?P<pk>[\w\-]+)/$', CursoDocenciaDetalle.as_view(), name='arbitraje_proyecto_investigacion_detalle'),
]