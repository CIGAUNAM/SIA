from SIA.widgets import *
from .models import *
from django import forms

from nucleo.models import Institucion
from django_select2.forms import Select2MultipleWidget, ModelSelect2Widget, Select2Widget


#

class AsesoriaEstudianteForm(forms.ModelForm):
    asesorado = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Asesorado",
        widget=ModelSelect2Widget(
            search_fields=['first_name__icontains', 'last_name__icontains', 'username__icontains'],
            queryset=User.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    tipo = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
                             choices=(('', 'Seleccionar tipo de Asesoría'), ('RESIDENCIA', 'Residencia'),
                                      ('PRACTICA', 'Prácticas profesionales'),
                                      ('ESTANCIA', 'Estancia de investigación'),
                                      ('ASESORIA_TECNICA', 'Asesoría técnica'), ('SERVICIO_SOCIAL', 'Servicio Social')),
                             required=True)
    nivel_academico = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        choices=getattr(settings, 'NIVEL_ACADEMICO', ), required=True)
    programa = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)

    beca = forms.ModelChoiceField(
        required=False,
        queryset=Beca.objects.all(),
        label="Beca",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Beca.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    proyecto = forms.ModelChoiceField(
        required=False,
        queryset=ProyectoInvestigacion.objects.all(),
        label="Proyecto",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=ProyectoInvestigacion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    institucion = forms.ModelChoiceField(
        queryset=Institucion.objects.all(),
        label="Institución",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Institucion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    dependencia = forms.ModelChoiceField(
        queryset=Dependencia.objects.all(),
        label="Dependencia",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            dependent_fields={'institucion': 'institucion'},
            queryset=Dependencia.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    periodo_academico = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True,
                                        label='Semestre/Año académico')
    fecha_inicio = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=True)
    fecha_fin = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=True)

    class Meta:
        model = AsesoriaEstudiante
        exclude = ['usuario', ]


class SupervisionInvestigadorPostDoctoralForm(forms.ModelForm):
    investigador = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Investigador",
        widget=ModelSelect2Widget(
            search_fields=['first_name__icontains', 'last_name__icontains', 'username__icontains'],
            queryset=User.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    titulo_proyecto = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True,
                                      label='Disciplina')
    institucion2 = forms.ModelChoiceField(
        queryset=Institucion.objects.all(),
        label="Institución",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Institucion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    dependencia = forms.ModelChoiceField(
        queryset=Dependencia.objects.all(),
        label="Dependencia",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            dependent_fields={'institucion': 'institucion'},
            queryset=Dependencia.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    proyecto = forms.ModelChoiceField(
        required=True,
        queryset=ProyectoInvestigacion.objects.all(),
        label="Proyecto",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=ProyectoInvestigacion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    beca = forms.ModelChoiceField(
        required=False,
        queryset=Beca.objects.all(),
        label="Beca",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Beca.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )

    fecha_inicio = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=True)
    fecha_fin = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=True)

    class Meta:
        model = SupervisionInvestigadorPostDoctoral
        exclude = ['usuario', ]
        widgets = {
        }


class DesarrolloGrupoInvestigacionInternoForm(forms.ModelForm):
    nombre = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)
    fecha_inicio = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=True)
    fecha_fin = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=True)
    pais = forms.ModelChoiceField(
        required=True,
        queryset=Pais.objects.all(),
        label="Pais",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Pais.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )

    class Meta:
        model = DesarrolloGrupoInvestigacionInterno
        exclude = []
        widgets = {
            "usuarios": Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class DireccionTesisForm(forms.ModelForm):
    titulo_tesis = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)
    programa = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)
    asesorado = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Asesorado",
        widget=ModelSelect2Widget(
            search_fields=['first_name__icontains', 'last_name__icontains', 'username__icontains'],
            queryset=User.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    director = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Director",
        widget=ModelSelect2Widget(
            search_fields=['first_name__icontains', 'last_name__icontains', 'username__icontains'],
            queryset=User.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    codirector = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Co-director",
        widget=ModelSelect2Widget(
            search_fields=['first_name__icontains', 'last_name__icontains', 'username__icontains'],
            queryset=User.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    nivel_academico = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        choices=getattr(settings, 'NIVEL_ACADEMICO', ), required=True)
    status = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
                               choices=(
                               ('', '-------'), ('EN_PROCESO', 'Tesis en proceso'), ('TERMINADA', 'Tesis terminada')),
                               required=True)

    institucion2 = forms.ModelChoiceField(
        queryset=Institucion.objects.all(),
        label="Institución",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Institucion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    dependencia = forms.ModelChoiceField(
        queryset=Dependencia.objects.all(),
        label="Dependencia",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            dependent_fields={'institucion': 'institucion'},
            queryset=Dependencia.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    beca = forms.ModelChoiceField(
        required=False,
        queryset=Beca.objects.all(),
        label="Beca",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Beca.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    reconocimiento_text = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}))

    fecha_examen = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=False)
    fecha_inicio = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=True)
    fecha_fin = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=True)

    class Meta:
        model = DireccionTesis
        exclude = []
        widgets = {
            "tutores": wSortedSelect2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class ComiteTutoralForm(forms.ModelForm):
    estudiante = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Estudiante",
        widget=ModelSelect2Widget(
            search_fields=['first_name__icontains', 'last_name__icontains', 'username__icontains'],
            queryset=User.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    programa = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)
    titulo_tesis = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)
    institucion2 = forms.ModelChoiceField(
        queryset=Institucion.objects.all(),
        label="Institución",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Institucion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    dependencia = forms.ModelChoiceField(
        queryset=Dependencia.objects.all(),
        label="Dependencia",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            dependent_fields={'institucion': 'institucion'},
            queryset=Dependencia.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    fecha_inicio = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=True)
    fecha_fin = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=False)
    fecha_examen = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=False)

    class Meta:
        model = ComiteTutoral
        exclude = []
        widgets = {
            'miembros_comite': Select2MultipleWidget(
                attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class ComiteCandidaturaDoctoralForm(forms.ModelForm):
    candidato = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Asesorado",
        widget=ModelSelect2Widget(
            search_fields=['first_name__icontains', 'last_name__icontains', 'username__icontains'],
            queryset=User.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    titulo_tesis = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)
    proyecto = forms.ModelChoiceField(
        required=False,
        queryset=ProyectoInvestigacion.objects.all(),
        label="Proyecto de investigación",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=ProyectoInvestigacion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    programa_doctorado = forms.ModelChoiceField(
        queryset=ProgramaDoctorado.objects.all(),
        label="Programa de doctorado",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=ProgramaDoctorado.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    institucion = forms.ModelChoiceField(
        queryset=Institucion.objects.all(),
        label="Institución",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Institucion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    dependencia = forms.ModelChoiceField(
        queryset=Dependencia.objects.all(),
        label="Dependencia",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            dependent_fields={'institucion': 'institucion'},
            queryset=Dependencia.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    fecha_defensa = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=True)

    class Meta:
        model = ComiteCandidaturaDoctoral
        exclude = []
        widgets = {
            'miembros_comite': wSortedSelect2MultipleWidget(
                attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }
