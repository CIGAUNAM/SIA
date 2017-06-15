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
                                         fields=('cargo', 'dependencia', 'fecha_inicio', 'fecha_fin'))
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
                                         fields=('representacion', 'dependencia', 'fecha_inicio', 'fecha_fin'))
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
                                         fields=('comision_academica', 'fecha_inicio', 'fecha_fin'))
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
                                         fields=('actividad_apoyo', 'dependencia', 'fecha_inicio', 'fecha_fin'))
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
                                         fields=('actividad_apoyo', 'dependencia', 'fecha_inicio', 'fecha_fin'))
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


class RepresentacionJSON(View):
    def get(self, request):
        try:
            #usuarioid = User.objects.get(username=request.user.username).id
            items = Representacion.objects.all()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre',))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class RepresentacionLista(ObjectCreateMixinNucleo, View):
    form_class = RepresentacionForm
    model = Representacion
    aux = RepresentacionContext.contexto
    template_name = 'main.html'


class RepresentacionDetalle(ObjectUpdateMixinNucleo, View):
    form_class = RepresentacionForm
    model = Representacion
    aux = RepresentacionContext.contexto
    template_name = 'main.html'


class RepresentacionEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(Representacion, pk=pk)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class ComisionJSON(View):
    def get(self, request):
        try:
            #usuarioid = User.objects.get(username=request.user.username).id
            items = Comision.objects.all()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre',))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ComisionLista(ObjectCreateMixinNucleo, View):
    form_class = ComisionForm
    model = Comision
    aux = ComisionContext.contexto
    template_name = 'main.html'


class ComisionDetalle(ObjectUpdateMixinNucleo, View):
    form_class = ComisionForm
    model = Comision
    aux = ComisionContext.contexto
    template_name = 'main.html'


class ComisionEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(Comision, pk=pk)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class ActividadApoyoJSON(View):
    def get(self, request):
        try:
            #usuarioid = User.objects.get(username=request.user.username).id
            items = ActividadApoyo.objects.all()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre',))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ActividadApoyoLista(ObjectCreateMixinNucleo, View):
    form_class = ActividadApoyoForm
    model = ActividadApoyo
    aux = ActividadApoyoContext.contexto
    template_name = 'main.html'


class ActividadApoyoDetalle(ObjectUpdateMixinNucleo, View):
    form_class = ActividadApoyoForm
    model = ActividadApoyo
    aux = ActividadApoyoContext.contexto
    template_name = 'main.html'


class ActividadApoyoEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(ActividadApoyo, pk=pk)
            item.delete()
            return redirect('../')
        except:
            raise Http404