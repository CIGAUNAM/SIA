"""Eje 3 · Docencia y formación de recursos humanos: tesis, comités tutorales y de candidatura, sinodalías,
becarios, estancias, servicio social, movilidad estudiantil, premios de estudiantes, posdoctorantes y cursos."""

import re
from datetime import date, datetime

from distinciones.models import DistincionAlumno
from docencia.models import CursoEscolarizado, CursoExtracurricular
from formacion_recursos_humanos.models import (AsesoriaEstudiante, ComiteCandidaturaDoctoral, ComiteCandidaturaMiembro,
                                               ComiteTutoral, ComiteTutoralMiembro, DireccionTesis, JuradoExamen,
                                               MovilidadEstudiante, SupervisionPostdoctoral)
from nucleo.models import (Asignatura, Beca, Distincion, Modalidad, ModalidadBeca, NivelAcademico, ProgramaAcademico,
                           SIN_FECHA)
from nucleo.similitud import normalizar

from .base import _pais, fecha, inicio_periodo, leer_hoja, numero, texto, titulo
from .produccion import _participantes

ARCHIVO = 'Eje3_Docencia_GC_IR_300826.xlsx'
N = NivelAcademico


def nivel(valor, programa=''):
    t = normalizar(f'{texto(valor)} {texto(programa)}')
    if 'doc' in t:
        return N.DOCTORADO
    if 'maest' in t or t.startswith('mae'):
        return N.MAESTRIA
    if 'lic' in t or 'ingenier' in t:
        return N.LICENCIATURA
    return N.MAESTRIA if 'posgrado' in t else N.LICENCIATURA


def programa(ctx, valor, nivel_):
    """'DOC Geografía' → programa «Geografía» de doctorado (sin duplicar «Doctorado en Geografía»)."""
    t = re.sub(r'^(DOC|MAE|LIC|MTRIA|ESP)\.?\s+', '', titulo(valor), flags=re.IGNORECASE).strip()
    if not t or t == '?':
        return None
    base = re.sub(r'^(doctorado|maestria|licenciatura|posgrado|programa de doctorado)\s+(en|de)\s+', '', normalizar(t))
    cache = ctx.__dict__.setdefault('_programas', {})
    if (base, nivel_) in cache:
        return cache[(base, nivel_)]
    for p in ProgramaAcademico.objects.filter(nivel=nivel_):
        otro = re.sub(r'^(doctorado|maestria|licenciatura|posgrado)\s+(en|de)\s+', '', normalizar(p.nombre))
        if otro == base:
            cache[(base, nivel_)] = p
            return p
    p = ctx.guardar(ProgramaAcademico(nombre=t[:255], nivel=nivel_))
    cache[(base, nivel_)] = p
    return p


def estudiante(ctx, nombre, f):
    persona = ctx.persona(re.sub(r'^(Dra?|Mtr[oa]|Lic)\.\s*', '', texto(nombre)))
    if persona is None:
        return None
    genero = normalizar(texto(f.get('genero')))
    cambios = False
    if genero and not persona.genero:
        persona.genero = 'FEMENINO' if genero.startswith('f') else 'MASCULINO' if genero.startswith('m') else 'OTRO'
        cambios = True
    pais = _pais(f.get('nacionalidad'))
    if pais and not persona.nacionalidad_id:
        persona.nacionalidad = pais
        cambios = True
    if cambios:
        ctx.guardar(persona)
    return persona


def institucion(ctx, f, col='institucion', col_dep='dependencia'):
    inst = ctx.institucion(f.get(col))
    dep = texto(f.get(col_dep))
    if dep and (not inst or normalizar(dep) != normalizar(inst.nombre)):
        return ctx.institucion(dep, padre=inst) or inst
    return inst or ctx.institucion('UNAM')


