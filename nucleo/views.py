
from rest_framework import generics
from . permissions import UserListReadOnly, IsAdminUserOrReadOnly
from rest_framework import permissions
from django.core import serializers
from django.views.generic import View
import uuid

from SIA.utils import *
from . forms import *
from . utils import *
from . models import *
from . serializers import *

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

def inicio(request):
    return render(request=request, context=None, template_name='dashboard.html')






























class PaisJSON(View):
    def get(self, request):
        try:
            #usuarioid = User.objects.get(username=request.user.username).id
            items = Pais.objects.all()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'zona', 'codigo'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class PaisLista(ObjectCreateMixinNucleo, View):
    form_class = PaisForm
    model = Pais
    aux = PaisContext.contexto
    template_name = 'pais.html'


class PaisDetalle(ObjectUpdateMixinNucleo, View):
    form_class = PaisForm
    model = Pais
    aux = PaisContext.contexto
    template_name = 'pais.html'


class PaisEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(Pais, pk=pk)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class EstadoJSON(View):
    def get(self, request):
        try:
            #usuarioid = User.objects.get(username=request.user.username).id
            items = Estado.objects.all()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'pais'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class EstadoLista(ObjectCreateMixinNucleo, View):
    form_class = EstadoForm
    model = Estado
    aux = EstadoContext.contexto
    template_name = 'estado.html'


class EstadoDetalle(ObjectUpdateMixinNucleo, View):
    form_class = EstadoForm
    model = Estado
    aux = EstadoContext.contexto
    template_name = 'estado.html'


class EstadoEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(Estado, pk=pk)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class CiudadJSON(View):
    def get(self, request):
        try:
            #usuarioid = User.objects.get(username=request.user.username).id
            items = Ciudad.objects.all()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'estado'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class CiudadLista(ObjectCreateMixinNucleo, View):
    form_class = CiudadForm
    model = Ciudad
    aux = CiudadContext.contexto
    template_name = 'ciudad.html'


class CiudadDetalle(ObjectUpdateMixinNucleo, View):
    form_class = CiudadForm
    model = Ciudad
    aux = CiudadContext.contexto
    template_name = 'ciudad.html'


class CiudadEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(Ciudad, pk=pk)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class InstitucionJSON(View):
    def get(self, request):
        try:
            #usuarioid = User.objects.get(username=request.user.username).id
            items = Institucion.objects.all().exclude(nombre='Universidad Nacional Autónoma de México (UNAM)')
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'pais'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class InstitucionLista(ObjectCreateMixinNucleo, View):
    form_class = InstitucionForm
    model = Institucion
    aux = InstitucionContext.contexto
    template_name = 'institucion.html'


class InstitucionDetalle1(ObjectUpdateMixinNucleo, View):
    form_class = InstitucionForm
    model = Institucion
    aux = InstitucionContext.contexto
    template_name = 'institucion.html'


class InstitucionEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(Institucion, pk=pk)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class InstitucionAgregar(ObjectModalCreateMixin, View):
    form_class = InstitucionForm
    model = Institucion
    template_name = 'modal/form_agregar_institucion.html'


class InstitucionDetalle(ObjectModalUpdateMixin, View):
    form_class = InstitucionForm
    model = Institucion
    template_name = 'modal/form_detalle_institucion.html'


class DependenciaJSON(View):
    def get(self, request):
        try:
            #usuarioid = User.objects.get(username=request.user.username).id
            items = Dependencia.objects.all()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre_dependencia', 'institucion_dependencia'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class DependenciaLista(ObjectCreateMixinNucleo, View):
    form_class = DependenciaForm
    model = Dependencia
    aux = DependenciaContext.contexto
    template_name = 'dependencia.html'


class DependenciaDetalle1(ObjectUpdateMixinNucleo, View):
    form_class = DependenciaForm
    model = Dependencia
    aux = DependenciaContext.contexto
    template_name = 'dependencia.html'


class DependenciaEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(Dependencia, pk=pk)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class DependenciaAgregar(ObjectModalCreateMixin, View):
    form_class = DependenciaForm
    model = Dependencia
    template_name = 'modal/form_agregar_dependencia.html'


class DependenciaDetalle(ObjectModalUpdateMixin, View):
    form_class = DependenciaForm
    model = Dependencia
    template_name = 'modal/form_detalle_dependencia.html'


class DepartamentoJSON(View):
    def get(self, request):
        try:
            items = Departamento.objects.all()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'dependencia'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class DepartamentoLista(ObjectCreateMixinNucleo, View):
    form_class = DepartamentoForm
    model = Departamento
    aux = DepartamentoContext.contexto
    template_name = 'departamento.html'


class DepartamentoDetalle(ObjectUpdateMixinNucleo, View):
    form_class = DepartamentoForm
    model = Departamento
    aux = DepartamentoContext.contexto
    template_name = 'departamento.html'


class DepartamentoEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(Departamento, pk=pk)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class CargoJSON(View):
    def get(self, request):
        try:
            #usuarioid = User.objects.get(username=request.user.username).id
            items = Cargo.objects.all().exclude(nombre='Cátedras CONACYT').exclude(nombre='Investigador UNAM').exclude(
                nombre='Investigador Postdoctoral').exclude(nombre='Investigador por convenio').exclude(
                nombre='Investigador CONACYT').exclude(nombre='Investigador Invitado')
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'tipo_cargo'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class CargoLista(ObjectCreateMixinNucleo, View):
    form_class = CargoForm
    model = Cargo
    aux = CargoContext.contexto
    template_name = 'cargo.html'


class CargoDetalle(ObjectUpdateMixinNucleo, View):
    form_class = CargoForm
    model = Cargo
    aux = CargoContext.contexto
    template_name = 'cargo.html'


class CargoEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(Cargo, pk=pk)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class AreaEspecialidadJSON(View):
    def get(self, request):
        try:
            #usuarioid = User.objects.get(username=request.user.username).id
            items = AreaEspecialidad.objects.all()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'area_conocimiento'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class AreaEspecialidadLista(ObjectCreateMixinNucleo, View):
    form_class = AreaEspecialidadForm
    model = AreaEspecialidad
    aux = AreaEspecialidadContext.contexto
    template_name = 'area_especialidad.html'


class AreaEspecialidadDetalle(ObjectUpdateMixinNucleo, View):
    form_class = AreaEspecialidadForm
    model = AreaEspecialidad
    aux = AreaEspecialidadContext.contexto
    template_name = 'area_especialidad.html'


class AreaEspecialidadEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(AreaEspecialidad, pk=pk)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class ImpactoSocialJSON(View):
    def get(self, request):
        try:
            #usuarioid = User.objects.get(username=request.user.username).id
            items = ImpactoSocial.objects.all()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre',))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ImpactoSocialLista(ObjectCreateMixinNucleo, View):
    form_class = ImpactoSocialForm
    model = ImpactoSocial
    aux = ImpactoSocialContext.contexto
    template_name = 'simple.html'


class ImpactoSocialDetalle(ObjectUpdateMixinNucleo, View):
    form_class = ImpactoSocialForm
    model = ImpactoSocial
    aux = ImpactoSocialContext.contexto
    template_name = 'simple.html'


class ImpactoSocialEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(ImpactoSocial, pk=pk)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class FinanciamientoJSON(View):
    def get(self, request):
        try:
            items = Financiamiento.objects.all()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'tipo_financiamiento', 'dependencia'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class FinanciamientoLista(ObjectCreateMixinNucleo, View):
    form_class = FinanciamientoForm
    model = Financiamiento
    aux = FinanciamientoContext.contexto
    template_name = 'financiamiento.html'


