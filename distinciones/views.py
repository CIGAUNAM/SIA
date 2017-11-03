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
                items = DistincionAcademico.objects.all().exclude(condecorados=usuarioid)
            else:
                items = DistincionAcademico.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('distincion', 'institucion', 'ambito', 'fecha'))

            json = json.replace('INSTITUCIONAL', 'Institucional')
            json = json.replace('REGIONAL', 'Regional')
            json = json.replace('NACIONAL', 'Nacional')
            json = json.replace('INTERNACIONAL', 'Internacional')
            json = json.replace('OTRO', 'Otro')

            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class DistincionAcademicoLista(ObjectCreateMixin, View):
    form_class = DistincionAcademicoForm
    model = DistincionAcademico
    aux = DistincionAcademicoContext.contexto
    template_name = 'distincion_academicos.html'


class DistincionAcademicoDetalle(ObjectUpdateMixin, View):
    form_class = DistincionAcademicoForm
    model = DistincionAcademico
    aux = DistincionAcademicoContext.contexto
    template_name = 'distincion_academicos.html'


class DistincionAcademicoEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(DistincionAcademico, pk=pk, condecorados=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class DistincionAlumnoJSON(View):
    otros = False
    def get(self, request):

        try:
            usuarioid = User.objects.get(username=request.user.username).id
            if self.otros:
                items = DistincionAlumno.objects.all().exclude(tutores=usuarioid)
            else:
                items = DistincionAlumno.objects.filter(tutores=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('distincion', 'alumno', 'grado_academico', 'dependencia', 'ambito', 'fecha'))

            json = json.replace('INSTITUCIONAL', 'Institucional')
            json = json.replace('REGIONAL', 'Regional')
            json = json.replace('NACIONAL', 'Nacional')
            json = json.replace('INTERNACIONAL', 'Internacional')
            json = json.replace('OTRO', 'Otro')

            json = json.replace('LICENCIATURA', 'Licenciatura')
            json = json.replace('MAESTRIA', 'Maestría')
            json = json.replace('DOCTORADO', 'Doctorado')

            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class DistincionAlumnoLista(ObjectCreateVarMixin, View):
    form_class = DistincionAlumnoForm
    model = DistincionAlumno
    aux = DistincionAlumnoContext.contexto
    template_name = 'distincion_alumnos.html'


class DistincionAlumnoDetalle(ObjectUpdateVarMixin, View):
    form_class = DistincionAlumnoForm
    model = DistincionAlumno
    aux = DistincionAlumnoContext.contexto
    template_name = 'distincion_alumnos.html'


class DistincionAlumnoEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(DistincionAlumno, pk=pk, tutores=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404