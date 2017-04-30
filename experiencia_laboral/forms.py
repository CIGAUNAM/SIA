from SIA.widgets import *
from . models import *
from django import forms
from nucleo.models import *
#

class ExperienciaLaboralForm(forms.ModelForm):
    dependencia = forms.ModelChoiceField(Dependencia.objects.all().order_by('dependencia'), widget=wSelectSingle)
    nombramiento = forms.ModelChoiceField(Nombramiento.objects.all().order_by('nombramiento'), widget=wSelectSingle)
    es_nombramiento_definitivo = forms.BooleanField()
    cargo = forms.ModelChoiceField(Cargo.objects.all().order_by('cargo'), widget=wSelectSingle)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    fecha_inicio = forms.CharField(widget=wDateField)
    fecha_fin = forms.CharField(widget=wDateField)

    class Meta:
        model = ExperienciaLaboral
        exclude = ['usuario', 'tags', ]


class LineaInvestigacionForm(forms.ModelForm):
    linea_investigacion = forms.CharField(widget=wCharField)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    dependencia = forms.ModelChoiceField(Dependencia.objects.all().order_by('dependencia'), widget=wSelectSingle)
    fecha_inicio = forms.CharField(widget=wDateField)
    fecha_fin = forms.CharField(widget=wDateField)

    class Meta:
        model = LineaInvestigacion
        exclude = ['usuario', 'tags', ]


class CapacidadPotencialidadForm(forms.ModelForm):
    competencia = forms.CharField(widget=wCharField)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    fecha_inicio = forms.CharField(widget=wDateField)
    fecha_fin = forms.CharField(widget=wDateField)

    class Meta:
        model = CapacidadPotencialidad
        exclude = ['usuario', 'tags', ]
