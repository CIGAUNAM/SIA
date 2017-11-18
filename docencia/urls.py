from django.conf.urls import url
from . views import *


urlpatterns = [
    url(r'^cursos-escolarizados/json/', CursoDocenciaEscolarizadoJSON.as_view(), name='curso_docencia_escolarizado_lista__json'),
    url(r'^cursos-escolarizados/json-otros/', CursoDocenciaEscolarizadoJSON.as_view(otros=True), name='curso_docencia_escolarizado_lista__json_otros'),
    url(r'^cursos-escolarizados/$', CursoDocenciaEscolarizadoLista.as_view(), name='curso_docencia_escolarizado_lista'),
    url(r'^cursos-escolarizados/(?P<pk>[\w\-]+)/eliminar$', CursoDocenciaEliminar.as_view(), name='curso_docencia_escolarizado_eliminar'),
    url(r'^cursos-escolarizados/(?P<pk>[\w\-]+)/$', CursoDocenciaEscolarizadoDetalle.as_view(), name='curso_docencia_escolarizado_detalle'),

    url(r'^cursos-extracurriculares/json/', CursoDocenciaExtracurricularJSON.as_view(), name='curso_docencia_extracurriculares_lista__json'),
    url(r'^cursos-extracurriculares/json-otros/', CursoDocenciaExtracurricularJSON.as_view(otros=True), name='curso_docencia_extracurriculares_lista__json_otros'),
    url(r'^cursos-extracurriculares/$', CursoDocenciaExtracurricularLista.as_view(), name='curso_docencia_extracurriculares_lista'),
    url(r'^cursos-extracurriculares/(?P<pk>[\w\-]+)/eliminar$', CursoDocenciaEliminar.as_view(), name='curso_docencia_extracurriculares_eliminar'),
    url(r'^cursos-extracurriculares/(?P<pk>[\w\-]+)/$', CursoDocenciaExtracurricularDetalle.as_view(), name='curso_docencia_extracurriculares_detalle'),

    url(r'^articulos-docencia/json/', ArticuloDocenciaJSON.as_view(), name='articulo_docencia_lista__json'),
    url(r'^articulos-docencia/json-otros/', ArticuloDocenciaJSON.as_view(otros=True), name='articulo_docencia_lista__json_otros'),
    url(r'^articulos-docencia/$', ArticuloDocenciaLista.as_view(), name='articulo_docencia_lista'),
    url(r'^articulos-docencia/(?P<pk>[\w\-]+)/eliminar$', ArticuloDocenciaEliminar.as_view(), name='articulo_docencia_eliminar'),
    url(r'^articulos-docencia/(?P<pk>[\w\-]+)/$', ArticuloDocenciaDetalle.as_view(), name='articulo_docencia_detalle'),

    url(r'^libros-docencia/json/', LibroDocenciaJSON.as_view(), name='libro_docencia_lista__json'),
    url(r'^libros-docencia/json-otros/', LibroDocenciaJSON.as_view(otros=True), name='libro_docencia_lista__json_otros'),
    url(r'^libros-docencia/$', LibroDocenciaLista.as_view(), name='libro_docencia_lista'),
    url(r'^libros-docencia/(?P<pk>[\w\-]+)/eliminar$', LibroDocenciaEliminar.as_view(), name='libro_docencia_eliminar'),
    url(r'^libros-docencia/(?P<pk>[\w\-]+)/$', LibroDocenciaDetalle.as_view(), name='libro_docencia_detalle'),

    url(r'^programas-estudio/json/', ProgramaEstudioJSON.as_view(), name='programa_estudio_lista__json'),
    url(r'^programas-estudio/$', ProgramaEstudioLista.as_view(), name='programa_estudio_lista'),
    url(r'^programas-estudio/(?P<pk>[\w\-]+)/eliminar$', ProgramaEstudioEliminar.as_view(), name='programa_estudio_eliminar'),
    url(r'^programas-estudio/(?P<pk>[\w\-]+)/$', ProgramaEstudioDetalle.as_view(), name='programa_estudio_detalle'),

]