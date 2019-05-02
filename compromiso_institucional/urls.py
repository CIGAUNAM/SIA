from django.conf.urls import url
from . views import *

urlpatterns = [

    url(r'^labores-directivas-coordinacion/json/', LaborDirectivaCoordinacionJSON.as_view(), name='labor_directiva_coordinacion_lista__json'),
    url(r'^labores-directivas-coordinacion/$', LaborDirectivaCoordinacionLista.as_view(), name='labor_directiva_coordinacion_lista'),
    url(r'^labores-directivas-coordinacion/(?P<pk>[\w\-]+)/eliminar$', LaborDirectivaCoordinacionEliminar.as_view(), name='labor_directiva_coordinacion_eliminar'),
    url(r'^labores-directivas-coordinacion/(?P<pk>[\w\-]+)/$', LaborDirectivaCoordinacionDetalle.as_view(), name='labor_directiva_coordinacion_detalle'),

    url(r'^representaciones-organos-colegiados-unam/json/', RepresentacionOrganoColegiadoJSON.as_view(), name='representacion_organo_colegiado_unam_lista__json'),
    url(r'^representaciones-organos-colegiados-unam/$', RepresentacionOrganoColegiadoLista.as_view(), name='representacion_organo_colegiado_unam_lista'),
    url(r'^representaciones-organos-colegiados-unam/(?P<pk>[\w\-]+)/eliminar$', RepresentacionOrganoColegiadoEliminar.as_view(), name='representacion_organo_colegiado_unam_eliminar'),
    url(r'^representaciones-organos-colegiados-unam/(?P<pk>[\w\-]+)/$', RepresentacionOrganoColegiadoDetalle.as_view(), name='representacion_organo_colegiado_unam_detalle'),

    url(r'^comisiones-institucionales-ciga/json/', ComisionAcademicaJSON.as_view(), name='comision_institucional_lista__json'),
    url(r'^comisiones-institucionales-ciga/$', ComisionAcademicaLista.as_view(), name='comision_institucional_lista'),
    url(r'^comisiones-institucionales-ciga/(?P<pk>[\w\-]+)/eliminar$', ComisionAcademicaEliminar.as_view(), name='comision_institucional_eliminar'),
    url(r'^comisiones-institucionales-ciga/(?P<pk>[\w\-]+)/$', ComisionAcademicaDetalle.as_view(), name='comision_institucional_detalle'),

    url(r'^apoyos-tecnicos/json/', ApoyoTecnicoJSON.as_view(), name='apoyo_tecnico_lista__json'),
    url(r'^apoyos-tecnicos/$', ApoyoTecnicoLista.as_view(), name='apoyo_tecnico_lista'),
    url(r'^apoyos-tecnicos/(?P<pk>[\w\-]+)/eliminar$', ApoyoTecnicoEliminar.as_view(), name='apoyo_tecnico_eliminar'),
    url(r'^apoyos-tecnicos/(?P<pk>[\w\-]+)/$', ApoyoTecnicoDetalle.as_view(), name='apoyo_tecnico_detalle'),

    url(r'^otras-actividades/json/', ApoyoOtraActividadJSON.as_view(), name='apoyo_otra_actividad_lista__json'),
    url(r'^otras-actividades/$', ApoyoOtraActividadLista.as_view(), name='apoyo_otra_actividad_lista'),
    url(r'^otras-actividades/(?P<pk>[\w\-]+)/eliminar$', ApoyoOtraActividadEliminar.as_view(), name='apoyo_otra_actividad_eliminar'),
    url(r'^otras-actividades/(?P<pk>[\w\-]+)/$', ApoyoOtraActividadDetalle.as_view(), name='apoyo_otra_actividad_detalle'),

    url(r'^representaciones/json/', RepresentacionJSON.as_view(), name='representacion_lista__json'),
    url(r'^representaciones/$', RepresentacionLista.as_view(), name='representacion_lista'),
    # url(r'^representaciones/(?P<pk>[\w\-]+)/eliminar$', RepresentacionEliminar.as_view(), name='representacion_eliminar'),
    url(r'^representaciones/(?P<pk>[\w\-]+)/$', RepresentacionDetalle.as_view(), name='representacion_detalle'),

    url(r'^comisiones-institucionales/json/', ComisionJSON.as_view(), name='comisioninstitucional_lista__json'),
    url(r'^comisiones-institucionales/$', ComisionLista.as_view(), name='comisioninstitucional_lista'),
    # url(r'^comisiones/(?P<pk>[\w\-]+)/eliminar$', ComisionEliminar.as_view(), name='comision_eliminar'),
    url(r'^comisiones-institucionales/(?P<pk>[\w\-]+)/$', ComisionDetalle.as_view(), name='comisioninstitucional_detalle'),

    url(r'^actividades-apoyo/json/', ActividadApoyoJSON.as_view(), name='actividad_apoyo_lista__json'),
    url(r'^actividades-apoyo/$', ActividadApoyoLista.as_view(), name='actividad_apoyo_lista'),
    # url(r'^actividades-apoyo/(?P<pk>[\w\-]+)/eliminar$', ActividadApoyoEliminar.as_view(), name='actividad_apoyo_eliminar'),
    url(r'^actividades-apoyo/(?P<pk>[\w\-]+)/$', ActividadApoyoDetalle.as_view(), name='actividad_apoyo_detalle'),

]