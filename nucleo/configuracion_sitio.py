"""Valores de Unfold que dependen de la configuración de la entidad."""

from .models import ConfiguracionEntidad


def subtitulo(request):
    return str(ConfiguracionEntidad.actual(request))
