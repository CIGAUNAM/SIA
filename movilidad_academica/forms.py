from SIA.widgets import *
from . models import *

from django import forms

#

class MovilidadAcademicaForm(forms.ModelForm):
    academico = forms.ModelChoiceField(User.objects.all().order_by('first_name'), widget=wSelectSingle, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    dependencia = forms.ModelChoiceField(Dependencia.objects.all().order_by('dependencia'), widget=wSelectSingle, required=True)
    actividades = forms.CharField(widget=wTextarea, required=False)
    fecha_inicio = forms.CharField(widget=wDateField, required=True)
    fecha_fin = forms.CharField(widget=wDateField, required=True)
    intercambio_unam = forms.BooleanField(required=False)
    financiamiento = forms.ModelChoiceField(Financiamiento.objects.all().order_by('programa'), widget=wSelectSingle, required=True)
    proyecto_investigacion = forms.ModelChoiceField(Proyecto.objects.all().order_by('nombre_proyecto'), widget=wSelectSingle, required=True)

    class Meta:
        model = MovilidadAcademica
        exclude = ['tipo', 'usuario', 'tags', ]