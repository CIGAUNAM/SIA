from SIA.widgets import *
from . models import *
from django import forms

from nucleo.models import Institucion
from django_select2.forms import Select2MultipleWidget

#

class CursoDocenciaForm(forms.ModelForm):
    nivel = forms.ChoiceField(widget=Select3Widget, choices=(('OTRO', 'Otro'), ('LICENCIATURA', 'Licenciatura'), ('MAESTRIA', 'Maestría'), ('DOCTORADO', 'Doctorado')), required=True)
    licenciatura = forms.ModelChoiceField(
        required=False,
        queryset=ProgramaLicenciatura.objects.all(),
        label="Programa de licenciatura",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            #dependent_fields={'dependencia': 'dependencia'},
        )
    )
    maestria = forms.ModelChoiceField(
        required=False,
        queryset=ProgramaMaestria.objects.all(),
        label="Programa de maestría",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            # dependent_fields={'dependencia': 'dependencia'},
        )
    )
    doctorado = forms.ModelChoiceField(
        required=False,
        queryset=ProgramaDoctorado.objects.all(),
        label="Programa de doctorado",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            # dependent_fields={'dependencia': 'dependencia'},
        )
    )
    asignatura = forms.ModelChoiceField(
        queryset=Asignatura.objects.all(),
        label="Asignatura",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            # dependent_fields={'dependencia': 'dependencia'},
        )
    )
    modalidad = forms.ChoiceField(widget=Select3Widget, choices=(('PRESENCIAL', 'Presencial'), ('EN_LINEA', 'En línea')), required=True)
    institucion = forms.ModelChoiceField(
        queryset=Institucion.objects.all(),
        label="Institución",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            # dependent_fields={'dependencia': 'dependencia'},
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
    fecha_inicio = forms.DateField(widget=wDateField, required=True)
    fecha_fin = forms.DateField(widget=wDateField, required=True)
    total_horas = forms.CharField(widget=wNumberField, required=True)

    class Meta:
        model = CursoDocencia
        exclude = ['usuario', 'tipo', ]
        widgets = {
            'academicos_participantes': Select3MultipleWidget,
            'otras_dependencias_participantes': Select3MultipleWidget,
        }