class FinanciamientoDetalle(ObjectUpdateMixinNucleo, View):
    form_class = FinanciamientoForm
    model = Financiamiento
    aux = FinanciamientoContext.contexto
    template_name = 'financiamiento.html'


class FinanciamientoEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(Financiamiento, pk=pk)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class MetodologiaJSON(View):
    def get(self, request):
        try:
            #usuarioid = User.objects.get(username=request.user.username).id
            items = Metodologia.objects.all()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre',))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class MetodologiaLista(ObjectCreateMixinNucleo, View):
    form_class = MetodologiaForm
    model = Metodologia
    aux = MetodologiaContext.contexto
    template_name = 'simple.html'


class MetodologiaDetalle(ObjectUpdateMixinNucleo, View):
    form_class = MetodologiaForm
    model = Metodologia
    aux = MetodologiaContext.contexto
    template_name = 'simple.html'


class MetodologiaEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(Metodologia, pk=pk)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class BecaJSON(View):
    def get(self, request):
        try:
            #usuarioid = User.objects.get(username=request.user.username).id
            items = Beca.objects.all()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre',))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class BecaLista(ObjectCreateMixinNucleo, View):
    form_class = BecaForm
    model = Beca
    aux = BecaContext.contexto
    template_name = 'beca.html'


class BecaDetalle(ObjectUpdateMixinNucleo, View):
    form_class = BecaForm
    model = Beca
    aux = BecaContext.contexto
    template_name = 'beca.html'


class BecaEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(Beca, pk=pk)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class ReconocimientoJSON(View):
    def get(self, request):
        try:
            #usuarioid = User.objects.get(username=request.user.username).id
            items = Reconocimiento.objects.all()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre',))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ReconocimientoLista(ObjectCreateMixinNucleo, View):
    form_class = ReconocimientoForm
    model = Reconocimiento
    aux = ReconocimientoContext.contexto
    template_name = 'simple.html'


class ReconocimientoDetalle(ObjectUpdateMixinNucleo, View):
    form_class = ReconocimientoForm
    model = Reconocimiento
    aux = ReconocimientoContext.contexto
    template_name = 'simple.html'


class ReconocimientoEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(Reconocimiento, pk=pk)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class ProgramaLicenciaturaJSON(View):
    def get(self, request):
        try:
            #usuarioid = User.objects.get(username=request.user.username).id
            items = ProgramaLicenciatura.objects.all()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'area_conocimiento'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ProgramaLicenciaturaLista(ObjectCreateMixinNucleo, View):
    form_class = ProgramaLicenciaturaForm
    model = ProgramaLicenciatura
    aux = ProgramaLicenciaturaContext.contexto
    template_name = 'programa_academico.html'


class ProgramaLicenciaturaDetalle(ObjectUpdateMixinNucleo, View):
    form_class = ProgramaLicenciaturaForm
    model = ProgramaLicenciatura
    aux = ProgramaLicenciaturaContext.contexto
    template_name = 'programa_academico.html'


class ProgramaLicenciaturaEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(ProgramaLicenciatura, pk=pk)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class ProgramaMaestriaJSON(View):
    def get(self, request):
        try:
            #usuarioid = User.objects.get(username=request.user.username).id
            items = ProgramaMaestria.objects.all()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'area_conocimiento'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ProgramaMaestriaLista(ObjectCreateMixinNucleo, View):
    form_class = ProgramaMaestriaForm
    model = ProgramaMaestria
    aux = ProgramaMaestriaContext.contexto
    template_name = 'programa_academico.html'


class ProgramaMaestriaDetalle(ObjectUpdateMixinNucleo, View):
    form_class = ProgramaMaestriaForm
    model = ProgramaMaestria
    aux = ProgramaMaestriaContext.contexto
    template_name = 'programa_academico.html'


class ProgramaMaestriaEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(ProgramaMaestria, pk=pk)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class ProgramaDoctoradoJSON(View):
    def get(self, request):
        try:
            #usuarioid = User.objects.get(username=request.user.username).id
            items = ProgramaDoctorado.objects.all()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'area_conocimiento'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ProgramaDoctoradoLista(ObjectCreateMixinNucleo, View):
    form_class = ProgramaDoctoradoForm
    model = ProgramaDoctorado
    aux = ProgramaDoctoradoContext.contexto
    template_name = 'programa_academico.html'


class ProgramaDoctoradoDetalle(ObjectUpdateMixinNucleo, View):
    form_class = ProgramaDoctoradoForm
    model = ProgramaDoctorado
    aux = ProgramaDoctoradoContext.contexto
    template_name = 'programa_academico.html'


class ProgramaDoctoradoEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(ProgramaDoctorado, pk=pk)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class TipoEventoJSON(View):
    def get(self, request):
        try:
            #usuarioid = User.objects.get(username=request.user.username).id
            items = TipoEvento.objects.all()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre',))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class TipoEventoLista(ObjectCreateMixinNucleo, View):
    form_class = TipoEventoForm
    model = TipoEvento
    aux = TipoEventoContext.contexto
    template_name = 'simple.html'


class TipoEventoDetalle(ObjectUpdateMixinNucleo, View):
    form_class = TipoEventoForm
    model = TipoEvento
    aux = TipoEventoContext.contexto
    template_name = 'simple.html'


class TipoEventoEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(TipoEvento, pk=pk)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class TipoCursoJSON(View):
    def get(self, request):
        try:
            items = TipoCurso.objects.all()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre',))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class TipoCursoLista(ObjectCreateMixinNucleo, View):
    form_class = TipoCursoForm
    model = TipoCurso
    aux = TipoCursoContext.contexto
    template_name = 'simple.html'


class TipoCursoDetalle(ObjectUpdateMixinNucleo, View):
    form_class = TipoCursoForm
    model = TipoCurso
    aux = TipoCursoContext.contexto
    template_name = 'simple.html'


class TipoCursoEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(TipoCurso, pk=pk)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class EventoJSON(View):
    def get(self, request):
        try:
            #usuarioid = User.objects.get(username=request.user.username).id
            items = Evento.objects.all()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'tipo', 'fecha_inicio'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class EventoLista(ObjectCreateMixinNucleo, View):
    form_class = EventoForm
    model = Evento
    aux = EventoContext.contexto
    template_name = 'evento.html'


class EventoDetalle(ObjectUpdateMixinNucleo, View):
    form_class = EventoForm
    model = Evento
    aux = EventoContext.contexto
    template_name = 'evento.html'


class EventoEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(Evento, pk=pk)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class DistincionJSON(View):
    def get(self, request):
        try:
            #usuarioid = User.objects.get(username=request.user.username).id
            items = Distincion.objects.all()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'tipo'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class DistincionLista(ObjectCreateMixinNucleo, View):
    form_class = DistincionForm
    model = Distincion
    aux = DistincionContext.contexto
    template_name = 'distincion.html'


class DistincionDetalle(ObjectUpdateMixinNucleo, View):
    form_class = DistincionForm
    model = Distincion
    aux = DistincionContext.contexto
    template_name = 'distincion.html'


class DistincionEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(Distincion, pk=pk)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class MemoriaJSON(View):
    def get(self, request):
        try:
            #usuarioid = User.objects.get(username=request.user.username).id
            items = Memoria.objects.all()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'estado'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class EditorialJSON(View):
    def get(self, request):
        try:
            #usuarioid = User.objects.get(username=request.user.username).id
            items = Editorial.objects.all()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'pais'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class EditorialLista(ObjectCreateMixinNucleo, View):
    form_class = EditorialForm
    model = Editorial
    aux = EditorialContext.contexto
    template_name = 'editorial.html'


class EditorialDetalle(ObjectUpdateMixinNucleo, View):
    form_class = EditorialForm
    model = Editorial
    aux = EditorialContext.contexto
    template_name = 'editorial.html'


class EditorialEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(Editorial, pk=pk)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class ColeccionJSON(View):
    def get(self, request):
        try:
            #usuarioid = User.objects.get(username=request.user.username).id
            items = Coleccion.objects.all()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ColeccionLista(ObjectCreateMixinNucleo, View):
    form_class = ColeccionForm
    model = Coleccion
    aux = ColeccionContext.contexto
    template_name = 'simple.html'


class ColeccionDetalle(ObjectUpdateMixinNucleo, View):
    form_class = ColeccionForm
    model = Coleccion
    aux = ColeccionContext.contexto
    template_name = 'simple.html'


class ColeccionEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(Coleccion, pk=pk)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class RevistaJSON(View):
    def get(self, request):
        try:
            items = Revista.objects.all()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'pais'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class RevistaLista(ObjectCreateMixinNucleo, View):
    form_class = RevistaForm
    model = Revista
    aux = RevistaContext.contexto
    template_name = 'revista.html'


class RevistaDetalle(ObjectUpdateMixinNucleo, View):
    form_class = RevistaForm
    model = Revista
    aux = RevistaContext.contexto
    template_name = 'revista.html'


class RevistaEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(Revista, pk=pk)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class AsignaturaJSON(View):
    def get(self, request):
        try:
            #usuarioid = User.objects.get(username=request.user.username).id
            items = Asignatura.objects.all()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class AsignaturaLista(ObjectCreateMixinNucleo, View):
    form_class = AsignaturaForm
    model = Asignatura
    aux = AsignaturaContext.contexto
    template_name = 'simple.html'


class AsignaturaDetalle(ObjectUpdateMixinNucleo, View):
    form_class = AsignaturaForm
    model = Asignatura
    aux = AsignaturaContext.contexto
    template_name = 'simple.html'


class AsignaturaEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(Asignatura, pk=pk)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class MedioDivulgacionJSON(View):
    def get(self, request):
        try:
            #usuarioid = User.objects.get(username=request.user.username).id
            items = MedioDivulgacion.objects.all()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre_medio', 'tipo', 'canal', 'ciudad'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class MedioDivulgacionLista(ObjectCreateMixinNucleo, View):
    form_class = MedioDivulgacionForm
    model = MedioDivulgacion
    aux = MedioDivulgacionContext.contexto
    template_name = 'medio_divulgacion.html'


class MedioDivulgacionDetalle(ObjectUpdateMixinNucleo, View):
    form_class = MedioDivulgacionForm
    model = MedioDivulgacion
    aux = MedioDivulgacionContext.contexto
    template_name = 'medio_divulgacion.html'


class MedioDivulgacionEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(MedioDivulgacion, pk=pk)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class PersonaJSON(View):
    def get(self, request):
        try:
            #usuarioid = User.objects.get(username=request.user.username).id
            items = User.objects.all()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('username', 'first_name', 'last_name'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class PersonaLista(View):
    form_class = PersonaForm
    model = User
    aux = PersonaContext.contexto
    template_name = 'user.html'

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class, 'aux': self.aux, 'active': 'lista'})

    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            new_obj = bound_form.save(commit=False)
            new_username = "".join(new_obj.first_name.split() + new_obj.last_name.split())
            new_obj.username = ''.join(e for e in new_username if e.isalnum())
            new_obj.username = new_obj.username.lower()
            new_obj.password = "".join(str(uuid.uuid4()).split('-'))
            new_obj = bound_form.save()
            return redirect('./'+str(new_obj.pk))
        else:
            return render(request, self.template_name, {'form': bound_form, 'aux': self.aux, 'active': 'agregar'})


