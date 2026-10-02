"""Eje 2 · Vinculación académica: eventos organizados y participaciones, arbitrajes, comités editoriales,
comisiones de evaluación, órganos colegiados, redes, sociedades científicas y movilidad (sabáticos, estancias,
visitantes)."""

import re

from compromiso_institucional.models import Comision, ComisionInstitucional
from difusion_cientifica.models import OrganizacionEventoAcademico, ParticipacionEventoAcademico, \
    ParticipacionEventoAcademicoAutor
from distinciones.models import SociedadCientifica
from movilidad_academica.models import MovilidadAcademica
from nucleo.models import SIN_FECHA, Ambito, Evento, Revista, TipoEvento
from nucleo.similitud import normalizar
from vinculacion.models import ArbitrajePublicacion, ConsejoEditorial, OtraComision, RedAcademica, TipoComision

from .base import _pais, anio, fecha, fecha_en_periodo, inicio_periodo, leer_hoja, mes, numero, si_no, texto, titulo
from .produccion import _indices, _participantes

ARCHIVO = 'Eje2_VinculacionAcademica_GC_IR_010926.xlsx'
F = ComisionInstitucional.Funcion
TIPOS_EVENTO = {'coloqui': 'Coloquio', 'congres': 'Congreso', 'sesion': 'Sesión de congreso', 'seminari': 'Seminario',
                'taller': 'Taller', 'mesa': 'Mesa redonda', 'reunion': 'Reunión', 'simposi': 'Simposio',
                'encuentro': 'Encuentro', 'jornada': 'Jornada', 'conversatori': 'Conversatorio', 'foro': 'Foro',
                'diplomado': 'Diplomado', 'conferencia': 'Conferencia', 'feria': 'Feria', 'curso': 'Curso',
                'exposici': 'Exposición', 'festival': 'Festival', 'presentaci': 'Presentación de libro'}


def ambito(valor, por_defecto=Ambito.NACIONAL):
    t = normalizar(texto(valor))
    return next((v for clave, v in (('internac', Ambito.INTERNACIONAL), ('extranj', Ambito.INTERNACIONAL),
                                    ('nacional', Ambito.NACIONAL), ('mexican', Ambito.NACIONAL),
                                    ('institucional', Ambito.INSTITUCIONAL), ('estatal', Ambito.REGIONAL),
                                    ('regional', Ambito.REGIONAL), ('local', Ambito.LOCAL)) if clave in t), por_defecto)


def tipo_evento(ctx, valor):
    t = normalizar(texto(valor))
    nombre = next((n for clave, n in TIPOS_EVENTO.items() if clave in t), None) or (texto(valor).capitalize() or 'Otro')
    tipo = TipoEvento.objects.filter(nombre__iexact=nombre).first()
    return tipo or ctx.guardar(TipoEvento(nombre=nombre[:100]))


def evento(ctx, nombre, tipo, inicio, fin, pais, ciudad, ambito_, ponentes=None, asistentes=None, vistas=None):
    obj = Evento.objects.filter(nombre__iexact=nombre, fecha_inicio=inicio).first()
    if obj is None:
        obj = Evento(nombre=nombre[:255], tipo=tipo, fecha_inicio=inicio, fecha_fin=max(fin or inicio, inicio),
                     pais=pais or ctx.mexico, ciudad=ciudad[:255], ambito=ambito_)
    obj.numero_ponentes = obj.numero_ponentes or ponentes
    obj.numero_asistentes = obj.numero_asistentes or asistentes
    obj.numero_vistas = obj.numero_vistas or vistas
    return ctx.guardar(obj)


def _usuario(ctx, hoja, fila, *valores):
    for v in valores:
        u = ctx.cuenta(v, hoja, fila, crear=False)
        if u:
            return u
    # Sin cuenta: se crea con la forma más completa del nombre («Monroy Sais, Ana Sofía» mejor que «Monroy, Sofía»).
    for v in sorted(valores, key=lambda v: -len(texto(v))):
        u = ctx.cuenta(v, hoja, fila)
        if u:
            return u
    hoja.rechazo(fila, f'No se reconoce al académico «{texto(valores[0])}».')
    return None


