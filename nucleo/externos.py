"""Consultas a servicios públicos (Crossref, ORCID)."""

import json
import urllib.error
import urllib.parse
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


def orcid_por_correo(correo):
    """(ORCID, nombre en formato de cita) de quien tiene ese correo público en ORCID; None si no hay uno solo."""
    if not correo or correo.endswith('.invalid'):
        return None
    datos = obtener_json('https://pub.orcid.org/v3.0/expanded-search/?q='
                         + urllib.parse.quote(f'email:{correo.strip().lower()}'))
    resultados = datos.get('expanded-result') or []
    if len(resultados) != 1:
        return None
    r = resultados[0]
    return r['orcid-id'], formato_cita(r.get('given-names'), r.get('family-names')) or r.get('credit-name') or ''


def buscar_perfiles(consulta, maximo=1000):
    """Perfiles públicos de ORCID que cumplen la consulta (sintaxis de búsqueda de ORCID).

    Devuelve dicts con `orcid`, `nombres`, `apellidos`, `nombre` (formato de cita) e `instituciones`.
    """
    perfiles, inicio = [], 0
    while inicio < maximo:
        datos = obtener_json('https://pub.orcid.org/v3.0/expanded-search/?'
                             + urllib.parse.urlencode({'q': consulta, 'start': inicio, 'rows': min(200, maximo)}))
        pagina = datos.get('expanded-result') or []
        for r in pagina:
            nombres, apellidos = (r.get('given-names') or '').strip(), (r.get('family-names') or '').strip()
            perfiles.append({'orcid': r['orcid-id'], 'nombres': nombres, 'apellidos': apellidos,
                             'nombre': formato_cita(nombres, apellidos) or r.get('credit-name') or '',
                             'instituciones': r.get('institution-name') or []})
        inicio += len(pagina)
        if not pagina or inicio >= (datos.get('num-found') or 0):
            break
    return perfiles


def perfiles_por_afiliacion(instituciones):
    consulta = ' OR '.join(f'affiliation-org-name:"{nombre}"' for nombre in instituciones if nombre)
    return buscar_perfiles(consulta) if consulta else []


def perfiles_por_nombre(nombres, apellidos, maximo=20):
    """Perfiles cuyo primer apellido y primer nombre coinciden (p. ej. 'Pérez' y 'Juan')."""
    apellido, nombre = (apellidos.split() or [''])[0], (nombres.split() or [''])[0]
    if not apellido or not nombre or len(nombre.strip('.')) < 2:
        return []
    return buscar_perfiles(f'family-name:"{apellido}" AND given-names:"{nombre}"', maximo=maximo)
