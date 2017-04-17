from . models import *
from django import forms

#

class AsesorEstanciaForm(forms.ModelForm):
    class Meta:
        model = AsesorEstancia
        exclude = ['usuario',]


class DireccionTesisForm(forms.ModelForm):
    class Meta:
        model = DireccionTesis
        exclude = ['usuario',]


class ComiteTutoralForm(forms.ModelForm):
    class Meta:
        model = ComiteTutoral
        exclude = []


class ComiteCandidaturaDoctoralForm(forms.ModelForm):
    class Meta:
        model = ComiteCandidaturaDoctoral
        exclude = []