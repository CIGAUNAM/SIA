url_categoria = 'formacion-recursos-humanos'
bc_seccion = 'Formación de Recursos Humanos'


class AsesoriaEstudianteContext:
    obj = 'asesoría'
    objs = 'asesorías'
    Objs = 'Asesorías en residencias, prácticas, estancias o servicio social'
    url_seccion = 'asesorias'

    contexto = {'url_categoria': url_categoria, 'url_seccion': url_seccion,
                'tab_lista': 'Mis ' + objs, 'tab_agregar': 'Agregar ' + obj,
                'tab_detalle': 'Editar ' + obj,
                'titulo_lista': 'Mis ' + objs, 'titulo_agregar': 'Agregar ' + obj,
                'titulo_detalle': 'Editar ' + obj, 'objeto': obj, 'breadcrumb_seccion': bc_seccion, 'titulo_pagina': Objs,
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


class DireccionTesisContext:
    obj = 'dirección de tésis'
    objs = 'direcciones de tésis'
    Objs = 'Direcciones de tésis'
    url_seccion = 'direccion-tesis'

    contexto = {'url_categoria': url_categoria, 'url_seccion': url_seccion,
                'tab_lista': 'Mis ' + objs, 'tab_agregar': 'Agregar ' + obj,
                'tab_detalle': 'Editar ' + obj, 'tab_otros': Objs + ' de otros miembros', 'titulo_lista_otros': Objs + " de otros miembros",
                'titulo_lista': 'Mis ' + objs, 'titulo_agregar': 'Agregar ' + obj,
                'titulo_detalle': 'Editar ' + obj, 'objeto': obj, 'breadcrumb_seccion': bc_seccion, 'titulo_pagina': Objs,
                'titulos_tabla': ['Título', 'Asesorado', 'Nivel', 'Dependencia', 'Fecha inicio', 'fecha fin', 'fecha examen']}

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
                 '"data": "fields.titulo",\n' \
                 '"fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {\n' \
                 '$(nTd).html("<a href=\'/' + str(
        contexto['url_categoria']) + '/' + str(
        contexto['url_seccion']) + '/" + oData.pk + "\'>" + oData.fields.titulo + "</a>");\n' \
                   '}\n' \
                   '},\n' \
                   '{"data": "fields.asesorado"},\n' \
                   '{"data": "fields.nivel_academico"},\n' \
                   '{"data": "fields.dependencia"},\n' \
                   '{"data": "fields.fecha_inicio"},\n' \
                   '{"data": "fields.fecha_fin"},\n' \
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
                  '"data": "fields.titulo",\n' \
                  '"fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {\n' \
                  '$(nTd).html("<a href=\'/' + str(
        contexto['url_categoria']) + '/' + str(
        contexto['url_seccion']) + '/" + oData.pk + "\'>" + oData.fields.titulo + "</a>");\n' \
                   '}\n' \
                   '},\n' \
                   '{"data": "fields.asesorado"},\n' \
                   '{"data": "fields.nivel_academico"},\n' \
                   '{"data": "fields.dependencia"},\n' \
                   '{"data": "fields.fecha_inicio"},\n' \
                   '{"data": "fields.fecha_fin"},\n' \
                   '{"data": "fields.fecha_examen"},\n' \
                   ']\n' \
                   '});\n' \
                   '});\n' \
                   '</script>'

    contexto['tabla_otros'] = tabla_otros


class SupervisionInvestigadorPostDoctoralContext:
    obj = 'supervisión a investigador'
    objs = 'supervisiones a investigadores'
    Objs = 'Supervisiones a investigadores'
    url_seccion = 'supervision-investigadores-postdoctorales'
    usuarios = True

    contexto = {'url_categoria': url_categoria, 'url_seccion': url_seccion,
                'tab_lista': 'Mis ' + objs, 'tab_agregar': 'Agregar ' + obj,
                'tab_detalle': 'Editar ' + obj,
                'titulo_lista': 'Mis ' + objs, 'titulo_agregar': 'Agregar ' + obj,
                'titulo_detalle': 'Editar ' + obj, 'objeto': obj, 'breadcrumb_seccion': bc_seccion, 'titulo_pagina': Objs,
                'titulos_tabla': ['Investigador', 'Dependencia', 'Fecha inicio', 'Proyecto']}


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


class DesarrolloGrupoInvestigacionInternoContext:
    obj = 'grupo de investigación interno'
    objs = 'grupos de investigación internos'
    Objs = 'Grupos de investigación interno'
    url_seccion = 'grupos-investigacion-internos'
    usuarios = True

    contexto = {'url_categoria': url_categoria, 'url_seccion': url_seccion,
                'tab_lista': 'Mis ' + objs, 'tab_agregar': 'Agregar ' + obj,
                'tab_detalle': 'Editar ' + obj, 'tab_otros': Objs + ' de otros miembros', 'titulo_lista_otros': Objs + " de otros miembros",
                'titulo_lista': 'Mis ' + objs, 'titulo_agregar': 'Agregar ' + obj,
                'titulo_detalle': 'Editar ' + obj, 'objeto': obj, 'breadcrumb_seccion': bc_seccion, 'titulo_pagina': Objs,
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


class ComiteTutoralContext:
    obj = 'comité tutoral'
    objs = 'comités tutorales'
    Objs = 'Comités tutorales'
    url_seccion = 'comites-tutorales'

    contexto = {'url_categoria': url_categoria, 'url_seccion': url_seccion,
                'tab_lista': 'Mis ' + objs, 'tab_agregar': 'Agregar ' + obj,
                'tab_detalle': 'Editar ' + obj, 'tab_otros': Objs + ' de otros miembros', 'titulo_lista_otros': Objs + " de otros miembros",
                'titulo_lista': 'Mis ' + objs, 'titulo_agregar': 'Agregar ' + obj,
                'titulo_detalle': 'Editar ' + obj, 'objeto': obj, 'breadcrumb_seccion': bc_seccion, 'titulo_pagina': Objs,
                'titulos_tabla': ['Estudiante', 'Fecha de inicio', 'fecha de fin', 'Programa']}

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
                                    '{"data": "fields.fecha_inicio"},\n' \
                                    '{"data": "fields.fecha_fin"},\n' \
                                    '{"data": "fields.programa"},\n' \
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
                                    '{"data": "fields.fecha_inicio"},\n' \
                                    '{"data": "fields.fecha_fin"},\n' \
                                    '{"data": "fields.programa"},\n' \
                                ']\n' \
                            '});\n' \
                        '});\n' \
                  '</script>'

    contexto['tabla_otros'] = tabla_otros


class ComiteCandidaturaDoctoralContext:
    obj = 'comité de examen candidatura doctoral'
    objs = 'comités de examen candidaturas doctorales'
    Objs = 'Comités de examen candidaturas doctorales'
    url_seccion = 'comites-candidatura-doctoral'

    contexto = {'url_categoria': url_categoria, 'url_seccion': url_seccion,
                'tab_lista': 'Mis ' + objs, 'tab_agregar': 'Agregar ' + obj,
                'tab_detalle': 'Editar ' + obj, 'tab_otros': Objs + ' de otros miembros', 'titulo_lista_otros': Objs + " de otros miembros",
                'titulo_lista': 'Mis ' + objs, 'titulo_agregar': 'Agregar ' + obj,
                'titulo_detalle': 'Editar ' + obj, 'objeto': obj, 'breadcrumb_seccion': bc_seccion, 'titulo_pagina': Objs,
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