url_categoria = 'formacion-recursos-humanos'
bc_seccion = 'Formación de Recursos Humanos'


class AsesoriaEstudianteContext:
    obj = 'Asesoría'
    objs = 'Asesorías'
    url_seccion = 'asesorias'

    contexto = {'url_categoria': url_categoria, 'url_seccion': url_seccion,
                'tab_lista': 'Mis ' + objs, 'tab_agregar': 'Agregar ' + obj,
                'tab_detalle': 'Editar ' + obj,
                'titulo_lista': 'Mis ' + objs, 'titulo_agregar': 'Agregar ' + obj,
                'titulo_detalle': 'Editar ' + obj, 'objeto': obj.split()[0].lower(), 'breadcrumb_seccion': bc_seccion, 'titulo_pagina': objs,
                'titulos_tabla': ['Asesorado', 'Grado', 'Programa', 'Dependencia', 'Finalizado']}


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
                                        '"data": "fields.asesorado",\n' \
                                        '"fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {\n' \
                                            '$(nTd).html("<a href=\'/' + str(contexto['url_categoria']) + '/' + str(contexto['url_seccion']) + '/" + oData.pk + "\'>" + oData.fields.asesorado + "</a>");\n' \
                                        '}\n' \
                                    '},\n' \
                                    '{"data": "fields.nivel_academico"},\n' \
                                    '{"data": "fields.programa"},\n' \
                                    '{"data": "fields.dependencia"},\n' \
                                    '{"data": "fields.fecha_fin"},\n' \
                                ']\n' \
                            '});\n' \
                        '});\n' \
                  '</script>'

    contexto['tabla_mios'] = tabla_mios


class SupervisionInvestigadorPostDoctoralContext:
    obj = 'Supervisión a investigador'
    objs = 'Supervisiones a investigadores'
    url_seccion = 'supervision-investigadores-postdoctorales'
    usuarios = True

    contexto = {'url_categoria': url_categoria, 'url_seccion': url_seccion,
                'tab_lista': 'Mis ' + objs, 'tab_agregar': 'Agregar ' + obj,
                'tab_detalle': 'Editar ' + obj, 'tab_otros': objs + ' de otros miembros',
                'titulo_lista': 'Mis ' + objs, 'titulo_agregar': 'Agregar ' + obj,
                'titulo_detalle': 'Editar ' + obj, 'objeto': obj.lower(), 'breadcrumb_seccion': bc_seccion, 'titulo_pagina': objs,
                'titulos_tabla': ['Título', 'Tipo', 'Revista', 'Status', 'Fecha']}


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
                                        '"data": "fields.investigador",\n' \
                                        '"fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {\n' \
                                            '$(nTd).html("<a href=\'/' + str(contexto['url_categoria']) + '/' + str(contexto['url_seccion']) + '/" + oData.pk + "\'>" + oData.fields.investigador + "</a>");\n' \
                                        '}\n' \
                                    '},\n' \
                                    '{"data": "fields.dependencia"},\n' \
                                    '{"data": "fields.fecha_inicio"},\n' \
                                    '{"data": "fields.proyecto"},\n' \
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
                                        '"data": "fields.investigador",\n' \
                                        '"fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {\n' \
                                            '$(nTd).html("<a href=\'/' + str(contexto['url_categoria']) + '/' + str(contexto['url_seccion']) + '/" + oData.pk + "\'>" + oData.fields.investigador + "</a>");\n' \
                                        '}\n' \
                                    '},\n' \
                                    '{"data": "fields.dependencia"},\n' \
                                    '{"data": "fields.fecha_inicio"},\n' \
                                    '{"data": "fields.proyecto"},\n' \
                                ']\n' \
                            '});\n' \
                        '});\n' \
                  '</script>'

    contexto['tabla_otros'] = tabla_otros


