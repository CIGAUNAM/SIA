from SIA.widgets import *
from . models import *
from django import forms
from nucleo.models import Institucion, Pais, Estado, Ciudad, Editorial, Coleccion, Libro as LibroDocencia
from django_select2.forms import Select2MultipleWidget, Select2Widget, ModelSelect2Widget

#

class CursoDocenciaEscolarizadoForm(forms.ModelForm):
    nivel = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}), choices=(('', 'Seleccionar nivel de curso'), ('LICENCIATURA', 'Licenciatura'), ('MAESTRIA', 'Maestría'), ('DOCTORADO', 'Doctorado')), required=True)
    licenciatura = forms.ModelChoiceField(
        required=False,
        queryset=ProgramaLicenciatura.objects.all(),
        label="Programa de licenciatura",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=ProgramaLicenciatura.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    maestria = forms.ModelChoiceField(
        required=False,
        queryset=ProgramaMaestria.objects.all(),
        label="Programa de maestría",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=ProgramaMaestria.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    doctorado = forms.ModelChoiceField(
        required=False,
        queryset=ProgramaDoctorado.objects.all(),
        label="Programa de doctorado",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=ProgramaDoctorado.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    asignatura = forms.ModelChoiceField(
        queryset=Asignatura.objects.all(),
        label="Asignatura",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Asignatura.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    modalidad = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}), choices=(('', 'Seleccionar modalidad de curso'), ('PRESENCIAL', 'Presencial'), ('EN_LINEA', 'En línea'), ('MIXTO', 'Mixto')), required=True)
    nombramiento = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
                              choices=(('', '-------'), ('TITULAR', 'Titular o Coordinador'), ('COLABORADOR', 'Colaborador o Invitado')), required=True)
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
    fecha_inicio = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    fecha_fin = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    total_horas = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}), required=True)
    periodo_academico = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True, label='Semestre/Año académico')

    class Meta:
        model = CursoDocenciaEscolarizado
        exclude = ['usuario', ]


class CursoDocenciaExtracurricularForm(forms.ModelForm):
    asignatura = forms.ModelChoiceField(
        queryset=Asignatura.objects.all(),
        label="Asignatura",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Asignatura.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    tipo = forms.ModelChoiceField(
        queryset=TipoCurso.objects.all(),
        label="Tipo de curso",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=TipoCurso.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    modalidad = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}), choices=(('', 'Seleccionar modalidad de curso'), ('PRESENCIAL', 'Presencial'), ('EN_LINEA', 'En línea'), ('MIXTO', 'Mixto')), required=True)
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
    fecha_inicio = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    fecha_fin = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    total_horas = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}), required=True)
    periodo_academico = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True, label='Semestre/Año académico')

    class Meta:
        model = CursoDocenciaExtracurricular
        exclude = ['usuario', ]
        widgets = {
        }


class ArticuloDocenciaForm(forms.ModelForm):
    titulo = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True, label='Título de artículo')
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
                                  required=False, label='Descripción')
    status = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
                               choices=getattr(settings, 'STATUS_PUBLICACION_ARTICULO', ), required=True)
    solo_electronico = forms.BooleanField(required=False)
    url = forms.URLField(widget=URLInput(attrs={'class': 'form-control pull-right'}), required=False)
    fecha = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=True, label='Fecha de publicación')
    revista = forms.ModelChoiceField(
        queryset=Revista.objects.all(),
        label="Revista",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Revista.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    volumen = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False)
    numero = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False,
                             label='Número')
    pagina_inicio = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}),
                                    required=True, label='Número de página donde inicia')
    pagina_fin = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}),
                                 required=True, label='Número de página final')

    class Meta:
        model = ArticuloDocencia
        exclude = []
        widgets = {
            "autores": wSortedSelect2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'alumnos': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'agradecimientos': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class LibroDocenciaForm(forms.ModelForm): # Posiblemente MANTENER, creo que estaba duplicado (borrar el otro)
    nombre = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}), required=False)
    pais = forms.ModelChoiceField(
        queryset=Pais.objects.all(),
        label="Pais",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Pais.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    ciudad_text = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}))
    editorial_text = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}))
    coleccion_text = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}))
    status = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        choices=getattr(settings, 'STATUS_PUBLICACION_LIBRO', ), required=True)
    tipo_participacion = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        choices=(('AUTORIA', 'Autoría'), ('COMPILACION', 'Compilación')), required=True)
    fecha = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=False)
    numero_edicion = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}))
    numero_paginas = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}))

    volumen = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False)
    isbn = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False)
    url = forms.URLField(widget=URLInput(attrs={'class': 'form-control pull-right'}), required=False)
    class Meta:
        model = LibroDocencia
        exclude = ['tipo', ]
        widgets = {
            "autores": wSortedSelect2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'coordinadores': wSortedSelect2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'prologo': wSortedSelect2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'agradecimientos': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class ProgramaEstudioForm(forms.ModelForm):
    nombre = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True,
                             label='Nombre del programa de estudio.')
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
                                  required=False, label='Descripción')
    nivel = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
                             choices=(
                                 ('', 'Seleccionar un nivel académico'), ('LICENCIATURA', 'Licenciatura'), ('MAESTRIA', 'Maestría'),
                                 ('DOCTORADO', 'Doctorado'), ('OTRO', 'Otro')), required=True)
    fecha = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=True, label='Fecha de publicación')
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
        model = ProgramaEstudio
        exclude = ['usuario', ]