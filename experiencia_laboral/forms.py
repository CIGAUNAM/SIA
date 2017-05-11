from SIA.widgets import *
from . models import *
from django import forms
from nucleo.models import *
#

class ExperienciaLaboralForm(forms.ModelForm):
    dependencia = forms.ModelChoiceField(Dependencia.objects.all().order_by('dependencia'), widget=wSelectSingle, required=True)
    nombramiento = forms.ModelChoiceField(Nombramiento.objects.all().order_by('nombramiento'), widget=wSelectSingle, required=False)
    es_nombramiento_definitivo = forms.BooleanField()
    cargo = forms.ModelChoiceField(Cargo.objects.all().order_by('nombre'), widget=wSelectSingle, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    fecha_inicio = forms.CharField(widget=wDateField, required=True)
    fecha_fin = forms.CharField(widget=wDateField, required=False)

    class Meta:
        model = ExperienciaLaboral
        exclude = ['usuario', ]


class LineaInvestigacionForm(forms.ModelForm):
    linea_investigacion = forms.CharField(widget=wCharField, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    dependencia = forms.ModelChoiceField(Dependencia.objects.all().order_by('dependencia'), widget=wSelectSingle, required=True)
    fecha_inicio = forms.CharField(widget=wDateField, required=True)
    fecha_fin = forms.CharField(widget=wDateField, required=False)

    class Meta:
        model = LineaInvestigacion
        exclude = ['usuario', ]


class CapacidadPotencialidadForm(forms.ModelForm):
    competencia = forms.CharField(widget=wCharField, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    fecha_inicio = forms.CharField(widget=wDateField, required=True)
    fecha_fin = forms.CharField(widget=wDateField, required=False)

    class Meta:
        model = CapacidadPotencialidad
        exclude = ['usuario', ]
