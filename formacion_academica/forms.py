#from django import forms

from SIA.widgets import *
from .models import *
from django.conf import settings
#from django_select2.views import AutoResponseView

from django_select2.forms import ModelSelect2Widget, Select2Widget, Select2MultipleWidget
from nucleo.models import Institucion

class NombreModelSelect3Widget(ModelSelect3Widget):
    search_fields = [
        'nombre__icontains',
    ]


class CursoEspecializacionForm(forms.ModelForm):
    nombre = forms.CharField(widget=wCharField, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    tipo = forms.ChoiceField(widget=Select3Widget, choices=getattr(settings, 'CURSO_ESPECIALIZACION_TIPO', ), required=True)
    horas = forms.CharField(widget=wNumberField, required=True)
    modalidad = forms.ChoiceField(widget=Select3Widget, choices=getattr(settings, 'CURSO_ESPECIALIZACION_MODALIDAD', ), required=True)
    area_conocimiento = forms.ModelChoiceField(
        queryset=AreaConocimiento.objects.all(),
        label="Área de conocimiento",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            # dependent_fields={'dependencia': 'dependencia'},
        )
    )
    fecha_inicio = forms.CharField(widget=wDateField, required=True)
    fecha_fin = forms.CharField(widget=wDateField, required=False)
    institucion = forms.ModelChoiceField(
        queryset=Institucion.objects.all(),
        label="Institución",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            #dependent_fields={'dependencia': 'dependencia'},
        )
    )
    dependencia = forms.ModelChoiceField(
        queryset=Dependencia.objects.all(),
        label="Dependencia",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            dependent_fields={'institucion': 'institucion'},
            max_results=500,
        )
    )

    class Meta:
        model = CursoEspecializacion
        exclude = ['usuario', ]
        widgets = {
            'dependencia': NombreModelSelect3Widget,
            'area_conocimiento': NombreModelSelect3Widget,
        }
        help_texts = {
            "cargo": 'Group to which this message belongs to',
        }





class LicenciaturaForm(forms.ModelForm):
    carrera = forms.ModelChoiceField(
        queryset=ProgramaLicenciatura.objects.all(),
        label="Institución",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    descripcion = forms.CharField(widget=wTextarea, required=False)
    institucion = forms.ModelChoiceField(
        queryset=Institucion.objects.all(),
        label="Institución",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        ), required=False,
    )
    dependencia = forms.ModelChoiceField(
        queryset=Dependencia.objects.all(),
        label="Dependencia",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            dependent_fields={'institucion': 'institucion'},
            max_results=500,
        )
    )
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
    programa = forms.ModelChoiceField(
        queryset=ProgramaMaestria.objects.all(),
        label="Institución",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    descripcion = forms.CharField(widget=wTextarea, required=False)
    institucion = forms.ModelChoiceField(
        queryset=Institucion.objects.all(),
        label="Institución",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        ), required=False,
    )
    dependencia = forms.ModelChoiceField(
        queryset=Dependencia.objects.all(),
        label="Dependencia",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            dependent_fields={'institucion': 'institucion'},
            max_results=500,
        )
    )
    titulo_tesis = forms.CharField(widget=wCharField, required=True)
    tesis_doc = forms.FileField(required=False)  # corregir y poner el campo como los demas
    tesis_url = forms.CharField(widget=wCharField, required=False)  # corregir valiadr url
    fecha_inicio = forms.CharField(widget=wDateField, required=True)
    fecha_fin = forms.CharField(widget=wDateField, required=True)
    fecha_grado = forms.CharField(widget=wDateField, required=True)

    class Meta:
        model = Maestria
        exclude = ['usuario', ]


class DoctoradoForm(forms.ModelForm):
    programa = forms.ModelChoiceField(
        queryset=ProgramaMaestria.objects.all(),
        label="Institución",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    descripcion = forms.CharField(widget=wTextarea, required=False)
    institucion = forms.ModelChoiceField(
        queryset=Institucion.objects.all(),
        label="Institución",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        ), required=False,
    )
    dependencia = forms.ModelChoiceField(
        queryset=Dependencia.objects.all(),
        label="Dependencia",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            dependent_fields={'institucion': 'institucion'},
            max_results=500,
        )
    )
    titulo_tesis = forms.CharField(widget=wCharField, required=True)
    tesis_doc = forms.FileField(required=False)  # corregir y poner el campo como los demas
    tesis_url = forms.CharField(widget=wCharField, required=False)  # corregir valiadr url
    fecha_inicio = forms.CharField(widget=wDateField, required=True)
    fecha_fin = forms.CharField(widget=wDateField, required=True)
    fecha_grado = forms.CharField(widget=wDateField, required=True)

    class Meta:
        model = Doctorado
        exclude = ['usuario', ]


class PostDoctoradoForm(forms.ModelForm):
    nombre = forms.CharField(widget=wCharField, required=True, label='Título de Post Doctorado')
    descripcion = forms.CharField(widget=wTextarea, required=False)
    area_conocimiento = forms.ModelChoiceField(
        queryset=AreaConocimiento.objects.all(),
        label="Área de conocimiento",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            # dependent_fields={'dependencia': 'dependencia'},
        )
    )
    institucion = forms.ModelChoiceField(
        queryset=Institucion.objects.all(),
        label="Institución",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        ), required=False,
    )
    dependencia = forms.ModelChoiceField(
        queryset=Dependencia.objects.all(),
        label="Dependencia",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            dependent_fields={'institucion': 'institucion'},
            max_results=500,
        )
    )
    proyecto = forms.ModelChoiceField(
        queryset=Proyecto.objects.all(),
        label="Proyecto",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        ), required=False,
    )
    fecha_inicio = forms.CharField(widget=wDateField, required=True, label='Fecha de inicio')
    fecha_fin = forms.CharField(widget=wDateField, required=False, label='Fecha de finalización')

    class Meta:
        model = PostDoctorado
        exclude = ['usuario', ]
