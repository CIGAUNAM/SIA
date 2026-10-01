"""Eje 4 · Vinculación con la sociedad: eventos de divulgación organizados y participaciones, presencia en medios,
asesorías y servicios externos; y convenios con otras entidades."""

from decimal import Decimal, InvalidOperation

from compromiso_institucional.models import Comision, ComisionInstitucional
from divulgacion_cientifica.models import (OrganizadoPor, OrganizacionEventoDivulgacion, ParticipacionEventoDivulgacion,
                                           ParticipacionEventoDivulgacionAutor, ProgramaMedio)
from nucleo.models import Ambito, Institucion, MedioDivulgacion
from nucleo.similitud import normalizar
from vinculacion.models import Convenio, OtraComision, ServicioAsesoriaExterna, TipoComision

from .base import _pais, fecha, fecha_celda, inicio_periodo, leer_hoja, si_no, texto, titulo
from .produccion import _participantes
from .vinculacion_academica import ambito, evento, tipo_evento

ARCHIVO = 'Eje4_VinculacionSociedad_GC_IR_020926.xlsx'
ARCHIVO_CONVENIOS = 'Convenios_VZ.xlsx'
CLASIFICACION = {'federal': Institucion.Clasificacion.FEDERAL, 'estatal': Institucion.Clasificacion.ESTATAL,
                 'municipal': Institucion.Clasificacion.MUNICIPAL, 'no lucrativo': Institucion.Clasificacion.NO_LUCRATIVA,
                 'sociedad civil': Institucion.Clasificacion.NO_LUCRATIVA, 'no gubernamental': Institucion.Clasificacion.NO_LUCRATIVA,
                 'privado': Institucion.Clasificacion.PRIVADA, 'academic': Institucion.Clasificacion.ACADEMICA,
                 'comunidad': Institucion.Clasificacion.COMUNIDAD}


def organizado_por(valor):
    t = normalizar(texto(valor))
    for clave, v in (('unidad com', OrganizadoPor.UNIDAD_COMUNICACION), ('copartic', OrganizadoPor.COPARTICIPACION),
                     ('cinig', OrganizadoPor.COMISION), ('ceid', OrganizadoPor.COMISION), ('comisi', OrganizadoPor.COMISION),
                     ('otras dep', OrganizadoPor.EXTERNA), ('pers acad', OrganizadoPor.PERSONAL_ACADEMICO)):
        if clave in t:
            return v
    return ''


def clasificar(ctx, institucion, *valores):
    """Pone la clasificación (federal, estatal, sociedad civil, comunidad…) a la institución si no la tiene."""
    if institucion is None or institucion.clasificacion:
        return institucion
    t = normalizar(' '.join(texto(v) for v in valores))
    clasificacion = next((v for clave, v in CLASIFICACION.items() if clave in t), '')
    if not clasificacion and 'gobierno' in t:
        clasificacion = Institucion.Clasificacion.ESTATAL if 'estado' in t else Institucion.Clasificacion.FEDERAL
    if clasificacion:
        institucion.clasificacion = clasificacion
        ctx.guardar(institucion)
    return institucion


def organizacion(ctx, libro):
    hoja = ctx.hoja(f'{ARCHIVO} › org even div')
    for fila, f in leer_hoja(libro, 'org even div'):
        with ctx.fila(hoja, fila):
            nombre = titulo(f['nombre del evento'])
            if not nombre:
                continue
            hoja.filas += 1
            usuario = ctx.cuenta(f['registrado por'], hoja, fila)
            if usuario is None:
                hoja.rechazo(fila, f'No se reconoce al académico «{texto(f["registrado por"])}».')
                continue
            inicio = fecha(f['dia inicio'], f['mes inicio'], f['ano inicio'], por_defecto=inicio_periodo(f['informes ciga']))
            ev = evento(ctx, nombre, tipo_evento(ctx, f['tipo de evento']), inicio,
                        fecha(f['dia fin'], f['mes fin'], f['ano fin'], por_defecto=inicio), _pais(f['pais']),
                        texto(f['ciudad']), ambito(f['ambito'], Ambito.INSTITUCIONAL), None if not texto(f['numero de ponentes'])
                        else int(float(texto(f['numero de ponentes']) or 0)), None if not texto(f['numero de asistentes'])
                        else int(float(texto(f['numero de asistentes']) or 0)))
            if OrganizacionEventoDivulgacion.objects.filter(evento=ev, usuario=usuario).exists():
                hoja.existente(OrganizacionEventoDivulgacion)
                continue
            nivel = normalizar(texto(f['nivel de responsabilidad']))
            ctx.guardar(OrganizacionEventoDivulgacion(
                evento=ev, usuario=usuario, organizado_por=organizado_por(f['tipo evento']) or OrganizadoPor.PERSONAL_ACADEMICO,
                tipo_participacion='COORDINADOR' if 'coordinador' in nivel else 'APOYO_TECNICO' if 'ayudante' in nivel
                else 'COMITE_ORGANIZADOR'))
            hoja.creado(OrganizacionEventoDivulgacion)
    return hoja


