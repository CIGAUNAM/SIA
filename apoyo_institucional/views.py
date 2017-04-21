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
                                         fields=('cargo', 'dependencia', 'cargo_inicio', 'cargo_fin'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class CargoAcademicoAdministrativoLista(ObjectCreateMixin, View):
    form_class = CargoAcademicoAdministrativoForm
    model = CargoAcademicoAdministrativo
    aux = CargoAcademicoAdministrativoContext.contexto
    template_name = 'main.html'


class CargoAcademicoAdministrativoDetalle(ObjectUpdateMixin, View):
    form_class = CargoAcademicoAdministrativoForm
    model = CargoAcademicoAdministrativo
    aux = CargoAcademicoAdministrativoContext.contexto
    template_name = 'main.html'


class RepresentacionOrganoColegiadoJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = RepresentacionOrganoColegiado.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('representacion', 'ante', 'cargo_inicio', 'cargo_fin'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class RepresentacionOrganoColegiadoLista(ObjectCreateMixin, View):
    form_class = RepresentacionOrganoColegiadoForm
    model = RepresentacionOrganoColegiado
    aux = RepresentacionOrganoColegiadoContext.contexto
    template_name = 'main.html'


class RepresentacionOrganoColegiadoDetalle(ObjectUpdateMixin, View):
    form_class = RepresentacionOrganoColegiadoForm
    model = RepresentacionOrganoColegiado
    aux = RepresentacionOrganoColegiadoContext.contexto
    template_name = 'main.html'


class ComisionAcademicaJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = ComisionAcademica.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('comision_academica', 'fecha_inicio', 'fecha_fin'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ComisionAcademicaLista(ObjectCreateMixin, View):
    form_class = ComisionAcademicaForm
    model = ComisionAcademica
    aux = ComisionAcademicaContext.contexto
    template_name = 'main.html'


class ComisionAcademicaDetalle(ObjectUpdateMixin, View):
    form_class = ComisionAcademicaForm
    model = ComisionAcademica
    aux = ComisionAcademicaContext.contexto
    template_name = 'main.html'


class ApoyoTecnicoJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = ApoyoTecnico.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('apoyo_tecnico', 'dependencia', 'apoyo_inicio', 'apoyo_fin'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ApoyoTecnicoLista(ObjectCreateMixin, View):
    form_class = ApoyoTecnicoForm
    model = ApoyoTecnico
    aux = ApoyoTecnicoContext.contexto
    template_name = 'main.html'


class ApoyoTecnicoDetalle(ObjectUpdateMixin, View):
    form_class = ApoyoTecnicoForm
    model = ApoyoTecnico
    aux = ApoyoTecnicoContext.contexto
    template_name = 'main.html'


class ApoyoOtraActividadJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = ApoyoOtraActividad.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('apoyo_actividad', 'dependencia', 'apoyo_inicio', 'apoyo_fin'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ApoyoOtraActividadLista(ObjectCreateMixin, View):
    form_class = ApoyoOtraActividadForm
    model = ApoyoOtraActividad
    aux = ApoyoOtraActividadContext.contexto
    template_name = 'main.html'


class ApoyoOtraActividadDetalle(ObjectUpdateMixin, View):
    form_class = ApoyoOtraActividadForm
    model = ApoyoOtraActividad
    aux = ApoyoOtraActividadContext.contexto
    template_name = 'main.html'


