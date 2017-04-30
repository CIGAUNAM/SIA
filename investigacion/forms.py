from SIA.widgets import *

from . models import *
from nucleo.models import Libro as LibroInvestigacion
from nucleo.models import Proyecto as ProyectoInvestigacion

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
    class Meta:
        model = CapituloLibroInvestigacion
        exclude = ['tags', ]


class MapaArbitradoForm(forms.ModelForm):
    class Meta:
        model = MapaArbitrado
        exclude = ['tags', ]


class InformeTecnicoForm(forms.ModelForm):
    class Meta:
        model = InformeTecnico
        exclude = ['tags', ]


class LibroInvestigacionForm(forms.ModelForm):
    class Meta:
        model = LibroInvestigacion
        exclude = ['tipo', 'tags', ]


class ProyectoInvestigacionForm(forms.ModelForm):
    class Meta:
        model = ProyectoInvestigacion
        exclude = ['tipo', 'tags', ]