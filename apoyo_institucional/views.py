from django.http.response import (Http404, HttpResponse)
from django.views.generic import View
from django.core import serializers
from SIA.utils import *
from . forms import *
from . utils import *
from . models import *

# Create your views here.


class CargoAcademicoAdministrativoJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = CargoAcademicoAdministrativo.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('cargo', 'dependencia', 'cargo_inicio', 'cargo_fin'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class CargoAcademicoAdministrativoLista(ObjectCreateMixin, View):
    form_class = CargoAcademicoAdministrativoForm
    model = CargoAcademicoAdministrativo
    aux = CargoAcademicoAdministrativoContext.contexto
    template_name = 'main_otros.html'


class CargoAcademicoAdministrativoDetalle(ObjectUpdateMixin, View):
    form_class = CargoAcademicoAdministrativoForm
    model = CargoAcademicoAdministrativo
    aux = CargoAcademicoAdministrativoContext.contexto
    template_name = 'main_otros.html'