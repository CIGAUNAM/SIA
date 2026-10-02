"""Eje 2 · Proyectos y publicaciones: proyectos, artículos, libros, capítulos, mapas, informes técnicos, memorias,
reseñas y publicaciones de divulgación."""

import re
from datetime import date
from difflib import SequenceMatcher
from decimal import Decimal, InvalidOperation

from divulgacion_cientifica.models import (ArticuloDivulgacion, ArticuloDivulgacionAutor, CapituloLibroDivulgacion,
                                           CapituloLibroDivulgacionAutor)
from difusion_cientifica.models import MemoriaInExtenso, MemoriaInExtensoAutor
from investigacion.models import (ArticuloCientifico, ArticuloCientificoAutor, CapituloLibroInvestigacion,
                                  CapituloLibroInvestigacionAutor, MapaArbitrado, MapaArbitradoAutor,
                                  ObjetivoDesarrolloSostenible, ProyectoInvestigacion, ProyectoResponsable,
                                  PublicacionTecnica, PublicacionTecnicaAutor)
from nucleo.models import SIN_FECHA, Indice, Libro, LibroParticipante, MetricaRevista, Revista, StatusPublicacion
from nucleo.similitud import normalizar

from .base import _pais, anio, fecha, fecha_en_periodo, inicio_periodo, leer_hoja, numero, si_no, texto, titulo

ARCHIVO = 'Eje2_Proyectos&Publicaciones_GC.xlsx'
P = ProyectoInvestigacion
ESTADOS = {'publicado': StatusPublicacion.PUBLICADO, 'en prensa': StatusPublicacion.EN_PRENSA,
           'aceptado': StatusPublicacion.ACEPTADO, 'enviado': StatusPublicacion.ENVIADO}
CAMPO_FECHA = {StatusPublicacion.PUBLICADO: 'fecha_publicado', StatusPublicacion.EN_PRENSA: 'fecha_enprensa',
               StatusPublicacion.ACEPTADO: 'fecha_aceptado', StatusPublicacion.ENVIADO: 'fecha_enviado'}
INDICES = [('wos', 'Web of Science: SCI/SSCI/SCI-EX'), ('isi', 'Web of Science: SCI/SSCI/SCI-EX'),
           ('scopus', 'Scopus'), ('latindex', 'Latindex'), ('scielo', 'SciELO'), ('redalyc', 'RedALyC'),
           ('conacyt', 'Revistas CONACYT'), ('clase', 'Clase'), ('otros', 'Otros Indices')]


def _estado(valor):
    return ESTADOS.get(texto(valor).lower(), StatusPublicacion.PUBLICADO)


def _fechar(obj, estado, anio_, periodo, mes_=None):
    obj.status = estado
    setattr(obj, CAMPO_FECHA[estado], fecha_en_periodo(anio_, periodo, mes_))


def _isbn(valor):
    m = re.search(r'97[89][\d\- ]{10,16}\d|\b\d[\d\- ]{8,11}[\dXx]\b', texto(valor))
    return re.sub(r'[\s]', '', m.group(0))[:20] if m else ''


def _decimal(valor):
    try:
        return Decimal(texto(valor).replace(',', '.'))
    except (InvalidOperation, ValueError):
        return None


def _paginas(obj, inicio, fin):
    i, f = numero(inicio), numero(fin)
    obj.pagina_inicio = i or None
    obj.pagina_fin = f if f and i and f >= i else None


def _participantes(ctx, through, campo, obj, personas, **extra):
    existentes = set(through.objects.filter(**{campo: obj}).values_list('persona_id', flat=True))
    orden = len(existentes)
    for persona in personas:
        if persona.pk not in existentes:
            orden += 1
            ctx.guardar(through(**{campo: obj}, persona=persona, orden=orden, **extra))
            existentes.add(persona.pk)


