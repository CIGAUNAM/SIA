from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
# from nucleo import views
from .views import *

urlpatterns = [
    url(r'^paises/json/', PaisJSON.as_view(), name='pais_lista__json'),
    url(r'^paises/$', PaisLista.as_view(), name='pais_lista'),
    # url(r'^paises/(?P<pk>[\w\-]+)/eliminar$', PaisEliminar.as_view(), name='pais_eliminar'),
    url(r'^paises/(?P<pk>[\w\-]+)/$', PaisDetalle.as_view(), name='pais_detalle'),

    url(r'^estados/json/', EstadoJSON.as_view(), name='estado_lista__json'),
    url(r'^estados/$', EstadoLista.as_view(), name='estado_lista'),
    # url(r'^estados/(?P<pk>[\w\-]+)/eliminar$', EstadoEliminar.as_view(), name='estado_eliminar'),
    url(r'^estados/(?P<pk>[\w\-]+)/$', EstadoDetalle.as_view(), name='estado_detalle'),

    url(r'^ciudades/json/', CiudadJSON.as_view(), name='ciudad_lista__json'),
    url(r'^ciudades/$', CiudadLista.as_view(), name='ciudad_lista'),
    # url(r'^ciudades/(?P<pk>[\w\-]+)/eliminar$', CiudadEliminar.as_view(), name='ciudad_eliminar'),
    url(r'^ciudades/(?P<pk>[\w\-]+)/$', CiudadDetalle.as_view(), name='ciudad_detalle'),

    url(r'^instituciones/json/', InstitucionJSON.as_view(), name='institucion_lista__json'),
    url(r'^instituciones/$', InstitucionLista.as_view(), name='institucion_lista'),
    # url(r'^instituciones/(?P<pk>[\w\-]+)/eliminar$', InstitucionEliminar.as_view(), name='institucion_eliminar'),
    url(r'^instituciones/(?P<pk>[\w\-]+)/$', InstitucionDetalle.as_view(), name='institucion_detalle'),

    url(r'^dependencias/json/', DependenciaJSON.as_view(), name='dependencia_lista__json'),
    url(r'^dependencias/$', DependenciaLista.as_view(), name='dependencia_lista'),
    # url(r'^dependencias/(?P<pk>[\w\-]+)/eliminar$', DependenciaEliminar.as_view(), name='dependencia_eliminar'),
    url(r'^dependencias/(?P<pk>[\w\-]+)/$', DependenciaDetalle.as_view(), name='dependencia_detalle'),

    url(r'^departamentos/json/', DepartamentoJSON.as_view(), name='departamento_lista__json'),
    url(r'^departamentos/$', DepartamentoLista.as_view(), name='departamento_lista'),
    # url(r'^departamentos/(?P<pk>[\w\-]+)/eliminar$', DepartamentoEliminar.as_view(), name='departamento_eliminar'),
    url(r'^departamentos/(?P<pk>[\w\-]+)/$', DepartamentoDetalle.as_view(), name='departamento_detalle'),

    url(r'^cargos/json/', CargoJSON.as_view(), name='cargo_lista__json'),
    url(r'^cargos/$', CargoLista.as_view(), name='cargo_lista'),
    # url(r'^cargos/(?P<pk>[\w\-]+)/eliminar$', CargoEliminar.as_view(), name='cargo_eliminar'),
    url(r'^cargos/(?P<pk>[\w\-]+)/$', CargoDetalle.as_view(), name='cargo_detalle'),

    url(r'^areas-especialidad/json/', AreaEspecialidadJSON.as_view(), name='area_especialidad_lista__json'),
    url(r'^areas-especialidad/$', AreaEspecialidadLista.as_view(), name='area_especialidad_lista'),
    # url(r'^areas-especialidad/(?P<pk>[\w\-]+)/eliminar$', AreaEspecialidadEliminar.as_view(), name='area_especialidad_eliminar'),
    url(r'^areas-especialidad/(?P<pk>[\w\-]+)/$', AreaEspecialidadDetalle.as_view(), name='area_especialidad_detalle'),

    url(r'^impactos-sociales/json/', ImpactoSocialJSON.as_view(), name='impacto_social_lista__json'),
    url(r'^impactos-sociales/$', ImpactoSocialLista.as_view(), name='impacto_social_lista'),
    # url(r'^impactos-sociales/(?P<pk>[\w\-]+)/eliminar$', ImpactoSocialEliminar.as_view(), name='impacto_social_eliminar'),
    url(r'^impactos-sociales/(?P<pk>[\w\-]+)/$', ImpactoSocialDetalle.as_view(), name='impacto_social_detalle'),

    url(r'^financiamientos/json/', FinanciamientoJSON.as_view(), name='financiamiento_lista__json'),
    url(r'^financiamientos/$', FinanciamientoLista.as_view(), name='financiamiento_lista'),
    # url(r'^financiamientos/(?P<pk>[\w\-]+)/eliminar$', FinanciamientoEliminar.as_view(), name='financiamiento_eliminar'),
    url(r'^financiamientos/(?P<pk>[\w\-]+)/$', FinanciamientoDetalle.as_view(), name='financiamiento_detalle'),

    url(r'^metodologias/json/', MetodologiaJSON.as_view(), name='metodologia_lista__json'),
    url(r'^metodologias/$', MetodologiaLista.as_view(), name='metodologia_lista'),
    # url(r'^metodologias/(?P<pk>[\w\-]+)/eliminar$', MetodologiaEliminar.as_view(), name='metodologia_eliminar'),
    url(r'^metodologias/(?P<pk>[\w\-]+)/$', MetodologiaDetalle.as_view(), name='metodologia_detalle'),

    url(r'^becas/json/', BecaJSON.as_view(), name='beca_lista__json'),
    url(r'^becas/$', BecaLista.as_view(), name='beca_lista'),
    # url(r'^becas/(?P<pk>[\w\-]+)/eliminar$', BecaEliminar.as_view(), name='beca_eliminar'),
    url(r'^becas/(?P<pk>[\w\-]+)/$', BecaDetalle.as_view(), name='beca_detalle'),

    url(r'^reconocimientos/json/', ReconocimientoJSON.as_view(), name='reconocimiento_lista__json'),
    url(r'^reconocimientos/$', ReconocimientoLista.as_view(), name='reconocimiento_lista'),
    # url(r'^reconocimientos/(?P<pk>[\w\-]+)/eliminar$', ReconocimientoEliminar.as_view(), name='reconocimiento_eliminar'),
    url(r'^reconocimientos/(?P<pk>[\w\-]+)/$', ReconocimientoDetalle.as_view(), name='reconocimiento_detalle'),

    url(r'^programas-licenciatura/json/', ProgramaLicenciaturaJSON.as_view(), name='programa_licenciatura_lista__json'),
    url(r'^programas-licenciatura/$', ProgramaLicenciaturaLista.as_view(), name='programa_licenciatura_lista'),
    # url(r'^programas-licenciatura/(?P<pk>[\w\-]+)/eliminar$', ProgramaLicenciaturaEliminar.as_view(), name='programa_licenciatura_eliminar'),
    url(r'^programas-licenciatura/(?P<pk>[\w\-]+)/$', ProgramaLicenciaturaDetalle.as_view(), name='programa_licenciatura_detalle'),

    url(r'^programas-maestria/json/', ProgramaMaestriaJSON.as_view(), name='programa_maestria_lista__json'),
    url(r'^programas-maestria/$', ProgramaMaestriaLista.as_view(), name='programa_maestria_lista'),
    # url(r'^programas-maestria/(?P<pk>[\w\-]+)/eliminar$', ProgramaMaestriaEliminar.as_view(), name='programa_maestria_eliminar'),
    url(r'^programas-maestria/(?P<pk>[\w\-]+)/$', ProgramaMaestriaDetalle.as_view(), name='programa_maestria_detalle'),

    url(r'^programas-doctorado/json/', ProgramaDoctoradoJSON.as_view(), name='programa_doctorado_lista__json'),
    url(r'^programas-doctorado/$', ProgramaDoctoradoLista.as_view(), name='programa_doctorado_lista'),
    # url(r'^programas-doctorado/(?P<pk>[\w\-]+)/eliminar$', ProgramaDoctoradoEliminar.as_view(), name='programa_doctorado_eliminar'),
    url(r'^programas-doctorado/(?P<pk>[\w\-]+)/$', ProgramaDoctoradoDetalle.as_view(), name='programa_doctorado_detalle'),

    url(r'^tipos-evento/json/', TipoEventoJSON.as_view(), name='tipo_evento_lista__json'),
    url(r'^tipos-evento/$', TipoEventoLista.as_view(), name='tipo_evento_lista'),
    # url(r'^tipos-evento/(?P<pk>[\w\-]+)/eliminar$', TipoEventoEliminar.as_view(), name='tipo_evento_eliminar'),
    url(r'^tipos-evento/(?P<pk>[\w\-]+)/$', TipoEventoDetalle.as_view(), name='tipo_evento_detalle'),

    url(r'^eventos/json/', EventoJSON.as_view(), name='evento_lista__json'),
    url(r'^eventos/$', EventoLista.as_view(), name='evento_lista'),
    # url(r'^eventos/(?P<pk>[\w\-]+)/eliminar$', EventoEliminar.as_view(), name='evento_eliminar'),
    url(r'^eventos/(?P<pk>[\w\-]+)/$', EventoDetalle.as_view(), name='evento_detalle'),

    url(r'^distinciones/json/', DistincionJSON.as_view(), name='distincion_lista__json'),
    url(r'^distinciones/$', DistincionLista.as_view(), name='distincion_lista'),
    # url(r'^distinciones/(?P<pk>[\w\-]+)/eliminar$', DistincionEliminar.as_view(), name='distincion_eliminar'),
    url(r'^distinciones/(?P<pk>[\w\-]+)/$', DistincionDetalle.as_view(), name='distincion_detalle'),

    url(r'^proyectos/json/', ProyectoJSON.as_view(), name='proyecto_lista__json'),
    url(r'^proyectos/$', ProyectoLista.as_view(), name='proyecto_lista'),
    # url(r'^proyectos/(?P<pk>[\w\-]+)/eliminar$', ProyectoEliminar.as_view(), name='proyecto_eliminar'),
    url(r'^proyectos/(?P<pk>[\w\-]+)/$', ProyectoDetalle.as_view(), name='proyecto_detalle'),

    url(r'^memorias/json/', MemoriaJSON.as_view(), name='memoria_lista__json'),
    url(r'^memorias/$', MemoriaLista.as_view(), name='memoria_lista'),
    # url(r'^memorias/(?P<pk>[\w\-]+)/eliminar$', MemoriaEliminar.as_view(), name='memoria_eliminar'),
    url(r'^memorias/(?P<pk>[\w\-]+)/$', MemoriaDetalle.as_view(), name='memoria_detalle'),

    url(r'^editoriales/json/', EditorialJSON.as_view(), name='editorial_lista__json'),
    url(r'^editoriales/$', EditorialLista.as_view(), name='editorial_lista'),
    # url(r'^editoriales/(?P<pk>[\w\-]+)/eliminar$', EditorialEliminar.as_view(), name='editorial_eliminar'),
    url(r'^editoriales/(?P<pk>[\w\-]+)/$', EditorialDetalle.as_view(), name='editorial_detalle'),

    url(r'^colecciones/json/', ColeccionJSON.as_view(), name='coleccion_lista__json'),
    url(r'^colecciones/$', ColeccionLista.as_view(), name='coleccion_lista'),
    # url(r'^colecciones/(?P<pk>[\w\-]+)/eliminar$', ColeccionEliminar.as_view(), name='coleccion_eliminar'),
    url(r'^colecciones/(?P<pk>[\w\-]+)/$', ColeccionDetalle.as_view(), name='coleccion_detalle'),

    url(r'^libros/json/', LibroJSON.as_view(), name='libro_lista__json'),
    url(r'^libros/$', LibroLista.as_view(), name='libro_lista'),
    # url(r'^libros/(?P<pk>[\w\-]+)/eliminar$', LibroEliminar.as_view(), name='libro_eliminar'),
    url(r'^libros/(?P<pk>[\w\-]+)/$', LibroDetalle.as_view(), name='libro_detalle'),

    url(r'^revistas/json/', RevistaJSON.as_view(), name='revista_lista__json'),
    url(r'^revistas/$', RevistaLista.as_view(), name='revista_lista'),
    # url(r'^revistas/(?P<pk>[\w\-]+)/eliminar$', RevistaEliminar.as_view(), name='revista_eliminar'),
    url(r'^revistas/(?P<pk>[\w\-]+)/$', RevistaDetalle.as_view(), name='revista_detalle'),

    url(r'^asignaturas/json/', AsignaturaJSON.as_view(), name='asignatura_lista__json'),
    url(r'^asignaturas/$', AsignaturaLista.as_view(), name='asignatura_lista'),
    # url(r'^asignaturas/(?P<pk>[\w\-]+)/eliminar$', AsignaturaEliminar.as_view(), name='asignatura_eliminar'),
    url(r'^asignaturas/(?P<pk>[\w\-]+)/$', AsignaturaDetalle.as_view(), name='asignatura_detalle'),

    url(r'^medios-divulgacion/json/', MedioDivulgacionJSON.as_view(), name='medio_divulgacion_lista__json'),
    url(r'^medios-divulgacion/$', MedioDivulgacionLista.as_view(), name='medio_divulgacion_lista'),
    # url(r'^medios-divulgacion/(?P<pk>[\w\-]+)/eliminar$', MedioDivulgacionEliminar.as_view(), name='medio_divulgacion_eliminar'),
    url(r'^medios-divulgacion/(?P<pk>[\w\-]+)/$', MedioDivulgacionDetalle.as_view(), name='medio_divulgacion_detalle'),







    # url(r'^rest/tags/$', views.TagList.as_view()),
    # url(r'^rest/tag/(?P<pk>[0-9]+)/$', views.TagDetail.as_view()),
    # url(r'^rest/zonas.paises/$', views.ZonaPaisList.as_view()),
    # url(r'^rest/zona.pais/(?P<pk>[0-9]+)/$', views.ZonaPaisDetail.as_view()),
    # url(r'^rest/paises/$', views.PaisList.as_view()),
    # url(r'^rest/pais/(?P<pk>[0-9]+)/$', views.PaisDetail.as_view()),
    # url(r'^rest/estados/$', views.EstadoList.as_view()),
    # url(r'^rest/estado/(?P<pk>[0-9]+)/$', views.EstadoDetail.as_view()),
    # url(r'^rest/ciudades/$', views.CiudadList.as_view()),
    # url(r'^rest/ciudad/(?P<pk>[0-9]+)/$', views.CiudadDetail.as_view()),
    # url(r'^rest/users/$', views.UserList.as_view()),
    # url(r'^rest/user/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    # url(r'^rest/instituciones/$', views.InstitucionList.as_view()),
    # url(r'^rest/institucion/(?P<pk>[0-9]+)/$', views.InstitucionDetail.as_view()),
    # url(r'^rest/dependencias/$', views.DependenciaList.as_view()),
    # url(r'^rest/dependencia/(?P<pk>[0-9]+)/$', views.DependenciaDetail.as_view()),
    # url(r'^rest/cargos/$', views.CargoList.as_view()),
    # url(r'^rest/nombre/(?P<pk>[0-9]+)/$', views.CargoDetail.as_view()),
    # url(r'^rest/nombramientos/$', views.NombramientoList.as_view()),
    # url(r'^rest/nombramientos/(?P<pk>[0-9]+)/$', views.NombramientoDetail.as_view()),
    # url(r'^rest/areas.conocimiento/$', views.AreaConocimientoList.as_view()),
    # url(r'^rest/area.conocimiento/(?P<pk>[0-9]+)/$', views.AreaConocimientoDetail.as_view()),
    # url(r'^rest/areas.especialidad/$', views.AreaEspecialidadList.as_view()),
    # url(r'^rest/area.especialidad/(?P<pk>[0-9]+)/$', views.AreaEspecialidadDetail.as_view()),
    # url(r'^rest/impactos.sociales/$', views.ImpactoSocialList.as_view()),
    # url(r'^rest/impacto.social/(?P<pk>[0-9]+)/$', views.ImpactoSocialDetail.as_view()),
    # url(r'^rest/programas.financiamiento/$', views.ProgramaFinanciamientoList.as_view()),
    # url(r'^rest/programa.financiamiento/(?P<pk>[0-9]+)/$', views.ProgramaFinanciamientoDetail.as_view()),
    # url(r'^rest/financiamientos/$', views.FinanciamientoList.as_view()),
    # url(r'^rest/financiamiento/(?P<pk>[0-9]+)/$', views.FinanciamientoDetail.as_view()),
    # url(r'^rest/metodologias/$', views.MetodologiaList.as_view()),
    # url(r'^rest/metodologia/(?P<pk>[0-9]+)/$', views.MetodologiaDetail.as_view()),
    # url(r'^rest/programas.licenciatura/$', views.ProgramaLicenciaturaList.as_view()),
    # url(r'^rest/programa.licenciatura/(?P<pk>[0-9]+)/$', views.ProgramaLicenciaturaDetail.as_view()),
    # url(r'^rest/programas.maestria/$', views.ProgramaMaestriaList.as_view()),
    # url(r'^rest/programa.maestria/(?P<pk>[0-9]+)/$', views.ProgramaMaestriaDetail.as_view()),
    # url(r'^rest/programas.doctorado/$', views.ProgramaDoctoradoList.as_view()),
    # url(r'^rest/programa.doctorado/(?P<pk>[0-9]+)/$', views.ProgramaDoctoradoDetail.as_view()),
    # url(r'^rest/proyectos/$', views.ProyectoList.as_view()),
    # url(r'^rest/proyecto/(?P<pk>[0-9]+)/$', views.ProyectoDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
