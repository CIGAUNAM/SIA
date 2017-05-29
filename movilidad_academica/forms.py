from SIA.widgets import *
from . models import *

from django import forms
from nucleo.models import Institucion
from django_select2.forms import Select2MultipleWidget

#

class MovilidadAcademicaForm(forms.ModelForm):
    academico = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Académico",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            #dependent_fields={'dependencia': 'dependencia'},
        )
    )
    descripcion = forms.CharField(widget=wTextarea, required=False)
    institucion = forms.ModelChoiceField(
        required=False,
        queryset=Institucion.objects.all(),
        label="Institución",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            #dependent_fields={'dependencia': 'dependencia'},
        )
    )
    dependencia = forms.ModelChoiceField(
        queryset=Dependencia.objects.all(),
        label="Dependencia",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            dependent_fields={'institucion': 'institucion'},
            max_results=500,
        )
    )
    actividades = forms.CharField(widget=wTextarea, required=True)
    fecha_inicio = forms.CharField(widget=wDateField, required=True)
    fecha_fin = forms.CharField(widget=wDateField, required=True)
    intercambio_unam = forms.BooleanField(required=False, label='Es intercambio UNAM')
    financiamiento = forms.ModelChoiceField(
        queryset=Financiamiento.objects.all(),
        label="Financiamiento",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            #dependent_fields={'dependencia': 'dependencia'},
        )
    )
    proyecto_investigacion = forms.ModelChoiceField(
        queryset=Proyecto.objects.all(),
        label="Proyecto de investigación",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            #dependent_fields={'dependencia': 'dependencia'},
        )
    )

    class Meta:
        model = MovilidadAcademica
        exclude = ['tipo', 'usuario', ]
        widgets = {
            'redes_academicas': Select3MultipleWidget,
        }