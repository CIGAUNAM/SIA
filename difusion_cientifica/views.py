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
                                         fields=('titulo', 'ciudad', 'fecha', 'evento'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class MemoriaInExtensoLista(ObjectCreateVarMixin, View):
    form_class = MemoriaInExtensoForm
    model = MemoriaInExtenso
    aux = MemoriaInExtensoContext.contexto
    template_name = 'main.html'


class MemoriaInExtensoDetalle(ObjectUpdateVarMixin, View):
    form_class = MemoriaInExtensoForm
    model = MemoriaInExtenso
    aux = MemoriaInExtensoContext.contexto
    template_name = 'main.html'



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
    template_name = 'main.html'


class PrologoLibroDetalle(ObjectUpdateMixin, View):
    form_class = PrologoLibroForm
    model = PrologoLibro
    aux = PrologoLibroContext.contexto
    template_name = 'main.html'



class ResenaJSON(View):
    def get(self, request):

        try:
            usuarioid = User.objects.get(username=request.user.username).id

            items = Resena.objects.filter(usuario=usuarioid)

            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('titulo', 'libro_resenado', 'revista_resenada', 'libro_publica', 'revista_publica'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ResenaLista(ObjectCreateMixin, View):
    form_class = ResenaForm
    model = Resena
    aux = ResenaContext.contexto
    template_name = 'main.html'


class ResenaDetalle(ObjectUpdateMixin, View):
    form_class = ResenaForm
    model = Resena
    aux = ResenaContext.contexto
    template_name = 'main.html'



class OrganizacionEventoAcademicoJSON(View):
    def get(self, request):

        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = OrganizacionEventoAcademico.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('evento', 'responsabilidad', 'ambito'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class OrganizacionEventoAcademicoLista(ObjectCreateMixin, View):
    form_class = OrganizacionEventoAcademicoForm
    model = OrganizacionEventoAcademico
    aux = OrganizacionEventoAcademicoContext.contexto
    template_name = 'main.html'


class OrganizacionEventoAcademicoDetalle(ObjectUpdateMixin, View):
    form_class = OrganizacionEventoAcademicoForm
    model = OrganizacionEventoAcademico
    aux = OrganizacionEventoAcademicoContext.contexto
    template_name = 'main.html'



class ParticipacionEventoAcademicoJSON(View):
    def get(self, request):

        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = ParticipacionEventoAcademico.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('titulo', 'evento', 'ambito'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ParticipacionEventoAcademicoLista(ObjectCreateMixin, View):
    form_class = ParticipacionEventoAcademicoForm
    model = ParticipacionEventoAcademico
    aux = ParticipacionEventoAcademicoContext.contexto
    template_name = 'main.html'


class ParticipacionEventoAcademicoDetalle(ObjectUpdateMixin, View):
    form_class = ParticipacionEventoAcademicoForm
    model = ParticipacionEventoAcademico
    aux = ParticipacionEventoAcademicoContext.contexto
    template_name = 'main.html'