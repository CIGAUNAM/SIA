
from django.http.response import HttpResponse


from . permissions import IsOwnerOrReadOnly

from rest_framework import permissions
from formacion_academica.serializers import *
from rest_framework import generics

from nucleo.models import User

from . models import CursoEspecializacion
from django.http.response import (Http404, HttpResponse)
from django.shortcuts import (render, get_object_or_404, render_to_response)

from django.core import serializers




# Create your views here.



def inicio(request):
    return render(request, 'dashboard.html')


def cursos_json(request):
    try:
        usuarioid = User.objects.get(username=request.user.username).id
        cursos = CursoEspecializacion.objects.filter(usuario=usuarioid)
        json = serializers.serialize('json', cursos, fields=('nombre_curso','tipo', 'horas', 'dependencia', 'slug'), use_natural_foreign_keys=True)
        return HttpResponse(json, content_type='application/json')
    except:
        raise Http404


def cursos_especializacion(request):
    return render(request, 'cursos_especializacion.html', {'active': 'mis_cursos'})


def curso_especializacion_detalle(request, slug):
    plantilla = {'categoria': 'formacion', 'seccion': 'cursos-especializacion', 'titulo_lista': 'Mis Cursos'}

    curso = CursoEspecializacion.objects.get(slug=slug)

    return render(request, template_name='cursos_especializacion.html', context={'active': 'curso_detalle', 'curso': curso, 'plantilla': plantilla})


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