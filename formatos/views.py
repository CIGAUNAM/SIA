from django.shortcuts import render

from django.http.response import (Http404, HttpResponse)
from django.views.generic import View, DeleteView
from django.core.urlresolvers import reverse_lazy

from django.core import serializers
from SIA.utils import *
from .forms import *
from .utils import *

from formatos.forms import *

# Create your views here.


class FormatoServicioTransporteJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = FormatoServicioTransporte.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items,
                                         fields=('fecha_inicio', 'ciudad'),
                                         use_natural_foreign_keys=True)
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class FormatoServicioTransporteLista(ObjectCreateMixin, View):
    form_class = FormatoServicioTransporteForm
    model = FormatoServicioTransporte
    aux = FormatoServicioTransporteContext.contexto
    template_name = 'servicio_transporte.html'


class FormatoServicioTransporteDetalle(ObjectUpdateMixin, View):
    form_class = FormatoServicioTransporteForm
    model = FormatoServicioTransporte
    aux = FormatoServicioTransporteContext.contexto
    template_name = 'servicio_transporte.html'


class FormatoServicioTransporteEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(FormatoServicioTransporte, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404



class FormatoLicenciaGoceSueldoJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = FormatoLicenciaGoceSueldo.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items,
                                         fields=('fecha_inicio', 'ciudad'),
                                         use_natural_foreign_keys=True)
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class FormatoLicenciaGoceSueldoLista(ObjectCreateMixin, View):
    form_class = FormatoLicenciaGoceSueldoForm
    model = FormatoLicenciaGoceSueldo
    aux = FormatoLicenciaGoceSueldoContext.contexto
    template_name = 'main.html'


class FormatoLicenciaGoceSueldoDetalle(ObjectUpdateMixin, View):
    form_class = FormatoLicenciaGoceSueldoForm
    model = FormatoLicenciaGoceSueldo
    aux = FormatoLicenciaGoceSueldoContext.contexto
    template_name = 'main.html'


class FormatoLicenciaGoceSueldoEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(FormatoLicenciaGoceSueldo, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404



class FormatoPagoViaticoJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = FormatoPagoViatico.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items,
                                         fields=('evento', 'fecha_salida'),
                                         use_natural_foreign_keys=True)
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class FormatoPagoViaticoLista(ObjectCreateMixin, View):
    form_class = FormatoPagoViaticoForm
    model = FormatoPagoViatico
    aux = FormatoPagoViaticoContext.contexto
    template_name = 'pago_viaticos.html'


class FormatoPagoViaticoDetalle(ObjectUpdateMixin, View):
    form_class = FormatoPagoViaticoForm
    model = FormatoPagoViatico
    aux = FormatoPagoViaticoContext.contexto
    template_name = 'pago_viaticos.html'


class FormatoPagoViaticoEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(FormatoLicenciaGoceSueldo, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404