"""Reglas del informe anual: a qué año pertenece un registro para efectos de cierre."""

from .models import EstadoPublicacion, PeriodoInforme, StatusPublicacion, es_sin_fecha


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
        fecha = obj.fecha if obj.status == StatusPublicacion.PUBLICADO else None
    elif hasattr(obj, 'fecha_inicio') and hasattr(obj, 'fecha_fin'):
        fecha = obj.fecha_fin
    elif campo_fecha:
        fecha = valor_ruta(obj, campo_fecha)
    else:
        fecha = None
    return fecha.year if fecha and not es_sin_fecha(fecha) else None  # "Sin fecha" (1900) no cae en ningún informe.


def esta_cerrado(obj, campo_fecha=None, anios_cerrados=None):
    anio = anio_cierre(obj, campo_fecha)
    if anio is None:
        return False
    cerrados = PeriodoInforme.anios_cerrados() if anios_cerrados is None else anios_cerrados
    return anio in cerrados
