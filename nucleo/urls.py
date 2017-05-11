from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from nucleo import views

urlpatterns = [
    url(r'^tags/', views.TagLista.as_view()),

    url(r'^rest/tags/$', views.TagList.as_view()),
    url(r'^rest/tag/(?P<pk>[0-9]+)/$', views.TagDetail.as_view()),
    url(r'^rest/zonas.paises/$', views.ZonaPaisList.as_view()),
    url(r'^rest/zona.pais/(?P<pk>[0-9]+)/$', views.ZonaPaisDetail.as_view()),
    url(r'^rest/paises/$', views.PaisList.as_view()),
    url(r'^rest/pais/(?P<pk>[0-9]+)/$', views.PaisDetail.as_view()),
    url(r'^rest/estados/$', views.EstadoList.as_view()),
    url(r'^rest/estado/(?P<pk>[0-9]+)/$', views.EstadoDetail.as_view()),
    url(r'^rest/ciudades/$', views.CiudadList.as_view()),
    url(r'^rest/ciudad/(?P<pk>[0-9]+)/$', views.CiudadDetail.as_view()),
    url(r'^rest/users/$', views.UserList.as_view()),
    url(r'^rest/user/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^rest/instituciones/$', views.InstitucionList.as_view()),
    url(r'^rest/institucion/(?P<pk>[0-9]+)/$', views.InstitucionDetail.as_view()),
    url(r'^rest/dependencias/$', views.DependenciaList.as_view()),
    url(r'^rest/dependencia/(?P<pk>[0-9]+)/$', views.DependenciaDetail.as_view()),
    url(r'^rest/cargos/$', views.CargoList.as_view()),
    url(r'^rest/nombre/(?P<pk>[0-9]+)/$', views.CargoDetail.as_view()),
    url(r'^rest/nombramientos/$', views.NombramientoList.as_view()),
    url(r'^rest/nombramientos/(?P<pk>[0-9]+)/$', views.NombramientoDetail.as_view()),
    url(r'^rest/areas.conocimiento/$', views.AreaConocimientoList.as_view()),
    url(r'^rest/area.conocimiento/(?P<pk>[0-9]+)/$', views.AreaConocimientoDetail.as_view()),
    url(r'^rest/areas.especialidad/$', views.AreaEspecialidadList.as_view()),
    url(r'^rest/area.especialidad/(?P<pk>[0-9]+)/$', views.AreaEspecialidadDetail.as_view()),
    url(r'^rest/impactos.sociales/$', views.ImpactoSocialList.as_view()),
    url(r'^rest/impacto.social/(?P<pk>[0-9]+)/$', views.ImpactoSocialDetail.as_view()),
    url(r'^rest/programas.financiamiento/$', views.ProgramaFinanciamientoList.as_view()),
    url(r'^rest/programa.financiamiento/(?P<pk>[0-9]+)/$', views.ProgramaFinanciamientoDetail.as_view()),
    url(r'^rest/financiamientos/$', views.FinanciamientoList.as_view()),
    url(r'^rest/financiamiento/(?P<pk>[0-9]+)/$', views.FinanciamientoDetail.as_view()),
    url(r'^rest/metodologias/$', views.MetodologiaList.as_view()),
    url(r'^rest/metodologia/(?P<pk>[0-9]+)/$', views.MetodologiaDetail.as_view()),
    url(r'^rest/programas.licenciatura/$', views.ProgramaLicenciaturaList.as_view()),
    url(r'^rest/programa.licenciatura/(?P<pk>[0-9]+)/$', views.ProgramaLicenciaturaDetail.as_view()),
    url(r'^rest/programas.maestria/$', views.ProgramaMaestriaList.as_view()),
    url(r'^rest/programa.maestria/(?P<pk>[0-9]+)/$', views.ProgramaMaestriaDetail.as_view()),
    url(r'^rest/programas.doctorado/$', views.ProgramaDoctoradoList.as_view()),
    url(r'^rest/programa.doctorado/(?P<pk>[0-9]+)/$', views.ProgramaDoctoradoDetail.as_view()),
    url(r'^rest/proyectos/$', views.ProyectoList.as_view()),
    url(r'^rest/proyecto/(?P<pk>[0-9]+)/$', views.ProyectoDetail.as_view())
]


urlpatterns = format_suffix_patterns(urlpatterns)