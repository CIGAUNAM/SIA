from django.shortcuts import render
from django.http.response import (Http404, HttpResponse)
from django.views.generic import View
from django.core import serializers
from SIA.utils import *
from . forms import *
from . utils import *
from . models import *
from django.db.models import Q

# Create your views here.


class MovilidadJSON(View):
    tipo = None
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = MovilidadAcademica.objects.filter(usuario=usuarioid, tipo=self.tipo).values('pk', 'academico__first_name', 'academico__last_name', 'dependencia__dependencia', 'dependencia__ciudad__estado__pais__pais', 'fecha_inicio')
            #for i in items:
            #    i['fecha_inicio'] = str(i['fecha_inicio'])

            json = '['
            for i in items:
                json += '{"model": "movilidad_academica.movilidadacademica", "pk": '
                json += str(i['pk'])
                json += ', "fields": {"academico": '
                json += '"' + str(i['academico__first_name']) + ' ' + str(i['academico__last_name']) + '", '
                json += '"dependencia": ' + '"' + str(i['dependencia__dependencia']) + '", '
                json += '"pais": ' + '"' + str(i['dependencia__ciudad__estado__pais__pais']) + '", '
                json += '"fecha_inicio": ' + '"' + str(i['fecha_inicio']) + '"'
                json += '}}, '
            json += ']'
            json = json.replace('}}, ]', '}}]')
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class MovilidadLista(ObjectCreateMixin, View):
    tipo = None
    form_class = MovilidadAcademicaForm
    model = MovilidadAcademica
    aux = InvitadoContext.contexto
    template_name = 'main_otros.html'

    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            new_obj = bound_form.save(commit=False)
            new_obj.tipo = self.tipo
            new_obj.usuario = request.user
            new_obj = bound_form.save()
            return redirect("/" + self.aux['url_categoria'] + "/" + self.aux['url_seccion'] + "/" + str(new_obj.pk)) #corregir el redirect
        else:
            return render(request, self.template_name, {'form': bound_form, 'aux': self.aux, 'active': 'agregar'})


class MovilidadDetalle(ObjectUpdateMixin, View):
    form_class = MovilidadAcademicaForm
    model = MovilidadAcademica
    aux = InvitadoContext.contexto
    template_name = 'main_otros.html'

    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        bound_form = self.form_class(request.POST, instance=obj)
        if bound_form.is_valid():
            det_obj = bound_form.save()
            return redirect("/" + self.aux['url_categoria'] + "/" + self.aux['url_seccion'] + "/" + str(det_obj.pk)) #corregir el redirect
        else:
            return render(request, self.template_name, {'aux': self.aux, 'form': bound_form, 'active': 'detalle'})