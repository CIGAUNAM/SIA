from django.http.response import (Http404, HttpResponse)
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.core import serializers
from SIA.utils import *
from . forms import *
from . utils import *
from . models import *

# Create your views here.


class ArbitrajePublicacionAcademicaJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = ArbitrajePublicacionAcademica.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('fecha_dictamen', 'tipo', 'revista', 'libro', 'capitulo_libro', 'institucion'))

            json = json.replace('CAPITULO_LIBRO', 'Capítulo de libro')
            json = json.replace('ARTICULO', 'Artículo en revista')
            json = json.replace('LIBRO', 'Libro')


            json = json.replace(' "revista": null,', '')
            json = json.replace('"revista": null,', '')

            json = json.replace(' "libro": "",', '')
            json = json.replace(' "capitulo_libro": "",', '')

            json = json.replace('"revista"', '"publicacion"')
            json = json.replace('"capitulo_libro"', '"publicacion"')
            json = json.replace('"libro"', '"publicacion"')

            json = json.replace(',   }', '}')
            json = json.replace(',  }', '}')
            json = json.replace(', }', '}')
            json = json.replace(',}', '}')

            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ArbitrajePublicacionAcademicaLista(ObjectCreateMixin, View):
    form_class = ArbitrajePublicacionAcademicaForm
    model = ArbitrajePublicacionAcademica
    aux = ArbitrajePublicacionAcademicaContext.contexto
    template_name = 'arbitraje_publicacion_academica.html'


class ArbitrajePublicacionAcademicaDetalle(ObjectUpdateMixin, View):
    form_class = ArbitrajePublicacionAcademicaForm
    model = ArbitrajePublicacionAcademica
    aux = ArbitrajePublicacionAcademicaContext.contexto
    template_name = 'arbitraje_publicacion_academica.html'


class ArbitrajePublicacionAcademicaEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(ArbitrajePublicacionAcademica, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class OtraComisionArbitrajeJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = OtraComisionArbitraje.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('comision', 'dependencia', 'fecha'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class OtraComisionArbitrajeLista(ObjectCreateMixin, View):
    form_class = OtraComisionArbitrajeForm
    model = OtraComisionArbitraje
    aux = OtraComisionContext.contexto
    template_name = 'otra_comision.html'


class OtraComisionArbitrajeDetalle(ObjectUpdateMixin, View):
    form_class = OtraComisionArbitrajeForm
    model = OtraComisionArbitraje
    aux = OtraComisionContext.contexto
    template_name = 'otra_comision.html'


class OtraComisionArbitrajeEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(OtraComisionArbitraje, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class RedAcademicaJSON(View):
    otros = False
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            if self.otros:
                items = RedAcademica.objects.all().exclude(participantes__id__exact=usuarioid)
            else:
                items = RedAcademica.objects.filter(participantes__id__exact=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'ambito', 'fecha_constitucion'))

            json = json.replace('LOCAL', 'Local')
            json = json.replace('REGIONAL', 'Regional')
            json = json.replace('NACIONAL', 'Nacional')
            json = json.replace('INTERNACIONAL', 'Internacional')
            json = json.replace('OTRO', 'Otro')
            json = json.replace('false', '"No"')
            json = json.replace('true', '"Si"')

            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class RedAcademicaLista(ObjectCreateVarMixin, View):
    form_class = RedAcademicaForm
    model = RedAcademica
    aux = RedAcademicaContext.contexto
    template_name = 'red_academica.html'


class RedAcademicaDetalle(ObjectUpdateVarMixin, View):
    form_class = RedAcademicaForm
    model = RedAcademica
    aux = RedAcademicaContext.contexto
    template_name = 'red_academica.html'


class RedAcademicaEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(RedAcademica, pk=pk, usuarios=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class ConvenioOtraEntidadJSON(View):
    otros = False
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            if self.otros:
                items = ConvenioOtraEntidad.objects.all().exclude(participantes__id__exact=usuarioid)
            else:
                items = ConvenioOtraEntidad.objects.filter(participantes__id__exact=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'fecha_inicio', 'fecha_fin'))

            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ConvenioOtraEntidadLista(ObjectCreateVarMixin, View):
    form_class = ConvenioOtraEntidadForm
    model = ConvenioOtraEntidad
    aux = ConvenioOtraEntidadContext.contexto
    template_name = 'convenio_otra_entidad.html'


class ConvenioOtraEntidadDetalle(ObjectUpdateVarMixin, View):
    form_class = ConvenioOtraEntidadForm
    model = ConvenioOtraEntidad
    aux = ConvenioOtraEntidadContext.contexto
    template_name = 'convenio_otra_entidad.html'


class ConvenioOtraEntidadEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(ConvenioOtraEntidad, pk=pk, usuarios=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class ServicioAsesoriaExternaJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = ServicioAsesoriaExterna.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre_servicio', 'clasificacion_servicio', 'fecha_inicio', 'fecha_fin'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ServicioAsesoriaExternaLista(ObjectCreateMixin, View):
    form_class = ServicioAsesoriaExternaForm
    model = ServicioAsesoriaExterna
    aux = ServicioAsesoriaExternaContext.contexto
    template_name = 'servicio_externo.html'


class ServicioAsesoriaExternaDetalle(ObjectUpdateMixin, View):
    form_class = ServicioAsesoriaExternaForm
    model = ServicioAsesoriaExterna
    aux = ServicioAsesoriaExternaContext.contexto
    template_name = 'servicio_externo.html'


class ServicioAsesoriaExternaEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(ServicioAsesoriaExterna, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404