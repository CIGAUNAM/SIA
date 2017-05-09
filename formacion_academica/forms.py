from django import forms

from SIA.widgets import *
from .models import *
from django.conf import settings

from django_select2.forms import Select2Widget, Select2MultipleWidget
from nucleo.models import Institucion


class CursoEspecializacionForm(forms.ModelForm):
    nombre_curso = forms.CharField(widget=wCharField, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    tipo = forms.ChoiceField(widget=Select3Widget, choices=getattr(settings, 'CURSO_ESPECIALIZACION_TIPO', ), required=True)
    horas = forms.CharField(widget=wNumberField, required=True)
    modalidad = forms.ChoiceField(widget=Select3Widget, choices=getattr(settings, 'CURSO_ESPECIALIZACION_MODALIDAD', ), required=True)
    fecha_inicio = forms.CharField(widget=wDateField, required=True)
    fecha_fin = forms.CharField(widget=wDateField, required=False)
    area_conocimiento = forms.ModelChoiceField(AreaConocimiento.objects.all().order_by('pk'), widget=Select3Widget, required=True)
    dependencia = forms.ModelChoiceField(Dependencia.objects.all().order_by('dependencia'), widget=Select3Widget, required=True)

    class Meta:
        model = CursoEspecializacion
        exclude = ['usuario', 'tags', ]


class LicenciaturaForm(forms.ModelForm):
    carrera = forms.ModelChoiceField(ProgramaLicenciatura.objects.all().order_by('programa'), widget=wSelectSingle, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    dependencia = forms.ModelChoiceField(Dependencia.objects.all().order_by('dependencia'), widget=wSelectSingle, required=True)
    titulo_tesis = forms.CharField(widget=wCharField, required=True)
    tesis_doc = forms.FileField(required=False)  # corregir y poner el campo como los demas
    tesis_url = forms.CharField(widget=wCharField, required=False)  # corregir valiadr url
    fecha_inicio = forms.CharField(widget=wDateField, required=True)
    fecha_fin = forms.CharField(widget=wDateField, required=True)
    fecha_grado = forms.CharField(widget=wDateField, required=True)

    class Meta:
        model = Licenciatura
        exclude = ['usuario', 'tags', ]


class MaestriaForm(forms.ModelForm):
    programa = forms.ModelChoiceField(ProgramaMaestria.objects.all().order_by('programa'), widget=wSelectSingle, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    dependencia = forms.ModelChoiceField(Dependencia.objects.all().order_by('dependencia'), widget=wSelectSingle, required=True)
    titulo_tesis = forms.CharField(widget=wCharField, required=True)
    tesis_doc = forms.FileField(required=False)  # corregir y poner el campo como los demas
    tesis_url = forms.CharField(widget=wCharField, required=False)  # corregir valiadr url
    fecha_inicio = forms.CharField(widget=wDateField, required=True)
    fecha_fin = forms.CharField(widget=wDateField, required=False)
    fecha_grado = forms.CharField(widget=wDateField, required=False)

    class Meta:
        model = Maestria
        exclude = ['usuario', 'tags', ]


class DoctoradoForm(forms.ModelForm):
    programa = forms.ModelChoiceField(ProgramaDoctorado.objects.all().order_by('programa'), widget=wSelectSingle, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    dependencia = forms.ModelChoiceField(Dependencia.objects.all().order_by('dependencia'), widget=wSelectSingle, required=True)
    titulo_tesis = forms.CharField(widget=wCharField, required=True)
    tesis_doc = forms.FileField(required=False)  # corregir y poner el campo como los demas
    tesis_url = forms.CharField(widget=wCharField, required=False)  # corregir valiadr url
    fecha_inicio = forms.CharField(widget=wDateField, required=True)
    fecha_fin = forms.CharField(widget=wDateField, required=False)
    fecha_grado = forms.CharField(widget=wDateField, required=False)

    class Meta:
        model = Doctorado
        exclude = ['usuario', 'tags', ]


class PostDoctoradoForm(forms.ModelForm):
    titulo = forms.CharField(widget=wCharField, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    area_conocimiento = forms.ModelChoiceField(AreaConocimiento.objects.all().order_by('categoria'),
                                               widget=wSelectSingle, required=True)
    dependencia = forms.ModelChoiceField(Dependencia.objects.all().order_by('dependencia'), widget=wSelectSingle, required=True)
    proyecto = forms.ModelChoiceField(Proyecto.objects.all().order_by('nombre_proyecto'), widget=wSelectSingle, required=True)
    fecha_inicio = forms.CharField(widget=wDateField, required=True)
    fecha_fin = forms.CharField(widget=wDateField, required=False)

    class Meta:
        model = PostDoctorado
        exclude = ['usuario', 'tags', ]
