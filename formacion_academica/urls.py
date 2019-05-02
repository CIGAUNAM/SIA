from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . views import *

urlpatterns = [

    url(r'^cursos-especializacion/json/', CursoEspecializacionJSON.as_view(), name='curso_especializacion_lista__json'),
    url(r'^cursos-especializacion/$', CursoEspecializacionLista.as_view(), name='curso_especializacion_lista'),
    url(r'^cursos-especializacion/(?P<pk>[\w\-]+)/eliminar$', CursoEspecializacionEliminar.as_view(), name='curso_especializacion_eliminar'),
    url(r'^cursos-especializacion/(?P<pk>[\w\-]+)/$', CursoEspecializacionDetalle.as_view(), name='curso_especializacion_detalle'),

    url(r'^licenciaturas/json/', LicenciaturaJSON.as_view(), name='licenciatura_lista__json'),
    url(r'^licenciaturas/$', LicenciaturaLista.as_view(), name='licenciatura_lista'),
    url(r'^licenciaturas/(?P<pk>[\w\-]+)/eliminar$', LicenciaturaEliminar.as_view(), name='licenciatura_eliminar'),
    url(r'^licenciaturas/(?P<pk>[\w\-]+)/$', LicenciaturaDetalle.as_view(), name='licenciatura_detalle'),

    url(r'^maestrias/json/', MaestriaJSON.as_view(), name='maestria_lista__json'),
    url(r'^maestrias/$', MaestriaLista.as_view(), name='maestria_lista'),
    url(r'^maestrias/(?P<pk>[\w\-]+)/eliminar$', MaestriaEliminar.as_view(), name='maestria_eliminar'),
    url(r'^maestrias/(?P<pk>[\w\-]+)/$', MaestriaDetalle.as_view(), name='maestria_detalle'),

    url(r'^doctorados/json/', DoctoradoJSON.as_view(), name='doctorado_lista__json'),
    url(r'^doctorados/$', DoctoradoLista.as_view(), name='doctorado_lista'),
    url(r'^doctorados/(?P<pk>[\w\-]+)/eliminar$', DoctoradoEliminar.as_view(), name='doctorado_eliminar'),
    url(r'^doctorados/(?P<pk>[\w\-]+)/$', DoctoradoDetalle.as_view(), name='doctorado_detalle'),

    url(r'^postdoctorados/json/', PostDoctoradoJSON.as_view(), name='postdoctorado_lista__json'),
    url(r'^postdoctorados/$', PostDoctoradoLista.as_view(), name='postdoctorado_lista'),
    url(r'^postdoctorados/(?P<pk>[\w\-]+)/eliminar$', PostDoctoradoEliminar.as_view(), name='postdoctorado_eliminar'),
    url(r'^postdoctorados/(?P<pk>[\w\-]+)/$', PostDoctoradoDetalle.as_view(), name='postdoctorado_detalle'),

]

urlpatterns = format_suffix_patterns(urlpatterns)




