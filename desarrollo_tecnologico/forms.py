from SIA.widgets import *
from .models import *
from django import forms

from django_select2.forms import Select2MultipleWidget, ModelSelect2Widget

#

class DesarrolloTecnologicoForm(forms.ModelForm):
    nombre = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}), required=True)
    version = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False)
    patente = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False)
    licencia = forms.ModelChoiceField(
        required=False,
        queryset=Licencia.objects.all(),
        label="Licencia",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Licencia.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    url = forms.URLField(widget=URLInput(attrs={'class': 'form-control pull-right'}), required=False)
    fecha = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    proyecto = forms.ModelChoiceField(
        required=False,
        queryset=ProyectoInvestigacion.objects.all(),
        label="Proyecto",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=ProyectoInvestigacion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )

    class Meta:
        model = DesarrolloTecnologico
        exclude = []
        widgets = {
            'autores': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class LicenciaForm(forms.ModelForm):
    nombre = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}), required=False)
    url = forms.URLField(widget=URLInput(attrs={'class': 'form-control pull-right'}), required=False)

    class Meta:
        model = Licencia
        exclude = []
