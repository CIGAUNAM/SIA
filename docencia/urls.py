from django.conf.urls import url
from . views import *


urlpatterns = [
    url(r'^cursos-escolarizados/json2/', CursoDocenciaEscolarizadoJSON.as_view(), name='curso_docencia_escolarizado_lista__json'),
    url(r'^cursos-escolarizados/json2-otros/', CursoDocenciaEscolarizadoJSON.as_view(otros=True), name='curso_docencia_escolarizado_lista__json_otros'),
    url(r'^cursos-escolarizados/$', CursoDocenciaEscolarizadoLista.as_view(), name='curso_docencia_escolarizado_lista'),
    url(r'^cursos-escolarizados/(?P<pk>[\w\-]+)/eliminar$', CursoDocenciaEliminar.as_view(), name='curso_docencia_escolarizado_eliminar'),
    url(r'^cursos-escolarizados/(?P<pk>[\w\-]+)/$', CursoDocenciaEscolarizadoDetalle.as_view(), name='curso_docencia_escolarizado_detalle'),

    url(r'^cursos-extracurriculares/json2/', CursoDocenciaExtracurricularJSON.as_view(), name='curso_docencia_extracurricular_lista__json'),
    url(r'^cursos-extracurriculares/json2-otros/', CursoDocenciaExtracurricularJSON.as_view(otros=True), name='curso_docencia_extracurricular_lista__json_otros'),
    url(r'^cursos-extracurriculares/$', CursoDocenciaExtracurricularLista.as_view(), name='curso_docencia_extracurricular_lista'),
    url(r'^cursos-extracurriculares/(?P<pk>[\w\-]+)/eliminar$', CursoDocenciaEliminar.as_view(), name='curso_docencia_extracurricular_eliminar'),
    url(r'^cursos-extracurriculares/(?P<pk>[\w\-]+)/$', CursoDocenciaExtracurricularDetalle.as_view(), name='curso_docencia_extracurricular_detalle'),

    url(r'^articulos-docencia/json2/', ArticuloDocenciaJSON.as_view(), name='articulo_docencia_lista__json'),
    url(r'^articulos-docencia/json2-otros/', ArticuloDocenciaJSON.as_view(otros=True), name='articulo_docencia_lista__json_otros'),
    url(r'^articulos-docencia/$', ArticuloDocenciaLista.as_view(), name='articulo_docencia_lista'),
    url(r'^articulos-docencia/(?P<pk>[\w\-]+)/eliminar$', ArticuloDocenciaEliminar.as_view(), name='articulo_docencia_eliminar'),
    url(r'^articulos-docencia/(?P<pk>[\w\-]+)/$', ArticuloDocenciaDetalle.as_view(), name='articulo_docencia_detalle'),

    url(r'^libros-docencia/json2/', LibroDocenciaJSON.as_view(), name='libro_docencia_lista__json'),
    url(r'^libros-docencia/json2-otros/', LibroDocenciaJSON.as_view(otros=True), name='libro_docencia_lista__json_otros'),
    url(r'^libros-docencia/$', LibroDocenciaLista.as_view(), name='libro_docencia_lista'),
    url(r'^libros-docencia/(?P<pk>[\w\-]+)/eliminar$', LibroDocenciaEliminar.as_view(), name='libro_docencia_eliminar'),
    url(r'^libros-docencia/(?P<pk>[\w\-]+)/$', LibroDocenciaDetalle.as_view(), name='libro_docencia_detalle'),

    url(r'^programas-estudio/json2/', ProgramaEstudioJSON.as_view(), name='programa_estudio_lista__json'),
    url(r'^programas-estudio/$', ProgramaEstudioLista.as_view(), name='programa_estudio_lista'),
    url(r'^programas-estudio/(?P<pk>[\w\-]+)/eliminar$', ProgramaEstudioEliminar.as_view(), name='programa_estudio_eliminar'),
    url(r'^programas-estudio/(?P<pk>[\w\-]+)/$', ProgramaEstudioDetalle.as_view(), name='programa_estudio_detalle'),

]