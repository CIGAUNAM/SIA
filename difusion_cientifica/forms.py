from SIA.widgets import *
from . models import *

from django import forms
from nucleo.models import Pais, Estado, Ciudad
from django_select2.forms import Select2MultipleWidget
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
    evento = forms.ModelChoiceField(
        queryset=Evento.objects.all(),
        label="Evento",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    pagina_inicio = forms.CharField(widget=wNumberField, required=True)
    pagina_fin = forms.CharField(widget=wNumberField, required=True)
    issn = forms.CharField(widget=wCharField, required=False)
    url = forms.CharField(widget=wCharField, required=False)  # corregir valiadr url
    proyecto = forms.ModelChoiceField(
        required=False,
        queryset=Proyecto.objects.all(),
        label="Pais",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )

    class Meta:
        model = MemoriaInExtenso
        exclude = ['tags', ]
        widgets = {
            'usuarios': Select3MultipleWidget,
            'editores': Select3MultipleWidget,
            'indices': Select3MultipleWidget,
            'agradecimientos': Select3MultipleWidget,
        }


class PrologoLibroForm(forms.ModelForm):
    descripcion = forms.CharField(widget=wTextarea, required=True)
    libro = forms.ModelChoiceField(
        queryset=Libro.objects.all(),
        label="Libro",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    pagina_inicio = forms.CharField(widget=wNumberField, required=True, label='Páginal inicial')
    pagina_fin = forms.CharField(widget=wNumberField, required=True, label='Páginal final')
    url = forms.CharField(widget=wCharField, required=False, label='URL')  # corregir valiadr url

    class Meta:
        model = PrologoLibro
        exclude = ['usuario', 'tags', ]


class ResenaForm(forms.ModelForm):
    titulo = forms.CharField(widget=wCharField, required=True, label='Título de reseña')
    tipo = forms.ChoiceField(widget=Select3Widget, choices=getattr(settings, 'RESENA__TIPO', ), required=True)
    libro_resenado = forms.ModelChoiceField(
        required=False,
        queryset=Libro.objects.all(),
        label="Libro reseñado",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    revista_resenada = forms.ModelChoiceField(
        required=False,
        queryset=Revista.objects.all(),
        label="Revista reseñada",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    descripcion = forms.CharField(widget=wTextarea, required=False)
    libro_publica = forms.ModelChoiceField(
        required=False,
        queryset=Libro.objects.all(),
        label="Libro que publica",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    revista_publica = forms.ModelChoiceField(
        required=False,
        queryset=Revista.objects.all(),
        label="Revista que publica",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    pagina_inicio = forms.CharField(widget=wNumberField, required=True)
    pagina_fin = forms.CharField(widget=wNumberField, required=True)
    url = forms.CharField(widget=wCharField, required=False)  # corregir valiadr url

    def __init__(self, *args, **kwargs):
        super(ResenaForm, self).__init__(*args, **kwargs)
        #self.fields['tipo'].widget = forms.ChoiceField(attrs={'placeholder': 'Select Year'})

    class Meta:
        model = Resena
        exclude = ['usuario', ]


class OrganizacionEventoAcademicoForm(forms.ModelForm):
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
        model = OrganizacionEventoAcademico
        exclude = ['usuario', ]


class ParticipacionEventoAcademicoForm(forms.ModelForm):
    titulo = forms.CharField(widget=wCharField, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    evento = forms.ModelChoiceField(
        queryset=Evento.objects.all(),
        label="Evento",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    ambito = forms.ChoiceField(widget=Select3Widget, choices=getattr(settings, 'EVENTO__AMBITO', ), required=True)
    resumen_publicado = forms.BooleanField(required=False, label='Resumen publicado')
    por_invitacion = forms.BooleanField(required=False, label='Participación por invitación')
    ponencia_magistral = forms.BooleanField(required=False, label='Ponencia Magistral')

    class Meta:
        model = ParticipacionEventoAcademico
        exclude = ['usuario', ]
