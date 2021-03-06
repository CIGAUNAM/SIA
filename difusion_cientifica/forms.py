from SIA.widgets import *
from . models import *

from django import forms
from nucleo.models import Pais, Estado, Ciudad
from django_select2.forms import Select2MultipleWidget, ModelSelect2Widget, Select2Widget

#

class MemoriaInExtensoForm(forms.ModelForm):
    nombre = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True, label='Título de memoria in extenso')
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}), required=False)
    evento = forms.ModelChoiceField(
        queryset=Evento.objects.all(),
        label="Evento",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Evento.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'},
        )
    )
    editorial_text = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True,
                             label='Editorial')
    pagina_inicio = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}),
                                    required=True, label='Número de página inicial')
    pagina_fin = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}),
                                 required=True, label='Número de página final')
    issn = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False)

    class Meta:
        model = MemoriaInExtenso
        exclude = []
        widgets = {
            'indices': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'autores': wSortedSelect2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }



class ResenaForm(forms.ModelForm):
    titulo = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right', 'unique': True}), required=True, label='Título de reseña')
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
                                  required=False)
    tipo = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}), choices=getattr(settings, 'RESENA__TIPO', ), required=True)
    libro_resenado = forms.ModelChoiceField(
        required=False,
        queryset=Libro.objects.all(),
        label="Libro reseñado",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Libro.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    articulo_resenado = forms.ModelChoiceField(
        required=False,
        queryset=ArticuloCientifico.objects.all(),
        label="Artículo",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=ArticuloCientifico.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    fecha = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=True)
    revista_publica = forms.ModelChoiceField(
        required=True,
        queryset=Revista.objects.all(),
        label="Revista que publica",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Revista.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    pagina_inicio = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}), required=True)
    pagina_fin = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}), required=True)
    url = forms.URLField(widget=URLInput(attrs={'class': 'form-control pull-right'}), required=False)

    class Meta:
        model = Resena
        exclude = []
        widgets = {
            'autores': wSortedSelect2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class TraduccionForm(forms.ModelForm):
    titulo = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True, label='Título')
    # titulo_original = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True, label='Título original')
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
                                  required=False)
    tipo = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}), choices=getattr(settings, 'RESENA__TIPO', ), required=True)
    libro = forms.ModelChoiceField(
        required=False,
        queryset=Libro.objects.all(),
        label="Libro",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Libro.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    articulo = forms.ModelChoiceField(
        required=False,
        queryset=ArticuloCientifico.objects.all(),
        label="Artículo",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=ArticuloCientifico.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    fecha = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=True)
    url = forms.URLField(widget=URLInput(attrs={'class': 'form-control pull-right'}), required=False)

    class Meta:
        model = Traduccion
        exclude = []
        widgets = {
            'autores': wSortedSelect2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class OrganizacionEventoAcademicoForm(forms.ModelForm):
    evento = forms.ModelChoiceField(
        queryset=Evento.objects.all(),
        label="Evento",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'], 
            queryset=Evento.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}), required=False)
    numero_ponentes = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}), required=True)
    numero_asistentes = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}), required=True)
    ambito = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}), choices=getattr(settings, 'EVENTO__AMBITO', ), required=True)
    coordinador_general = forms.ModelChoiceField(
        required=False,
        queryset=User.objects.all(),
        label="Coordinador general",
        widget=ModelSelect2Widget(
            search_fields=['first_name__icontains', 'last_name__icontains'],
            queryset=User.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )

    class Meta:
        model = OrganizacionEventoAcademico
        exclude = []
        widgets = {
            'comite_organizador': wSortedSelect2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'ayudantes': wSortedSelect2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'apoyo_tecnico': wSortedSelect2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class ParticipacionEventoAcademicoForm(forms.ModelForm):
    titulo = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}), required=False)
    evento = forms.ModelChoiceField(
        queryset=Evento.objects.all(),
        label="Evento",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Evento.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    ambito = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}), choices=getattr(settings, 'EVENTO__AMBITO', ), required=True)
    resumen_publicado = forms.BooleanField(required=False, label='Resumen publicado')
    por_invitacion = forms.BooleanField(required=False, label='Participación por invitación')
    ponencia_magistral = forms.BooleanField(required=False, label='Ponencia Magistral')

    class Meta:
        model = ParticipacionEventoAcademico
        exclude = []
        widgets = {
            'autores': wSortedSelect2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }
