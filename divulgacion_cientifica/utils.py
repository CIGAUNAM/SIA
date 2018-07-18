url_categoria = 'divulgacion-cientifica'
bc_seccion = 'Divulgación Científica'

class ArticuloDivulgacionContext:
    obj = 'Artículo de Divulgación'
    objs = 'Artículos de Divulgación'
    url_seccion = 'articulos-divulgacion'

    contexto = {'url_categoria': url_categoria, 'url_seccion': url_seccion,
                'tab_lista': 'Mis ' + objs, 'tab_agregar': 'Agregar ' + obj,
                'tab_detalle': 'Editar ' + obj, 'tab_otros': objs + ' de otros miembros',
                'titulo_lista': 'Mis ' + objs, 'titulo_agregar': 'Agregar ' + obj,
                'titulo_detalle': 'Editar ' + obj, 'objeto': obj.lower(), 'breadcrumb_seccion': bc_seccion, 'titulo_pagina': objs,
                'titulos_tabla': ['Título', 'Status', 'Revista']}


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
                'tab_detalle': 'Editar ' + obj, 'tab_otros': objs + ' de otros miembros',
                'titulo_lista': 'Mis ' + objs, 'titulo_agregar': 'Agregar ' + obj,
                'titulo_detalle': 'Editar ' + obj, 'objeto': obj.split()[0].lower(), 'breadcrumb_seccion': bc_seccion, 'titulo_pagina': objs,
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
                                    '{"data": "fields.libro"},\n' \
                                ']\n' \
                            '});\n' \
                        '});\n' \
                  '</script>'

    contexto['tabla_otros'] = tabla_otros


class OrganizacionEventoDivulgacionContext:
    obj = 'Evento (organización para divulgación)'
    objs = 'Eventos (organización para divulgación)'
    url_seccion = 'organizacion-eventos-divulgacion'

    contexto = {'url_categoria': url_categoria, 'url_seccion': url_seccion,
                'tab_lista': 'Mis ' + objs, 'tab_agregar': 'Agregar ' + obj,
                'tab_detalle': 'Editar ' + obj,
                'titulo_lista': 'Mis ' + objs, 'titulo_agregar': 'Agregar ' + obj,
                'titulo_detalle': 'Editar ' + obj, 'objeto': obj.split()[0].lower(), 'breadcrumb_seccion': bc_seccion, 'titulo_pagina': objs,
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
    obj = 'Participación en evento de divulgación'
    objs = 'Participación en eventos de divulgación'
    url_seccion = 'participacion-eventos-divulgacion'

    contexto = {'url_categoria': url_categoria, 'url_seccion': url_seccion,
                'tab_lista': 'Mis ' + objs, 'tab_agregar': 'Agregar ' + obj,
                'tab_detalle': 'Editar ' + obj, 'tab_otros': objs + ' de otros miembros',
                'titulo_lista': 'Mis ' + objs, 'titulo_agregar': 'Agregar ' + obj,
                'titulo_detalle': 'Editar ' + obj, 'objeto': obj.split()[0].lower(), 'breadcrumb_seccion': bc_seccion, 'titulo_pagina': objs,
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
                                    '{"data": "fields.evento"},\n' \
                                    '{"data": "fields.ambito"},\n' \
                                ']\n' \
                            '});\n' \
                        '});\n' \
                  '</script>'

    contexto['tabla_otros'] = tabla_otros


class ProgramaRadioTelevisionInternetContext:
    obj = 'Programa de Radio/Televisión/Internet'
    objs = 'Programas de Radio/Televisión/Internet'
    url_seccion = 'medios-divulgacion'

    contexto = {'url_categoria': url_categoria, 'url_seccion': url_seccion,
                'tab_lista': 'Mis ' + objs, 'tab_agregar': 'Agregar ' + obj,
                'tab_detalle': 'Editar ' + obj,
                'titulo_lista': 'Mis ' + objs, 'titulo_agregar': 'Agregar ' + obj,
                'titulo_detalle': 'Editar ' + obj, 'objeto': obj.split()[0].lower(), 'breadcrumb_seccion': bc_seccion, 'titulo_pagina': 'Programas de Radio/Televisión/Internet',
                'titulos_tabla': ['Tema', 'Fecha', 'Actividad', 'Medio']}


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
                                    '{"data": "fields.actividad"},\n' \
                                    '{"data": "fields.medio_divulgacion"},\n' \
                                ']\n' \
                            '});\n' \
                        '});\n' \
                  '</script>'

    contexto['tabla_mios'] = tabla_mios


class LibroDivulgacionContext:
    obj = 'Libro'
    objs = 'Libros'
    url_seccion = 'libros-divulgacion'

    contexto = {'url_categoria': url_categoria, 'url_seccion': url_seccion,
                'tab_lista': 'Mis ' + objs, 'tab_agregar': 'Agregar ' + obj,
                'tab_detalle': 'Editar ' + obj, 'tab_otros': objs + ' de otros miembros',
                'titulo_lista': 'Mis ' + objs, 'titulo_agregar': 'Agregar ' + obj,
                'titulo_detalle': 'Editar ' + obj, 'objeto': obj.lower(), 'breadcrumb_seccion': bc_seccion, 'titulo_pagina': objs,
                'titulos_tabla': ['Título', 'Editorial', 'Ciudad', 'Status', 'Fecha']}


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
                                        '"data": "fields.nombre",\n' \
                                        '"fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {\n' \
                                            '$(nTd).html("<a href=\'/' + str(contexto['url_categoria']) + '/' + str(contexto['url_seccion']) + '/" + oData.pk + "\'>" + oData.fields.nombre + "</a>");\n' \
                                        '}\n' \
                                    '},\n' \
                                    '{"data": "fields.editorial"},\n' \
                                    '{"data": "fields.ciudad"},\n' \
                                    '{"data": "fields.status"},\n' \
                                    '{"data": "fields.fecha"},\n' \
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
                                        '"data": "fields.nombre",\n' \
                                        '"fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {\n' \
                                            '$(nTd).html("<a href=\'/' + str(contexto['url_categoria']) + '/' + str(contexto['url_seccion']) + '/" + oData.pk + "\'>" + oData.fields.nombre + "</a>");\n' \
                                        '}\n' \
                                    '},\n' \
                                    '{"data": "fields.editorial"},\n' \
                                    '{"data": "fields.ciudad"},\n' \
                                    '{"data": "fields.status"},\n' \
                                    '{"data": "fields.fecha"},\n' \
                                ']\n' \
                            '});\n' \
                        '});\n' \
                  '</script>'

    contexto['tabla_otros'] = tabla_otros