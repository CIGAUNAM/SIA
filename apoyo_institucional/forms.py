from SIA.widgets import *
from . models import *

from django import forms

#

class CargoAcademicoAdministrativoForm(forms.ModelForm):
    cargo = forms.ModelChoiceField(Cargo.objects.all().order_by('nombre'), widget=wSelect, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    dependencia = forms.ModelChoiceField(Dependencia.objects.all().order_by('dependencia'), widget=wSelect, required=True)
    cargo_inicio = forms.CharField(widget=wDateField, required=True)
    cargo_fin = forms.CharField(widget=wDateField, required=True)

    class Meta:
        model = CargoAcademicoAdministrativo
        exclude = ['usuario', ]


class RepresentacionOrganoColegiadoForm(forms.ModelForm):
    representacion = forms.ModelChoiceField(Representacion.objects.all().order_by('representacion'), widget=wSelect, required=True)
    ante = forms.ModelChoiceField(Dependencia.objects.all().order_by('dependencia'), widget=wSelect, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    cargo_inicio = forms.CharField(widget=wDateField, required=True)
    cargo_fin = forms.CharField(widget=wDateField, required=True)

    class Meta:
        model = RepresentacionOrganoColegiado
        exclude = ['usuario', ]


class ComisionAcademicaForm(forms.ModelForm):
    comision_academica = forms.ModelChoiceField(Comision.objects.all().order_by('comision'), widget=wSelect, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    es_evaluacion = forms.BooleanField(required=False)
    fecha_inicio = forms.CharField(widget=wDateField, required=True)
    fecha_fin = forms.CharField(widget=wDateField, required=True)

    class Meta:
        model = ComisionAcademica
        exclude = ['usuario', ]


class ApoyoTecnicoForm(forms.ModelForm):
    apoyo_tecnico = forms.ModelChoiceField(Actividad.objects.all().order_by('actividad'), widget=wSelect, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    dependencia = forms.ModelChoiceField(Dependencia.objects.all().order_by('dependencia'), widget=wSelect, required=True)
    apoyo_inicio = forms.CharField(widget=wDateField, required=True)
    apoyo_fin = forms.CharField(widget=wDateField, required=True)

    class Meta:
        model = ApoyoTecnico
        exclude = ['usuario', ]


class ApoyoOtraActividadForm(forms.ModelForm):
    apoyo_actividad = forms.ModelChoiceField(Actividad.objects.all().order_by('actividad'), widget=wSelect, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    dependencia = forms.ModelChoiceField(Dependencia.objects.all().order_by('dependencia'), widget=wSelect, required=True)
    apoyo_inicio = forms.CharField(widget=wDateField, required=True)
    apoyo_fin = forms.CharField(widget=wDateField, required=True)

    class Meta:
        model = ApoyoOtraActividad
        exclude = ['usuario', ]


