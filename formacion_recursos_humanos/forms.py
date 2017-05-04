from SIA.widgets import *
from . models import *
from django import forms

#

class AsesorEstanciaForm(forms.ModelForm):
    asesorado = forms.ModelChoiceField(User.objects.all().order_by('first_name'), widget=wSelectSingle, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    tipo = forms.ChoiceField(widget=wSelectSingle, choices=(('', ''), ('', ''), ('RESIDENCIA', 'Residencia'), ('PRACTICA', 'Práctica'), ('ESTANCIA', 'Estancia'), ('SERVICIO_SOCIAL', 'Servicio Social'), ('OTRO', 'Otro')), required=True)
    grado_academico = forms.ChoiceField(widget=wSelectSingle, choices=getattr(settings, 'GRADO_ACADEMICO', ), required=True)
    programa_licenciatura = forms.ModelChoiceField(ProgramaLicenciatura.objects.all().order_by('programa'), widget=wSelectSingle, required=True)
    programa_maestria = forms.ModelChoiceField(ProgramaMaestria.objects.all().order_by('programa'), widget=wSelectSingle, required=True)
    programa_doctorado = forms.ModelChoiceField(ProgramaDoctorado.objects.all().order_by('programa'), widget=wSelectSingle, required=True)
    beca = forms.ModelChoiceField(Beca.objects.all().order_by('beca'), widget=wSelectSingle, required=True)
    proyecto = forms.ModelChoiceField(Proyecto.objects.all().order_by('nombre_proyecto'), widget=wSelectSingle, required=True)
    dependencia = forms.ModelChoiceField(Dependencia.objects.all().order_by('dependencia'), widget=wSelectSingle, required=True)
    fecha_inicio = forms.CharField(widget=wDateField, required=True)
    fecha_fin = forms.CharField(widget=wDateField, required=True)

    class Meta:
        model = AsesorEstancia
        exclude = ['usuario',]


class DireccionTesisForm(forms.ModelForm):
    class Meta:
        model = DireccionTesis
        exclude = ['usuario',]


class ComiteTutoralForm(forms.ModelForm):
    class Meta:
        model = ComiteTutoral
        exclude = []


class ComiteCandidaturaDoctoralForm(forms.ModelForm):
    class Meta:
        model = ComiteCandidaturaDoctoral
        exclude = []