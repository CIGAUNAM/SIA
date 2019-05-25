from django.views.generic import View
from django.core import serializers
from SIA.utils import *
from . forms import *
from . utils import *
from . models import *

# Create your views here.


class LaborDirectivaCoordinacionJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = LaborDirectivaCoordinacion.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('tipo_cargo', 'institucion', 'fecha_inicio', 'fecha_fin'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class LaborDirectivaCoordinacionLista(ObjectCreateMixin, View):
    form_class = LaborDirectivaCoordinacionForm
    model = LaborDirectivaCoordinacion
    aux = LaborDirectivaCoordinacionContext.contexto
    template_name = 'labor_directiva_coordinacion.html'


class LaborDirectivaCoordinacionDetalle(ObjectUpdateMixin, View):
    form_class = LaborDirectivaCoordinacionForm
    model = LaborDirectivaCoordinacion
    aux = LaborDirectivaCoordinacionContext.contexto
    template_name = 'labor_directiva_coordinacion.html'


class LaborDirectivaCoordinacionEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(LaborDirectivaCoordinacion, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class RepresentacionOrganoColegiadoUNAMJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = RepresentacionOrganoColegiadoUNAM.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('tipo_representacion', 'representacion_dentro_unam', 'representacion_dentro_unam_otra',
                                                 'representacion_fuera_unam', 'institucion_dentro_unam', 'institucion_fuera_unam'          
                                                 'representacion_unam', 'fecha_inicio', 'fecha_fin'))

            json = json.replace('DENTRO', 'Dentro de la UNAM')
            json = json.replace('REPRESENTACION', 'Con representacion UNAM (Solo por designación)')

            json = json.replace(' "institucion_dentro_unam": null,', '')
            json = json.replace(' "institucion_fuera_unam": null,', '')
            json = json.replace(' "representacion_dentro_unam": "",', '')
            json = json.replace(' "representacion_dentro_unam_otra": "",', '')
            json = json.replace(' "representacion_fuera_unam": "",', '')

            json = json.replace('"institucion_dentro_unam"', '"institucion"')
            json = json.replace('"institucion_fuera_unam"', '"institucion"')
            json = json.replace('"representacion_dentro_unam"', '"representacion"')
            json = json.replace('"representacion_fuera_unam"', '"representacion"')
            json = json.replace('"representacion_dentro_unam_otra"', '"representacion"')

            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class RepresentacionOrganoColegiadoUNAMLista(ObjectCreateMixin, View):
    form_class = RepresentacionOrganoColegiadoUNAMForm
    model = RepresentacionOrganoColegiadoUNAM
    aux = RepresentacionOrganoColegiadoUNAMContext.contexto
    template_name = 'representacion_organo_colegiado.html'


class RepresentacionOrganoColegiadoUNAMDetalle(ObjectUpdateMixin, View):
    form_class = RepresentacionOrganoColegiadoUNAMForm
    model = RepresentacionOrganoColegiadoUNAM
    aux = RepresentacionOrganoColegiadoUNAMContext.contexto
    template_name = 'representacion_organo_colegiado.html'


class RepresentacionOrganoColegiadoEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(RepresentacionOrganoColegiadoUNAM, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class ComisionAcademicaJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = ComisionInstitucionalCIGA.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('comision_academica', 'institucion', 'fecha_inicio', 'fecha_fin'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ComisionAcademicaLista(ObjectCreateMixin, View):
    form_class = ComisionInstitucionalCIGAForm
    model = ComisionInstitucionalCIGA
    aux = ComisionAcademicaContext.contexto
    template_name = 'comision_institucional_ciga.html'


class ComisionAcademicaDetalle(ObjectUpdateMixin, View):
    form_class = ComisionInstitucionalCIGAForm
    model = ComisionInstitucionalCIGA
    aux = ComisionAcademicaContext.contexto
    template_name = 'comision_institucional_ciga.html'


class ComisionAcademicaEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(ComisionInstitucionalCIGA, pk=pk, usuario=request.user)
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
            items = ComisionInstitucional.objects.all()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre',))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ComisionLista(ObjectCreateMixinNucleo, View):
    form_class = ComisionForm
    model = ComisionInstitucional
    aux = ComisionContext.contexto
    template_name = 'main.html'


class ComisionDetalle(ObjectUpdateMixinNucleo, View):
    form_class = ComisionForm
    model = ComisionInstitucional
    aux = ComisionContext.contexto
    template_name = 'main.html'


class ComisionEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(ComisionInstitucional, pk=pk)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class ActividadApoyoJSON(View):
    def get(self, request):
        try:
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