def beca(valor, nivel_):
    t = normalizar(texto(valor))
    if not t or t in ('no tiene', 'si', 'otros', 'unam'):
        return None
    if 'paep' in t:
        nombre = 'Programa de Apoyo a los Estudios de Posgrado (PAEP)'
    elif 'papiit' in t:
        nombre = 'Programa de Apoyo a Proyectos de Investigación e Innovación Tecnológica (PAPIIT)'
    elif 'papime' in t:
        nombre = 'Programa de Apoyo a Proyectos para Innovar y Mejorar la Educación (PAPIME)'
    elif 'dgapa' in t:
        nombre = 'Programa de Becas Posdoctorales en la UNAM (POSDOC)'
    elif 'posdoc' in t:
        nombre = 'Estancias Posdoctorales por México'
    elif 'secihti' in t or 'conacyt' in t:
        nombre = 'Beca de proyecto' if nivel_ == N.LICENCIATURA else 'Becas Nacionales para Estudios de Posgrado'
        return Beca.objects.filter(nombre=nombre, institucion__nombre__icontains='SECIHTI').first()
    else:
        return None
    return Beca.objects.filter(nombre=nombre).first()


def modalidad_beca(valor):
    t = normalizar(texto(valor))
    for clave, m in (('titula', ModalidadBeca.TITULACION), ('grado', ModalidadBeca.TITULACION),
                     ('conclusion', ModalidadBeca.CONCLUSION), ('movilidad', ModalidadBeca.MOVILIDAD),
                     ('doctorado', ModalidadBeca.DOCTORADO), ('maestria', ModalidadBeca.MAESTRIA),
                     ('licenciatura', ModalidadBeca.LICENCIATURA), ('estudios', ModalidadBeca.MAESTRIA)):
        if clave in t:
            return m
    return ''


# --------------------------------------------------------------------------------------------------- Formación RH
def formacion(ctx, libro):
    hoja = ctx.hoja(f'{ARCHIVO} › Formación RH')
    for fila, f in leer_hoja(libro, 'Formación RH'):
        with ctx.fila(hoja, fila):
            tipo = normalizar(texto(f['tipo de participacion']))
            if not tipo or not texto(f['nombre de estudiante']):
                continue
            hoja.filas += 1
            usuarios = ctx.cuentas(f['registrado por'], hoja, fila)
            # Una tesis que registró un tutor externo del posgrado entra con él como persona (sin cuenta); lo demás
            # (comités, sinodalías, movilidad…) es solo del personal de la entidad.
            externo = None if usuarios or 'direccion de tesis' not in tipo else ctx.persona(f['registrado por'])
            if not usuarios and externo is None:
                hoja.rechazo(fila, f'«{texto(f["registrado por"])}» no es personal de la entidad (no tiene cuenta).')
                continue
            usuario, otros = (usuarios[0] if usuarios else None), [u.persona for u in usuarios[1:]]
            alumno = estudiante(ctx, f['nombre de estudiante'], f)
            nivel_ = nivel(f['grado academico'], f.get('programa academico carrera'))
            prog = programa(ctx, f.get('programa academico carrera'), nivel_)
            inst = institucion(ctx, f)
            periodo_inicio = inicio_periodo(f['periodo'])
            inicio = fecha(f.get('dia'), f['mes de inicio'], f['ano de inicio'], por_defecto=periodo_inicio)
            fin = fecha(f.get('dia fin'), f['mes fin'], f['ano fin'], por_defecto=None) if texto(f['ano fin']) else None
            titulo_ = titulo(f.get('titulo de tesis o proyecto'))
            tutor = ctx.persona(f.get('nombre del tutor principal'))
            if tutor is None and otros:
                tutor = otros[0] if 'direccion de tesis' not in tipo else None
            if 'direccion de tesis' in tipo and 'concluida' in tipo:
                fin = ctx.en_periodo_reportado(fin, f['periodo'], hoja, fila, 'El examen')
            if 'direccion de tesis' in tipo:
                tesis(ctx, hoja, fila, f, usuario.persona if usuario else externo, alumno, nivel_, prog, inst, inicio, fin,
                      titulo_, tutor,
                      concluida='concluida' in tipo, codirector=otros[0] if otros else None)
            elif 'comites tutorales' in tipo:
                if ComiteTutoral.objects.filter(estudiante=alumno, comitetutoralmiembro__persona=usuario.persona).exists():
                    hoja.existente(ComiteTutoral)
                    continue
                comite = ctx.guardar(ComiteTutoral(estudiante=alumno, nivel=nivel_, programa=prog, titulo_tesis=titulo_[:255],
                                                   institucion=inst, fecha_inicio=inicio, fecha_fin=fin))
                _participantes(ctx, ComiteTutoralMiembro, 'comite', comite,
                               [p for p in (tutor, usuario.persona, *otros) if p])
                hoja.creado(ComiteTutoral)
            elif 'candidatura' in tipo:
                defensa = fin or inicio
                if ComiteCandidaturaDoctoral.objects.filter(candidato=alumno, fecha_defensa=defensa).exists():
                    hoja.existente(ComiteCandidaturaDoctoral)
                    continue
                comite = ctx.guardar(ComiteCandidaturaDoctoral(candidato=alumno, titulo_tesis=titulo_[:255], programa=prog,
                                                               institucion=inst, fecha_defensa=defensa, director=tutor))
                _participantes(ctx, ComiteCandidaturaMiembro, 'comite', comite, [usuario.persona, *otros])
                hoja.creado(ComiteCandidaturaDoctoral)
            elif 'sinodal' in tipo:
                examen = fin or inicio
                if JuradoExamen.objects.filter(usuario=usuario, estudiante=alumno, fecha_examen=examen).exists():
                    hoja.existente(JuradoExamen)
                    continue
                ctx.guardar(JuradoExamen(estudiante=alumno, nivel=nivel_, programa=prog, titulo_tesis=titulo_[:255],
                                         tutor=tutor, institucion=inst, fecha_examen=examen, usuario=usuario))
                hoja.creado(JuradoExamen)
            elif 'movilidad' in tipo:
                movilidad(ctx, hoja, f, usuario, alumno, nivel_, prog, inicio, fin, f.get('inst receptora'),
                          f.get('pais de movilidad'), f.get('tipo de beca'))
            elif 'premio' in tipo:
                premio(ctx, hoja, f, usuario, alumno, nivel_, inicio)
            else:
                tipo_asesoria = {'becario': AsesoriaEstudiante.Tipo.BECARIO, 'estancia': AsesoriaEstudiante.Tipo.ESTANCIA,
                                 'servicio': AsesoriaEstudiante.Tipo.SERVICIO_SOCIAL}
                t = next((v for k, v in tipo_asesoria.items() if k in tipo), None)
                if t is None:
                    hoja.rechazo(fila, f'Tipo de participación no reconocido: «{texto(f["tipo de participacion"])}».')
                    continue
                asesoria(ctx, hoja, usuario, alumno, t, nivel_, prog, inst, inicio, fin,
                         beca(f.get('cuenta con beca'), nivel_), modalidad_beca(f.get('tipo de beca')))
    return hoja