def _autores(ctx, f, col_autores, col_adscritos='autores adscritos a la entidad'):
    """Autores del producto, con los adscritos a la entidad aunque falten en la lista completa."""
    personas = ctx.autores(f.get(col_autores))
    for p in ctx.autores(f.get(col_adscritos, '')):
        if p not in personas:
            personas.append(p)
    return personas


def _duplicado(modelo, campo, valor):
    clave = normalizar(valor)
    return next((o for o in modelo.objects.filter(**{f'{campo}__iexact': valor})), None) or next(
        (o for o in modelo.objects.filter(**{f'{campo}__icontains': valor[:40]})
         if normalizar(getattr(o, campo)) == clave), None)


# --------------------------------------------------------------------------------------------------- proyectos
def _financiamiento(f, institucion_txt):
    clase = texto(f['clase p grafica']).upper()
    programa = texto(f['programa dependencia unam que financia']).upper()
    inst = institucion_txt.upper()
    if 'PAPIIT' in clase or 'PAPIIT' in programa:
        return P.Financiamiento.PAPIIT
    if 'PAPIME' in clase or 'PAPIME' in programa:
        return P.Financiamiento.PAPIME
    if 'SECIHTI' in clase or 'SECIHTI' in inst or 'CONACYT' in inst or 'CONAHCYT' in inst:
        return P.Financiamiento.CONACYT
    if 'EXTRA' in clase or 'autogenerados' in texto(f['financiamiento unam']).lower():
        return P.Financiamiento.EXTRAORDINARIOS
    return P.Financiamiento.SIN_RECURSOS


def _elegir(valor, opciones, por_defecto=''):
    t = normalizar(texto(valor))
    return next((v for clave, v in opciones if clave in t), por_defecto)


