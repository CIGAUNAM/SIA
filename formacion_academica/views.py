from django.http.response import HttpResponse

from .permissions import IsOwnerOrReadOnly

from rest_framework import permissions
from formacion_academica.serializers import *
from rest_framework import generics

from nucleo.models import User

from .models import CursoEspecializacion
from django.http.response import (Http404, HttpResponse)
from django.shortcuts import (render, get_object_or_404, render_to_response, redirect)
from django.views.generic import View

from django.core import serializers

from .forms import *


# Create your views here.

def inicio(request):
    return render(request, 'dashboard.html')


class CursoEspecializacionJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            cursos = CursoEspecializacion.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', cursos,
                                         fields=('nombre_curso', 'fecha_inicio', 'horas', 'dependencia', 'slug'),
                                         use_natural_foreign_keys=True)
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class CursoEspecializacionLista(View):
    form_class = CursoEspecializacionForm

    def contexto_cursos(self):
        return {'categoria_url': 'formacion', 'seccion_url': 'cursos-especializacion', 'tab_lista': 'Mis Cursos',
                'tab_agregar': 'Agregar curso', 'titulo_pagina': 'Cursos de especialización',
                'breadcrumb_seccion': 'Formación académica', 'form': "algo xD"}

    def get(self, request):
        return render(request, 'cursos_especializacion.html',
                      {'active': 'mis_cursos', 'plantilla': self.contexto_cursos(), 'form': self.form_class})

    def post(self, request):
        bound_form = self.form_class(request.POST)

        if bound_form.is_valid():
            bound_form.usuario_id = User.objects.get(username=request.user.username).id
            nuevo_curso = bound_form.save()
            return redirect(nuevo_curso)
        else:
            return render(request, 'cursos_especializacion.html', {'active': 'agregar', 'plantilla': self.contexto_cursos(), 'form': bound_form})



def cursos_json(request):
    try:
        usuarioid = User.objects.get(username=request.user.username).id
        cursos = CursoEspecializacion.objects.filter(usuario=usuarioid)
        json = serializers.serialize('json', cursos,
                                     fields=('nombre_curso', 'fecha_inicio', 'horas', 'dependencia', 'slug'),
                                     use_natural_foreign_keys=True)
        return HttpResponse(json, content_type='application/json')
    except:
        raise Http404


def contexto_cursos():
    return {'categoria_url': 'formacion', 'seccion_url': 'cursos-especializacion', 'tab_lista': 'Mis Cursos',
            'tab_agregar': 'Agregar curso', 'titulo_pagina': 'Cursos de especialización',
            'breadcrumb_seccion': 'Formación académica'}


def curso_especializacion_detalle(request, slug):
    curso = CursoEspecializacion.objects.get(slug=slug)

    return render(request, template_name='cursos_especializacion.html',
                  context={'active': 'curso_detalle', 'curso': curso, 'plantilla': contexto_cursos()})


def curso_especializacion_crear(request):
    if request.method == 'POST':
        form = CursoEspecializacionForm(request.POST)
        if form.is_valid():
            form.usuario = request.user
            nuevo_curso = form.save()
            return redirect(nuevo_curso)
        else:
            pass
    else:
        pass


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
