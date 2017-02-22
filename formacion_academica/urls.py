from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from formacion_academica import views

urlpatterns = [
    url(r'^cursos.especializacion/$', views.CursoEspecializacionList.as_view()),
    url(r'^curso.especializacion/(?P<pk>[0-9]+)/$', views.CursoEspecializacionDetail.as_view()),
    url(r'^licenciaturas/$', views.LicenciaturaList.as_view()),
    url(r'^licenciatura/(?P<pk>[0-9]+)/$', views.LicenciaturaDetail.as_view()),
    url(r'^maestrias/$', views.MaestriaList.as_view()),
    url(r'^maestria/(?P<pk>[0-9]+)/$', views.MaestriaDetail.as_view()),
    url(r'^doctorados/$', views.DoctoradoList.as_view()),
    url(r'^doctorado/(?P<pk>[0-9]+)/$', views.DoctoradoDetail.as_view()),
    url(r'^postdoctorados/$', views.PostDoctoradoList.as_view()),
    url(r'^postdoctorado/(?P<pk>[0-9]+)/$', views.PostDoctoradoDetail.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)