def proyectos(ctx, libro):
    hoja = ctx.hoja(f'{ARCHIVO} › proyectos')
    ods = {normalizar(o.nombre): o for o in ObjetivoDesarrolloSostenible.objects.all()}
    aproximadas = 0
    for fila, f in leer_hoja(libro, 'proyectos'):
        with ctx.fila(hoja, fila):
            nombre = titulo(f['nombre del proyecto'])
            if not nombre:
                continue
            hoja.filas += 1
            periodo = texto(f['periodo'])
            if not inicio_periodo(periodo):
                hoja.rechazo(fila, f'«{nombre[:60]}»: fuera de los periodos reportados («{periodo}»): no se integró al informe.')
                continue
            proyecto = ProyectoInvestigacion.objects.filter(nombre__iexact=nombre).first()
            creado = proyecto is None
            if creado:
                proyecto = P(nombre=nombre[:255])
                estado = texto(f['estado']).lower()
                proyecto.status = {'concluido': P.Status.CONCLUIDO, 'nuevo': P.Status.NUEVO}.get(estado, P.Status.EN_PROCESO)
                # El Excel no trae fechas: «nuevo» empezó en el periodo; los demás, sin fecha de inicio conocida.
                proyecto.fecha_inicio = inicio_periodo(periodo) if proyecto.status == P.Status.NUEVO else SIN_FECHA
                proyecto.fecha_fin = date(inicio_periodo(periodo).year + 1, 6, 30) \
                    if proyecto.status == P.Status.CONCLUIDO else None
                aproximadas += 1
                proyecto.es_permanente = texto(f['temporalidad del proyecto']).lower().startswith('perm')
                proyecto.clasificacion = _elegir(f['clasificacion'], [
                    ('basic', P.Clasificacion.BASICO), ('aplicad', P.Clasificacion.APLICADO),
                    ('innova', P.Clasificacion.INNOVACION), ('desarrollo', P.Clasificacion.DESARROLLO_TECNOLOGICO)],
                    P.Clasificacion.APLICADO)
                proyecto.organizacion = P.Organizacion.INDIVIDUAL if 'individ' in normalizar(texto(f['organizacion'])) \
                    else P.Organizacion.COLECTIVO
                proyecto.modalidad = _elegir(f['modalidad'], [
                    ('multi', P.ModalidadProyecto.MULTIDISCIPLINARIO), ('inter', P.ModalidadProyecto.INTERDISCIPLINARIO),
                    ('trans', P.ModalidadProyecto.TRANSDISCIPLINARIO)], P.ModalidadProyecto.DISCIPLINARIO)
                proyecto.tematica_genero = si_no(f['tematica de genero'])
                proyecto.impacto_social = texto(f['impacto social']).capitalize()[:255]
                institucion_txt = texto(f['institucion'])
                proyecto.financiamiento = _financiamiento(f, institucion_txt)
                proyecto.financiamiento_unam = _elegir(f['financiamiento unam'], [
                    ('concursado', P.FinanciamientoUNAM.CONCURSADO), ('fuera', P.FinanciamientoUNAM.FUERA),
                    ('autogenerados', P.FinanciamientoUNAM.AUTOGENERADOS)])
                proyecto.financiamiento_externo = _elegir(f['financiamiento externo'], [
                    ('federal', P.FinanciamientoExterno.FEDERAL), ('estatal', P.FinanciamientoExterno.ESTATAL),
                    ('extranjero', P.FinanciamientoExterno.EXTRANJERO),
                    ('no lucrativo', P.FinanciamientoExterno.PRIVADO_NO_LUCRATIVO), ('privado', P.FinanciamientoExterno.PRIVADO)])
                proyecto.prioridad = _elegir(f['prioridad estrategica'], [
                    ('toxic', P.Prioridad.AGENTES_TOXICOS), ('agua', P.Prioridad.AGUA), ('cultura', P.Prioridad.CULTURA),
                    ('educa', P.Prioridad.EDUCACION), ('energ', P.Prioridad.ENERGIA), ('salud', P.Prioridad.SALUD),
                    ('seguridad', P.Prioridad.SEGURIDAD), ('socioecol', P.Prioridad.SOCIOECOLOGICOS),
                    ('soberania', P.Prioridad.SOBERANIA_ALIMENTARIA), ('vivienda', P.Prioridad.VIVIENDA)])
                proyecto.financiamiento_clave = texto(f['clave de proyecto'])[:30]
                if institucion_txt:
                    proyecto.financiamiento_institucion = ctx.institucion(institucion_txt.split(';')[0], f['pais'])
                ctx.guardar(proyecto)
                hoja.creado(P)
            else:
                ctx.reportado(proyecto, hoja)
            objetivos = []
            for col in ('objetivos del desarrollo sostenible1', 'objetivos del desarrollo sostenible2',
                        'objetivos del desarrollo sostenible3', 'objetivos del desarrollo sostenible4',
                        'objetivos del desarrollo sostenible'):
                for nombre_ods in texto(f.get(col)).split(';'):
                    clave = normalizar(nombre_ods)
                    encontrado = next((o for k, o in ods.items() if clave and (
                        clave in k or k in clave or SequenceMatcher(None, clave, k).ratio() >= 0.85)), None)
                    if encontrado:
                        objetivos.append(encontrado)
                    elif clave:
                        hoja.aviso(fila, f'ODS no reconocido: «{nombre_ods.strip()}».')
            proyecto.objetivos_ods.add(*objetivos)
            responsable = ctx.persona(f['responsable'])
            registrante = ctx.usuario(f['registrado por'])
            participacion = texto(f['tipo de participacion']).lower()
            responsables = [p for p in (responsable,) if p]
            if registrante and participacion.startswith(('responsable', 'co')):
                responsables.append(registrante.persona)
            _participantes(ctx, ProyectoResponsable, 'proyecto', proyecto, responsables)
            if registrante and participacion.startswith('participante'):
                proyecto.participantes.add(registrante.persona)
    if aproximadas:
        hoja.aviso('-', f'{aproximadas} proyectos sin fechas en el Excel: inicio «sin fecha» (o el inicio del periodo si '
                        'es nuevo) y término al cierre del periodo si concluyó.')
    return hoja


