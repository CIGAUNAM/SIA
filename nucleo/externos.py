"""Consultas a servicios públicos (Crossref, ORCID)."""

import json
import urllib.error
import urllib.request

from .nombres import formato_cita, normalizar_orcid

TIEMPO_ESPERA = 12


class ErrorServicio(Exception):
    pass


def obtener_json(url, encabezados=None):
    from .models import ConfiguracionEntidad

    remitente = ConfiguracionEntidad.actual().remitente_correos.split('<')[-1].rstrip('>')
    solicitud = urllib.request.Request(url, headers={
        'User-Agent': f'SIA/1.0 (mailto:{remitente})', 'Accept': 'application/json', **(encabezados or {})})
    try:
        with urllib.request.urlopen(solicitud, timeout=TIEMPO_ESPERA) as respuesta:
            return json.loads(respuesta.read().decode('utf-8'))
    except urllib.error.HTTPError as error:
        if error.code == 404:
            raise ErrorServicio('No se encontró el registro solicitado.')
        raise ErrorServicio(f'El servicio respondió con un error ({error.code}).')
    except (urllib.error.URLError, TimeoutError) as error:
        raise ErrorServicio(f'No fue posible conectarse al servicio ({error}).')


def nombre_orcid(orcid):
    """Nombre en formato de cita a partir del registro público de ORCID ('' si no es público)."""
    orcid = normalizar_orcid(orcid)
    if not orcid:
        raise ErrorServicio('El ORCID debe tener el formato 0000-0000-0000-000X.')
    nombre = obtener_json(f'https://pub.orcid.org/v3.0/{orcid}/person').get('name') or {}
    valor = lambda clave: ((nombre.get(clave) or {}).get('value') or '').strip()
    return formato_cita(valor('given-names'), valor('family-name')) or valor('credit-name')
