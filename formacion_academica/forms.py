from django import forms

from SIA.widgets import *
from .models import *
from django.conf import settings
from nucleo.models import Institucion


class CursoEspecializacionForm(forms.ModelForm):
    # datesss = forms.DateField(widget=DatePicker(options={"format": "mm/dd/yyyy", "autoclose": True}))
    nombre_curso = forms.CharField(widget=wCharField)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    tipo = forms.ChoiceField(widget=wSelectSingle, choices=getattr(settings, 'CURSO_ESPECIALIZACION_TIPO', ))
    horas = forms.CharField(widget=wNumberField)
    modalidad = forms.ChoiceField(widget=wSelectSingle, choices=getattr(settings, 'CURSO_ESPECIALIZACION_MODALIDAD', ))
    fecha_inicio = forms.CharField(widget=wDateField)
    # fecha_inicio = forms.CharField()
    # fecha_fin = forms.CharField()
    fecha_fin = forms.CharField(widget=wDateField)
    area_conocimiento = forms.ModelChoiceField(AreaConocimiento.objects.all().order_by('categoria'),
                                               widget=wSelectSingle)
    dependencia = forms.ModelChoiceField(Dependencia.objects.all().order_by('dependencia'), widget=wSelectSingle)

    class Meta:
        model = CursoEspecializacion
        exclude = ['usuario', 'tags', ]


class LicenciaturaForm(forms.ModelForm):
    carrera = forms.ModelChoiceField(ProgramaLicenciatura.objects.all().order_by('programa'), widget=wSelectSingle)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    dependencia = forms.ModelChoiceField(Dependencia.objects.all().order_by('dependencia'), widget=wSelectSingle)
    titulo_tesis = forms.CharField(widget=wCharField)
    tesis_doc = forms.FileField(required=False)  # corregir y poner el campo como los demas
    tesis_url = forms.CharField(widget=wCharField, required=False)  # corregir valiadr url
    fecha_inicio = forms.CharField(widget=wDateField)
    fecha_fin = forms.CharField(widget=wDateField)
    fecha_grado = forms.CharField(widget=wDateField)

    class Meta:
        model = Licenciatura
        exclude = ['usuario', 'tags', ]


class MaestriaForm(forms.ModelForm):
    programa = forms.ModelChoiceField(ProgramaMaestria.objects.all().order_by('programa'), widget=wSelectSingle)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    dependencia = forms.ModelChoiceField(Dependencia.objects.all().order_by('dependencia'), widget=wSelectSingle)
    titulo_tesis = forms.CharField(widget=wCharField)
    tesis_doc = forms.FileField(required=False)  # corregir y poner el campo como los demas
    tesis_url = forms.CharField(widget=wCharField, required=False)  # corregir valiadr url
    fecha_inicio = forms.CharField(widget=wDateField)
    fecha_fin = forms.CharField(widget=wDateField)
    fecha_grado = forms.CharField(widget=wDateField)

    class Meta:
        model = Maestria
        exclude = ['usuario', 'tags', ]


class DoctoradoForm(forms.ModelForm):
    programa = forms.ModelChoiceField(ProgramaDoctorado.objects.all().order_by('programa'), widget=wSelectSingle)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    dependencia = forms.ModelChoiceField(Dependencia.objects.all().order_by('dependencia'), widget=wSelectSingle)
    titulo_tesis = forms.CharField(widget=wCharField)
    tesis_doc = forms.FileField(required=False)  # corregir y poner el campo como los demas
    tesis_url = forms.CharField(widget=wCharField, required=False)  # corregir valiadr url
    fecha_inicio = forms.CharField(widget=wDateField)
    fecha_fin = forms.CharField(widget=wDateField)
    fecha_grado = forms.CharField(widget=wDateField)

    class Meta:
        model = Doctorado
        exclude = ['usuario', 'tags', ]


class PostDoctoradoForm(forms.ModelForm):
    titulo = forms.CharField(widget=wCharField)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    area_conocimiento = forms.ModelChoiceField(AreaConocimiento.objects.all().order_by('categoria'),
                                               widget=wSelectSingle)
    dependencia = forms.ModelChoiceField(Dependencia.objects.all().order_by('dependencia'), widget=wSelectSingle)
    proyecto = forms.ModelChoiceField(Proyecto.objects.all().order_by('nombre_proyecto'), widget=wSelectSingle)
    fecha_inicio = forms.CharField(widget=wDateField)
    fecha_fin = forms.CharField(widget=wDateField)

    class Meta:
        model = PostDoctorado
        exclude = ['usuario', 'tags', ]
