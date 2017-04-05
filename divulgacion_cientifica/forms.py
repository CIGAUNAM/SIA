from . models import *
from nucleo.models import Libro as LibroDivulgacion
from django import forms

#

class ArticuloDivulgacionForm(forms.ModelForm):
    class Meta:
        model = ArticuloDivulgacion
        exclude = ['tags', ]


class CapituloLibroDivulgacionForm(forms.ModelForm):
    class Meta:
        model = CapituloLibroDivulgacion
        exclude = ['usuario', 'tags', ]


class OrganizacionEventoDivulgacionForm(forms.ModelForm):
    class Meta:
        model = OrganizacionEventoDivulgacion
        exclude = ['usuario', 'tags', ]


class ParticipacionEventoDivulgacionForm(forms.ModelForm):
    class Meta:
        model = ParticipacionEventoDivulgacion
        exclude = ['usuario', 'tags', ]


class ProgramaRadioTelevisionInternetForm(forms.ModelForm):
    class Meta:
        model = ProgramaRadioTelevisionInternet
        exclude = ['usuario', 'tags', ]


class LibroDivulgacionForm(forms.ModelForm):
    class Meta:
        model = LibroDivulgacion
        exclude = ['tipo', 'tags', ]