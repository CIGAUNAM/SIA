from SIA.widgets import *
from . models import *
from django import forms

#

class AsesorEstanciaForm(forms.ModelForm):
    asesorado = forms.ModelChoiceField(User.objects.all(), widget=wSelect, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    tipo = forms.ChoiceField(widget=wSelect, choices=(('', ''), ('', ''), ('RESIDENCIA', 'Residencia'), ('PRACTICA', 'Práctica'), ('ESTANCIA', 'Estancia'), ('SERVICIO_SOCIAL', 'Servicio Social'), ('OTRO', 'Otro')), required=True)
    grado_academico = forms.ChoiceField(widget=wSelect, choices=getattr(settings, 'GRADO_ACADEMICO', ), required=True)
    programa_licenciatura = forms.ModelChoiceField(ProgramaLicenciatura.objects.all(), widget=wSelect, required=True)
    programa_maestria = forms.ModelChoiceField(ProgramaMaestria.objects.all(), widget=wSelect, required=True)
    programa_doctorado = forms.ModelChoiceField(ProgramaDoctorado.objects.all(), widget=wSelect, required=True)
    beca = forms.ModelChoiceField(Beca.objects.all(), widget=wSelect, required=True)
    proyecto = forms.ModelChoiceField(Proyecto.objects.all(), widget=wSelect, required=True)
    dependencia = forms.ModelChoiceField(Dependencia.objects.all(), widget=wSelect, required=True)
    fecha_inicio = forms.CharField(widget=wDateField, required=True)
    fecha_fin = forms.CharField(widget=wDateField, required=True)

    class Meta:
        model = AsesorEstancia
        exclude = ['usuario',]


class DireccionTesisForm(forms.ModelForm):
    titulo = forms.CharField(widget=wCharField, required=True)
    asesorado = forms.ModelChoiceField(User.objects.all(), widget=wSelect, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    grado_academico = forms.ChoiceField(widget=wSelect, choices=getattr(settings, 'GRADO_ACADEMICO', ), required=True)
    dependencia = forms.ModelChoiceField(Dependencia.objects.all(), widget=wSelect, required=True)
    beca = forms.ModelChoiceField(Beca.objects.all(), widget=wSelect, required=True)
    reconocimiento = forms.ModelChoiceField(Reconocimiento.objects.all(), widget=wSelect, required=True)
    fecha_examen = forms.CharField(widget=wDateField, required=False)

    class Meta:
        model = DireccionTesis
        exclude = ['usuario',]


class ComiteTutoralForm(forms.ModelForm):
    tipo = forms.ChoiceField(widget=wSelect, choices=(('', ''), ('', ''), ('MAESTRIA', 'Maestría'), ('DOCTORADO', 'Doctorado')), required=True)
    programa_maestria = forms.ModelChoiceField(ProgramaMaestria.objects.all(), widget=wSelect, required=True)
    programa_doctorado = forms.ModelChoiceField(ProgramaDoctorado.objects.all(), widget=wSelect, required=True)
    status = forms.ChoiceField(widget=wSelect, choices=(('', ''), ('', ''), ('EN_PROCESO', 'En proceso'), ('CONCLUIDO', 'Concluído')), required=True)
    fecha_inicio = forms.CharField(widget=wDateField, required=True)
    fecha_fin = forms.CharField(widget=wDateField, required=False)
    asesorado = forms.ModelChoiceField(User.objects.all(), widget=wSelect, required=True)
    asesor_principal = forms.ModelChoiceField(User.objects.all(), widget=wSelect, required=True)
    proyecto = forms.ModelChoiceField(Proyecto.objects.all(), widget=wSelect, required=True)
    dependencia = forms.ModelChoiceField(Dependencia.objects.all(), widget=wSelect, required=True)

    class Meta:
        model = ComiteTutoral
        exclude = []


class ComiteCandidaturaDoctoralForm(forms.ModelForm):
    asesorado = forms.ModelChoiceField(User.objects.all(), widget=wSelect, required=True)
    asesor_principal = forms.ModelChoiceField(User.objects.all(), widget=wSelect, required=True)
    proyecto = forms.ModelChoiceField(Proyecto.objects.all(), widget=wSelect, required=True)
    programa_doctorado = forms.ModelChoiceField(ProgramaDoctorado.objects.all(), widget=wSelect, required=True)
    dependencia = forms.ModelChoiceField(Dependencia.objects.all(), widget=wSelect, required=True)
    fecha_defensa = forms.CharField(widget=wDateField, required=True)

    class Meta:
        model = ComiteCandidaturaDoctoral
        exclude = []