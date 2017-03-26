from django.shortcuts import redirect, render, get_object_or_404

class ExperienciaLaboralContext:
    contexto = {'url_categoria': 'experiencia', 'url_seccion': 'laborales',
                'tab_lista': 'Mis Experiencias Laborales', 'tab_agregar': 'Agregar Experiencia Laboral',
                'tab_detalle': 'Editar Experiencia Laboral',
                'titulo_lista': 'Mis Licenciaturas', 'titulo_agregar': 'Agregar Experiencia Laboral',
                'titulo_detalle': 'Editar Experiencia Laboral',
                'objeto': 'experiencia laboral', 'breadcrumb_seccion': 'Experiencia Laboral', 'titulo_pagina': 'Experiencias Laborales',
                'titulos_tabla': ['Nombramiento', 'Cargo', 'Fecha de inicio', 'Dependencia']}


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
                                        '"data": "fields.cargo",\n' \
                                        '"fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {\n' \
                                            '$(nTd).html("<a href=\'/' + str(contexto['url_categoria']) + '/' + str(contexto['url_seccion']) + '/" + oData.pk + "\'>" + oData.fields.cargo + "</a>");\n' \
                                        '}\n' \
                                    '},\n' \
                                    '{"data": "fields.nombramiento"},\n' \
                                    '{"data": "fields.fecha_inicio"},\n' \
                                    '{"data": "fields.dependencia"},\n' \
                                ']\n' \
                            '});\n' \
                        '});\n' \
                  '</script>'

    contexto['tabla_mios'] = tabla_mios


class LineaInvestigacionContext:
    jkljkl = "shalala"
    contexto = {'url_categoria': 'experiencia', 'url_seccion': 'lineas-investigacion',
                'tab_lista': 'Mis Lìneas de Investigación', 'tab_agregar': 'Agregar Lìnea de Investigación',
                'tab_detalle': 'Editar Lìnea de Investigación',
                'titulo_lista': 'Mis Lìneas de Investigación', 'titulo_agregar': 'Agregar Lìnea de Investigación',
                'titulo_detalle': 'Editar Lìnea de Investigación',
                'objeto': 'lìnea de investigación' + jkljkl, 'breadcrumb_seccion': 'Lìneas de Investigación', 'titulo_pagina': 'Lìneas de Investigación',
                'titulos_tabla': ['Lìnea de Investigación', 'Fecha de inicio', 'Dependencia']}


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
                                        '"data": "fields.linea_investigacion",\n' \
                                        '"fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {\n' \
                                            '$(nTd).html("<a href=\'/' + str(contexto['url_categoria']) + '/' + str(contexto['url_seccion']) + '/" + oData.pk + "\'>" + oData.fields.linea_investigacion + "</a>");\n' \
                                        '}\n' \
                                    '},\n' \
                                    '{"data": "fields.fecha_inicio"},\n' \
                                    '{"data": "fields.dependencia"},\n' \
                                ']\n' \
                            '});\n' \
                        '});\n' \
                  '</script>'

    contexto['tabla_mios'] = tabla_mios



class CapacidadPotencialidadContext:
    contexto = {'url_categoria': 'experiencia', 'url_seccion': 'capacidades',
                'tab_lista': 'Mis Capacidades y Potencialidades', 'tab_agregar': 'Agregar Capacidad o Potencialidad',
                'tab_detalle': 'Editar Capacidad o Potencialidad',
                'titulo_lista': 'Mis Capacidades y Potencialidades', 'titulo_agregar': 'Agregar Capacidad o Potencialidad',
                'titulo_detalle': 'Editar Capacidad o Potencialidad',
                'objeto': 'competencia', 'breadcrumb_seccion': 'Capacidades y Potencialidades', 'titulo_pagina': 'Capacidades y Potencialidades',
                'titulos_tabla': ['Competencia', 'Fecha de inicio']}


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
                                        '"data": "fields.competencia",\n' \
                                        '"fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {\n' \
                                            '$(nTd).html("<a href=\'/' + str(contexto['url_categoria']) + '/' + str(contexto['url_seccion']) + '/" + oData.pk + "\'>" + oData.fields.competencia + "</a>");\n' \
                                        '}\n' \
                                    '},\n' \
                                    '{"data": "fields.fecha_inicio"},\n' \
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



