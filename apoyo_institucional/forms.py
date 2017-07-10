from SIA.widgets import *
from .models import *

from django import forms
from django_select2.forms import Select2MultipleWidget

#

class CargoAcademicoAdministrativoForm(forms.ModelForm):
    cargo = forms.ModelChoiceField(
        queryset=Cargo.objects.all(),
        label="Cargo",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    descripcion = forms.CharField(widget=wTextarea, required=False)
    institucion = forms.ModelChoiceField(
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
    fecha_inicio = forms.CharField(widget=wDateField, required=True)
    fecha_fin = forms.CharField(widget=wDateField, required=True)

    class Meta:
        model = CargoAcademicoAdministrativo
        exclude = ['usuario', ]


class RepresentacionOrganoColegiadoForm(forms.ModelForm):
    representacion = forms.ModelChoiceField(
        queryset=Representacion.objects.all(),
        label="Representación",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    descripcion = forms.CharField(widget=wTextarea, required=False)
    institucion = forms.ModelChoiceField(
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
    fecha_inicio = forms.CharField(widget=wDateField, required=True)
    fecha_fin = forms.CharField(widget=wDateField, required=True)

    class Meta:
        model = RepresentacionOrganoColegiado
        exclude = ['usuario', ]


class ComisionAcademicaForm(forms.ModelForm):
    comision_academica = forms.ModelChoiceField(
        queryset=Comision.objects.all(),
        label="Comisión",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    descripcion = forms.CharField(widget=wTextarea, required=False)
    es_evaluacion = forms.BooleanField(required=False)
    fecha_inicio = forms.CharField(widget=wDateField, required=True)
    fecha_fin = forms.CharField(widget=wDateField, required=True)
    institucion = forms.ModelChoiceField(
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

    class Meta:
        model = ComisionAcademica
        exclude = ['usuario', ]



class ApoyoTecnicoForm(forms.ModelForm):
    actividad_apoyo = forms.ModelChoiceField(
        queryset=ActividadApoyo.objects.all(),
        label="Actividad de apoyo",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    descripcion = forms.CharField(widget=wTextarea, required=False)
    institucion = forms.ModelChoiceField(
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
    fecha_inicio = forms.CharField(widget=wDateField, required=True)
    fecha_fin = forms.CharField(widget=wDateField, required=True)

    class Meta:
        model = ApoyoTecnico
        exclude = ['usuario', ]


class ApoyoOtraActividadForm(forms.ModelForm):
    actividad_apoyo = forms.ModelChoiceField(
        queryset=ActividadApoyo.objects.all(),
        label="Actividad de apoyo",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    descripcion = forms.CharField(widget=wTextarea, required=False)
    institucion = forms.ModelChoiceField(
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
    fecha_inicio = forms.CharField(widget=wDateField, required=True)
    fecha_fin = forms.CharField(widget=wDateField, required=True)

    class Meta:
        model = ApoyoOtraActividad
        exclude = ['usuario', ]


class RepresentacionForm(forms.ModelForm):
    class Meta:
        model = Representacion
        exclude = []
        widgets = {
            'nombre': wCharField,
            'descripcion': wTextarea,
        }


class ComisionForm(forms.ModelForm):
    class Meta:
        model = Comision
        exclude = []
        widgets = {
            'nombre': wCharField,
            'descripcion': wTextarea,
        }


class ActividadApoyoForm(forms.ModelForm):
    class Meta:
        model = ActividadApoyo
        exclude = []
        widgets = {
            'nombre': wCharField,
            'descripcion': wTextarea,
        }