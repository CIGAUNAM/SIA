from SIA.widgets import *
from .models import *
from django import forms
from nucleo.models import *
from django_select2.forms import ModelSelect2Widget

#

class ExperienciaLaboralForm(forms.ModelForm):
    institucion = forms.ModelChoiceField(
        required=True,
        queryset=Institucion.objects.all(),
        label="Institución",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'], queryset=Institucion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}

        )
    )
    dependencia = forms.ModelChoiceField(
        queryset=Dependencia.objects.all(),
        label="Dependencia",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'], queryset=Dependencia.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'},
            dependent_fields={'institucion': 'institucion'},
        )
    )
    nombramiento = forms.ModelChoiceField(
        required=False,
        queryset=Nombramiento.objects.all(),
        label="Nombramiento",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'], queryset=Nombramiento.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    es_nombramiento_definitivo = forms.BooleanField(label='Es nombramiento definitivo', required=False)
    cargo = forms.ModelChoiceField(
        queryset=Cargo.objects.all(),
        label="Cargo",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'], queryset=Cargo.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}), required=False, label='Descripción')
    fecha_inicio = forms.DateField(widget=wDateInput(attrs={'data-provide': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True, label='Fecha de inicio')
    fecha_fin = forms.DateField(widget=wDateInput(attrs={'data-provide': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=False, label='Fecha de finalización')

    class Meta:
        model = ExperienciaLaboral
        exclude = ['usuario', ]


class LineaInvestigacionForm(forms.ModelForm):
    linea_investigacion = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True, label='Línea de investigación')
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}), required=False, label='Descripción')
    institucion = forms.ModelChoiceField(
        queryset=Institucion.objects.all(),
        label="Institución",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'], queryset=Institucion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    dependencia = forms.ModelChoiceField(
        queryset=Dependencia.objects.all(),
        label="Dependencia",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'], queryset=Dependencia.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'},
            dependent_fields={'institucion': 'institucion'}
        )
    )
    fecha_inicio = forms.DateField(widget=wDateInput(attrs={'data-provide': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True, label='Fecha de inicio')
    fecha_fin = forms.DateField(widget=wDateInput(attrs={'data-provide': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=False, label='Fecha de finalización')

    class Meta:
        model = LineaInvestigacion
        exclude = ['usuario', ]


class CapacidadPotencialidadForm(forms.ModelForm):
    nombre = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True, label='Capacidad o Potencialidad')
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}), required=False, label='Descripción')
    fecha_inicio = forms.DateField(widget=wDateInput(attrs={'data-provide': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True, label='Fecha de inicio')
    fecha_fin = forms.DateField(widget=wDateInput(attrs={'data-provide': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=False, label='Fecha de finalización')

    class Meta:
        model = CapacidadPotencialidad
        exclude = ['usuario', ]
