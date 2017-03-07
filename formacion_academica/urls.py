from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from formacion_academica.views import *

urlpatterns = [

    url(r'^cursos-especializacion/$', cursos_especializacion, name='cursos_especializacion'),
    url(r'^cursos-especializacion/cursos_json/', cursos_json, name='cursos_json'),
    url(r'^cursos-especializacion/(?P<slug>[\w\-]+)/$', curso_especializacion_detalle, name='cursos_especializacion'),


    url(r'^acursos.especializacion/$', CursoEspecializacionList.as_view()),
    url(r'^acurso.especializacion/(?P<pk>[0-9]+)/$', CursoEspecializacionDetail.as_view()),
    url(r'^alicenciaturas/$', LicenciaturaList.as_view()),
    url(r'^alicenciatura/(?P<pk>[0-9]+)/$', LicenciaturaDetail.as_view()),
    url(r'^amaestrias/$', MaestriaList.as_view()),
    url(r'^amaestria/(?P<pk>[0-9]+)/$', MaestriaDetail.as_view()),
    url(r'^adoctorados/$', DoctoradoList.as_view()),
    url(r'^adoctorado/(?P<pk>[0-9]+)/$', DoctoradoDetail.as_view()),
    url(r'^apostdoctorados/$', PostDoctoradoList.as_view()),
    url(r'^apostdoctorado/(?P<pk>[0-9]+)/$', PostDoctoradoDetail.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)




