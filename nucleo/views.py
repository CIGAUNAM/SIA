from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from nucleo.models import *
from nucleo.serializers import *
from rest_framework import generics
from . permissions import IsOwnerOrReadOnly, UserListReadOnly, IsAdminUserOrReadOnly
from rest_framework import permissions
from django.core import serializers
from django.views.generic import View

from SIA.utils import *
from . forms import *
from . utils import *
from . models import *


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
    template_name = 'main.html'


class PaisDetalle(ObjectUpdateMixinNucleo, View):
    form_class = PaisForm
    model = Pais
    aux = PaisContext.contexto
    template_name = 'main.html'


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
    template_name = 'main.html'


class EstadoDetalle(ObjectUpdateMixinNucleo, View):
    form_class = EstadoForm
    model = Estado
    aux = EstadoContext.contexto
    template_name = 'main.html'


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
    template_name = 'main.html'


class CiudadDetalle(ObjectUpdateMixinNucleo, View):
    form_class = CiudadForm
    model = Ciudad
    aux = CiudadContext.contexto
    template_name = 'main.html'


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
            items = Institucion.objects.all()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'pais'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class InstitucionLista(ObjectCreateMixinNucleo, View):
    form_class = InstitucionForm
    model = Institucion
    aux = InstitucionContext.contexto
    template_name = 'main.html'


class InstitucionDetalle(ObjectUpdateMixinNucleo, View):
    form_class = InstitucionForm
    model = Institucion
    aux = InstitucionContext.contexto
    template_name = 'main.html'


class InstitucionEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(Institucion, pk=pk)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class DependenciaJSON(View):
    def get(self, request):
        try:
            #usuarioid = User.objects.get(username=request.user.username).id
            items = Dependencia.objects.all()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'institucion'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class DependenciaLista(ObjectCreateMixinNucleo, View):
    form_class = DependenciaForm
    model = Dependencia
    aux = DependenciaContext.contexto
    template_name = 'main.html'


class DependenciaDetalle(ObjectUpdateMixinNucleo, View):
    form_class = DependenciaForm
    model = Dependencia
    aux = DependenciaContext.contexto
    template_name = 'main.html'


class DependenciaEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(Dependencia, pk=pk)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class DepartamentoJSON(View):
    def get(self, request):
        try:
            #usuarioid = User.objects.get(username=request.user.username).id
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
    template_name = 'main.html'


class DepartamentoDetalle(ObjectUpdateMixinNucleo, View):
    form_class = DepartamentoForm
    model = Departamento
    aux = DepartamentoContext.contexto
    template_name = 'main.html'


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
            items = Cargo.objects.all()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'tipo_cargo'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class CargoLista(ObjectCreateMixinNucleo, View):
    form_class = CargoForm
    model = Cargo
    aux = CargoContext.contexto
    template_name = 'main.html'


class CargoDetalle(ObjectUpdateMixinNucleo, View):
    form_class = CargoForm
    model = Cargo
    aux = CargoContext.contexto
    template_name = 'main.html'


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
    template_name = 'main.html'


class AreaEspecialidadDetalle(ObjectUpdateMixinNucleo, View):
    form_class = AreaEspecialidadForm
    model = AreaEspecialidad
    aux = AreaEspecialidadContext.contexto
    template_name = 'main.html'


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
    template_name = 'main.html'


class ImpactoSocialDetalle(ObjectUpdateMixinNucleo, View):
    form_class = ImpactoSocialForm
    model = ImpactoSocial
    aux = ImpactoSocialContext.contexto
    template_name = 'main.html'


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
            #usuarioid = User.objects.get(username=request.user.username).id
            items = Financiamiento.objects.all()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'tipo_financiamiento'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class FinanciamientoLista(ObjectCreateMixinNucleo, View):
    form_class = FinanciamientoForm
    model = Financiamiento
    aux = FinanciamientoContext.contexto
    template_name = 'main.html'


class FinanciamientoDetalle(ObjectUpdateMixinNucleo, View):
    form_class = FinanciamientoForm
    model = Financiamiento
    aux = FinanciamientoContext.contexto
    template_name = 'main.html'


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
    template_name = 'main.html'


class MetodologiaDetalle(ObjectUpdateMixinNucleo, View):
    form_class = MetodologiaForm
    model = Metodologia
    aux = MetodologiaContext.contexto
    template_name = 'main.html'


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
    template_name = 'main.html'


class BecaDetalle(ObjectUpdateMixinNucleo, View):
    form_class = BecaForm
    model = Beca
    aux = BecaContext.contexto
    template_name = 'main.html'


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
    template_name = 'main.html'


class ReconocimientoDetalle(ObjectUpdateMixinNucleo, View):
    form_class = ReconocimientoForm
    model = Reconocimiento
    aux = ReconocimientoContext.contexto
    template_name = 'main.html'


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
    template_name = 'main.html'


class ProgramaLicenciaturaDetalle(ObjectUpdateMixinNucleo, View):
    form_class = ProgramaLicenciaturaForm
    model = ProgramaLicenciatura
    aux = ProgramaLicenciaturaContext.contexto
    template_name = 'main.html'


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
    template_name = 'main.html'


class ProgramaMaestriaDetalle(ObjectUpdateMixinNucleo, View):
    form_class = ProgramaMaestriaForm
    model = ProgramaMaestria
    aux = ProgramaMaestriaContext.contexto
    template_name = 'main.html'


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
    template_name = 'main.html'


class ProgramaDoctoradoDetalle(ObjectUpdateMixinNucleo, View):
    form_class = ProgramaDoctoradoForm
    model = ProgramaDoctorado
    aux = ProgramaDoctoradoContext.contexto
    template_name = 'main.html'


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
    template_name = 'main.html'