# --------------------------------------------------------------------------------------------------- eventos
def organizacion_eventos(ctx, libro):
    hoja = ctx.hoja(f'{ARCHIVO} › Org even acad')
    for fila, f in leer_hoja(libro, 'Org even acad'):
        with ctx.fila(hoja, fila):
            nombre = titulo(f['nombre del evento'])
            if not nombre:
                continue
            hoja.filas += 1
            usuario = _usuario(ctx, hoja, fila, f['registrado por'], f['organizadores'])
            if not usuario:
                continue
            inicio = fecha(f['dia inicio'], f['mes inicio'], f['ano inicio'])
            ev = evento(ctx, nombre, tipo_evento(ctx, f['tipo de evento']), inicio,
                        fecha(f['dia termino'], f['mes termino'], f['ano de termino'], por_defecto=inicio),
                        _pais(f['pais']), texto(f['ciudad']), ambito(f['ambito']), numero(f['de ponentes']),
                        numero(f['de asistentes presenciales en vivo']), numero(f['vistas de videos en linea']))
            nivel = normalizar(texto(f['nivel de responsabilidad']))
            T = OrganizacionEventoAcademico.TipoParticipacion if hasattr(OrganizacionEventoAcademico, 'TipoParticipacion') \
                else None
            participacion = 'COORDINADOR' if 'coordinador' in nivel else 'APOYO_TECNICO' if 'apoyo' in nivel \
                else 'COMITE_ORGANIZADOR'
            if OrganizacionEventoAcademico.objects.filter(evento=ev, usuario=usuario).exists():
                hoja.existente(OrganizacionEventoAcademico)
                continue
            ctx.guardar(OrganizacionEventoAcademico(evento=ev, tipo_participacion=participacion, usuario=usuario))
            hoja.creado(OrganizacionEventoAcademico)
    return hoja


def participacion_eventos(ctx, libro):
    hoja = ctx.hoja(f'{ARCHIVO} › Part Even Acad')
    P = ParticipacionEventoAcademico
    for fila, f in leer_hoja(libro, 'Part Even Acad'):
        with ctx.fila(hoja, fila):
            nombre = titulo(f['titulo tema de la participacion'])
            evento_ = titulo(f['nombre del evento donde se presento'])
            if not nombre or not evento_:
                continue
            hoja.filas += 1
            inicio = fecha(f['dia inicio'], f['mes inicio'], f['ano inicio'],
                           por_defecto=inicio_periodo(f['informes ciga']))
            if P.objects.filter(titulo__iexact=nombre, evento__iexact=evento_).exists():
                hoja.existente(P)
                continue
            tipo = texto(f['tipo de participacion']).lower()
            if not tipo.startswith('ponente') and 'cartel' not in tipo:
                hoja.aviso(fila, f'«{nombre[:45]}»: participación «{texto(f["tipo de participacion"])}»; '
                                 'se registró como ponencia (el modelo solo distingue ponencia y póster).')
            p = P(tipo=P.Tipo.POSTER if 'cartel' in tipo or 'poster' in tipo else P.Tipo.PONENCIA, titulo=nombre[:255],
                  evento=evento_[:254], ciudad=texto(f['ciudad'])[:255], lugar=texto(f['estado'])[:254],
                  pais=_pais(f['pais']) or ctx.mexico, fecha=inicio, ambito=ambito(f['ambito']),
                  institucion=ctx.institucion(f['entidad sede del evento'], f['pais']),
                  por_invitacion=si_no(f['por invitacion']), ponencia_magistral=si_no(f['ponencia magistral']))
            ctx.guardar(p)
            hoja.creado(P)
            personas = ctx.autores(f['autores']) or []
            for persona in ctx.autores(f['autores adscritos a la entidad']):
                if persona not in personas:
                    personas.append(persona)
            registrante = ctx.usuario(f['registrado por'])
            if registrante and registrante.persona not in personas:
                personas.append(registrante.persona)
            _participantes(ctx, ParticipacionEventoAcademicoAutor, 'participacion', p, personas)
    return hoja


