url_categoria = 'formacion-academica'
bc_seccion = 'Formación Académica'


class CursoEspecializacionContext:
    obj = 'Curso de Especialización'
    objs = 'Cursos de Especialización'
    url_seccion = 'cursos-especializacion'

    contexto = {'url_categoria': url_categoria, 'url_seccion': url_seccion,
                'tab_lista': 'Mis ' + objs, 'tab_agregar': 'Agregar ' + obj,
                'tab_detalle': 'Editar ' + obj,
                'titulo_lista': 'Mis ' + objs, 'titulo_agregar': 'Agregar ' + obj,
                'titulo_detalle': 'Editar ' + obj, 'objeto': obj.lower(), 'breadcrumb_seccion': bc_seccion, 'titulo_pagina': objs,
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
    obj = 'Licenciatura'
    objs = 'Licenciaturas'
    url_seccion = 'licenciaturas'

    contexto = {'url_categoria': url_categoria, 'url_seccion': url_seccion,
                'tab_lista': 'Mis ' + objs, 'tab_agregar': 'Agregar ' + obj,
                'tab_detalle': 'Editar ' + obj,
                'titulo_lista': 'Mis ' + objs, 'titulo_agregar': 'Agregar ' + obj,
                'titulo_detalle': 'Editar ' + obj, 'objeto': obj.lower(), 'breadcrumb_seccion': bc_seccion, 'titulo_pagina': objs,
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
                'tab_lista': 'Mis Maestrías', 'tab_agregar': 'Agregar Maestría', 'tab_detalle': 'Editar Maestría',
                'titulo_lista': 'Mis Maestrías', 'titulo_agregar': 'Agregar Maestría',
                'titulo_detalle': 'Editar Maestría',
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
                'tab_lista': 'Mis Doctorados', 'tab_agregar': 'Agregar Doctorado', 'tab_detalle': 'Editar Doctorado',
                'titulo_lista': 'Mis Doctorados', 'titulo_agregar': 'Agregar Doctorado',
                'titulo_detalle': 'Editar Doctorado',
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
                'tab_lista': 'Mis Postdoctorados', 'tab_agregar': 'Agregar Postdoctorado', 'tab_detalle': 'Editar Postdoctorado',
                'titulo_lista': 'Mis Postdoctorados', 'titulo_agregar': 'Agregar Postdoctorado',
                'titulo_detalle': 'Editar Postdoctorado',
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