def tesis(ctx, hoja, fila, f, responsable, alumno, nivel_, prog, inst, inicio, fin, titulo_, tutor, concluida,
          codirector=None):
    if not titulo_:
        titulo_ = f'Tesis de {alumno} ({N(nivel_).label.lower()})'
        hoja.aviso(fila, f'Tesis de «{alumno}» sin título en el Excel: se registró como «{titulo_}».')
    existente = DireccionTesis.objects.filter(titulo_tesis__iexact=titulo_[:255]).first()
    if existente:
        if concluida and existente.status != DireccionTesis.Status.TERMINADA:
            existente.status, existente.fecha_examen = DireccionTesis.Status.TERMINADA, fin or existente.fecha_examen
            ctx.guardar(existente)
        hoja.existente(DireccionTesis)
        return
    director, codirector = responsable, codirector or ctx.persona(f.get('cotutor'))
    if tutor and tutor != responsable:
        director, codirector = tutor, responsable
    beca_ = beca(f.get('cuenta con beca'), nivel_)
    reconocimiento = texto(f.get('reconocimiento'))
    t = DireccionTesis(titulo_tesis=titulo_[:255], nivel=nivel_, programa=prog, asesorado=alumno, institucion=inst,
                       status=DireccionTesis.Status.TERMINADA if concluida else DireccionTesis.Status.EN_PROCESO,
                       fecha_inicio=inicio if inicio != SIN_FECHA else (fin or SIN_FECHA),
                       fecha_fin=fin if concluida else None, fecha_examen=fin if concluida else None,
                       beca=beca_, modalidad_beca=modalidad_beca(f.get('tipo de beca')) if beca_ else '',
                       director=director, codirector=codirector if codirector != director else None)
    if reconocimiento:
        t.reconocimiento = Distincion.objects.filter(nombre='Mención en examen de grado').first()
        t.detalle_reconocimiento = reconocimiento[:255]
    if t.fecha_fin and t.fecha_fin < t.fecha_inicio:
        t.fecha_inicio = t.fecha_fin
    ctx.guardar(t)
    hoja.creado(DireccionTesis)


