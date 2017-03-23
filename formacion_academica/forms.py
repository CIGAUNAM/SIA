from . models import *
from django import forms


#


class CursoEspecializacionForm(forms.ModelForm):
    class Meta:
        model = CursoEspecializacion

        exclude = ['usuario', 'tags', ]


class LicenciaturaForm(forms.ModelForm):
    class Meta:
        model = Licenciatura
        exclude = ['usuario', 'tags', ]


class MaestriaForm(forms.ModelForm):
    class Meta:
        model = Maestria
        exclude = ['usuario', 'tags', ]


class DoctoradoForm(forms.ModelForm):
    class Meta:
        model = Doctorado
        exclude = ['usuario', 'tags', ]


class PostDoctoradoForm(forms.ModelForm):
    class Meta:
        model = PostDoctorado
        exclude = ['usuario', 'tags', ]


