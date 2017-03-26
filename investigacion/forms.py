from . models import *
from django import forms

#

class ArticuloCientificoForm(forms.ModelForm):
    class Meta:
        model = ArticuloCientifico
        exclude = ['tags', ]