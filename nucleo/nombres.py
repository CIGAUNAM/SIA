"""Nombre de las personas en formato de cita: `Apellidos, I. N.` (p. ej. `Pérez García, J. C.`).

Es el formato de Scopus, Web of Science y APA; al empezar por los apellidos, el orden alfabético
de la cadena es el orden por apellido.
"""

import re

PARTICULAS = {'de', 'del', 'la', 'las', 'los', 'y', 'e', 'da', 'das', 'do', 'dos', 'van', 'von', 'der', 'di'}


def iniciales(nombres):
    """'Juan Carlos' → 'J. C.'; 'Jean-Pierre' → 'J.-P.'; 'E.J' → 'E. J.'; se omiten 'de', 'la'..."""
    resultado = []
    for palabra in (nombres or '').replace('.', '. ').split():
        if palabra.lower() in PARTICULAS:
            continue
        partes = [p for p in palabra.strip('.').split('-') if p]
        letras = ['{}.'.format(next((c for c in parte if c.isalpha()), '').upper()) for parte in partes]
        if letras and all(len(x) > 1 for x in letras):
            resultado.append('-'.join(letras))
    return ' '.join(resultado)


def formato_cita(nombres, apellidos):
    nombres, apellidos = ' '.join((nombres or '').split()), ' '.join((apellidos or '').split())
    if not apellidos:
        return nombres
    abreviado = iniciales(nombres)
    return f'{apellidos}, {abreviado}' if abreviado else apellidos


def partes_cita(nombre):
    """('Pérez García', 'J. C.') a partir de 'Pérez García, J. C.'. Sin coma, todo se toma como apellidos."""
    apellidos, _, nombres = (nombre or '').rpartition(',')
    if not apellidos:
        return nombres.strip(), ''
    return apellidos.strip(), nombres.strip()


def normalizar_orcid(valor):
    """'https://orcid.org/0000-0002-1825-0097' → '0000-0002-1825-0097'."""
    valor = (valor or '').strip().rstrip('/').rsplit('/', 1)[-1].upper()
    return valor if re.fullmatch(r'\d{4}-\d{4}-\d{4}-\d{3}[\dX]', valor) else ''
