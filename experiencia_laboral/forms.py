from . models import *
from django import forms

#

class ExperienciaLaboralForm(forms.ModelForm):
    class Meta:
        model = ExperienciaLaboral
        exclude = ['usuario', 'tags', ]


class LineaInvestigacionForm(forms.ModelForm):
    class Meta:
        model = LineaInvestigacion
        exclude = ['usuario', 'tags', ]


class CapacidadPotencialidadForm(forms.ModelForm):
    class Meta:
        model = CapacidadPotencialidad
        exclude = ['usuario', 'tags', ]
