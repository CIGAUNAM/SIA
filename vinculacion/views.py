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
                                         fields=('tipo', 'revista', 'libro', 'capitulo_libro', 'fecha_dictamen'))
            json = json.replace('REVISTA', 'Revista')
            json = json.replace('CAPITULO_LIBRO', 'Capítulo de libro')
            json = json.replace('LIBRO', 'Libro')

            json = json.replace('"revista": null,', '')
            json = json.replace('"libro": null,', '')
            json = json.replace('"capitulo_libro": null,', '')

            json = json.replace('"revista"', '"publicacion"')
            json = json.replace('"libro"', '"publicacion"')
            json = json.replace('"capitulo_libro"', '"publicacion"')

            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ArbitrajePublicacionAcademicaLista(ObjectCreateMixin, View):
    form_class = ArbitrajePublicacionAcademicaForm
    model = ArbitrajePublicacionAcademica
    aux = ArbitrajePublicacionAcademicaContext.contexto
    template_name = 'arbitraje_publicacion.html'


class ArbitrajePublicacionAcademicaDetalle(ObjectUpdateMixin, View):
    form_class = ArbitrajePublicacionAcademicaForm
    model = ArbitrajePublicacionAcademica
    aux = ArbitrajePublicacionAcademicaContext.contexto
    template_name = 'arbitraje_publicacion.html'


class ArbitrajePublicacionAcademicaEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(ArbitrajePublicacionAcademica, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


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
    template_name = 'arbitraje_proyecto_investigacion.html'


class ArbitrajeProyectoInvestigacionDetalle(ObjectUpdateMixin, View):
    form_class = ArbitrajeProyectoInvestigacionForm
    model = ArbitrajeProyectoInvestigacion
    aux = ArbitrajeProyectoInvestigacionContext.contexto
    template_name = 'arbitraje_proyecto_investigacion.html'


class ArbitrajeProyectoInvestigacionEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(ArbitrajeProyectoInvestigacion, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


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
    template_name = 'arbitraje_otra_actividad.html'


class ArbitrajeOtraActividadDetalle(ObjectUpdateMixin, View):
    form_class = ArbitrajeOtraActividadForm
    model = ArbitrajeOtraActividad
    aux = ArbitrajeOtraActividadContext.contexto
    template_name = 'arbitraje_otra_actividad.html'


class ArbitrajeOtraActividadEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(ArbitrajeOtraActividad, pk=pk, usuario=request.user)
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
    template_name = 'convenio.html'


class ConvenioEntidadNoAcademicaDetalle(ObjectUpdateVarMixin, View):
    form_class = ConvenioEntidadNoAcademicaForm
    model = ConvenioEntidadNoAcademica
    aux = ConvenioEntidadNoAcademicaContext.contexto
    template_name = 'convenio.html'


class ConvenioEntidadNoAcademicaEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(ConvenioEntidadNoAcademica, pk=pk, usuarios=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


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
    template_name = 'servicio_externo.html'


class ServicioExternoEntidadNoAcademicaDetalle(ObjectUpdateMixin, View):
    form_class = ServicioExternoEntidadNoAcademicaForm
    model = ServicioExternoEntidadNoAcademica
    aux = ServicioExternoEntidadNoAcademicaContext.contexto
    template_name = 'servicio_externo.html'


class ServicioExternoEntidadNoAcademicaEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(ServicioExternoEntidadNoAcademica, pk=pk, usuario=request.user)
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