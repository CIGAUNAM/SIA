from SIA.widgets import *
from . models import *
from nucleo.models import Libro as LibroDivulgacion, Editorial, Coleccion
from django import forms
from django_select2.forms import Select2MultipleWidget
from nucleo.models import Libro as LibroInvestigacion
from nucleo.models import Pais, Estado, Ciudad

#

class ArticuloDivulgacionForm(forms.ModelForm):
    titulo = forms.CharField(widget=wCharField, required=True, label='Título de artículo')
    descripcion = forms.CharField(widget=wTextarea, required=False, label='Descripción')
    tipo = forms.ChoiceField(widget=Select3Widget, choices=(
        ('ARTICULO', 'Artículo'), ('ACTA', 'Acta'), ('CARTA', 'Carta'), ('RESENA', 'Reseña'), ('OTRO', 'Otro')),
                             required=True)
    status = forms.ChoiceField(widget=Select3Widget, choices=getattr(settings, 'STATUS_PUBLICACION', ), required=True)
    indizado = forms.BooleanField()
    url = forms.CharField(widget=wCharField, required=False)  # corregir valiadr url
    solo_electronico = forms.BooleanField()
    revista = forms.ModelChoiceField(
        queryset=Revista.objects.all(),
        label="Revista",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    fecha = forms.CharField(widget=wDateField, required=True, label='Fecha de publicación')
    volumen = forms.CharField(widget=wCharField, required=False)
    numero = forms.CharField(widget=wNumberField, required=False, label='Número')
    issn = forms.CharField(widget=wCharField, required=False, label='ISSN Impreso')
    pagina_inicio = forms.CharField(widget=wNumberField, required=True, label='Número de página donde inicia')
    pagina_fin = forms.CharField(widget=wNumberField, required=True, label='Número de página final')
    id_doi = forms.CharField(widget=wCharField, required=False, label='ID DOI')

    class Meta:
        model = ArticuloDivulgacion
        exclude = []
        widgets = {
            'usuarios': Select2MultipleWidget,
            'alumnos': Select2MultipleWidget,
            'indices': Select2MultipleWidget,
            'proyectos': Select2MultipleWidget,
        }


class CapituloLibroDivulgacionForm(forms.ModelForm):
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
        model = CapituloLibroDivulgacion
        exclude = ['usuario', ]
        widgets = {
            'proyectos': Select2MultipleWidget,
        }


class OrganizacionEventoDivulgacionForm(forms.ModelForm):
    evento = forms.ModelChoiceField(
        queryset=Evento.objects.all(),
        label="Evento",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    descripcion = forms.CharField(widget=wTextarea, required=False)
    responsabilidad = forms.ChoiceField(widget=Select3Widget, choices=getattr(settings, 'EVENTO__RESPONSABILIDAD', ), required=True)
    numero_ponentes = forms.CharField(widget=wNumberField, required=True)
    numero_asistentes = forms.CharField(widget=wNumberField, required=True)
    ambito = forms.ChoiceField(widget=Select3Widget, choices=getattr(settings, 'EVENTO__AMBITO', ), required=True)

    class Meta:
        model = OrganizacionEventoDivulgacion
        exclude = ['usuario', ]


class ParticipacionEventoDivulgacionForm(forms.ModelForm):
    titulo = forms.CharField(widget=wCharField, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    evento = forms.ModelChoiceField(
        queryset=Evento.objects.all(),
        label="Evento",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    resumen_publicado = forms.BooleanField(required=False, label='Resumen publicado')
    ambito = forms.ChoiceField(widget=Select3Widget, choices=getattr(settings, 'EVENTO__AMBITO', ), required=True)
    por_invitacion = forms.BooleanField(required=False, label='Participación por invitación')
    ponencia_magistral = forms.BooleanField(required=False, label='Ponencia Magistral')

    class Meta:
        model = ParticipacionEventoDivulgacion
        exclude = ['usuario', ]


class ProgramaRadioTelevisionInternetForm(forms.ModelForm):
    tema = forms.CharField(widget=wCharField, required=True)
    fecha = forms.CharField(widget=wDateField, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    actividad = forms.ChoiceField(widget=Select3Widget, choices=(('PRODUCCION', 'Producciòn'), ('PARTICIPACION', 'Participaciòn'), ('ENTREVISTA', 'Entrevista'), ('OTRA', 'Otra')), required=True)
    medio = forms.ChoiceField(widget=Select3Widget, choices=(('PERIODICO', 'Periódico'), ('RADIO', 'Radio'), ('TV', 'Televisión'), ('INTERNET', 'Internet'), ('OTRO', 'Otro')), required=True)
    nombre_medio = forms.ModelChoiceField(
        queryset=MedioDivulgacion.objects.all(),
        label="Medio de divulgación",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )

    class Meta:
        model = ProgramaRadioTelevisionInternet
        exclude = ['usuario', ]


class LibroDivulgacionForm(forms.ModelForm):
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