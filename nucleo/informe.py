"""Reglas del informe anual: a qué año pertenece un registro para efectos de cierre."""

from .models import EstadoPublicacion, PeriodoInforme, StatusPublicacion


def valor_ruta(obj, ruta):
    """Sigue una ruta tipo `libro__fecha_publicado` a partir de `obj`."""
    for parte in ruta.split('__'):
        obj = getattr(obj, parte, None)
        if obj is None:
            return None
    return obj


def anio_cierre(obj, campo_fecha=None):
    """Año que "fija" el registro en un informe, o None si sigue abierto.

    - Publicaciones: el año de publicación, solo cuando ya están publicadas.
    - Actividades con periodo: el año de término, solo cuando ya terminaron.
    - Registros con una sola fecha: el año de esa fecha (`campo_fecha`).
    """
    if isinstance(obj, EstadoPublicacion):
        return obj.fecha.year if obj.status == StatusPublicacion.PUBLICADO and obj.fecha else None
    if hasattr(obj, 'fecha_inicio') and hasattr(obj, 'fecha_fin'):
        return obj.fecha_fin.year if obj.fecha_fin else None
    if campo_fecha:
        fecha = valor_ruta(obj, campo_fecha)
        return fecha.year if fecha else None
    return None


def esta_cerrado(obj, campo_fecha=None, anios_cerrados=None):
    anio = anio_cierre(obj, campo_fecha)
    if anio is None:
        return False
    cerrados = PeriodoInforme.anios_cerrados() if anios_cerrados is None else anios_cerrados
    return anio in cerrados
