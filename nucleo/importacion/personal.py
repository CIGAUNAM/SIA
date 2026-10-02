"""Planta académica: cuentas, datos personales y situación por año (nombramiento, PRIDE, SNII, contrato)."""

import re
from datetime import date

from nucleo.models import Nombramiento, SituacionAcademica, User

from nucleo.similitud import normalizar

from .base import fecha_celda, leer_hoja, numero, texto

ARCHIVO = 'Eje2_PlantaAcademica_CISIC_2023-2026_GC.xlsx'
ANIOS = {2023: ('categoria y nivel sic 2023 ago 2023', 'nivel pride ago 2023', 'nivel snii ago 2023'),
         2024: ('categoria y nivel sic 2024 ago 2024', 'nivel pride ago 2024', 'nivel snii ago 2024'),
         2025: ('cat nivel infociga2025 ago 2025', 'nivel pride ago 2025', 'nivel snii ago 2025'),
         2026: ('cat nivel infociga2026 ago 2026', 'nivel pride ago 2026', 'snii ago 2026')}
ANIO_CORTE = 2026
GRADOS = {'DOCTORADO': ('Dr.', 'Dra.'), 'MAESTRIA': ('Mtro.', 'Mtra.'), 'LICENCIATURA': ('Lic.', 'Lic.')}
SNI = {'i': 'I', 'ii': 'II', 'iii': 'III', 'emerito': 'E', 'emérito': 'E', 'candidato': 'C', 'c': 'C'}
CONTRATOS = {'DEFINITIVO': 'DEFINITIVO', 'INTERINO': 'INTERINO', 'OBRA DETERMINADA': 'OBRA_DETERMINADA'}


def nombramiento(codigo):
    """'INV TIT B TC' → Investigador Titular B, Tiempo Completo; 'TEC ACAD ASO C TC' → Técnico Académico Asociado C…"""
    t = texto(codigo).upper()
    m = re.match(r'(INV|TEC ACAD)\s+(TIT|ASOC?|AUX)\s+([ABC])\s*(TC|MT)?', t)
    if not m:
        return None
    base = 'Investigador' if m.group(1) == 'INV' else 'Técnico Académico'
    categoria = {'TIT': 'Titular', 'ASO': 'Asociado', 'ASOC': 'Asociado', 'AUX': 'Auxiliar'}[m.group(2)]
    tiempo = 'Medio tiempo' if m.group(4) == 'MT' else 'Tiempo Completo'
    return Nombramiento.objects.filter(nombre=f'{base} {categoria} {m.group(3)}, {tiempo}').first()


def pride(valor):
    t = texto(valor).upper()
    if t.startswith('PRIDE '):
        return t[-1]
    return SituacionAcademica.Pride.EQUIVALENCIA if t.startswith('EQUIVALENCIA') else ''


def sni(valor):
    return SNI.get(texto(valor).lower(), '')


def _nombre_propio(texto_mayusculas):
    return ' '.join(p.lower() if p in {'DE', 'LA', 'DEL', 'LAS', 'LOS', 'Y'} else p.capitalize()
                    for p in texto_mayusculas.split())


