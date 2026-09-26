"""Normalización de datos existentes (idempotente).

Se usa desde la migración `nucleo.0003` (con modelos históricos) y desde el comando
`normalizar_datos`, que debe correrse después de cargar el fixture legacy con `loaddata`.
"""

import re
import unicodedata


def _clave(texto):
    texto = unicodedata.normalize('NFKD', texto or '').encode('ascii', 'ignore').decode().lower()
    return re.sub(r'\s+', ' ', texto).strip()


def _normalizar_doi(valor):
    valor = (valor or '').strip()
    valor = re.sub(r'^(https?://)?(dx\.)?doi\.org/', '', valor, flags=re.IGNORECASE)
    valor = re.sub(r'^doi:\s*', '', valor, flags=re.IGNORECASE)
    return valor.lower()


def jerarquia_instituciones(Institucion):
    """'Facultad de Ciencias, UNAM' → 'Facultad de Ciencias' dependiente de 'UNAM' (si 'UNAM' existe en el país)."""
    raices = {(_clave(i.nombre), i.pais_id): i for i in Institucion.objects.filter(padre__isnull=True)}
    cambios = 0
    for institucion in Institucion.objects.filter(padre__isnull=True, nombre__contains=', '):
        cabeza, _, cola = institucion.nombre.rpartition(', ')
        padre = raices.get((_clave(cola), institucion.pais_id))
        if not cabeza.strip() or padre is None or padre.pk == institucion.pk:
            continue
        repetida = Institucion.objects.filter(nombre=cabeza.strip(), padre=padre, pais_id=institucion.pais_id,
                                              ciudad=institucion.ciudad).exists()
        if not repetida:
            institucion.nombre = cabeza.strip()
            institucion.padre = padre
            institucion.save(update_fields=['nombre', 'padre'])
            cambios += 1
    return cambios


def ambitos(Evento, ParticipacionEventoAcademico, ParticipacionEventoDivulgacion, sede_id):
    sede = [sede_id] if sede_id else []
    total = 0
    for modelo, campo in ((Evento, 'pais'), (ParticipacionEventoAcademico, 'pais'),
                          (ParticipacionEventoDivulgacion, 'evento__pais')):
        total += modelo.objects.filter(**{f'{campo}__in': sede}).exclude(ambito='NACIONAL').update(ambito='NACIONAL')
        total += (modelo.objects.exclude(**{f'{campo}__in': sede}).exclude(ambito='INTERNACIONAL')
                  .update(ambito='INTERNACIONAL'))
    return total


def dois(ArticuloCientifico):
    """Normaliza DOIs; lo que no es un DOI (una URL cualquiera) pasa al campo URL si está vacío."""
    cambios = 0
    for articulo in ArticuloCientifico.objects.exclude(doi=''):
        doi = _normalizar_doi(articulo.doi)
        url = articulo.url
        if not doi.startswith('10.'):
            url = url or articulo.doi.strip()[:200]
            doi = ''
        if (doi, url) != (articulo.doi, articulo.url):
            ArticuloCientifico.objects.filter(pk=articulo.pk).update(doi=doi, url=url)
            cambios += 1
    return cambios


def metricas_revistas(ArticuloCientifico, MetricaRevista):
    """Crea la métrica (JCR) de cada revista y año a partir del factor de impacto capturado en los artículos."""
    creadas = 0
    articulos = ArticuloCientifico.objects.filter(factor_impacto__isnull=False).order_by('pk')
    for articulo in articulos:
        fecha = (articulo.fecha_publicado or articulo.fecha_enprensa or articulo.fecha_aceptado
                 or articulo.fecha_enviado)
        if fecha is None:
            continue
        _, creada = MetricaRevista.objects.get_or_create(
            revista_id=articulo.revista_id, anio=fecha.year, fuente='JCR',
            defaults={'factor_impacto': articulo.factor_impacto})
        creadas += creada
    return creadas


def normalizar(get_model, sede_id):
    """`sede_id`: pk del país sede de la entidad (si falta, todo se considera internacional)."""
    return {
        'instituciones reorganizadas': jerarquia_instituciones(get_model('nucleo', 'Institucion')),
        'ámbitos recalculados': ambitos(get_model('nucleo', 'Evento'),
                                        get_model('difusion_cientifica', 'ParticipacionEventoAcademico'),
                                        get_model('divulgacion_cientifica', 'ParticipacionEventoDivulgacion'),
                                        sede_id),
        'DOIs corregidos': dois(get_model('investigacion', 'ArticuloCientifico')),
        'métricas de revista creadas': metricas_revistas(get_model('investigacion', 'ArticuloCientifico'),
                                                         get_model('nucleo', 'MetricaRevista')),
    }
