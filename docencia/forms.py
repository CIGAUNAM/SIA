from . models import *
from django import forms

#

class CursoDocenciaForm(forms.ModelForm):
    class Meta:
        model = CursoDocencia
        exclude = ['usuario', 'tags', ]