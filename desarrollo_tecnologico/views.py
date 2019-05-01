from django.http.response import (Http404, HttpResponse)
from django.views.generic import View
from django.core import serializers
from SIA.utils import *
from .forms import DesarrolloTecnologicoForm, LicenciaForm
from .models import DesarrolloTecnologico, Licencia
from .utils import DesarrolloTecnologicoContext, LicenciaContext
from nucleo.models import User
from django.contrib import messages

# Create your views here.


class DesarrolloTecnologicoJSON(View):
    otros = False

    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id

            if self.otros:
                items = DesarrolloTecnologico.objects.all().exclude(autores=usuarioid)
            else:
                items = DesarrolloTecnologico.objects.filter(autores=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'patente', 'licencia', 'fecha'))
            return HttpResponse(json, content_type='application/json2')
        except:
            raise Http404


class DesarrolloTecnologicoLista(ObjectCreateVarMixin, View):
    form_class = DesarrolloTecnologicoForm
    model = DesarrolloTecnologico
    aux = DesarrolloTecnologicoContext.contexto
    aux['success'] = False
    template_name = 'desarrollo_tecnologico.html'


class DesarrolloTecnologicoDetalle(ObjectUpdateVarMixin, View):
    form_class = DesarrolloTecnologicoForm
    model = DesarrolloTecnologico
    aux = DesarrolloTecnologicoContext.contexto

    template_name = 'desarrollo_tecnologico.html'

    def post(self, request, pk):
        self.aux['success'] = False
        obj = get_object_or_404(self.model, pk=pk)
        bound_form = self.form_class(request.POST, instance=obj)
        if bound_form.is_valid():
            det_obj = bound_form.save()
            messages.success(request, "Registro actualizado con éxito")
            return redirect('./')
        else:
            return render(request, self.template_name, {'aux': self.aux, 'form': bound_form, 'active': 'detalle'})


class DesarrolloTecnologicoEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(DesarrolloTecnologico, pk=pk, usuarios=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class LicenciaJSON(View):
    def get(self, request):
        try:
            items = Licencia.objects.all()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', ))
            return HttpResponse(json, content_type='application/json2')
        except:
            raise Http404


class LicenciaLista(ObjectCreateMixinNucleo, View):
    form_class = LicenciaForm
    model = Licencia
    aux = LicenciaContext.contexto
    template_name = 'main.html'


class LicenciaDetalle(ObjectUpdateMixinNucleo, View):
    form_class = LicenciaForm
    model = Licencia
    aux = LicenciaContext.contexto
    template_name = 'main.html'


class LicenciaEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(Licencia, pk=pk)
            item.delete()
            return redirect('../')
        except:
            raise Http404