# --------------------------------------------------------------------------------------------------- artículos
def _indices(revista, valor):
    t = normalizar(texto(valor))
    for clave, nombre in INDICES:
        if clave in t:
            indice = Indice.objects.filter(nombre=nombre).first()
            if indice:
                revista.indices.add(indice)


def articulos(ctx, libro):
    hoja = ctx.hoja(f'{ARCHIVO} › Artículos')
    for fila, f in leer_hoja(libro, 'Artículos'):
        with ctx.fila(hoja, fila):
            nombre = titulo(f['titulo'])
            if not nombre:
                continue
            hoja.filas += 1
            periodo = texto(f['informes ciga jul ano 1 jun ano 2'])
            if _duplicado(ArticuloCientifico, 'titulo', nombre):
                hoja.existente(ArticuloCientifico)
                continue
            internacional = texto(f['origen de la revista']).lower().startswith('inter')
            revista = ctx.revista(f['nombre de la revista o documento'],
                                  pais=None if internacional else 'México', abreviado=f['nombre abreviado de la revista wos'])
            if revista is None:
                hoja.rechazo(fila, f'«{nombre[:60]}»: no indica la revista.')
                continue
            if revista.pais.name == 'México' and internacional:
                revista.pais = _pais('Desconocido') or revista.pais
                ctx.guardar(revista)
            issn = texto(f.get('issn'))
            if issn and not (revista.issn_impreso or revista.issn_electronico) and re.fullmatch(r'\d{4}-?\d{3}[\dXx]', issn):
                revista.issn_impreso = issn
                ctx.guardar(revista)
            _indices(revista, f['indice s que lo registran'])
            a = ArticuloCientifico(titulo=nombre[:255], revista=revista, volumen=texto(f['volumen'])[:50],
                                   numero=texto(f['numeros'])[:50], doi=texto(f['identificador digital de objetos doi'])[:255],
                                   solo_electronico=si_no(f['unicamente publicacion electronica']),
                                   factor_impacto=_decimal(f['factor de impactos wos']))
            _paginas(a, f['pagina de inicio'], f['pagina de termino'])
            _fechar(a, _estado(f['estado de la publicacion']), f['ano'], periodo)
            ctx.guardar(a)
            hoja.creado(ArticuloCientifico)
            if 'carta' in normalizar(texto(f['tipo publicacion']) + texto(f['tipo de documento'])):
                hoja.aviso(fila, f'«{nombre[:50]}» es carta al editor: se registró como artículo.')
            _participantes(ctx, ArticuloCientificoAutor, 'articulo', a, _autores(ctx, f, 'autores tal como aparecen en el articulo'))
            cuartil, fi = texto(f['cuartil scimago']).upper(), _decimal(f['factor de impactos wos'])
            anio_ = anio(f['ano'])
            if anio_ and (fi is not None or cuartil in MetricaRevista.Cuartil.values):
                metrica, _ = MetricaRevista.objects.get_or_create(
                    revista=revista, anio=anio_, fuente=MetricaRevista.Fuente.JCR, defaults={'factor_impacto': fi or 0})
                if cuartil in MetricaRevista.Cuartil.values and not metrica.cuartil:
                    metrica.cuartil = cuartil
                    metrica.save()
    return hoja


