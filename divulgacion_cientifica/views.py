from django.http.response import (Http404, HttpResponse)
from django.views.generic import View
from django.core import serializers
from SIA.utils import *
from . forms import *
from . utils import *
from . models import *

#

# Create your views here.

class ArticuloDivulgacionJSON(View):
    otros = False
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            if self.otros:
                items = ArticuloDivulgacion.objects.all().exclude(usuarios__id__exact=usuarioid)
            else:
                items = ArticuloDivulgacion.objects.filter(usuarios__id__exact=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('titulo', 'tipo', 'status', 'revista'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ArticuloDivulgacionLista(ObjectCreateVarMixin, View):
    form_class = ArticuloDivulgacionForm
    model = ArticuloDivulgacion
    aux = ArticuloDivulgacionContext.contexto
    template_name = 'articulo_divulgacion.html'


class ArticuloDivulgacionDetalle(ObjectUpdateVarMixin, View):
    form_class = ArticuloDivulgacionForm
    model = ArticuloDivulgacion
    aux = ArticuloDivulgacionContext.contexto
    template_name = 'articulo_divulgacion.html'


class ArticuloDivulgacionEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(ArticuloDivulgacion, pk=pk, usuarios=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class CapituloLibroDivulgacionJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = CapituloLibroDivulgacion.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('titulo', 'libro'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class CapituloLibroDivulgacionLista(ObjectCreateMixin, View):
    form_class = CapituloLibroDivulgacionForm
    model = CapituloLibroDivulgacion
    aux = CapituloLibroDivulgacionContext.contexto
    template_name = 'capitulo_libro_divulgacion.html'


class CapituloLibroDivulgacionDetalle(ObjectUpdateMixin, View):
    form_class = CapituloLibroDivulgacionForm
    model = CapituloLibroDivulgacion
    aux = CapituloLibroDivulgacionContext.contexto
    template_name = 'capitulo_libro_divulgacion.html'


class CapituloLibroDivulgacionEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(CapituloLibroDivulgacion, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class OrganizacionEventoDivulgacionJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = OrganizacionEventoDivulgacion.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('evento', 'responsabilidad', 'ambito'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class OrganizacionEventoDivulgacionLista(ObjectCreateMixin, View):
    form_class = OrganizacionEventoDivulgacionForm
    model = OrganizacionEventoDivulgacion
    aux = OrganizacionEventoDivulgacionContext.contexto
    template_name = 'organizacion_evento_divulgacion.html'


class OrganizacionEventoDivulgacionDetalle(ObjectUpdateMixin, View):
    form_class = OrganizacionEventoDivulgacionForm
    model = OrganizacionEventoDivulgacion
    aux = OrganizacionEventoDivulgacionContext.contexto
    template_name = 'organizacion_evento_divulgacion.html'


class OrganizacionEventoDivulgacionEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(OrganizacionEventoDivulgacion, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class ParticipacionEventoDivulgacionJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = ParticipacionEventoDivulgacion.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('titulo', 'evento', 'ambito'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ParticipacionEventoDivulgacionLista(ObjectCreateMixin, View):
    form_class = ParticipacionEventoDivulgacionForm
    model = ParticipacionEventoDivulgacion
    aux = ParticipacionEventoDivulgacionContext.contexto
    template_name = 'participacion_evento_divulgacion.html'


class ParticipacionEventoDivulgacionDetalle(ObjectUpdateMixin, View):
    form_class = ParticipacionEventoDivulgacionForm
    model = ParticipacionEventoDivulgacion
    template_name = 'participacion_evento_divulgacion.html'
    aux = ParticipacionEventoDivulgacionContext.contexto


class ParticipacionEventoDivulgacionEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(ParticipacionEventoDivulgacion, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class ProgramaRadioTelevisionInternetJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = ProgramaRadioTelevisionInternet.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('tema', 'fecha', 'nombre_medio', 'medio'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ProgramaRadioTelevisionInternetLista(ObjectCreateMixin, View):
    form_class = ProgramaRadioTelevisionInternetForm
    model = ProgramaRadioTelevisionInternet
    aux = ProgramaRadioTelevisionInternetContext.contexto
    template_name = 'medio_divulgacion.html'


class ProgramaRadioTelevisionInternetDetalle(ObjectUpdateMixin, View):
    form_class = ProgramaRadioTelevisionInternetForm
    model = ProgramaRadioTelevisionInternet
    aux = ProgramaRadioTelevisionInternetContext.contexto
    template_name = 'medio_divulgacion.html'


class ProgramaRadioTelevisionInternetEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(ProgramaRadioTelevisionInternet, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class LibroDivulgacionJSON(View):
    otros = False
    def get(self, request):

        try:
            usuarioid = User.objects.get(username=request.user.username).id
            if self.otros:
                items = LibroDivulgacion.objects.filter(tipo='DIVULGACION').exclude(usuarios__id__exact=usuarioid)
            else:
                items = LibroDivulgacion.objects.filter(usuarios__id__exact=usuarioid, tipo='DIVULGACION')
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'editorial', 'ciudad', 'status', 'fecha'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class LibroDivulgacionLista(ObjectCreateVarMixin, View):
    form_class = LibroDivulgacionForm
    model = LibroDivulgacion
    aux = LibroDivulgacionContext.contexto
    template_name = 'libro_divulgacion.html'

    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            new_obj = bound_form.save(commit=False)
            new_obj.tipo = 'DIVULGACION'
            new_obj = bound_form.save()

            return redirect("/" + self.aux['url_categoria'] + "/" + self.aux['url_seccion'] + "/" + str(new_obj.pk)) #corregir el redirect

        else:
            return render(request, self.template_name, {'form': bound_form, 'aux': self.aux, 'active': 'agregar'})


class LibroDivulgacionDetalle(ObjectUpdateVarMixin, View):
    form_class = LibroDivulgacionForm
    model = LibroDivulgacion
    aux = LibroDivulgacionContext.contexto
    template_name = 'libro_divulgacion.html'


class LibroDivulgacionEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(LibroDivulgacion, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404