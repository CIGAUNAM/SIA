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

class InvitadoJSON(View):
    otros = False
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = MovilidadAcademica.objects.filter(usuario=usuarioid, tipo='INVITACION').only('academico__first_name',
                                                                                            'academico__last_name',
                                                                                            'dependencia__ciudad__estado__pais__pais',
                                                                                            'fecha_inicio')
            json = serializers.serialize('json', items, use_natural_foreign_keys=True)
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class InvitadoLista(ObjectCreateMixin, View):
    form_class = MovilidadAcademicaForm
    model = MovilidadAcademica
    aux = InvitadoContext.contexto
    template_name = 'main_otros.html'

    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            new_obj = bound_form.save(commit=False)
            new_obj.tipo = 'INVITACION'
            new_obj.usuario = request.user
            new_obj = bound_form.save()
            return redirect("/" + self.aux['url_categoria'] + "/" + self.aux['url_seccion'] + "/" + str(new_obj.pk)) #corregir el redirect
        else:
            return render(request, self.template_name, {'form': bound_form, 'aux': self.aux, 'active': 'agregar'})


class InvitadoDetalle(ObjectUpdateMixin, View):
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