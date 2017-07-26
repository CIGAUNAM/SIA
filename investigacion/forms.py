from SIA.widgets import *

from .models import *
from nucleo.models import Libro as LibroInvestigacion
from nucleo.models import Proyecto as ProyectoInvestigacion, ProblemaNacionalConacyt
# from nucleo.models import ProblemaNacionalConacyt, Metodologia, AreaEspecialidad, ImpactoSocial, Financiamiento


from django import forms

from django.conf import settings
from django_select2.forms import Select2MultipleWidget, Select2TagWidget

from django_select2.forms import Select2Widget, ModelSelect2MultipleWidget


#

class ArticuloCientificoForm(forms.ModelForm):
    titulo = forms.CharField(widget=wCharField, required=True, label='Título de artículo')
    descripcion = forms.CharField(widget=wTextarea, required=False, label='Descripción')
    tipo = forms.ChoiceField(widget=Select3Widget, choices=(
        ('ARTICULO', 'Artículo'), ('ACTA', 'Acta'), ('CARTA', 'Carta'), ('RESENA', 'Reseña'), ('OTRO', 'Otro')),
                             required=True)
    status = forms.ChoiceField(widget=Select3Widget, choices=getattr(settings, 'STATUS_PUBLICACION', ), required=True)
    solo_electronico = forms.BooleanField(required=False)
    nombre_abreviado_wos = forms.CharField(widget=wCharField, required=False, label='Nombre abreviado WOS')
    url = forms.CharField(widget=wCharField, required=False)  # corregir valiadr url
    fecha = forms.DateField(widget=wDateField, required=True, label='Fecha de publicación')
    revista = forms.ModelChoiceField(
        queryset=Revista.objects.all(),
        label="Revista",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            # dependent_fields={'dependencia': 'dependencia'},
        )
    )
    volumen = forms.CharField(widget=wCharField, required=False)
    numero = forms.CharField(widget=wCharField, required=False, label='Número')
    issn_impreso = forms.CharField(widget=wCharField, required=False, label='ISSN Impreso')
    issn_online = forms.CharField(widget=wCharField, required=False, label='ISSN Impreso')
    pagina_inicio = forms.CharField(widget=wNumberField, required=True, label='Número de página donde inicia')
    pagina_fin = forms.CharField(widget=wNumberField, required=True, label='Número de página final')
    id_doi = forms.CharField(widget=wCharField, required=False, label='ID DOI')
    id_wos = forms.CharField(widget=wCharField, required=False, label='ID WOS')
    proyecto = forms.ModelChoiceField(
        required=False,
        queryset=Proyecto.objects.all(),
        label="Proyecto",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )

    class Meta:
        model = ArticuloCientifico
        exclude = []
        widgets = {
            'usuarios': Select3MultipleWidgetOrdered,
            'alumnos': Select3MultipleWidget,
            'indices': Select3MultipleWidget,
        }


class CapituloLibroInvestigacionForm(forms.ModelForm):
    titulo = forms.CharField(widget=wCharField, required=True, label='Título del capítulo')
    descripcion = forms.CharField(widget=wTextarea, required=False)
    libro = forms.ModelChoiceField(
        queryset=Libro.objects.filter(tipo='INVESTIGACION'),
        label="Libro",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            # dependent_fields={'dependencia': 'dependencia'},
        )
    )
    pagina_inicio = forms.CharField(widget=wNumberField, required=True, label='Número de página donde inicia')
    pagina_fin = forms.CharField(widget=wNumberField, required=True, label='Número de página final')
    proyecto = forms.ModelChoiceField(
        required=False,
        queryset=Proyecto.objects.all(),
        label="Proyecto",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )

    class Meta:
        model = CapituloLibroInvestigacion
        exclude = ['usuario', ]


