from django.shortcuts import redirect, render, get_object_or_404



class LicenciaturaContext:
    contexto = {'url_categoria': 'formacion', 'url_seccion': 'licenciaturas',
                'tab_lista': 'Mis Licenciaturas', 'tab_agregar': 'Agregar Licenciatura',
                'tab_detalle': 'Editar Licenciatura',
                'titulo_lista': 'Mis Licenciaturas', 'titulo_agregar': 'Agregar Licenciatura',
                'titulo_detalle': 'Editar Licenciatura',
                'objeto': 'licenciatura', 'breadcrumb_seccion': 'Formación académica', 'titulo_pagina': 'Licenciaturas',
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
    contexto = {'url_categoria': 'formacion', 'url_seccion': 'maestrias',
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
    contexto = {'url_categoria': 'formacion', 'url_seccion': 'doctorados',
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
    contexto = {'url_categoria': 'formacion', 'url_seccion': 'postdoctorados',
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
                                        '"data": "fields.titulo",\n' \
                                        '"fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {\n' \
                                            '$(nTd).html("<a href=\'/' + str(contexto['url_categoria']) + '/' + str(contexto['url_seccion']) + '/" + oData.pk + "\'>" + oData.fields.titulo + "</a>");\n' \
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













class ObjectCreateMixin:
    form_class = None
    template_name = ''
    aux = {}

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class, 'aux': self.aux, 'active': 'lista'})

    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            new_obj = bound_form.save(commit=False)
            new_obj.usuario = request.user
            new_obj = bound_form.save()
            return redirect(new_obj)
        else:
            return render(request, self.template_name, {'form': bound_form, 'aux': self.aux, 'active': 'agregar'})


class ObjectUpdateMixin:
    form_class = None
    template_name = ''
    aux = {}

    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk, usuario=request.user)
        return render(request, self.template_name, {'form': self.form_class(instance=obj), 'aux': self.aux, 'active': 'detalle'})

    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk, usuario=request.user)
        bound_form = self.form_class(request.POST, instance=obj)
        if bound_form.is_valid():
            det_obj = bound_form.save(commit=False)
            det_obj.usuario = request.user
            det_obj = bound_form.save()
            return redirect(det_obj)
            self.det_obj.pk
        else:
            return render(request, self.template_name, {'aux': self.aux, 'form': bound_form, 'active': 'detalle'})



