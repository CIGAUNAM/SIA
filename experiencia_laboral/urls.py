from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . views import *




urlpatterns = [

    url(r'^laborales/json/', ExperienciaLaboralJSON.as_view(), name='experiencia_laboral_lista__json'),
    url(r'^laborales/$', ExperienciaLaboralLista.as_view(), name='experiencia_laboral_lista'),
    url(r'^laborales/(?P<pk>[\w\-]+)/eliminar$', ExperienciaLaboralEliminar.as_view(), name='experiencia_laboral_eliminar'),
    url(r'^laborales/(?P<pk>[\w\-]+)/$', ExperienciaLaboralDetalle.as_view(), name='experiencia_laboral_detalle'),

    url(r'^lineas-investigacion/json/', LineaInvestigacionJSON.as_view(), name='linea_investigacion_lista__json'),
    url(r'^lineas-investigacion/$', LineaInvestigacionLista.as_view(), name='linea_investigacion_lista'),
    url(r'^lineas-investigacion/(?P<pk>[\w\-]+)/eliminar$', LineaInvestigacionEliminar.as_view(), name='linea_investigacion_eliminar'),
    url(r'^lineas-investigacion/(?P<pk>[\w\-]+)/$', LineaInvestigacionDetalle.as_view(), name='linea_investigacion_detalle'),

    url(r'^capacidades/json/', CapacidadPotencialidadJSON.as_view(), name='capacidad_potencialidad_lista__json'),
    url(r'^capacidades/$', CapacidadPotencialidadLista.as_view(), name='capacidad_potencialidad_lista'),
    url(r'^capacidades/(?P<pk>[\w\-]+)/eliminar$', CapacidadPotencialidadEliminar.as_view(), name='capacidad_potencialidad_eliminar'),
    url(r'^capacidades/(?P<pk>[\w\-]+)/$', CapacidadPotencialidadDetalle.as_view(), name='capacidad_potencialidad_detalle'),

]
urlpatterns = format_suffix_patterns(urlpatterns)