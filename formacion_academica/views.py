from django.shortcuts import render
from django.http.response import HttpResponse

from . permissions import IsOwnerOrReadOnly

from rest_framework import permissions
from formacion_academica.serializers import *
from rest_framework import generics

# Create your views here.


class CursoEspecializacionList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = CursoEspecializacion.objects.all()
    serializer_class = CursoEspecializacionSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class CursoEspecializacionDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = CursoEspecializacion.objects.all()
    serializer_class = CursoEspecializacionSerializer


class LicenciaturaList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = Licenciatura.objects.all()
    serializer_class = LicenciaturaSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class LicenciaturaDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = Licenciatura.objects.all()
    serializer_class = LicenciaturaSerializer


class MaestriaList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = Maestria.objects.all()
    serializer_class = MaestriaSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class MaestriaDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = Maestria.objects.all()
    serializer_class = MaestriaSerializer


class DoctoradoList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = Doctorado.objects.all()
    serializer_class = DoctoradoSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class DoctoradoDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = Doctorado.objects.all()
    serializer_class = DoctoradoSerializer


class PostDoctoradoList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = PostDoctorado.objects.all()
    serializer_class = PostDoctoradoSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class PostDoctoradoDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = PostDoctorado.objects.all()
    serializer_class = PostDoctoradoSerializer