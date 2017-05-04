from SIA.widgets import *
from . models import *
from nucleo.models import Libro as LibroDivulgacion, Editorial, Coleccion
from django import forms

#

class ArticuloDivulgacionForm(forms.ModelForm):
    titulo = forms.CharField(widget=wCharField, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    tipo = forms.ChoiceField(widget=wSelectSingle, choices=(('', ''), ('', ''), ('ARTICULO', 'Artículo'), ('ACTA', 'Acta'), ('CARTA', 'Carta'), ('RESENA', 'Reseña'), ('OTRO', 'Otro')), required=True)
    status = forms.ChoiceField(widget=wSelectSingle, choices=getattr(settings, 'STATUS_PUBLICACION', ), required=True)
    indizado = forms.BooleanField(required=False)
    url = forms.CharField(widget=wCharField, required=False)  # corregir valiadr url
    solo_electronico = forms.BooleanField()
    revista = forms.ModelChoiceField(Revista.objects.all().order_by('nombre_revista'), widget=wSelectSingle, required=True)
    fecha = forms.CharField(widget=wDateField, required=True)
    volumen = forms.CharField(widget=wCharField, required=False)
    numero = forms.CharField(widget=wNumberField, required=False)
    issn = forms.CharField(widget=wCharField, required=False)
    pagina_inicio = forms.CharField(widget=wNumberField, required=True)
    pagina_fin = forms.CharField(widget=wNumberField, required=True)
    id_doi = forms.CharField(widget=wCharField, required=False)

    class Meta:
        model = ArticuloDivulgacion
        exclude = ['tags', ]


class CapituloLibroDivulgacionForm(forms.ModelForm):
    titulo = forms.CharField(widget=wCharField, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    libro = forms.ModelChoiceField(Libro.objects.all().order_by('nombre_libro'), widget=wSelectSingle, required=True)
    pagina_inicio = forms.CharField(widget=wNumberField, required=True)
    pagina_fin = forms.CharField(widget=wNumberField, required=True)

    class Meta:
        model = CapituloLibroDivulgacion
        exclude = ['usuario', 'tags', ]


class OrganizacionEventoDivulgacionForm(forms.ModelForm):
    evento = forms.ModelChoiceField(Evento.objects.all().order_by('nombre_evento'), widget=wSelectSingle, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    responsabilidad = forms.ChoiceField(widget=wSelectSingle, choices=getattr(settings, 'EVENTO__RESPONSABILIDAD', ), required=True)
    numero_ponentes = forms.CharField(widget=wNumberField, required=True)
    numero_asistentes = forms.CharField(widget=wNumberField, required=True)
    ambito = forms.ChoiceField(widget=wSelectSingle, choices=getattr(settings, 'EVENTO__AMBITO', ), required=True)

    class Meta:
        model = OrganizacionEventoDivulgacion
        exclude = ['usuario', 'tags', ]


class ParticipacionEventoDivulgacionForm(forms.ModelForm):
    titulo = forms.CharField(widget=wCharField, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    evento = forms.ModelChoiceField(Evento.objects.all().order_by('nombre_evento'), widget=wSelectSingle, required=True)
    resumen_publicado = forms.BooleanField()
    ambito = forms.ChoiceField(widget=wSelectSingle, choices=getattr(settings, 'EVENTO__AMBITO', ), required=True)
    por_invitacion = forms.BooleanField()
    ponencia_magistral = forms.BooleanField()

    class Meta:
        model = ParticipacionEventoDivulgacion
        exclude = ['usuario', 'tags', ]


class ProgramaRadioTelevisionInternetForm(forms.ModelForm):
    tema = forms.CharField(widget=wCharField, required=True)
    fecha = forms.CharField(widget=wDateField, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    actividad = forms.ChoiceField(widget=wSelectSingle, choices=(('', ''), ('', ''), ('PRODUCCION', 'Producciòn'), ('PARTICIPACION', 'Participaciòn'), ('ENTREVISTA', 'Entrevista'), ('OTRA', 'Otra')), required=True)
    medio = forms.ChoiceField(widget=wSelectSingle, choices=(('', ''), ('', ''), ('PERIODICO', 'Periódico'), ('RADIO', 'Radio'), ('TV', 'Televisión'), ('INTERNET', 'Internet'), ('OTRO', 'Otro')), required=True)
    nombre_medio = forms.ModelChoiceField(MedioDivulgacion.objects.all().order_by('nombre_medio'), widget=wSelectSingle, required=True)

    class Meta:
        model = ProgramaRadioTelevisionInternet
        exclude = ['usuario', 'tags', ]


class LibroDivulgacionForm(forms.ModelForm):
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
        model = LibroDivulgacion
        exclude = ['tipo', 'tags', ]