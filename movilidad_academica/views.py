from django.shortcuts import render
from django.http.response import (Http404, HttpResponse)
from django.views.generic import View
from django.core import serializers
from SIA.utils import *
from .forms import *
from .models import *
from .utils import *
from django.db.models import Q


# Create your views here.


class MovilidadJSON(View):
    tipo = None
    obj = None
    objs = None
    Objs = None
    url_seccion = None

    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = MovilidadAcademica.objects.filter(
                usuario=usuarioid, tipo=self.tipo).values('pk', 'academico__first_name', 'academico__last_name',
                                                          'dependencia__nombre', 'dependencia__ciudad__estado__pais__nombre', 'fecha_inicio')
            json = '['
            for i in items:
                json += '{"model": "movilidad_academica.movilidadacademica", "pk": '
                json += str(i['pk'])
                json += ', "fields": {"academico": '
                json += '"' + str(i['academico__first_name']) + ' ' + str(i['academico__last_name']) + '", '
                json += '"dependencia": ' + '"' + str(i['dependencia__nombre']) + '", '
                json += '"pais": ' + '"' + str(i['dependencia__ciudad__estado__pais__nombre']) + '", '
                json += '"fecha_inicio": ' + '"' + str(i['fecha_inicio']) + '"'
                json += '}}, '
            json += ']'
            json = json.replace('}}, ]', '}}]')
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class MovilidadLista(ObjectCreateMixin, View):
    tipo = None
    obj = None
    objs = None
    Objs = None

    url_seccion = None
    url_categoria = 'movilidad-academica'

    form_class = MovilidadAcademicaForm
    model = MovilidadAcademica


    def contexto(self):

        mi_contexto = {'url_categoria': str(self.url_categoria), 'url_seccion': str(self.url_seccion),
                    'tab_lista': 'Mis ' + str(self.objs), 'tab_agregar': 'Agregar ' + str(self.obj),
                    'tab_detalle': 'Editar ' + str(self.obj),
                    'titulo_lista': 'Mis ' + str(self.objs), 'titulo_agregar': 'Agregar ' + str(self.obj),
                    'titulo_detalle': 'Editar ' + str(self.obj), 'objeto': str(self.obj).lower(),
                    'breadcrumb_seccion': 'Movilidad Académica', 'titulo_pagina': str(self.Objs),
                    'titulos_tabla': ['Académico', 'Procedencia', 'País', 'Inicio']}

        tabla_mios = '<script>\n' \
                     'jQuery(document).ready(function ($jquery) {\n' \
                     '$jquery("#tabla_json").dataTable({\n' \
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

        mi_contexto['tabla_mios'] = tabla_mios
        return mi_contexto

    aux = contexto

    template_name = 'movilidad_academica.html'

    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            new_obj = bound_form.save(commit=False)
            new_obj.tipo = self.tipo
            new_obj.usuario = request.user
            new_obj = bound_form.save()
            return redirect("/" + self.url_categoria + "/" + self.url_seccion + "/" + str(
                new_obj.pk))  # corregir el redirect
        else:
            return render(request, self.template_name, {'form': bound_form, 'aux': self.aux, 'active': 'agregar'})


class MovilidadDetalle(ObjectUpdateMixin, View):
    form_class = MovilidadAcademicaForm
    model = MovilidadAcademica
    tipo = None
    obj = None
    objs = None
    Objs = None
    url_seccion = None
    url_categoria = 'movilidad-academica'

    def contexto(self):

        mi_contexto = {'url_categoria': str(self.url_categoria), 'url_seccion': str(self.url_seccion),
                    'tab_lista': 'Mis ' + str(self.objs), 'tab_agregar': 'Agregar ' + str(self.obj),
                    'tab_detalle': 'Editar ' + str(self.obj),
                    'titulo_lista': 'Mis ' + str(self.objs), 'titulo_agregar': 'Agregar ' + str(self.obj),
                    'titulo_detalle': 'Editar ' + str(self.obj), 'objeto': str(self.obj).lower(),
                    'breadcrumb_seccion': 'Movilidad Académica', 'titulo_pagina': str(self.Objs),
                    'titulos_tabla': ['Académico', 'Procedencia', 'País', 'Inicio']}

        tabla_mios = '<script>\n' \
                     'jQuery(document).ready(function ($jquery) {\n' \
                     '$jquery("#tabla_json").dataTable({\n' \
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

        mi_contexto['tabla_mios'] = tabla_mios
        return mi_contexto

    aux = contexto

    template_name = 'movilidad_academica.html'

    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        bound_form = self.form_class(request.POST, instance=obj)
        if bound_form.is_valid():
            det_obj = bound_form.save()
            return redirect("/" + self.url_categoria + "/" + self.url_seccion + "/" + str(det_obj.pk))  # corregir el redirect
        else:
            return render(request, self.template_name, {'aux': self.aux, 'form': bound_form, 'active': 'detalle'})


class MovilidadAcademicaEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(MovilidadAcademica, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404



##


class InvitadoMovilidadJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = InvitadoMovilidad.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items,
                                         fields=('invitado', 'dependencia', 'pais', 'fecha_inicio'),
                                         use_natural_foreign_keys=True)
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404



class InvitadoMovilidadLista(ObjectCreateMixin, View):
    form_class = InvitadoMovilidadForm
    model = InvitadoMovilidad
    aux = InvitadoMovilidadContext.contexto
    template_name = 'invitado_movilidad.html'


class InvitadoMovilidadDetalle(ObjectUpdateMixin, View):
    form_class = InvitadoMovilidadForm
    model = InvitadoMovilidad
    aux = InvitadoMovilidadContext.contexto
    template_name = 'invitado_movilidad.html'


class InvitadoMovilidadEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(InvitadoMovilidad, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class EstanciaMovilidadJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = EstanciaMovilidad.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items,
                                         fields=('anfitrion', 'dependencia', 'pais', 'fecha_inicio'),
                                         use_natural_foreign_keys=True)
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class EstanciaMovilidadLista(ObjectCreateMixin, View):
    form_class = EstanciaMovilidadForm
    model = EstanciaMovilidad
    aux = EstanciaMovilidadContext.contexto
    template_name = 'estancia_movilidad.html'


class EstanciaMovilidadDetalle(ObjectUpdateMixin, View):
    form_class = EstanciaMovilidadForm
    model = EstanciaMovilidad
    aux = EstanciaMovilidadContext.contexto
    template_name = 'estancia_movilidad.html'


class EstanciaMovilidadEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(EstanciaMovilidad, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404



class SabaticoMovilidadJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = SabaticoMovilidad.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items,
                                         fields=('anfitrion', 'dependencia', 'pais', 'fecha_inicio'),
                                         use_natural_foreign_keys=True)
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class SabaticoMovilidadLista(ObjectCreateMixin, View):
    form_class = SabaticoMovilidadForm
    model = SabaticoMovilidad
    aux = SabaticoMovilidadContext.contexto
    template_name = 'sabatico_movilidad.html'


class SabaticoMovilidadDetalle(ObjectUpdateMixin, View):
    form_class = SabaticoMovilidadForm
    model = SabaticoMovilidad
    aux = SabaticoMovilidadContext.contexto
    template_name = 'sabatico_movilidad.html'


class SabaticoMovilidadEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(SabaticoMovilidad, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404