# --------------------------------------------------------------------------------------------------- libros
def _libro(ctx, f, nombre, tipo, periodo, col_anio='ano de publicacion', col_estado='estado de la publicacion'):
    existente = _duplicado(Libro, 'titulo', nombre)
    edicion = numero(f.get('numero de edicion')) or 1
    if existente:
        ediciones = Libro.objects.filter(titulo=existente.titulo)
        isbn, limpio = _isbn(f.get('isbn')), lambda v: re.sub(r'[^\dX]', '', (v or '').upper())
        anio_ = anio(f.get(col_anio))
        # Otra edición solo si cambian el ISBN y el año: el ISBN del Excel a veces es otro del mismo libro y un año
        # distinto suele ser el mismo libro reportado en prensa.
        if not isbn or not anio_ or any(limpio(e.isbn) in (limpio(isbn), '') or e.fecha_publicado is None
                                        or e.fecha_publicado.year == anio_ for e in ediciones):
            return next((e for e in ediciones if limpio(e.isbn) == limpio(isbn)), existente), False
        # El Excel suele dejar «1» en el número de edición.
        nombre = existente.titulo
        edicion = max(edicion, max(e.numero_edicion for e in ediciones) + 1)
    libro_ = Libro(titulo=nombre[:255], tipo=tipo, editorial=texto(f.get('casa s editorial es'))[:255],
                   pais=_pais(f.get('pais')) or ctx.mexico, ciudad=texto(f.get('ciudad'))[:255],
                   coleccion=texto(f.get('coleccion serie numero o volumen'))[:255],
                   numero_edicion=edicion,
                   numero_paginas=numero(f.get('paginas totales del libro')) or None,
                   isbn=_isbn(f.get('isbn')), url=texto(f.get('vinculo web'))[:200] if texto(f.get('vinculo web')).startswith('http') else '',
                   arbitrado_pares=si_no(f.get('arbitrado por pares academicos')))
    _fechar(libro_, _estado(f.get(col_estado)), f.get(col_anio), periodo)
    ctx.guardar(libro_)
    return libro_, True


def libros(ctx, libro, hoja_nombre='Libros publicados', tipo=Libro.Tipo.INVESTIGACION, encabezado=0,
           col_rol='participacion', col_autores='autor es'):
    hoja = ctx.hoja(f'{ARCHIVO} › {hoja_nombre}')
    for fila, f in leer_hoja(libro, hoja_nombre, encabezado):
        with ctx.fila(hoja, fila):
            nombre = titulo(f['titulo'])
            if not nombre:
                continue
            hoja.filas += 1
            libro_, creado = _libro(ctx, f, nombre, tipo, texto(f.get('informes ciga')))
            (hoja.creado if creado else hoja.existente)(Libro)
            rol = LibroParticipante.Rol.COORDINADOR if 'coord' in texto(f.get(col_rol)).lower() else LibroParticipante.Rol.AUTOR
            _participantes(ctx, LibroParticipante, 'libro', libro_, _autores(ctx, f, col_autores), rol=rol)
    return hoja


def capitulos(ctx, libro, hoja_nombre='Capítulos', tipo=Libro.Tipo.INVESTIGACION, modelo=CapituloLibroInvestigacion,
              through=CapituloLibroInvestigacionAutor, col_autores='autores del capitulo'):
    hoja = ctx.hoja(f'{ARCHIVO} › {hoja_nombre}')
    for fila, f in leer_hoja(libro, hoja_nombre):
        with ctx.fila(hoja, fila):
            nombre, nombre_libro = titulo(f['titulo del capitulo']), titulo(f['titulo del libro'])
            if not nombre or not nombre_libro:
                continue
            hoja.filas += 1
            libro_, creado = _libro(ctx, f, nombre_libro, tipo, texto(f.get('informes ciga')),
                                    col_anio='ano de publicacion', col_estado='estado de la publicacion')
            if creado:
                hoja.creado(Libro)
                editores = ctx.autores(f.get('editores coordinadores del libro'))
                _participantes(ctx, LibroParticipante, 'libro', libro_, editores, rol=LibroParticipante.Rol.EDITOR)
            existente = modelo.objects.filter(libro=libro_, titulo__iexact=nombre).first()
            if existente:
                hoja.existente(modelo)
                continue
            capitulo = modelo(libro=libro_, titulo=nombre[:255])
            _paginas(capitulo, f.get('pagina de inicio', f.get('paginas inicio')), f.get('pagina de termino', f.get('paginas fin')))
            ctx.guardar(capitulo)
            hoja.creado(modelo)
            _participantes(ctx, through, 'capitulo', capitulo, _autores(ctx, f, col_autores))
    return hoja


