from django.http.response import (Http404, HttpResponse)
from django.views.generic import View
from django.core import serializers
from SIA.utils import *
from . forms import *
from . utils import *
from . models import *
from django.db.models import Q

# Create your views here.


class CursoDocenciaLicenciaturaJSON(View):
    otros = False
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id

            if self.otros:
                items = CursoDocencia.objects.filter(tipo='ESCOLARIZADO').exclude(usuarios__id__exact=usuarioid).exclude(usuario=usuarioid)
            else:
                items = CursoDocencia.objects.filter(Q(usuarios__id__exact=usuarioid, tipo='ESCOLARIZADO') | Q(usuario=usuarioid, tipo='ESCOLARIZADO'))
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('asignatura', 'nivel', 'dependencia', 'fecha_inicio', 'total_horas'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class CursoDocenciaLicenciaturaLista(ObjectCreateMixin, View):
    form_class = CursoDocenciaForm
    model = CursoDocencia
    CursoDocenciaContext.url_seccion = 'cursos-escolarizados'
    aux = CursoDocenciaContext.contexto
    template_name = 'main_otros.html'


class CursoDocenciaLicenciaturaDetalle(ObjectUpdateMixin, View):
    form_class = CursoDocenciaForm
    model = CursoDocencia
    CursoDocenciaContext.url_seccion = 'cursos-escolarizados'
    aux = CursoDocenciaContext.contexto
    template_name = 'main_otros.html'