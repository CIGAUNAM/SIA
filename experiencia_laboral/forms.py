from SIA.widgets import *
from . models import *
from django import forms
from nucleo.models import *
#

class ExperienciaLaboralForm(forms.ModelForm):
    institucion = forms.ModelChoiceField(
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
    nombramiento = forms.ModelChoiceField(
        queryset=Nombramiento.objects.all(),
        label="Nombramiento",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    es_nombramiento_definitivo = forms.BooleanField(label='Es nombramiento definitivo', required=False)
    cargo = forms.ModelChoiceField(
        queryset=Cargo.objects.all(),
        label="Cargo",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    descripcion = forms.CharField(widget=wTextarea, required=False, label='Descripción')
    fecha_inicio = forms.CharField(widget=wDateField, required=True, label='Fecha de inicio')
    fecha_fin = forms.CharField(widget=wDateField, required=False, label='Fecha de finalización')

    class Meta:
        model = ExperienciaLaboral
        exclude = ['usuario', ]


class LineaInvestigacionForm(forms.ModelForm):
    linea_investigacion = forms.CharField(widget=wCharField, required=True, label='Línea de investigación')
    descripcion = forms.CharField(widget=wTextarea, required=False, label='Descripción')
    institucion = forms.ModelChoiceField(
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
    fecha_inicio = forms.CharField(widget=wDateField, required=True, label='Fecha de inicio')
    fecha_fin = forms.CharField(widget=wDateField, required=False, label='Fecha de finalización')

    class Meta:
        model = LineaInvestigacion
        exclude = ['usuario', ]


class CapacidadPotencialidadForm(forms.ModelForm):
    nombre = forms.CharField(widget=wCharField, required=True, label='Capacidad o Potencialidad')
    descripcion = forms.CharField(widget=wTextarea, required=False, label='Descripción')
    fecha_inicio = forms.CharField(widget=wDateField, required=True, label='Fecha de inicio')
    fecha_fin = forms.CharField(widget=wDateField, required=False, label='Fecha de finalización')

    class Meta:
        model = CapacidadPotencialidad
        exclude = ['usuario', ]