def asesoria(ctx, hoja, usuario, alumno, tipo, nivel_, prog, inst, inicio, fin, beca_, modalidad):
    if AsesoriaEstudiante.objects.filter(usuario=usuario, asesorado=alumno, tipo=tipo, fecha_inicio=inicio).exists():
        hoja.existente(AsesoriaEstudiante)
        return
    ctx.guardar(AsesoriaEstudiante(asesorado=alumno, tipo=tipo, nivel=nivel_, programa=prog, institucion=inst,
                                   fecha_inicio=inicio, fecha_fin=fin if fin and fin >= inicio else None, beca=beca_,
                                   modalidad_beca=modalidad if beca_ else '', usuario=usuario))
    hoja.creado(AsesoriaEstudiante)


def movilidad(ctx, hoja, f, usuario, alumno, nivel_, prog, inicio, fin, receptora, pais, beca_txt):
    if MovilidadEstudiante.objects.filter(estudiante=alumno, fecha_inicio=inicio).exists():
        hoja.existente(MovilidadEstudiante)
        return
    receptora_ = ctx.institucion(receptora, pais)
    if receptora_ is None:
        hoja.rechazo('-', f'Movilidad de «{alumno}» sin institución receptora.')
        return
    ctx.guardar(MovilidadEstudiante(estudiante=alumno, nivel=nivel_, programa=prog, institucion_receptora=receptora_,
                                    beca=beca(beca_txt, nivel_), detalle_beca=texto(beca_txt)[:255],
                                    fecha_inicio=inicio, fecha_fin=fin if fin and fin >= inicio else None,
                                    usuario=usuario))
    hoja.creado(MovilidadEstudiante)


def premio(ctx, hoja, f, usuario, alumno, nivel_, inicio):
    nombre = normalizar(texto(f.get('premio')))
    distincion = Distincion.objects.filter(
        nombre__icontains='Sánchez Crispín' if 'crispin' in nombre else 'Investigación de Campo' if 'campo' in nombre
        else 'cartel científico' if 'cartel' in nombre else texto(f.get('premio'))[:40]).first()
    if distincion is None:
        hoja.rechazo('-', f'Premio no está en el catálogo de distinciones: «{texto(f.get("premio"))}».')
        return
    if DistincionAlumno.objects.filter(alumno=alumno, distincion=distincion).exists():
        hoja.existente(DistincionAlumno)
        return
    d = ctx.guardar(DistincionAlumno(distincion=distincion, alumno=alumno, nivel=nivel_, fecha=inicio,
                                     institucion=ctx.institucion(f.get('institucion otorgante'))))
    d.tutores.add(usuario.persona)
    hoja.creado(DistincionAlumno)


