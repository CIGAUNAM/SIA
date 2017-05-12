from SIA.widgets import *
from . models import *
from django import forms

#

class CursoDocenciaForm(forms.ModelForm):
    nivel = forms.ChoiceField(widget=wSelect, choices=(('LICENCIATURA', 'Licenciatura'), ('MAESTRIA', 'Maestría'), ('DOCTORADO', 'Doctorado')), required=True)
    licenciatura = forms.ModelChoiceField(ProgramaLicenciatura.objects.all(), widget=wSelect, required=True)
    maestria = forms.ModelChoiceField(ProgramaMaestria.objects.all(), widget=wSelect, required=True)
    doctorado = forms.ModelChoiceField(ProgramaDoctorado.objects.all(), widget=wSelect, required=True)
    asignatura = forms.ModelChoiceField(Asignatura.objects.all(), widget=wSelect, required=True)
    modalidad = forms.ChoiceField(widget=wSelect, choices=(('PRESENCIAL', 'Presencial'), ('EN_LINEA', 'En línea')), required=True)
    dependencia = forms.ModelChoiceField(Dependencia.objects.all(), widget=wSelect, required=True)
    fecha_inicio = forms.CharField(widget=wDateField, required=True)
    fecha_fin = forms.CharField(widget=wDateField, required=True)
    total_horas = forms.CharField(widget=wNumberField, required=True)

    class Meta:
        model = CursoDocencia
        exclude = ['usuario', 'tipo', ]