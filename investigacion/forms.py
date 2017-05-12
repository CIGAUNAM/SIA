from SIA.widgets import *

from .models import *
from nucleo.models import Libro as LibroInvestigacion
from nucleo.models import Proyecto as ProyectoInvestigacion, ProblemaNacionalConacyt
# from nucleo.models import ProblemaNacionalConacyt, Metodologia, AreaEspecialidad, ImpactoSocial, Financiamiento


from django import forms

from django.conf import settings
from django_select2.forms import Select2MultipleWidget

from django_select2.forms import Select2Widget, ModelSelect2MultipleWidget


#

class ArticuloCientificoForm(forms.ModelForm):
    titulo = forms.CharField(widget=wCharField, required=True, label='Título de artículo')
    descripcion = forms.CharField(widget=wTextarea, required=False, label='Descripción')
    tipo = forms.ChoiceField(widget=Select3Widget, choices=(
    ('ARTICULO', 'Artículo'), ('ACTA', 'Acta'), ('CARTA', 'Carta'), ('RESENA', 'Reseña'), ('OTRO', 'Otro')),
                             required=True)
    status = forms.ChoiceField(widget=Select3Widget, choices=getattr(settings, 'STATUS_PUBLICACION', ), required=True)
    solo_electronico = forms.BooleanField()
    nombre_abreviado_wos = forms.CharField(widget=wCharField, required=False, label='Nombre abreviado WOS')
    url = forms.CharField(widget=wCharField, required=False)  # corregir valiadr url
    fecha = forms.CharField(widget=wDateField, required=True, label='Fecha de publicación')
    revista = forms.ModelChoiceField(
        queryset=Revista.objects.all(),
        label="Revista",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            # dependent_fields={'dependencia': 'dependencia'},
        )
    )
    volumen = forms.CharField(widget=wCharField, required=False)
    numero = forms.CharField(widget=wNumberField, required=False, label='Número')
    issn_impreso = forms.CharField(widget=wCharField, required=False, label='ISSN Impreso')
    issn_online = forms.CharField(widget=wCharField, required=False, label='ISSN Impreso')
    pagina_inicio = forms.CharField(widget=wNumberField, required=True, label='Número de página donde inicia')
    pagina_fin = forms.CharField(widget=wNumberField, required=True, label='Número de página final')
    id_doi = forms.CharField(widget=wCharField, required=False, label='ID DOI')
    id_wos = forms.CharField(widget=wCharField, required=False, label='ID WOS')

    # proyectos = forms.ModelMultipleChoiceField(Proyecto)

    class Meta:
        model = ArticuloCientifico
        exclude = []
        widgets = {
            'usuarios': Select2MultipleWidget,
            'alumnos': Select2MultipleWidget,
            'indices': Select2MultipleWidget,
            'proyectos': Select2MultipleWidget,
        }


class CapituloLibroInvestigacionForm(forms.ModelForm):
    titulo = forms.CharField(widget=wCharField, required=True, label='Título del capítulo')
    descripcion = forms.CharField(widget=wTextarea, required=False)
    libro = forms.ModelChoiceField(
        queryset=Libro.objects.all(),
        label="Libro",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            # dependent_fields={'dependencia': 'dependencia'},
        )
    )
    pagina_inicio = forms.CharField(widget=wNumberField, required=True, label='Número de página donde inicia')
    pagina_fin = forms.CharField(widget=wNumberField, required=True, label='Número de página final')

    class Meta:
        model = CapituloLibroInvestigacion
        exclude = ['usuario', ]
        widgets = {
            'proyectos': Select2MultipleWidget,
        }


