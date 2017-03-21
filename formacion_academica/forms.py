from . models import *
from django import forms


#


class CursoEspecializacionForm(forms.ModelForm):
    class Meta:
        model = CursoEspecializacion
        exclude = ['slug', 'usuario', 'tags', ]


class LicenciaturaForm(forms.ModelForm):
    class Meta:
        model = Licenciatura
        exclude = ['slug', 'usuario', ]


class MaestriaForm(forms.ModelForm):
    class Meta:
        model = Maestria
        exclude = ['slug', 'usuario', ]


class DoctoradoForm(forms.ModelForm):
    class Meta:
        model = Doctorado
        exclude = ['slug', 'usuario', ]


class PostDoctoradoForm(forms.ModelForm):
    class Meta:
        model = PostDoctorado
        exclude = ['slug', 'usuario', ]


