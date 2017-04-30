from SIA.widgets import *

from . models import *
from nucleo.models import Libro as LibroInvestigacion
from nucleo.models import Proyecto as ProyectoInvestigacion
from nucleo.models import ProblemaNacionalConacyt, Metodologia, AreaEspecialidad, ImpactoSocial, Financiamiento


from django import forms

from django.conf import settings

#

class ArticuloCientificoForm(forms.ModelForm):
    titulo = forms.CharField(widget=wCharField)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    tipo = forms.ChoiceField(widget=wSelectSingle, choices=(('', ''), ('', ''), ('ARTICULO', 'Artículo'), ('ACTA', 'Acta'), ('CARTA', 'Carta'), ('RESENA', 'Reseña'), ('OTRO', 'Otro')))
    revista = forms.ModelChoiceField(Revista.objects.all().order_by('nombre_revista'), widget=wSelectSingle)
    status = forms.ChoiceField(widget=wSelectSingle, choices=getattr(settings, 'STATUS_PUBLICACION', ))
    solo_electronico = forms.BooleanField()
    #usuarios = forms.ModelMultipleChoiceField(User)
    #alumnos = forms.ModelMultipleChoiceField(User)
    #indices = forms.ModelMultipleChoiceField(Indice)
    nombre_abreviado_wos = forms.CharField(widget=wCharField, required=False)
    url = forms.CharField(widget=wCharField, required=False)  # corregir valiadr url
    fecha = forms.CharField(widget=wDateField)
    volumen = forms.CharField(widget=wCharField, required=False)
    numero = forms.CharField(widget=wCharField, required=False)
    issn_impreso = forms.CharField(widget=wCharField, required=False)
    issn_online = forms.CharField(widget=wCharField, required=False)
    pagina_inicio = forms.CharField(widget=wNumberField)
    pagina_fin = forms.CharField(widget=wNumberField)
    id_doi = forms.CharField(widget=wCharField, required=False)
    id_wos = forms.CharField(widget=wCharField, required=False)
    #proyectos = forms.ModelMultipleChoiceField(Proyecto)

    class Meta:
        model = ArticuloCientifico
        exclude = ['tags', ]


class CapituloLibroInvestigacionForm(forms.ModelForm):
    titulo = forms.CharField(widget=wCharField)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    libro = forms.ModelChoiceField(Libro.objects.all().order_by('nombre_libro'), widget=wSelectSingle)
    pagina_inicio = forms.CharField(widget=wNumberField)
    pagina_fin = forms.CharField(widget=wNumberField)

    class Meta:
        model = CapituloLibroInvestigacion
        exclude = ['usuario', 'tags', ]


class MapaArbitradoForm(forms.ModelForm):
    titulo = forms.CharField(widget=wCharField, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    escala = forms.CharField(widget=wCharField)
    status = forms.ChoiceField(widget=wSelectSingle, choices=getattr(settings, 'STATUS_PUBLICACION', ))
    ciudad = forms.ModelChoiceField(Ciudad.objects.all().order_by('ciudad'), widget=wSelectSingle)
    editorial = forms.ModelChoiceField(Editorial.objects.all().order_by('editorial'), widget=wSelectSingle)
    fecha = forms.CharField(widget=wDateField)
    numero_edicion = forms.CharField(widget=wNumberField)
    numero_paginas = forms.CharField(widget=wNumberField)
    coleccion = forms.ModelChoiceField(Coleccion.objects.all().order_by('coleccion'), widget=wSelectSingle)
    volumen = forms.CharField(widget=wCharField)
    isbn = forms.CharField(widget=wCharField, required=False)
    url = forms.CharField(widget=wCharField, required=False)  # corregir valiadr url

    class Meta:
        model = MapaArbitrado
        exclude = ['tags', ]


class InformeTecnicoForm(forms.ModelForm):
    titulo = forms.CharField(widget=wCharField, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    fecha = forms.CharField(widget=wDateField)
    numero_paginas = forms.CharField(widget=wNumberField)
    url = forms.CharField(widget=wCharField, required=False)  # corregir valiadr url

    class Meta:
        model = InformeTecnico
        exclude = ['tags', ]


class LibroInvestigacionForm(forms.ModelForm):
    nombre_libro = forms.CharField(widget=wCharField, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    editorial = forms.ModelChoiceField(Editorial.objects.all().order_by('editorial'), widget=wSelectSingle)
    ciudad = forms.ModelChoiceField(Ciudad.objects.all().order_by('ciudad'), widget=wSelectSingle)
    fecha = forms.CharField(widget=wDateField)
    numero_edicion = forms.CharField(widget=wNumberField)
    numero_paginas = forms.CharField(widget=wNumberField)
    coleccion = forms.ModelChoiceField(Coleccion.objects.all().order_by('coleccion'), widget=wSelectSingle)
    volumen = forms.CharField(widget=wCharField)
    isbn = forms.CharField(widget=wCharField, required=False)
    url = forms.CharField(widget=wCharField, required=False)  # corregir valiadr url
    status = forms.ChoiceField(widget=wSelectSingle, choices=getattr(settings, 'STATUS_PUBLICACION', ))

    class Meta:
        model = LibroInvestigacion
        exclude = ['tipo', 'tags', ]


class ProyectoInvestigacionForm(forms.ModelForm):
    nombre_proyecto = forms.CharField(widget=wCharField, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    es_permanente = forms.BooleanField()
    fecha_inicio = forms.CharField(widget=wDateField)
    fecha_fin = forms.CharField(widget=wDateField)
    status = forms.ChoiceField(widget=wSelectSingle, choices=getattr(settings, 'STATUS_PROYECTO', ))
    clasificacion = forms.ChoiceField(widget=wSelectSingle, choices=getattr(settings, 'CLASIFICACION_PROYECTO', ))
    organizacion = forms.ChoiceField(widget=wSelectSingle, choices=getattr(settings, 'ORGANIZACION_PROYECTO', ))
    modalidad = forms.ChoiceField(widget=wSelectSingle, choices=getattr(settings, 'MODALIDAD_PROYECTO', ))
    tematica_genero = forms.BooleanField()
    #problemaconacyt podria ser  no multiple
    descripcion_problema_nacional_conacyt = forms.CharField(widget=wTextarea, required=False)

    class Meta:
        model = ProyectoInvestigacion
        exclude = ['tipo', 'tags', ]