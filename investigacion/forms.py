from SIA.widgets import *

from . models import *
from nucleo.models import Libro as LibroInvestigacion
from nucleo.models import Proyecto as ProyectoInvestigacion
from nucleo.models import ProblemaNacionalConacyt, Metodologia, AreaEspecialidad, ImpactoSocial, Financiamiento


from django import forms

from django.conf import settings

from django_select2.forms import Select2Widget, ModelSelect2MultipleWidget

#

class ArticuloCientificoForm(forms.ModelForm):
    titulo = forms.CharField(widget=wCharField, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    tipo = forms.ChoiceField(widget=wSelect, choices=(('', ''), ('', ''), ('ARTICULO', 'Artículo'), ('ACTA', 'Acta'), ('CARTA', 'Carta'), ('RESENA', 'Reseña'), ('OTRO', 'Otro')), required=True)
    revista = forms.ModelChoiceField(Revista.objects.all().order_by('nombre_revista'), widget=wSelect, required=True)
    status = forms.ChoiceField(widget=wSelect, choices=getattr(settings, 'STATUS_PUBLICACION', ), required=True)
    solo_electronico = forms.BooleanField()
    #usuarios = forms.ModelMultipleChoiceField(User, widget=ModelSelect2MultipleWidget)
    #alumnos = forms.ModelMultipleChoiceField(User)
    indices = forms.MultipleChoiceField(Indice, widget=ModelSelect2MultipleWidget)
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
    #proyectos = forms.ModelMultipleChoiceField(Proyecto)

    class Meta:
        model = ArticuloCientifico
        exclude = []


class CapituloLibroInvestigacionForm(forms.ModelForm):
    titulo = forms.CharField(widget=wCharField, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    libro = forms.ModelChoiceField(Libro.objects.all().order_by('nombre_libro'), widget=wSelect, required=True)
    pagina_inicio = forms.CharField(widget=wNumberField, required=True)
    pagina_fin = forms.CharField(widget=wNumberField, required=True)

    class Meta:
        model = CapituloLibroInvestigacion
        exclude = ['usuario', ]


class MapaArbitradoForm(forms.ModelForm):
    titulo = forms.CharField(widget=wCharField, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    escala = forms.CharField(widget=wCharField, required=True)
    status = forms.ChoiceField(widget=wSelect, choices=getattr(settings, 'STATUS_PUBLICACION', ), required=True)
    ciudad = forms.ModelChoiceField(Ciudad.objects.all().order_by('ciudad'), widget=wSelect, required=True)
    editorial = forms.ModelChoiceField(Editorial.objects.all().order_by('editorial'), widget=wSelect, required=True)
    fecha = forms.CharField(widget=wDateField, required=True)
    numero_edicion = forms.CharField(widget=wNumberField, required=True)
    numero_paginas = forms.CharField(widget=wNumberField, required=True)
    coleccion = forms.ModelChoiceField(Coleccion.objects.all().order_by('coleccion'), widget=wSelect, required=False)
    volumen = forms.CharField(widget=wCharField, required=False)
    isbn = forms.CharField(widget=wCharField, required=False)
    url = forms.CharField(widget=wCharField, required=False)  # corregir valiadr url

    class Meta:
        model = MapaArbitrado
        exclude = []


class InformeTecnicoForm(forms.ModelForm):
    titulo = forms.CharField(widget=wCharField, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    fecha = forms.CharField(widget=wDateField, required=True)
    numero_paginas = forms.CharField(widget=wNumberField, required=True)
    url = forms.CharField(widget=wCharField, required=False)  # corregir valiadr url

    class Meta:
        model = InformeTecnico
        exclude = []


class LibroInvestigacionForm(forms.ModelForm):
    nombre_libro = forms.CharField(widget=wCharField, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    editorial = forms.ModelChoiceField(Editorial.objects.all().order_by('editorial'), widget=wSelect)
    ciudad = forms.ModelChoiceField(Ciudad.objects.all().order_by('ciudad'), widget=wSelect)
    fecha = forms.CharField(widget=wDateField)
    numero_edicion = forms.CharField(widget=wNumberField)
    numero_paginas = forms.CharField(widget=wNumberField)
    coleccion = forms.ModelChoiceField(Coleccion.objects.all().order_by('coleccion'), widget=wSelect)
    volumen = forms.CharField(widget=wCharField)
    isbn = forms.CharField(widget=wCharField, required=False)
    url = forms.CharField(widget=wCharField, required=False)  # corregir valiadr url
    status = forms.ChoiceField(widget=wSelect, choices=getattr(settings, 'STATUS_PUBLICACION', ))

    class Meta:
        model = LibroInvestigacion
        exclude = ['tipo', ]


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
    #problemaconacyt podria ser  no multiple
    descripcion_problema_nacional_conacyt = forms.CharField(widget=wTextarea, required=False)

    class Meta:
        model = ProyectoInvestigacion
        exclude = ['tipo', ]