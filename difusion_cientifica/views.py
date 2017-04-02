from django.http.response import (Http404, HttpResponse)
from django.views.generic import View
from django.core import serializers
from SIA.utils import *
from . forms import *
from . utils import *
from . models import *

# Create your views here.

class MemoriaInExtensoJSON(View):
    otros = False
    def get(self, request):

        try:
            usuarioid = User.objects.get(username=request.user.username).id
            if self.otros:
                items = MemoriaInExtenso.objects.all().exclude(usuarios__id__exact=usuarioid)
            else:
                items = MemoriaInExtenso.objects.filter(usuarios__id__exact=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('titulo', 'ciudad', 'fecha', 'evento'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class MemoriaInExtensoLista(ObjectCreateVarMixin, View):
    form_class = MemoriaInExtensoForm
    model = MemoriaInExtenso
    aux = MemoriaInExtensoContext.contexto
    template_name = 'main_otros.html'


class MemoriaInExtensoDetalle(ObjectUpdateVarMixin, View):
    form_class = MemoriaInExtensoForm
    model = MemoriaInExtenso
    aux = MemoriaInExtensoContext.contexto
    template_name = 'main_otros.html'



class PrologoLibroJSON(View):
    otros = False
    def get(self, request):

        try:
            usuarioid = User.objects.get(username=request.user.username).id
            if self.otros:
                items = PrologoLibro.objects.all().exclude(usuarios__id__exact=usuarioid)
            else:
                items = PrologoLibro.objects.filter(usuarios__id__exact=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('libro',))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class PrologoLibroLista(ObjectCreateVarMixin, View):
    form_class = PrologoLibroForm
    model = PrologoLibro
    aux = PrologoLibroContext.contexto
    template_name = 'main_otros.html'


class PrologoLibroDetalle(ObjectUpdateVarMixin, View):
    form_class = PrologoLibroForm
    model = PrologoLibro
    aux = PrologoLibroContext.contexto
    template_name = 'main_otros.html'