"""Detección de posibles registros duplicados por similitud de nombres."""

import re
import unicodedata
from difflib import SequenceMatcher
from functools import reduce

from django.db.models import Q

PALABRAS_VACIAS = {'de', 'del', 'la', 'las', 'el', 'los', 'y', 'e', 'en', 'para', 'the', 'of', 'and', 'for', 'a'}


def normalizar(texto):
    """Minúsculas, sin acentos ni puntuación, espacios simples."""
    texto = unicodedata.normalize('NFKD', texto or '').encode('ascii', 'ignore').decode()
    return re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', ' ', texto.lower())).strip()


def _palabras_clave(texto, maximo=2):
    palabras = [p for p in normalizar(texto).split() if p not in PALABRAS_VACIAS and len(p) > 2]
    return sorted(palabras, key=len, reverse=True)[:maximo]


VARIANTES = {'a': 'aáàäâ', 'e': 'eéèëê', 'i': 'iíìïî', 'o': 'oóòöô', 'u': 'uúùüû', 'n': 'nñ', 'c': 'cç'}


def patron_sin_acentos(palabra):
    """Expresión regular que encuentra la palabra con o sin acentos (funciona en SQLite y PostgreSQL)."""
    return ''.join(f'[{VARIANTES[c]}]' if c in VARIANTES else re.escape(c) for c in normalizar(palabra))


def nombres_compatibles(a, b):
    """'J. C.' ≈ 'Juan Carlos' ≈ 'Juan C.'; 'Juan' ≉ 'José'."""
    ta, tb = normalizar(a).split(), normalizar(b).split()
    if not ta or not tb:
        return True
    if ta[0][0] != tb[0][0]:
        return False
    if all(len(t) == 1 for t in ta) or all(len(t) == 1 for t in tb):
        corto, largo = sorted((ta, tb), key=len)
        return all(x[0] == y[0] for x, y in zip(corto, largo))
    return ta[0] == tb[0] or parecidos(a, b)


def parecidos(a, b, umbral=0.85):
    a, b = normalizar(a), normalizar(b)
    if not a or not b:
        return False
    return a == b or SequenceMatcher(None, a, b).ratio() >= umbral or set(a.split()) == set(b.split())


def candidatos(queryset, campos, texto, excluir_pk=None, limite=5):
    """Registros de `queryset` cuyo texto (concatenación de `campos`) se parece a `texto`."""
    palabras = _palabras_clave(texto)
    if not palabras:
        return []
    filtro = reduce(lambda q, palabra: q | Q(**{f'{campos[-1]}__iregex': patron_sin_acentos(palabra)}), palabras, Q())
    qs = queryset.filter(filtro)
    if excluir_pk is not None:
        qs = qs.exclude(pk=excluir_pk)
    resultado = []
    for obj in qs[:200]:
        texto_obj = ' '.join(str(getattr(obj, campo) or '') for campo in campos)
        if parecidos(texto, texto_obj):
            resultado.append(obj)
            if len(resultado) >= limite:
                break
    return resultado


def personas_parecidas(queryset, nombre, apellidos, excluir_pk=None, limite=5):
    """Personas con apellidos equivalentes y el mismo nombre o la misma inicial (J. Pérez ≈ Juan Pérez)."""
    palabras = _palabras_clave(apellidos, maximo=1)
    if not palabras:
        return []
    qs = queryset.filter(apellidos__iregex=patron_sin_acentos(palabras[0]))
    if excluir_pk is not None:
        qs = qs.exclude(pk=excluir_pk)
    resultado = []
    for persona in qs[:200]:
        if parecidos(apellidos, persona.apellidos, umbral=0.9) and nombres_compatibles(nombre, persona.nombre):
            resultado.append(persona)
            if len(resultado) >= limite:
                break
    return resultado
