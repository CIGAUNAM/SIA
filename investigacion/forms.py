from . models import *
from nucleo.models import Libro as LibroInvestigacion
from django import forms

#

class ArticuloCientificoForm(forms.ModelForm):
    class Meta:
        model = ArticuloCientifico
        exclude = ['tags', ]


class CapituloLibroInvestigacionForm(forms.ModelForm):
    class Meta:
        model = CapituloLibroInvestigacion
        exclude = ['tags', ]


class MapaArbitradoForm(forms.ModelForm):
    class Meta:
        model = MapaArbitrado
        exclude = ['tags', ]


class InformeTecnicoForm(forms.ModelForm):
    class Meta:
        model = InformeTecnico
        exclude = ['tags', ]


class LibroInvestigacionForm(forms.ModelForm):
    class Meta:
        model = LibroInvestigacion
        exclude = ['tipo', 'tags', ]