from SIA.widgets import *
from .models import *

from django import forms
from django_select2.forms import Select2MultipleWidget, ModelSelect2Widget

#

class CargoAcademicoAdministrativoForm(forms.ModelForm):
    cargo = forms.ModelChoiceField(
        queryset=Cargo.objects.all(),
        label="Cargo",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Cargo.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}), required=False)
    dependencia = forms.ModelChoiceField(
        queryset=Dependencia.objects.all(),
        label="Dependencia",
        widget=ModelSelect2Widget(
            search_fields=['nombre_dependencia__icontains'],
            queryset=Dependencia.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    fecha_inicio = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    fecha_fin = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)

    class Meta:
        model = CargoAcademicoAdministrativo
        exclude = ['usuario', ]


class RepresentacionOrganoColegiadoForm(forms.ModelForm):
    representacion = forms.ModelChoiceField(
        queryset=Representacion.objects.all(),
        label="Representación",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Representacion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}), required=False)
    dependencia = forms.ModelChoiceField(
        queryset=Dependencia.objects.all(),
        label="Dependencia",
        widget=ModelSelect2Widget(
            search_fields=['nombre_dependencia__icontains'],
            queryset=Dependencia.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    fecha_inicio = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    fecha_fin = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)

    class Meta:
        model = RepresentacionOrganoColegiado
        exclude = ['usuario', ]


class ComisionAcademicaForm(forms.ModelForm):
    comision_academica = forms.ModelChoiceField(
        queryset=Comision.objects.all(),
        label="Comisión",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Comision.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}), required=False)
    es_evaluacion = forms.BooleanField(required=False)
    fecha_inicio = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    fecha_fin = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    dependencia = forms.ModelChoiceField(
        queryset=Dependencia.objects.all(),
        label="Dependencia",
        widget=ModelSelect2Widget(
            search_fields=['nombre_dependencia__icontains'],
            queryset=Dependencia.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )

    class Meta:
        model = ComisionAcademica
        exclude = ['usuario', ]


class ApoyoTecnicoForm(forms.ModelForm):
    actividad_apoyo = forms.ModelChoiceField(
        queryset=ActividadApoyo.objects.all(),
        label="Actividad de apoyo",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=ActividadApoyo.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}), required=False)
    dependencia = forms.ModelChoiceField(
        queryset=Dependencia.objects.all(),
        label="Dependencia",
        widget=ModelSelect2Widget(
            search_fields=['nombre_dependencia__icontains'],
            queryset=Dependencia.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    fecha_inicio = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    fecha_fin = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)

    class Meta:
        model = ApoyoTecnico
        exclude = ['usuario', ]


class ApoyoOtraActividadForm(forms.ModelForm):
    actividad_apoyo = forms.ModelChoiceField(
        queryset=ActividadApoyo.objects.all(),
        label="Actividad de apoyo",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=ActividadApoyo.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}), required=False)
    dependencia = forms.ModelChoiceField(
        queryset=Dependencia.objects.all(),
        label="Dependencia",
        widget=ModelSelect2Widget(
            search_fields=['nombre_dependencia__icontains'],
            queryset=Dependencia.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    fecha_inicio = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    fecha_fin = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)

    class Meta:
        model = ApoyoOtraActividad
        exclude = ['usuario', ]


class RepresentacionForm(forms.ModelForm):
    class Meta:
        model = Representacion
        exclude = []
        widgets = {
            'nombre_dependencia': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion_dependencia': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
        }


class ComisionForm(forms.ModelForm):
    class Meta:
        model = Comision
        exclude = []
        widgets = {
            'nombre_dependencia': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion_dependencia': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
        }


class ActividadApoyoForm(forms.ModelForm):
    class Meta:
        model = ActividadApoyo
        exclude = []
        widgets = {
            'nombre_dependencia': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion_dependencia': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
        }