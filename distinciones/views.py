from django.http.response import (Http404, HttpResponse)
from django.views.generic import View
from django.core import serializers
from SIA.utils import *
from . forms import *
from . utils import *
from . models import *
from django.contrib import messages


# Create your views here.

class DistincionAcademicoJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id

            items = DistincionAcademico.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('distincion', 'institucion', 'fecha'))

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
            item = get_object_or_404(DistincionAcademico, pk=pk, usuario=request.user)
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
                                         fields=('distincion', 'alumno', 'nivel_academico', 'institucion', 'fecha'))

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





class ParticipacionComisionExpertosJSON(View):
    otros = False
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = ParticipacionComisionExpertos.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'institucion', 'fecha_inicio'))

            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ParticipacionComisionExpertosLista(ObjectCreateMixin, View):
    form_class = ParticipacionComisionExpertosForm
    model = ParticipacionComisionExpertos
    aux = ParticipacionComisionExpertosContext.contexto
    template_name = 'comision_expertos.html'


class ParticipacionComisionExpertosDetalle(ObjectUpdateMixin, View):
    form_class = ParticipacionComisionExpertosForm
    model = ParticipacionComisionExpertos
    aux = ParticipacionComisionExpertosContext.contexto
    template_name = 'comision_expertos.html'


class ParticipacionComisionExpertosEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(ParticipacionComisionExpertos, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404




class ParticipacionSociedadCientificaJSON(View):
    otros = False
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = ParticipacionSociedadCientifica.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'fecha_inicio', 'tipo', 'ambito'))

            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ParticipacionSociedadCientificaLista(ObjectCreateMixin, View):
    form_class = ParticipacionSociedadCientificaForm
    model = ParticipacionSociedadCientifica
    aux = ParticipacionSociedadCientificaContext.contexto
    template_name = 'sociedad_cientifica.html'


class ParticipacionSociedadCientificaDetalle(ObjectUpdateMixin, View):
    form_class = ParticipacionSociedadCientificaForm
    model = ParticipacionSociedadCientifica
    aux = ParticipacionSociedadCientificaContext.contexto
    template_name = 'sociedad_cientifica.html'


class ParticipacionSociedadCientificaEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(ParticipacionSociedadCientifica, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class CitaPublicacionJSON(View):
    otros = False
    def get(self, request):

        try:
            usuarioid = User.objects.get(username=request.user.username).id
            if self.otros:
                items = CitaPublicacion.objects.all().exclude(tutores=usuarioid)
            else:
                items = CitaPublicacion.objects.filter(tutores=usuarioid)
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


class CitaPublicacionLista(ObjectCreateVarMixin, View):
    form_class = CitaPublicacionForm
    model = CitaPublicacion
    aux = CitaPublicacionContext.contexto
    template_name = 'cita_publicacion.html'


class CitaPublicacionDetalle(ObjectUpdateVarMixin, View):
    form_class = CitaPublicacionForm
    model = CitaPublicacion
    aux = CitaPublicacionContext.contexto
    template_name = 'cita_publicacion.html'


class CitaPublicacionEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(CitaPublicacion, pk=pk, tutores=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404




