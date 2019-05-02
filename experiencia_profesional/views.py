from django.shortcuts import render

from . permissions import IsOwnerOrReadOnly
from rest_framework import permissions
from experiencia_profesional.serializers import *
from rest_framework import generics
from django.http.response import (Http404, HttpResponse)
from django.views.generic import View
from django.core import serializers
from SIA.utils import *
from . forms import *
from . utils import *


# Create your views here.



class ExperienciaProfesionalJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            experiencias = ExperienciaProfesional.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', experiencias,
                                         fields=('cargo2', 'nombramiento', 'fecha_inicio', 'institucion'),
                                         use_natural_foreign_keys=True)
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ExperienciaProfesionalLista(ObjectCreateMixin, View):
    form_class = ExperienciaLaboralForm
    model = ExperienciaProfesional
    aux = ExperienciaLaboralContext.contexto
    template_name = 'experiencia_profesional.html'


class ExperienciaProfesionalDetalle(ObjectUpdateMixin, View):
    form_class = ExperienciaLaboralForm
    model = ExperienciaProfesional
    aux = ExperienciaLaboralContext.contexto

    template_name = 'experiencia_profesional.html'


class ExperienciaProfesionalEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(ExperienciaProfesional, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class LineaInvestigacionJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            experiencias = LineaInvestigacion.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', experiencias,
                                         fields=('linea_investigacion', 'fecha_inicio', 'institucion'),
                                         use_natural_foreign_keys=True)
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class LineaInvestigacionLista(ObjectCreateMixin, View):
    form_class = LineaInvestigacionForm
    model = LineaInvestigacion
    aux = LineaInvestigacionContext.contexto
    template_name = 'linea_investigacion.html'


class LineaInvestigacionDetalle(ObjectUpdateMixin, View):
    form_class = LineaInvestigacionForm
    model = LineaInvestigacion
    aux = LineaInvestigacionContext.contexto
    template_name = 'linea_investigacion.html'


class LineaInvestigacionEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(LineaInvestigacion, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class CapacidadPotencialidadJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            experiencias = CapacidadPotencialidad.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', experiencias,
                                         fields=('nombre', 'fecha_inicio'),
                                         use_natural_foreign_keys=True)
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class CapacidadPotencialidadLista(ObjectCreateMixin, View):
    form_class = CapacidadPotencialidadForm
    model = CapacidadPotencialidad
    aux = CapacidadPotencialidadContext.contexto
    template_name = 'capacidad_potencialidad.html'


class CapacidadPotencialidadDetalle(ObjectUpdateMixin, View):
    form_class = CapacidadPotencialidadForm
    model = CapacidadPotencialidad
    aux = CapacidadPotencialidadContext.contexto
    template_name = 'capacidad_potencialidad.html'


class CapacidadPotencialidadEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(CapacidadPotencialidad, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404




















class ExperienciaLaboralList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = ExperienciaProfesional.objects.all()
    serializer_class = ExperienciaLaboralSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class ExperienciaLaboralDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = ExperienciaProfesional.objects.all()
    serializer_class = ExperienciaLaboralSerializer


class LineaInvestigacionList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = LineaInvestigacion.objects.all()
    serializer_class = LineaInvestigacionSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class LineaInvestigacionDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = LineaInvestigacion.objects.all()
    serializer_class = LineaInvestigacionSerializer


class CapacidadPotencialidadList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = CapacidadPotencialidad.objects.all()
    serializer_class = CapacidadPotencialidadSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class CapacidadPotencialidadDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = CapacidadPotencialidad.objects.all()
    serializer_class = CapacidadPotencialidadSerializer