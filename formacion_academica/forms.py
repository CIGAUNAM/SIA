from django import forms

from SIA.widgets import *
from . models import *
from django.conf import settings
from nucleo.models import Institucion

class CursoEspecializacionForm(forms.ModelForm):
    #datesss = forms.DateField(widget=DatePicker(options={"format": "mm/dd/yyyy", "autoclose": True}))
    nombre_curso = forms.CharField(widget=wCharField)
    descripcion = forms.CharField(widget=wTextarea)
    tipo = forms.ChoiceField(widget=wSelectSingle, choices=getattr(settings, 'CURSO_ESPECIALIZACION_TIPO', ))
    institucion = forms.ModelChoiceField(Institucion.objects.all().order_by('institucion'), widget=wSelectSingle)
    dependencia = forms.ModelChoiceField(Dependencia.objects.all().order_by('dependencia'), widget=wSelectSingle)

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


