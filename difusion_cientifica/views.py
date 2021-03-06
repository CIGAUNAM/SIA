from django.http.response import (Http404, HttpResponse)
from django.views.generic import View
from django.core import serializers
from django.db.models import Q
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
                items = MemoriaInExtenso.objects.all().exclude(autores__id__exact=usuarioid)
            else:
                items = MemoriaInExtenso.objects.filter(autores__id__exact=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'evento'))
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
    # template_name = 'main.html'


class MemoriaInExtensoEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(MemoriaInExtenso, pk=pk, usuarios=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class ResenaJSON(View):
    otros = False
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            if self.otros:
                items = Resena.objects.all().exclude(autores__id__exact=usuarioid)
            else:
                items = Resena.objects.filter(autores__id__exact=usuarioid)

            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('titulo', 'tipo', 'libro_resenado', 'articulo_resenado', 'revista_publica', 'fecha'))
            json = json.replace('"libro_resenado": null, ', '')
            json = json.replace('"articulo_resenado": null, ', '')
            json = json.replace('LIBRO', 'Libro')
            json = json.replace('ARTICULO', 'Artículo')
            json = json.replace('articulo_resenado', 'publicacion_resenada')
            json = json.replace('libro_resenado', 'publicacion_resenada')

            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ResenaLista(ObjectCreateVarMixin, View):
    form_class = ResenaForm
    model = Resena
    aux = ResenaContext.contexto
    template_name = 'resena.html'


class ResenaDetalle(ObjectUpdateVarMixin, View):
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
    otros = False
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            if self.otros:
                items = Traduccion.objects.all().exclude(autores__id__exact=usuarioid)
            else:
                items = Traduccion.objects.filter(autores__id__exact=usuarioid)

            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('titulo', 'tipo', 'libro', 'articulo', 'fecha'))
            json = json.replace('"libro": null, ', '')
            json = json.replace('"articulo": null, ', '')
            json = json.replace('LIBRO', 'Libro')
            json = json.replace('ARTICULO', 'Artículo')
            json = json.replace('articulo', 'publicacion')
            json = json.replace('libro', 'publicacion')

            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class TraduccionLista(ObjectCreateVarMixin, View):
    form_class = TraduccionForm
    model = Traduccion
    aux = TraduccionContext.contexto
    template_name = 'traduccion.html'


class TraduccionDetalle(ObjectUpdateVarMixin, View):
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
    otros = False
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id

            if self.otros:
                items = OrganizacionEventoAcademico.objects.all().exclude(Q(coordinador_general__id__exact=usuarioid) & Q(comite_organizador__id__exact=usuarioid) & Q(ayudantes__id__exact=usuarioid) & Q(apoyo_tecnico__id__exact=usuarioid)).distinct()
            else:
                items = OrganizacionEventoAcademico.objects.filter(Q(coordinador_general__id__exact=usuarioid) | Q(comite_organizador__id__exact=usuarioid) | Q(ayudantes__id__exact=usuarioid) | Q(apoyo_tecnico__id__exact=usuarioid)).distinct()

            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('evento', 'responsabilidad', 'ambito'))

            json = json.replace('INSTITUCIONAL', 'Institucional')
            json = json.replace('REGIONAL', 'Regional')
            json = json.replace('INTERNACIONAL', 'Internacional')
            json = json.replace('NACIONAL', 'Nacional')

            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class OrganizacionEventoAcademicoLista(ObjectCreateVarMixin, View):
    form_class = OrganizacionEventoAcademicoForm
    model = OrganizacionEventoAcademico
    aux = OrganizacionEventoAcademicoContext.contexto
    template_name = 'organizacion_evento_academico.html'


class OrganizacionEventoAcademicoDetalle(ObjectUpdateVarMixin, View):
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
    otros = False
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            if self.otros:
                items = ParticipacionEventoAcademico.objects.exclude(autores__id__exact=usuarioid)
            else:
                items = ParticipacionEventoAcademico.objects.filter(autores__id__exact=usuarioid)

            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('titulo', 'evento', 'ambito'))

            json = json.replace('COORDINADOR', 'Coordinador general')
            json = json.replace('COMITE', 'Comité organizador')
            json = json.replace('AYUDANTE', 'Ayudante')
            json = json.replace('TECNICO', 'Apoyo técnico')
            json = json.replace('OTRO', 'Otro')
            json = json.replace('INSTITUCIONAL', 'Institucional')
            json = json.replace('REGIONAL', 'Regional')
            json = json.replace('INTERNACIONAL', 'Internacional')
            json = json.replace('NACIONAL', 'Nacional')


            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ParticipacionEventoAcademicoLista(ObjectCreateVarMixin, View):
    form_class = ParticipacionEventoAcademicoForm
    model = ParticipacionEventoAcademico
    aux = ParticipacionEventoAcademicoContext.contexto
    template_name = 'participacion_evento_academico.html'


class ParticipacionEventoAcademicoDetalle(ObjectUpdateVarMixin, View):
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