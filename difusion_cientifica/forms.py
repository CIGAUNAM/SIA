from . models import *

from django import forms

#

class MemoriaInExtensoForm(forms.ModelForm):
    class Meta:
        model = MemoriaInExtenso
        exclude = ['tags', ]


class PrologoLibroForm(forms.ModelForm):
    class Meta:
        model = PrologoLibro
        exclude = ['tags', ]


class ResenaForm(forms.ModelForm):
    class Meta:
        model = Resena
        exclude = ['tags', ]


class OrganizacionEventoAcademicoForm(forms.ModelForm):
    class Meta:
        model = OrganizacionEventoAcademico
        exclude = ['tags', ]


class ParticipacionEventoAcademicoForm(forms.ModelForm):
    class Meta:
        model = ParticipacionEventoAcademico
        exclude = ['tags', ]