def hojas_sueltas(ctx, libro):
    """«Movilidad» y «Premios» repiten filas de Formación RH: entran solo las que falten."""
    hoja = ctx.hoja(f'{ARCHIVO} › Movilidad / Premios')
    for fila, f in leer_hoja(libro, 'Movilidad'):
        with ctx.fila(hoja, fila):
            if not texto(f['nombre de estudiante']):
                continue
            hoja.filas += 1
            usuario = ctx.cuenta(f['nombre del tutor principal'], hoja, fila)
            if usuario is None:
                hoja.rechazo(fila, f'No se reconoce al tutor «{texto(f["nombre del tutor principal"])}».')
                continue
            alumno = estudiante(ctx, f['nombre de estudiante'], f)
            nivel_ = nivel(f['grado academico'], f['programa academico carrera'])
            movilidad(ctx, hoja, f, usuario, alumno, nivel_, programa(ctx, f['programa academico carrera'], nivel_),
                      fecha(None, f['mes de inicio'], f['ano de inicio']), fecha(None, f['mes de fin'], f['ano de fin']),
                      f['institucion receptora'], f['pais'], f['tipo de beca'])
    for fila, f in leer_hoja(libro, 'Premios'):
        with ctx.fila(hoja, fila):
            if not texto(f['nombre de estudiante']):
                continue
            hoja.filas += 1
            usuario = ctx.cuenta(f['nombre del tutor principal'], hoja, fila)
            if usuario is None:
                hoja.rechazo(fila, f'No se reconoce al tutor «{texto(f["nombre del tutor principal"])}».')
                continue
            alumno = estudiante(ctx, f['nombre de estudiante'], f)
            premio(ctx, hoja, f, usuario, alumno, nivel(f['grado academico']), fecha(None, f['mes de inicio'],
                                                                                    f['ano de inicio']))
    return hoja


# --------------------------------------------------------------------------------------------------- posdocs
def posdoctorados(ctx, libro):
    hoja = ctx.hoja(f'{ARCHIVO} › IxMx & Posdoctorales')
    for fila, f in leer_hoja(libro, 'IxMx & Posdoctorales'):
        with ctx.fila(hoja, fila):
            nombre = re.sub(r'^(Dra?|Mtr[oa])\.\s*', '', texto(f['nombre de estudiante']))
            if not nombre:
                continue
            hoja.filas += 1
            tutor = ctx.cuenta(f['registrado por'], hoja, fila)
            posdoc = ctx.usuario(nombre)
            if tutor is None or posdoc is None:
                hoja.rechazo(fila, f'No se reconoce a «{texto(f["registrado por"])}» o a «{nombre}».')
                continue
            inicio = fecha(f['dia'], f['mes de inicio'], f['ano de inicio'])
            if SupervisionPostdoctoral.objects.filter(investigador=posdoc.persona, fecha_inicio=inicio).exists():
                hoja.existente(SupervisionPostdoctoral)
                continue
            ixm = 'ixm' in normalizar(texto(f['tipo de participacion']))
            beca_ = Beca.objects.filter(nombre='Investigadoras e Investigadores por México').first() if ixm \
                else beca(f['cuenta con beca'], N.DOCTORADO)
            fin = fecha(f['dia fin'], f['mes fin'], f['ano fin']) if texto(f['ano fin']) else None
            ctx.guardar(SupervisionPostdoctoral(
                investigador=posdoc.persona, titulo_proyecto=titulo(f['titulo de tesis o proyecto'])[:200] or '—',
                institucion=ctx.institucion(f['institucion']), beca=beca_, modalidad_beca=ModalidadBeca.POSDOCTORAL,
                fecha_inicio=inicio, fecha_fin=fin, usuario=tutor))
            hoja.creado(SupervisionPostdoctoral)
    return hoja


# --------------------------------------------------------------------------------------------------- cursos
def _semestre(valor, inicio):
    if isinstance(valor, datetime):
        return f'{valor.year}-{1 if valor.month <= 6 else 2}'
    return texto(valor)[:20] or f'{inicio.year}-{1 if inicio.month <= 6 else 2}'


def _modalidad(valor):
    t = normalizar(texto(valor))
    return Modalidad.EN_LINEA if 'linea' in t else Modalidad.MIXTO if 'hibrid' in t or 'mixt' in t else Modalidad.PRESENCIAL


def _asignatura(ctx, nombre):
    a = Asignatura.objects.filter(nombre__iexact=nombre[:255]).first()
    return a or ctx.guardar(Asignatura(nombre=nombre[:255]))


