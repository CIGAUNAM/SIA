from SIA.widgets import *
from .models import *

from django import forms
from django_select2.forms import Select2MultipleWidget, ModelSelect2Widget, Select2Widget

#

class LaborDirectivaCoordinacionForm(forms.ModelForm):
    institucion2 = forms.ModelChoiceField(
        queryset=Institucion.objects.all(),
        label="Institución",
        widget=ModelSelect2Widget(
            search_fields=['nombre_institucion__icontains'],
            queryset=Institucion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    dependencia = forms.ModelChoiceField(
        queryset=Dependencia.objects.all(),
        label="Dependencia",
        widget=ModelSelect2Widget(
            search_fields=['nombre_dependencia__icontains'],
            dependent_fields={'institucion': 'institucion'},
            queryset=Dependencia.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    fecha_inicio = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    fecha_fin = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)

    class Meta:
        model = LaborDirectivaCoordinacion
        exclude = ['usuario', ]
        widgets = {
            'tipo_cargo': TextInput(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class RepresentacionOrganoColegiadoUNAMForm(forms.ModelForm):
    tipo_representacion = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right', 'placeholder': 'Tipo de representación'}),
        choices=(('', '-------'), ('DENTRO', 'Dentro de la UNAM'), ('FUERA', 'Fuera de la UNAM')), required=False)
    representacion_dentro_unam = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        choices=(('', '-------'), ('PRIDE', 'PRIDE'), ('CAACS', 'CAACS'), ('CONSEJO_INTERNO', 'Consejo interno'),
                 ('COMISION_DICTAMINADORA', 'Comisión dictaminadora'), ('COMISION_EVALUADORA', 'Comisiòn evaluadora'),
                 ('OTRA', 'Otra')), required=False)

    representacion_dentro_unam_otra = forms.CharField(widget=TextInput(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}), required=True)
    representacion_fuera_unam = forms.CharField(widget=TextInput(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}), required=True)

    institucion_dentro_unam = forms.ModelChoiceField(
        queryset=InstitucionSimple.objects.filter(institucion_perteneceunam=True),
        label="Institución",
        widget=ModelSelect2Widget(
            search_fields=['institucion_nombre__icontains'],
            queryset=InstitucionSimple.objects.filter(institucion_perteneceunam=True),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    institucion_fuera_unam = forms.ModelChoiceField(
        queryset=InstitucionSimple.objects.filter(institucion_perteneceunam=True),
        label="Institución",
        widget=ModelSelect2Widget(
            search_fields=['institucion_nombre__icontains'],
            queryset=InstitucionSimple.objects.filter(institucion_perteneceunam=True),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    fecha_inicio = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    fecha_fin = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)

    class Meta:
        model = RepresentacionOrganoColegiadoUNAM
        exclude = ['usuario', ]



class ComisionInstitucionalCIGAForm(forms.ModelForm):
    tipo_institucion = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right', 'placeholder': 'Tipo de representación'}),
        choices=(('', '-------'), ('INTERIOR', 'Al interior del CIGA'), ('EXTERIOR', 'Al exterior del CIGA')), required=False)
    fecha_inicio = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    fecha_fin = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    institucion2 = forms.ModelChoiceField(
        queryset=Institucion.objects.all(),
        label="Institución",
        widget=ModelSelect2Widget(
            search_fields=['nombre_institucion__icontains'],
            queryset=Institucion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
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
        model = ComisionInstitucionalCIGA
        exclude = ['usuario', ]
        widgets = {
            'tipo_comision': TextInput(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


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
    institucion = forms.ModelChoiceField(
        queryset=Institucion.objects.all(),
        label="Institución",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Institucion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    dependencia = forms.ModelChoiceField(
        queryset=Dependencia.objects.all(),
        label="Dependencia",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            dependent_fields={'institucion': 'institucion'},
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
    institucion = forms.ModelChoiceField(
        queryset=Institucion.objects.all(),
        label="Institución",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Institucion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    dependencia = forms.ModelChoiceField(
        queryset=Dependencia.objects.all(),
        label="Dependencia",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            dependent_fields={'institucion': 'institucion'},
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
            'titulo_proyecto': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
        }


class ComisionForm(forms.ModelForm):
    class Meta:
        model = ComisionInstitucional
        exclude = []
        widgets = {
            'titulo_proyecto': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
        }


class ActividadApoyoForm(forms.ModelForm):
    class Meta:
        model = ActividadApoyo
        exclude = []
        widgets = {
            'titulo_proyecto': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
        }