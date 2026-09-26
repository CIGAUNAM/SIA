from django.db.models import Prefetch


def _through(modelo, campo):
    """Modelo intermedio de una relación M2M con `Persona` y el accesor inverso desde `modelo`."""
    m2m = modelo._meta.get_field(campo)
    through = m2m.remote_field.through
    accesor = through._meta.get_field(m2m.m2m_field_name()).remote_field.get_accessor_name()
    return through, accesor


def prefetch_personas(modelo, campo):
    """Prefetch que conserva el orden de la tabla intermedia (autores, tutores...)."""
    through, accesor = _through(modelo, campo)
    if through._meta.auto_created:
        return Prefetch(campo)
    return Prefetch(accesor, queryset=through.objects.select_related('persona'))


def personas_ordenadas(obj, campo):
    """Personas de una relación M2M en el orden capturado (usa el prefetch si existe)."""
    through, accesor = _through(type(obj), campo)
    if through._meta.auto_created:
        return list(getattr(obj, campo).all())
    return [fila.persona for fila in getattr(obj, accesor).all()]
