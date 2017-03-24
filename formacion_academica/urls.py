from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . views import *

urlpatterns = [

    url(r'^cursos-especializacion/$', CursoEspecializacionLista.as_view(), name='curso_especializacion_lista'),
    url(r'^cursos-especializacion/cursos_json/', CursoEspecializacionJSON.as_view(), name='curso_especializacion_lista__json'),
    url(r'^cursos-especializacion/(?P<pk>[\w\-]+)/$', CursoEspecializacionDetalle.as_view(), name='curso_especializacion_detalle'),

    url(r'^licenciaturas/licenciaturas_json/', LicenciaturaJSON.as_view(), name='licenciatura_lista__json'),
    url(r'^licenciaturas/$', LicenciaturaLista.as_view(), name='licenciatura_lista'),
    url(r'^licenciaturas/(?P<pk>[\w\-]+)/$', LicenciaturaDetalle.as_view(), name='licenciatura_detalle'),

    url(r'^maestrias/json/', MaestriaJSON.as_view(), name='maestria_lista__json'),
    url(r'^maestrias/$', MaestriaLista.as_view(), name='maestria_lista'),
    url(r'^maestrias/(?P<pk>[\w\-]+)/$', MaestriaDetalle.as_view(), name='maestria_detalle'),

    #url(r'^acursos.especializacion/$', CursoEspecializacionList.as_view()),
    #url(r'^acurso.especializacion/(?P<pk>[0-9]+)/$', CursoEspecializacionDetail.as_view()),
    #url(r'^alicenciaturas/$', LicenciaturaList.as_view()),
    #url(r'^alicenciatura/(?P<pk>[0-9]+)/$', LicenciaturaDetail.as_view()),
    #url(r'^amaestrias/$', MaestriaList.as_view()),
    #url(r'^amaestria/(?P<pk>[0-9]+)/$', MaestriaDetail.as_view()),
    #url(r'^adoctorados/$', DoctoradoList.as_view()),
    #url(r'^adoctorado/(?P<pk>[0-9]+)/$', DoctoradoDetail.as_view()),
    #url(r'^apostdoctorados/$', PostDoctoradoList.as_view()),
    #url(r'^apostdoctorado/(?P<pk>[0-9]+)/$', PostDoctoradoDetail.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)




