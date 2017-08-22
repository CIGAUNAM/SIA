from SIA.widgets import *
from . models import *
from django import forms

from nucleo.models import Institucion
from django_select2.forms import Select2MultipleWidget, Select2Widget, ModelSelect2Widget

#

class CursoDocenciaForm(forms.ModelForm):
    nivel = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}), choices=(('', 'Seleccionar nivel de curso'), ('LICENCIATURA', 'Licenciatura'), ('MAESTRIA', 'Maestría'), ('DOCTORADO', 'Doctorado'), ('OTRO', 'Otro')), required=True)
    licenciatura = forms.ModelChoiceField(
        required=False,
        queryset=ProgramaLicenciatura.objects.all(),
        label="Programa de licenciatura",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=ProgramaLicenciatura.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    maestria = forms.ModelChoiceField(
        required=False,
        queryset=ProgramaMaestria.objects.all(),
        label="Programa de maestría",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=ProgramaMaestria.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    doctorado = forms.ModelChoiceField(
        required=False,
        queryset=ProgramaDoctorado.objects.all(),
        label="Programa de doctorado",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=ProgramaDoctorado.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    asignatura = forms.ModelChoiceField(
        queryset=Asignatura.objects.all(),
        label="Asignatura",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Asignatura.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    modalidad = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}), choices=(('', 'Seleccionar modalidad de curso'), ('PRESENCIAL', 'Presencial'), ('EN_LINEA', 'En línea'), ('MIXTO', 'Mixto'), ('OTRO', 'Otro')), required=True)
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
    total_horas = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}), required=True)

    class Meta:
        model = CursoDocencia
        exclude = ['usuario', 'tipo', ]
        widgets = {
            'academicos_participantes': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'otras_dependencias_participantes': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }