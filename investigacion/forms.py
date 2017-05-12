from SIA.widgets import *

from .models import *
from nucleo.models import Libro as LibroInvestigacion
from nucleo.models import Proyecto as ProyectoInvestigacion
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
    revista = forms.ModelChoiceField(
        queryset=Revista.objects.all(),
        label="Revista",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            # dependent_fields={'dependencia': 'dependencia'},
        )
    )
    status = forms.ChoiceField(widget=Select3Widget, choices=getattr(settings, 'STATUS_PUBLICACION', ), required=True)
    solo_electronico = forms.BooleanField()
    nombre_abreviado_wos = forms.CharField(widget=wCharField, required=False)
    url = forms.CharField(widget=wCharField, required=False)  # corregir valiadr url
    fecha = forms.CharField(widget=wDateField, required=True)
    volumen = forms.CharField(widget=wCharField, required=False)
    numero = forms.CharField(widget=wNumberField, required=False)
    issn_impreso = forms.CharField(widget=wCharField, required=False)
    issn_online = forms.CharField(widget=wCharField, required=False)
    pagina_inicio = forms.CharField(widget=wNumberField, required=True)
    pagina_fin = forms.CharField(widget=wNumberField, required=True)
    id_doi = forms.CharField(widget=wCharField, required=False)
    id_wos = forms.CharField(widget=wCharField, required=False)

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
    titulo = forms.CharField(widget=wCharField, required=True,)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    libro = forms.ModelChoiceField(
        queryset=Libro.objects.all(),
        label="Libro",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            # dependent_fields={'dependencia': 'dependencia'},
        )
    )
    pagina_inicio = forms.CharField(widget=wNumberField, required=True)
    pagina_fin = forms.CharField(widget=wNumberField, required=True)

    class Meta:
        model = CapituloLibroInvestigacion
        exclude = ['usuario', ]
        widgets = {
            'proyectos': Select2MultipleWidget,
        }


class MapaArbitradoForm(forms.ModelForm):
    titulo = forms.CharField(widget=wCharField, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    escala = forms.CharField(widget=wCharField, required=True)
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
    fecha = forms.CharField(widget=wDateField, required=True)
    numero_edicion = forms.CharField(widget=wNumberField, required=True)
    numero_paginas = forms.CharField(widget=wNumberField, required=True)
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
    nombre_libro = forms.CharField(widget=wCharField, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    editorial = forms.ModelChoiceField(Editorial.objects.all(), widget=wSelect)
    ciudad = forms.ModelChoiceField(Ciudad.objects.all(), widget=wSelect)
    fecha = forms.CharField(widget=wDateField)
    numero_edicion = forms.CharField(widget=wNumberField)
    numero_paginas = forms.CharField(widget=wNumberField)
    coleccion = forms.ModelChoiceField(Coleccion.objects.all(), widget=wSelect)
    volumen = forms.CharField(widget=wCharField)
    isbn = forms.CharField(widget=wCharField, required=False)
    url = forms.CharField(widget=wCharField, required=False)  # corregir valiadr url
    status = forms.ChoiceField(widget=wSelect, choices=getattr(settings, 'STATUS_PUBLICACION', ))

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
    nombre_proyecto = forms.CharField(widget=wCharField, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    es_permanente = forms.BooleanField()
    fecha_inicio = forms.CharField(widget=wDateField)
    fecha_fin = forms.CharField(widget=wDateField)
    status = forms.ChoiceField(widget=wSelect, choices=getattr(settings, 'STATUS_PROYECTO', ))
    clasificacion = forms.ChoiceField(widget=wSelect, choices=getattr(settings, 'CLASIFICACION_PROYECTO', ))
    organizacion = forms.ChoiceField(widget=wSelect, choices=getattr(settings, 'ORGANIZACION_PROYECTO', ))
    modalidad = forms.ChoiceField(widget=wSelect, choices=getattr(settings, 'MODALIDAD_PROYECTO', ))
    tematica_genero = forms.BooleanField()
    # problemaconacyt podria ser  no multiple
    descripcion_problema_nacional_conacyt = forms.CharField(widget=wTextarea, required=False)

    class Meta:
        model = ProyectoInvestigacion
        exclude = ['tipo', ]
