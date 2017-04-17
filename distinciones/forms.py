from . models import *
from django import forms

#

class DistincionAcademicoForm(forms.ModelForm):
    class Meta:
        model = DistincionAcademico
        exclude = []


class DistincionAlumnoForm(forms.ModelForm):
    class Meta:
        model = DistincionAlumno
        exclude = []