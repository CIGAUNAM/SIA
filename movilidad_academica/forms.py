from SIA.widgets import *
from . models import *

from django import forms

from django_select2.forms import Select2MultipleWidget, ModelSelect2Widget, Select2Widget

#

class MovilidadAcademicaForm(forms.ModelForm):
    academico = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Académico",
        widget=ModelSelect2Widget(
            search_fields=['first_name__icontains', 'last_name__icontains', 'username__icontains'],
            queryset=User.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
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
    actividades = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}), required=True)
    fecha_inicio = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    fecha_fin = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    intercambio_unam = forms.BooleanField(required=False, label='Es intercambio UNAM')
    financiamiento = forms.ModelChoiceField(
        queryset=Financiamiento.objects.all(),
        label="Financiamiento",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Financiamiento.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    proyecto = forms.ModelChoiceField(
        queryset=ProyectoInvestigacion.objects.all(),
        label="Proyecto de investigación",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=ProyectoInvestigacion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )

    class Meta:
        model = MovilidadAcademica
        exclude = ['tipo', 'usuario', ]
        widgets = {
            'redes_academicas': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class InvitadoMovilidadForm(forms.ModelForm):
    invitado = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True, label='Invitado')
    institucion = forms.ModelChoiceField(
        queryset=InstitucionSimple.objects.all(),
        label="Institución",
        widget=ModelSelect2Widget(
            search_fields=['institucion_nombre__icontains'],
            queryset=InstitucionSimple.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    dependencia = forms.ModelChoiceField(
        queryset=Dependencia.objects.all(),
        label="Dependencia",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Dependencia.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    actividades = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}), required=True)
    fecha_inicio = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    fecha_fin = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    intercambio_unam = forms.BooleanField(required=False, label='Es intercambio UNAM')
    financiamiento = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
                               choices=(('', '-------'), ('PROGRAMAS_UNAM', 'Programas UNAM'), ('POR_PROYECTO', 'Por proyecto'), ('PRESUPUESTO_OPERATIVO', 'Presupuesto operativo')))
    proyecto = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True, label='Proyecto')

    class Meta:
        model = InvitadoMovilidad
        exclude = ['usuario', ]
        widgets = {
            'redes_academicas': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class EstanciaAcademicaForm(forms.ModelForm):
    anfitrion = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True, label='Anfitrión')
    institucion = forms.ModelChoiceField(
        queryset=InstitucionSimple.objects.all(),
        label="Institución",
        widget=ModelSelect2Widget(
            search_fields=['institucion_nombre__icontains'],
            queryset=InstitucionSimple.objects.all(),
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
    actividades = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}), required=True)
    fecha_inicio = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    fecha_fin = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    intercambio_unam = forms.BooleanField(required=False, label='Es intercambio UNAM')
    financiamiento = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        choices=(('', '-------'), ('PROGRAMAS_UNAM', 'Programas UNAM'), ('POR_PROYECTO', 'Por proyecto'),
                 ('PRESUPUESTO_OPERATIVO', 'Presupuesto operativo')))
    proyecto = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), label='Proyecto')

    class Meta:
        model = EstanciaAcademica
        exclude = ['usuario', ]
        widgets = {
            'redes_academicas': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class SabaticoMovilidadForm(forms.ModelForm):
    anfitrion = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True,
                                label='Anfitrión')
    institucion = forms.ModelChoiceField(
        queryset=InstitucionSimple.objects.all(),
        label="Institución",
        widget=ModelSelect2Widget(
            search_fields=['institucion_nombre__icontains'],
            queryset=InstitucionSimple.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    dependencia = forms.ModelChoiceField(
        queryset=Dependencia.objects.all(),
        label="Dependencia",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Dependencia.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    actividades = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}), required=True)
    fecha_inicio = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    fecha_fin = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    financiamiento = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        choices=(('', '-------'), ('PROGRAMAS_UNAM', 'Programas UNAM'), ('POR_PROYECTO', 'Por proyecto'),
                 ('PRESUPUESTO_OPERATIVO', 'Presupuesto operativo')))
    proyecto = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), label='Proyecto')

    class Meta:
        model = SabaticoMovilidad
        exclude = ['usuario', ]
        widgets = {
            'redes_academicas': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }