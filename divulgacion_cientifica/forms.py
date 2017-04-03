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
        exclude = ['tags', ]


class OrganizacionEventoDivulgacionForm(forms.ModelForm):
    class Meta:
        model = OrganizacionEventoDivulgacion
        exclude = ['tags', ]


class ParticipacionEventoDivulgacionForm(forms.ModelForm):
    class Meta:
        model = ParticipacionEventoDivulgacion
        exclude = ['tags', ]


class MedioDivulgacionForm(forms.ModelForm):
    class Meta:
        model = MedioDivulgacion
        exclude = ['tags', ]


class ProgramaRadioTelevisionInternetForm(forms.ModelForm):
    class Meta:
        model = ProgramaRadioTelevisionInternet
        exclude = ['tags', ]


class LibroDivulgacionForm(forms.ModelForm):
    class Meta:
        model = LibroDivulgacion
        exclude = ['tipo', 'tags', ]