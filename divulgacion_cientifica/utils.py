url_categoria = 'divulgacion-cientifica'


class ArticuloDivulgacionContext:
    obj = 'Artículo de Divulgación'
    objs = 'Artículos de Divulgación'
    url_seccion = 'articulos-divulgacion'

    contexto = {'url_categoria': url_categoria, 'url_seccion': url_seccion,
                'tab_lista': 'Mis ' + objs, 'tab_agregar': 'Agregar ' + obj,
                'tab_detalle': 'Editar ' + obj, 'tab_otros': objs + ' de otros miembros',
                'titulo_lista': 'Mis ' + objs, 'titulo_agregar': 'Agregar ' + obj,
                'titulo_detalle': 'Editar ' + obj, 'objeto': obj.lower(), 'breadcrumb_seccion': obj, 'titulo_pagina': objs,
                'titulos_tabla': ['Título', 'Tipo', 'Status', 'Revista']}


    tabla_mios =  '<script>\n' \
                    '       jQuery(document).ready(function ($jquery) {\n' \
                    '       $jquery("#tabla_json").dataTable({\n' \
                                '"iDisplayLength": 15,\n' \
                                '"ajax": {\n' \
                                    '"processing": true,\n' \
                                    '"url": "/' + str(contexto['url_categoria']) + '/' + str(contexto['url_seccion']) + '/json/",\n' \
                                    '"dataSrc": ""\n' \
                                '},\n' \
                                '"columns": [\n' \
                                    '{\n' \
                                        '"data": "fields.titulo",\n' \
                                        '"fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {\n' \
                                            '$(nTd).html("<a href=\'/' + str(contexto['url_categoria']) + '/' + str(contexto['url_seccion']) + '/" + oData.pk + "\'>" + oData.fields.titulo + "</a>");\n' \
                                        '}\n' \
                                    '},\n' \
                                    '{"data": "fields.tipo"},\n' \
                                    '{"data": "fields.status"},\n' \
                                    '{"data": "fields.revista"},\n' \
                                ']\n' \
                            '});\n' \
                        '});\n' \
                  '</script>'

    contexto['tabla_mios'] = tabla_mios

    tabla_otros =  '<script>\n' \
                    '       jQuery(document).ready(function ($jquery) {\n' \
                    '       $jquery("#tabla_json_otros").dataTable({\n' \
                                '"iDisplayLength": 15,\n' \
                                '"ajax": {\n' \
                                    '"processing": true,\n' \
                                    '"url": "/' + str(contexto['url_categoria']) + '/' + str(contexto['url_seccion']) + '/json-otros/",\n' \
                                    '"dataSrc": ""\n' \
                                '},\n' \
                                '"columns": [\n' \
                                    '{\n' \
                                        '"data": "fields.titulo",\n' \
                                        '"fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {\n' \
                                            '$(nTd).html("<a href=\'/' + str(contexto['url_categoria']) + '/' + str(contexto['url_seccion']) + '/" + oData.pk + "\'>" + oData.fields.titulo + "</a>");\n' \
                                        '}\n' \
                                    '},\n' \
                                    '{"data": "fields.tipo"},\n' \
                                    '{"data": "fields.status"},\n' \
                                    '{"data": "fields.revista"},\n' \
                                ']\n' \
                            '});\n' \
                        '});\n' \
                  '</script>'

    contexto['tabla_otros'] = tabla_otros



class CapituloLibroDivulgacionContext:
    obj = 'Capitulo de Libro de Divulgación'
    objs = 'Capitulos de Libros de Divulgación'
    url_seccion = 'capitulos-libros-divulgacion'

    contexto = {'url_categoria': url_categoria, 'url_seccion': url_seccion,
                'tab_lista': 'Mis ' + objs, 'tab_agregar': 'Agregar ' + obj,
                'tab_detalle': 'Editar ' + obj,
                'titulo_lista': 'Mis ' + objs, 'titulo_agregar': 'Agregar ' + obj,
                'titulo_detalle': 'Editar ' + obj, 'objeto': obj.split()[0].lower(), 'breadcrumb_seccion': obj, 'titulo_pagina': objs,
                'titulos_tabla': ['Título', 'Libro']}


    tabla_mios =  '<script>\n' \
                    '       jQuery(document).ready(function ($jquery) {\n' \
                    '       $jquery("#tabla_json").dataTable({\n' \
                                '"iDisplayLength": 15,\n' \
                                '"ajax": {\n' \
                                    '"processing": true,\n' \
                                    '"url": "/' + str(contexto['url_categoria']) + '/' + str(contexto['url_seccion']) + '/json/",\n' \
                                    '"dataSrc": ""\n' \
                                '},\n' \
                                '"columns": [\n' \
                                    '{\n' \
                                        '"data": "fields.titulo",\n' \
                                        '"fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {\n' \
                                            '$(nTd).html("<a href=\'/' + str(contexto['url_categoria']) + '/' + str(contexto['url_seccion']) + '/" + oData.pk + "\'>" + oData.fields.titulo + "</a>");\n' \
                                        '}\n' \
                                    '},\n' \
                                    '{"data": "fields.libro"},\n' \
                                ']\n' \
                            '});\n' \
                        '});\n' \
                  '</script>'

    contexto['tabla_mios'] = tabla_mios