# --------------------------------------------------------------------------------------------------- arbitrajes
def arbitraje_publicaciones(ctx, libro):
    hoja = ctx.hoja(f'{ARCHIVO} › Arbitraje publicaciones')
    T = ArbitrajePublicacion.Tipo
    for fila, f in leer_hoja(libro, 'Arbitraje publicaciones'):
        with ctx.fila(hoja, fila):
            obra = titulo(f['nombre de la revista o libro'])
            if not obra:
                continue
            hoja.filas += 1
            usuario = _usuario(ctx, hoja, fila, f['nombre del academico que dictamino'], f['registrado por'])
            if not usuario:
                continue
            tipo = texto(f['tipo']).lower()
            dictamen = fecha(None, f['mes'], f['ano'], por_defecto=inicio_periodo(f['informes ciga']))
            extranjera = texto(f['publicacion']).lower().startswith('extr')
            if tipo.startswith('revista'):
                revista = ctx.revista(obra, pais=None if extranjera else 'México')
                if extranjera and revista.pais.name == 'México' and not revista.articulocientifico_set.exists():
                    revista.pais = _pais('Desconocido') or revista.pais
                    ctx.guardar(revista)
                _indices(revista, f['indice s que lo registran'])
                datos = {'tipo': T.ARTICULO, 'revista': revista, 'obra': ''}
            else:
                datos = {'tipo': T.CAPITULO_LIBRO if 'cap' in tipo else T.LIBRO, 'revista': None, 'obra': obra[:255],
                         'institucion': ctx.institucion(f['editorial'])}
            if ArbitrajePublicacion.objects.filter(usuario=usuario, fecha_dictamen=dictamen,
                                                   **{k: v for k, v in datos.items() if k != 'institucion'}).exists():
                hoja.existente(ArbitrajePublicacion)
                continue
            ctx.guardar(ArbitrajePublicacion(fecha_dictamen=dictamen, usuario=usuario, **datos))
            hoja.creado(ArbitrajePublicacion)
    return hoja


def consejos_editoriales(ctx, libro):
    hoja = ctx.hoja(f'{ARCHIVO} › Consejos y comités editoriales')
    C = ConsejoEditorial
    for fila, f in leer_hoja(libro, 'Consejos y comités editoriales'):
        with ctx.fila(hoja, fila):
            nombre = titulo(f['nombre de la publicacion'])
            if not nombre:
                continue
            hoja.filas += 1
            usuario = _usuario(ctx, hoja, fila, f['persona participante'])
            if not usuario:
                continue
            t = normalizar(texto(f['tipo']))
            tipo = C.Tipo.CONSEJO_CIENTIFICO if t.startswith('consejo cientif') else \
                C.Tipo.CONSEJO_EDITORIAL if t.startswith('consejo') else C.Tipo.COMITE_EDITORIAL
            origen = C.Origen.EXTRANJERA if texto(f['ambito']).lower().startswith('extr') else C.Origen.NACIONAL
            es_coleccion = re.search(r'colecci|serie', nombre, re.IGNORECASE)
            revista = None if es_coleccion else ctx.revista(nombre, f['pais'] if origen == C.Origen.EXTRANJERA else 'México')
            filtro = {'revista': revista} if revista else {'publicacion__iexact': nombre}
            existente = C.objects.filter(usuario=usuario, tipo=tipo, **filtro).first()
            if existente:
                ctx.reportado(existente, hoja)
                ctx.vigencia(existente, f['informes ciga'])
                continue
            consejo = ctx.guardar(C(tipo=tipo, revista=revista, publicacion='' if revista else nombre[:255], origen=origen,
                          fecha_inicio=inicio_periodo(f['informes ciga']) or SIN_FECHA, usuario=usuario))
            ctx.vigencia(consejo, f['informes ciga'])
            hoja.creado(C)
    hoja.aviso('-', 'Los comités editoriales no traen fechas: inicio = el del periodo en que se reportaron.')
    return hoja


