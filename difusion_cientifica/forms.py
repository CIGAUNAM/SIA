from SIA.widgets import *
from . models import *

from django import forms
from nucleo.models import Pais, Estado, Ciudad
#

class MemoriaInExtensoForm(forms.ModelForm):
    nombre = forms.CharField(widget=wCharField, required=True, label='Título de memoria in extenso')
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

    fecha = forms.CharField(widget=wDateField, required=True)
    evento = forms.ModelChoiceField(Evento.objects.all(), widget=wSelect, required=True)
    pais_origen = forms.ModelChoiceField(Pais.objects.all(), widget=wSelect, required=True)
    pagina_inicio = forms.CharField(widget=wNumberField, required=True)
    pagina_fin = forms.CharField(widget=wNumberField, required=True)
    issn = forms.CharField(widget=wCharField, required=False)
    url = forms.CharField(widget=wCharField, required=False)  # corregir valiadr url

    class Meta:
        model = MemoriaInExtenso
        exclude = ['tags', ]


class PrologoLibroForm(forms.ModelForm):
    descripcion = forms.CharField(widget=wTextarea, required=False)
    libro = forms.ModelChoiceField(Libro.objects.all(), widget=wSelect, required=True)
    pagina_inicio = forms.CharField(widget=wNumberField, required=True)
    pagina_fin = forms.CharField(widget=wNumberField, required=True)
    url = forms.CharField(widget=wCharField, required=False)  # corregir valiadr url

    class Meta:
        model = PrologoLibro
        exclude = ['usuario', 'tags', ]


class ResenaForm(forms.ModelForm):
    titulo = forms.CharField(widget=wCharField, required=True)
    libro_resenado = forms.ModelChoiceField(Libro.objects.all(), widget=wSelect, required=True)
    revista_resenada = forms.ModelChoiceField(Revista.objects.all(), widget=wSelect, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    libro_publica = forms.ModelChoiceField(Libro.objects.all(), widget=wSelect, required=True)
    revista_publica = forms.ModelChoiceField(Revista.objects.all(), widget=wSelect, required=True)
    pagina_inicio = forms.CharField(widget=wNumberField, required=True)
    pagina_fin = forms.CharField(widget=wNumberField, required=True)
    url = forms.CharField(widget=wCharField, required=False)  # corregir valiadr url

    class Meta:
        model = Resena
        exclude = ['usuario', ]


class OrganizacionEventoAcademicoForm(forms.ModelForm):
    evento = forms.ModelChoiceField(Evento.objects.all(), widget=wSelect, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    responsabilidad = forms.ChoiceField(widget=wSelect, choices=getattr(settings, 'EVENTO__RESPONSABILIDAD', ), required=True)
    numero_ponentes = forms.CharField(widget=wNumberField, required=True)
    numero_asistentes = forms.CharField(widget=wNumberField, required=True)
    ambito = forms.ChoiceField(widget=wSelect, choices=getattr(settings, 'EVENTO__AMBITO', ), required=True)

    class Meta:
        model = OrganizacionEventoAcademico
        exclude = ['usuario', ]


class ParticipacionEventoAcademicoForm(forms.ModelForm):
    titulo = forms.CharField(widget=wCharField, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    evento = forms.ModelChoiceField(Evento.objects.all(), widget=wSelect, required=True)
    resumen_publicado = forms.BooleanField(required=False)
    ambito = forms.ChoiceField(widget=wSelect, choices=getattr(settings, 'EVENTO__AMBITO', ), required=True)
    por_invitacion = forms.BooleanField(required=False)
    ponencia_magistral = forms.BooleanField(required=False)

    class Meta:
        model = ParticipacionEventoAcademico
        exclude = ['usuario', ]
