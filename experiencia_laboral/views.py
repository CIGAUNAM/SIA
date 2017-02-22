from django.shortcuts import render
from django.http.response import HttpResponse

from . permissions import IsOwnerOrReadOnly

from rest_framework import permissions
from experiencia_laboral.serializers import *
from rest_framework import generics

# Create your views here.


class ExperienciaLaboralList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = ExperienciaLaboral.objects.all()
    serializer_class = ExperienciaLaboralSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class ExperienciaLaboralDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = ExperienciaLaboral.objects.all()
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