def arbitraje_proyectos(ctx, libro):
    hoja = ctx.hoja(f'{ARCHIVO} › Arbitrajes proyectos')
    tipo = TipoComision.objects.get(pk=5)  # Comisiones evaluadoras de proyectos
    for fila, f in leer_hoja(libro, 'Arbitrajes proyectos'):
        with ctx.fila(hoja, fila):
            programa = titulo(f['nombre del programa de proyectos'])
            if not programa and not texto(f['institucion']):
                continue
            hoja.filas += 1
            usuario = _usuario(ctx, hoja, fila, f['registrado por'])
            if not usuario:
                continue
            institucion = ctx.institucion(f['institucion'], f['pais'])
            if texto(f['dependencia']):
                institucion = ctx.institucion(f['dependencia'], f['pais'], padre=institucion)
            inicio = fecha_en_periodo(f['ano fin'], f['informes ciga'])
            if OtraComision.objects.filter(usuario=usuario, tipo=tipo, descripcion__iexact=programa[:255],
                                           fecha_inicio=inicio).exists():
                hoja.existente(OtraComision)
                continue
            ctx.guardar(OtraComision(tipo=tipo, descripcion=programa[:255], institucion=institucion, fecha_inicio=inicio,
                                     fecha_fin=inicio, cantidad=numero(f['numero proyectos evaluados']) or 1,
                                     usuario=usuario))
            hoja.creado(OtraComision)
    return hoja


# --------------------------------------------------------------------------------------------------- comisiones
def comision_del_catalogo(tipo_evaluacion, clase, nombre):
    """Entrada del catálogo depurado a partir de cómo el informe clasificó la comisión."""
    t = normalizar(f'{tipo_evaluacion} {clase} {nombre}')
    reglas = [('consejo externo', 'Consejo externo de evaluación'),
              ('consejo academico', 'Consejo académico de otra institución'),
              ('pride', 'Comisión Evaluadora del PRIDE'), ('dictaminadora', 'Comisión Dictaminadora'),
              ('aspirantes', 'Comisión evaluadora de aspirantes a posgrado'),
              ('admision', 'Comisión evaluadora de aspirantes a posgrado'),
              ('ingreso', 'Comisión evaluadora de aspirantes a posgrado'),
              ('plan', 'Comisión de creación o modificación de plan de estudios'),
              ('infocab', 'Comisión Evaluadora de la Iniciativa para Fortalecer la Carrera Académica en el '
                          'Bachillerato (INFOCAB)'),
              ('plaza', 'Comité evaluador de plaza académica'), ('snii', 'Comisión Dictaminadora del Sistema Nacional '
                                                                       'de Investigadoras e Investigadores (SNII)'),
              ('padron', 'Comité de evaluación de padrón o sistema estatal de investigadores'),
              ('premio', 'Jurado de premio o reconocimiento'), ('reconocimiento', 'Jurado de premio o reconocimiento'),
              ('congreso', 'Comité científico de evento'), ('evento', 'Comité científico de evento')]
    nombre_catalogo = next((n for clave, n in reglas if clave in t), 'Comisión de evaluación externa')
    return Comision.objects.get(nombre=nombre_catalogo)


