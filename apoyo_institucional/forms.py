from . models import *

from django import forms

#

class CargoAcademicoAdministrativoForm(forms.ModelForm):
    class Meta:
        model = CargoAcademicoAdministrativo
        exclude = ['usuario', 'tags', ]


class RepresentacionOrganoColegiadoForm(forms.ModelForm):
    class Meta:
        model = RepresentacionOrganoColegiado
        exclude = ['usuario', 'tags', ]


class ComisionAcademicaForm(forms.ModelForm):
    class Meta:
        model = ComisionAcademica
        exclude = ['usuario', 'tags', ]


class ApoyoTecnicoForm(forms.ModelForm):
    class Meta:
        model = ApoyoTecnico
        exclude = ['usuario', 'tags', ]


class ApoyoOtraActividadForm(forms.ModelForm):
    class Meta:
        model = ApoyoTecnico
        exclude = ['usuario', 'tags', ]


