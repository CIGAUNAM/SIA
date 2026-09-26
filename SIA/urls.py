from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

from nucleo import cuentas

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='admin:index', permanent=False)),
    path('admin/recuperar/', cuentas.SolicitarRecuperacion.as_view(), name='admin_password_reset'),
    path('admin/recuperar/enviado/', cuentas.RecuperacionEnviada.as_view(), name='password_reset_done'),
    path('admin/recuperar/<uidb64>/<token>/', cuentas.NuevaContrasena.as_view(), name='password_reset_confirm'),
    path('admin/recuperar/listo/', cuentas.ContrasenaCambiada.as_view(), name='password_reset_complete'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
