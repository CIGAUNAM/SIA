url_categoria = 'formacion-academica'
bc_seccion = 'Formación académica'


class CursoEspecializacionContext:
    obj = 'curso de especialización'
    objs = 'cursos de especialización'
    url_seccion = 'cursos-especializacion'

    contexto = {'url_categoria': url_categoria, 'url_seccion': url_seccion,
                'tab_lista': 'Mis ' + objs, 'tab_agregar': 'Agregar ' + obj,
                'tab_detalle': 'Editar ' + obj,
                'titulo_lista': 'Mis ' + objs, 'titulo_agregar': 'Agregar ' + obj,
                'titulo_detalle': 'Editar ' + obj, 'objeto': obj, 'breadcrumb_seccion': bc_seccion, 'titulo_pagina': objs.title(),
                'titulos_tabla': ['Curso', 'Tipo', 'Horas', 'Dependencia', 'Fin']}

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
                                    '{"data": "fields.tipo"},\n' \
                                    '{"data": "fields.horas"},\n' \
                                    '{"data": "fields.dependencia"},\n' \
                                    '{"data": "fields.fecha_fin"},\n' \
                                ']\n' \
                            '});\n' \
                        '});\n' \
                  '</script>'

    contexto['tabla_mios'] = tabla_mios


class LicenciaturaContext:
    obj = 'licenciatura'
    objs = 'licenciaturas'
    url_seccion = 'licenciaturas'

    contexto = {'url_categoria': url_categoria, 'url_seccion': url_seccion,
                'tab_lista': 'Mis ' + objs, 'tab_agregar': 'Agregar ' + obj,
                'tab_detalle': 'Editar ' + obj,
                'titulo_lista': 'Mis ' + objs, 'titulo_agregar': 'Agregar ' + obj,
                'titulo_detalle': 'Editar ' + obj, 'objeto': obj, 'breadcrumb_seccion': bc_seccion, 'titulo_pagina': objs.title(),
                'titulos_tabla': ['Carrera', 'Título de Tesis', 'Fecha de grado', 'Dependencia']}


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
                                        '"data": "fields.carrera",\n' \
                                        '"fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {\n' \
                                            '$(nTd).html("<a href=\'/' + str(contexto['url_categoria']) + '/' + str(contexto['url_seccion']) + '/" + oData.pk + "\'>" + oData.fields.carrera + "</a>");\n' \
                                        '}\n' \
                                    '},\n' \
                                    '{"data": "fields.titulo_tesis"},\n' \
                                    '{"data": "fields.fecha_grado"},\n' \
                                    '{"data": "fields.dependencia"},\n' \
                                ']\n' \
                            '});\n' \
                        '});\n' \
                  '</script>'

    contexto['tabla_mios'] = tabla_mios


class MaestriaContext:
    url_seccion = 'maestrias'

    contexto = {'url_categoria': url_categoria, 'url_seccion': 'maestrias',
                'tab_lista': 'Mis maestrías', 'tab_agregar': 'Agregar maestría', 'tab_detalle': 'Editar maestría',
                'titulo_lista': 'Mis maestrías', 'titulo_agregar': 'Agregar Maestría',
                'titulo_detalle': 'Editar maestría',
                'objeto': 'maestría', 'breadcrumb_seccion': 'Formación académica', 'titulo_pagina': 'Maestrías',
                'titulos_tabla': ['Programa', 'Título de Tesis', 'Fecha de grado', 'Dependencia']}

    tabla_mios =  '<script>\n' \
                    'jQuery(document).ready(function ($jquery) {\n' \
                    '$jquery("#tabla_json").dataTable({\n' \
                                '"iDisplayLength": 15,\n' \
                                '"ajax": {\n' \
                                    '"processing": true,\n' \
                                    '"url": "/' + str(contexto['url_categoria']) + '/' + str(contexto['url_seccion']) + '/json/",\n' \
                                    '"dataSrc": ""\n' \
                                '},\n' \
                                '"columns": [\n' \
                                    '{\n' \
                                        '"data": "fields.programa",\n' \
                                        '"fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {\n' \
                                            '$(nTd).html("<a href=\'/' + str(contexto['url_categoria']) + '/' + str(contexto['url_seccion']) + '/" + oData.pk + "\'>" + oData.fields.programa + "</a>");\n' \
                                        '}\n' \
                                    '},\n' \
                                    '{"data": "fields.titulo_tesis"},\n' \
                                    '{"data": "fields.fecha_grado"},\n' \
                                    '{"data": "fields.dependencia"},\n' \
                                ']\n' \
                            '});\n' \
                        '});\n' \
                  '</script>'

    contexto['tabla_mios'] = tabla_mios


