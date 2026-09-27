"""Sugerencias de ORCID para las cuentas que no lo tienen.

Se buscan en ORCID los perfiles con el nombre de cada académico y los afiliados a la entidad; el cruce es por
nombre, así que un administrador confirma cada sugerencia antes de guardarla.
"""

import hashlib
from concurrent.futures import ThreadPoolExecutor

from django.core.cache import cache

from .externos import ErrorServicio, perfiles_por_afiliacion, perfiles_por_nombre
from .fusion import fusionar
from .models import ConfiguracionEntidad, Persona, User
from .nombres import PARTICULAS, partes_cita
from .similitud import normalizar

CACHE_SEGUNDOS = 60 * 60


def _partes(cuenta):
    """(nombres, apellidos) de la cuenta: su nombre legal o, si falta, el de su persona."""
    if cuenta.last_name:
        return cuenta.first_name, cuenta.last_name
    apellidos, nombres = partes_cita(cuenta.persona.nombre)
    return nombres, apellidos


def _palabras(texto):
    return [t for t in normalizar(texto).split() if t not in PARTICULAS]


def coincidencia(nombres, apellidos, perfil):
    """'exacta', 'probable' o None.

    Compara palabras sin importar el orden, porque ORCID a veces invierte o parte distinto nombre y apellidos
    ('RUIZ-LÓPEZ CINTHIA', 'Gustavo' + 'Martín Morales'). Se descarta si el perfil contradice el nombre: le sobran
    palabras y a la vez le faltan otras de la cuenta ('Alvarez León' frente a 'Alvarez Larrain').
    """
    a_nombres, a_apellidos = _palabras(nombres), _palabras(apellidos)
    p = _palabras(f"{perfil['nombres']} {perfil['apellidos']}")
    if not a_nombres or not a_apellidos or a_apellidos[0] not in p:
        return None
    iniciales = {t for t in p if len(t) == 1}
    if a_nombres[0] not in p and a_nombres[0][0] not in iniciales:
        return None
    cuenta = set(a_nombres + a_apellidos)
    sobran = {t for t in p if t not in cuenta and not (len(t) == 1 and any(c.startswith(t) for c in cuenta))}
    faltan = {t for t in cuenta if t not in p and t[0] not in iniciales}
    if sobran and faltan:
        return None
    return 'exacta' if not sobran and not faltan else 'probable'


def _afiliada(perfil, claves):
    texto = normalizar(' '.join(perfil['instituciones']))
    return any(clave in texto for clave in claves)


def _buscar_por_nombre(nombres, apellidos):
    llave = 'nucleo:orcid_nombre:' + hashlib.md5(f'{normalizar(nombres)}|{normalizar(apellidos)}'.encode()).hexdigest()
    perfiles = cache.get(llave)
    if perfiles is None:
        try:
            perfiles = perfiles_por_nombre(nombres, apellidos)
        except ErrorServicio:
            return []
        cache.set(llave, perfiles, CACHE_SEGUNDOS)
    return perfiles


def sugerencias(request=None):
    """[(cuenta, [(perfil, nivel, afiliada), ...])] para las cuentas activas cuya persona no tiene ORCID.

    Primero las coincidencias exactas y con afiliación a la entidad o a su institución madre.
    """
    config = ConfiguracionEntidad.actual(request)
    claves = [normalizar(x) for x in (config.nombre, config.institucion_madre, config.institucion_madre_siglas,
                                      config.siglas) if x]
    usados = set(Persona.objects.filter(usuario__isnull=False).exclude(orcid='').values_list('orcid', flat=True))
    cuentas = list(User.objects.filter(is_active=True, persona__orcid='').select_related('persona')
                   .order_by('persona__nombre'))
    partes = [_partes(c) for c in cuentas]

    llave = 'nucleo:orcid_afiliacion:' + hashlib.md5(normalizar(config.nombre).encode()).hexdigest()
    de_la_entidad = cache.get(llave)
    if de_la_entidad is None:
        try:
            de_la_entidad = perfiles_por_afiliacion([config.nombre])
        except ErrorServicio:
            de_la_entidad = []
        cache.set(llave, de_la_entidad, CACHE_SEGUNDOS)
    with ThreadPoolExecutor(max_workers=8) as grupo:
        por_nombre = list(grupo.map(lambda p: _buscar_por_nombre(*p), partes))

    resultado = []
    for cuenta, (nombres, apellidos), propios in zip(cuentas, partes, por_nombre):
        candidatos = {}
        for perfil in [*propios, *de_la_entidad]:
            if perfil['orcid'] in usados or perfil['orcid'] in candidatos:
                continue
            if nivel := coincidencia(nombres, apellidos, perfil):
                candidatos[perfil['orcid']] = (perfil, nivel, _afiliada(perfil, claves))
        if candidatos:
            orden = sorted(candidatos.values(), key=lambda c: (not c[2], c[1] != 'exacta'))
            resultado.append((cuenta, orden[:4]))
    return resultado


def preseleccion(candidatos):
    """ORCID que conviene marcar de entrada: el único que coincide exacto y está afiliado a la entidad."""
    seguros = [perfil['orcid'] for perfil, nivel, afiliada in candidatos if nivel == 'exacta' and afiliada]
    return seguros[0] if len(seguros) == 1 else ''


def asignar_orcid(persona, orcid):
    """Guarda el ORCID en la persona; si otra persona sin cuenta ya lo tenía, es la misma y se fusiona."""
    otra = Persona.objects.filter(orcid=orcid).exclude(pk=persona.pk).first()
    if otra is not None:
        if otra.tiene_cuenta:
            raise ValueError(f'{orcid} ya es de la cuenta {otra.usuario}.')
        fusionar(persona, [otra])
    persona.orcid = orcid
    persona.save(update_fields=['orcid', 'actualizado'])
    return otra