class TipoEventoDetalle(ObjectUpdateMixinNucleo, View):
    form_class = TipoEventoForm
    model = TipoEvento
    aux = TipoEventoContext.contexto
    template_name = 'main.html'


class TipoEventoEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(TipoEvento, pk=pk)
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
    template_name = 'main.html'


class EventoDetalle(ObjectUpdateMixinNucleo, View):
    form_class = EventoForm
    model = Evento
    aux = EventoContext.contexto
    template_name = 'main.html'


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
                                         fields=('nombre', 'estado'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class DistincionLista(ObjectCreateMixinNucleo, View):
    form_class = DistincionForm
    model = Distincion
    aux = DistincionContext.contexto
    template_name = 'main.html'


class DistincionDetalle(ObjectUpdateMixinNucleo, View):
    form_class = DistincionForm
    model = Distincion
    aux = DistincionContext.contexto
    template_name = 'main.html'


class DistincionEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(Distincion, pk=pk)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class ProyectoJSON(View):
    def get(self, request):
        try:
            #usuarioid = User.objects.get(username=request.user.username).id
            items = Proyecto.objects.all()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'estado'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ProyectoLista(ObjectCreateMixinNucleo, View):
    form_class = ProyectoForm
    model = Proyecto
    aux = ProyectoContext.contexto
    template_name = 'main.html'


class ProyectoDetalle(ObjectUpdateMixinNucleo, View):
    form_class = ProyectoForm
    model = Proyecto
    aux = ProyectoContext.contexto
    template_name = 'main.html'


class ProyectoEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(Proyecto, pk=pk)
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


class MemoriaLista(ObjectCreateMixinNucleo, View):
    form_class = MemoriaForm
    model = Memoria
    aux = MemoriaContext.contexto
    template_name = 'main.html'


class MemoriaDetalle(ObjectUpdateMixinNucleo, View):
    form_class = MemoriaForm
    model = Memoria
    aux = MemoriaContext.contexto
    template_name = 'main.html'


class MemoriaEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(Memoria, pk=pk)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class EditorialJSON(View):
    def get(self, request):
        try:
            #usuarioid = User.objects.get(username=request.user.username).id
            items = Editorial.objects.all()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'estado'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class EditorialLista(ObjectCreateMixinNucleo, View):
    form_class = EditorialForm
    model = Editorial
    aux = EditorialContext.contexto
    template_name = 'main.html'


class EditorialDetalle(ObjectUpdateMixinNucleo, View):
    form_class = EditorialForm
    model = Editorial
    aux = EditorialContext.contexto
    template_name = 'main.html'


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
                                         fields=('nombre', 'estado'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ColeccionLista(ObjectCreateMixinNucleo, View):
    form_class = ColeccionForm
    model = Coleccion
    aux = ColeccionContext.contexto
    template_name = 'main.html'


class ColeccionDetalle(ObjectUpdateMixinNucleo, View):
    form_class = ColeccionForm
    model = Coleccion
    aux = ColeccionContext.contexto
    template_name = 'main.html'


class ColeccionEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(Coleccion, pk=pk)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class LibroJSON(View):
    def get(self, request):
        try:
            #usuarioid = User.objects.get(username=request.user.username).id
            items = Libro.objects.all()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'estado'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class LibroLista(ObjectCreateMixinNucleo, View):
    form_class = LibroForm
    model = Libro
    aux = LibroContext.contexto
    template_name = 'main.html'


class LibroDetalle(ObjectUpdateMixinNucleo, View):
    form_class = LibroForm
    model = Libro
    aux = LibroContext.contexto
    template_name = 'main.html'


class LibroEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(Libro, pk=pk)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class RevistaJSON(View):
    def get(self, request):
        try:
            #usuarioid = User.objects.get(username=request.user.username).id
            items = Revista.objects.all()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'estado'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class RevistaLista(ObjectCreateMixinNucleo, View):
    form_class = RevistaForm
    model = Revista
    aux = RevistaContext.contexto
    template_name = 'main.html'


class RevistaDetalle(ObjectUpdateMixinNucleo, View):
    form_class = RevistaForm
    model = Revista
    aux = RevistaContext.contexto
    template_name = 'main.html'


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
                                         fields=('nombre', 'estado'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class AsignaturaLista(ObjectCreateMixinNucleo, View):
    form_class = AsignaturaForm
    model = Asignatura
    aux = AsignaturaContext.contexto
    template_name = 'main.html'


class AsignaturaDetalle(ObjectUpdateMixinNucleo, View):
    form_class = AsignaturaForm
    model = Asignatura
    aux = AsignaturaContext.contexto
    template_name = 'main.html'


class AsignaturaEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(Asignatura, pk=pk)
            item.delete()
            return redirect('../')
        except:
            raise Http404




















"""
class InstitucionCrear(View):
    form_class = InstitucionForm
    model = Institucion
    #template_name = 'agregar_institucion.html'

    def get(self, request):
        return render(request, self.template_name, {'form_institucion': self.form_class})

    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            new_obj = bound_form.save()
            print(str(new_obj) + 'guardado')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            #return HttpResponseRedirect("")
            #return HttpResponse("<script>$('#agregar-institucion').modal('hide');</script>")
        else:
            return render(request, self.template_name, {'form_institucion': bound_form})
"""

















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


class InstitucionList(generics.ListCreateAPIView):
    queryset = Institucion.objects.all()
    serializer_class = InstitucionSerializer

class InstitucionDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Institucion.objects.all()
    serializer_class = InstitucionSerializer


class DependenciaList(generics.ListCreateAPIView):
    queryset = Dependencia.objects.all()
    serializer_class = DependenciaSerializer

class DependenciaDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
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
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer

class ProyectoDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer

#@permission_classes((permissions.IsAuthenticatedOrReadOnly,))