class MapaArbitradoForm(forms.ModelForm):
    titulo = forms.CharField(widget=wCharField, required=True, label='Título del mapa')
    descripcion = forms.CharField(widget=wTextarea, required=False)
    escala = forms.CharField(widget=wCharField, required=True, label='Escala')
    status = forms.ChoiceField(widget=Select3Widget, choices=getattr(settings, 'STATUS_PUBLICACION', ), required=True)
    pais = forms.ModelChoiceField(
        required=False,
        queryset=Pais.objects.all(),
        label="Pais",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    estado = forms.ModelChoiceField(
        required=False,
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
    fecha = forms.DateField(widget=wDateField, required=True, label='fecha de liberación')
    numero_edicion = forms.CharField(widget=wNumberField, required=True, label='Número de edición')
    numero_paginas = forms.CharField(widget=wNumberField, required=True, label='Número de páginas')
    coleccion = forms.ModelChoiceField(
        required=False,
        queryset=Coleccion.objects.all(),
        label="Coleccion",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            required=False,
        )
    )
    volumen = forms.CharField(widget=wCharField, required=False)
    isbn = forms.CharField(widget=wCharField, required=False)
    url = forms.URLField(widget=wUrlField, required=False)  # corregir valiadr url
    proyecto = forms.ModelChoiceField(
        required=False,
        queryset=Proyecto.objects.all(),
        label="Proyecto",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )

    class Meta:
        model = MapaArbitrado
        exclude = []
        widgets = {
            'usuarios': Select3MultipleWidget,
            'editores': Select3MultipleWidget,
            'coordinadores': Select3MultipleWidget,
        }


class InformeTecnicoForm(forms.ModelForm):
    titulo = forms.CharField(widget=wCharField, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    fecha = forms.DateField(widget=wDateField, required=True)
    numero_paginas = forms.CharField(widget=wNumberField, required=True)
    url = forms.CharField(widget=wCharField, required=False)  # corregir valiadr url
    proyecto = forms.ModelChoiceField(
        required=False,
        queryset=Proyecto.objects.all(),
        label="Proyecto",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )

    class Meta:
        model = InformeTecnico
        exclude = []
        widgets = {
            'usuarios': Select3MultipleWidget,
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
            dependent_fields={'pais': 'pais'},
        )
    )
    status = forms.ChoiceField(widget=Select3Widget, choices=getattr(settings, 'STATUS_PUBLICACION', ), required=True)
    fecha = forms.DateField(widget=wDateField)
    numero_edicion = forms.CharField(widget=wNumberField)
    numero_paginas = forms.CharField(widget=wNumberField)
    coleccion = forms.ModelChoiceField(
        required=False,
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
            'usuarios': Select3MultipleWidget,
            'editores': Select3MultipleWidget,
            'coordinadores': Select3MultipleWidget,
            'proyectos': Select3MultipleWidget,
        }


class ProyectoInvestigacionForm(forms.ModelForm):
    nombre = forms.CharField(widget=wCharField, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    es_permanente = forms.BooleanField(required=False)
    fecha_inicio = forms.DateField(widget=wDateField)
    fecha_fin = forms.DateField(widget=wDateField)
    status = forms.ChoiceField(widget=Select3Widget, choices=getattr(settings, 'STATUS_PROYECTO', ))
    clasificacion = forms.ChoiceField(widget=Select3Widget, choices=getattr(settings, 'CLASIFICACION_PROYECTO', ))
    organizacion = forms.ChoiceField(widget=Select3Widget, choices=getattr(settings, 'ORGANIZACION_PROYECTO', ))
    modalidad = forms.ChoiceField(widget=Select3Widget, choices=getattr(settings, 'MODALIDAD_PROYECTO', ))
    tematica_genero = forms.BooleanField(required=False)
    problema_nacional_conacyt = forms.ModelChoiceField(
        required=False,
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
            'problemas_nacionales_conacyt': Select3MultipleWidget,
            'usuarios': Select3MultipleWidget,
            'participantes': Select3MultipleWidget,
            'dependencias': Select3MultipleWidget,
            'financiamientos': Select3MultipleWidget,
            'metodologias': Select3MultipleWidget,
            'especialidades': Select3MultipleWidget,
            'impactos_sociales': Select3MultipleWidget,
            'tecnicos': Select3MultipleWidget,
            'alumnos_doctorado': Select3MultipleWidget,
            'alumnos_maestria': Select3MultipleWidget,
            'alumnos_licenciatura': Select3MultipleWidget,
        }