class PersonaDetalle(ObjectUpdateMixinNucleo, View):
    form_class = PersonaForm
    model = User
    aux = PersonaContext.contexto
    template_name = 'user.html'


    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        return render(request, self.template_name, {'form': self.form_class(instance=obj), 'aux': self.aux, 'active': 'detalle'})

    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        bound_form = self.form_class(request.POST, instance=obj)
        if bound_form.is_valid():

            det_obj = bound_form.save(commit=False)
            new_username = "".join(det_obj.first_name.split() + det_obj.last_name.split())
            det_obj.username = ''.join(e for e in new_username if e.isalnum())
            det_obj.username = det_obj.username.lower()
            det_obj.password = obj.password
            det_obj = bound_form.save()

            return redirect('../'+str(pk))
        else:
            return render(request, self.template_name, {'aux': self.aux, 'form': bound_form, 'active': 'detalle'})


class PersonaEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(User, pk=pk)
            item.delete()
            return redirect('../')
        except:
            raise Http404



class UserJSON(View):
    def get(self, request):
        try:
            #usuarioid = User.objects.get(username=request.user.username).id
            items = User.objects.all()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('username', 'first_name', 'last_name', 'email', 'pais_origen', 'ciudad'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class UserLista(View):
    form_class = UserForm
    model = User
    aux = PersonaContext.contexto
    template_name = 'user.html'

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class, 'aux': self.aux, 'active': 'lista'})

    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            new_obj = bound_form.save(commit=False)
            new_username = "".join(new_obj.first_name.split() + new_obj.last_name.split())
            new_obj.username = ''.join(e for e in new_username if e.isalnum())
            new_obj.username = new_obj.username.lower()
            new_obj.password = "".join(str(uuid.uuid4()).split('-'))
            new_obj = bound_form.save()
            return redirect(new_obj)
        else:
            return render(request, self.template_name, {'form': bound_form, 'aux': self.aux, 'active': 'agregar'})


class UserDetalle(View):
    form_class = UserForm
    model = User
    aux = PersonaContext.contexto
    template_name = 'user.html'

    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        return render(request, self.template_name, {'form': self.form_class(instance=obj), 'aux': self.aux, 'active': 'detalle'})

    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        bound_form = self.form_class(request.POST, instance=obj)
        if bound_form.is_valid():
            #det_obj = bound_form.save(commit=False)
            det_obj = bound_form.save()
            return redirect(det_obj)
        else:
            return render(request, self.template_name, {'aux': self.aux, 'form': bound_form, 'active': 'detalle'})



class UserEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(User, pk=pk)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class PerfilUsuario(View):
    form_class = UserForm
    model = User
    aux = UserContext.contexto
    template_name = 'perfil_usuario.html'

    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        print(pk)
        print(request.user.pk)
        if int(pk) == int(request.user.pk):
            return render(request, self.template_name, {'form': self.form_class(instance=obj), 'aux': self.aux, 'active': 'detalle'})
        else:
            return redirect('/perfil-usuario/' + str(request.user.pk))


    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        bound_form = self.form_class(request.POST, request.FILES or None, instance=obj)
        if bound_form.is_valid() and pk==request.user.pk:
            print(bound_form)
            det_obj = bound_form.save(commit=False)
            det_obj.username = request.user
            det_obj = bound_form.save()
            return redirect('/perfil-usuario/' + str(pk))
        else:
            return render(request, self.template_name, {'aux': self.aux, 'form': bound_form, 'active': 'detalle'})



class ProyectoArbitradoJSON(View):
    def get(self, request):
        try:
            #usuarioid = User.objects.get(username=request.user.username).id
            items = Ciudad.objects.all()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'fecha_inicio', 'institucion', 'dependencia', 'status'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404














class ZonaPaisList(generics.ListCreateAPIView):
    queryset = ZonaPais.objects.all()
    serializer_class = ZonaPaisSerializer

class ZonaPaisDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = ZonaPais.objects.all()
    serializer_class = ZonaPaisSerializer


class PaisList(generics.ListCreateAPIView):
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer

class PaisDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer


class EstadoList(generics.ListCreateAPIView):
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer

class EstadoDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer

