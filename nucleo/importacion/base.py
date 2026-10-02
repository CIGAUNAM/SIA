"""Utilidades para importar las hojas de cálculo del informe anual: limpieza de valores, fechas, personas,
instituciones y revistas, y el reporte de compatibilidad (qué se importó, qué ya existía y qué no cupo)."""

import re
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import date, datetime
from difflib import SequenceMatcher

from cities_light.models import Country
from django.db.models import Q

from nucleo.models import DOMINIO_SIN_CORREO as DOMINIO, SIN_FECHA, Institucion, Persona, Revista, User
from nucleo.nombres import formato_cita
from nucleo.normalizacion import sin_comillas
from nucleo.similitud import normalizar, patron_sin_acentos, personas_parecidas

VACIOS = {'', '?', 'n/a', 'na', 'n/d', 'nd', 'no aplica', '-', '--', 'ninguno', 'ninguna', 'no', 'sin dato', 's/n',
          'no se reporta', 'no se reportó', 'none'}
MESES = {m: i for i, m in enumerate(
    ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre',
     'diciembre'], start=1)} | {'setiembre': 9}


def texto(valor, vacio_si_no=True):
    """Texto limpio; '?', 'N/A', 'n/d'… cuentan como vacío. Con `vacio_si_no=False`, 'No' se conserva."""
    if valor is None:
        return ''
    if isinstance(valor, float) and valor.is_integer():
        valor = int(valor)
    t = ' '.join(str(valor).split())
    clave = t.lower().strip('.')
    if clave in VACIOS and (vacio_si_no or clave != 'no'):
        return ''
    return t


def titulo(valor):
    return sin_comillas(texto(valor)).strip(' .')


def numero(valor):
    t = texto(valor).replace(',', '')
    try:
        return int(float(t))
    except ValueError:
        return None


def si_no(valor):
    return texto(valor, vacio_si_no=False).lower().startswith(('si', 'sí', 'yes'))


def mes(valor):
    t = normalizar(texto(valor))
    if isinstance(valor, (int, float)) or t.isdigit():
        n = numero(valor)
        return n if n and 1 <= n <= 12 else None
    return next((n for nombre, n in MESES.items() if t.startswith(nombre[:3])), None)


def anio(valor):
    if isinstance(valor, (date, datetime)):
        return valor.year
    n = numero(valor)
    return n if n and 1900 <= n <= 2100 else None


def fecha(dia=None, mes_=None, anio_=None, por_defecto=None):
    """Fecha con día, mes (número o nombre) y año sueltos; sin año, `por_defecto` o "sin fecha" (1900)."""
    if isinstance(anio_, (date, datetime)):
        return anio_ if isinstance(anio_, date) and not isinstance(anio_, datetime) else anio_.date()
    a = anio(anio_)
    if a is None:
        return por_defecto or SIN_FECHA
    m = mes(mes_) or 1
    d = numero(dia) or 1
    for dia_valido in (d, 28):
        try:
            return date(a, m, dia_valido)
        except ValueError:
            continue
    return date(a, m, 1)


def fecha_celda(valor, por_defecto=None):
    if isinstance(valor, datetime):
        return valor.date()
    if isinstance(valor, date):
        return valor
    a = anio(valor)
    return date(a, 1, 1) if a else (por_defecto or SIN_FECHA)


def inicio_periodo(periodo):
    """'2025-2026' → 1 de julio de 2025 (el informe de la entidad va de julio a junio)."""
    m = re.match(r'(\d{4})-\d{4}', texto(periodo))
    return date(int(m.group(1)), 7, 1) if m else None


def fecha_en_periodo(anio_, periodo, mes_=None, dia=None):
    """Fecha de un producto con solo año (y quizá mes) que cae dentro del periodo del informe en que se reportó:
    así cuenta igual para el informe de la entidad (jul-jun) y para el anual de la UNAM (ene-dic)."""
    a = anio(anio_)
    inicio = inicio_periodo(periodo)
    if a is None:
        return inicio or SIN_FECHA
    if mes(mes_):
        return fecha(dia, mes_, a)
    candidata = date(a, 1, 1)
    if inicio and candidata < inicio <= date(a, 12, 31):
        return inicio
    return candidata


