from SIA.widgets import *
from . models import *
from django import forms

#

class DesarrolloTecnologicoForm(forms.ModelForm):
    nombre_desarrollo_tecnologico = forms.CharField(widget=wCharField, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    version = forms.CharField(widget=wCharField, required=True)
    patente = forms.CharField(widget=wCharField, required=True)
    licencia = forms.ModelChoiceField(Licencia.objects.all(), widget=wSelectSingle, required=True)
    url = forms.CharField(widget=wCharField, required=False)  # corregir valiadr url
    fecha = forms.CharField(widget=wDateField, required=True)

    class Meta:
        model = DesarrolloTecnologico
        exclude = []