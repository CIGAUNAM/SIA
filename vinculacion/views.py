from django.http.response import (Http404, HttpResponse)
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
    template_name = 'main.html'


class ArbitrajePublicacionAcademicaDetalle(ObjectUpdateMixin, View):
    form_class = ArbitrajePublicacionAcademicaForm
    model = ArbitrajePublicacionAcademica
    aux = ArbitrajePublicacionAcademicaContext.contexto
    template_name = 'main.html'



class ArbitrajeProyectoInvestigacionJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = ArbitrajeProyectoInvestigacion.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('proyecto', 'fecha',))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ArbitrajeProyectoInvestigacionLista(ObjectCreateMixin, View):
    form_class = ArbitrajeProyectoInvestigacionForm
    model = ArbitrajeProyectoInvestigacion
    aux = ArbitrajeProyectoInvestigacionContext.contexto
    template_name = 'main.html'


class ArbitrajeProyectoInvestigacionDetalle(ObjectUpdateMixin, View):
    form_class = ArbitrajeProyectoInvestigacionForm
    model = ArbitrajeProyectoInvestigacion
    aux = ArbitrajeProyectoInvestigacionContext.contexto
    template_name = 'main.html'



class ArbitrajeOtraActividadJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = ArbitrajeOtraActividad.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('actividad', 'dependencia', 'fecha'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ArbitrajeOtraActividadLista(ObjectCreateMixin, View):
    form_class = ArbitrajeOtraActividadForm
    model = ArbitrajeOtraActividad
    aux = ArbitrajeOtraActividadContext.contexto
    template_name = 'main.html'


class ArbitrajeOtraActividadDetalle(ObjectUpdateMixin, View):
    form_class = ArbitrajeOtraActividadForm
    model = ArbitrajeOtraActividad
    aux = ArbitrajeOtraActividadContext.contexto
    template_name = 'main.html'



class RedAcademicaJSON(View):
    otros = False
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            if self.otros:
                items = RedAcademica.objects.all().exclude(usuarios__id__exact=usuarioid)
            else:
                items = RedAcademica.objects.filter(usuarios__id__exact=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'clasificacion', 'fecha_constitucion', 'vigente'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class RedAcademicaLista(ObjectCreateVarMixin, View):
    form_class = RedAcademicaForm
    model = RedAcademica
    aux = RedAcademicaContext.contexto
    template_name = 'main.html'


class RedAcademicaDetalle(ObjectUpdateVarMixin, View):
    form_class = RedAcademicaForm
    model = RedAcademica
    aux = RedAcademicaContext.contexto
    template_name = 'main.html'



class ConvenioEntidadNoAcademicaJSON(View):
    otros = False
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            if self.otros:
                items = ConvenioEntidadNoAcademica.objects.all().exclude(usuarios__id__exact=usuarioid)
            else:
                items = ConvenioEntidadNoAcademica.objects.filter(usuarios__id__exact=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'es_agradecimiento', 'clasificacion_entidad', 'fecha_inicio', 'fecha_fin'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ConvenioEntidadNoAcademicaLista(ObjectCreateVarMixin, View):
    form_class = ConvenioEntidadNoAcademicaForm
    model = ConvenioEntidadNoAcademica
    aux = ConvenioEntidadNoAcademicaContext.contexto
    template_name = 'main.html'


class ConvenioEntidadNoAcademicaDetalle(ObjectUpdateVarMixin, View):
    form_class = ConvenioEntidadNoAcademicaForm
    model = ConvenioEntidadNoAcademica
    aux = ConvenioEntidadNoAcademicaContext.contexto
    template_name = 'main.html'



class ServicioExternoEntidadNoAcademicaJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = ServicioExternoEntidadNoAcademica.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre_servicio', 'clasificacion_servicio', 'dependencia', 'fecha_inicio', 'fecha_fin'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ServicioExternoEntidadNoAcademicaLista(ObjectCreateMixin, View):
    form_class = ServicioExternoEntidadNoAcademicaForm
    model = ServicioExternoEntidadNoAcademica
    aux = ServicioExternoEntidadNoAcademicaContext.contexto
    template_name = 'main.html'


class ServicioExternoEntidadNoAcademicaDetalle(ObjectUpdateMixin, View):
    form_class = ServicioExternoEntidadNoAcademicaForm
    model = ServicioExternoEntidadNoAcademica
    aux = ServicioExternoEntidadNoAcademicaContext.contexto
    template_name = 'main.html'



class OtroProgramaVinculacionJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = OtroProgramaVinculacion.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre_servicio', 'fecha', 'tipo'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class OtroProgramaVinculacionLista(ObjectCreateMixin, View):
    form_class = OtroProgramaVinculacionForm
    model = OtroProgramaVinculacion
    aux = OtroProgramaVinculacionContext.contexto
    template_name = 'main.html'


class OtroProgramaVinculacionDetalle(ObjectUpdateMixin, View):
    form_class = OtroProgramaVinculacionForm
    model = OtroProgramaVinculacion
    aux = OtroProgramaVinculacionContext.contexto
    template_name = 'main.html'