def _tokens(nombre):
    t = unicodedata.normalize('NFKD', nombre or '').encode('ascii', 'ignore').decode().lower()
    alias = {'ma': 'maria', 'ma.': 'maria', 'fco': 'francisco', 'jf': 'jean'}
    return [alias.get(p, p) for p in re.split(r'[^a-z]+', t)
            if len(p) > 1 and p not in {'de', 'del', 'la', 'las', 'los', 'y', 'dra', 'dr', 'mtra', 'mtro'}]


def _token_igual(a, b):
    return a == b or (len(a) > 3 and len(b) > 3 and SequenceMatcher(None, a, b).ratio() >= 0.8) or (
        len(a) == 1 and b.startswith(a)) or (len(b) == 1 and a.startswith(b))


def _abarca(consulta, nombre_completo):
    """Todos los tokens de la consulta aparecen (con tolerancia a errores de dedo) en el nombre completo."""
    return consulta and all(any(_token_igual(q, t) for t in nombre_completo) for q in consulta)


def _pais(nombre):
    t = texto(nombre)
    if not t:
        return None
    sin_acentos = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode()
    return (Country.objects.filter(name__iexact=t).first()
            or Country.objects.filter(name_ascii__iexact=sin_acentos).first()
            or Country.objects.filter(name_ascii__istartswith=sin_acentos.split('/')[0].strip()).first()
            or Country.objects.filter(alternate_names__iregex=r'(^|;)' + re.escape(t) + r'(;|$)').first())


def _titulo_principal(nombre):
    """'Investigaciones Geográficas, Boletín del…' → 'investigaciones geograficas'; 'Revista Etnobiología' →
    'etnobiologia'; 'PatryTer. Revista Latinoamericana…' → 'patryter'."""
    base = re.split(r'[,.:(]| - ', nombre, maxsplit=1)[0]
    base = normalizar(base)
    return re.sub(r'^(revista|the|journal)\s+', '', base).strip()


@dataclass
class Hoja:
    nombre: str
    creados: Counter = field(default_factory=Counter)
    existentes: Counter = field(default_factory=Counter)
    rechazados: list = field(default_factory=list)
    avisos: list = field(default_factory=list)
    filas: int = 0

    def creado(self, modelo):
        self.creados[modelo._meta.verbose_name_plural] += 1

    def existente(self, modelo):
        self.existentes[modelo._meta.verbose_name_plural] += 1

    def rechazo(self, fila, motivo):
        self.rechazados.append((fila, motivo))

    def aviso(self, fila, motivo):
        self.avisos.append((fila, motivo))


class _Fila:
    def __init__(self, hoja, fila):
        from django.db import transaction
        self.hoja, self.numero, self.atomic = hoja, fila, transaction.atomic()

    def __enter__(self):
        self.atomic.__enter__()
        return self

    def __exit__(self, tipo, error, traza):
        self.atomic.__exit__(tipo, error, traza)
        if error is not None and isinstance(error, Exception):
            mensaje = ' '.join(str(error).split())[:220]
            self.hoja.rechazo(self.numero, f'{type(error).__name__}: {mensaje}')
            return True
        return False


