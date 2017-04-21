from django.http.response import (Http404, HttpResponse)
from django.views.generic import View
from django.core import serializers
from SIA.utils import *
from . forms import DesarrolloTecnologicoForm
from . models import DesarrolloTecnologico
from . utils import DesarrolloTecnologicoContext
from nucleo.models import User
from django.db.models import Q

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
                                         fields=('nombre_desarrollo_tecnologico', 'patente', 'licencia', 'fecha'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class DesarrolloTecnologicoLista(ObjectCreateVarMixin, View):
    form_class = DesarrolloTecnologicoForm
    model = DesarrolloTecnologico
    aux = DesarrolloTecnologicoContext.contexto
    template_name = 'main.html'



class DesarrolloTecnologicoDetalle(ObjectUpdateVarMixin, View):
    form_class = DesarrolloTecnologicoForm
    model = DesarrolloTecnologico
    aux = DesarrolloTecnologicoContext.contexto
    template_name = 'main.html'