class DoctoradoContext:
    url_seccion = 'doctorados'

    contexto = {'url_categoria': url_categoria, 'url_seccion': 'doctorados',
                'tab_lista': 'Mis doctorados', 'tab_agregar': 'Agregar doctorado', 'tab_detalle': 'Editar doctorado',
                'titulo_lista': 'Mis doctorados', 'titulo_agregar': 'Agregar doctorado',
                'titulo_detalle': 'Editar doctorado',
                'objeto': 'doctorado', 'breadcrumb_seccion': 'Formación académica', 'titulo_pagina': 'Doctorados',
                'titulos_tabla': ['Programa', 'Título de Tesis', 'Fecha de grado', 'Dependencia']}

    tabla_mios =  '<script>\n' \
                    'jQuery(document).ready(function ($jquery) {\n' \
                    '$jquery("#tabla_json").dataTable({\n' \
                                '"iDisplayLength": 15,\n' \
                                '"ajax": {\n' \
                                    '"processing": true,\n' \
                                    '"url": "/' + str(contexto['url_categoria']) + '/' + str(contexto['url_seccion']) + '/json/",\n' \
                                    '"dataSrc": ""\n' \
                                '},\n' \
                                '"columns": [\n' \
                                    '{\n' \
                                        '"data": "fields.programa",\n' \
                                        '"fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {\n' \
                                            '$(nTd).html("<a href=\'/' + str(contexto['url_categoria']) + '/' + str(contexto['url_seccion']) + '/" + oData.pk + "\'>" + oData.fields.programa + "</a>");\n' \
                                        '}\n' \
                                    '},\n' \
                                    '{"data": "fields.titulo_tesis"},\n' \
                                    '{"data": "fields.fecha_grado"},\n' \
                                    '{"data": "fields.dependencia"},\n' \
                                ']\n' \
                            '});\n' \
                        '});\n' \
                  '</script>'

    contexto['tabla_mios'] = tabla_mios


class PostDoctoradoContext:
    url_seccion = 'postdoctorados'

    contexto = {'url_categoria': url_categoria, 'url_seccion': 'postdoctorados',
                'tab_lista': 'Mis postdoctorados', 'tab_agregar': 'Agregar postdoctorado', 'tab_detalle': 'Editar postdoctorado',
                'titulo_lista': 'Mis postdoctorados', 'titulo_agregar': 'Agregar postdoctorado',
                'titulo_detalle': 'Editar postdoctorado',
                'objeto': 'postdoctorado', 'breadcrumb_seccion': 'Formación académica', 'titulo_pagina': 'Postdoctorados',
                'titulos_tabla': ['Tìtulo', 'Área de conocimiento', 'Fecha fin', 'Proyecto', 'Dependencia']}

    tabla_mios =  '<script>\n' \
                    'jQuery(document).ready(function ($jquery) {\n' \
                    '$jquery("#tabla_json").dataTable({\n' \
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
                                    '{"data": "fields.area_conocimiento"},\n' \
                                    '{"data": "fields.fecha_fin"},\n' \
                                    '{"data": "fields.proyecto"},\n' \
                                    '{"data": "fields.dependencia"},\n' \
                                ']\n' \
                            '});\n' \
                        '});\n' \
                  '</script>'

    contexto['tabla_mios'] = tabla_mios