class Contexto:
    """Búsquedas con memoria para no duplicar personas, instituciones y revistas al importar."""

    def __init__(self, motivo, carpeta=None):
        self.motivo = motivo[:100]
        self.carpeta = carpeta
        self._libros = {}
        self._vigencias = {}
        self.usuarios = []
        self._usuario_tokens = []
        for u in User.objects.select_related('persona'):
            self.registrar_usuario(u)
        self._personas = {}
        self._instituciones = {}
        self._revistas = {}
        self.mexico = Country.objects.get(code2='MX')
        self.hojas = []
        self.personas_creadas = 0

    def registrar_usuario(self, usuario):
        """Agrega (o actualiza) una cuenta en el índice de búsqueda, sin repetirla."""
        self._usuario_tokens = [x for x in self._usuario_tokens if x[0].pk is None or x[0].pk != usuario.pk]
        self.usuarios = [u for u in self.usuarios if u.pk is None or u.pk != usuario.pk]
        self.usuarios.append(usuario)
        self._usuario_tokens.append((usuario, _tokens(f'{usuario.first_name} {usuario.last_name}'),
                                     usuario.email.split('@')[0].lower()))

    def libro(self, archivo):
        """Libro de Excel de la carpeta del informe (abierto una sola vez)."""
        import openpyxl

        if archivo not in self._libros:
            self._libros[archivo] = openpyxl.load_workbook(self.carpeta / archivo, read_only=True, data_only=True)
        return self._libros[archivo]

    def cuenta(self, valor, hoja=None, fila=None, crear=True):  # crear: True, False o 'posdoc' (solo posdocs)
        """Como `usuario`, pero si quien registró algo no tiene cuenta, la crea: registró producción en el sistema con
        que se armó el informe, así que es de la entidad. Viene como «Nombre Apellido(login)» o «Apellidos, Nombre»."""
        t = texto(valor)
        # «Merlo, A.»: con iniciales, como en las citas (solo si una sola cuenta coincide).
        usuario = self.usuario(valor) or (self._usuario_de_cita(t) if re.search(r',\s*\w\.', t) else None)
        m = re.match(r'^(.+?)\(([\w.\-]+)\)\s*$', t)
        if usuario or not crear:
            return usuario
        if m and normalizar(m.group(1)) not in ('desconocido', ''):
            partes = m.group(1).title().split()
            corte = -2 if len(partes) >= 3 else -1
            nombre, apellidos, login = ' '.join(partes[:corte]), ' '.join(partes[corte:]), m.group(2).lower()
        else:
            m = re.match(r'^([^\W\d][\w\'\- ]+),\s*([^\W\d][\w\'\- ]+)$', t)
            if not m or any(len(p) < 3 for p in (m.group(1).strip(), m.group(2).strip())):
                return None  # «Lupita» o iniciales: no alcanza para saber quién es.
            apellidos, nombre = m.group(1).strip(), m.group(2).strip()
            login = None
        foto = self._foto_posdoc(nombre, apellidos)
        if crear == 'posdoc' and not foto:
            return None
        login = login or foto or re.sub(r'[^a-z]', '', normalizar(nombre)[:1] + normalizar(apellidos.split('-')[0].split()[0]))
        usuario = User(email=f'{login}@{DOMINIO}', first_name=nombre, last_name=apellidos, is_active=True, is_staff=True,
                       tipo=User.Tipo.POSTDOCTORADO if foto else User.Tipo.OTRO)
        usuario.set_unusable_password()
        # Si ya figuraba como persona sin cuenta (sus publicaciones en el SIA), la cuenta queda con esa persona.
        parecidas = personas_parecidas(Persona.objects.filter(usuario__isnull=True), formato_cita(nombre, apellidos),
                                       limite=2)
        if len(parecidas) == 1:
            usuario.persona = parecidas[0]
        self.guardar(usuario)
        self.registrar_usuario(usuario)
        if hoja is not None:
            tipo = 'posdoc (su foto viene con las de posdoctorado)' if foto else 'falta indicar su tipo (posdoc, técnico…)'
            hoja.aviso(fila, f'Se creó la cuenta de «{usuario}» ({login}): {tipo}.')
        return usuario

    def _foto_posdoc(self, nombre, apellidos):
        """Login de un posdoc según el nombre de su foto en «Copia de Posdoc.zip» (inicial(es) + primer apellido)."""
        import zipfile

        if not hasattr(self, '_fotos'):
            self._fotos = []
            for archivo in (self.carpeta.glob('*Posdoc*.zip') if self.carpeta else []):
                with zipfile.ZipFile(archivo) as z:
                    self._fotos += [re.sub(r'[^a-z]', '', normalizar(n.rsplit('.', 1)[0])) for n in z.namelist()]
        apellido = re.sub(r'[^a-z]', '', normalizar(apellidos.split('-')[0].split()[0]))
        inicial = normalizar(nombre)[:1]
        return next((f for f in self._fotos if f.endswith(apellido) and f.startswith(inicial)
                     and len(f) - len(apellido) <= 3), None)

    def cuentas(self, valor, hoja=None, fila=None):
        """Cuentas de varios académicos en una celda («Ruiz, Cinthia & Vieyra, Antonio»), en orden. Con varios nombres
        suele ir algún coautor externo, así que entonces solo se crea la cuenta de quien es posdoc de la entidad."""
        resultado = []
        partes = [p for p in re.split(r'\s*(?:&|;|/|\s+y\s+|\s+a\s+)\s*', texto(valor)) if p.strip()]
        for parte in partes:
            usuario = self.cuenta(parte, hoja, fila, crear=True if len(partes) == 1 else 'posdoc')
            if usuario and usuario not in resultado:
                resultado.append(usuario)
        return resultado

    def fila(self, hoja, fila):
        """Cada fila en su propio punto de guardado: si falla, se reporta como no cargada y se sigue con la otra."""
        return _Fila(hoja, fila)

    def hoja(self, nombre):
        self.hojas.append(Hoja(nombre))
        return self.hojas[-1]

    def vigencia(self, obj, periodo):
        """Anota en qué periodo se reportó un registro (sociedad, red, comisión, comité). Al final, lo que no se volvió
        a reportar en el último periodo se cierra al terminar el suyo."""
        inicio = inicio_periodo(periodo)
        if inicio:
            clave = (type(obj), obj.pk)
            self._vigencias[clave] = max(self._vigencias.get(clave, inicio), inicio)

    def cerrar_no_reportados(self):
        from datetime import date as fecha_

        if not self._vigencias:
            return 0
        ultimo = max(self._vigencias.values())
        cerrados = 0
        for (modelo, pk), inicio in self._vigencias.items():
            if inicio >= ultimo:
                continue
            fin = fecha_(inicio.year + 1, 6, 30)
            # También los que traían un término posterior: si no se volvió a reportar, no siguió.
            obj = modelo.objects.filter(Q(fecha_fin__isnull=True) | Q(fecha_fin__gt=fin), pk=pk).first()
            if obj is not None:
                obj.fecha_fin = max(fin, getattr(obj, 'fecha_inicio', None) or fin)
                obj._change_reason = 'Cerrado: no se volvió a reportar en el informe siguiente'
                obj.save()
                cerrados += 1
        return cerrados

    def reportado(self, obj, hoja):
        """Un registro que ya existía y el informe vuelve a reportar: queda en su historial (así no se cierra como
        registro abandonado del SIA anterior)."""
        hoja.existente(type(obj))
        obj._change_reason = 'Reportado de nuevo en las hojas del informe anual'
        obj.save()

    def guardar(self, obj, **kwargs):
        obj._change_reason = self.motivo
        obj.save(**kwargs)
        return obj

    # -- académicos -------------------------------------------------------------------------------
    def usuario(self, valor):
        """Cuenta del académico a partir de 'Nombre Apellido(usuario)', 'Apellido, Nombre' o 'APELLIDOS NOMBRE'."""
        t = texto(valor)
        if not t:
            return None
        m = re.search(r'\(([\w.\-]+)\)\s*$', t)
        if m:
            login = m.group(1).lower()
            candidato = next((u for u, _, local in self._usuario_tokens if local == login), None)
            if candidato is None:  # «amerlo» = inicial del nombre + apellido (cuentas con correo provisional).
                candidatos = [u for u, completo, _ in self._usuario_tokens if completo and len(login) > 3
                              and normalizar(u.first_name)[:1] == login[0]
                              and any(t == login[1:] for t in _tokens(u.last_name))]
                candidato = candidatos[0] if len(candidatos) == 1 else None
            if candidato:
                return candidato
            t = t[:m.start()]
        consulta = _tokens(t)
        coincidencias = [u for u, completo, _ in self._usuario_tokens if _abarca(consulta, completo)]
        if not coincidencias:  # La cuenta tiene un nombre más corto («Hugo Zavala» vs «ZAVALA VACA HUGO ALEJANDRO»).
            coincidencias = [u for u, completo, _ in self._usuario_tokens if len(completo) >= 2
                             and _abarca(completo, consulta)]
        coincidencias = list({u.pk or id(u): u for u in coincidencias}.values())
        if len(coincidencias) > 1:  # «Mas, Jean Francois» vs otros Mas: el que abarque más tokens.
            coincidencias = [u for u in coincidencias if _abarca(_tokens(f'{u.first_name} {u.last_name}')[:2], consulta)
                             ] or coincidencias
        return coincidencias[0] if len(coincidencias) == 1 else None

    # -- personas ---------------------------------------------------------------------------------
    def persona(self, nombre):
        """Persona en formato de cita: la de la cuenta si es académico de la entidad; si no, una parecida o nueva."""
        t = titulo(nombre).strip(' ,;')
        if not t or len(t) < 3:
            return None
        usuario = self._usuario_de_cita(t) if ',' in t else self.usuario(t)
        if usuario:
            return usuario.persona
        if ',' in t:
            from nucleo.nombres import partes_cita
            apellidos, nombres = partes_cita(t)
            cita = formato_cita(nombres, apellidos) if nombres else apellidos
        else:
            cita = self._a_cita(t)
        clave = normalizar(cita)
        if clave in self._personas:
            return self._personas[clave]
        parecida = next(iter(personas_parecidas(Persona.objects.all(), cita, limite=1)), None)
        if parecida is None:
            parecida = self.guardar(Persona(nombre=cita[:255]))
            self.personas_creadas += 1
        self._personas[clave] = parecida
        return parecida

    def _usuario_de_cita(self, cita):
        """«Mas, J.-F.» o «Ramírez, M. I.»: apellidos dentro de los de la cuenta e iniciales compatibles."""
        from nucleo.nombres import partes_cita
        from nucleo.similitud import nombres_compatibles

        apellidos, nombres = partes_cita(cita)
        consulta = _tokens(apellidos)
        candidatos = [u for u, _, _ in self._usuario_tokens
                      if _abarca(consulta, _tokens(u.last_name) + _tokens(u.first_name)[1:])
                      and (not nombres or nombres_compatibles(nombres, u.first_name))]
        if len(candidatos) != 1:  # «Astier, Marta» escrito al revés o con nombre completo: el método general.
            return self.usuario(cita) if not candidatos else None
        return candidatos[0]

    @staticmethod
    def _a_cita(nombre_completo):
        """'Saray Bucio Mendoza' → 'Bucio Mendoza, S.'; 'Yadira Méndez-Lemus' → 'Méndez-Lemus, Y.'."""
        partes = nombre_completo.split()
        if len(partes) == 1:
            return nombre_completo
        n_apellidos = 2 if len(partes) >= 3 else 1
        return formato_cita(' '.join(partes[:-n_apellidos]), ' '.join(partes[-n_apellidos:]))

    ROLES = re.compile(r'\((?:coords?|coordinador(?:es|as|a)?|comps?|compilador(?:es|as)?|eds?|editor(?:es|as|a)?|'
                       r'dirs?)\.?\)|\bet al\.?|\(\d{4}\w?\)', re.IGNORECASE)
    VANCOUVER = re.compile(r'^(.+?)\s+([A-Z]{1,3})$')  # «Mas JF», «Ghilardi A»
    INICIALES = re.compile(r'^(?:[A-ZÁÉÍÓÚÑÜ][a-záéíóú]?[.\-:]*\s*){1,4}$')

    def _nombres_en_lista(self, t):
        """Separa una lista de autores en nombres individuales, sea «Apellido, I., Apellido, I.» (pares),
        «Apellido, Nombre; Apellido, Nombre» o «Nombre Apellido, Nombre Apellido»."""
        t = self.ROLES.sub('', t)
        t = re.sub(r'\s+(?:&|y|and|e)\s+', ', ', t)
        if ';' in t:
            return [p.strip(' .,:') for p in t.split(';') if p.strip(' .,:')]
        partes = [p.strip(' .:…') for p in t.split(',') if p.strip(' .:…')]
        segundos = partes[1::2]
        en_pares = segundos and sum(bool(self.INICIALES.match(p)) for p in segundos) * 2 >= len(segundos)
        nombres, i = [], 0
        while i < len(partes):
            siguiente = partes[i + 1] if i + 1 < len(partes) else ''
            # «Apellido, I.» o «Apellido, Nombre» (una sola palabra): es un par; «Nombre Apellido» va solo.
            if siguiente and (en_pares or self.INICIALES.match(siguiente) or (
                    len(siguiente.split()) == 1 and not self.VANCOUVER.match(partes[i]))):
                nombres.append(f'{partes[i]}, {siguiente}')
                i += 2
            else:
                nombres.append(partes[i])
                i += 1
        return nombres

    def autores(self, cadena, adscritos=''):
        """Personas de una lista de autores en cualquiera de los formatos de `_nombres_en_lista`."""
        # Un autor por renglón («Borrego, Armonía⏎Rivas, Hilda»): el salto de línea separa como «;».
        t = texto(re.sub(r'\s*[\r\n]+\s*', '; ', str(cadena)) if cadena else '') or texto(adscritos)
        if not t:
            return []
        resultado = []
        for n in self._nombres_en_lista(t):
            if len(re.sub(r'[^A-Za-zÁÉÍÓÚÑáéíóúñ]', '', n)) < 3 or re.search(r'[()\d]', n):
                continue  # Restos de puntuación, iniciales sueltas o nombres de instituciones.
            vancouver = self.VANCOUVER.match(n) if ',' not in n else None
            if vancouver:
                n = f'{vancouver.group(1)}, {" ".join(vancouver.group(2))}'

            p = self.persona(n)
            if p and p not in resultado:
                resultado.append(p)
        return resultado

    # -- instituciones y revistas -----------------------------------------------------------------
    def institucion(self, nombre, pais=None, padre=None):
        t = titulo(nombre)
        if not t:
            return None
        clave = (normalizar(t), getattr(padre, 'pk', None))
        if clave in self._instituciones:
            return self._instituciones[clave]
        siglas = {normalizar(m) for m in re.findall(r'\(([^)]+)\)', t)}
        base = normalizar(re.sub(r'\([^)]*\)', '', t))
        base = re.sub(r'\s+unam$', '', base).strip() or base  # «ENES Morelia, UNAM» → «enes morelia».
        qs = Institucion.objects.select_related('pais')
        encontrada = None
        enes = re.match(r'^(enes|escuela nacional de estudios superiores)\s+(unidad\s+)?(\w+)', base)
        if enes:  # Las ENES de la UNAM se escriben de muchas formas: «ENES, Morelia», «ENES Morelia, UNAM»…
            encontrada = qs.filter(nombre__iregex=r'\(ENES\) Unidad ' + patron_sin_acentos(enes.group(3))).first()
        for i in ([] if encontrada else qs.filter(nombre__iregex=r'\y' + patron_sin_acentos(base.split()[0]) if base else '.')):
            nombre_i = normalizar(re.sub(r'\([^)]*\)', '', i.nombre))
            siglas_i = {normalizar(m) for m in re.findall(r'\(([^)]+)\)', i.nombre)}
            if nombre_i == base or (siglas and siglas & siglas_i) or base in siglas_i or (
                    len(base) > 12 and SequenceMatcher(None, nombre_i, base).ratio() >= 0.93):
                encontrada = i
                break
        if encontrada is None and len(base) <= 10:  # 'UNAM', 'SECIHTI', 'UMSNH': búsqueda por siglas.
            encontrada = next((i for i in qs.filter(nombre__icontains=f'({t})')), None)
        if encontrada is None:
            encontrada = self.guardar(Institucion(nombre=t[:255], pais=_pais(pais) or self.mexico, padre=padre))
            self._creadas_instituciones = getattr(self, '_creadas_instituciones', 0) + 1
        self._instituciones[clave] = encontrada
        return encontrada

    def revista(self, nombre, pais=None, tipo=Revista.Tipo.CIENTIFICA, abreviado=''):
        t = titulo(nombre)
        if not t:
            return None
        clave = normalizar(t)
        if clave in self._revistas:
            return self._revistas[clave]
        principal = _titulo_principal(t)
        encontrada = None
        palabra = (principal or normalizar(t)).split()[0]
        for r in Revista.objects.filter(nombre__iregex=patron_sin_acentos(palabra)):
            if normalizar(r.nombre) == clave or _titulo_principal(r.nombre) == principal or (
                    len(clave) > 10 and SequenceMatcher(None, normalizar(r.nombre), clave).ratio() >= 0.93):
                encontrada = r
                break
        if encontrada is None and abreviado:
            encontrada = Revista.objects.filter(nombre_abreviado__iexact=abreviado).first()
        if encontrada is None:
            encontrada = self.guardar(Revista(nombre=t[:255], tipo=tipo, pais=_pais(pais) or self.mexico,
                                              nombre_abreviado=texto(abreviado)[:255]))
            self._creadas_revistas = getattr(self, '_creadas_revistas', 0) + 1
        self._revistas[clave] = encontrada
        return encontrada


def leer_hoja(libro, nombre, fila_encabezado=0, columnas_previas=()):
    """Filas de una hoja como diccionarios {encabezado normalizado: valor}, con el número de fila del Excel.

    `columnas_previas`: nombres de columnas que los datos traen antes del primer encabezado (hojas desfasadas)."""
    ws = libro[nombre]
    filas = list(ws.iter_rows(values_only=True))
    encabezados = list(columnas_previas) + [normalizar(texto(c)) for c in filas[fila_encabezado]]
    vistos = defaultdict(int)
    claves = []
    for e in encabezados:
        vistos[e] += 1
        claves.append(e if vistos[e] == 1 else f'{e} {vistos[e]}')
    for numero_fila, fila in enumerate(filas[fila_encabezado + 1:], start=fila_encabezado + 2):
        if not any(texto(c) for c in fila):
            continue
        yield numero_fila, dict(zip(claves, fila))
