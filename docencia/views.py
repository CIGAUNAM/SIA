from django.http.response import (Http404, HttpResponse)
from django.views.generic import View
from django.core import serializers
from SIA.utils import *
from . forms import *
from . utils import *
from . models import *
from django.db.models import Q

# Create your views here.


class CursoDocenciaEscolarizadoJSON(View):
    otros = False
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id

            if self.otros:
                items = CursoDocencia.objects.filter(tipo='ESCOLARIZADO').exclude(academicos_participantes__id__exact=usuarioid).exclude(usuario=usuarioid)
            else:
                items = CursoDocencia.objects.filter(Q(academicos_participantes__id__exact=usuarioid, tipo='ESCOLARIZADO') | Q(usuario=usuarioid, tipo='ESCOLARIZADO'))
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('asignatura', 'nivel', 'dependencia', 'fecha_inicio', 'total_horas'))

            json = json.replace('LICENCIATURA', 'Licenciatura')
            json = json.replace('MAESTRIA', 'Maestría')
            json = json.replace('DOCTORADO', 'Doctorado')
            json = json.replace('OTRO', 'Otro')

            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class CursoDocenciaEscolarizadoLista(ObjectCreateMixin, View):
    form_class = CursoDocenciaForm
    model = CursoDocencia
    aux = CursoDocenciaEscolarizadoContext.contexto
    template_name = 'cursos_docencia.html'

    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            new_obj = bound_form.save(commit=False)
            new_obj.tipo = 'ESCOLARIZADO'
            new_obj.usuario = request.user
            new_obj = bound_form.save()
            return redirect("/" + self.aux['url_categoria'] + "/" + self.aux['url_seccion'] + "/" + str(new_obj.pk)) #corregir el redirect
        else:
            return render(request, self.template_name, {'form': bound_form, 'aux': self.aux, 'active': 'agregar'})


class CursoDocenciaEscolarizadoDetalle(ObjectUpdateMixin, View):
    form_class = CursoDocenciaForm
    model = CursoDocencia
    aux = CursoDocenciaEscolarizadoContext.contexto
    template_name = 'cursos_docencia.html'

    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        bound_form = self.form_class(request.POST, instance=obj)
        if bound_form.is_valid():
            det_obj = bound_form.save()
            return redirect("/" + self.aux['url_categoria'] + "/" + self.aux['url_seccion'] + "/" + str(det_obj.pk)) #corregir el redirect
        else:
            return render(request, self.template_name, {'aux': self.aux, 'form': bound_form, 'active': 'detalle'})


class CursoDocenciaExtracurricularJSON(View):
    otros = False
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id

            if self.otros:
                items = CursoDocencia.objects.filter(tipo='EXTRACURRICULAR').exclude(academicos_participantes__id__exact=usuarioid).exclude(usuario=usuarioid)
            else:
                items = CursoDocencia.objects.filter(Q(academicos_participantes__id__exact=usuarioid, tipo='EXTRACURRICULAR') | Q(usuario=usuarioid, tipo='EXTRACURRICULAR'))
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('asignatura', 'nivel', 'dependencia', 'fecha_inicio', 'total_horas'))

            json = json.replace('LICENCIATURA', 'Licenciatura')
            json = json.replace('MAESTRIA', 'Maestría')
            json = json.replace('DOCTORADO', 'Doctorado')
            json = json.replace('OTRO', 'Otro')

            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class CursoDocenciaExtracurricularLista(ObjectCreateMixin, View):
    form_class = CursoDocenciaForm
    model = CursoDocencia
    aux = CursoDocenciaExtracurricularContext.contexto
    template_name = 'cursos_docencia.html'

    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            new_obj = bound_form.save(commit=False)
            new_obj.tipo = 'EXTRACURRICULAR'
            new_obj.usuario = request.user
            new_obj = bound_form.save()
            return redirect("/" + self.aux['url_categoria'] + "/" + self.aux['url_seccion'] + "/" + str(new_obj.pk)) #corregir el redirect
        else:
            return render(request, self.template_name, {'form': bound_form, 'aux': self.aux, 'active': 'agregar'})


class CursoDocenciaExtracurricularDetalle(ObjectUpdateMixin, View):
    form_class = CursoDocenciaForm
    model = CursoDocencia
    aux = CursoDocenciaExtracurricularContext.contexto
    template_name = 'cursos_docencia.html'

    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        bound_form = self.form_class(request.POST, instance=obj)
        if bound_form.is_valid():
            det_obj = bound_form.save()
            return redirect("/" + self.aux['url_categoria'] + "/" + self.aux['url_seccion'] + "/" + str(det_obj.pk)) #corregir el redirect
        else:
            return render(request, self.template_name, {'aux': self.aux, 'form': bound_form, 'active': 'detalle'})



class CursoDocenciaEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(CursoDocencia, Q(pk=pk, academicos_participantes=request.user) | Q(pk=pk, usuario=request.user))
            item.delete()
            return redirect('../')
        except:
            raise Http404