def comisiones(ctx, libro, hoja_nombre, col_tipo, col_clase, col_nombre):
    hoja = ctx.hoja(f'{ARCHIVO} › {hoja_nombre}')
    for fila, f in leer_hoja(libro, hoja_nombre):
        with ctx.fila(hoja, fila):
            nombre = titulo(f[col_nombre])
            if not nombre:
                continue
            hoja.filas += 1
            usuario = _usuario(ctx, hoja, fila, f['registrado por'])
            if not usuario:
                continue
            comision = comision_del_catalogo(texto(f[col_tipo]), texto(f.get(col_clase)), nombre)
            institucion_txt = texto(f.get('revisar coherencia y limpiar institucion') or f.get('institucion'))
            dependencia = texto(f.get('revisar coherencia y limpiar dependencia') or f.get('dependencia'))
            institucion = ctx.institucion(institucion_txt)
            if dependencia and normalizar(dependencia) != normalizar(institucion_txt):
                institucion = ctx.institucion(dependencia, padre=institucion if institucion and
                                              normalizar(institucion_txt) in ('unam',) else None) or institucion
            a_fin = anio(f['ano fin'])
            inicio = fecha(None, f['mes inicio'], f['ano inicio'], por_defecto=fecha(None, None, a_fin) if a_fin
                           else inicio_periodo(f['informes ciga']))
            fin = fecha(None, f['mes fin'], a_fin, por_defecto=None) if a_fin else None
            if fin and fin < inicio:
                fin = inicio
            funcion = F.EVALUADOR if comision.seccion in ('DOCENCIA', 'EXTERNA', 'ARBITRAJE', 'COLEGIADO') else F.INTEGRANTE
            existente = ComisionInstitucional.objects.filter(usuario=usuario, comision=comision, fecha_inicio=inicio,
                                                             detalle__iexact=nombre[:255]).first()
            if existente:
                ctx.reportado(existente, hoja)
                ctx.vigencia(existente, f['informes ciga'])
                continue
            nueva = ctx.guardar(ComisionInstitucional(comision=comision, funcion=funcion, detalle=nombre[:255],
                                                      institucion=institucion, ambito=comision.ambito_sugerido,
                                                      fecha_inicio=inicio, fecha_fin=fin, usuario=usuario))
            ctx.vigencia(nueva, f['informes ciga'])
            hoja.creado(ComisionInstitucional)
    return hoja


# --------------------------------------------------------------------------------------------------- redes y sociedades
def redes(ctx, libro):
    hoja = ctx.hoja(f'{ARCHIVO} › Redes')
    for fila, f in leer_hoja(libro, 'Redes'):
        with ctx.fila(hoja, fila):
            nombre = titulo(f['nombre de la red'])
            if not nombre:
                continue
            hoja.filas += 1
            red = RedAcademica.objects.filter(nombre__iexact=nombre[:255]).first()
            if red is None:
                constitucion = anio(f['ano de constitucion'])
                red = ctx.guardar(RedAcademica(
                    nombre=nombre[:255], ambito=ambito(f['ambito'], Ambito.INTERNACIONAL),
                    objetivos=texto(f['objetivos']) or '—', fecha_constitucion=fecha(None, None, constitucion)))
                hoja.creado(RedAcademica)
            else:
                ctx.reportado(red, hoja)
            ctx.vigencia(red, f.get(''))  # La columna del periodo no tiene encabezado en esta hoja.
            personas = ctx.autores(f['academicos de la entidad participantes'])
            registrante = ctx.usuario(f['registrado por'])
            if registrante:
                personas.append(registrante.persona)
            red.participantes.add(*personas)
    return hoja


def sociedades(ctx, libro):
    hoja = ctx.hoja(f'{ARCHIVO} › Sociedades')
    S = SociedadCientifica
    for fila, f in leer_hoja(libro, 'Sociedades'):
        with ctx.fila(hoja, fila):
            nombre = titulo(f['nombre de la sociedad'])
            if not nombre:
                continue
            hoja.filas += 1
            usuario = _usuario(ctx, hoja, fila, f['registrado por'])
            if not usuario:
                continue
            existente = S.objects.filter(usuario=usuario, nombre__iexact=nombre[:255]).first()
            if existente:
                ctx.reportado(existente, hoja)
                ctx.vigencia(existente, f['informes ciga'])
                continue
            participacion = normalizar(texto(f['participacion']))
            cargo = texto(f['cargo'])
            inicio = fecha(f['dia inicio'], f['mes inicio'], f['ano inicio'], por_defecto=inicio_periodo(f['informes ciga']))
            fin = fecha(f['dia fin'], f['mes fin'], f['ano fin'], por_defecto=None) if anio(f['ano fin']) else None
            sociedad = ctx.guardar(S(nombre=nombre[:255], descripcion=cargo if len(cargo) < 120 else '',
                          tipo=S.Tipo.ELECCION if 'eleccion' in participacion else S.Tipo.INVITACION,
                          ambito=ambito(f['ambito'], Ambito.INTERNACIONAL), fecha_inicio=inicio,
                          fecha_fin=fin if fin and fin >= inicio else None, usuario=usuario))
            ctx.vigencia(sociedad, f['informes ciga'])
            hoja.creado(S)
    return hoja


