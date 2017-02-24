from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from formacion_academica import views

urlpatterns = [

    url(r'^cursos-especializacion/$', views.curso_especializacion, name='cursos_especializacion'),


    url(r'^acursos.especializacion/$', views.CursoEspecializacionList.as_view()),
    url(r'^acurso.especializacion/(?P<pk>[0-9]+)/$', views.CursoEspecializacionDetail.as_view()),
    url(r'^alicenciaturas/$', views.LicenciaturaList.as_view()),
    url(r'^alicenciatura/(?P<pk>[0-9]+)/$', views.LicenciaturaDetail.as_view()),
    url(r'^amaestrias/$', views.MaestriaList.as_view()),
    url(r'^amaestria/(?P<pk>[0-9]+)/$', views.MaestriaDetail.as_view()),
    url(r'^adoctorados/$', views.DoctoradoList.as_view()),
    url(r'^adoctorado/(?P<pk>[0-9]+)/$', views.DoctoradoDetail.as_view()),
    url(r'^apostdoctorados/$', views.PostDoctoradoList.as_view()),
    url(r'^apostdoctorado/(?P<pk>[0-9]+)/$', views.PostDoctoradoDetail.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)




