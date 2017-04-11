from . models import *

from django import forms

#

class MovilidadAcademicaForm(forms.ModelForm):
    class Meta:
        model = MovilidadAcademica
        exclude = ['tipo', 'usuario', 'tags', ]