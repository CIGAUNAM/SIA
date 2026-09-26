"""Importación de artículos desde Crossref (DOI), BibTeX u ORCID.

El resultado se usa para abrir el formulario de alta ya lleno: el académico revisa y guarda.
"""

import html
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import date


from nucleo.models import ConfiguracionEntidad, Persona, Revista, normalizar_doi, normalizar_issn
from nucleo.similitud import normalizar, personas_parecidas

TIEMPO_ESPERA = 12


class ErrorImportacion(Exception):
    pass


@dataclass
class DatosArticulo:
    titulo: str = ''
    revista: str = ''
    issn: list = field(default_factory=list)
    volumen: str = ''
    numero: str = ''
    pagina_inicio: int | None = None
    pagina_fin: int | None = None
    fecha: date | None = None
    doi: str = ''
    url: str = ''
    autores: list = field(default_factory=list)  # [(nombre, apellidos)]


def _obtener_json(url, encabezados=None):
    solicitud = urllib.request.Request(url, headers={
        'User-Agent': f"SIA/1.0 (mailto:{ConfiguracionEntidad.actual().remitente_correos.split('<')[-1].rstrip('>')})",
        **(encabezados or {})})
    try:
        with urllib.request.urlopen(solicitud, timeout=TIEMPO_ESPERA) as respuesta:
            return json.loads(respuesta.read().decode('utf-8'))
    except urllib.error.HTTPError as error:
        if error.code == 404:
            raise ErrorImportacion('No se encontró el registro solicitado.')
        raise ErrorImportacion(f'El servicio respondió con un error ({error.code}).')
    except (urllib.error.URLError, TimeoutError) as error:
        raise ErrorImportacion(f'No fue posible conectarse al servicio ({error}).')


def _limpiar(texto):
    """Quita etiquetas (<i>, <sub>...) y entidades HTML que Crossref incluye en títulos."""
    return ' '.join(html.unescape(re.sub(r'<[^>]+>', '', texto or '')).split())


def _paginas(texto):
    partes = re.findall(r'\d+', texto or '')
    inicio = int(partes[0]) if partes else None
    fin = int(partes[1]) if len(partes) > 1 else None
    return inicio, fin


def desde_crossref(doi):
    doi = normalizar_doi(doi)
    if not doi.startswith('10.'):
        raise ErrorImportacion('Escribe un DOI válido (empieza con "10.").')
    mensaje = _obtener_json(f'https://api.crossref.org/works/{urllib.parse.quote(doi)}')['message']
    partes_fecha = None
    for clave in ('published-print', 'published-online', 'issued'):
        partes_fecha = (mensaje.get(clave) or {}).get('date-parts', [[None]])[0]
        if partes_fecha and partes_fecha[0]:
            break
    fecha = None
    if partes_fecha and partes_fecha[0]:
        anio, mes, dia = (list(partes_fecha) + [1, 1])[:3]
        fecha = date(anio, mes or 1, dia or 1)
    inicio, fin = _paginas(mensaje.get('page'))
    return DatosArticulo(
        titulo=_limpiar((mensaje.get('title') or [''])[0]),
        revista=_limpiar((mensaje.get('container-title') or [''])[0]),
        issn=[normalizar_issn(x) for x in mensaje.get('ISSN', [])],
        volumen=mensaje.get('volume', ''), numero=mensaje.get('issue', ''),
        pagina_inicio=inicio, pagina_fin=fin, fecha=fecha, doi=doi, url=mensaje.get('URL', ''),
        autores=[(a.get('given', ''), a.get('family', '')) for a in mensaje.get('author', []) if a.get('family')],
    )


def _campos_bibtex(cuerpo):
    """Campos `nombre = {valor}` o `nombre = "valor"` de una entrada BibTeX (admite llaves anidadas)."""
    campos, i = {}, 0
    while True:
        coincidencia = re.compile(r'\s*,?\s*(\w+)\s*=\s*').match(cuerpo, i)
        if not coincidencia:
            break
        nombre, i = coincidencia.group(1).lower(), coincidencia.end()
        if i >= len(cuerpo):
            break
        if cuerpo[i] in '{"':
            cierre = '}' if cuerpo[i] == '{' else '"'
            nivel, j = 0, i
            while j < len(cuerpo):
                if cuerpo[j] == '{':
                    nivel += 1
                elif cuerpo[j] == '}':
                    nivel -= 1
                if (cierre == '}' and nivel == 0) or (cierre == '"' and j > i and cuerpo[j] == '"' and nivel == 0):
                    break
                j += 1
            valor, i = cuerpo[i + 1:j], j + 1
        else:
            fin = re.compile(r'[,}\n]').search(cuerpo, i)
            valor, i = cuerpo[i:fin.start() if fin else len(cuerpo)], (fin.start() if fin else len(cuerpo))
        campos[nombre] = ' '.join(valor.replace('{', '').replace('}', '').split())
    return campos


def _autor_bibtex(texto):
    if ',' in texto:
        apellidos, _, nombre = texto.partition(',')
    else:
        *nombre, apellidos = texto.split() or ['']
        nombre = ' '.join(nombre)
    return nombre.strip(), apellidos.strip()


def desde_bibtex(texto):
    articulos = []
    for cuerpo in re.split(r'@\w+\s*\{', texto)[1:]:
        cuerpo = cuerpo.split(',', 1)[1] if ',' in cuerpo else cuerpo  # Quita la llave de cita.
        campos = _campos_bibtex(cuerpo)
        if not campos.get('title'):
            continue
        inicio, fin = _paginas(campos.get('pages'))
        anio = int(campos['year']) if campos.get('year', '').isdigit() else None
        articulos.append(DatosArticulo(
            titulo=campos['title'], revista=campos.get('journal', ''),
            issn=[normalizar_issn(x) for x in re.split(r'[,; ]+', campos.get('issn', '')) if x],
            volumen=campos.get('volume', ''), numero=campos.get('number', ''), pagina_inicio=inicio,
            pagina_fin=fin, fecha=date(anio, 1, 1) if anio else None, doi=normalizar_doi(campos.get('doi', '')),
            url=campos.get('url', ''),
            autores=[_autor_bibtex(a) for a in re.split(r'\s+and\s+', campos.get('author', '')) if a.strip()],
        ))
    if not articulos:
        raise ErrorImportacion('No se encontró ninguna entrada BibTeX con título.')
    return articulos


def obras_orcid(orcid):
    """[(título, año, DOI)] de las obras públicas de un ORCID."""
    orcid = orcid.strip().rsplit('/', 1)[-1]
    if not re.fullmatch(r'\d{4}-\d{4}-\d{4}-\d{3}[\dX]', orcid):
        raise ErrorImportacion('El ORCID debe tener el formato 0000-0000-0000-000X.')
    datos = _obtener_json(f'https://pub.orcid.org/v3.0/{orcid}/works', {'Accept': 'application/json'})
    obras = []
    for grupo in datos.get('group', []):
        resumen = (grupo.get('work-summary') or [{}])[0]
        doi = next((normalizar_doi(e.get('external-id-value')) for e in
                    (resumen.get('external-ids') or {}).get('external-id', [])
                    if e.get('external-id-type') == 'doi'), '')
        titulo = (((resumen.get('title') or {}).get('title')) or {}).get('value', '')
        anio = (((resumen.get('publication-date') or {}).get('year')) or {}).get('value', '')
        obras.append((titulo, anio, doi))
    return obras


def buscar_revista(datos):
    for issn in datos.issn:
        revista = Revista.objects.filter(issn_impreso=issn).first() or Revista.objects.filter(
            issn_electronico=issn).first()
        if revista:
            return revista
    if datos.revista:
        objetivo = normalizar(datos.revista)
        for revista in Revista.objects.filter(nombre__icontains=datos.revista.split()[0])[:100]:
            if normalizar(revista.nombre) == objetivo or normalizar(revista.nombre_abreviado) == objetivo:
                return revista
    return None


def resolver_autores(datos, usuario):
    """Personas del catálogo para cada autor; si no hay una parecida se crea (sin verificar)."""
    personas, nuevas = [], []
    for nombre, apellidos in datos.autores:
        parecidas = personas_parecidas(Persona.objects.all(), nombre, apellidos)
        parecidas.sort(key=lambda p: p.usuario_id is None)  # Prefiere a quien tiene cuenta.
        if parecidas:
            personas.append(parecidas[0])
        else:
            persona = Persona.objects.create(nombre=nombre or '—', apellidos=apellidos, creado_por=usuario)
            personas.append(persona)
            nuevas.append(persona)
    return personas, nuevas


def parametros_alta(datos, usuario):
    """Parámetros GET para el formulario de alta y avisos para el usuario."""
    avisos = []
    revista = buscar_revista(datos)
    if revista is None and datos.revista:
        avisos.append(f'La revista "{datos.revista}" no está en el catálogo: agrégala con el botón + del campo Revista.')
    personas, nuevas = resolver_autores(datos, usuario)
    if nuevas:
        avisos.append('Se agregaron al catálogo de personas: ' + ', '.join(str(p) for p in nuevas) + '.')
    parametros = {
        'titulo': datos.titulo, 'volumen': datos.volumen, 'numero': datos.numero, 'doi': datos.doi,
        'url': datos.url, 'status': 'PUBLICADO',
        'fecha_publicado': datos.fecha.strftime('%d/%m/%Y') if datos.fecha else '',
        'pagina_inicio': datos.pagina_inicio or '', 'pagina_fin': datos.pagina_fin or '',
        'revista': revista.pk if revista else '', '_autores': ','.join(str(p.pk) for p in personas),
    }
    return {k: v for k, v in parametros.items() if v not in ('', None)}, avisos