class DesarrolloGrupoInvestigacionInternoContext:
    obj = 'Grupo de investigación'
    objs = 'Grupos de investigación'
    url_seccion = 'grupos-investigacion-internos'
    usuarios = True

    contexto = {'url_categoria': url_categoria, 'url_seccion': url_seccion,
                'tab_lista': 'Mis ' + objs, 'tab_agregar': 'Agregar ' + obj,
                'tab_detalle': 'Editar ' + obj, 'tab_otros': objs + ' de otros miembros',
                'titulo_lista': 'Mis ' + objs, 'titulo_agregar': 'Agregar ' + obj,
                'titulo_detalle': 'Editar ' + obj, 'objeto': obj.lower(), 'breadcrumb_seccion': bc_seccion, 'titulo_pagina': objs,
                'titulos_tabla': ['Nombre', 'Fecha de inicio', 'País']}


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
                                    '{"data": "fields.fecha_inicio"},\n' \
                                    '{"data": "fields.pais"},\n' \
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
                                    '{"data": "fields.fecha_inicio"},\n' \
                                    '{"data": "fields.pais"},\n' \
                                ']\n' \
                            '});\n' \
                        '});\n' \
                  '</script>'

    contexto['tabla_otros'] = tabla_otros


class DireccionTesisContext:
    obj = 'Dirección de Tesis'
    objs = 'Direcciones de Tesis'
    url_seccion = 'direccion-tesis'

    contexto = {'url_categoria': url_categoria, 'url_seccion': url_seccion,
                'tab_lista': 'Mis ' + objs, 'tab_agregar': 'Agregar ' + obj,
                'tab_detalle': 'Editar ' + obj, 'tab_otros': objs + ' de otros miembros',
                'titulo_lista': 'Mis ' + objs, 'titulo_agregar': 'Agregar ' + obj,
                'titulo_detalle': 'Editar ' + obj, 'objeto': obj.split()[0].lower(), 'breadcrumb_seccion': bc_seccion, 'titulo_pagina': objs,
                'titulos_tabla': ['Título', 'Asesorado', 'Nivel', 'Dependencia', 'Examen']}

    tabla_mios = '<script>\n' \
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
                 '"data": "fields.asesorado",\n' \
                 '"fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {\n' \
                 '$(nTd).html("<a href=\'/' + str(
        contexto['url_categoria']) + '/' + str(
        contexto['url_seccion']) + '/" + oData.pk + "\'>" + oData.fields.asesorado + "</a>");\n' \
                   '}\n' \
                   '},\n' \
                   '{"data": "fields.asesorado"},\n' \
                   '{"data": "fields.nivel_academico"},\n' \
                   '{"data": "fields.dependencia"},\n' \
                   '{"data": "fields.fecha_examen"},\n' \
                   ']\n' \
                   '});\n' \
                   '});\n' \
                   '</script>'

    contexto['tabla_mios'] = tabla_mios

    tabla_otros = '<script>\n' \
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
                  '"data": "fields.asesorado",\n' \
                  '"fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {\n' \
                  '$(nTd).html("<a href=\'/' + str(
        contexto['url_categoria']) + '/' + str(
        contexto['url_seccion']) + '/" + oData.pk + "\'>" + oData.fields.asesorado + "</a>");\n' \
                   '}\n' \
                   '},\n' \
                   '{"data": "fields.asesorado"},\n' \
                   '{"data": "fields.nivel_academico"},\n' \
                   '{"data": "fields.dependencia"},\n' \
                   '{"data": "fields.fecha_examen"},\n' \
                   ']\n' \
                   '});\n' \
                   '});\n' \
                   '</script>'

    contexto['tabla_otros'] = tabla_otros