def importar(ctx, libro):
    hoja = ctx.hoja(f'{ARCHIVO} › Personal CIGA actualizada')
    for fila, f in leer_hoja(libro, 'Personal CIGA actualizada'):
        with ctx.fila(hoja, fila):
            nombre = texto(f['nombre'])
            if not nombre:
                continue
            hoja.filas += 1
            usuario = ctx.usuario(nombre)
            mujer = texto(f['sexo']).upper().startswith('F')
            if usuario is None:
                # «APELLIDO1 APELLIDO2 NOMBRES»: los dos primeros son apellidos (salvo apellidos compuestos raros).
                partes = nombre.split()
                apellidos, nombres = _nombre_propio(' '.join(partes[:2])), _nombre_propio(' '.join(partes[2:]))
                correo = re.sub(r'[^a-z.]', '', f'{nombres.split()[0]}.{apellidos.split()[0]}'.lower()
                                .translate(str.maketrans('áéíóúñü', 'aeiounu'))) + '@sin-correo.invalid'
                usuario = User(email=correo, first_name=nombres, last_name=apellidos, is_active=True, is_staff=True)
                usuario.set_unusable_password()
                hoja.creado(User)
            else:
                hoja.existente(User)
            categoria = normalizar(texto(f['categoria']))
            usuario.tipo = User.Tipo.TECNICO if categoria.startswith('tec') else User.Tipo.INVESTIGADOR
            usuario.numero_trabajador = usuario.numero_trabajador or str(numero(f['clave academico']) or '')
            usuario.fecha_nacimiento = usuario.fecha_nacimiento or fecha_celda(f['fecha de nacimiento'], por_defecto=None)
            usuario.genero = usuario.genero or (User.Genero.FEMENINO if mujer else User.Genero.MASCULINO)
            grado = GRADOS.get(texto(f['grado academico']).upper())
            usuario.grado = usuario.grado or (grado[1 if mujer else 0] if grado else '')
            antiguedad = numero(f['antiguedad 2026'])  # Antigüedad académica en la UNAM al corte de agosto.
            if usuario.ingreso_unam is None and antiguedad is not None:
                usuario.ingreso_unam = date(ANIO_CORTE - antiguedad, 8, 1)
            if texto(f['tipo de contrato']).upper() == 'BAJA' and usuario.egreso_entidad is None:
                usuario.egreso_entidad = date(ANIO_CORTE, 8, 1)
            ctx.guardar(usuario)
            ctx.registrar_usuario(usuario)
            if not any(texto(f[c]) for c in ('formacion lic', 'formacion mae', 'formacion doc')):
                pass
            elif not usuario.grados.exists():
                hoja.aviso(fila, f'{usuario}: la formación (LIC/MAE/DOC) solo trae la disciplina, sin institución ni '
                                 'fecha; no se puede registrar como grado académico.')

            area = texto(f['area snii'])
            for anio_, (col_cat, col_pride, col_sni) in ANIOS.items():
                codigo = texto(f[col_cat])
                if codigo.upper() == 'BAJA':  # Se fue al cierre: cuenta en el periodo con su último nombramiento.
                    codigo = texto(f[ANIOS[anio_ - 1][0]]) if anio_ - 1 in ANIOS else ''
                    if not codigo:
                        continue
                situacion, creada = SituacionAcademica.objects.get_or_create(usuario=usuario, anio=anio_)
                situacion.nombramiento = nombramiento(codigo)
                if codigo and situacion.nombramiento is None and codigo.lower() != 'sin nivel':
                    hoja.aviso(fila, f'{usuario} {anio_}: nombramiento «{codigo}» no está en el catálogo.')
                situacion.pride = pride(f[col_pride])
                situacion.sni = sni(f[col_sni])
                situacion.area_sni = area if situacion.sni else ''
                if anio_ == ANIO_CORTE:
                    situacion.contrato = CONTRATOS.get(texto(f['tipo de contrato']).upper(), '')
                ctx.guardar(situacion)
                (hoja.creado if creada else hoja.existente)(SituacionAcademica)
            ultima = usuario.situaciones.order_by('-anio').first()
            if ultima:  # El perfil muestra lo vigente.
                usuario.pride = ultima.pride if ultima.pride in User.Pride.values else ''
                usuario.sni = ultima.sni
                ctx.guardar(usuario)
    posdoctorantes(ctx)
    return hoja


ARCHIVO_POSDOCS = 'Eje3_Docencia_GC_IR_300826.xlsx'


def posdoctorantes(ctx):
    """Cuentas de posdoctorantes e Investigadores por México (IxM), con sus fechas en la entidad."""
    from .base import fecha

    hoja = ctx.hoja(f'{ARCHIVO_POSDOCS} › IxMx & Posdoctorales (cuentas)')
    for fila, f in leer_hoja(ctx.libro(ARCHIVO_POSDOCS), 'IxMx & Posdoctorales'):
        with ctx.fila(hoja, fila):
            nombre = re.sub(r'^(Dra?|Mtr[oa])\.\s*', '', texto(f['nombre de estudiante']))
            if not nombre:
                continue
            hoja.filas += 1
            ixm = 'ixm' in texto(f['tipo de participacion']).lower()
            usuario = ctx.usuario(nombre)
            if usuario is None:
                partes = nombre.split()
                corte = -2 if len(partes) >= 3 else -1
                local = re.sub(r'[^a-z.]', '', f'{partes[0]}.{partes[corte]}'.lower().translate(
                    str.maketrans('áéíóúñü', 'aeiounu')))
                usuario = User(email=f'{local}@sin-correo.invalid', first_name=' '.join(partes[:corte]),
                               last_name=' '.join(partes[corte:]), is_active=True, is_staff=True)
                usuario.set_unusable_password()
                hoja.creado(User)
            else:
                hoja.existente(User)
            usuario.tipo = User.Tipo.INVESTIGADOR if ixm else User.Tipo.POSTDOCTORADO
            usuario.genero = usuario.genero or (User.Genero.FEMENINO if texto(f['genero']).lower().startswith('f')
                                                else User.Genero.MASCULINO)
            inicio = fecha(f['dia'], f['mes de inicio'], f['ano de inicio'])
            usuario.ingreso_entidad = usuario.ingreso_entidad or inicio
            if texto(f['ano fin']):
                usuario.egreso_entidad = usuario.egreso_entidad or fecha(f['dia fin'], f['mes fin'], f['ano fin'])
            ctx.guardar(usuario)
            ctx.registrar_usuario(usuario)
            if ixm:
                for anio_ in range(max(inicio.year, 2023), ANIO_CORTE + 1):
                    situacion, creada = SituacionAcademica.objects.get_or_create(usuario=usuario, anio=anio_)
                    situacion.contrato = SituacionAcademica.Contrato.IXM
                    ctx.guardar(situacion)
                    (hoja.creado if creada else hoja.existente)(SituacionAcademica)
    return hoja

