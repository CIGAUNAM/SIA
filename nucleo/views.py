from django.shortcuts import render
from django.http import HttpResponse

from nucleo.models import *
from nucleo.serializers import *
from rest_framework import generics
from . permissions import IsOwnerOrReadOnly, UserListReadOnly, IsAdminUserOrReadOnly
from rest_framework import permissions



def inicio(request):
    return render(request=request, context=None, template_name='dashboard.html')







class TagLista(generics.ListCreateAPIView):

    def get(self):
        return Tag.objects.all()


class TagList(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ZonaPaisList(generics.ListCreateAPIView):
    queryset = ZonaPais.objects.all()
    serializer_class = ZonaPaisSerializer

class ZonaPaisDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = ZonaPais.objects.all()
    serializer_class = ZonaPaisSerializer


class PaisList(generics.ListCreateAPIView):
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer

class PaisDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer


class EstadoList(generics.ListCreateAPIView):
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer

class EstadoDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer

class CiudadList(generics.ListCreateAPIView):
    queryset = Ciudad.objects.all()
    serializer_class = CiudadSerializer

class CiudadDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Ciudad.objects.all()
    serializer_class = CiudadSerializer


class UserList(generics.ListCreateAPIView):
    permission_classes = (UserListReadOnly,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUserOrReadOnly,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class InstitucionList(generics.ListCreateAPIView):
    queryset = Institucion.objects.all()
    serializer_class = InstitucionSerializer

class InstitucionDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Institucion.objects.all()
    serializer_class = InstitucionSerializer


class DependenciaList(generics.ListCreateAPIView):
    queryset = Dependencia.objects.all()
    serializer_class = DependenciaSerializer

class DependenciaDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Dependencia.objects.all()
    serializer_class = DependenciaSerializer


class CargoList(generics.ListCreateAPIView):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer

class CargoDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer


class NombramientoList(generics.ListCreateAPIView):
    permission_classes = (UserListReadOnly,)
    queryset = Nombramiento.objects.all()
    serializer_class = NombramientoSerializer

class NombramientoDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (UserListReadOnly,)
    queryset = Nombramiento.objects.all()
    serializer_class = NombramientoSerializer


class AreaConocimientoList(generics.ListCreateAPIView):
    permission_classes = (UserListReadOnly,)
    queryset = AreaConocimiento.objects.all()
    serializer_class = AreaConocimientoSerializer

class AreaConocimientoDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (UserListReadOnly,)
    queryset = AreaConocimiento.objects.all()
    serializer_class = AreaConocimientoSerializer


class AreaEspecialidadList(generics.ListCreateAPIView):
    queryset = AreaEspecialidad.objects.all()
    serializer_class = AreaEspecialidadSerializer

class AreaEspecialidadDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = AreaEspecialidad.objects.all()
    serializer_class = AreaEspecialidadSerializer


class ImpactoSocialList(generics.ListCreateAPIView):
    queryset = ImpactoSocial.objects.all()
    serializer_class = ImpactoSocialSerializer

class ImpactoSocialDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = ImpactoSocial.objects.all()
    serializer_class = ImpactoSocialSerializer


class FinanciamientoList(generics.ListCreateAPIView):
    queryset = Financiamiento.objects.all()
    serializer_class = FinanciamientoSerializer

class FinanciamientoDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Financiamiento.objects.all()
    serializer_class = FinanciamientoSerializer


class MetodologiaList(generics.ListCreateAPIView):
    queryset = Metodologia.objects.all()
    serializer_class = MetodologiaSerializer

class MetodologiaDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Metodologia.objects.all()
    serializer_class = MetodologiaSerializer


class ProgramaLicenciaturaList(generics.ListCreateAPIView):
    queryset = ProgramaLicenciatura.objects.all()
    serializer_class = ProgramaLicenciaturaSerializer

class ProgramaLicenciaturaDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = ProgramaLicenciatura.objects.all()
    serializer_class = ProgramaLicenciaturaSerializer


class ProgramaMaestriaList(generics.ListCreateAPIView):
    queryset = ProgramaMaestria.objects.all()
    serializer_class = ProgramaMaestriaSerializer

class ProgramaMaestriaDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = ProgramaMaestria.objects.all()
    serializer_class = ProgramaMaestriaSerializer


class ProgramaDoctoradoList(generics.ListCreateAPIView):
    queryset = ProgramaDoctorado.objects.all()
    serializer_class = ProgramaDoctoradoSerializer


class ProgramaDoctoradoDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = ProgramaDoctorado.objects.all()
    serializer_class = ProgramaDoctoradoSerializer


class ProyectoList(generics.ListCreateAPIView):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer

class ProyectoDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer

#@permission_classes((permissions.IsAuthenticatedOrReadOnly,))