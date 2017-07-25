from django.conf.urls import url
from . views import *

urlpatterns = [

    url(r'^cargos-academico-administrativos/json/', CargoAcademicoAdministrativoJSON.as_view(), name='cargo_academico_administrativo_lista__json'),
    url(r'^cargos-academico-administrativos/$', CargoAcademicoAdministrativoLista.as_view(), name='cargo_academico_administrativo_lista'),
    url(r'^cargos-academico-administrativos/(?P<pk>[\w\-]+)/eliminar$', CargoAcademicoAdministrativoEliminar.as_view(), name='cargo_academico_administrativo_eliminar'),
    url(r'^cargos-academico-administrativos/(?P<pk>[\w\-]+)/$', CargoAcademicoAdministrativoDetalle.as_view(), name='cargo_academico_administrativo_detalle'),

    url(r'^representaciones-organos-colegiados/json/', RepresentacionOrganoColegiadoJSON.as_view(), name='representacion_organo_colegiado_lista__json'),
    url(r'^representaciones-organos-colegiados/$', RepresentacionOrganoColegiadoLista.as_view(), name='representacion_organo_colegiado_lista'),
    url(r'^representaciones-organos-colegiados/(?P<pk>[\w\-]+)/eliminar$', RepresentacionOrganoColegiadoEliminar.as_view(), name='representacion_organo_colegiado_eliminar'),
    url(r'^representaciones-organos-colegiados/(?P<pk>[\w\-]+)/$', RepresentacionOrganoColegiadoDetalle.as_view(), name='representacion_organo_colegiado_detalle'),

    url(r'^comisiones-academicas/json/', ComisionAcademicaJSON.as_view(), name='comision_academica_lista__json'),
    url(r'^comisiones-academicas/$', ComisionAcademicaLista.as_view(), name='comision_academica_lista'),
    url(r'^comisiones-academicas/(?P<pk>[\w\-]+)/eliminar$', ComisionAcademicaEliminar.as_view(), name='comision_academica_eliminar'),
    url(r'^comisiones-academicas/(?P<pk>[\w\-]+)/$', ComisionAcademicaDetalle.as_view(), name='comision_academica_detalle'),

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

    url(r'^comisiones/json/', ComisionJSON.as_view(), name='comision_lista__json'),
    url(r'^comisiones/$', ComisionLista.as_view(), name='comision_lista'),
    # url(r'^comisiones/(?P<pk>[\w\-]+)/eliminar$', ComisionEliminar.as_view(), name='comision_eliminar'),
    url(r'^comisiones/(?P<pk>[\w\-]+)/$', ComisionDetalle.as_view(), name='comision_detalle'),

    url(r'^actividades-apoyo/json/', ActividadApoyoJSON.as_view(), name='actividad_apoyo_lista__json'),
    url(r'^actividades-apoyo/$', ActividadApoyoLista.as_view(), name='actividad_apoyo_lista'),
    # url(r'^actividades-apoyo/(?P<pk>[\w\-]+)/eliminar$', ActividadApoyoEliminar.as_view(), name='actividad_apoyo_eliminar'),
    url(r'^actividades-apoyo/(?P<pk>[\w\-]+)/$', ActividadApoyoDetalle.as_view(), name='actividad_apoyo_detalle'),

]