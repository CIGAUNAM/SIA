from SIA.widgets import *
from .models import *
from django import forms

from django_select2.forms import Select2MultipleWidget


#

class DesarrolloTecnologicoForm(forms.ModelForm):
    nombre = forms.CharField(widget=wCharField, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    version = forms.CharField(widget=wCharField, required=True)
    patente = forms.CharField(widget=wCharField, required=True)
    licencia = forms.ModelChoiceField(
        queryset=Licencia.objects.all(),
        label="Licencia",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            # dependent_fields={'dependencia': 'dependencia'},
        )
    )
    url = forms.CharField(widget=wCharField, required=False)  # corregir valiadr url
    fecha = forms.CharField(widget=wDateField, required=True)
    proyecto = forms.ModelChoiceField(
        required=False,
        queryset=Proyecto.objects.all(),
        label="Proyecto",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            # dependent_fields={'dependencia': 'dependencia'},
        )
    )

    class Meta:
        model = DesarrolloTecnologico
        exclude = []
        widgets = {
            'autores': Select3MultipleWidget,
            # 'agradecimientos': Select3MultipleWidget,
        }


class LicenciaForm(forms.ModelForm):
    nombre = forms.CharField(widget=wCharField, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    url = forms.CharField(widget=wCharField, required=False)  # corregir valiadr url

    class Meta:
        model = Licencia
        exclude = []
