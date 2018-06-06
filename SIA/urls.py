"""SIA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from django.contrib.auth import views as auth_views

#from nucleo.views import inicio
from nucleo.views import *
from django.conf.urls.static import static
from django.conf.urls import url
from SIA.views import *



urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'adminlte/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'adminlte/login.html'}, name='logout'),

    #url(r'^password_change/$', auth_views.password_change, name='password_change'),
    #url(r'^password_change/done/$', auth_views.password_change_done, name='password_change_done'),
    #url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    #url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),

    url(r'^formacion-academica/', include('formacion_academica.urls')),
    url(r'^experiencia/', include('experiencia_laboral.urls')),
    url(r'^investigacion/', include('investigacion.urls')),
    url(r'^difusion-cientifica/', include('difusion_cientifica.urls')),
    url(r'^divulgacion-cientifica/', include('divulgacion_cientifica.urls')),
    url(r'^vinculacion/', include('vinculacion.urls')),
    url(r'^docencia/', include('docencia.urls')),
    url(r'^apoyo-institucional/', include('apoyo_institucional.urls')),
    url(r'^movilidad-academica/', include('movilidad_academica.urls')),
    url(r'^formacion-recursos-humanos/', include('formacion_recursos_humanos.urls')),
    url(r'^desarrollos-tecnologicos/', include('desarrollo_tecnologico.urls')),
    url(r'^distinciones/', include('distinciones.urls')),
    url(r'^formatos/', include('formatos.urls')),
    url(r'^nucleo/', include('nucleo.urls')),

    url(r'^web/cv-investigadores/$', CVInvestigadorLista.as_view(), name='cv_investigador_lista'),
    url(r'^web/cv-investigadores/(?P<pk>[\w\-]+)/$', CVInvestigadorDetalle.as_view(), name='cv_investigador_detalle'),
    url(r'^web/cv-investigadores/(?P<pk>[\w\-]+)/pdf/$', CVInvestigadorPDF.as_view(), name='cv_investigador_detalle'),

    url(r'^web/publicaciones/$', WebPublicacionLista.as_view(), name='web_publicacion_lista'),
    url(r'^web/publicaciones/(?P<pk>[\w\-]+)/$', WebPublicacionDetalle.as_view(), name='web_publicacion_detalle'),

    url(r'^web/articulos/$', WebArticuloLista.as_view(), name='web_articulo_lista'),
    url(r'^web/articulos/(?P<pk>[\w\-]+)/$', WebArticuloDetalle.as_view(), name='web_articulo_detalle'),

    url(r'^web/proyectos/$', WebProyectoLista.as_view(), name='web_proyecto_lista'),
    url(r'^web/proyectos/(?P<pk>[\w\-]+)/$', WebProyectoDetalle.as_view(), name='web_proyecto_detalle'),



    url(r'^web/proyectos-actuales', PerfilUsuario.as_view(), name='perfil_usuario'),

    url(r'^perfil-usuario/$', PerfilUsuario.as_view(), name='perfil_usuario'),

    url(r'^reportes/historico$', ReporteHistorico.as_view(), name='reporte_historico'),
    url(r'^reportes/informe-actividades$', InformeActividades.as_view(), name='informe_actividades'),


    url(r'^admin/', admin.site.urls),
    url(r'^select2/', include('django_select2.urls')),
    url(r'^$', Dashboard.as_view(), name='dashboard'),
    url('^', include('django.contrib.auth.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

