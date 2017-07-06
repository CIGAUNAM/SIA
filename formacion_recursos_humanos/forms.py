from SIA.widgets import *
from . models import *
from django import forms

from nucleo.models import Institucion
from django_select2.forms import Select2MultipleWidget
#

class AsesorEstanciaForm(forms.ModelForm):
    asesorado = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Asesorado",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            #dependent_fields={'dependencia': 'dependencia'},
        )
    )
    descripcion = forms.CharField(widget=wTextarea, required=False)
    tipo = forms.ChoiceField(widget=Select3Widget, choices=(('RESIDENCIA', 'Residencia'), ('PRACTICA', 'Práctica'), ('ESTANCIA', 'Estancia'), ('SERVICIO_SOCIAL', 'Servicio Social'), ('OTRO', 'Otro')), required=True)
    grado_academico = forms.ChoiceField(widget=Select3Widget, choices=getattr(settings, 'GRADO_ACADEMICO', ), required=True)
    programa_licenciatura = forms.ModelChoiceField(
        required=False,
        queryset=ProgramaLicenciatura.objects.all(),
        label="Programa de licenciatura",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            # dependent_fields={'dependencia': 'dependencia'},
        )
    )
    programa_maestria = forms.ModelChoiceField(
        required=False,
        queryset=ProgramaMaestria.objects.all(),
        label="Programa de mestria",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            # dependent_fields={'dependencia': 'dependencia'},
        )
    )
    programa_doctorado = forms.ModelChoiceField(
        required=False,
        queryset=ProgramaDoctorado.objects.all(),
        label="Programa de doctorado",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            # dependent_fields={'dependencia': 'dependencia'},
        )
    )
    beca = forms.ModelChoiceField(
        required=False,
        queryset=Beca.objects.all(),
        label="Beca",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            # dependent_fields={'dependencia': 'dependencia'},
        )
    )
    proyecto = forms.ModelChoiceField(
        required=False,
        queryset=Proyecto.objects.all(),
        label="Proyecto",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            # dependent_fields={'dependencia': 'dependencia'},
        )
    )
    institucion = forms.ModelChoiceField(
        required=False,
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
    fecha_inicio = forms.CharField(widget=wDateField, required=True)
    fecha_fin = forms.CharField(widget=wDateField, required=True)

    class Meta:
        model = AsesorEstancia
        exclude = ['usuario',]


class DireccionTesisForm(forms.ModelForm):
    titulo = forms.CharField(widget=wCharField, required=True)
    asesorado = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Asesorado",
        widget=ModelSelect3Widget(
            search_fields=['first_name__icontains'],
        )
    )
    descripcion = forms.CharField(widget=wTextarea, required=False)
    grado_academico = forms.ChoiceField(widget=Select3Widget, choices=getattr(settings, 'GRADO_ACADEMICO', ), required=True)
    institucion = forms.ModelChoiceField(
        required=False,
        queryset=Institucion.objects.all(),
        label="Institución",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            # dependent_fields={'dependencia': 'dependencia'},
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
    beca = forms.ModelChoiceField(
        required=False,
        queryset=Beca.objects.all(),
        label="Beca",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            # dependent_fields={'dependencia': 'dependencia'},
        )
    )
    reconocimiento = forms.ModelChoiceField(
        required=False,
        queryset=Reconocimiento.objects.all(),
        label="Reconocimiento",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            # dependent_fields={'dependencia': 'dependencia'},
        )
    )
    fecha_examen = forms.CharField(widget=wDateField, required=True)

    class Meta:
        model = DireccionTesis
        exclude = ['usuario',]


class ComiteTutoralForm(forms.ModelForm):
    grado_academico = forms.ChoiceField(widget=Select3Widget, choices=(('MAESTRIA', 'Maestría'), ('DOCTORADO', 'Doctorado')), required=True)
    programa_maestria = forms.ModelChoiceField(
        required=False,
        queryset=ProgramaMaestria.objects.all(),
        label="Programa de maestria",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    programa_doctorado = forms.ModelChoiceField(
        required=False,
        queryset=ProgramaDoctorado.objects.all(),
        label="Programa de doctorado",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    status = forms.ChoiceField(widget=Select3Widget, choices=(('EN_PROCESO', 'En proceso'), ('CONCLUIDO', 'Concluído')), required=True)
    fecha_inicio = forms.CharField(widget=wDateField, required=True)
    fecha_fin = forms.CharField(widget=wDateField, required=False)
    asesorado = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Asesorado",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    asesor_principal = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Asesor principal",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    proyecto = forms.ModelChoiceField(
        required=False,
        queryset=Proyecto.objects.all(),
        label="Proyecto",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    institucion = forms.ModelChoiceField(
        required=False,
        queryset=Institucion.objects.all(),
        label="Institución",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
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
        model = ComiteTutoral
        exclude = []
        widgets = {
            'otros_asesores': Select3MultipleWidget,
            'sinodales': Select3MultipleWidget,
        }


class ComiteCandidaturaDoctoralForm(forms.ModelForm):
    asesorado = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Asesorado",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    asesor_principal = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Asesor principal",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    proyecto = forms.ModelChoiceField(
        required=False,
        queryset=Proyecto.objects.all(),
        label="Proyecto",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    programa_doctorado = forms.ModelChoiceField(
        queryset=ProgramaDoctorado.objects.all(),
        label="Programa de doctorado",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    institucion = forms.ModelChoiceField(
        required=False,
        queryset=Institucion.objects.all(),
        label="Institución",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
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
    fecha_defensa = forms.CharField(widget=wDateField, required=True)

    class Meta:
        model = ComiteCandidaturaDoctoral
        exclude = []
        widgets = {
            'otros_asesores': Select3MultipleWidget,
            'sinodales': Select3MultipleWidget,
        }