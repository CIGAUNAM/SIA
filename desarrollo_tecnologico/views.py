from django.http.response import (Http404, HttpResponse)
from django.views.generic import View
from django.core import serializers
from SIA.utils import *
from . forms import DesarrolloTecnologicoForm
from . models import DesarrolloTecnologico
from nucleo.models import User
from django.db.models import Q

# Create your views here.


class DesarrolloTecnologicoJSON(View):
    otros = False
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id

            if self.otros:
                items = DesarrolloTecnologico.objects.filter(tipo='ESCOLARIZADO').exclude(usuarios__id__exact=usuarioid).exclude(usuario=usuarioid)
            else:
                items = DesarrolloTecnologico.objects.filter(Q(usuarios__id__exact=usuarioid, tipo='ESCOLARIZADO') | Q(usuario=usuarioid, tipo='ESCOLARIZADO'))
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('asignatura', 'nivel', 'dependencia', 'fecha_inicio', 'total_horas'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class DesarrolloTecnologicoLista(ObjectCreateMixin, View):
    form_class = DesarrolloTecnologicoForm
    model = DesarrolloTecnologico
    aux = DesarrolloTecnologicoContext.contexto
    template_name = 'main_otros.html'

    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            new_obj = bound_form.save(commit=False)
            new_obj.tipo = 'ESCOLARIZADO'
            new_obj.usuario = request.user
            new_obj = bound_form.save()
            return redirect("/" + self.aux['url_categoria'] + "/" + self.aux['url_seccion'] + "/" + str(new_obj.pk)) #corregir el redirect
        else:
            return render(request, self.template_name, {'form': bound_form, 'aux': self.aux, 'active': 'agregar'})


class DesarrolloTecnologicoDetalle(ObjectUpdateMixin, View):
    form_class = DesarrolloTecnologicoForm
    model = DesarrolloTecnologico
    aux = DesarrolloTecnologicoContext.contexto
    template_name = 'main_otros.html'

    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        bound_form = self.form_class(request.POST, instance=obj)
        if bound_form.is_valid():
            det_obj = bound_form.save()
            return redirect("/" + self.aux['url_categoria'] + "/" + self.aux['url_seccion'] + "/" + str(det_obj.pk)) #corregir el redirect
        else:
            return render(request, self.template_name, {'aux': self.aux, 'form': bound_form, 'active': 'detalle'})

