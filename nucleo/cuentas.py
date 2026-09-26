"""Recuperación de contraseña por correo, con el estilo del admin (Unfold)."""

from django.contrib import admin
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import views as auth_views
from unfold.widgets import INPUT_CLASSES

from .models import ConfiguracionEntidad

CLASES = ' '.join(INPUT_CLASSES)


class ConContextoAdmin:
    titulo = ''

    def get_context_data(self, **kwargs):
        return {**admin.site.each_context(self.request), **super().get_context_data(**kwargs), 'title': self.titulo}


class FormularioCorreo(auth_forms.PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = CLASES


class FormularioNuevaContrasena(auth_forms.SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            campo.widget.attrs['class'] = CLASES


class SolicitarRecuperacion(ConContextoAdmin, auth_views.PasswordResetView):
    titulo = 'Recuperar contraseña'
    form_class = FormularioCorreo
    template_name = 'registration/sia/solicitar.html'
    email_template_name = 'registration/sia/correo.txt'
    subject_template_name = 'registration/sia/asunto.txt'

    def form_valid(self, form):
        entidad = ConfiguracionEntidad.actual(self.request)
        self.from_email = entidad.remitente_correos
        self.extra_email_context = {'entidad': entidad}
        return super().form_valid(form)


class RecuperacionEnviada(ConContextoAdmin, auth_views.PasswordResetDoneView):
    titulo = 'Revisa tu correo'
    template_name = 'registration/sia/mensaje.html'


class NuevaContrasena(ConContextoAdmin, auth_views.PasswordResetConfirmView):
    titulo = 'Nueva contraseña'
    form_class = FormularioNuevaContrasena
    template_name = 'registration/sia/nueva.html'


class ContrasenaCambiada(ConContextoAdmin, auth_views.PasswordResetCompleteView):
    titulo = 'Contraseña actualizada'
    template_name = 'registration/sia/mensaje.html'
