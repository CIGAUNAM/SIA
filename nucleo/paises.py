"""Países: catálogo de django-cities-light (`cities_light.Country`) cargado desde `nucleo/fixtures/paises.json`.

El fixture se guarda en el repositorio (no se importa de GeoNames) para que los ids sean estables. Tiene los países
ISO de GeoNames con nombres en español y, sin código ISO, los que usaba el SIA anterior (Inglaterra, Desconocido...).
"""

import json
from pathlib import Path

FIXTURE = Path(__file__).parent / 'fixtures' / 'paises.json'
#: Códigos del SIA anterior que corresponden a un país con código ISO (Inglaterra y Gales → Reino Unido).
ALIAS = {'EU': 'US', '1': 'NL', '67': 'KR', '78': 'AE', '23': 'GB', '44': 'GB'}


def equivalencia(paises_anteriores, paises):
    """{pk anterior: pk en el catálogo}.

    `paises_anteriores`: [(pk, código, nombre)] del SIA anterior; `paises`: [(pk, code2, nombre)] del catálogo.
    Se relacionan por código ISO (o su alias) y, los que no tienen código, por nombre.
    """
    por_codigo = {code2: pk for pk, code2, _ in paises if code2}
    por_nombre = {nombre: pk for pk, code2, nombre in paises if not code2}
    resultado, faltan = {}, []
    for pk, codigo, nombre in paises_anteriores:
        codigo = (codigo or '').upper()
        nuevo = por_codigo.get(ALIAS.get(codigo, codigo)) or por_nombre.get(nombre)
        if nuevo is None:
            faltan.append(f'{nombre} ({codigo})')
        resultado[pk] = nuevo
    if faltan:
        raise ValueError('Países sin equivalente en el catálogo: ' + ', '.join(faltan))
    return resultado


def del_fixture():
    return [(o['pk'], o['fields']['code2'], o['fields']['name']) for o in json.loads(FIXTURE.read_text('utf-8'))]
