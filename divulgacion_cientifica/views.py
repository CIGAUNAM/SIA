from django.http.response import (Http404, HttpResponse)
from django.views.generic import View
from django.core import serializers
from SIA.utils import *
from . forms import *
from . utils import *
from . models import *

#

# Create your views here.

class ArticuloDivulgacionJSON(View):
    otros = False
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            if self.otros:
                items = ArticuloDivulgacion.objects.all().exclude(usuarios__id__exact=usuarioid)
            else:
                items = ArticuloDivulgacion.objects.filter(usuarios__id__exact=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('titulo', 'tipo', 'status', 'revista'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ArticuloDivulgacionLista(ObjectCreateVarMixin, View):
    form_class = ArticuloDivulgacionForm
    model = ArticuloDivulgacion
    aux = ArticuloDivulgacionContext.contexto
    template_name = 'main_otros.html'


class ArticuloDivulgacionDetalle(ObjectUpdateVarMixin, View):
    form_class = ArticuloDivulgacionForm
    model = ArticuloDivulgacion
    aux = ArticuloDivulgacionContext.contexto
    template_name = 'main_otros.html'



class CapituloLibroDivulgacionJSON(View):
    otros = False
    def get(self, request):

        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = CapituloLibroDivulgacion.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('titulo', 'libro'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class CapituloLibroDivulgacionLista(ObjectCreateMixin, View):
    form_class = CapituloLibroDivulgacionForm
    model = CapituloLibroDivulgacion
    aux = CapituloLibroDivulgacionContext.contexto
    template_name = 'main_otros.html'


class CapituloLibroDivulgacionDetalle(ObjectUpdateMixin, View):
    form_class = CapituloLibroDivulgacionForm
    model = CapituloLibroDivulgacion
    aux = CapituloLibroDivulgacionContext.contexto
    template_name = 'main_otros.html'



class OrganizacionEventoDivulgacionJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = OrganizacionEventoDivulgacion.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('evento', 'responsabilidad', 'ambito'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class OrganizacionEventoDivulgacionLista(ObjectCreateMixin, View):
    form_class = OrganizacionEventoDivulgacionForm
    model = OrganizacionEventoDivulgacion
    aux = OrganizacionEventoDivulgacionContext.contexto
    template_name = 'main_otros.html'


class OrganizacionEventoDivulgacionDetalle(ObjectUpdateMixin, View):
    form_class = OrganizacionEventoDivulgacionForm
    model = OrganizacionEventoDivulgacion
    aux = OrganizacionEventoDivulgacionContext.contexto
    template_name = 'main_otros.html'



class ParticipacionEventoDivulgacionJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = ParticipacionEventoDivulgacion.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('titulo', 'evento', 'ambito'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ParticipacionEventoDivulgacionLista(ObjectCreateMixin, View):
    form_class = ParticipacionEventoDivulgacionForm
    model = ParticipacionEventoDivulgacion
    aux = ParticipacionEventoDivulgacionContext.contexto
    template_name = 'main_otros.html'


class ParticipacionEventoDivulgacionDetalle(ObjectUpdateMixin, View):
    form_class = ParticipacionEventoDivulgacionForm
    model = ParticipacionEventoDivulgacion
    template_name = 'main_otros.html'
    aux = ParticipacionEventoDivulgacionContext.contexto



class ProgramaRadioTelevisionInternetJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = ProgramaRadioTelevisionInternet.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('tema', 'fecha', 'nombre_medio', 'medio'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ProgramaRadioTelevisionInternetLista(ObjectCreateMixin, View):
    form_class = ProgramaRadioTelevisionInternetForm
    model = ProgramaRadioTelevisionInternet
    aux = ProgramaRadioTelevisionInternetContext.contexto
    template_name = 'main_otros.html'


class ProgramaRadioTelevisionInternetDivulgacionDetalle(ObjectUpdateMixin, View):
    form_class = ProgramaRadioTelevisionInternetForm
    model = ProgramaRadioTelevisionInternet
    aux = ProgramaRadioTelevisionInternetContext.contexto
    template_name = 'main_otros.html'



