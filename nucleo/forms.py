from . models import *
from django import forms
from django.core.exceptions import ValidationError

from SIA.widgets import *

#


"""
class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        exclude = []

    def clean_tag(self):
        return self.cleaned_data['tag'].lower()
"""


class ZonaPaisForm(forms.ModelForm):
    class Meta:
        model = ZonaPais
        exclude = []


class PaisForm(forms.ModelForm):
    class Meta:
        model = Pais
        exclude = []


class EstadoForm(forms.ModelForm):
    class Meta:
        model = Estado
        exclude = []


class CiudadForm(forms.ModelForm):
    class Meta:
        model = Ciudad
        exclude = []


class InstitucionForm(forms.ModelForm):
    pais = forms.ModelChoiceField(
        queryset=Pais.objects.all(),
        label="País",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    class Meta:
        model = Institucion
        exclude = []
        widgets = {
            'nombre': wCharField,
            'descripcion': wTextarea,
        }


class DependenciaForm(forms.ModelForm):
    class Meta:
        model = Dependencia
        exclude = []


class DepartamentoForm(forms.ModelForm):
    class Meta:
        model = Departamento
        exclude = []


class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        exclude = []


class NombramientoForm(forms.ModelForm):
    class Meta:
        model = Nombramiento
        exclude = []


class AreaConocimientoForm(forms.ModelForm):
    class Meta:
        model = AreaConocimiento
        exclude = []


class AreaEspecialidadForm(forms.ModelForm):
    class Meta:
        model = AreaEspecialidad
        exclude = []


class ImpactoSocialForm(forms.ModelForm):
    class Meta:
        model = ImpactoSocial
        exclude = []


#class ProgramaFinanciamientoForm(forms.ModelForm):
#    class Meta:
#        model = ProgramaFinanciamiento
#        exclude = []


class FinanciamientoForm(forms.ModelForm):
    class Meta:
        model = Financiamiento
        exclude = []


class MetodologiaForm(forms.ModelForm):
    class Meta:
        model = Metodologia
        exclude = []


class BecaForm(forms.ModelForm):
    class Meta:
        model = Beca
        exclude = []


class ReconocimientoForm(forms.ModelForm):
    class Meta:
        model = Reconocimiento
        exclude = []

"""
class TesisForm(forms.ModelForm):
    class Meta:
        model = DireccionTesis
        exclude = []
"""

class ProgramaLicenciaturaForm(forms.ModelForm):
    class Meta:
        model = ProgramaLicenciatura
        exclude = []


class ProgramaMaestriaForm(forms.ModelForm):
    class Meta:
        model = ProgramaMaestria
        exclude = []


class ProgramaDoctoradoForm(forms.ModelForm):
    class Meta:
        model = ProgramaDoctorado
        exclude = []


class TipoEventoForm(forms.ModelForm):
    class Meta:
        model = TipoEvento
        exclude = []


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        exclude = []


class DistincionForm(forms.ModelForm):
    class Meta:
        model = Distincion
        exclude = []


class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        exclude = []

