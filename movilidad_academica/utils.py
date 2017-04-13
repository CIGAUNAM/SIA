
"""
class MovilidadContext():
    obj = None
    objs = None
    url_categoria = 'movilidad-academica'
    url_seccion = None

    def contexto(self):
        contexto = {'url_categoria': str(self.url_categoria), 'url_seccion': str(self.url_seccion),
                'tab_lista': 'Mis ' + str(self.objs), 'tab_agregar': 'Agregar ' + str(self.obj),
                'tab_detalle': 'Editar ' + str(self.obj),
                'titulo_lista': 'Mis ' + str(self.objs), 'titulo_agregar': 'Agregar ' + str(self.obj),
                'titulo_detalle': 'Editar ' + str(self.obj), 'objeto': str(self.obj).lower(), 'breadcrumb_seccion': str(self.obj), 'titulo_pagina': str(self.objs),
                'titulos_tabla': ['Académico', 'Procedencia', 'País', 'Inicio']}

        tabla_mios = '<script>\n' \
                    '       jQuery(document).ready(function ($jquery) {\n' \
                    '       $jquery("#tabla_json").dataTable({\n' \
                                '"iDisplayLength": 15,\n' \
                                '"ajax": {\n' \
                                    '"processing": true,\n' \
                                    '"url": "/' + str(self.url_categoria) + '/' + str(self.url_seccion) + '/json/",\n' \
                                    '"dataSrc": ""\n' \
                                '},\n' \
                                '"columns": [\n' \
                                    '{\n' \
                                        '"data": "fields.academico",\n' \
                                        '"fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {\n' \
                                            '$(nTd).html("<a href=\'/' + str(self.url_categoria) + '/' + str(self.url_seccion) + '/" + oData.pk + "\'>" + oData.fields.academico + "</a>");\n' \
                                        '}\n' \
                                    '},\n' \
                                    '{"data": "fields.dependencia"},\n' \
                                    '{"data": "fields.pais"},\n' \
                                    '{"data": "fields.fecha_inicio"},\n' \
                                ']\n' \
                            '});\n' \
                        '});\n' \
                  '</script>'

        contexto['tabla_mios'] = tabla_mios
        return contexto
"""