# --------------------------------------------------------------------------------------------------- movilidad
def movilidad(ctx, libro, hoja_nombre, tipo, col_anfitrion='registrado por'):
    hoja = ctx.hoja(f'{ARCHIVO} › {hoja_nombre}')
    M = MovilidadAcademica
    for fila, f in leer_hoja(libro, hoja_nombre):
        with ctx.fila(hoja, fila):
            actividad = texto(f['actividad que realiza'])
            persona = texto(f['nombre del academico'])
            if not actividad and not persona:
                continue
            hoja.filas += 1
            visitante = tipo == M.Tipo.INVITACION or texto(f.get('tipo de personal')).lower().startswith('extern')
            usuario = _usuario(ctx, hoja, fila, f.get(col_anfitrion), f.get('registrado por'),
                               f['nombre del academico'] if not visitante else None)
            if not usuario:
                continue
            institucion_txt = f.get('institucion receptora') or f.get('institucion que visita') or \
                f.get('institucion donde proviene')
            pais = f.get('pais') or f.get('pais que visita') or f.get('pais donde proviene')
            inicio = fecha(f['dia inicio'], f['mes inicio'], f['ano inicio'], por_defecto=inicio_periodo(f['informe ciga']))
            fin = fecha(f['dia fin'], f['mes fin'], f.get('ano inicio 2'), por_defecto=inicio)
            if M.objects.filter(usuario=usuario, tipo=tipo, fecha_inicio=inicio).exists():
                hoja.existente(M)
                continue
            ctx.guardar(M(tipo=tipo, academico=(persona or str(usuario))[:255], visitante=visitante,
                          institucion=ctx.institucion(institucion_txt, pais), actividades=actividad or '—',
                          intercambio_unam=si_no(f.get('intercambio unam')), fecha_inicio=inicio,
                          fecha_fin=max(fin, inicio), usuario=usuario,
                          financiamiento=M.Financiamiento.PROGRAMAS_UNAM if texto(f.get('financiamiento')).upper() == 'UNAM'
                          else M.Financiamiento.OTRO if texto(f.get('financiamiento')) else ''))
            hoja.creado(M)
    return hoja


def importar(ctx, libro):
    organizacion_eventos(ctx, libro)
    participacion_eventos(ctx, libro)
    arbitraje_publicaciones(ctx, libro)
    consejos_editoriales(ctx, libro)
    arbitraje_proyectos(ctx, libro)
    comisiones(ctx, libro, 'comisiones de evaluación', 'tipo de evaluacion ubicacion en informe',
               'revisar coherencia y limpiar comite o comision', 'nombre comite o comision')
    comisiones(ctx, libro, 'Organos Colegiados', 'ubicacion en informe', 'comite o comision 2', 'comite o comision')
    redes(ctx, libro)
    sociedades(ctx, libro)
    movilidad(ctx, libro, 'sabatico', MovilidadAcademica.Tipo.SABATICO)
    movilidad(ctx, libro, 'estancias cortas de colaboració', MovilidadAcademica.Tipo.ESTANCIA)
    movilidad(ctx, libro, 'invitados', MovilidadAcademica.Tipo.INVITACION, col_anfitrion='anfintrion')
