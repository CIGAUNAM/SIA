from django.conf.urls import url
from . views import *


urlpatterns = [
    url(r'^cursos-escolarizados/json/', CursoDocenciaLicenciaturaJSON.as_view(), name='curso_docencia_licenciatura_lista__json'),
    url(r'^cursos-escolarizados/$', CursoDocenciaLicenciaturaLista.as_view(), name='arbitraje_publicacion_academica_lista'),
    url(r'^cursos-escolarizados/(?P<pk>[\w\-]+)/$', CursoDocenciaLicenciaturaDetalle.as_view(), name='arbitraje_publicacion_academica_detalle'),

    #url(r'^cursos-extracurriculares/json/', CursoDocenciaJSON.as_view(), name='arbitraje_proyecto_investigacion_lista__json'),
    #url(r'^cursos-extracurriculares/$', CursoDocenciaLista.as_view(), name='arbitraje_proyecto_investigacion_lista'),
    #url(r'^cursos-extracurriculares/(?P<pk>[\w\-]+)/$', CursoDocenciaDetalle.as_view(), name='arbitraje_proyecto_investigacion_detalle'),
]