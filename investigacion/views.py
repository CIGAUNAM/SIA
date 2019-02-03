from django.shortcuts import render

from django.http.response import (Http404, HttpResponse)
from django.views.generic import View
from django.core import serializers
from SIA.utils import *
from . forms import *
from . utils import *
from django.db.models import Q
from django.contrib import messages

# Create your views here.


class ArticuloCientificoJSON(View):
    otros = False
    def get(self, request):

        try:
            usuarioid = User.objects.get(username=request.user.username).id
            if self.otros:
                articulos = ArticuloCientifico.objects.all().exclude(Q(autores__id__exact=usuarioid) & Q(alumnos__id__exact=usuarioid) & Q(agradecimientos__id__exact=usuarioid)).distinct()
            else:
                articulos = ArticuloCientifico.objects.filter(Q(autores__id__exact=usuarioid) | Q(alumnos__id__exact=usuarioid) | Q(agradecimientos__id__exact=usuarioid)).distinct()
            json = serializers.serialize('json', articulos, use_natural_foreign_keys=True,
                                         fields=('titulo', 'revista', 'status', 'fecha'))

            json = json.replace('PUBLICADO', 'Publicado')
            json = json.replace('ACEPTADO', 'Aceptado')
            json = json.replace('ENVIADO', 'Enviado')
            json = json.replace('ENVIADO', 'Enviado')

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
            item = get_object_or_404(ArticuloCientifico, pk=pk, autores=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class CapituloLibroInvestigacionJSON(View):
    otros = False
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id

            if self.otros:
                items = CapituloLibroInvestigacion.objects.all().exclude(autores__id__exact=usuarioid)
            else:
                items = CapituloLibroInvestigacion.objects.filter(autores__id__exact=usuarioid)

            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('titulo', 'libro', 'pagina_inicio', 'pagina_fin'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class CapituloLibroInvestigacionLista(ObjectCreateVarMixin, View):
    form_class = CapituloLibroInvestigacionForm
    model = CapituloLibroInvestigacion
    aux = CapituloLibroInvestigacionContext.contexto
    template_name = 'capitulo_libro.html'


class CapituloLibroInvestigacionDetalle(ObjectUpdateVarMixin, View):
    form_class = CapituloLibroInvestigacionForm
    model = CapituloLibroInvestigacion
    aux = CapituloLibroInvestigacionContext.contexto
    template_name = 'capitulo_libro.html'


class CapituloLibroInvestigacionEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(CapituloLibroInvestigacion, pk=pk, autores=request.user)
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
                items = MapaArbitrado.objects.all().exclude(autores__id__exact=usuarioid)
            else:
                items = MapaArbitrado.objects.filter(autores__id__exact=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('titulo', 'status', 'editorial', 'fecha'))

            json = json.replace('PUBLICADO', 'Publicado')
            json = json.replace('EN_PRENSA', 'En prensa')
            json = json.replace('ACEPTADO', 'Aceptado')
            json = json.replace('ENVIADO', 'Enviado')
            json = json.replace('ENVIADO', 'Enviado')

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
                items = InformeTecnico.objects.all().exclude(autores__id__exact=usuarioid)
            else:
                items = InformeTecnico.objects.filter(autores__id__exact=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('titulo', 'fecha', 'numero_paginas'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class InformeTecnicoLista(ObjectCreateVarMixin, View):
    form_class = InformeTecnicoForm
    model = InformeTecnico
    aux = InformeTecnicoContext.contexto
    template_name = 'informe_tecnico.html'


class InformeTecnicoDetalle(ObjectUpdateVarMixin, View):
    form_class = InformeTecnicoForm
    model = InformeTecnico
    aux = InformeTecnicoContext.contexto
    template_name = 'informe_tecnico.html'


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
                items = Libro.objects.filter(tipo='INVESTIGACION').exclude(Q(autores__id__exact=usuarioid) & Q(coordinadores__id__exact=usuarioid) & Q(agradecimientos__id__exact=usuarioid)
                                                                           & Q(prologo__id__exact=usuarioid))
            else:
                items = Libro.objects.filter(tipo='INVESTIGACION').filter(Q(autores__id__exact=usuarioid) | Q(coordinadores__id__exact=usuarioid) | Q(agradecimientos__id__exact=usuarioid)
                                                                           | Q(prologo__id__exact=usuarioid))
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'editorial_text', 'ciudad_text', 'status', 'fecha'))

            json = json.replace('PUBLICADO', 'Publicado')
            json = json.replace('EN_PRENSA', 'En prensa')
            json = json.replace('ACEPTADO', 'Aceptado')
            json = json.replace('ENVIADO', 'Enviado')

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
            messages.success(request, "Registro creado con éxito")
            return redirect("/" + self.aux['url_categoria'] + "/" + self.aux['url_seccion'] + "/" + str(new_obj.pk)) #corregir el redirect

        else:
            return render(request, self.template_name, {'form': bound_form, 'aux': self.aux, 'active': 'agregar'})


class LibroInvestigacionDetalle(ObjectUpdateVarMixin, View):
    form_class = LibroInvestigacionForm
    model = LibroInvestigacion
    aux = LibroInvestigacionContext.contexto
    template_name = 'libro_investigacion.html'

    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        return render(request, self.template_name, {'form': self.form_class(instance=obj), 'aux': self.aux, 'active': 'detalle'})

    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        bound_form = self.form_class(request.POST, instance=obj)
        if bound_form.is_valid():
            det_obj = bound_form.save()
            messages.success(request, "Registro actualizado con éxito")
            return redirect("/" + self.aux['url_categoria'] + "/" + self.aux['url_seccion'] + "/" + str(det_obj.pk))  # corregir el redirect
        else:
            return render(request, self.template_name, {'aux': self.aux, 'form': bound_form, 'active': 'detalle'})


class LibroInvestigacionEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(Libro, pk=pk, tipo='INVESTIGACION')
            item.delete()
            return redirect('/investigacion/libros-investigacion/')
        except:
            raise Http404


class ProyectoInvestigacionJSON(View):
    otros = False
    def get(self, request):

        try:
            usuarioid = User.objects.get(username=request.user.username).id
            if self.otros:
                items = ProyectoInvestigacion.objects.all().exclude(Q(responsables__id__exact=usuarioid) & Q(participantes__id__exact=usuarioid) & Q(tecnicos__id__exact=usuarioid)).distinct()
            else:
                items = ProyectoInvestigacion.objects.filter(Q(responsables__id__exact=usuarioid) | Q(participantes__id__exact=usuarioid) | Q(tecnicos__id__exact=usuarioid)).distinct()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'fecha_inicio', 'status', 'clasificacion', 'modalidad'))

            json = json.replace('NUEVO', 'Nuevo')
            json = json.replace('EN_PROCESO', 'En proceso')
            json = json.replace('CONCLUIDO', 'Concluído')
            json = json.replace('OTRO', 'Otro')
            json = json.replace('OTRA', 'Otra')

            json = json.replace('BASICO', 'Básico')
            json = json.replace('APLICADO', 'Aplicado')
            json = json.replace('DESARROLLO_TECNOLOGICO', 'Desarrollo tecnológico')
            json = json.replace('INNOVACION', 'Innovación')
            json = json.replace('INVESTIGACION_FRONTERA', 'Investigación de frontera')
            json = json.replace('OTRO', 'Otro')

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
            item = get_object_or_404(ProyectoInvestigacion, pk=pk)
            item.delete()
            return redirect('../')
        except:
            raise Http404