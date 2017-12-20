from SIA.widgets import *
from . models import *
from django import forms

from nucleo.models import Institucion
from django_select2.forms import Select2MultipleWidget, ModelSelect2Widget, Select2Widget

#

class DistincionAcademicoForm(forms.ModelForm):
    distincion = forms.ModelChoiceField(
        queryset=Distincion.objects.all(),
        label="Distincion",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Distincion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    institucion = forms.ModelChoiceField(
        queryset=Institucion.objects.all(),
        label="Institución",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Institucion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    fecha = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)

    class Meta:
        model = DistincionAcademico
        exclude = ['usuario']


class DistincionAlumnoForm(forms.ModelForm):
    distincion = forms.ModelChoiceField(
        queryset=Distincion.objects.all(),
        label="Distincion",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Distincion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    alumno = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Alumno",
        widget=ModelSelect2Widget(
            search_fields=['first_name__icontains', 'last_name__icontains', 'username__icontains'],
            queryset=User.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    nivel_academico = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}), choices=getattr(settings, 'NIVEL_ACADEMICO', ), required=True)
    institucion = forms.ModelChoiceField(
        queryset=Institucion.objects.all(),
        label="Institución",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Institucion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    fecha = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)

    class Meta:
        model = DistincionAlumno
        exclude = []
        widgets = {
            'tutores': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class ParticipacionComisionExpertosForm(forms.ModelForm):
    nombre = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}), required=False, label='Descripción')
    institucion = forms.ModelChoiceField(
        queryset=Institucion.objects.all(),
        label="Institución",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Institucion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    fecha_inicio = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    fecha_fin = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)

    class Meta:
        model = ParticipacionComisionExpertos
        exclude = ['usuario', ]



class ParticipacionSociedadCientificaForm(forms.ModelForm):
    nombre = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}), required=False, label='Descripción')
    tipo = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}), choices=(('', '-------'), ('INVITACION', 'Por invitación'), ('ELECCION', 'Por elección')), required=True)
    fecha_inicio = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    fecha_fin = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)

    class Meta:
        model = ParticipacionSociedadCientifica
        exclude = ['usuario', ]



class CitaPublicacionForm(forms.ModelForm):
    tipo_trabajo_citado = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
                             choices=(('', '-------'), ('ARTICULO', 'Artículo'), ('LIBRO', 'Libro'), ('CAPITULO_LIBRO', 'Capítulo de libro')), required=True)
    articulo_citado = forms.ModelChoiceField(
        queryset=ArticuloCientifico.objects.all(),
        label="Artículo Científico",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=ArticuloCientifico.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    libro_citado = forms.ModelChoiceField(
        queryset=Libro.objects.all(),
        label="Libro",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Libro.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    capitulo_libro_citado = forms.ModelChoiceField(
        queryset=CapituloLibroInvestigacion.objects.all(),
        label="Capítulo de libro de investigación",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=CapituloLibroInvestigacion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}), required=False, label='Descripción')

    class Meta:
        model = CitaPublicacion
        exclude = []
        widgets = {
            'citado_en_articulos': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'citado_en_libros': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'citado_en_capitulos_libros': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'usuarios': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'})
        }