class ComiteTutoralContext:
    obj = 'Comité Tutoral'
    objs = 'Comités Tutorales'
    url_seccion = 'comites-tutorales'

    contexto = {'url_categoria': url_categoria, 'url_seccion': url_seccion,
                'tab_lista': 'Mis ' + objs, 'tab_agregar': 'Agregar ' + obj,
                'tab_detalle': 'Editar ' + obj, 'tab_otros': objs + ' de otros miembros',
                'titulo_lista': 'Mis ' + objs, 'titulo_agregar': 'Agregar ' + obj,
                'titulo_detalle': 'Editar ' + obj, 'objeto': obj.split()[0].lower(), 'breadcrumb_seccion': bc_seccion, 'titulo_pagina': objs,
                'titulos_tabla': ['Asesorado', 'Grado', 'Programa', 'Dependencia', 'Proyecto']}


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
                                        '"data": "fields.estudiante",\n' \
                                        '"fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {\n' \
                                            '$(nTd).html("<a href=\'/' + str(contexto['url_categoria']) + '/' + str(contexto['url_seccion']) + '/" + oData.pk + "\'>" + oData.fields.estudiante + "</a>");\n' \
                                        '}\n' \
                                    '},\n' \
                                    '{"data": "fields.nivel_academico"},\n' \
                                    '{"data": "fields.programa"},\n' \
                                    '{"data": "fields.dependencia"},\n' \
                                    '{"data": "fields.proyecto"},\n' \
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
                                        '"data": "fields.estudiante",\n' \
                                        '"fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {\n' \
                                            '$(nTd).html("<a href=\'/' + str(contexto['url_categoria']) + '/' + str(contexto['url_seccion']) + '/" + oData.pk + "\'>" + oData.fields.estudiante + "</a>");\n' \
                                        '}\n' \
                                    '},\n' \
                                    '{"data": "fields.nivel_academico"},\n' \
                                    '{"data": "fields.programa"},\n' \
                                    '{"data": "fields.dependencia"},\n' \
                                    '{"data": "fields.proyecto"},\n' \
                                ']\n' \
                            '});\n' \
                        '});\n' \
                  '</script>'

    contexto['tabla_otros'] = tabla_otros



class ComiteCandidaturaDoctoralContext:
    obj = 'Comité de Candidatura Doctoral'
    objs = 'Comités de Candidatura Doctoral'
    url_seccion = 'comites-candidatura-doctoral'

    contexto = {'url_categoria': url_categoria, 'url_seccion': url_seccion,
                'tab_lista': 'Mis ' + objs, 'tab_agregar': 'Agregar ' + obj,
                'tab_detalle': 'Editar ' + obj, 'tab_otros': objs + ' de otros miembros',
                'titulo_lista': 'Mis ' + objs, 'titulo_agregar': 'Agregar ' + obj,
                'titulo_detalle': 'Editar ' + obj, 'objeto': obj.split()[0].lower(), 'breadcrumb_seccion': bc_seccion, 'titulo_pagina': objs,
                'titulos_tabla': ['Candidato', 'Programa', 'Proyecto', 'Defensa']}


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
                                        '"data": "fields.candidato",\n' \
                                        '"fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {\n' \
                                            '$(nTd).html("<a href=\'/' + str(contexto['url_categoria']) + '/' + str(contexto['url_seccion']) + '/" + oData.pk + "\'>" + oData.fields.candidato + "</a>");\n' \
                                        '}\n' \
                                    '},\n' \
                                    '{"data": "fields.programa_doctorado"},\n' \
                                    '{"data": "fields.proyecto"},\n' \
                                    '{"data": "fields.fecha_defensa"},\n' \
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
                                        '"data": "fields.candidato",\n' \
                                        '"fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {\n' \
                                            '$(nTd).html("<a href=\'/' + str(contexto['url_categoria']) + '/' + str(contexto['url_seccion']) + '/" + oData.pk + "\'>" + oData.fields.candidato + "</a>");\n' \
                                        '}\n' \
                                    '},\n' \
                                    '{"data": "fields.programa_doctorado"},\n' \
                                    '{"data": "fields.proyecto"},\n' \
                                    '{"data": "fields.fecha_defensa"},\n' \
                                ']\n' \
                            '});\n' \
                        '});\n' \
                  '</script>'

    contexto['tabla_otros'] = tabla_otros