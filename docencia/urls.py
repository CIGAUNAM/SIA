from django.conf.urls import url
from . views import *


urlpatterns = [
    url(r'^cursos-escolarizados/json/', ArbitrajePublicacionAcademicaJSON.as_view(), name='arbitraje_publicacion_academica_lista__json'),
    url(r'^cursos-escolarizados/$', ArbitrajePublicacionAcademicaLista.as_view(), name='arbitraje_publicacion_academica_lista'),
    url(r'^cursos-escolarizados/(?P<pk>[\w\-]+)/$', ArbitrajePublicacionAcademicaDetalle.as_view(), name='arbitraje_publicacion_academica_detalle'),

    url(r'^cursos-extracurriculares/json/', ArbitrajeProyectoInvestigacionJSON.as_view(), name='arbitraje_proyecto_investigacion_lista__json'),
    url(r'^cursos-extracurriculares/$', ArbitrajeProyectoInvestigacionLista.as_view(), name='arbitraje_proyecto_investigacion_lista'),
    url(r'^cursos-extracurriculares/(?P<pk>[\w\-]+)/$', ArbitrajeProyectoInvestigacionDetalle.as_view(), name='arbitraje_proyecto_investigacion_detalle'),
]