def participacion(ctx, libro):
    hoja = ctx.hoja(f'{ARCHIVO} › Part en even div')
    P = ParticipacionEventoDivulgacion
    for fila, f in leer_hoja(libro, 'Part en even div'):
        with ctx.fila(hoja, fila):
            nombre, nombre_evento = titulo(f['titulo de la presentacion']), titulo(f['nombre del evento donde se presento'])
            if not nombre or not nombre_evento:
                continue
            hoja.filas += 1
            inicio = fecha(f['dia inicio'], f['mes inicio'], f['ano inicio'], por_defecto=inicio_periodo(f['informes ciga']))
            ambito_ = ambito(f['ambiambito'], Ambito.INSTITUCIONAL)
            ev = evento(ctx, nombre_evento, tipo_evento(ctx, f['tipo de evento']), inicio,
                        fecha(f['dia fin'], f['mes fin'], f['ano fin'], por_defecto=inicio), _pais(f['pais']),
                        texto(f['ciudad']), ambito_)
            if P.objects.filter(titulo__iexact=nombre[:255], evento=ev).exists():
                hoja.existente(P)
                continue
            p = ctx.guardar(P(tipo=P.Tipo.PONENCIA, titulo=nombre[:255], evento=ev, fecha=inicio, ambito=ambito_,
                              organizado_por=organizado_por(f['tipo evento']), por_invitacion=si_no(f['por invitacion'])))
            hoja.creado(P)
            personas = ctx.autores(f['autores'])
            for persona in ctx.autores(f['autores adscritos a la entidad']):
                if persona not in personas:
                    personas.append(persona)
            registrante = ctx.cuenta(f['registrado por'], hoja, fila)
            if registrante and registrante.persona not in personas:
                personas.append(registrante.persona)
            _participantes(ctx, ParticipacionEventoDivulgacionAutor, 'participacion', p, personas)
    return hoja


def medios(ctx, libro):
    hoja = ctx.hoja(f'{ARCHIVO} › presencia medios')
    A = ProgramaMedio.Actividad
    for fila, f in leer_hoja(libro, 'presencia medios'):
        with ctx.fila(hoja, fila):
            tema = titulo(f['tema de la entrevista']) or titulo(f['nombre del programa'])
            if not tema:
                continue
            hoja.filas += 1
            usuario = ctx.cuenta(f['registrado por'], hoja, fila)
            if usuario is None:
                hoja.rechazo(fila, f'No se reconoce al académico «{texto(f["registrado por"])}».')
                continue
            tipo_programa = normalizar(texto(f['tipo programa']))
            nombre_medio = titulo(f['nombre del programa'])[:255] or 'Sin nombre'
            tipo_medio = MedioDivulgacion.Tipo.RADIO if normalizar(texto(f['medio'])) == 'radio' else MedioDivulgacion.Tipo.INTERNET
            medio = MedioDivulgacion.objects.filter(nombre__iexact=nombre_medio, tipo=tipo_medio).first() or ctx.guardar(
                MedioDivulgacion(nombre=nombre_medio, tipo=tipo_medio, canal=texto(f['estacion en la que se difunde'])[:255],
                                 pais=ctx.mexico))
            actividad = normalizar(texto(f['actividad']))
            actividad = A.TRANSMISION if 'transmision' in tipo_programa else A.ENTREVISTA if 'entrevista' in actividad \
                else A.PRODUCCION if 'produccion' in actividad else A.PARTICIPACION if 'particip' in actividad else A.OTRA
            fecha_ = fecha(f['dia'], f['mes'], f['ano'], por_defecto=inicio_periodo(f['informes ciga']))
            if ProgramaMedio.objects.filter(usuario=usuario, tema__iexact=tema[:254], fecha=fecha_, medio=medio).exists():
                hoja.existente(ProgramaMedio)
                continue
            participantes = texto(f['nombre del academico participante'])
            ctx.guardar(ProgramaMedio(tema=tema[:254], fecha=fecha_, actividad=actividad, medio=medio, usuario=usuario,
                                      descripcion=f'{texto(f["tipo programa"])}. Participan: {participantes}'.strip(' .:')
                                      if participantes else texto(f['tipo programa'])))
            hoja.creado(ProgramaMedio)
    return hoja


