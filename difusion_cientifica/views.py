from django.http.response import (Http404, HttpResponse)
from django.views.generic import View
from django.core import serializers
from SIA.utils import *
from . forms import *
from . utils import *
from . models import *

# Create your views here.

class MemoriaInExtensoJSON(View):
    otros = False
    def get(self, request):

        try:
            usuarioid = User.objects.get(username=request.user.username).id
            if self.otros:
                items = MemoriaInExtenso.objects.all().exclude(usuarios__id__exact=usuarioid)
            else:
                items = MemoriaInExtenso.objects.filter(usuarios__id__exact=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'ciudad', 'fecha', 'evento'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class MemoriaInExtensoLista(ObjectCreateVarMixin, View):
    form_class = MemoriaInExtensoForm
    model = MemoriaInExtenso
    aux = MemoriaInExtensoContext.contexto
    template_name = 'memoria_in_extenso.html'


class MemoriaInExtensoDetalle(ObjectUpdateVarMixin, View):
    form_class = MemoriaInExtensoForm
    model = MemoriaInExtenso
    aux = MemoriaInExtensoContext.contexto
    template_name = 'memoria_in_extenso.html'


class MemoriaInExtensoEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(MemoriaInExtenso, pk=pk, usuarios=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class PrologoLibroJSON(View):
    def get(self, request):

        try:
            usuarioid = User.objects.get(username=request.user.username).id

            items = PrologoLibro.objects.filter(usuario=usuarioid)

            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('libro',))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class PrologoLibroLista(ObjectCreateMixin, View):
    form_class = PrologoLibroForm
    model = PrologoLibro
    aux = PrologoLibroContext.contexto
    template_name = 'prologo_libro.html'


class PrologoLibroDetalle(ObjectUpdateMixin, View):
    form_class = PrologoLibroForm
    model = PrologoLibro
    aux = PrologoLibroContext.contexto
    template_name = 'prologo_libro.html'


class PrologoLibroEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(PrologoLibro, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class ResenaJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = Resena.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('titulo', 'libro_resenado', 'revista_resenada', 'revista_publica'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ResenaLista(ObjectCreateMixin, View):
    form_class = ResenaForm
    model = Resena
    aux = ResenaContext.contexto
    template_name = 'resena.html'


class ResenaDetalle(ObjectUpdateMixin, View):
    form_class = ResenaForm
    model = Resena
    aux = ResenaContext.contexto
    template_name = 'resena.html'


class ResenaEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(Resena, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class TraduccionJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = Traduccion.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('titulo_original', 'tipo', 'fecha'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class TraduccionLista(ObjectCreateMixin, View):
    form_class = TraduccionForm
    model = Traduccion
    aux = TraduccionContext.contexto
    template_name = 'main.html'


class TraduccionDetalle(ObjectUpdateMixin, View):
    form_class = TraduccionForm
    model = Traduccion
    aux = TraduccionContext.contexto
    template_name = 'traduccion.html'


class TraduccionEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(Resena, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class OrganizacionEventoAcademicoJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = OrganizacionEventoAcademico.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('evento', 'responsabilidad', 'ambito'))

            json = json.replace('COORDINADOR', 'Coordinador general')
            json = json.replace('COMITE', 'Comité organizador')
            json = json.replace('AYUDANTE', 'Ayudante')
            json = json.replace('TECNICO', 'Apoyo técnico')
            json = json.replace('OTRO', 'Otro')
            json = json.replace('INSTITUCIONAL', 'Institucional')
            json = json.replace('REGIONAL', 'Regional')
            json = json.replace('NACIONAL', 'Nacional')
            json = json.replace('INTERNACIONAL', 'Internacional')

            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class OrganizacionEventoAcademicoLista(ObjectCreateMixin, View):
    form_class = OrganizacionEventoAcademicoForm
    model = OrganizacionEventoAcademico
    aux = OrganizacionEventoAcademicoContext.contexto
    template_name = 'organizacion_evento_academico.html'


class OrganizacionEventoAcademicoDetalle(ObjectUpdateMixin, View):
    form_class = OrganizacionEventoAcademicoForm
    model = OrganizacionEventoAcademico
    aux = OrganizacionEventoAcademicoContext.contexto
    template_name = 'organizacion_evento_academico.html'


class OrganizacionEventoAcademicoEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(OrganizacionEventoAcademico, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class ParticipacionEventoAcademicoJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = ParticipacionEventoAcademico.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('titulo', 'evento', 'ambito'))

            json = json.replace('COORDINADOR', 'Coordinador general')
            json = json.replace('COMITE', 'Comité organizador')
            json = json.replace('AYUDANTE', 'Ayudante')
            json = json.replace('TECNICO', 'Apoyo técnico')
            json = json.replace('OTRO', 'Otro')
            json = json.replace('INSTITUCIONAL', 'Institucional')
            json = json.replace('REGIONAL', 'Regional')
            json = json.replace('NACIONAL', 'Nacional')
            json = json.replace('INTERNACIONAL', 'Internacional')

            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ParticipacionEventoAcademicoLista(ObjectCreateMixin, View):
    form_class = ParticipacionEventoAcademicoForm
    model = ParticipacionEventoAcademico
    aux = ParticipacionEventoAcademicoContext.contexto
    template_name = 'participacion_evento_academico.html'


class ParticipacionEventoAcademicoDetalle(ObjectUpdateMixin, View):
    form_class = ParticipacionEventoAcademicoForm
    model = ParticipacionEventoAcademico
    aux = ParticipacionEventoAcademicoContext.contexto
    template_name = 'participacion_evento_academico.html'


class ParticipacionEventoAcademicoEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(ParticipacionEventoAcademico, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404