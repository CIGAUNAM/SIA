"""Validación de identificadores mexicanos (RFC, CURP) y teléfonos.

- RFC y CURP: formato, fecha real y dígito verificador (algoritmos del SAT y de RENAPO).
- Teléfono: `phonenumbers` (libphonenumber de Google); México por omisión, otros países con `+código`.
"""

import re
from datetime import date

import phonenumbers
from django.core.exceptions import ValidationError

REGION_TELEFONO = 'MX'

_RFC = re.compile(r'^([A-ZÑ&]{3,4})(\d{2})(\d{2})(\d{2})([A-Z\d]{2}[A\d])$')
_CURP = re.compile(r'^[A-Z][AEIOUX][A-Z]{2}(\d{2})(\d{2})(\d{2})[HMX](AS|BC|BS|CC|CL|CM|CS|CH|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|'
                   r'OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)[B-DF-HJ-NP-TV-Z]{3}[A-Z\d]\d$')
_TABLA_RFC = '0123456789ABCDEFGHIJKLMN&OPQRSTUVWXYZ Ñ'
_TABLA_CURP = '0123456789ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'


def _fecha(aa, mm, dd, siglo_por_letra=None):
    """date o None; el siglo se infiere (RFC) o lo indica el carácter 17 de la CURP (dígito: 1900, letra: 2000)."""
    anio = int(aa)
    if siglo_por_letra is None:
        anio += 1900 if anio > date.today().year % 100 else 2000
    else:
        anio += 2000 if siglo_por_letra.isalpha() else 1900
    try:
        return date(anio, int(mm), int(dd))
    except ValueError:
        return None


def digito_rfc(rfc):
    base = rfc[:-1].rjust(12)  # El RFC de persona moral (12) se completa con un espacio al inicio.
    resto = 11 - sum(_TABLA_RFC.index(c) * (13 - i) for i, c in enumerate(base)) % 11
    return 'A' if resto == 10 else '0' if resto == 11 else str(resto)


def digito_curp(curp):
    return str((10 - sum(_TABLA_CURP.index(c) * (18 - i) for i, c in enumerate(curp[:17])) % 10) % 10)


def validar_rfc(valor):
    rfc = (valor or '').strip().upper()
    coincide = _RFC.match(rfc)
    if not coincide:
        raise ValidationError('El RFC debe tener 13 caracteres (persona física) o 12 (moral), p. ej. GODE561231GR8.')
    if _fecha(*coincide.group(2, 3, 4)) is None:
        raise ValidationError('La fecha contenida en el RFC no existe.')
    if rfc[-1] != digito_rfc(rfc):
        raise ValidationError('El RFC no es válido: su dígito verificador no corresponde. Revisa la homoclave.')


def validar_curp(valor):
    curp = (valor or '').strip().upper()
    coincide = _CURP.match(curp)
    if not coincide:
        raise ValidationError('La CURP debe tener 18 caracteres con el formato oficial, p. ej. HEGG560427MVZRRL04.')
    if _fecha(*coincide.group(1, 2, 3), siglo_por_letra=curp[16]) is None:
        raise ValidationError('La fecha contenida en la CURP no existe.')
    if curp[-1] != digito_curp(curp):
        raise ValidationError('La CURP no es válida: su dígito verificador no corresponde.')


def fecha_de_curp(curp):
    coincide = _CURP.match((curp or '').strip().upper())
    return _fecha(*coincide.group(1, 2, 3), siglo_por_letra=curp.strip().upper()[16]) if coincide else None


def _numero(valor):
    try:
        return phonenumbers.parse((valor or '').strip(), REGION_TELEFONO)
    except phonenumbers.NumberParseException:
        return None


def validar_telefono(valor):
    numero = _numero(valor)
    if numero is None or not phonenumbers.is_valid_number(numero):
        raise ValidationError('Escribe un teléfono válido: 10 dígitos si es de México (p. ej. 443 322 3854) o con '
                              '+código de país si es de otro país. Puede llevar extensión (ext. 123).')


def normalizar_telefono(valor):
    """'(443) 322-3854' → '+52 443 322 3854' (formato internacional); si no se puede interpretar, igual que llegó."""
    numero = _numero(valor)
    if numero is None or not phonenumbers.is_valid_number(numero):
        return (valor or '').strip()
    return phonenumbers.format_number(numero, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
