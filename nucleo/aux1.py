class ProyectoJSON(View):
    def get(self, request):
        try:
            #usuarioid = User.objects.get(username=request.user.username).id
            items = Proyecto.objects.all()
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('nombre', 'estado'))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class ProyectoLista(ObjectCreateMixinNucleo, View):
    form_class = ProyectoForm
    model = Proyecto
    aux = ProyectoContext.contexto
    template_name = 'main.html'


class ProyectoDetalle(ObjectUpdateMixinNucleo, View):
    form_class = ProyectoForm
    model = Proyecto
    aux = ProyectoContext.contexto
    template_name = 'main.html'


class ProyectoEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(Proyecto, pk=pk)
            item.delete()
            return redirect('../')
        except:
            raise Http404