from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . views import *




urlpatterns = [

    url(r'^laborales/json/', ExperienciaLaboralJSON.as_view(), name='experiencia_laboral_lista__json'),
    url(r'^laborales/$', ExperienciaLaboralLista.as_view(), name='experiencia_laboral_lista'),
    url(r'^laborales/(?P<pk>[\w\-]+)/$', ExperienciaLaboralDetalle.as_view(), name='experiencia_laboral_detalle'),

    url(r'^lineas-investigacion/json/', LineaInvestigacionJSON.as_view(), name='linea_investigacion_lista__json'),
    url(r'^lineas-investigacion/$', LineaInvestigacionLista.as_view(), name='linea_investigacion_lista'),
    url(r'^lineas-investigacion/(?P<pk>[\w\-]+)/$', LineaInvestigacionDetalle.as_view(), name='linea_investigacion_detalle'),

    url(r'^capacidades/json/', CapacidadPotencialidadJSON.as_view(), name='capacidad_potencialidad_lista__json'),
    url(r'^capacidades/$', CapacidadPotencialidadLista.as_view(), name='capacidad_potencialidad_lista'),
    url(r'^capacidades/(?P<pk>[\w\-]+)/$', CapacidadPotencialidadDetalle.as_view(), name='capacidad_potencialidad_detalle'),



    #url(r'^experiencias.laborales/$', views.ExperienciaLaboralList.as_view()),
    #url(r'^experiencia.laboral/(?P<pk>[0-9]+)/$', views.ExperienciaLaboralDetail.as_view()),

    #url(r'^lineas.investigacion/$', views.LineaInvestigacionList.as_view()),
    #url(r'^linea.investigacion/(?P<pk>[0-9]+)/$', views.LineaInvestigacionDetail.as_view()),

    #url(r'^capacidades.potencialidades/$', views.CapacidadPotencialidadList.as_view()),
    #url(r'^capacidad.potencialidad/(?P<pk>[0-9]+)/$', views.CapacidadPotencialidadDetail.as_view()),

]
urlpatterns = format_suffix_patterns(urlpatterns)