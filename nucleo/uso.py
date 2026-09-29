"""Quién usa un registro de catálogo compartido (persona, institución, revista...).

Define quién puede editarlo: si nadie lo usa, cualquiera; si lo usa una sola cuenta, solo esa; si lo usan varias,
solo la administración (ver `CompartidoAdmin`).
"""

from dataclasses import dataclass, field

from django.contrib import admin

from .fusion import relaciones_hacia

PROFUNDIDAD = 3  # Catálogos que usan catálogos (p. ej. una dependencia usa a su institución): hasta este nivel.


@dataclass
class Uso:
    registros: int = 0  # Registros que apuntan al catálogo.
    usuarios: set = field(default_factory=set)  # Cuentas dueñas de esos registros.


def _rutas_a_cuentas(modelo):
    """Lookups que llevan de un registro de `modelo` a las cuentas que lo usan; None si es un catálogo."""
    from .admin_base import PropietarioAdmin
    from .models import Participante, User

    if modelo is User:
        return ['pk']  # La cuenta de una persona usa a esa persona.
    model_admin = admin.site._registry.get(modelo)
    if isinstance(model_admin, PropietarioAdmin):
        return list(model_admin.propietarios)
    if issubclass(modelo, Participante):
        # Tabla intermedia (autores, tutores...): la usan la persona participante y los dueños del registro padre.
        rutas = ['persona__usuario']
        for campo in modelo._meta.concrete_fields:
            if campo.is_relation and campo.name != 'persona':
                rutas += [f'{campo.name}__{r}' for r in (_rutas_a_cuentas(campo.related_model) or [])]
        return rutas
    return None


def uso(obj, _profundidad=PROFUNDIDAD, _vistos=None):
    """Cuántos registros usan `obj` y qué cuentas son sus dueñas (sin el historial ni las evidencias)."""
    vistos = _vistos if _vistos is not None else set()
    vistos.add((type(obj), obj.pk))
    resultado = Uso()
    for modelo, campo in relaciones_hacia(type(obj)):
        registros = modelo._default_manager.filter(**{campo.name: obj})
        resultado.registros += registros.count()
        rutas = _rutas_a_cuentas(modelo)
        if rutas is not None:
            for ruta in rutas:
                resultado.usuarios.update(u for u in registros.values_list(ruta, flat=True) if u is not None)
        elif _profundidad > 0:
            for otro in registros:  # Otro catálogo: cuentan quienes lo usen a él.
                if (modelo, otro.pk) not in vistos:
                    resultado.usuarios |= uso(otro, _profundidad - 1, vistos).usuarios
    return resultado
