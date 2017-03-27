from django.shortcuts import render

from django.http.response import (Http404, HttpResponse)
from django.views.generic import View
from django.core import serializers
from SIA.utils import *
from . forms import *
from . utils import *


# Create your views here.


class ArticuloCientificoJSON(View):
    otros = False
    def get(self, request):

        try:
            usuarioid = User.objects.get(username=request.user.username).id
            if self.otros:
                articulos = ArticuloCientifico.objects.all().exclude(usuarios__id__exact=usuarioid)
            else:
                articulos = ArticuloCientifico.objects.filter(usuarios__id__exact=usuarioid)
            json = serializers.serialize('json', articulos, use_natural_foreign_keys=True,
                                         fields=('titulo', 'tipo', 'revista', 'status', 'fecha'))
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



class CapituloLibroInvestigacionJSON(View):
    otros = False
    def get(self, request):

        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = CapituloLibroInvestigacion.objects.filter(usuario__id__exact=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('titulo', 'libro', 'pagina_inicio', 'pagina_fin'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class CapituloLibroInvestigacionLista(ObjectCreateVarMixin, View):
    form_class = CapituloLibroInvestigacionForm
    model = CapituloLibroInvestigacion
    aux = CapituloLibroInvestigacionContext.contexto
    template_name = 'main_otros.html'


class CapituloLibroInvestigacionDetalle(ObjectUpdateVarMixin, View):
    form_class = CapituloLibroInvestigacionForm
    model = CapituloLibroInvestigacion
    aux = CapituloLibroInvestigacionContext.contexto
    template_name = 'main_otros.html'



class MapaArbitradoJSON(View):
    otros = False
    def get(self, request):

        try:
            usuarioid = User.objects.get(username=request.user.username).id
            if self.otros:
                items = MapaArbitrado.objects.all().exclude(usuarios__id__exact=usuarioid)
            else:
                items = MapaArbitrado.objects.filter(usuarios__id__exact=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('titulo', 'status', 'editorial', 'fecha'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class MapaArbitradoLista(ObjectCreateVarMixin, View):
    form_class = MapaArbitradoForm
    model = MapaArbitrado
    aux = MapaArbitradoContext.contexto
    template_name = 'main_otros.html'


class MapaArbitradoDetalle(ObjectUpdateVarMixin, View):
    form_class = MapaArbitradoForm
    model = MapaArbitrado
    aux = MapaArbitradoContext.contexto
    template_name = 'main_otros.html'



class InformeTecnicoJSON(View):
    otros = False
    def get(self, request):

        try:
            usuarioid = User.objects.get(username=request.user.username).id
            if self.otros:
                items = InformeTecnico.objects.all().exclude(usuarios__id__exact=usuarioid)
            else:
                items = InformeTecnico.objects.filter(usuarios__id__exact=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('titulo', 'fecha', 'numero_paginas'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class InformeTecnicoLista(ObjectCreateVarMixin, View):
    form_class = InformeTecnicoForm
    model = InformeTecnico
    aux = InformeTecnicoContext.contexto
    template_name = 'main_otros.html'


class InformeTecnicoDetalle(ObjectUpdateVarMixin, View):
    form_class = InformeTecnicoForm
    model = InformeTecnico
    aux = InformeTecnicoContext.contexto
    template_name = 'main_otros.html'