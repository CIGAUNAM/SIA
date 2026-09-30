"""Ver por académico: un administrador acota las listas de producción a los registros de un académico.

No es suplantar: sigue siendo él (sus permisos, su nombre en el historial); solo cambia qué registros ve. La
elección vive en la sesión y se muestra en una franja arriba de cada página (`admin/base_site.html`).
"""

from .models import User

SESION = 'sia_ver_academico'


def academico_acotado(request):
    """El académico elegido por un administrador, o None."""
    from .admin_base import es_administrador

    usuario = getattr(request, 'user', None)
    pk = getattr(request, 'session', {}).get(SESION)
    if not pk or usuario is None or not usuario.is_authenticated or not es_administrador(usuario):
        return None
    if not hasattr(request, '_academico_acotado'):
        request._academico_acotado = User.objects.select_related('persona').filter(pk=pk, is_active=True).first()
    return request._academico_acotado


def contexto(request):
    """Procesador de contexto: la franja "Viendo la producción de..." en todas las páginas del admin."""
    return {'academico_acotado': academico_acotado(request)}
