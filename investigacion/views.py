from django.shortcuts import render

from django.http.response import (Http404, HttpResponse)
from django.views.generic import View
from django.core import serializers
from SIA.utils import *
from . forms import *
from . utils import *


# Create your views here.


class ArticuloCientificoJSON(View):
    otros = False
    def get(self, request):

        try:
            usuarioid = User.objects.get(username=request.user.username).id
            if self.otros:
                articulos = ArticuloCientifico.objects.all().exclude(usuarios__id__exact=usuarioid)
            else:
                articulos = ArticuloCientifico.objects.filter(usuarios__id__exact=usuarioid)
            json = serializers.serialize('json', articulos, use_natural_foreign_keys=True,
                                         fields=('titulo', 'tipo', 'revista', 'status', 'fecha'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ArticuloCientificoLista(ObjectCreateVarMixin, View):
    form_class = ArticuloCientificoForm
    model = ArticuloCientifico
    aux = ArticuloCientificoContext.contexto
    template_name = 'articulo_cientifico.html'


class ArticuloCientificoDetalle(ObjectUpdateVarMixin, View):
    form_class = ArticuloCientificoForm
    model = ArticuloCientifico
    aux = ArticuloCientificoContext.contexto
    template_name = 'articulo_cientifico.html'


class ArticuloCientificoEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(ArticuloCientifico, pk=pk, usuarios=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class CapituloLibroInvestigacionJSON(View):
    otros = False
    def get(self, request):

        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = CapituloLibroInvestigacion.objects.filter(usuario__id__exact=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('titulo', 'libro', 'pagina_inicio', 'pagina_fin'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class CapituloLibroInvestigacionLista(ObjectCreateMixin, View):
    form_class = CapituloLibroInvestigacionForm
    model = CapituloLibroInvestigacion
    aux = CapituloLibroInvestigacionContext.contexto
    template_name = 'capitulo_libro.html'


class CapituloLibroInvestigacionDetalle(ObjectUpdateMixin, View):
    form_class = CapituloLibroInvestigacionForm
    model = CapituloLibroInvestigacion
    aux = CapituloLibroInvestigacionContext.contexto
    template_name = 'capitulo_libro.html'


class CapituloLibroInvestigacionEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(CapituloLibroInvestigacion, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class MapaArbitradoJSON(View):
    otros = False
    def get(self, request):

        try:
            usuarioid = User.objects.get(username=request.user.username).id
            if self.otros:
                items = MapaArbitrado.objects.all().exclude(usuarios__id__exact=usuarioid)
            else:
                items = MapaArbitrado.objects.filter(usuarios__id__exact=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('titulo', 'status', 'editorial', 'fecha'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class MapaArbitradoLista(ObjectCreateVarMixin, View):
    form_class = MapaArbitradoForm
    model = MapaArbitrado
    aux = MapaArbitradoContext.contexto
    template_name = 'mapa_arbitrado.html'


class MapaArbitradoDetalle(ObjectUpdateVarMixin, View):
    form_class = MapaArbitradoForm
    model = MapaArbitrado
    aux = MapaArbitradoContext.contexto
    template_name = 'mapa_arbitrado.html'


class MapaArbitradoEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(MapaArbitrado, pk=pk, usuarios=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class InformeTecnicoJSON(View):
    otros = False
    def get(self, request):

        try:
            usuarioid = User.objects.get(username=request.user.username).id
            if self.otros:
                items = InformeTecnico.objects.all().exclude(usuarios__id__exact=usuarioid)
            else:
                items = InformeTecnico.objects.filter(usuarios__id__exact=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('titulo', 'fecha', 'numero_paginas'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class InformeTecnicoLista(ObjectCreateVarMixin, View):
    form_class = InformeTecnicoForm
    model = InformeTecnico
    aux = InformeTecnicoContext.contexto
    template_name = 'informe_tecnico_publico.html'


class InformeTecnicoDetalle(ObjectUpdateVarMixin, View):
    form_class = InformeTecnicoForm
    model = InformeTecnico
    aux = InformeTecnicoContext.contexto
    template_name = 'informe_tecnico_publico.html'


class InformeTecnicoEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(InformeTecnico, pk=pk, usuarios=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class LibroInvestigacionJSON(View):
    otros = False
    def get(self, request):

        try:
            usuarioid = User.objects.get(username=request.user.username).id
            if self.otros:
                items = LibroInvestigacion.objects.filter(tipo='INVESTIGACION').exclude(usuarios__id__exact=usuarioid)
            else:
                items = LibroInvestigacion.objects.filter(usuarios__id__exact=usuarioid, tipo='INVESTIGACION')
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'editorial', 'ciudad', 'status', 'fecha'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class LibroInvestigacionLista(ObjectCreateVarMixin, View):
    form_class = LibroInvestigacionForm
    model = LibroInvestigacion
    aux = LibroInvestigacionContext.contexto
    template_name = 'libro_investigacion.html'

    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            new_obj = bound_form.save(commit=False)
            new_obj.tipo = 'INVESTIGACION'
            new_obj = bound_form.save()

            return redirect("/" + self.aux['url_categoria'] + "/" + self.aux['url_seccion'] + "/" + str(new_obj.pk)) #corregir el redirect

        else:
            return render(request, self.template_name, {'form': bound_form, 'aux': self.aux, 'active': 'agregar'})


class LibroInvestigacionDetalle(ObjectUpdateVarMixin, View):
    form_class = LibroInvestigacionForm
    model = LibroInvestigacion
    aux = LibroInvestigacionContext.contexto
    template_name = 'libro_investigacion.html'


class LibroInvestigacionEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(LibroInvestigacion, pk=pk, tipo='INVESTIGACION', usuarios=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class ProyectoInvestigacionJSON(View):
    otros = False
    def get(self, request):

        try:
            usuarioid = User.objects.get(username=request.user.username).id
            if self.otros:
                items = ProyectoInvestigacion.objects.filter(tipo='INVESTIGACION').exclude(usuarios__id__exact=usuarioid)
            else:
                items = ProyectoInvestigacion.objects.filter(usuarios__id__exact=usuarioid, tipo='INVESTIGACION')
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'fecha_inicio', 'status', 'clasificacion', 'modalidad'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ProyectoInvestigacionLista(ObjectCreateVarMixin, View):
    form_class = ProyectoInvestigacionForm
    model = ProyectoInvestigacion
    aux = ProyectoInvestigacionContext.contexto
    template_name = 'proyecto_investigacion.html'

    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            new_obj = bound_form.save(commit=False)
            new_obj.tipo = 'INVESTIGACION'
            new_obj = bound_form.save()
            return redirect("/" + self.aux['url_categoria'] + "/" + self.aux['url_seccion'] + "/" + str(new_obj.pk)) #corregir el redirect
        else:
            return render(request, self.template_name, {'form': bound_form, 'aux': self.aux, 'active': 'agregar'})


class ProyectoInvestigacionDetalle(ObjectUpdateVarMixin, View):
    form_class = ProyectoInvestigacionForm
    model = ProyectoInvestigacion
    aux = ProyectoInvestigacionContext.contexto
    template_name = 'proyecto_investigacion.html'

    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        bound_form = self.form_class(request.POST, instance=obj)
        if bound_form.is_valid():
            det_obj = bound_form.save()
            return redirect("/" + self.aux['url_categoria'] + "/" + self.aux['url_seccion'] + "/" + str(det_obj.pk)) #corregir el redirect
        else:
            return render(request, self.template_name, {'aux': self.aux, 'form': bound_form, 'active': 'detalle'})


class ProyectoInvestigacionEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(ProyectoInvestigacion, pk=pk, tipo='INVESTIGACION', usuarios=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404