class CiudadList(generics.ListCreateAPIView):
    queryset = Ciudad.objects.all()
    serializer_class = CiudadSerializer

class CiudadDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Ciudad.objects.all()
    serializer_class = CiudadSerializer


class UserList(generics.ListCreateAPIView):
    permission_classes = (UserListReadOnly,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUserOrReadOnly,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RESTInstitucionLista(generics.ListCreateAPIView):
    queryset = Institucion.objects.all()
    serializer_class = InstitucionSerializer

class RESTInstitucionDetalle(generics.RetrieveUpdateDestroyAPIView):
    queryset = Institucion.objects.all()
    serializer_class = InstitucionSerializer


class RESTDependenciaLista(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Dependencia.objects.all()
    serializer_class = DependenciaSerializer

class RESTDependenciaDetalle(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Dependencia.objects.all()
    serializer_class = DependenciaSerializer


class CargoList(generics.ListCreateAPIView):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer

class CargoDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer


class NombramientoList(generics.ListCreateAPIView):
    permission_classes = (UserListReadOnly,)
    queryset = Nombramiento.objects.all()
    serializer_class = NombramientoSerializer

class NombramientoDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (UserListReadOnly,)
    queryset = Nombramiento.objects.all()
    serializer_class = NombramientoSerializer


class AreaConocimientoList(generics.ListCreateAPIView):
    permission_classes = (UserListReadOnly,)
    queryset = AreaConocimiento.objects.all()
    serializer_class = AreaConocimientoSerializer

class AreaConocimientoDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (UserListReadOnly,)
    queryset = AreaConocimiento.objects.all()
    serializer_class = AreaConocimientoSerializer


class AreaEspecialidadList(generics.ListCreateAPIView):
    queryset = AreaEspecialidad.objects.all()
    serializer_class = AreaEspecialidadSerializer

class AreaEspecialidadDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = AreaEspecialidad.objects.all()
    serializer_class = AreaEspecialidadSerializer


class ImpactoSocialList(generics.ListCreateAPIView):
    queryset = ImpactoSocial.objects.all()
    serializer_class = ImpactoSocialSerializer

class ImpactoSocialDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = ImpactoSocial.objects.all()
    serializer_class = ImpactoSocialSerializer


class FinanciamientoList(generics.ListCreateAPIView):
    queryset = Financiamiento.objects.all()
    serializer_class = FinanciamientoSerializer

class FinanciamientoDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Financiamiento.objects.all()
    serializer_class = FinanciamientoSerializer


class MetodologiaList(generics.ListCreateAPIView):
    queryset = Metodologia.objects.all()
    serializer_class = MetodologiaSerializer

class MetodologiaDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Metodologia.objects.all()
    serializer_class = MetodologiaSerializer


class ProgramaLicenciaturaList(generics.ListCreateAPIView):
    queryset = ProgramaLicenciatura.objects.all()
    serializer_class = ProgramaLicenciaturaSerializer

class ProgramaLicenciaturaDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = ProgramaLicenciatura.objects.all()
    serializer_class = ProgramaLicenciaturaSerializer


class ProgramaMaestriaList(generics.ListCreateAPIView):
    queryset = ProgramaMaestria.objects.all()
    serializer_class = ProgramaMaestriaSerializer

class ProgramaMaestriaDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = ProgramaMaestria.objects.all()
    serializer_class = ProgramaMaestriaSerializer


class ProgramaDoctoradoList(generics.ListCreateAPIView):
    queryset = ProgramaDoctorado.objects.all()
    serializer_class = ProgramaDoctoradoSerializer


class ProgramaDoctoradoDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = ProgramaDoctorado.objects.all()
    serializer_class = ProgramaDoctoradoSerializer


class ProyectoList(generics.ListCreateAPIView):
    queryset = ProyectoInvestigacion.objects.all()
    serializer_class = ProyectoSerializer

class ProyectoDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = ProyectoInvestigacion.objects.all()
    serializer_class = ProyectoSerializer




