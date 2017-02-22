from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from nucleo import views

urlpatterns = [
    url(r'^tags/$', views.TagList.as_view()),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.TagDetail.as_view()),
    url(r'^zonas.paises/$', views.ZonaPaisList.as_view()),
    url(r'^zona.pais/(?P<pk>[0-9]+)/$', views.ZonaPaisDetail.as_view()),
    url(r'^paises/$', views.PaisList.as_view()),
    url(r'^pais/(?P<pk>[0-9]+)/$', views.PaisDetail.as_view()),
    url(r'^estados/$', views.EstadoList.as_view()),
    url(r'^estado/(?P<pk>[0-9]+)/$', views.EstadoDetail.as_view()),
    url(r'^ciudades/$', views.CiudadList.as_view()),
    url(r'^ciudad/(?P<pk>[0-9]+)/$', views.CiudadDetail.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^user/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^instituciones/$', views.InstitucionList.as_view()),
    url(r'^institucion/(?P<pk>[0-9]+)/$', views.InstitucionDetail.as_view()),
    url(r'^dependencias/$', views.DependenciaList.as_view()),
    url(r'^dependencia/(?P<pk>[0-9]+)/$', views.DependenciaDetail.as_view()),
    url(r'^cargos/$', views.CargoList.as_view()),
    url(r'^cargo/(?P<pk>[0-9]+)/$', views.CargoDetail.as_view()),
    url(r'^nombramientos/$', views.NombramientoList.as_view()),
    url(r'^nombramientos/(?P<pk>[0-9]+)/$', views.NombramientoDetail.as_view()),
    url(r'^areas.conocimiento/$', views.AreaConocimientoList.as_view()),
    url(r'^area.conocimiento/(?P<pk>[0-9]+)/$', views.AreaConocimientoDetail.as_view()),
    url(r'^areas.especialidad/$', views.AreaEspecialidadList.as_view()),
    url(r'^area.especialidad/(?P<pk>[0-9]+)/$', views.AreaEspecialidadDetail.as_view()),
    url(r'^impactos.sociales/$', views.ImpactoSocialList.as_view()),
    url(r'^impacto.social/(?P<pk>[0-9]+)/$', views.ImpactoSocialDetail.as_view()),
    url(r'^programas.financiamiento/$', views.ProgramaFinanciamientoList.as_view()),
    url(r'^programa.financiamiento/(?P<pk>[0-9]+)/$', views.ProgramaFinanciamientoDetail.as_view()),
    url(r'^financiamientos/$', views.FinanciamientoList.as_view()),
    url(r'^financiamiento/(?P<pk>[0-9]+)/$', views.FinanciamientoDetail.as_view()),
    url(r'^metodologias/$', views.MetodologiaList.as_view()),
    url(r'^metodologia/(?P<pk>[0-9]+)/$', views.MetodologiaDetail.as_view()),
    url(r'^programas.licenciatura/$', views.ProgramaLicenciaturaList.as_view()),
    url(r'^programa.licenciatura/(?P<pk>[0-9]+)/$', views.ProgramaLicenciaturaDetail.as_view()),
    url(r'^programas.maestria/$', views.ProgramaMaestriaList.as_view()),
    url(r'^programa.maestria/(?P<pk>[0-9]+)/$', views.ProgramaMaestriaDetail.as_view()),
    url(r'^programas.doctorado/$', views.ProgramaDoctoradoList.as_view()),
    url(r'^programa.doctorado/(?P<pk>[0-9]+)/$', views.ProgramaDoctoradoDetail.as_view()),
    url(r'^proyectos/$', views.ProyectoList.as_view()),
    url(r'^proyecto/(?P<pk>[0-9]+)/$', views.ProyectoDetail.as_view())
]


urlpatterns = format_suffix_patterns(urlpatterns)