# --------------------------------------------------------------------------------------------------- otros
def mapas(ctx, libro):
    hoja = ctx.hoja(f'{ARCHIVO} › mapas')
    for fila, f in leer_hoja(libro, 'mapas'):
        with ctx.fila(hoja, fila):
            nombre = titulo(f['titulo'])
            if not nombre:
                continue
            hoja.filas += 1
            if _duplicado(MapaArbitrado, 'titulo', nombre):
                hoja.existente(MapaArbitrado)
                continue
            mapa = MapaArbitrado(titulo=nombre[:255], publicacion=texto(f['casa s editorial es'])[:255],
                                 pais=_pais(f['pais']) or ctx.mexico, ciudad=texto(f['ciudad'])[:255],
                                 numero_paginas=numero(f['paginas totales']) or 0)
            _fechar(mapa, _estado(f['estado de la publicacion']), f['ano de publicacion'], texto(f['informes ciga']))
            ctx.guardar(mapa)
            hoja.creado(MapaArbitrado)
            _participantes(ctx, MapaArbitradoAutor, 'mapa', mapa, _autores(ctx, f, 'autor es'))
    return hoja


def informes(ctx, libro):
    hoja = ctx.hoja(f'{ARCHIVO} › informes')
    for fila, f in leer_hoja(libro, 'informes', columnas_previas=('tipo de publicacion',)):
        with ctx.fila(hoja, fila):
            nombre = titulo(f['titulo del reporte'])
            if not nombre:
                continue
            hoja.filas += 1
            if _duplicado(PublicacionTecnica, 'titulo', nombre):
                hoja.existente(PublicacionTecnica)
                continue
            instancia = ctx.institucion(texto(f['instancia s a la s que se presenta y o contraparte']).split(';')[0][:200])
            if instancia is None:
                hoja.rechazo(fila, f'«{nombre[:60]}»: no indica a qué instancia se presentó.')
                continue
            url = texto(f['vinculo web'])
            pub = PublicacionTecnica(titulo=nombre[:255], tipo=PublicacionTecnica.Tipo.INFORME_TECNICO,
                                     institucion=instancia, es_publico=True, url=url if url.startswith('http') else '')
            _fechar(pub, StatusPublicacion.PUBLICADO, f['ano de elaboracion'], texto(f['informes ciga']))
            ctx.guardar(pub)
            hoja.creado(PublicacionTecnica)
            _participantes(ctx, PublicacionTecnicaAutor, 'publicacion', pub,
                           _autores(ctx, f, 'autor es', 'autor es adscritos a la entidad'))
    return hoja


def memorias(ctx, libro):
    hoja = ctx.hoja(f'{ARCHIVO} › Memorias')
    for fila, f in leer_hoja(libro, 'Memorias'):
        with ctx.fila(hoja, fila):
            nombre = titulo(f['titulo del trabajo'])
            if not nombre:
                continue
            hoja.filas += 1
            if _duplicado(MemoriaInExtenso, 'titulo', nombre):
                hoja.existente(MemoriaInExtenso)
                continue
            lugar = texto(f['lugar del evento'])
            partes = [p.strip() for p in lugar.split(',')]
            pais = _pais(partes[-1]) if partes else None
            memoria = MemoriaInExtenso(titulo=nombre[:255], evento=texto(f['memoria o evento'])[:254] or '—', lugar=lugar[:254],
                                       fecha=fecha(None, f['mes del evento'], f['ano del evento'] or f['ano']),
                                       pais=pais or ctx.mexico, ciudad=(partes[0] if partes else '')[:255],
                                       isbn=texto(f['issn'])[:30])
            _paginas(memoria, f['paginas inicio'], f['paginas termino'])
            ctx.guardar(memoria)
            hoja.creado(MemoriaInExtenso)
            if texto(f['status']).lower() != 'publicado':
                hoja.aviso(fila, f'«{nombre[:50]}» está «{texto(f["status"])}»: las memorias no guardan estado editorial.')
            _participantes(ctx, MemoriaInExtensoAutor, 'memoria', memoria, _autores(ctx, f, 'autor es'))
    return hoja


