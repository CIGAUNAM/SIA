from .permissions import IsOwnerOrReadOnly
from rest_framework import permissions
from formacion_academica.serializers import *
from rest_framework import generics
from django.views.generic import View
from django.core import serializers
from SIA.utils import *
from .forms import *
from .utils import *
from nucleo.forms import *

# Create your views here.


class CursoEspecializacionJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            cursos = CursoEspecializacion.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', cursos,
                                         fields=('nombre', 'tipo', 'horas', 'dependencia', 'fecha_fin'),
                                         use_natural_foreign_keys=True)
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404



class CursoEspecializacionLista(ObjectCreateMixin, View):
    form_class = CursoEspecializacionForm
    model = CursoEspecializacion
    aux = CursoEspecializacionContext.contexto
    template_name = 'cursos_especializacion.html'


class CursoEspecializacionDetalle(ObjectUpdateMixin, View):
    form_class = CursoEspecializacionForm
    model = CursoEspecializacion
    aux = CursoEspecializacionContext.contexto
    template_name = 'cursos_especializacion.html'


class CursoEspecializacionEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(CursoEspecializacion, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class LicenciaturaJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            licenciaturas = Licenciatura.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', licenciaturas,
                                         fields=('carrera', 'titulo_tesis', 'fecha_grado', 'dependencia'),
                                         use_natural_foreign_keys=True)
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class LicenciaturaLista(ObjectCreateMixin, View):
    form_class = LicenciaturaForm
    model = Licenciatura
    aux = LicenciaturaContext.contexto
    template_name = 'licenciaturas.html'


class LicenciaturaDetalle(ObjectUpdateMixin, View):
    form_class = LicenciaturaForm
    model = Licenciatura
    aux = LicenciaturaContext.contexto
    template_name = 'licenciaturas.html'


class LicenciaturaEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(Licenciatura, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class MaestriaJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            maestrias = Maestria.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', maestrias,
                                         fields=('programa', 'titulo_tesis', 'fecha_grado', 'dependencia'),
                                         use_natural_foreign_keys=True)
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class MaestriaLista(ObjectCreateMixin, View):
    form_class = MaestriaForm
    model = Maestria
    aux = MaestriaContext.contexto
    template_name = 'maestrias.html'


class MaestriaDetalle(ObjectUpdateMixin, View):
    form_class = MaestriaForm
    model = Maestria
    aux = MaestriaContext.contexto
    template_name = 'maestrias.html'


class MaestriaEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(Maestria, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class DoctoradoJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            maestrias = Doctorado.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', maestrias,
                                         fields=('programa', 'titulo_tesis', 'fecha_grado', 'dependencia'),
                                         use_natural_foreign_keys=True)
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class DoctoradoLista(ObjectCreateMixin, View):
    form_class = DoctoradoForm
    model = Doctorado
    aux = DoctoradoContext.contexto
    template_name = 'doctorados.html'


class DoctoradoDetalle(ObjectUpdateMixin, View):
    form_class = DoctoradoForm
    model = Doctorado
    aux = DoctoradoContext.contexto
    template_name = 'doctorados.html'


class DoctoradoEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(Doctorado, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class PostDoctoradoJSON(View):
    def get(self, request):
        try:
            usuarioid = User.objects.get(username=request.user.username).id
            maestrias = PostDoctorado.objects.filter(usuario=usuarioid)
            json = serializers.serialize('json', maestrias,
                                         fields=('nombre', 'area_conocimiento', 'fecha_fin', 'proyecto', 'dependencia'),
                                         use_natural_foreign_keys=True)
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404


class PostDoctoradoLista(ObjectCreateMixin, View):
    form_class = PostDoctoradoForm
    model = PostDoctorado
    aux = PostDoctoradoContext.contexto
    template_name = 'post_doctorados.html'


class PostDoctoradoDetalle(ObjectUpdateMixin, View):
    form_class = PostDoctoradoForm
    model = PostDoctorado
    aux = PostDoctoradoContext.contexto
    template_name = 'post_doctorados.html'


class PostDoctoradoEliminar(View):
    def get(self, request, pk):
        try:
            item = get_object_or_404(PostDoctorado, pk=pk, usuario=request.user)
            item.delete()
            return redirect('../')
        except:
            raise Http404


class LicenciaturaLista1(View, LicenciaturaContext):
    form_class = LicenciaturaForm

    def get(self, request):
        return render(request, 'licenciaturas.html',
                      {'active': 'lista', 'plantilla': self.contexto, 'form': self.form_class})

    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            nueva_licenciatura = bound_form.save(commit=False)
            nueva_licenciatura.usuario = request.user
            nueva_licenciatura = bound_form.save()

            return redirect(nueva_licenciatura)
        else:
            return render(request, 'licenciaturas.html',
                          {'active': 'agregar', 'plantilla': self.contexto, 'form': bound_form})


class LicenciaturaDetalle1(View, LicenciaturaContext):
    form_class = LicenciaturaForm
    model = Licenciatura

    def get(self, request, pk):
        objeto = get_object_or_404(self.model, pk=pk, usuario=request.user)
        context = {'active': 'detalle', 'plantilla': self.contexto, 'form': self.form_class(instance=objeto),
                   'objeto': objeto}
        return render(request, 'licenciaturas.html', context)

    def post(self, request, pk):
        objeto = get_object_or_404(self.model, pk=pk, usuario=request.user)
        bound_form = self.form_class(request.POST, instance=objeto)

        if bound_form.is_valid():
            detalle_curso = bound_form.save(commit=False)
            detalle_curso.usuario = request.user
            detalle_curso = bound_form.save()
            return redirect(detalle_curso)
        else:
            return render(request, 'licenciaturas.html',
                          {'active': 'detalle', 'plantilla': self.contexto, 'form': bound_form})

    def get_update_url(self):
        return reverse('licenciatura_detalle', kwargs={'pk': self.form_class.pk})


class CursoEspecializacionList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = CursoEspecializacion.objects.all()
    serializer_class = CursoEspecializacionSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class CursoEspecializacionDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = CursoEspecializacion.objects.all()
    serializer_class = CursoEspecializacionSerializer


class LicenciaturaList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = Licenciatura.objects.all()
    serializer_class = LicenciaturaSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class LicenciaturaDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = Licenciatura.objects.all()
    serializer_class = LicenciaturaSerializer


class MaestriaList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = Maestria.objects.all()
    serializer_class = MaestriaSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class MaestriaDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = Maestria.objects.all()
    serializer_class = MaestriaSerializer


class DoctoradoList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = Doctorado.objects.all()
    serializer_class = DoctoradoSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class DoctoradoDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = Doctorado.objects.all()
    serializer_class = DoctoradoSerializer


class PostDoctoradoList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = PostDoctorado.objects.all()
    serializer_class = PostDoctoradoSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class PostDoctoradoDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = PostDoctorado.objects.all()
    serializer_class = PostDoctoradoSerializer
