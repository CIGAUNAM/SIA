from SIA.widgets import *
from . models import *
from django import forms

#

class DistincionAcademicoForm(forms.ModelForm):
    distincion = forms.ModelChoiceField(Distincion.objects.all().order_by('distincion'), widget=wSelectSingle, required=True)
    otorga = forms.ModelChoiceField(Dependencia.objects.all().order_by('dependencia'), widget=wSelectSingle, required=True)
    ambito = forms.ChoiceField(widget=wSelectSingle, choices=getattr(settings, 'DISTINCION__AMBITO', ), required=True)
    fecha = forms.CharField(widget=wDateField, required=True)

    class Meta:
        model = DistincionAcademico
        exclude = []


class DistincionAlumnoForm(forms.ModelForm):
    distincion = forms.ModelChoiceField(Distincion.objects.all().order_by('distincion'), widget=wSelectSingle, required=True)
    alumno = forms.ModelChoiceField(User.objects.all().order_by('first_name'), widget=wSelectSingle, required=True)
    grado_academico = forms.ChoiceField(widget=wSelectSingle, choices=getattr(settings, 'GRADO_ACADEMICO', ), required=True)
    otorga = forms.ModelChoiceField(Dependencia.objects.all().order_by('dependencia'), widget=wSelectSingle, required=True)
    ambito = forms.ChoiceField(widget=wSelectSingle, choices=getattr(settings, 'DISTINCION__AMBITO', ), required=True)
    fecha = forms.CharField(widget=wDateField, required=True)

    class Meta:
        model = DistincionAlumno
        exclude = []