class MapaArbitradoForm(forms.ModelForm):
    titulo = forms.CharField(widget=wCharField, required=True, label='Título del mapa')
    descripcion = forms.CharField(widget=wTextarea, required=False)
    escala = forms.CharField(widget=wCharField, required=True, label='Escala')
    status = forms.ChoiceField(widget=wSelect, choices=getattr(settings, 'STATUS_PUBLICACION', ), required=True)
    pais = forms.ModelChoiceField(
        queryset=Pais.objects.all(),
        label="Pais",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    estado = forms.ModelChoiceField(
        queryset=Estado.objects.all(),
        label="Estado",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            dependent_fields={'pais': 'pais'},
        )
    )
    ciudad = forms.ModelChoiceField(
        queryset=Ciudad.objects.all(),
        label="Ciudad",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            dependent_fields={'estado': 'estado'},
        )
    )
    editorial = forms.ModelChoiceField(
        queryset=Editorial.objects.all(),
        label="Editorial",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    fecha = forms.CharField(widget=wDateField, required=True, label='fecha de liberación')
    numero_edicion = forms.CharField(widget=wNumberField, required=True, label='Número de edición')
    numero_paginas = forms.CharField(widget=wNumberField, required=True, label='Número de páginas')
    coleccion = forms.ModelChoiceField(
        queryset=Coleccion.objects.all(),
        label="Coleccion",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    volumen = forms.CharField(widget=wCharField, required=False)
    isbn = forms.CharField(widget=wCharField, required=False)
    url = forms.CharField(widget=wCharField, required=False)  # corregir valiadr url

    class Meta:
        model = MapaArbitrado
        exclude = []
        widgets = {
            'usuarios': Select2MultipleWidget,
            'editores': Select2MultipleWidget,
            'coordinadores': Select2MultipleWidget,
            'proyectos': Select2MultipleWidget,
        }


class InformeTecnicoForm(forms.ModelForm):
    titulo = forms.CharField(widget=wCharField, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    fecha = forms.CharField(widget=wDateField, required=True)
    numero_paginas = forms.CharField(widget=wNumberField, required=True)
    url = forms.CharField(widget=wCharField, required=False)  # corregir valiadr url

    class Meta:
        model = InformeTecnico
        exclude = []
        widgets = {
            'usuarios': Select2MultipleWidget,
            'proyectos': Select2MultipleWidget,
        }


class LibroInvestigacionForm(forms.ModelForm):
    nombre = forms.CharField(widget=wCharField, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    pais = forms.ModelChoiceField(
        queryset=Pais.objects.all(),
        label="Pais",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    estado = forms.ModelChoiceField(
        queryset=Estado.objects.all(),
        label="Estado",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            dependent_fields={'pais': 'pais'},
        )
    )
    ciudad = forms.ModelChoiceField(
        queryset=Ciudad.objects.all(),
        label="Ciudad",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            dependent_fields={'estado': 'estado'},
        )
    )
    editorial = forms.ModelChoiceField(
        queryset=Editorial.objects.all(),
        label="Editorial",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    status = forms.ChoiceField(widget=wSelect, choices=getattr(settings, 'STATUS_PUBLICACION', ))
    fecha = forms.CharField(widget=wDateField)
    numero_edicion = forms.CharField(widget=wNumberField)
    numero_paginas = forms.CharField(widget=wNumberField)
    coleccion = forms.ModelChoiceField(
        queryset=Coleccion.objects.all(),
        label="Coleccion",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    volumen = forms.CharField(widget=wCharField, required=False)
    isbn = forms.CharField(widget=wCharField, required=False)
    url = forms.CharField(widget=wCharField, required=False)  # corregir valiadr url

    class Meta:
        model = LibroInvestigacion
        exclude = ['tipo', ]
        widgets = {
            'usuarios': Select2MultipleWidget,
            'editores': Select2MultipleWidget,
            'coordinadores': Select2MultipleWidget,
            'proyectos': Select2MultipleWidget,
        }


class ProyectoInvestigacionForm(forms.ModelForm):
    nombre = forms.CharField(widget=wCharField, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    es_permanente = forms.BooleanField()
    fecha_inicio = forms.CharField(widget=wDateField)
    fecha_fin = forms.CharField(widget=wDateField)
    status = forms.ChoiceField(widget=wSelect, choices=getattr(settings, 'STATUS_PROYECTO', ))
    clasificacion = forms.ChoiceField(widget=wSelect, choices=getattr(settings, 'CLASIFICACION_PROYECTO', ))
    organizacion = forms.ChoiceField(widget=wSelect, choices=getattr(settings, 'ORGANIZACION_PROYECTO', ))
    modalidad = forms.ChoiceField(widget=wSelect, choices=getattr(settings, 'MODALIDAD_PROYECTO', ))
    tematica_genero = forms.BooleanField()
    problema_nacional_conacyt = forms.ModelChoiceField(
        queryset=ProblemaNacionalConacyt.objects.all(),
        label="Problema Nacional Conacyt",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    descripcion_problema_nacional_conacyt = forms.CharField(widget=wTextarea, required=False)

    class Meta:
        model = ProyectoInvestigacion
        exclude = ['tipo', ]
        widgets = {
            'problemas_nacionales_conacyt': Select2MultipleWidget,
            'usuarios': Select2MultipleWidget,
            'participantes': Select2MultipleWidget,
            'dependencias': Select2MultipleWidget,
            'financiamientos': Select2MultipleWidget,
            'metodologias': Select2MultipleWidget,
            'especialidades': Select2MultipleWidget,
            'impactos_sociales': Select2MultipleWidget,
            'tecnicos': Select2MultipleWidget,
            'alumnos_doctorado': Select2MultipleWidget,
            'alumnos_maestria': Select2MultipleWidget,
            'alumnos_licenciatura': Select2MultipleWidget,
        }
