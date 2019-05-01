from django.views.generic import View
from django.core import serializers
from SIA.utils import *
from .forms import *
from .utils import *
from formatos.forms import *
from django.template.loader import get_template
from subprocess import Popen, PIPE
import tempfile
import os

# Create your views here.


class FormatoServicioTransporteJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = FormatoServicioTransporte.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items,
                                         fields=('fecha_inicio', 'ciudad'),
                                         use_natural_foreign_keys=True)
            return HttpResponse(json, content_type='application/json2')
        except:
            raise Http404


class FormatoServicioTransporteLista(ObjectCreateMixin, View):
    form_class = FormatoServicioTransporteForm
    model = FormatoServicioTransporte
    aux = FormatoServicioTransporteContext.contexto
    template_name = 'servicio_transporte.html'


class FormatoServicioTransporteDetalle(ObjectUpdateMixin, View):
    form_class = FormatoServicioTransporteForm
    model = FormatoServicioTransporte
    aux = FormatoServicioTransporteContext.contexto
    template_name = 'servicio_transporte.html'


class FormatoServicioTransporteEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(FormatoServicioTransporte, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404



class FormatoLicenciaGoceSueldoJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = FormatoLicenciaGoceSueldo.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items,
                                         fields=('evento', 'fecha_inicio'),
                                         use_natural_foreign_keys=True)
            return HttpResponse(json, content_type='application/json2')
        except:
            raise Http404


class FormatoLicenciaGoceSueldoLista(ObjectCreateMixin, View):
    form_class = FormatoLicenciaGoceSueldoForm
    model = FormatoLicenciaGoceSueldo
    aux = FormatoLicenciaGoceSueldoContext.contexto
    template_name = 'licencia_goce_sueldo.html'


class FormatoLicenciaGoceSueldoDetalle(ObjectUpdateMixin, View):
    form_class = FormatoLicenciaGoceSueldoForm
    model = FormatoLicenciaGoceSueldo
    aux = FormatoLicenciaGoceSueldoContext.contexto
    template_name = 'licencia_goce_sueldo.html'


class FormatoLicenciaGoceSueldoEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(FormatoLicenciaGoceSueldo, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404



class FormatoPagoViaticoJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            items = FormatoPagoViatico.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', items,
                                         fields=('evento', 'fecha_salida'),
                                         use_natural_foreign_keys=True)
            return HttpResponse(json, content_type='application/json2')
        except:
            raise Http404


class FormatoPagoViaticoLista(ObjectCreateMixin, View):
    form_class = FormatoPagoViaticoForm
    model = FormatoPagoViatico
    aux = FormatoPagoViaticoContext.contexto
    template_name = 'pago_viaticos.html'


class FormatoPagoViaticoDetalle(ObjectUpdateMixin, View):
    form_class = FormatoPagoViaticoForm
    model = FormatoPagoViatico
    aux = FormatoPagoViaticoContext.contexto
    template_name = 'pago_viaticos.html'


class FormatoPagoViaticoEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(FormatoLicenciaGoceSueldo, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class FormatoPagoViaticoPDF(View):

    def get(self, request, pk):
        item = FormatoPagoViatico.objects.get(pk=pk)
        print(pk)
        print(item)
        context = {
            'content': item
        }
        template = get_template('pago_viaticos.tex')

        rendered_tpl = template.render(context).encode('utf-8')
        print(rendered_tpl)

        with tempfile.TemporaryDirectory() as tempdir:
            for i in range(2):
                process = Popen(
                    ['pdflatex', '-output-directory', tempdir],
                    stdin=PIPE,
                    stdout=PIPE,
                )
                process.communicate(rendered_tpl)
            with open(os.path.join(tempdir, 'texput.pdf'), 'rb') as f:
                pdf = f.read()

        r = HttpResponse(content_type='application/pdf')
        r.write(pdf)
        return r
