from django.http.response import (Http404, HttpResponse)
from django.views.generic import View
from django.core import serializers
from SIA.utils import *
from . forms import *
from . utils import *
from . models import *
from django.db.models import Q

#

# Create your views here.

class ArticuloDivulgacionJSON(View):
    otros = False
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            if self.otros:
                items = ArticuloDivulgacion.objects.all().exclude(autores__id__exact=usuarioid)
            else:
                items = ArticuloDivulgacion.objects.filter(autores__id__exact=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('titulo', 'status', 'revista'))
            return HttpResponse(json, content_type='application/json2')
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
    otros = False
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id

            if self.otros:
                items = CapituloLibroDivulgacion.objects.all().exclude(autores__id__exact=usuarioid)
            else:
                items = CapituloLibroDivulgacion.objects.filter(autores__id__exact=usuarioid)

            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('titulo', 'libro'))
            return HttpResponse(json, content_type='application/json2')
        except:
            raise Http404


class CapituloLibroDivulgacionLista(ObjectCreateVarMixin, View):
    form_class = CapituloLibroDivulgacionForm
    model = CapituloLibroDivulgacion
    aux = CapituloLibroDivulgacionContext.contexto
    template_name = 'capitulo_libro_divulgacion.html'


class CapituloLibroDivulgacionDetalle(ObjectUpdateVarMixin, View):
    form_class = CapituloLibroDivulgacionForm
    model = CapituloLibroDivulgacion
    aux = CapituloLibroDivulgacionContext.contexto
    template_name = 'capitulo_libro_divulgacion.html'


class CapituloLibroDivulgacionEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(CapituloLibroDivulgacion, pk=pk, usuarios=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class OrganizacionEventoDivulgacionJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id

            items = OrganizacionEventoDivulgacion.objects.filter(usuario__id=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('evento2', 'tipo_participacion'))

            return HttpResponse(json, content_type='application/json2')
        except:
            raise Http404


class OrganizacionEventoDivulgacionLista(ObjectCreateVarMixin, View):
    form_class = OrganizacionEventoDivulgacionForm
    model = OrganizacionEventoDivulgacion
    aux = OrganizacionEventoDivulgacionContext.contexto
    template_name = 'organizacion_evento_divulgacion.html'


class OrganizacionEventoDivulgacionDetalle(ObjectUpdateVarMixin, View):
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
    otros = False
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            if self.otros:
                items = ParticipacionEventoDivulgacion.objects.exclude(autores=usuarioid)
            else:
                items = ParticipacionEventoDivulgacion.objects.filter(autores=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('evento', 'ambito'))

            json = json.replace('INSTITUCIONAL', 'Institucional')
            json = json.replace('REGIONAL', 'Regional')
            json = json.replace('INTERNACIONAL', 'Internacional')
            json = json.replace('NACIONAL', 'Nacional')
            json = json.replace('OTRO', 'Otro')
            json = json.replace('COORDINADOR', 'Coordinador general')
            json = json.replace('COMITE', 'Comité organizador')
            json = json.replace('AYUDANTE', 'Ayudante')
            json = json.replace('TECNICO', 'Apoyo técnico')

            return HttpResponse(json, content_type='application/json2')
        except:
            raise Http404


class ParticipacionEventoDivulgacionLista(ObjectCreateVarMixin, View):
    form_class = ParticipacionEventoDivulgacionForm
    model = ParticipacionEventoDivulgacion
    aux = ParticipacionEventoDivulgacionContext.contexto
    template_name = 'participacion_evento_divulgacion.html'


class ParticipacionEventoDivulgacionDetalle(ObjectUpdateVarMixin, View):
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
                                         fields=('tema', 'fecha', 'actividad', 'medio_divulgacion'))

            json = json.replace('PRODUCCION', 'Producciòn')
            json = json.replace('PARTICIPACION', 'Participaciòn')
            json = json.replace('ENTREVISTA', 'Entrevista')
            json = json.replace('OTRA', 'Otra')

            return HttpResponse(json, content_type='application/json2')
        except:
            raise Http404


class ProgramaRadioTelevisionInternetLista(ObjectCreateMixin, View):
    form_class = ProgramaRadioTelevisionInternetForm
    model = ProgramaRadioTelevisionInternet
    aux = ProgramaRadioTelevisionInternetContext.contexto
    template_name = 'medio_divulgacion_cientifica.html'


class ProgramaRadioTelevisionInternetDetalle(ObjectUpdateMixin, View):
    form_class = ProgramaRadioTelevisionInternetForm
    model = ProgramaRadioTelevisionInternet
    aux = ProgramaRadioTelevisionInternetContext.contexto
    template_name = 'medio_divulgacion_cientifica.html'


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
                items = Libro.objects.filter(tipo='DIVULGACION').exclude(
                    Q(autores__id__exact=usuarioid) & Q(compiladores__id__exact=usuarioid) & Q(
                        agradecimientos__id__exact=usuarioid))
            else:
                items = Libro.objects.filter(tipo='DIVULGACION').filter(
                    Q(autores__id__exact=usuarioid) | Q(compiladores__id__exact=usuarioid) | Q(
                        agradecimientos__id__exact=usuarioid))
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'editorial_text', 'ciudad_text', 'status', 'fecha_enviado',
                                                 'fecha_aceptado', 'fecha_enprensa', 'fecha_publicado'))

            json = json.replace('PUBLICADO', 'Publicado')
            json = json.replace('ACEPTADO', 'Aceptado')
            json = json.replace('EN_PRENSA', 'En prensa')
            json = json.replace('ENVIADO', 'Enviado')

            json = json.replace('"fecha_enviado": null,', '')
            json = json.replace('"fecha_aceptado": null,', '')
            json = json.replace('"fecha_enprensa": null,', '')
            json = json.replace('"fecha_publicado": null,', '')

            json = json.replace('"fecha_enviado"', '"fecha"')
            json = json.replace('"fecha_aceptado"', '"fecha"')
            json = json.replace('"fecha_enprensa"', '"fecha"')
            json = json.replace('"fecha_publicado"', '"fecha"')

            return HttpResponse(json, content_type='application/json2')
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

    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        return render(request, self.template_name, {'form': self.form_class(instance=obj), 'aux': self.aux, 'active': 'detalle'})

    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        bound_form = self.form_class(request.POST, instance=obj)
        if bound_form.is_valid():
            det_obj = bound_form.save()
            print(det_obj)
            return redirect("/" + self.aux['url_categoria'] + "/" + self.aux['url_seccion'] + "/" + str(det_obj.pk))  # corregir el redirect
        else:
            return render(request, self.template_name, {'aux': self.aux, 'form': bound_form, 'active': 'detalle'})


class LibroDivulgacionEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(LibroDivulgacion, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404