def resenas(ctx, libro):
    hoja = ctx.hoja(f'{ARCHIVO} › Reseñas')
    for fila, f in leer_hoja(libro, 'Reseñas'):
        with ctx.fila(hoja, fila):
            obra = titulo(f['titulo de la publicacion'])
            if not obra:
                continue
            hoja.filas += 1
            nombre = titulo(f['titulo de la resena'])
            nombre = obra if not nombre or normalizar(nombre) in ('presentacion del libro', normalizar(obra)) else nombre
            nombre = f'Reseña de {obra}'[:255] if nombre == obra else nombre[:255]
            if _duplicado(PublicacionTecnica, 'titulo', nombre):
                hoja.existente(PublicacionTecnica)
                continue
            donde = texto(f['nombre de la revista o libro donde se publica'])
            cita = ', '.join(x for x in (texto(f['autores editores coordinadores']), obra, texto(f['editorial']),
                                         texto(f['ano']), texto(f['isbn issn'])) if x)
            pub = PublicacionTecnica(titulo=nombre, tipo=PublicacionTecnica.Tipo.RESENA, es_publico=True,
                                     institucion=ctx.institucion(texto(f['editorial']) or donde, f['pais']),
                                     descripcion=f'Publicada en: {donde}. Obra reseñada: {cita}.'[:2000], cita=cita[:500],
                                     url=texto(f['referencia web']) if texto(f['referencia web']).startswith('http') else '')
            _fechar(pub, _estado(f['estado de la publicacion']), f['ano'], texto(f['informes ciga']))
            ctx.guardar(pub)
            hoja.creado(PublicacionTecnica)
            _participantes(ctx, PublicacionTecnicaAutor, 'publicacion', pub, ctx.autores(f['autor es de la resena']))
    return hoja


def articulos_divulgacion(ctx, libro):
    hoja = ctx.hoja(f'{ARCHIVO} › art divulgación')
    for fila, f in leer_hoja(libro, 'art divulgación'):
        with ctx.fila(hoja, fila):
            nombre = titulo(f['titulo'])
            if not nombre:
                continue
            hoja.filas += 1
            if _duplicado(ArticuloDivulgacion, 'titulo', nombre):
                hoja.existente(ArticuloDivulgacion)
                continue
            internacional = texto(f['origen de la revista']).lower().startswith('inter')
            revista = ctx.revista(f['nombre de la revista o documento'], pais=None if internacional else 'México',
                                  tipo=Revista.Tipo.DIVULGACION)
            a = ArticuloDivulgacion(titulo=nombre[:255], revista=revista, volumen=texto(f['volumen'])[:50],
                                    numero=texto(f['numeros'])[:50], solo_electronico=si_no(f['unicamente publicacion electronica']),
                                    url=texto(f['vinculo web'])[:200] if texto(f['vinculo web']).startswith('http') else '')
            _paginas(a, f['paginas inicio'], f['paginas fin'])
            _fechar(a, _estado(f['estado de la publicacion']), f['ano'], texto(f['informes ciga']))
            ctx.guardar(a)
            hoja.creado(ArticuloDivulgacion)
            _participantes(ctx, ArticuloDivulgacionAutor, 'articulo', a, _autores(ctx, f, 'autores'))
    return hoja


def importar(ctx, libro):
    proyectos(ctx, libro)
    articulos(ctx, libro)
    libros(ctx, libro)
    capitulos(ctx, libro)
    mapas(ctx, libro)
    informes(ctx, libro)
    memorias(ctx, libro)
    resenas(ctx, libro)
    articulos_divulgacion(ctx, libro)
    libros(ctx, libro, 'lib div', Libro.Tipo.DIVULGACION, encabezado=1, col_rol='nivel de responsabilidad')
    capitulos(ctx, libro, 'cap divulg', Libro.Tipo.DIVULGACION, CapituloLibroDivulgacion,
              CapituloLibroDivulgacionAutor, col_autores='autor es')
