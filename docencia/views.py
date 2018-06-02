from django.http.response import (Http404, HttpResponse)
from django.views.generic import View
from django.core import serializers
from SIA.utils import *
from . forms import *
from . utils import *
from . models import *
from nucleo.models import Libro as LibroLibroDocencia
from django.db.models import Q

# Create your views here.


class CursoDocenciaEscolarizadoJSON(View):
    otros = False
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = CursoDocenciaEscolarizado.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('asignatura', 'nivel', 'dependencia', 'fecha_inicio', 'total_horas'))
            json = json.replace('LICENCIATURA', 'Licenciatura')
            json = json.replace('MAESTRIA', 'Maestría')
            json = json.replace('DOCTORADO', 'Doctorado')

            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class CursoDocenciaEscolarizadoLista(ObjectCreateMixin, View):
    form_class = CursoDocenciaEscolarizadoForm
    model = CursoDocenciaEscolarizado
    aux = CursoDocenciaEscolarizadoContext.contexto
    template_name = 'curso_docencia_escolarizado.html'


class CursoDocenciaEscolarizadoDetalle(ObjectUpdateMixin, View):
    form_class = CursoDocenciaEscolarizadoForm
    model = CursoDocenciaEscolarizado
    aux = CursoDocenciaEscolarizadoContext.contexto
    template_name = 'curso_docencia_escolarizado.html'


class CursoDocenciaExtracurricularJSON(View):
    otros = False
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = CursoDocenciaExtracurricular.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('asignatura', 'dependencia', 'fecha_inicio', 'total_horas'))

            json = json.replace('LICENCIATURA', 'Licenciatura')
            json = json.replace('MAESTRIA', 'Maestría')
            json = json.replace('DOCTORADO', 'Doctorado')
            json = json.replace('OTRO', 'Otro')

            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class CursoDocenciaExtracurricularLista(ObjectCreateMixin, View):
    form_class = CursoDocenciaExtracurricularForm
    model = CursoDocenciaExtracurricular
    aux = CursoDocenciaExtracurricularContext.contexto
    template_name = 'curso_docencia_extracurricular.html'


class CursoDocenciaExtracurricularDetalle(ObjectUpdateMixin, View):
    form_class = CursoDocenciaExtracurricularForm
    model = CursoDocenciaExtracurricular
    aux = CursoDocenciaExtracurricularContext.contexto
    template_name = 'curso_docencia_extracurricular.html'


class CursoDocenciaEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(CursoDocenciaEscolarizado, Q(pk=pk, academicos_participantes=request.user) | Q(pk=pk, usuario=request.user))
            item.delete()
            return redirect('../')
        except:
            raise Http404


class ArticuloDocenciaJSON(View):
    otros = False
    def get(self, request):

        try:
            usuarioid = User.objects.get(username=request.user.username).id
            if self.otros:
                articulos = ArticuloDocencia.objects.all().exclude(usuarios__id__exact=usuarioid)
            else:
                articulos = ArticuloDocencia.objects.filter(usuarios__id__exact=usuarioid)
            json = serializers.serialize('json', articulos, use_natural_foreign_keys=True,
                                         fields=('titulo', 'tipo', 'revista', 'status', 'fecha'))

            json = json.replace('ARTICULO', 'Artículo')
            json = json.replace('ACTA', 'Acta')
            json = json.replace('CARTA', 'Carta')
            json = json.replace('RESENA', 'Reseña')
            json = json.replace('OTRO', 'Otro')

            json = json.replace('PUBLICADO', 'Publicado')
            json = json.replace('EN_PRENSA', 'En prensa')
            json = json.replace('ACEPTADO', 'Aceptado')
            json = json.replace('ENVIADO', 'Enviado')
            json = json.replace('ENVIADO', 'Enviado')

            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ArticuloDocenciaLista(ObjectCreateVarMixin, View):
    form_class = ArticuloDocenciaForm
    model = ArticuloDocencia
    aux = ArticuloDocenciaContext.contexto
    template_name = 'articulo_docencia.html'


class ArticuloDocenciaDetalle(ObjectUpdateVarMixin, View):
    form_class = ArticuloDocenciaForm
    model = ArticuloDocencia
    aux = ArticuloDocenciaContext.contexto
    template_name = 'articulo_docencia.html'


class ArticuloDocenciaEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(ArticuloDocencia, pk=pk, usuarios=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class LibroDocenciaJSON(View):
    otros = False
    def get(self, request):

        try:
            usuarioid = User.objects.get(username=request.user.username).id
            if self.otros:
                items = Libro.objects.filter(tipo='DOCENCIA').exclude(usuarios__id__exact=usuarioid)
            else:
                items = Libro.objects.filter(usuarios__id__exact=usuarioid, tipo='DOCENCIA')
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'editorial', 'ciudad', 'status', 'fecha'))

            json = json.replace('PUBLICADO', 'Publicado')
            json = json.replace('EN_PRENSA', 'En prensa')
            json = json.replace('ACEPTADO', 'Aceptado')
            json = json.replace('ENVIADO', 'Enviado')

            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class LibroDocenciaLista(ObjectCreateVarMixin, View):
    form_class = LibroDocenciaForm
    model = LibroLibroDocencia
    aux = LibroDocenciaContext.contexto
    template_name = 'libro_docencia.html'

    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            new_obj = bound_form.save(commit=False)
            new_obj.tipo = 'DOCENCIA'
            new_obj = bound_form.save()

            return redirect("/" + self.aux['url_categoria'] + "/" + self.aux['url_seccion'] + "/" + str(new_obj.pk)) #corregir el redirect

        else:
            return render(request, self.template_name, {'form': bound_form, 'aux': self.aux, 'active': 'agregar'})


class LibroDocenciaDetalle(ObjectUpdateVarMixin, View):
    form_class = LibroDocenciaForm
    model = LibroLibroDocencia
    aux = LibroDocenciaContext.contexto
    template_name = 'libro_docencia.html'

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


class LibroDocenciaEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(Libro, pk=pk, tipo='DOCENCIA', usuarios=request.user)
            item.delete()
            return redirect('/docencia/libros-docencia/')
        except:
            raise Http404














class ProgramaEstudioJSON(View):
    otros = False
    def get(self, request):

        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = ProgramaEstudio.objects.filter(usuario__id__exact=usuarioid,)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'nivel', 'fecha'))

            json = json.replace('LICENCIATURA', 'Licenciatura')
            json = json.replace('MAESTRIA', 'Maestría')
            json = json.replace('DOCTORADO', 'Doctorado')

            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404

class ProgramaEstudioLista(ObjectCreateMixin, View):
    form_class = ProgramaEstudioForm
    model = ProgramaEstudio
    aux = ProgramaEstudioContext.contexto
    template_name = 'programa_estudio.html'


class ProgramaEstudioDetalle(ObjectUpdateMixin, View):
    form_class = ProgramaEstudioForm
    model = ProgramaEstudio
    aux = ProgramaEstudioContext.contexto
    template_name = 'programa_estudio.html'


class ProgramaEstudioEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(ProgramaEstudio, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404
