from SIA.widgets import *
from . models import *
from django import forms

#

class CursoDocenciaForm(forms.ModelForm):
    nivel = forms.ChoiceField(widget=wSelectSingle, choices=(('', ''), ('', ''), ('LICENCIATURA', 'Licenciatura'), ('MAESTRIA', 'Maestría'), ('DOCTORADO', 'Doctorado')), required=True)
    licenciatura = forms.ModelChoiceField(ProgramaLicenciatura.objects.all().order_by('programa'), widget=wSelectSingle, required=True)
    maestria = forms.ModelChoiceField(ProgramaMaestria.objects.all().order_by('programa'), widget=wSelectSingle, required=True)
    doctorado = forms.ModelChoiceField(ProgramaDoctorado.objects.all().order_by('programa'), widget=wSelectSingle, required=True)
    asignatura = forms.ModelChoiceField(Asignatura.objects.all().order_by('asignatura'), widget=wSelectSingle, required=True)
    modalidad = forms.ChoiceField(widget=wSelectSingle, choices=(('', ''), ('', ''), ('PRESENCIAL', 'Presencial'), ('EN_LINEA', 'En línea')),required=True)
    dependencia = forms.ModelChoiceField(Dependencia.objects.all().order_by('dependencia'), widget=wSelectSingle, required=True)
    fecha_inicio = forms.CharField(widget=wDateField, required=True)
    fecha_fin = forms.CharField(widget=wDateField, required=True)
    total_horas = forms.CharField(widget=wNumberField, required=True)

    class Meta:
        model = CursoDocencia
        exclude = ['usuario', 'tipo', 'tags', ]