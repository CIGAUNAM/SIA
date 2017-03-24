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
from .utils import *

# Create your views here.

def inicio(request):
    return render(request, 'dashboard.html')


class CursoEspecializacionJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            cursos = CursoEspecializacion.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', cursos,
                                         fields=('nombre_curso', 'fecha_inicio', 'horas', 'dependencia'),
                                         use_natural_foreign_keys=True)
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class CursoEspecializacionLista(View):
    form_class = CursoEspecializacionForm
    active = None

    def contexto_cursos(self):
        return {'categoria_url': 'formacion', 'seccion_url': 'cursos-especializacion', 'tab_lista': 'Mis Cursos',
                'tab_agregar': 'Agregar curso', 'titulo_pagina': 'Cursos de especialización',
                'breadcrumb_seccion': 'Formación académica', 'form': "algo xD"}

    def get(self, request):
        self.active = 'mis_cursos'
        return render(request, 'cursos_especializacion.html',
                      {'active': self.active, 'plantilla': self.contexto_cursos(), 'form': self.form_class})

    def post(self, request):
        self.active = 'curso_detalle'
        bound_form = self.form_class(request.POST)

        if bound_form.is_valid():
            nuevo_curso = bound_form.save(commit=False)
            nuevo_curso.usuario = request.user
            nuevo_curso = bound_form.save()

            return redirect(nuevo_curso)
        else:
            return render(request, 'cursos_especializacion.html', {'active': 'agregar', 'plantilla': self.contexto_cursos(), 'form': bound_form})


class CursoEspecializacionDetalle(View):
    form_class = CursoEspecializacionForm
    model = CursoEspecializacion

    def contexto_cursos(self):
        return {'categoria_url': 'formacion', 'seccion_url': 'cursos-especializacion', 'tab_lista': 'Mis Cursos',
                'tab_agregar': 'Agregar curso', 'titulo_pagina': 'Cursos de especialización',
                'breadcrumb_seccion': 'Formación académica', 'form': "algo xD"}

    def get(self, request, pk):
        curso = get_object_or_404(self.model, pk=pk, usuario=request.user)
        context = {'active': 'detalle', 'plantilla': self.contexto_cursos(), 'form': self.form_class(instance=curso), 'curso': curso}
        return render(request, 'cursos_especializacion.html', context)

    def post(self, request, pk):
        curso = get_object_or_404(self.model, pk=pk, usuario=request.user)
        bound_form = self.form_class(request.POST, instance=curso)

        if bound_form.is_valid():
            detalle_curso = bound_form.save(commit=False)
            detalle_curso.usuario = request.user
            detalle_curso = bound_form.save()
            return redirect(detalle_curso)
        else:
            return render(request, 'cursos_especializacion.html', {'active': 'curso_detalle', 'plantilla': self.contexto_cursos(), 'form': bound_form})



class LicenciaturaJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            licenciaturas = Licenciatura.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', licenciaturas,
                                         fields=('carrera', 'titulo_tesis', 'fecha_grado', 'dependencia'),
                                         use_natural_foreign_keys=True)
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class LicenciaturaLista(View, LicenciaturaContext):
    form_class = LicenciaturaForm

    def get(self, request):
        return render(request, 'licenciaturas.html', {'active': 'lista', 'plantilla': self.contexto, 'form': self.form_class})

    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            nueva_licenciatura = bound_form.save(commit=False)
            nueva_licenciatura.usuario = request.user
            nueva_licenciatura = bound_form.save()

            return redirect(nueva_licenciatura)
        else:
            return render(request, 'licenciaturas.html', {'active': 'agregar', 'plantilla': self.contexto, 'form': bound_form})


class LicenciaturaDetalle(View, LicenciaturaContext):
    form_class = LicenciaturaForm
    model = Licenciatura

    def get(self, request, pk):
        objeto = get_object_or_404(self.model, pk=pk, usuario=request.user)
        context = {'active': 'detalle', 'plantilla': self.contexto, 'form': self.form_class(instance=objeto), 'objeto': objeto}
        return render(request, 'licenciaturas.html', context)

    def post(self, request, pk):
        objeto = get_object_or_404(self.model, pk=pk, usuario=request.user)
        bound_form = self.form_class(request.POST, instance=objeto)

        if bound_form.is_valid():
            detalle_curso = bound_form.save(commit=False)
            detalle_curso.usuario = request.user
            detalle_curso = bound_form.save()
            return redirect(detalle_curso)
        else:
            return render(request, 'licenciaturas.html', {'active': 'detalle', 'plantilla': self.contexto, 'form': bound_form})





class MaestriaJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            maestrias = Maestria.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', maestrias,
                                         fields=('programa', 'titulo_tesis', 'fecha_grado', 'dependencia'),
                                         use_natural_foreign_keys=True)
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class MaestriaLista(ObjectCreateMixin, View):
    form_class = MaestriaForm
    model = Maestria
    contexto = MaestriaContext
    template_name = 'formacion_academica_u.html'


class MaestriaDetalle(ObjectCreateMixin, View):
    form_class = MaestriaForm
    model = Maestria
    template_name = 'formacion_academica_u.html'
















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
