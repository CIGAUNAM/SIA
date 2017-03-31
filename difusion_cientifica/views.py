from django.shortcuts import render

# Create your views here.

class ArticuloCientificoJSON(View):
    otros = False
    def get(self, request):

        try:
            usuarioid = User.objects.get(username=request.user.username).id
            if self.otros:
                articulos = ArticuloCientifico.objects.all().exclude(usuarios__id__exact=usuarioid)
            else:
                articulos = ArticuloCientifico.objects.filter(usuarios__id__exact=usuarioid)
            json = serializers.serialize('json', articulos, use_natural_foreign_keys=True,
                                         fields=('titulo', 'tipo', 'revista', 'status', 'fecha'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ArticuloCientificoLista(ObjectCreateVarMixin, View):
    form_class = ArticuloCientificoForm
    model = ArticuloCientifico
    aux = ArticuloCientificoContext.contexto
    template_name = 'main_otros.html'


class ArticuloCientificoDetalle(ObjectUpdateVarMixin, View):
    form_class = ArticuloCientificoForm
    model = ArticuloCientifico
    aux = ArticuloCientificoContext.contexto
    template_name = 'main_otros.html'