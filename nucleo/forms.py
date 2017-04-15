from . models import *
from django import forms
from django.core.exceptions import ValidationError

#


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        exclude = ['slug', ]

    def clean_tag(self):
        return self.cleaned_data['tag'].lower()


class ZonaPaisForm(forms.ModelForm):
    class Meta:
        model = ZonaPais
        exclude = ['slug', ]


class PaisForm(forms.ModelForm):
    class Meta:
        model = Pais
        exclude = ['slug', ]


class EstadoForm(forms.ModelForm):
    class Meta:
        model = Estado
        exclude = ['slug', ]


class CiudadForm(forms.ModelForm):
    class Meta:
        model = Ciudad
        exclude = ['slug', ]


class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        exclude = ['slug', ]


class UbicacionForm(forms.ModelForm):
    class Meta:
        model = Ubicacion
        exclude = ['slug', ]


class InstitucionForm(forms.ModelForm):
    class Meta:
        model = Institucion
        exclude = ['slug', ]


class DependenciaForm(forms.ModelForm):
    class Meta:
        model = Dependencia
        exclude = ['slug', ]


class DepartamentoForm(forms.ModelForm):
    class Meta:
        model = Departamento
        exclude = ['slug', ]


class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        exclude = ['slug', ]


class NombramientoForm(forms.ModelForm):
    class Meta:
        model = Nombramiento
        exclude = ['slug', ]


class AreaConocimientoForm(forms.ModelForm):
    class Meta:
        model = AreaConocimiento
        exclude = ['slug', ]


class AreaEspecialidadForm(forms.ModelForm):
    class Meta:
        model = AreaEspecialidad
        exclude = ['slug', ]


class ImpactoSocialForm(forms.ModelForm):
    class Meta:
        model = ImpactoSocial
        exclude = ['slug', ]


class ProgramaFinanciamientoForm(forms.ModelForm):
    class Meta:
        model = ProgramaFinanciamiento
        exclude = ['slug', ]


class FinanciamientoForm(forms.ModelForm):
    class Meta:
        model = Financiamiento


class MetodologiaForm(forms.ModelForm):
    class Meta:
        model = Metodologia
        exclude = ['slug', ]


class BecaForm(forms.ModelForm):
    class Meta:
        model = Beca
        exclude = ['slug', ]


class ReconocimientoForm(forms.ModelForm):
    class Meta:
        model = Reconocimiento
        exclude = ['slug', ]


class TesisForm(forms.ModelForm):
    class Meta:
        model = DireccionTesis
        exclude = ['slug', ]


class ProgramaLicenciaturaForm(forms.ModelForm):
    class Meta:
        model = ProgramaLicenciatura
        exclude = ['slug', ]


class ProgramaMaestriaForm(forms.ModelForm):
    class Meta:
        model = ProgramaMaestria
        exclude = ['slug', ]


class ProgramaDoctoradoForm(forms.ModelForm):
    class Meta:
        model = ProgramaDoctorado
        exclude = ['slug', ]


class TipoEventoForm(forms.ModelForm):
    class Meta:
        model = TipoEvento
        exclude = ['slug', ]


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        exclude = ['slug', ]


class DistincionForm(forms.ModelForm):
    class Meta:
        model = Distincion
        exclude = ['slug', ]


class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        exclude = ['slug', ]

