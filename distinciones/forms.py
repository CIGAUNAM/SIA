from SIA.widgets import *
from . models import *
from django import forms

from nucleo.models import Institucion
from django_select2.forms import Select2MultipleWidget

#

class DistincionAcademicoForm(forms.ModelForm):
    distincion = forms.ModelChoiceField(
        queryset=Distincion.objects.all(),
        label="Distincion",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    institucion = forms.ModelChoiceField(
        required=False,
        queryset=Institucion.objects.all(),
        label="Institución",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
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
    ambito = forms.ChoiceField(widget=Select3Widget, choices=getattr(settings, 'DISTINCION__AMBITO', ), required=True)
    fecha = forms.DateField(widget=wDateField, required=True)

    class Meta:
        model = DistincionAcademico
        exclude = []
        widgets = {
            'condecorados': Select3MultipleWidget,
        }


class DistincionAlumnoForm(forms.ModelForm):
    distincion = forms.ModelChoiceField(
        queryset=Distincion.objects.all(),
        label="Distincion",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    alumno = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Alumno",
        widget=ModelSelect3Widget(
            search_fields=['first_name__icontains', 'last_name__icontains', 'username__icontains'],
        )
    )
    grado_academico = forms.ChoiceField(widget=Select3Widget, choices=getattr(settings, 'GRADO_ACADEMICO', ), required=True)
    institucion = forms.ModelChoiceField(
        required=False,
        queryset=Institucion.objects.all(),
        label="Institución",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
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
    ambito = forms.ChoiceField(widget=Select3Widget, choices=getattr(settings, 'DISTINCION__AMBITO', ), required=True)
    fecha = forms.DateField(widget=wDateField, required=True)

    class Meta:
        model = DistincionAlumno
        exclude = []
        widgets = {
            'tutores': Select3MultipleWidget,
        }