from rest_framework import permissions
from experiencia_laboral.serializers import *
from rest_framework import generics
from django.http.response import (Http404, HttpResponse)
from django.views.generic import View
from django.core import serializers
from SIA.utils import *
from .forms import *
from .utils import *
from django.db.models import Q


# Create your views here.


class AsesoriaEstudianteJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = AsesoriaEstudiante.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items,
                                         fields=(
                                             'asesorado', 'nivel_academico', 'programa_licenciatura',
                                             'programa_maestria',
                                             'programa_doctorado', 'dependencia', 'fecha_fin'),
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


class AsesoriaEstudianteLista(ObjectCreateMixin, View):
    form_class = AsesoriaEstudianteForm
    model = AsesoriaEstudiante
    aux = AsesoriaEstudianteContext.contexto
    template_name = 'asesoria_estudiante.html'


class AsesoriaEstudianteDetalle(ObjectUpdateMixin, View):
    form_class = AsesoriaEstudianteForm
    model = AsesoriaEstudiante
    aux = AsesoriaEstudianteContext.contexto
    template_name = 'asesoria_estudiante.html'


class AsesoriaEstudianteEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(AsesoriaEstudiante, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404






class SupervisionInvestigadorPostDoctoralJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = SupervisionInvestigadorPostDoctoral.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items,
                                         fields=(
                                             'investigador', 'dependencia', 'fecha_inicio', 'proyecto'),
                                         use_natural_foreign_keys=True)
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class SupervisionInvestigadorPostDoctoralLista(ObjectCreateMixin, View):
    form_class = SupervisionInvestigadorPostDoctoralForm
    model = SupervisionInvestigadorPostDoctoral
    aux = SupervisionInvestigadorPostDoctoralContext.contexto
    template_name = 'supervision_investigador.html'


class SupervisionInvestigadorPostDoctoralDetalle(ObjectUpdateMixin, View):
    form_class = SupervisionInvestigadorPostDoctoralForm
    model = SupervisionInvestigadorPostDoctoral
    aux = SupervisionInvestigadorPostDoctoralContext.contexto
    template_name = 'supervision_investigador.html'


class SupervisionInvestigadorPostDoctoralEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(SupervisionInvestigadorPostDoctoral, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404




class DesarrolloGrupoInvestigacionInternoJSON(View):
    otros = False
    def get(self, request):

        try:
            usuarioid = User.objects.get(username=request.user.username).id
            if self.otros:
                articulos = DesarrolloGrupoInvestigacionInterno.objects.all().exclude(usuarios__id__exact=usuarioid)
            else:
                articulos = DesarrolloGrupoInvestigacionInterno.objects.filter(usuarios__id__exact=usuarioid)

            json = serializers.serialize('json', articulos, use_natural_foreign_keys=True,
                                         fields=('nombre', 'fecha_inicio', 'pais'))

            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class DesarrolloGrupoInvestigacionInternoLista(ObjectCreateVarMixin, View):
    form_class = DesarrolloGrupoInvestigacionInternoForm
    model = DesarrolloGrupoInvestigacionInterno
    aux = DesarrolloGrupoInvestigacionInternoContext.contexto
    template_name = 'grupo_investigacion.html'


class DesarrolloGrupoInvestigacionInternoDetalle(ObjectUpdateVarMixin, View):
    form_class = DesarrolloGrupoInvestigacionInternoForm
    model = DesarrolloGrupoInvestigacionInterno
    aux = DesarrolloGrupoInvestigacionInternoContext.contexto
    template_name = 'grupo_investigacion.html'


class DesarrolloGrupoInvestigacionInternoEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(DesarrolloGrupoInvestigacionInterno, pk=pk, usuarios=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404








class DireccionTesisJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id

            if self.otros:
                items = DireccionTesis.objects.all().exclude(usuarios__id__exact=usuarioid)
            else:
                items = DireccionTesis.objects.filter(usuarios__id__exact=usuarioid)

            json = serializers.serialize('json', items,
                                         fields=(
                                             'titulo', 'asesorado', 'grado_academico', 'dependencia', 'fecha_examen'),
                                         use_natural_foreign_keys=True)
            json = json.replace('LICENCIATURA', 'Licenciatura')
            json = json.replace('MAESTRIA', 'Maestría')
            json = json.replace('DOCTORADO', 'Doctorado')

            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class DireccionTesisLista(ObjectCreateVarMixin, View):
    form_class = DireccionTesisForm
    model = DireccionTesis
    aux = DireccionTesisContext.contexto
    template_name = 'direccion_tesis.html'


class DireccionTesisDetalle(ObjectUpdateVarMixin, View):
    form_class = DireccionTesisForm
    model = DireccionTesis
    aux = DireccionTesisContext.contexto
    template_name = 'direccion_tesis.html'


class DireccionTesisEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(DireccionTesis, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class ComiteTutoralJSON(View):
    otros = False

    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            if self.otros:
                items = ComiteTutoral.objects.all().exclude(asesores=usuarioid).exclude(sinodales=usuarioid)
            else:
                items = ComiteTutoral.objects.filter(Q(asesores=usuarioid) | Q(sinodales=usuarioid))
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=(
                                             'asesorado', 'grado_academico', 'programa_maestria', 'programa_doctorado',
                                             'dependencia', 'proyecto'))
            json = json.replace('"programa_licenciatura": null,', '')
            json = json.replace('"programa_maestria": null,', '')
            json = json.replace('"programa_doctorado": null,', '')
            json = json.replace('LICENCIATURA', 'Licenciatura')
            json = json.replace('MAESTRIA', 'Maestría')
            json = json.replace('DOCTORADO', 'Doctorado')
            json = json.replace('programa_maestria', 'programa')
            json = json.replace('programa_doctorado', 'programa')
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ComiteTutoralLista(ObjectCreateVarMixin, View):
    form_class = ComiteTutoralForm
    model = ComiteTutoral
    aux = ComiteTutoralContext.contexto
    template_name = 'comite_tutoral.html'


class ComiteTutoralDetalle(ObjectUpdateVarMixin, View):
    form_class = ComiteTutoralForm
    model = ComiteTutoral
    aux = ComiteTutoralContext.contexto
    template_name = 'comite_tutoral.html'


class ComiteTutoralEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(ComiteCandidaturaDoctoral, Q(pk=pk, asesor_principal=request.user) | Q(pk=pk, otros_asesores=request.user) | Q(pk=pk, sinodales=request.user))
            item.delete()
            return redirect('../')
        except:
            raise Http404


class ComiteCandidaturaDoctoralJSON(View):
    otros = False

    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            if self.otros:
                items = ComiteCandidaturaDoctoral.objects.all().exclude(asesor_principal=usuarioid).exclude(otros_asesores=usuarioid).exclude(sinodales=usuarioid)
            else:
                items = ComiteCandidaturaDoctoral.objects.filter(Q(asesor_principal=usuarioid) | Q(otros_asesores=usuarioid) | Q(sinodales=usuarioid))
            json = serializers.serialize('json', items, use_natural_foreign_keys=True, fields=('asesorado', 'programa_doctorado', 'proyecto', 'fecha_defensa'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ComiteCandidaturaDoctoralLista(ObjectCreateVarMixin, View):
    form_class = ComiteCandidaturaDoctoralForm
    model = ComiteCandidaturaDoctoral
    aux = ComiteCandidaturaDoctoralContext.contexto
    template_name = 'comite_candidatura_doctoral.html'


class ComiteCandidaturaDoctoralDetalle(ObjectUpdateVarMixin, View):
    form_class = ComiteCandidaturaDoctoralForm
    model = ComiteCandidaturaDoctoral
    aux = ComiteCandidaturaDoctoralContext.contexto
    template_name = 'comite_candidatura_doctoral.html'


class ComiteCandidaturaDoctoralEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(ComiteCandidaturaDoctoral, Q(pk=pk, asesor_principal=request.user) | Q(pk=pk, otros_asesores=request.user) | Q(pk=pk, sinodales=request.user))
            item.delete()
            return redirect('../')
        except:
            raise Http404