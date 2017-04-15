from rest_framework import permissions
from experiencia_laboral.serializers import *
from rest_framework import generics
from django.http.response import (Http404, HttpResponse)
from django.views.generic import View
from django.core import serializers
from SIA.utils import *
from . forms import *
from . utils import *

# Create your views here.


class AsesorEstanciaJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = AsesorEstancia.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items,
                                         fields=('asesorado', 'grado_academico', 'programa_licenciatura', 'programa_maestria', 'programa_doctorado', 'dependencia', 'fecha_fin'),
                                         use_natural_foreign_keys=True)
            json = json.replace('"programa_licenciatura": null,', '')
            json = json.replace('"programa_maestria": null,', '')
            json = json.replace('"programa_doctorado": null,', '')
            json = json.replace('programa_licenciatura', 'programa')
            json = json.replace('programa_maestria', 'programa')
            json = json.replace('programa_doctorado', 'programa')
            json = json.replace('LICENCIATURA', 'Licenciatura')
            json = json.replace('MAESTRIA', 'Maestría')
            json = json.replace('DOCTORADO', 'Doctorado')

            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class AsesorEstanciaLista(ObjectCreateMixin, View):
    form_class = AsesorEstanciaForm
    model = AsesorEstancia
    aux = AsesorEstanciaContext.contexto
    template_name = 'main_otros.html'


class AsesorEstanciaDetalle(ObjectUpdateMixin, View):
    form_class = AsesorEstanciaForm
    model = AsesorEstancia
    aux = AsesorEstanciaContext.contexto
    template_name = 'main_otros.html'



class DireccionTesisJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = DireccionTesis.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items,
                                         fields=('titulo', 'asesorado', 'grado_academico', 'dependencia', 'fecha_examen'),
                                         use_natural_foreign_keys=True)
            json = json.replace('LICENCIATURA', 'Licenciatura')
            json = json.replace('MAESTRIA', 'Maestría')
            json = json.replace('DOCTORADO', 'Doctorado')

            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class DireccionTesisLista(ObjectCreateMixin, View):
    form_class = DireccionTesisForm
    model = DireccionTesis
    aux = DireccionTesisContext.contexto
    template_name = 'main_otros.html'


class DireccionTesisDetalle(ObjectUpdateMixin, View):
    form_class = DireccionTesisForm
    model = DireccionTesis
    aux = DireccionTesisContext.contexto
    template_name = 'main_otros.html'