def cursos(ctx, libro):
    hoja = ctx.hoja(f'{ARCHIVO} › CursosESCOLARIZADOS')
    for fila, f in leer_hoja(libro, 'CursosESCOLARIZADOS'):
        with ctx.fila(hoja, fila):
            materia = titulo(f['curso materia'])
            if not materia:
                continue
            hoja.filas += 1
            usuarios = ctx.cuentas(f['coordinador titular'], hoja, fila)
            if not usuarios:
                hoja.rechazo(fila, f'No se reconoce al académico «{texto(f["coordinador titular"])}».')
                continue
            for usuario in usuarios:
                inicio = fecha(None, f['mes inicio'], f['ano inicio'], por_defecto=inicio_periodo(f['periodo']))
                asignatura = _asignatura(ctx, materia)
                if CursoEscolarizado.objects.filter(usuario=usuario, asignatura=asignatura, fecha_inicio=inicio).exists():
                    hoja.existente(CursoEscolarizado)
                    continue
                nivel_ = nivel(f['nivel'], f['carrera programa'])
                fin = fecha(None, f['mes fin'], f['ano fin'], por_defecto=inicio)
                impartido = texto(f['impartido en'])
                inst = ctx.institucion(impartido.split(',')[0]) if impartido else ctx.institucion('UNAM')
                ctx.guardar(CursoEscolarizado(
                    nivel=nivel_, programa=programa(ctx, f['carrera programa'], nivel_), asignatura=asignatura,
                    modalidad=_modalidad(f['tipo de curso 2']),
                    nombramiento=CursoEscolarizado.Nombramiento.TITULAR if 'titular' in texto(f['nivel de participacion']).lower()
                    else CursoEscolarizado.Nombramiento.COLABORADOR,
                    institucion=inst, periodo_academico=_semestre(f['semestre'], inicio),
                    total_horas=numero(f['horas totales impartidas en la materia o curso al semestre']) or 0,
                    fecha_inicio=inicio, fecha_fin=max(fin, inicio), usuario=usuario))
                hoja.creado(CursoEscolarizado)
    return hoja


def cursos_extracurriculares(ctx, libro):
    hoja = ctx.hoja(f'{ARCHIVO} › Cursos_NO_ESCOLARIZADOS')
    C = CursoExtracurricular
    for fila, f in leer_hoja(libro, 'Cursos_NO_ESCOLARIZADOS '):
        with ctx.fila(hoja, fila):
            nombre = titulo(f['curso materia'])
            if not nombre:
                continue
            hoja.filas += 1
            usuarios = ctx.cuentas(f['coordinador titular'], hoja, fila)
            if not usuarios:
                hoja.rechazo(fila, f'No se reconoce al académico «{texto(f["coordinador titular"])}».')
                continue
            for usuario in usuarios:
                inicio = fecha(None, f['mes inicio'], f['ano inicio'], por_defecto=inicio_periodo(f['periodo']))
                asignatura = _asignatura(ctx, nombre)
                if C.objects.filter(usuario=usuario, asignatura=asignatura, fecha_inicio=inicio).exists():
                    hoja.existente(C)
                    continue
                fin = fecha(None, f['mes fin'], f['ano fin'], por_defecto=inicio)
                programa_ = normalizar(texto(f['programa']))
                ctx.guardar(C(asignatura=asignatura,
                              tipo=C.Tipo.DIPLOMADO if 'diplomado' in normalizar(texto(f['tipo de curso'])) else C.Tipo.CURSO,
                              clasificacion=C.Clasificacion.APOYO_POSGRADO if 'posgrado' in programa_ else C.Clasificacion.CAPACITACION,
                              modalidad=_modalidad(f['tipo de curso 2']), institucion=ctx.institucion(f['impartido en']) or
                              ctx.institucion('CIGA'), total_horas=numero(f['horas totales impartidas en la materia o curso al semestre']) or 0,
                              numero_asistentes=numero(f['asistentes']), fecha_inicio=inicio, fecha_fin=max(fin, inicio),
                              usuario=usuario))
                hoja.creado(C)
    return hoja


def importar(ctx, libro):
    posdoctorados(ctx, libro)
    formacion(ctx, libro)
    hojas_sueltas(ctx, libro)
    cursos(ctx, libro)
    cursos_extracurriculares(ctx, libro)
    hoja = ctx.hoja(f'{ARCHIVO} › Formación de recursos human / Docencia')
    hoja.aviso('-', 'Son exportaciones crudas del sistema de captura que alimentaron «Formación RH», '
                    '«CursosESCOLARIZADOS» y «Cursos_NO_ESCOLARIZADOS»; no se importan para no contar dos veces.')
