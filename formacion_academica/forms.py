from . models import *
from django import forms


#


class CursoEspecializacionForm(forms.ModelForm):
    class Meta:
        model = CursoEspecializacion
        exclude = ['slug', ]


class LicenciaturaForm(forms.ModelForm):
    class Meta:
        model = Licenciatura
        exclude = ['slug', ]


class MaestriaForm(forms.ModelForm):
    class Meta:
        model = Maestria
        exclude = ['slug', ]


class DoctoradoForm(forms.ModelForm):
    class Meta:
        model = Doctorado
        exclude = ['slug', ]


class PostDoctoradoForm(forms.ModelForm):
    class Meta:
        model = PostDoctorado
        exclude = ['slug', ]


