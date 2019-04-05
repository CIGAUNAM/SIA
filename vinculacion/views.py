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
                                         fields=('fecha_dictamen'))

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


class OtraComisionJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = OtraComision.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('comision', 'dependencia', 'fecha'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class OtraComisionLista(ObjectCreateMixin, View):
    form_class = OtraComisionForm
    model = OtraComision
    aux = OtraComisionContext.contexto
    template_name = 'otra_comision.html'


class OtraComisionDetalle(ObjectUpdateMixin, View):
    form_class = OtraComisionForm
    model = OtraComision
    aux = OtraComisionContext.contexto
    template_name = 'otra_comision.html'


class OtraComisionEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(OtraComision, pk=pk, usuario=request.user)
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


class ConvenioEntidadExternaJSON(View):
    otros = False
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            if self.otros:
                items = ConvenioEntidadExterna.objects.all().exclude(participantes__id__exact=usuarioid)
            else:
                items = ConvenioEntidadExterna.objects.filter(participantes__id__exact=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'fecha_inicio', 'fecha_fin'))

            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ConvenioEntidadExternaLista(ObjectCreateVarMixin, View):
    form_class = ConvenioEntidadExternaForm
    model = ConvenioEntidadExterna
    aux = ConvenioEntidadExternaContext.contexto
    template_name = 'convenio_entidad_externa.html'


class ConvenioEntidadExternaDetalle(ObjectUpdateVarMixin, View):
    form_class = ConvenioEntidadExternaForm
    model = ConvenioEntidadExterna
    aux = ConvenioEntidadExternaContext.contexto
    template_name = 'convenio_entidad_externa.html'


class ConvenioEntidadExternaEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(ConvenioEntidadExterna, pk=pk, usuarios=request.user)
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
    aux = ServicioExternoEntidadNoAcademicaContext.contexto
    template_name = 'servicio_externo.html'


class ServicioAsesoriaExternaDetalle(ObjectUpdateMixin, View):
    form_class = ServicioAsesoriaExternaForm
    model = ServicioAsesoriaExterna
    aux = ServicioExternoEntidadNoAcademicaContext.contexto
    template_name = 'servicio_externo.html'


class ServicioAsesoriaExternaEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(ServicioAsesoriaExterna, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class OtroProgramaVinculacionJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = OtroProgramaVinculacion.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'fecha', 'tipo'))

            json = json.replace('VINCULACION', 'Vinculación')
            json = json.replace('COLABORACION', 'Colaboración')
            json = json.replace('COOPERACION', 'Cooperación')
            json = json.replace('OTRO', 'Otro')

            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class OtroProgramaVinculacionLista(ObjectCreateMixin, View):
    form_class = OtroProgramaVinculacionForm
    model = OtroProgramaVinculacion
    aux = OtroProgramaVinculacionContext.contexto
    template_name = 'otro_programa_vinculacion.html'


class OtroProgramaVinculacionDetalle(ObjectUpdateMixin, View):
    form_class = OtroProgramaVinculacionForm
    model = OtroProgramaVinculacion
    aux = OtroProgramaVinculacionContext.contexto
    template_name = 'otro_programa_vinculacion.html'


class OtroProgramaVinculacionEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(OtroProgramaVinculacion, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class ClasificacionServicioJSON(View):
    def get(self, request):
        try:
            #usuarioid = User.objects.get(username=request.user.username).id
            items = ClasificacionServicio.objects.all()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ClasificacionServicioLista(ObjectCreateMixinNucleo, View):
    form_class = ClasificacionServicioForm
    model = ClasificacionServicio
    aux = ClasificacionServicioContext.contexto
    template_name = 'main.html'


class ClasificacionServicioDetalle(ObjectUpdateMixinNucleo, View):
    form_class = ClasificacionServicioForm
    model = ClasificacionServicio
    aux = ClasificacionServicioContext.contexto
    template_name = 'main.html'


class ClasificacionServicioEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(ClasificacionServicio, pk=pk)
            item.delete()
            return redirect('../')
        except:
            raise Http404