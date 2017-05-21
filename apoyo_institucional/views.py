from django.http.response import (Http404, HttpResponse)
from django.views.generic import View
from django.core import serializers
from SIA.utils import *
from . forms import *
from . utils import *
from . models import *

# Create your views here.


class CargoAcademicoAdministrativoJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = CargoAcademicoAdministrativo.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'dependencia', 'cargo_inicio', 'cargo_fin'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class CargoAcademicoAdministrativoLista(ObjectCreateMixin, View):
    form_class = CargoAcademicoAdministrativoForm
    model = CargoAcademicoAdministrativo
    aux = CargoAcademicoAdministrativoContext.contexto
    template_name = 'cargo_academico-administrativo.html'


class CargoAcademicoAdministrativoDetalle(ObjectUpdateMixin, View):
    form_class = CargoAcademicoAdministrativoForm
    model = CargoAcademicoAdministrativo
    aux = CargoAcademicoAdministrativoContext.contexto
    template_name = 'cargo_academico-administrativo.html'


class CargoAcademicoAdministrativoEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(CargoAcademicoAdministrativo, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class RepresentacionOrganoColegiadoJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = RepresentacionOrganoColegiado.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'ante', 'cargo_inicio', 'cargo_fin'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class RepresentacionOrganoColegiadoLista(ObjectCreateMixin, View):
    form_class = RepresentacionOrganoColegiadoForm
    model = RepresentacionOrganoColegiado
    aux = RepresentacionOrganoColegiadoContext.contexto
    template_name = 'representacion_organo_colegiado.html'


class RepresentacionOrganoColegiadoDetalle(ObjectUpdateMixin, View):
    form_class = RepresentacionOrganoColegiadoForm
    model = RepresentacionOrganoColegiado
    aux = RepresentacionOrganoColegiadoContext.contexto
    template_name = 'representacion_organo_colegiado.html'


class RepresentacionOrganoColegiadoEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(RepresentacionOrganoColegiado, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class ComisionAcademicaJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = ComisionAcademica.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'fecha_inicio', 'fecha_fin'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ComisionAcademicaLista(ObjectCreateMixin, View):
    form_class = ComisionAcademicaForm
    model = ComisionAcademica
    aux = ComisionAcademicaContext.contexto
    template_name = 'comision_academica.html'


class ComisionAcademicaDetalle(ObjectUpdateMixin, View):
    form_class = ComisionAcademicaForm
    model = ComisionAcademica
    aux = ComisionAcademicaContext.contexto
    template_name = 'comision_academica.html'


class ComisionAcademicaEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(ComisionAcademica, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class ApoyoTecnicoJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = ApoyoTecnico.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'dependencia', 'apoyo_inicio', 'apoyo_fin'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ApoyoTecnicoLista(ObjectCreateMixin, View):
    form_class = ApoyoTecnicoForm
    model = ApoyoTecnico
    aux = ApoyoTecnicoContext.contexto
    template_name = 'apoyo_tecnico.html'


class ApoyoTecnicoDetalle(ObjectUpdateMixin, View):
    form_class = ApoyoTecnicoForm
    model = ApoyoTecnico
    aux = ApoyoTecnicoContext.contexto
    template_name = 'apoyo_tecnico.html'


class ApoyoTecnicoEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(ApoyoTecnico, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class ApoyoOtraActividadJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = ApoyoOtraActividad.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'dependencia', 'apoyo_inicio', 'apoyo_fin'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ApoyoOtraActividadLista(ObjectCreateMixin, View):
    form_class = ApoyoOtraActividadForm
    model = ApoyoOtraActividad
    aux = ApoyoOtraActividadContext.contexto
    template_name = 'apoyo_otra_actividad.html'


class ApoyoOtraActividadDetalle(ObjectUpdateMixin, View):
    form_class = ApoyoOtraActividadForm
    model = ApoyoOtraActividad
    aux = ApoyoOtraActividadContext.contexto
    template_name = 'apoyo_otra_actividad.html'


class ApoyoOtraActividadEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(ApoyoOtraActividad, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


