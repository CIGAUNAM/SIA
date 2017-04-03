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
        exclude = ['usuario', 'tags', ]


class ResenaForm(forms.ModelForm):
    class Meta:
        model = Resena
        exclude = ['usuario', 'tags', ]


class OrganizacionEventoAcademicoForm(forms.ModelForm):
    class Meta:
        model = OrganizacionEventoAcademico
        exclude = ['usuario', 'tags', ]


class ParticipacionEventoAcademicoForm(forms.ModelForm):
    class Meta:
        model = ParticipacionEventoAcademico
        exclude = ['usuario', 'tags', ]
