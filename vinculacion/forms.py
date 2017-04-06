from . models import *
from django import forms

#

class ArbitrajePublicacionAcademicaForm(forms.ModelForm):
    class Meta:
        model = ArbitrajePublicacionAcademica
        exclude = ['usuario', 'tags', ]


class ArbitrajeProyectoInvestigacionForm(forms.ModelForm):
    class Meta:
        model = ArbitrajeProyectoInvestigacion
        exclude = ['usuario', 'tags', ]


class ArbitrajeOtraActividadForm(forms.ModelForm):
    class Meta:
        model = ArbitrajeOtraActividad
        exclude = ['usuario', 'tags', ]


class RedAcademicaForm(forms.ModelForm):
    class Meta:
        model = RedAcademica
        exclude = ['tags', ]


class ConvenioEntidadNoAcademicaForm(forms.ModelForm):
    class Meta:
        model = ConvenioEntidadNoAcademica
        exclude = ['tags', ]


class ServicioExternoEntidadNoAcademicaForm(forms.ModelForm):
    class Meta:
        model = ServicioExternoEntidadNoAcademica
        exclude = ['usuario', 'tags', ]


class OtroProgramaVinculacionForm(forms.ModelForm):
    class Meta:
        model = OtroProgramaVinculacion
        exclude = ['usuario', 'tags', ]