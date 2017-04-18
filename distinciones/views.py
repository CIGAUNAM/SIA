from django.http.response import (Http404, HttpResponse)
from django.views.generic import View
from django.core import serializers
from SIA.utils import *
from . forms import *
from . utils import *
from . models import *

# Create your views here.

class DistincionAcademicoJSON(View):
    otros = False
    def get(self, request):

        try:
            usuarioid = User.objects.get(username=request.user.username).id
            if self.otros:
                items = DistincionAcademico.objects.all().exclude(usuarios__id__exact=usuarioid)
            else:
                items = DistincionAcademico.objects.filter(usuarios__id__exact=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('titulo', 'ciudad', 'fecha', 'evento'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class DistincionAcademicoLista(ObjectCreateVarMixin, View):
    form_class = DistincionAcademicoForm
    model = DistincionAcademico
    aux = DistincionAcademicoContext.contexto
    template_name = 'main_otros.html'


class DistincionAcademicoDetalle(ObjectUpdateVarMixin, View):
    form_class = DistincionAcademicoForm
    model = DistincionAcademico
    aux = DistincionAcademicoContext.contexto
    template_name = 'main_otros.html'


class DistincionAlumnoJSON(View):
    otros = False
    def get(self, request):

        try:
            usuarioid = User.objects.get(username=request.user.username).id
            if self.otros:
                items = DistincionAlumno.objects.all().exclude(usuarios__id__exact=usuarioid)
            else:
                items = DistincionAlumno.objects.filter(usuarios__id__exact=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('titulo', 'ciudad', 'fecha', 'evento'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class DistincionAlumnoLista(ObjectCreateVarMixin, View):
    form_class = DistincionAlumnoForm
    model = DistincionAlumno
    aux = DistincionAlumnoContext.contexto
    template_name = 'main_otros.html'


class DistincionAlumnoDetalle(ObjectUpdateVarMixin, View):
    form_class = DistincionAlumnoForm
    model = DistincionAlumno
    aux = DistincionAlumnoContext.contexto
    template_name = 'main_otros.html'