class OrganizacionEventoDivulgacionContext:
    obj = 'Evento (organización para divulgación)'
    objs = 'Eventos (organización para divulgación)'
    url_seccion = 'organizacion-eventos-divulgacion'

    contexto = {'url_categoria': url_categoria, 'url_seccion': url_seccion,
                'tab_lista': 'Mis ' + objs, 'tab_agregar': 'Agregar ' + obj,
                'tab_detalle': 'Editar ' + obj,
                'titulo_lista': 'Mis ' + objs, 'titulo_agregar': 'Agregar ' + obj,
                'titulo_detalle': 'Editar ' + obj, 'objeto': obj.split()[0].lower(), 'breadcrumb_seccion': obj, 'titulo_pagina': objs,
                'titulos_tabla': ['Evento', 'Responsabilidad', 'Ambito']}


    tabla_mios =  '<script>\n' \
                    '       jQuery(document).ready(function ($jquery) {\n' \
                    '       $jquery("#tabla_json").dataTable({\n' \
                                '"iDisplayLength": 15,\n' \
                                '"ajax": {\n' \
                                    '"processing": true,\n' \
                                    '"url": "/' + str(contexto['url_categoria']) + '/' + str(contexto['url_seccion']) + '/json/",\n' \
                                    '"dataSrc": ""\n' \
                                '},\n' \
                                '"columns": [\n' \
                                    '{\n' \
                                        '"data": "fields.evento",\n' \
                                        '"fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {\n' \
                                            '$(nTd).html("<a href=\'/' + str(contexto['url_categoria']) + '/' + str(contexto['url_seccion']) + '/" + oData.pk + "\'>" + oData.fields.evento + "</a>");\n' \
                                        '}\n' \
                                    '},\n' \
                                    '{"data": "fields.responsabilidad"},\n' \
                                    '{"data": "fields.ambito"},\n' \
                                ']\n' \
                            '});\n' \
                        '});\n' \
                  '</script>'

    contexto['tabla_mios'] = tabla_mios



class ParticipacionEventoDivulgacionContext:
    obj = 'Evento (participación)'
    objs = 'Eventos (participación)'
    url_seccion = 'participacion-eventos-divulgacion'

    contexto = {'url_categoria': url_categoria, 'url_seccion': url_seccion,
                'tab_lista': 'Mis ' + objs, 'tab_agregar': 'Agregar ' + obj,
                'tab_detalle': 'Editar ' + obj,
                'titulo_lista': 'Mis ' + objs, 'titulo_agregar': 'Agregar ' + obj,
                'titulo_detalle': 'Editar ' + obj, 'objeto': obj.split()[0].lower(), 'breadcrumb_seccion': obj, 'titulo_pagina': objs,
                'titulos_tabla': ['Titulo', 'Evento', 'Ambito']}


    tabla_mios =  '<script>\n' \
                    '       jQuery(document).ready(function ($jquery) {\n' \
                    '       $jquery("#tabla_json").dataTable({\n' \
                                '"iDisplayLength": 15,\n' \
                                '"ajax": {\n' \
                                    '"processing": true,\n' \
                                    '"url": "/' + str(contexto['url_categoria']) + '/' + str(contexto['url_seccion']) + '/json/",\n' \
                                    '"dataSrc": ""\n' \
                                '},\n' \
                                '"columns": [\n' \
                                    '{\n' \
                                        '"data": "fields.titulo",\n' \
                                        '"fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {\n' \
                                            '$(nTd).html("<a href=\'/' + str(contexto['url_categoria']) + '/' + str(contexto['url_seccion']) + '/" + oData.pk + "\'>" + oData.fields.titulo + "</a>");\n' \
                                        '}\n' \
                                    '},\n' \
                                    '{"data": "fields.evento"},\n' \
                                    '{"data": "fields.ambito"},\n' \
                                ']\n' \
                            '});\n' \
                        '});\n' \
                  '</script>'

    contexto['tabla_mios'] = tabla_mios



class ProgramaRadioTelevisionInternetContext:
    obj = 'Medio de Divulgración'
    objs = 'Medios de Divulgración'
    url_seccion = 'medios-divulgacion'

    contexto = {'url_categoria': url_categoria, 'url_seccion': url_seccion,
                'tab_lista': 'Mis ' + objs, 'tab_agregar': 'Agregar ' + obj,
                'tab_detalle': 'Editar ' + obj,
                'titulo_lista': 'Mis ' + objs, 'titulo_agregar': 'Agregar ' + obj,
                'titulo_detalle': 'Editar ' + obj, 'objeto': obj.split()[0].lower(), 'breadcrumb_seccion': obj, 'titulo_pagina': objs,
                'titulos_tabla': ['Tema', 'Fecha', 'Medio', 'Tipo']}


    tabla_mios =  '<script>\n' \
                    '       jQuery(document).ready(function ($jquery) {\n' \
                    '       $jquery("#tabla_json").dataTable({\n' \
                                '"iDisplayLength": 15,\n' \
                                '"ajax": {\n' \
                                    '"processing": true,\n' \
                                    '"url": "/' + str(contexto['url_categoria']) + '/' + str(contexto['url_seccion']) + '/json/",\n' \
                                    '"dataSrc": ""\n' \
                                '},\n' \
                                '"columns": [\n' \
                                    '{\n' \
                                        '"data": "fields.tema",\n' \
                                        '"fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {\n' \
                                            '$(nTd).html("<a href=\'/' + str(contexto['url_categoria']) + '/' + str(contexto['url_seccion']) + '/" + oData.pk + "\'>" + oData.fields.tema + "</a>");\n' \
                                        '}\n' \
                                    '},\n' \
                                    '{"data": "fields.fecha"},\n' \
                                    '{"data": "fields.nombre_medio"},\n' \
                                    '{"data": "fields.medio"},\n' \
                                ']\n' \
                            '});\n' \
                        '});\n' \
                  '</script>'

    contexto['tabla_mios'] = tabla_mios