from SIA.widgets import *

from .models import *
from nucleo.models import Libro as LibroInvestigacion
from nucleo.models import ProblemaNacionalConacyt


from django import forms

from django.conf import settings
from django_select2.forms import Select2Widget, ModelSelect2Widget, ModelSelect2MultipleWidget, Select2MultipleWidget

#

class ArticuloCientificoForm(forms.ModelForm):
    titulo = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True,
                             label='Título de artículo')
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
    id_doi = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False,
                             label='ID DOI')
    id_wos = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False,
                             label='ID WOS')
    factor_impacto = forms.DecimalField(max_digits=5, decimal_places=3,
        required=False,
        widget=TextInput(attrs={'min': 0, 'class': 'form-control pull-right', 'step': '0.001'}),
        label='Factor de impácto')
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

    class Meta:
        model = ArticuloCientifico
        exclude = []
        widgets = {
            'autores': wSortedSelect2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'alumnos': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'agradecimientos': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class CapituloLibroInvestigacionForm(forms.ModelForm):
    titulo = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True,
                             label='Título del capítulo')
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
                                  required=False)
    libro = forms.ModelChoiceField(
        queryset=LibroInvestigacion.objects.filter(tipo='INVESTIGACION'),
        label="Libro",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=LibroInvestigacion.objects.filter(tipo='INVESTIGACION'),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    pagina_inicio = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}),
                                    required=True, label='Número de página donde inicia')
    pagina_fin = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}),
                                 required=True, label='Número de página final')
    class Meta:
        model = CapituloLibroInvestigacion
        exclude = []
        widgets = {
            "autores": wSortedSelect2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class MapaArbitradoForm(forms.ModelForm):
    titulo = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True,
                             label='Título del mapa')
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
                                  required=False)
    escala = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True,
                             label='Escala')
    status = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
                               choices=getattr(settings, 'STATUS_PUBLICACION_LIBRO', ), required=True)
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
    estado = forms.ModelChoiceField(
        required=True,
        queryset=Estado.objects.all(),
        label="Estado",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            dependent_fields={'pais': 'pais'},
            queryset=Estado.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    ciudad = forms.ModelChoiceField(
        queryset=Ciudad.objects.all(),
        label="Ciudad",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            dependent_fields={'estado': 'estado'},
            queryset=Ciudad.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    editorial = forms.ModelChoiceField(
        queryset=Editorial.objects.all(),
        label="Editorial",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Editorial.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    fecha = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=True, label='fecha de liberación')
    numero_edicion = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}),
                                     required=True, label='Número de edición')
    numero_paginas = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}),
                                     required=True, label='Número de páginas')
    coleccion = forms.ModelChoiceField(
        required=False,
        queryset=Coleccion.objects.all(),
        label="Coleccion",
        widget=ModelSelect2Widget(
            required=False,
            search_fields=['nombre__icontains'],
            queryset=Coleccion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    volumen = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False)
    isbn = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False)
    url = forms.URLField(widget=URLInput(attrs={'class': 'form-control pull-right'}), required=False)
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

    class Meta:
        model = MapaArbitrado
        exclude = []
        widgets = {
            "autores": wSortedSelect2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'editores': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'coordinadores': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class InformeTecnicoForm(forms.ModelForm):
    titulo = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
                                  required=False)
    fecha = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=True)
    numero_paginas = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}),
                                     required=True)
    url = forms.URLField(widget=URLInput(attrs={'class': 'form-control pull-right'}), required=False)
    proyecto = forms.ModelChoiceField(
        required=True,
        queryset=ProyectoInvestigacion.objects.all(),
        label="Proyecto de investigación",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=ProyectoInvestigacion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    es_publico = forms.BooleanField(required=False)

    class Meta:
        model = InformeTecnico
        exclude = []
        widgets = {
            "autores": Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class ProyectoInvestigacionForm(forms.ModelForm):
    es_permanente = forms.BooleanField(required=False)
    fecha_inicio = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=True, label='Fecha de inicio')
    fecha_fin = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=False, label='Fecha de fin')
    institucion = forms.ModelChoiceField(
        queryset=Institucion.objects.all(),
        label="Institución",
        widget=ModelSelect2Widget(
            search_fields=['nombre_institucion__icontains'],
            queryset=Institucion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    dependencia = forms.ModelChoiceField(
        queryset=Dependencia.objects.all(),
        label="Dependencia",
        widget=ModelSelect2Widget(
            search_fields=['nombre_dependencia__icontains'],
            dependent_fields={'institucion': 'institucion'},
            queryset=Dependencia.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    status = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        choices=getattr(settings, 'STATUS_PROYECTO'), required=True)
    clasificacion = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        choices=getattr(settings, 'CLASIFICACION_PROYECTO'), required=True)
    organizacion = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        choices=getattr(settings, 'ORGANIZACION_PROYECTO'), required=True)
    modalidad = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        choices=getattr(settings, 'MODALIDAD_PROYECTO'), required=True)
    tipo_financiamiento = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        choices=(('', '-------'), ('CONACYT', 'CONACYT'), ('PAPIIT', 'DGAPA-PAPIIT'), ('PAPIME', 'DGAPA-PAPIME'), ('EXTRAORDINARIOS', 'Ingresos extraordinarios'), ('SIN_RECURSOS', 'Sin recursos en el CIGA')), required=True)
    financiamiento_extraordinario = forms.ModelChoiceField(
        queryset=Dependencia.objects.all(),
        required=False,
        label="Dependencia",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Dependencia.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    financiamiento_sin_recurso_ciga = forms.ModelChoiceField(
        queryset=Dependencia.objects.all(),
        required=False,
        label="Dependencia",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Dependencia.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    tematica_genero = forms.BooleanField(required=False)
    problema_nacional_conacyt = forms.ModelChoiceField(
        queryset=ProblemaNacionalConacyt.objects.all(),
        label="Problema Nacional Conacyt",
        widget=ModelSelect2Widget(
            queryset=ProblemaNacionalConacyt.objects.all(),
            search_fields=['nombre__icontains'],
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        ),
        required=False
    )
    metodologias_text = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False, label='Metodologías')
    impacto_social_text = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False, label='Impacto social')
    num_alumnos_doctorado = forms.IntegerField(widget=NumberInput(attrs={'min': 0, 'class': 'form-control pull-right'}), required=True, label='Número de alumnos de doctorado', initial='0')
    num_alumnos_maestria = forms.IntegerField(widget=NumberInput(attrs={'min': 0, 'class': 'form-control pull-right'}), required=True, label='Número de alumnos de maestría', initial='0')
    num_alumnos_licenciatura = forms.IntegerField(widget=NumberInput(attrs={'min': 0, 'class': 'form-control pull-right'}), required=True, label='Número de alumnos de doctorado', initial='0')

    class Meta:
        model = ProyectoInvestigacion
        exclude = []
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
            'otro_problema_nacional_conacyt': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
            "responsables": wSortedSelect2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'participantes': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'dependencias': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            "financiamientos": Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'financiamiento_conacyt': TextInput(attrs={'class': 'form-control pull-right'}),
            'financiamiento_papiit': TextInput(attrs={'class': 'form-control pull-right'}),
            'financiamiento_papime': TextInput(attrs={'class': 'form-control pull-right'}),
            'metodologias': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'especialidades': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'areas_especialidad_wos': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'impactos_sociales': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'tecnicos': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'alumnos_doctorado': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'alumnos_maestria': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'alumnos_licenciatura': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'problemas_nacionales_conacyt': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'dependencias_colaboracion': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class LibroInvestigacionForm(forms.ModelForm): # Posiblemente MANTENER, creo que estaba duplicado (borrar el otro)
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
    coleccion_text = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False)

    status = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        choices=getattr(settings, 'STATUS_PUBLICACION_LIBRO', ), required=True)
    tipo_participacion = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        choices=(('', '-------'), ('AUTORIA', 'Autoría'), ('COMPILACION', 'Compilación')), required=True)
    fecha = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}))
    numero_edicion = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}))
    numero_paginas = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}))
    volumen = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False)
    isbn = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False)
    url = forms.URLField(widget=URLInput(attrs={'class': 'form-control pull-right'}), required=False)

    class Meta:
        model = LibroInvestigacion
        exclude = ['tipo', ]
        widgets = {
            "autores": wSortedSelect2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'coordinadores': wSortedSelect2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'prologo': wSortedSelect2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'agradecimientos': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }