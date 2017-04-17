from . models import *
from django import forms

#

class DesarrolloTecnologicoForm(forms.ModelForm):
    class Meta:
        model = DesarrolloTecnologico
        exclude = []