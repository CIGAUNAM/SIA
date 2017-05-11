#from django import forms

from SIA.widgets import *
from .models import *
from django.conf import settings

from django_select2.forms import ModelSelect2Widget, Select2Widget, Select2MultipleWidget



class CursoEspecializacionForm(forms.ModelForm):
    nombre = forms.CharField(widget=wCharField, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    tipo = forms.ChoiceField(widget=Select2Widget, choices=getattr(settings, 'CURSO_ESPECIALIZACION_TIPO', ), required=True)
    horas = forms.CharField(widget=wNumberField, required=True)
    modalidad = forms.ChoiceField(widget=Select3Widget, choices=getattr(settings, 'CURSO_ESPECIALIZACION_MODALIDAD', ), required=True)
    fecha_inicio = forms.CharField(widget=wDateField, required=True)
    fecha_fin = forms.CharField(widget=wDateField, required=False)
    area_conocimiento = forms.ModelChoiceField(AreaConocimiento.objects.all().order_by('pk'), widget=Select3Widget, required=True)
    dependencia = forms.ModelChoiceField(Dependencia.objects.all(), label='Dependencia',  widget=Select2MultipleWidget, required=True)
    #dependencia = forms.ChoiceField(label='Dependencia', widget=ModelSelect3Widget(model=Dependencia, search_fields=['nombre__icontains', ]), required=True)

    class Meta:
        model = CursoEspecializacion
        exclude = ['usuario', ]



class LicenciaturaForm(forms.ModelForm):
    carrera = forms.ModelChoiceField(ProgramaLicenciatura.objects.all().order_by('programa'), widget=wSelect, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    dependencia = forms.ModelChoiceField(Dependencia.objects.all().order_by('dependencia'), widget=wSelect, required=True)
    titulo_tesis = forms.CharField(widget=wCharField, required=True)
    tesis_doc = forms.FileField(required=False)  # corregir y poner el campo como los demas
    tesis_url = forms.CharField(widget=wCharField, required=False)  # corregir valiadr url
    fecha_inicio = forms.CharField(widget=wDateField, required=True)
    fecha_fin = forms.CharField(widget=wDateField, required=True)
    fecha_grado = forms.CharField(widget=wDateField, required=True)

    class Meta:
        model = Licenciatura
        exclude = ['usuario', ]


class MaestriaForm(forms.ModelForm):
    programa = forms.ModelChoiceField(ProgramaMaestria.objects.all().order_by('programa'), widget=wSelect, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    dependencia = forms.ModelChoiceField(Dependencia.objects.all().order_by('dependencia'), widget=wSelect, required=True)
    titulo_tesis = forms.CharField(widget=wCharField, required=True)
    tesis_doc = forms.FileField(required=False)  # corregir y poner el campo como los demas
    tesis_url = forms.CharField(widget=wCharField, required=False)  # corregir valiadr url
    fecha_inicio = forms.CharField(widget=wDateField, required=True)
    fecha_fin = forms.CharField(widget=wDateField, required=False)
    fecha_grado = forms.CharField(widget=wDateField, required=False)

    class Meta:
        model = Maestria
        exclude = ['usuario', ]


class DoctoradoForm(forms.ModelForm):
    programa = forms.ModelChoiceField(ProgramaDoctorado.objects.all().order_by('programa'), widget=wSelect, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    dependencia = forms.ModelChoiceField(Dependencia.objects.all().order_by('dependencia'), widget=wSelect, required=True)
    titulo_tesis = forms.CharField(widget=wCharField, required=True)
    tesis_doc = forms.FileField(required=False)  # corregir y poner el campo como los demas
    tesis_url = forms.CharField(widget=wCharField, required=False)  # corregir valiadr url
    fecha_inicio = forms.CharField(widget=wDateField, required=True)
    fecha_fin = forms.CharField(widget=wDateField, required=False)
    fecha_grado = forms.CharField(widget=wDateField, required=False)

    class Meta:
        model = Doctorado
        exclude = ['usuario', ]


class PostDoctoradoForm(forms.ModelForm):
    titulo = forms.CharField(widget=wCharField, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    area_conocimiento = forms.ModelChoiceField(AreaConocimiento.objects.all().order_by('categoria'),
                                               widget=wSelect, required=True)
    dependencia = forms.ModelChoiceField(Dependencia.objects.all().order_by('dependencia'), widget=wSelect, required=True)
    proyecto = forms.ModelChoiceField(Proyecto.objects.all().order_by('nombre_proyecto'), widget=wSelect, required=True)
    fecha_inicio = forms.CharField(widget=wDateField, required=True)
    fecha_fin = forms.CharField(widget=wDateField, required=False)

    class Meta:
        model = PostDoctorado
        exclude = ['usuario', ]
