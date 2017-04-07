from . models import *

from django import forms

#

class CargoAcademicoAdministrativoForm(forms.ModelForm):
    class Meta:
        model = CargoAcademicoAdministrativo
        exclude = ['tags', ]


class PrologoLibroForm(forms.ModelForm):
    class Meta:
        model = PrologoLibro
        exclude = ['usuario', 'tags', ]
