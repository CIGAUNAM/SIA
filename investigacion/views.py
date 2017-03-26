from django.shortcuts import render

from django.http.response import (Http404, HttpResponse)
from django.views.generic import View
from django.core import serializers
from SIA.utils import *
from . forms import *
from . utils import *


# Create your views here.


class ArticuloCientificoJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            #articulos = ArticuloCientifico.objects.all().exclude(usuarios__id__exact=usuarioid)
            articulos = ArticuloCientifico.objects.filter(usuarios__id__exact=usuarioid)
            json = serializers.serialize('json', articulos,
                                         fields=('titulo', 'tipo', 'revista', 'status', 'fecha'),
                                         use_natural_foreign_keys=True)

            print(type(json))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ArticuloCientificoLista(ObjectCreateVarMixin, View):
    form_class = ArticuloCientificoForm
    model = ArticuloCientifico
    aux = ArticuloCientificoContext.contexto
    template_name = 'main_otros.html'


class ArticuloCientificoDetalle(ObjectUpdateVarMixin, View):
    form_class = ArticuloCientificoForm
    model = ArticuloCientifico
    aux = ArticuloCientificoContext.contexto
    template_name = 'main_otros.html'