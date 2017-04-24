from . models import *
from django import forms
#from bootstrap_datepicker.widgets import DatePicker
#from django_select2 import fields, widgets

#

#class CursoEspecializacionTipo(fields.AutoModelSelect2TagField):
#    queryset = CursoEspecializacion.objects
#    #search_fields = ['tipo__icontains', ]


class CursoEspecializacionForm(forms.ModelForm):
    #datesss = forms.DateField(widget=DatePicker(options={"format": "mm/dd/yyyy", "autoclose": True}))
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