def asesorias(ctx, libro):
    hoja = ctx.hoja(f'{ARCHIVO} › Asesorías externas')
    S = ServicioAsesoriaExterna
    F = ComisionInstitucional.Funcion
    for fila, f in leer_hoja(libro, 'FALTA ARREGLAR Asesorias extern'):
        with ctx.fila(hoja, fila):
            nombre = titulo(f['nombre del servicio participacion'])
            if not nombre:
                continue
            hoja.filas += 1
            usuarios = ctx.cuentas(f['academico participantes'], hoja, fila)
            if not usuarios:
                hoja.rechazo(fila, f'No se reconoce al académico «{texto(f["academico participantes"])}».')
                continue
            receptora = clasificar(ctx, ctx.institucion(texto(f['nombre de la entidad que recibe']).split(';')[0][:200]),
                                   f['clasificacion de la institucion'], f['tipo de entidad'])
            inicio = fecha(None, f['mes inicio'], f['ano inicio'], por_defecto=inicio_periodo(f['informe ciga']))
            fin = fecha(None, f['mes fin'], f['ano inicio 2'], por_defecto=None) if texto(f['ano inicio 2']) else None
            fin = fin if fin and fin >= inicio else None
            tipo = normalizar(texto(f['tipo de servicio participacion']))
            for usuario in usuarios:
                if 'consejo' in tipo:  # Consejos consultivos y directivos son comisiones, no servicios.
                    nombre_cat = 'Consejo directivo de organización de la sociedad civil' if 'directivo' in tipo \
                        else 'Consejo consultivo o comité técnico gubernamental'
                    comision = Comision.objects.get(nombre=nombre_cat)
                    if ComisionInstitucional.objects.filter(usuario=usuario, comision=comision, detalle__iexact=nombre[:255]).exists():
                        hoja.existente(ComisionInstitucional)
                        continue
                    ctx.guardar(ComisionInstitucional(comision=comision, funcion=F.INTEGRANTE, detalle=nombre[:255],
                                                      institucion=receptora, ambito=comision.ambito_sugerido,
                                                      fecha_inicio=inicio, fecha_fin=fin, usuario=usuario))
                    hoja.creado(ComisionInstitucional)
                    continue
                if receptora is None:
                    hoja.rechazo(fila, f'«{nombre[:50]}» no indica la entidad que recibe el servicio.')
                    break
                if S.objects.filter(usuario=usuario, nombre__iexact=nombre[:254], fecha_inicio=inicio).exists():
                    hoja.existente(S)
                    continue
                ctx.guardar(S(tipo=S.Tipo.INCIDENCIA if 'incidencia' in tipo else S.Tipo.LABORATORIO if 'laboratorio' in tipo
                              else S.Tipo.EVALUACION if 'evaluacion' in tipo else S.Tipo.OTRO if 'otros' in tipo
                              else S.Tipo.ASESORIA, nombre=nombre[:254], institucion=receptora, fecha_inicio=inicio,
                              fecha_fin=fin, financiamiento='Sí' if si_no(f['incluye financiamiento']) else '',
                              usuario=usuario))
                hoja.creado(S)
    return hoja


def convenios(ctx):
    hoja = ctx.hoja(f'{ARCHIVO_CONVENIOS} › Hoja1')
    for fila, f in leer_hoja(ctx.libro(ARCHIVO_CONVENIOS), 'Hoja1', 1):
        with ctx.fila(hoja, fila):
            nombre = titulo(f['nombre del convenio'])
            if not nombre:
                continue
            hoja.filas += 1
            instituciones = [clasificar(ctx, ctx.institucion(n.strip()), f['clasificacion de la institucion'])
                             for n in texto(f['instituciones con las que se establece']).split(';') if n.strip()]
            instituciones = [i for i in instituciones if i]
            completo = f'{nombre} — {instituciones[0].nombre}' if instituciones else nombre
            if Convenio.objects.filter(nombre__iexact=completo[:254]).exists():
                hoja.existente(Convenio)
                continue
            try:
                monto = Decimal(texto(f['monto de financiamiento']).replace(',', '')) if texto(f['monto de financiamiento']) else None
            except InvalidOperation:
                monto = None
            inicio = fecha_celda(f['fecha de firma'], por_defecto=inicio_periodo(f['periodo']))
            fin = fecha_celda(f['termino de convenio'], por_defecto=None) if texto(f['termino de convenio']) else None
            c = ctx.guardar(Convenio(nombre=completo[:254], ambito=ambito(f['ambito']), objetivos=texto(f['objetivos']) or '—',
                                     es_renovacion=si_no(f['se trata de una renovacion']),
                                     financiamiento='Sí' if si_no(f['incluye financiamiento']) else '', monto=monto,
                                     fecha_inicio=inicio, fecha_fin=fin if fin and fin >= inicio else None))
            c.instituciones.add(*instituciones)
            hoja.creado(Convenio)
    return hoja


def importar(ctx, libro):
    organizacion(ctx, libro)
    participacion(ctx, libro)
    medios(ctx, libro)
    asesorias(ctx, libro)
    convenios(ctx)
