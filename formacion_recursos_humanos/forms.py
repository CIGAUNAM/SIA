from SIA.widgets import *
from . models import *
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
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}), required=False)
    tipo = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}), choices=(('', 'Seleccionar tipo de Asesoría'), ('RESIDENCIA', 'Residencia'), ('PRACTICA', 'Prácticas profesionales'), ('ESTANCIA', 'Estancia de investigación'), ('BECARIO', 'Becario de proyecto de investigación'), ('SERVICIO_SOCIAL', 'Servicio Social')), required=True)
    nivel_academico = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}), choices=getattr(settings, 'NIVEL_ACADEMICO', ), required=True)
    programa_licenciatura = forms.ModelChoiceField(
        required=False,
        queryset=ProgramaLicenciatura.objects.all(),
        label="Programa de licenciatura",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=ProgramaLicenciatura.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    programa_maestria = forms.ModelChoiceField(
        required=False,
        queryset=ProgramaMaestria.objects.all(),
        label="Programa de mestria",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=ProgramaMaestria.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    programa_doctorado = forms.ModelChoiceField(
        required=False,
        queryset=ProgramaDoctorado.objects.all(),
        label="Programa de doctorado",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=ProgramaDoctorado.objects.all(),
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
    fecha_inicio = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    fecha_fin = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)

    class Meta:
        model = AsesoriaEstudiante
        exclude = ['usuario',]


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
    disciplina = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True, label='Disciplina')
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
            'articulos': wSortedSelect2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'libros': wSortedSelect2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'capitulos_libros': wSortedSelect2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
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
        required=False,
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
            'usuarios': wSortedSelect2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }





class DireccionTesisForm(forms.ModelForm):
    titulo = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)
    especialidad = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)
    asesorado = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Asesorado",
        widget=ModelSelect2Widget(
            search_fields=['first_name__icontains', 'last_name__icontains', 'username__icontains'],
            queryset=User.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}), required=False)
    nivel_academico = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}), choices=getattr(settings, 'NIVEL_ACADEMICO', ), required=True)
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
    """
    reconocimiento = forms.ModelChoiceField(
        required=False,
        queryset=Reconocimiento.objects.all(),
        label="Reconocimiento",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Reconocimiento.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    """
    fecha_examen = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)

    class Meta:
        model = DireccionTesis
        exclude = []
        widgets = {
            'usuarios': wSortedSelect2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class ComiteTutoralForm(forms.ModelForm):
    grado_academico = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}), choices=(('', 'Seleccionar grado académico'), ('MAESTRIA', 'Maestría'), ('DOCTORADO', 'Doctorado')), required=True)
    programa_maestria = forms.ModelChoiceField(
        required=False,
        queryset=ProgramaMaestria.objects.all(),
        label="Programa de maestria",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=ProgramaMaestria.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    programa_doctorado = forms.ModelChoiceField(
        required=False,
        queryset=ProgramaDoctorado.objects.all(),
        label="Programa de doctorado",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=ProgramaDoctorado.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    status = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}), choices=(('', 'Seleccionar status'), ('EN_PROCESO', 'En proceso'), ('CONCLUIDO', 'Concluído')), required=True)
    fecha_inicio = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    fecha_fin = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=False)
    asesorado = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Asesorado",
        widget=ModelSelect2Widget(
            search_fields=['first_name__icontains', 'last_name__icontains', 'username__icontains'],
            queryset=User.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    asesor_principal = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Asesor principal",
        widget=ModelSelect2Widget(
            search_fields=['first_name__icontains', 'last_name__icontains', 'username__icontains'],
            queryset=User.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'},
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

    class Meta:
        model = ComiteTutoral
        exclude = []
        widgets = {
            'otros_asesores': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'sinodales': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class ComiteCandidaturaDoctoralForm(forms.ModelForm):
    asesorado = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Asesorado",
        widget=ModelSelect2Widget(
            search_fields=['first_name__icontains', 'last_name__icontains', 'username__icontains'],
            queryset=User.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    asesor_principal = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Asesor principal",
        widget=ModelSelect2Widget(
            search_fields=['first_name__icontains', 'last_name__icontains', 'username__icontains'],
            queryset=User.objects.all(),
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
    fecha_defensa = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)

    class Meta:
        model = ComiteCandidaturaDoctoral
        exclude = []
        widgets = {
            'otros_asesores': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'sinodales': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }