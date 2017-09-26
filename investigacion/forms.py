from SIA.widgets import *

from .models import *
from nucleo.models import Libro as LibroInvestigacion
from nucleo.models import Proyecto as ProyectoInvestigacion, ProblemaNacionalConacyt

from django import forms

from django.conf import settings
from django_select2.forms import Select2Widget, ModelSelect2Widget, ModelSelect2MultipleWidget, Select2MultipleWidget

from sortedm2m.forms import SortedMultipleChoiceField


#

class ArticuloCientificoForm(forms.ModelForm):
    titulo = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True,
                             label='Título de artículo')
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
                                  required=False, label='Descripción')
    tipo = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
                             choices=(
                             ('', 'Seleccionar un tipo de artículo'), ('ARTICULO', 'Artículo'), ('ACTA', 'Acta'),
                             ('CARTA', 'Carta'), ('RESENA', 'Reseña'), ('OTRO', 'Otro')), required=True)
    status = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
                               choices=getattr(settings, 'STATUS_PUBLICACION', ), required=True)
    solo_electronico = forms.BooleanField(required=False)
    url = forms.URLField(widget=URLInput(attrs={'class': 'form-control pull-right'}), required=False)
    fecha = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=True, label='Fecha de publicación')
    revista = forms.ModelChoiceField(
        queryset=Revista.objects.all(),
        label="Revista",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Revista.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    volumen = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False)
    numero = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False,
                             label='Número')
    issn_impreso = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False,
                                   label='ISSN Impreso')
    issn_online = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False,
                                  label='ISSN Impreso')
    pagina_inicio = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}),
                                    required=True, label='Número de página donde inicia')
    pagina_fin = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}),
                                 required=True, label='Número de página final')
    id_doi = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False,
                             label='ID DOI')
    id_wos = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False,
                             label='ID WOS')
    proyecto = forms.ModelChoiceField(
        required=False,
        queryset=Proyecto.objects.all(),
        label="Proyecto",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Proyecto.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )

    class Meta:
        model = ArticuloCientifico
        exclude = []
        widgets = {
            'usuarios': wSortedSelect2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'alumnos': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'indices': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class CapituloLibroInvestigacionForm(forms.ModelForm):
    titulo = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True,
                             label='Título del capítulo')
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
                                  required=False)
    libro = forms.ModelChoiceField(
        queryset=Libro.objects.filter(tipo='INVESTIGACION'),
        label="Libro",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Libro.objects.filter(tipo='INVESTIGACION'),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    pagina_inicio = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}),
                                    required=True, label='Número de página donde inicia')
    pagina_fin = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}),
                                 required=True, label='Número de página final')
    proyecto = forms.ModelChoiceField(
        required=False,
        queryset=Proyecto.objects.all(),
        label="Proyecto",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Proyecto.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )

    class Meta:
        model = CapituloLibroInvestigacion
        exclude = []
        widgets = {
            'usuarios': wSortedSelect2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class MapaArbitradoForm(forms.ModelForm):
    titulo = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True,
                             label='Título del mapa')
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
                                  required=False)
    escala = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True,
                             label='Escala')
    status = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
                               choices=getattr(settings, 'STATUS_PUBLICACION', ), required=True)
    pais = forms.ModelChoiceField(
        required=False,
        queryset=Pais.objects.all(),
        label="Pais",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Pais.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    estado = forms.ModelChoiceField(
        required=False,
        queryset=Estado.objects.all(),
        label="Estado",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            dependent_fields={'pais': 'pais'},
            queryset=Estado.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    ciudad = forms.ModelChoiceField(
        queryset=Ciudad.objects.all(),
        label="Ciudad",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            dependent_fields={'estado': 'estado'},
            queryset=Ciudad.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    editorial = forms.ModelChoiceField(
        queryset=Editorial.objects.all(),
        label="Editorial",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Editorial.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    fecha = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=True, label='fecha de liberación')
    numero_edicion = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}),
                                     required=True, label='Número de edición')
    numero_paginas = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}),
                                     required=True, label='Número de páginas')
    coleccion = forms.ModelChoiceField(
        required=False,
        queryset=Coleccion.objects.all(),
        label="Coleccion",
        widget=ModelSelect2Widget(
            required=False,
            search_fields=['nombre__icontains'],
            queryset=Coleccion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    volumen = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False)
    isbn = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False)
    url = forms.URLField(widget=URLInput(attrs={'class': 'form-control pull-right'}), required=False)
    proyecto = forms.ModelChoiceField(
        required=False,
        queryset=Proyecto.objects.all(),
        label="Proyecto",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Proyecto.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )

    class Meta:
        model = MapaArbitrado
        exclude = []
        widgets = {
            'usuarios': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'editores': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'coordinadores': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class InformeTecnicoForm(forms.ModelForm):
    titulo = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
                                  required=False)
    fecha = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=True)
    numero_paginas = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}),
                                     required=True)
    url = forms.URLField(widget=URLInput(attrs={'class': 'form-control pull-right'}), required=False)
    proyecto = forms.ModelChoiceField(
        required=False,
        queryset=Proyecto.objects.all(),
        label="Proyecto",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Proyecto.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )

    class Meta:
        model = InformeTecnico
        exclude = []
        widgets = {
            'usuarios': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class LibroInvestigacionForm(forms.ModelForm):
    nombre = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
                                  required=False)
    pais = forms.ModelChoiceField(
        queryset=Pais.objects.all(),
        label="Pais",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Pais.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    estado = forms.ModelChoiceField(
        queryset=Estado.objects.all(),
        label="Estado",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            dependent_fields={'pais': 'pais'},
            queryset=Estado.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    ciudad = forms.ModelChoiceField(
        queryset=Ciudad.objects.all(),
        label="Ciudad",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            dependent_fields={'estado': 'estado'},
            queryset=Ciudad.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    editorial = forms.ModelChoiceField(
        queryset=Editorial.objects.all(),
        label="Editorial",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            dependent_fields={'pais': 'pais'},
            queryset=Editorial.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    status = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
                               choices=getattr(settings, 'STATUS_PUBLICACION', ), required=True)
    fecha = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}))
    numero_edicion = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}))
    numero_paginas = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}))
    coleccion = forms.ModelChoiceField(
        required=False,
        queryset=Coleccion.objects.all(),
        label="Coleccion",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Coleccion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    volumen = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False)
    isbn = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False)
    url = forms.URLField(widget=URLInput(attrs={'class': 'form-control pull-right'}), required=False)

    class Meta:
        model = LibroInvestigacion
        exclude = ['tipo', ]
        widgets = {
            'usuarios': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'editores': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'coordinadores': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'proyectos': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class ProyectoInvestigacionForm(forms.ModelForm):
    nombre = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
                                  required=False)
    es_permanente = forms.BooleanField(required=False)
    fecha_inicio = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}))
    fecha_fin = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}))
    status = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
                               choices=getattr(settings, 'STATUS_PROYECTO', ))
    clasificacion = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        choices=getattr(settings, 'CLASIFICACION_PROYECTO', ))
    organizacion = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        choices=getattr(settings, 'ORGANIZACION_PROYECTO', ))
    modalidad = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        choices=getattr(settings, 'MODALIDAD_PROYECTO', ))
    tematica_genero = forms.BooleanField(required=False)
    problema_nacional_conacyt = forms.ModelChoiceField(
        required=False,
        queryset=ProblemaNacionalConacyt.objects.all(),
        label="Problema Nacional Conacyt",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=ProblemaNacionalConacyt.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    descripcion_problema_nacional_conacyt = forms.CharField(
        widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}), required=False)

    class Meta:
        model = ProyectoInvestigacion
        exclude = ['tipo', ]
        widgets = {
            'problemas_nacionales_conacyt': Select2MultipleWidget(
                attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'usuarios': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'participantes': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'dependencias': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'financiamientos': Select2MultipleWidget(
                attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'metodologias': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'especialidades': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'impactos_sociales': Select2MultipleWidget(
                attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'tecnicos': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'alumnos_doctorado': Select2MultipleWidget(
                attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'alumnos_maestria': Select2MultipleWidget(
                attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'alumnos_licenciatura': Select2MultipleWidget(
                attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


a = [(None, [
    {'name': 'usuarios', 'value': 359, 'label': ' ', 'selected': False, 'index': '0', 'attrs': {}, 'type': 'select',
     'template_name': 'widgets/w_select_option.html'}], 0), (None, [
    {'name': 'usuarios', 'value': 362, 'label': '16ymf 16ymf', 'selected': False, 'index': '1', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 1), (None, [
    {'name': 'usuarios', 'value': 463, 'label': 'A. Andablo Reyes', 'selected': False, 'index': '2', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 2), (None, [
    {'name': 'usuarios', 'value': 503, 'label': 'A. Espinoza Maya', 'selected': False, 'index': '3', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 3), (None, [
    {'name': 'usuarios', 'value': 511, 'label': 'A. Flamenco Sandoval', 'selected': False, 'index': '4', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 4), (None, [
    {'name': 'usuarios', 'value': 571, 'label': 'A. Lomelí Jiménez', 'selected': False, 'index': '5', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 5), (None, [
    {'name': 'usuarios', 'value': 692, 'label': 'A. Sánchez Duque', 'selected': False, 'index': '6', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 6), (None, [
    {'name': 'usuarios', 'value': 386, 'label': 'Adrián Ghilardi', 'selected': False, 'index': '7', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 7), (None, [
    {'name': 'usuarios', 'value': 559, 'label': 'Adrián Mas Jean François', 'selected': False, 'index': '8',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 8), (None, [
    {'name': 'usuarios', 'value': 412, 'label': 'Adriana Carolina Flores Díaz', 'selected': False, 'index': '9',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 9), (None, [
    {'name': 'usuarios', 'value': 604, 'label': 'Alberto Orozco Moreno', 'selected': False, 'index': '10', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 10), (None, [
    {'name': 'usuarios', 'value': 563, 'label': 'Alberto Ken Oyama', 'selected': False, 'index': '11', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 11), (None, [
    {'name': 'usuarios', 'value': 548, 'label': 'Aldo I. Hernández  Magaña', 'selected': False, 'index': '12',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 12), (None, [
    {'name': 'usuarios', 'value': 375, 'label': 'Alejandra Patricia Larrazábal De la Via', 'selected': False,
     'index': '13', 'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 13), (None, [
    {'name': 'usuarios', 'value': 485, 'label': 'Alejandro Casas Fernández', 'selected': False, 'index': '14',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 14), (None, [
    {'name': 'usuarios', 'value': 492, 'label': 'Alejandro Collantes', 'selected': False, 'index': '15', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 15), (None, [
    {'name': 'usuarios', 'value': 399, 'label': 'Alejandro Velázquez Montes', 'selected': False, 'index': '16',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 16), (None, [
    {'name': 'usuarios', 'value': 598, 'label': 'Alejandro Jalmacin Nené Preciado', 'selected': False, 'index': '17',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 17), (None, [
    {'name': 'usuarios', 'value': 361, 'label': 'alex alex', 'selected': False, 'index': '18', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 18), (None, [
    {'name': 'usuarios', 'value': 705, 'label': 'Alexey Voinov', 'selected': False, 'index': '19', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 19), (None, [
    {'name': 'usuarios', 'value': 635, 'label': 'Alexis Daniela Rivero Romero', 'selected': False, 'index': '20',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 20), (None, [
    {'name': 'usuarios', 'value': 595, 'label': 'Alfred N. Gichu', 'selected': False, 'index': '21', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 21), (None, [
    {'name': 'usuarios', 'value': 459, 'label': 'Alfredo Amador García', 'selected': False, 'index': '22', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 22), (None, [
    {'name': 'usuarios', 'value': 487, 'label': 'Alicia Castillo', 'selected': False, 'index': '23', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 23), (None, [
    {'name': 'usuarios', 'value': 400, 'label': 'Alina Alvarez Larrain', 'selected': False, 'index': '24', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 24), (None, [
    {'name': 'usuarios', 'value': 645, 'label': 'Amalio Santacruz Varela', 'selected': False, 'index': '25',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 25), (None, [
    {'name': 'usuarios', 'value': 388, 'label': 'Ana Burgos', 'selected': False, 'index': '26', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 26), (None, [
    {'name': 'usuarios', 'value': 524, 'label': 'Ana García de Fuentes', 'selected': False, 'index': '27', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 27), (None, [
    {'name': 'usuarios', 'value': 419, 'label': 'Ana Isabel Moreno Calles', 'selected': False, 'index': '28',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 28), (None, [
    {'name': 'usuarios', 'value': 657, 'label': 'Ana M. Soler Arechalde', 'selected': False, 'index': '29', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 29), (None, [
    {'name': 'usuarios', 'value': 507, 'label': 'Andrés Etter', 'selected': False, 'index': '30', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 30), (None, [
    {'name': 'usuarios', 'value': 523, 'label': 'Andres Garcia', 'selected': False, 'index': '31', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 31), (None, [
    {'name': 'usuarios', 'value': 432, 'label': 'Andrew Boni', 'selected': False, 'index': '32', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 32), (None, [
    {'name': 'usuarios', 'value': 643, 'label': 'Andrew Roth', 'selected': False, 'index': '33', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 33), (None, [
    {'name': 'usuarios', 'value': 483, 'label': 'Ángel Carrancho', 'selected': False, 'index': '34', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 34), (None, [
    {'name': 'usuarios', 'value': 512, 'label': 'Angel David Flores Domínguez', 'selected': False, 'index': '35',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 35), (None, [
    {'name': 'usuarios', 'value': 381, 'label': 'Angel Guadalupe Priego Santander', 'selected': False, 'index': '36',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 36), (None, [
    {'name': 'usuarios', 'value': 518, 'label': 'Angeles Gallegos A.', 'selected': False, 'index': '37', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 37), (None, [
    {'name': 'usuarios', 'value': 709, 'label': 'Antoinette WinklerPrins', 'selected': False, 'index': '38',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 38), (None, [
    {'name': 'usuarios', 'value': 568, 'label': 'Antonio Larrazábal De la Vía', 'selected': False, 'index': '39',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 39), (None, [
    {'name': 'usuarios', 'value': 594, 'label': 'Antonio Méndez Lemus', 'selected': False, 'index': '40', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 40), (None, [
    {'name': 'usuarios', 'value': 597, 'label': 'Antonio Napoletano', 'selected': False, 'index': '41', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 41), (None, [
    {'name': 'usuarios', 'value': 413, 'label': 'Armonía Borrego', 'selected': False, 'index': '42', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 42), (None, [
    {'name': 'usuarios', 'value': 517, 'label': 'Artemio Gallegos García', 'selected': False, 'index': '43',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 43), (None, [
    {'name': 'usuarios', 'value': 411, 'label': 'Arturo Balderas Torres', 'selected': False, 'index': '44', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 44), (None, [
    {'name': 'usuarios', 'value': 401, 'label': 'Arturo Muñiz Jauregui', 'selected': False, 'index': '45', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 45), (None, [
    {'name': 'usuarios', 'value': 533, 'label': 'Avto Gogichaishvili', 'selected': False, 'index': '46', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 46), (None, [
    {'name': 'usuarios', 'value': 581, 'label': 'Ayesa Martínez Serrano', 'selected': False, 'index': '47', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 47), (None, [
    {'name': 'usuarios', 'value': 619, 'label': 'Azucena Pérez Vega', 'selected': False, 'index': '48', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 48), (None, [
    {'name': 'usuarios', 'value': 508, 'label': 'B. Figueroa Rangel', 'selected': False, 'index': '49', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 49), (None, [
    {'name': 'usuarios', 'value': 504, 'label': 'Bailis Espinoza Medrano', 'selected': False, 'index': '50',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 50), (None, [
    {'name': 'usuarios', 'value': 606, 'label': 'Beatriz Ortega', 'selected': False, 'index': '51', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 51), (None, [
    {'name': 'usuarios', 'value': 418, 'label': 'Beatriz Tejera', 'selected': False, 'index': '52', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 52), (None, [
    {'name': 'usuarios', 'value': 549, 'label': 'Benigno Hernández de la Torre', 'selected': False, 'index': '53',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 53), (None, [
    {'name': 'usuarios', 'value': 365, 'label': 'Berenice Solis Castillo', 'selected': False, 'index': '54',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 54), (None, [
    {'name': 'usuarios', 'value': 698, 'label': 'Birgit Terhorst', 'selected': False, 'index': '55', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 55), (None, [
    {'name': 'usuarios', 'value': 382, 'label': 'Brian Napoletano', 'selected': False, 'index': '56', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 56), (None, [
    {'name': 'usuarios', 'value': 686, 'label': 'Bruce Ferguson', 'selected': False, 'index': '57', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 57), (None, [
    {'name': 'usuarios', 'value': 473, 'label': 'Bryan C. Pijanowski', 'selected': False, 'index': '58', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 58), (None, [
    {'name': 'usuarios', 'value': 673, 'label': 'C. Delgado Trejo', 'selected': False, 'index': '59', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 59), (None, [
    {'name': 'usuarios', 'value': 668, 'label': 'C. Gutiérrez Báez', 'selected': False, 'index': '60', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 60), (None, [
    {'name': 'usuarios', 'value': 516, 'label': 'C. Gabriel Vázquez', 'selected': False, 'index': '61', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 61), (None, [
    {'name': 'usuarios', 'value': 493, 'label': 'Camilo A. Correa Ayram', 'selected': False, 'index': '62', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 62), (None, [
    {'name': 'usuarios', 'value': 427, 'label': 'Carina Grajales', 'selected': False, 'index': '63', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 63), (None, [
    {'name': 'usuarios', 'value': 536, 'label': 'Carlos González Esquivel', 'selected': False, 'index': '64',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 64), (None, [
    {'name': 'usuarios', 'value': 462, 'label': 'Carlos Antonio Anaya Merchant', 'selected': False, 'index': '65',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 65), (None, [
    {'name': 'usuarios', 'value': 476, 'label': 'Cecilia I. Caballero Miranda', 'selected': False, 'index': '66',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 66), (None, [
    {'name': 'usuarios', 'value': 688, 'label': 'Citlalli López Binqüist', 'selected': False, 'index': '67',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 67), (None, [
    {'name': 'usuarios', 'value': 674, 'label': 'Claudia Uberhuaga', 'selected': False, 'index': '68', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 68), (None, [
    {'name': 'usuarios', 'value': 387, 'label': 'Claudio Garibay Orozco', 'selected': False, 'index': '69', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 69), (None, [
    {'name': 'usuarios', 'value': 535, 'label': 'Claudio González Arqueros', 'selected': False, 'index': '70',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 70), (None, [
    {'name': 'usuarios', 'value': 695, 'label': 'Cristóbal Daniel Sánchez Sánchez', 'selected': False, 'index': '71',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 71), (None, [
    {'name': 'usuarios', 'value': 574, 'label': 'Cruz López Contreras', 'selected': False, 'index': '72', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 72), (None, [
    {'name': 'usuarios', 'value': 529, 'label': 'D. Geissert Kientz', 'selected': False, 'index': '73', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 73), (None, [
    {'name': 'usuarios', 'value': 610, 'label': 'D. Palma López', 'selected': False, 'index': '74', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 74), (None, [
    {'name': 'usuarios', 'value': 644, 'label': 'D. Ryan Norris', 'selected': False, 'index': '75', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 75), (None, [
    {'name': 'usuarios', 'value': 701, 'label': 'D. T. Tyler Flockhart', 'selected': False, 'index': '76', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 76), (None, [
    {'name': 'usuarios', 'value': 679, 'label': 'Daniel A. Slayback', 'selected': False, 'index': '77', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 77), (None, [
    {'name': 'usuarios', 'value': 554, 'label': 'Daniel Iura Gonzalez', 'selected': False, 'index': '78', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 78), (None, [
    {'name': 'usuarios', 'value': 649, 'label': 'Daniel Schwindt', 'selected': False, 'index': '79', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 79), (None, [
    {'name': 'usuarios', 'value': 422, 'label': 'Dante Ariel  Ayala Ortiz', 'selected': False, 'index': '80',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 80), (None, [
    {'name': 'usuarios', 'value': 623, 'label': 'Diana Ramírez Mejía', 'selected': False, 'index': '81', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 81), (None, [
    {'name': 'usuarios', 'value': 648, 'label': 'Didac Santos Fita', 'selected': False, 'index': '82', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 82), (None, [
    {'name': 'usuarios', 'value': 699, 'label': 'Diego Torres Huerta', 'selected': False, 'index': '83', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 83), (None, [
    {'name': 'usuarios', 'value': 618, 'label': 'Diego Raúl Pérez Salicrup', 'selected': False, 'index': '84',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 84), (None, [
    {'name': 'usuarios', 'value': 553, 'label': 'E. Isunza Vera', 'selected': False, 'index': '85', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 85), (None, [
    {'name': 'usuarios', 'value': 454, 'label': 'Eduardo Alanís Rodríguez', 'selected': False, 'index': '86',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 86), (None, [
    {'name': 'usuarios', 'value': 434, 'label': 'Eduardo Frapolli', 'selected': False, 'index': '87', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 87), (None, [
    {'name': 'usuarios', 'value': 525, 'label': 'Eduardo García', 'selected': False, 'index': '88', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 88), (None, [
    {'name': 'usuarios', 'value': 603, 'label': 'Eduardo Orihuela Estefan', 'selected': False, 'index': '89',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 89), (None, [
    {'name': 'usuarios', 'value': 499, 'label': 'Ek del Val de Gortari', 'selected': False, 'index': '90', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 90), (None, [
    {'name': 'usuarios', 'value': 562, 'label': 'Elias K. Ucakuwun', 'selected': False, 'index': '91', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 91), (None, [
    {'name': 'usuarios', 'value': 659, 'label': 'Elizabeth Solleiro Rebolledo', 'selected': False, 'index': '92',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 92), (None, [
    {'name': 'usuarios', 'value': 583, 'label': 'Emily McClung de Tapia', 'selected': False, 'index': '93', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 93), (None, [
    {'name': 'usuarios', 'value': 468, 'label': 'Encarnación Ernesto Bobadilla Soto', 'selected': False, 'index': '94',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 94), (None, [
    {'name': 'usuarios', 'value': 544, 'label': 'Enrique Gómez Pech', 'selected': False, 'index': '95', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 95), (None, [
    {'name': 'usuarios', 'value': 440, 'label': 'Enrique Ojeda', 'selected': False, 'index': '96', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 96), (None, [
    {'name': 'usuarios', 'value': 561, 'label': 'Erik Juarez Blanquet', 'selected': False, 'index': '97', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 97), (None, [
    {'name': 'usuarios', 'value': 575, 'label': 'Erna M. López Granados', 'selected': False, 'index': '98', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 98), (None, [
    {'name': 'usuarios', 'value': 545, 'label': 'Ernest H. Williams', 'selected': False, 'index': '99', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 99), (None, [
    {'name': 'usuarios', 'value': 626, 'label': 'F. García Oliva', 'selected': False, 'index': '100', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 100), (None, [
    {'name': 'usuarios', 'value': 526, 'label': 'F. Gavi Reyes', 'selected': False, 'index': '101', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 101), (None, [
    {'name': 'usuarios', 'value': 629, 'label': 'F. Peña Vega', 'selected': False, 'index': '102', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 102), (None, [
    {'name': 'usuarios', 'value': 627, 'label': 'F. Pineda-García', 'selected': False, 'index': '103', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 103), (None, [
    {'name': 'usuarios', 'value': 660, 'label': 'F. Solís Domínguez', 'selected': False, 'index': '104', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 104), (None, [
    {'name': 'usuarios', 'value': 398, 'label': 'Fabiola Araceli Velázquez Ayala', 'selected': False, 'index': '105',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 105), (None, [
    {'name': 'usuarios', 'value': 505, 'label': 'Fabricio Espinoza Medrano', 'selected': False, 'index': '106',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 106), (None, [
    {'name': 'usuarios', 'value': 488, 'label': 'Federico Castrejón Ayala', 'selected': False, 'index': '107',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 107), (None, [
    {'name': 'usuarios', 'value': 458, 'label': 'Fernando Alvarado Ramos', 'selected': False, 'index': '108',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 108), (None, [
    {'name': 'usuarios', 'value': 640, 'label': 'Fernando Rosete Vergés', 'selected': False, 'index': '109',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 109), (None, [
    {'name': 'usuarios', 'value': 596, 'label': 'Francis N. Wegulo', 'selected': False, 'index': '110', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 110), (None, [
    {'name': 'usuarios', 'value': 390, 'label': 'Francisco Bautista Zúñiga', 'selected': False, 'index': '111',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 111), (None, [
    {'name': 'usuarios', 'value': 542, 'label': 'Francisco Gurri', 'selected': False, 'index': '112', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 112), (None, [
    {'name': 'usuarios', 'value': 654, 'label': 'Francisco de Asís Silva Bátiz', 'selected': False, 'index': '113',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 113), (None, [
    {'name': 'usuarios', 'value': 609, 'label': 'Frank Ostermann', 'selected': False, 'index': '114', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 114), (None, [
    {'name': 'usuarios', 'value': 404, 'label': 'Frida Nadiezda Güiza Valverde', 'selected': False, 'index': '115',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 115), (None, [
    {'name': 'usuarios', 'value': 436, 'label': 'G Legorreta Paulin', 'selected': False, 'index': '116', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 116), (None, [
    {'name': 'usuarios', 'value': 637, 'label': 'G. Rodríguez Tapia', 'selected': False, 'index': '117', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 117), (None, [
    {'name': 'usuarios', 'value': 646, 'label': 'G. E. Santana Huicochea', 'selected': False, 'index': '118',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 118), (None, [
    {'name': 'usuarios', 'value': 379, 'label': 'Gabriela Cuevas García', 'selected': False, 'index': '119',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 119), (None, [
    {'name': 'usuarios', 'value': 397, 'label': 'Gabriela Lemus', 'selected': False, 'index': '120', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 120), (None, [
    {'name': 'usuarios', 'value': 537, 'label': 'Gaspar González Sansón', 'selected': False, 'index': '121',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 121), (None, [
    {'name': 'usuarios', 'value': 543, 'label': 'Gemma Gómez Castillo', 'selected': False, 'index': '122', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 122), (None, [
    {'name': 'usuarios', 'value': 716, 'label': 'Georges Seingier', 'selected': False, 'index': '123', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 123), (None, [
    {'name': 'usuarios', 'value': 389, 'label': 'Gerardo Héctor Rubén Bocco Verdinelli', 'selected': False,
     'index': '124', 'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 124), (None, [
    {'name': 'usuarios', 'value': 621, 'label': 'Giacomo Rambaldi', 'selected': False, 'index': '125', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 125), (None, [
    {'name': 'usuarios', 'value': 445, 'label': 'Gian Delgado', 'selected': False, 'index': '126', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 126), (None, [
    {'name': 'usuarios', 'value': 576, 'label': 'Gilbert M. Nduru', 'selected': False, 'index': '127', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 127), (None, [
    {'name': 'usuarios', 'value': 528, 'label': 'Gilberto Gaxiola Castro', 'selected': False, 'index': '128',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 128), (None, [
    {'name': 'usuarios', 'value': 444, 'label': 'Guillermo Salas', 'selected': False, 'index': '129', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 129), (None, [
    {'name': 'usuarios', 'value': 680, 'label': 'Guillermo Iván Figueroa Béjar', 'selected': False, 'index': '130',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 130), (None, [
    {'name': 'usuarios', 'value': 665, 'label': 'H. Hernández Trejo', 'selected': False, 'index': '131', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 131), (None, [
    {'name': 'usuarios', 'value': 582, 'label': 'H. Leonardo Martínez Torres', 'selected': False, 'index': '132',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 132), (None, [
    {'name': 'usuarios', 'value': 406, 'label': 'Hebe Vessuri', 'selected': False, 'index': '133', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 133), (None, [
    {'name': 'usuarios', 'value': 475, 'label': 'Héctor Víctor Cabadas Báez', 'selected': False, 'index': '134',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 134), (None, [
    {'name': 'usuarios', 'value': 590, 'label': 'Helda Morales Iglesias', 'selected': False, 'index': '135',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 135), (None, [
    {'name': 'usuarios', 'value': 414, 'label': 'Hernando Rodriguez', 'selected': False, 'index': '136', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 136), (None, [
    {'name': 'usuarios', 'value': 684, 'label': 'Hijmans Hijmans', 'selected': False, 'index': '137', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 137), (None, [
    {'name': 'usuarios', 'value': 372, 'label': 'Hilda Rivas', 'selected': False, 'index': '138', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 138), (None, [
    {'name': 'usuarios', 'value': 696, 'label': 'Hind Taud', 'selected': False, 'index': '139', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 139), (None, [
    {'name': 'usuarios', 'value': 611, 'label': 'Hugo Perales', 'selected': False, 'index': '140', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 140), (None, [
    {'name': 'usuarios', 'value': 394, 'label': 'Hugo Alejandro Zavala Vaca', 'selected': False, 'index': '141',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 141), (None, [
    {'name': 'usuarios', 'value': 625, 'label': 'Hugo Magdaleno Ramírez Tobías', 'selected': False, 'index': '142',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 142), (None, [
    {'name': 'usuarios', 'value': 628, 'label': 'I. Torres-García', 'selected': False, 'index': '143', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 143), (None, [
    {'name': 'usuarios', 'value': 501, 'label': 'Ileana Espejel', 'selected': False, 'index': '144', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 144), (None, [
    {'name': 'usuarios', 'value': 498, 'label': 'Inna Dubrovina', 'selected': False, 'index': '145', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 145), (None, [
    {'name': 'usuarios', 'value': 617, 'label': 'Irene Pérez Llorente', 'selected': False, 'index': '146', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 146), (None, [
    {'name': 'usuarios', 'value': 711, 'label': 'Isela Zermeño', 'selected': False, 'index': '147', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 147), (None, [
    {'name': 'usuarios', 'value': 455, 'label': 'Israde Alcántara', 'selected': False, 'index': '148', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 148), (None, [
    {'name': 'usuarios', 'value': 652, 'label': 'Itzi Segundo', 'selected': False, 'index': '149', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 149), (None, [
    {'name': 'usuarios', 'value': 513, 'label': 'Iván Franch Pardo', 'selected': False, 'index': '150', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 150), (None, [
    {'name': 'usuarios', 'value': 437, 'label': 'J Tiburio', 'selected': False, 'index': '151', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 151), (None, [
    {'name': 'usuarios', 'value': 456, 'label': 'J. Alcántar Mejía', 'selected': False, 'index': '152', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 152), (None, [
    {'name': 'usuarios', 'value': 534, 'label': 'J. González Areu', 'selected': False, 'index': '153', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 153), (None, [
    {'name': 'usuarios', 'value': 588, 'label': 'J. Morales Contreras', 'selected': False, 'index': '154', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 154), (None, [
    {'name': 'usuarios', 'value': 633, 'label': 'J. Reyes López', 'selected': False, 'index': '155', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 155), (None, [
    {'name': 'usuarios', 'value': 710, 'label': 'J. Zavala Cruz', 'selected': False, 'index': '156', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 156), (None, [
    {'name': 'usuarios', 'value': 664, 'label': 'J. A. López Portillo', 'selected': False, 'index': '157', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 157), (None, [
    {'name': 'usuarios', 'value': 587, 'label': 'J. C. Mora Chaparro', 'selected': False, 'index': '158', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 158), (None, [
    {'name': 'usuarios', 'value': 700, 'label': 'J. F. Torrescano Valle', 'selected': False, 'index': '159',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 159), (None, [
    {'name': 'usuarios', 'value': 662, 'label': 'J. L. Palacio Prieto', 'selected': False, 'index': '160', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 160), (None, [
    {'name': 'usuarios', 'value': 694, 'label': 'J. M. Sánchez Núñez', 'selected': False, 'index': '161', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 161), (None, [
    {'name': 'usuarios', 'value': 480, 'label': 'J. P. Carbonelli', 'selected': False, 'index': '162', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 162), (None, [
    {'name': 'usuarios', 'value': 675, 'label': 'Jacquie Burgess', 'selected': False, 'index': '163', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 163), (None, [
    {'name': 'usuarios', 'value': 589, 'label': 'Jaime Morales Hernández', 'selected': False, 'index': '164',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 164), (None, [
    {'name': 'usuarios', 'value': 403, 'label': 'Jaime Paneque Gálvez', 'selected': False, 'index': '165', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 165), (None, [
    {'name': 'usuarios', 'value': 556, 'label': 'Jaime Urrutia Fucugauchi', 'selected': False, 'index': '166',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 166), (None, [
    {'name': 'usuarios', 'value': 578, 'label': 'Javier Martínez', 'selected': False, 'index': '167', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 167), (None, [
    {'name': 'usuarios', 'value': 385, 'label': 'Jean Francois Mas', 'selected': False, 'index': '168', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 168), (None, [
    {'name': 'usuarios', 'value': 641, 'label': 'Jeffrey Ross Ibarra', 'selected': False, 'index': '169', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 169), (None, [
    {'name': 'usuarios', 'value': 703, 'label': 'Jeroen Verplanke', 'selected': False, 'index': '170', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 170), (None, [
    {'name': 'usuarios', 'value': 442, 'label': 'Jesús Fuentes', 'selected': False, 'index': '171', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 171), (None, [
    {'name': 'usuarios', 'value': 573, 'label': 'Jesús Alonso Luna Béjar', 'selected': False, 'index': '172',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 172), (None, [
    {'name': 'usuarios', 'value': 531, 'label': 'Joaquin Giménez de Azcarate', 'selected': False, 'index': '173',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 173), (None, [
    {'name': 'usuarios', 'value': 433, 'label': 'John Healey', 'selected': False, 'index': '174', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 174), (None, [
    {'name': 'usuarios', 'value': 421, 'label': 'Jorge Gonzalez', 'selected': False, 'index': '175', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 175), (None, [
    {'name': 'usuarios', 'value': 687, 'label': 'Jorge Morfin Rios', 'selected': False, 'index': '176', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 176), (None, [
    {'name': 'usuarios', 'value': 620, 'label': 'Jorge Quetzal Argueta', 'selected': False, 'index': '177', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 177), (None, [
    {'name': 'usuarios', 'value': 522, 'label': 'Jorge E. Gama Castro', 'selected': False, 'index': '178', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 178), (None, [
    {'name': 'usuarios', 'value': 441, 'label': 'José Fariña', 'selected': False, 'index': '179', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 179), (None, [
    {'name': 'usuarios', 'value': 447, 'label': 'José Hernández', 'selected': False, 'index': '180', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 180), (None, [
    {'name': 'usuarios', 'value': 423, 'label': 'Jose Pimentel', 'selected': False, 'index': '181', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 181), (None, [
    {'name': 'usuarios', 'value': 658, 'label': 'José Alberto Solis Navarrete', 'selected': False, 'index': '182',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 182), (None, [
    {'name': 'usuarios', 'value': 614, 'label': 'José Aldo Plancarte Trujillo', 'selected': False, 'index': '183',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 183), (None, [
    {'name': 'usuarios', 'value': 373, 'label': 'José Antonio Navarrete Pacheco', 'selected': False, 'index': '184',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 184), (None, [
    {'name': 'usuarios', 'value': 393, 'label': 'Jose Antonio Vieyra Medrano', 'selected': False, 'index': '185',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 185), (None, [
    {'name': 'usuarios', 'value': 461, 'label': 'José Eduardo Anaya Gomez', 'selected': False, 'index': '186',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 186), (None, [
    {'name': 'usuarios', 'value': 449, 'label': 'José Luis Macías', 'selected': False, 'index': '187', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 187), (None, [
    {'name': 'usuarios', 'value': 585, 'label': 'Jose Maria Michel Fuentes', 'selected': False, 'index': '188',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 188), (None, [
    {'name': 'usuarios', 'value': 616, 'label': 'Juan Pulido', 'selected': False, 'index': '189', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 189), (None, [
    {'name': 'usuarios', 'value': 591, 'label': 'Juan J. Morales', 'selected': False, 'index': '190', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 190), (None, [
    {'name': 'usuarios', 'value': 599, 'label': 'Julie Noriega', 'selected': False, 'index': '191', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 191), (None, [
    {'name': 'usuarios', 'value': 693, 'label': 'Julio Sánchez Escudero', 'selected': False, 'index': '192',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 192), (None, [
    {'name': 'usuarios', 'value': 593, 'label': 'Julius G. Muchemi', 'selected': False, 'index': '193', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 193), (None, [
    {'name': 'usuarios', 'value': 601, 'label': 'Karen S. Oberhauser', 'selected': False, 'index': '194', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 194), (None, [
    {'name': 'usuarios', 'value': 369, 'label': 'Karine Lefebvre', 'selected': False, 'index': '195', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 195), (None, [
    {'name': 'usuarios', 'value': 697, 'label': 'Keiko Teranisho Castillo', 'selected': False, 'index': '196',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 196), (None, [
    {'name': 'usuarios', 'value': 551, 'label': 'Keith A. Hobson', 'selected': False, 'index': '197', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 197), (None, [
    {'name': 'usuarios', 'value': 384, 'label': 'Keith Michael McCall', 'selected': False, 'index': '198', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 198), (None, [
    {'name': 'usuarios', 'value': 715, 'label': 'L Menéndez Carrera', 'selected': False, 'index': '199', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 199), (None, [
    {'name': 'usuarios', 'value': 678, 'label': 'L. Morales Barquero', 'selected': False, 'index': '200', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 200), (None, [
    {'name': 'usuarios', 'value': 624, 'label': 'L. G. Ramírez Sanchez', 'selected': False, 'index': '201', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 201), (None, [
    {'name': 'usuarios', 'value': 502, 'label': 'L. M. Espinosa Rodríguez', 'selected': False, 'index': '202',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 202), (None, [
    {'name': 'usuarios', 'value': 490, 'label': 'Laura Chang Martínez', 'selected': False, 'index': '203', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 203), (None, [
    {'name': 'usuarios', 'value': 704, 'label': 'Laura Villamil Echeverri', 'selected': False, 'index': '204',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 204), (None, [
    {'name': 'usuarios', 'value': 647, 'label': 'Laura Alicia Santillán Hernández', 'selected': False, 'index': '205',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 205), (None, [
    {'name': 'usuarios', 'value': 608, 'label': 'Laura P. Osorio', 'selected': False, 'index': '206', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 206), (None, [
    {'name': 'usuarios', 'value': 707, 'label': 'Leonard I. Wassenaar', 'selected': False, 'index': '207', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 207), (None, [
    {'name': 'usuarios', 'value': 448, 'label': 'Leticia Merino', 'selected': False, 'index': '208', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 208), (None, [
    {'name': 'usuarios', 'value': 471, 'label': 'Lincoln P. Brower', 'selected': False, 'index': '209', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 209), (None, [
    {'name': 'usuarios', 'value': 509, 'label': 'Linda S. Fink', 'selected': False, 'index': '210', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 210), (None, [
    {'name': 'usuarios', 'value': 370, 'label': 'Lorena Poncela Rodríguez', 'selected': False, 'index': '211',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 211), (None, [
    {'name': 'usuarios', 'value': 690, 'label': 'Lorena Soto Pinto', 'selected': False, 'index': '212', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 212), (None, [
    {'name': 'usuarios', 'value': 706, 'label': 'Lorenzo Vázquez Selem', 'selected': False, 'index': '213', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 213), (None, [
    {'name': 'usuarios', 'value': 438, 'label': 'Lucia Almeida', 'selected': False, 'index': '214', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 214), (None, [
    {'name': 'usuarios', 'value': 451, 'label': 'Luis Cancer Pomar', 'selected': False, 'index': '215', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 215), (None, [
    {'name': 'usuarios', 'value': 497, 'label': 'Luís Dourado', 'selected': False, 'index': '216', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 216), (None, [
    {'name': 'usuarios', 'value': 428, 'label': 'Luis García', 'selected': False, 'index': '217', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 217), (None, [
    {'name': 'usuarios', 'value': 430, 'label': 'Luis Ramírez', 'selected': False, 'index': '218', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 218), (None, [
    {'name': 'usuarios', 'value': 602, 'label': 'Luis Daniel Olivares Martínez', 'selected': False, 'index': '219',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 219), (None, [
    {'name': 'usuarios', 'value': 539, 'label': 'Luis Fernando Gopar Merino', 'selected': False, 'index': '220',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 220), (None, [
    {'name': 'usuarios', 'value': 374, 'label': 'Luis Miguel Morales Manilla', 'selected': False, 'index': '221',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 221), (None, [
    {'name': 'usuarios', 'value': 429, 'label': 'Luz Elena García Martínez', 'selected': False, 'index': '222',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 222), (None, [
    {'name': 'usuarios', 'value': 467, 'label': 'M. Boada Juncá', 'selected': False, 'index': '223', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 223), (None, [
    {'name': 'usuarios', 'value': 479, 'label': 'M. Campos Sánchez', 'selected': False, 'index': '224', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 224), (None, [
    {'name': 'usuarios', 'value': 521, 'label': 'M. Farfán Gutiérrez', 'selected': False, 'index': '225', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 225), (None, [
    {'name': 'usuarios', 'value': 676, 'label': 'M. Kinyanjui', 'selected': False, 'index': '226', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 226), (None, [
    {'name': 'usuarios', 'value': 656, 'label': 'M. Solange Grimoldi', 'selected': False, 'index': '227', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 227), (None, [
    {'name': 'usuarios', 'value': 666, 'label': 'M. Vargas Sandoval', 'selected': False, 'index': '228', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 228), (None, [
    {'name': 'usuarios', 'value': 712, 'label': 'M. Zirión Martínez', 'selected': False, 'index': '229', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 229), (None, [
    {'name': 'usuarios', 'value': 552, 'label': 'M. Isabel Ramirez', 'selected': False, 'index': '230', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 230), (None, [
    {'name': 'usuarios', 'value': 572, 'label': 'M. Lourdes González Arqueros', 'selected': False, 'index': '231',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 231), (None, [
    {'name': 'usuarios', 'value': 669, 'label': 'M. R. Domìnguez Carrasco', 'selected': False, 'index': '232',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 232), (None, [
    {'name': 'usuarios', 'value': 670, 'label': 'M. T. Camacho Olmedo', 'selected': False, 'index': '233', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 233), (None, [
    {'name': 'usuarios', 'value': 377, 'label': 'Manuel Bollo Manent', 'selected': False, 'index': '234', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 234), (None, [
    {'name': 'usuarios', 'value': 520, 'label': 'Manuel J. Macía', 'selected': False, 'index': '235', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 235), (None, [
    {'name': 'usuarios', 'value': 408, 'label': 'Manuel Zavala', 'selected': False, 'index': '236', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 236), (None, [
    {'name': 'usuarios', 'value': 383, 'label': 'Manuel Eduardo Mendoza Cantú', 'selected': False, 'index': '237',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 237), (None, [
    {'name': 'usuarios', 'value': 420, 'label': 'Marcela Morales', 'selected': False, 'index': '238', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 238), (None, [
    {'name': 'usuarios', 'value': 380, 'label': 'Margaret Skutsch', 'selected': False, 'index': '239', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 239), (None, [
    {'name': 'usuarios', 'value': 426, 'label': 'Margarita Alvarado', 'selected': False, 'index': '240', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 240), (None, [
    {'name': 'usuarios', 'value': 431, 'label': 'María Vizcaíno', 'selected': False, 'index': '241', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 241), (None, [
    {'name': 'usuarios', 'value': 682, 'label': 'María del Socorro Figueroa Béjar', 'selected': False, 'index': '242',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 242), (None, [
    {'name': 'usuarios', 'value': 376, 'label': 'María Estela Carmona Jiménez', 'selected': False, 'index': '243',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 243), (None, [
    {'name': 'usuarios', 'value': 402, 'label': 'María Isabel Ramírez Ramírez', 'selected': False, 'index': '244',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 244), (None, [
    {'name': 'usuarios', 'value': 368, 'label': 'Maria Lourdes González Arqueros', 'selected': False, 'index': '245',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 245), (None, [
    {'name': 'usuarios', 'value': 671, 'label': 'María Teresa Ramírez Herrera', 'selected': False, 'index': '246',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 246), (None, [
    {'name': 'usuarios', 'value': 538, 'label': 'María Virginia González Santiago', 'selected': False, 'index': '247',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 247), (None, [
    {'name': 'usuarios', 'value': 405, 'label': 'Mariana Vallejo Ramos', 'selected': False, 'index': '248', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 248), (None, [
    {'name': 'usuarios', 'value': 363, 'label': 'Mario Figueroa Cárdenas', 'selected': False, 'index': '249',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 249), (None, [
    {'name': 'usuarios', 'value': 515, 'label': 'Mário Freitas', 'selected': False, 'index': '250', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 250), (None, [
    {'name': 'usuarios', 'value': 566, 'label': 'Marit Kraagt', 'selected': False, 'index': '251', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 251), (None, [
    {'name': 'usuarios', 'value': 392, 'label': 'Marta Astier', 'selected': False, 'index': '252', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 252), (None, [
    {'name': 'usuarios', 'value': 424, 'label': 'Martha Velazquez', 'selected': False, 'index': '253', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 253), (None, [
    {'name': 'usuarios', 'value': 605, 'label': 'Martí Orta Martínez', 'selected': False, 'index': '254', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 254), (None, [
    {'name': 'usuarios', 'value': 477, 'label': 'Martin Cadena Salgado', 'selected': False, 'index': '255', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 255), (None, [
    {'name': 'usuarios', 'value': 708, 'label': 'Martina Wilde', 'selected': False, 'index': '256', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 256), (None, [
    {'name': 'usuarios', 'value': 474, 'label': 'Matthias Bücker', 'selected': False, 'index': '257', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 257), (None, [
    {'name': 'usuarios', 'value': 564, 'label': 'Maxime Kieffer', 'selected': False, 'index': '258', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 258), (None, [
    {'name': 'usuarios', 'value': 541, 'label': 'Maximilien Gueze', 'selected': False, 'index': '259', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 259), (None, [
    {'name': 'usuarios', 'value': 527, 'label': 'Mayra Gavito', 'selected': False, 'index': '260', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 260), (None, [
    {'name': 'usuarios', 'value': 634, 'label': 'Mercedes Rivera León', 'selected': False, 'index': '261', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 261), (None, [
    {'name': 'usuarios', 'value': 470, 'label': 'Miguel Bravo', 'selected': False, 'index': '262', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 262), (None, [
    {'name': 'usuarios', 'value': 500, 'label': 'Miguel Escalona', 'selected': False, 'index': '263', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 263), (None, [
    {'name': 'usuarios', 'value': 577, 'label': 'Miguel Maass Moreno', 'selected': False, 'index': '264', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 264), (None, [
    {'name': 'usuarios', 'value': 435, 'label': 'Miguel Martínez', 'selected': False, 'index': '265', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 265), (None, [
    {'name': 'usuarios', 'value': 486, 'label': 'Miguel Angel Castillo Santiago', 'selected': False, 'index': '266',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 266), (None, [
    {'name': 'usuarios', 'value': 460, 'label': 'Mirna Ambrosio', 'selected': False, 'index': '267', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 267), (None, [
    {'name': 'usuarios', 'value': 681, 'label': 'Mónica Adriana Figueroa Béjar', 'selected': False, 'index': '268',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 268), (None, [
    {'name': 'usuarios', 'value': 546, 'label': 'Muki Haklay', 'selected': False, 'index': '269', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 269), (None, [
    {'name': 'usuarios', 'value': 713, 'label': 'N Águila Carrasco', 'selected': False, 'index': '270', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 270), (None, [
    {'name': 'usuarios', 'value': 478, 'label': 'Nadia Campos Salas', 'selected': False, 'index': '271', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 271), (None, [
    {'name': 'usuarios', 'value': 565, 'label': 'Nagesh Kolagani', 'selected': False, 'index': '272', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 272), (None, [
    {'name': 'usuarios', 'value': 469, 'label': 'Nayda Luz Bravo Hernández', 'selected': False, 'index': '273',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 273), (None, [
    {'name': 'usuarios', 'value': 689, 'label': 'Neyra Sosa Gutiérrez', 'selected': False, 'index': '274', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 274), (None, [
    {'name': 'usuarios', 'value': 702, 'label': 'Nicolás Vargas Ramírez', 'selected': False, 'index': '275',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 275), (None, [
    {'name': 'usuarios', 'value': 491, 'label': 'Noah Chutz', 'selected': False, 'index': '276', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 276), (None, [
    {'name': 'usuarios', 'value': 496, 'label': 'O. Delgado Carranza', 'selected': False, 'index': '277', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 277), (None, [
    {'name': 'usuarios', 'value': 446, 'label': 'Octavio González', 'selected': False, 'index': '278', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 278), (None, [
    {'name': 'usuarios', 'value': 410, 'label': 'Omar Montaño', 'selected': False, 'index': '279', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 279), (None, [
    {'name': 'usuarios', 'value': 632, 'label': 'Omar Raul Masera', 'selected': False, 'index': '280', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 280), (None, [
    {'name': 'usuarios', 'value': 514, 'label': 'Oscar Frausto', 'selected': False, 'index': '281', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 281), (None, [
    {'name': 'usuarios', 'value': 506, 'label': 'Osvaldo Esquivel Lucatero', 'selected': False, 'index': '282',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 282), (None, [
    {'name': 'usuarios', 'value': 484, 'label': 'Oswaldo Carrillo', 'selected': False, 'index': '283', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 283), (None, [
    {'name': 'usuarios', 'value': 663, 'label': 'P. Moreno Casasola', 'selected': False, 'index': '284', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 284), (None, [
    {'name': 'usuarios', 'value': 714, 'label': 'Pablo Álvarez', 'selected': False, 'index': '285', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 285), (None, [
    {'name': 'usuarios', 'value': 417, 'label': 'Pablo Argueta', 'selected': False, 'index': '286', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 286), (None, [
    {'name': 'usuarios', 'value': 557, 'label': 'Pablo Jaramillo López', 'selected': False, 'index': '287', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 287), (None, [
    {'name': 'usuarios', 'value': 622, 'label': 'Palaniappan Ramu', 'selected': False, 'index': '288', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 288), (None, [
    {'name': 'usuarios', 'value': 651, 'label': 'Paola Segundo Métay', 'selected': False, 'index': '289', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 289), (None, [
    {'name': 'usuarios', 'value': 465, 'label': 'Patricia Balvanera', 'selected': False, 'index': '290', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 290), (None, [
    {'name': 'usuarios', 'value': 638, 'label': 'Paul Roge', 'selected': False, 'index': '291', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 291), (None, [
    {'name': 'usuarios', 'value': 584, 'label': 'Paula Melic', 'selected': False, 'index': '292', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 292), (None, [
    {'name': 'usuarios', 'value': 371, 'label': 'Pedro Sergio Urquijo Torres', 'selected': False, 'index': '293',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 293), (None, [
    {'name': 'usuarios', 'value': 642, 'label': 'Peter Rosset', 'selected': False, 'index': '294', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 294), (None, [
    {'name': 'usuarios', 'value': 655, 'label': 'Peter Simmons', 'selected': False, 'index': '295', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 295), (None, [
    {'name': 'usuarios', 'value': 530, 'label': 'Peter R. W. Gerritsen', 'selected': False, 'index': '296', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 296), (None, [
    {'name': 'usuarios', 'value': 532, 'label': 'Pierre Glynn', 'selected': False, 'index': '297', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 297), (None, [
    {'name': 'usuarios', 'value': 367, 'label': 'Quetzalcoatl Orozco Ramirez', 'selected': False, 'index': '298',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 298), (None, [
    {'name': 'usuarios', 'value': 452, 'label': 'R. Aguilar Romero', 'selected': False, 'index': '299', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 299), (None, [
    {'name': 'usuarios', 'value': 560, 'label': 'R. Jiménez Ramírez', 'selected': False, 'index': '300', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 300), (None, [
    {'name': 'usuarios', 'value': 569, 'label': 'R. Lemoine Rodríguez', 'selected': False, 'index': '301', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 301), (None, [
    {'name': 'usuarios', 'value': 466, 'label': 'R. C. Barrientos Medina', 'selected': False, 'index': '302',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 302), (None, [
    {'name': 'usuarios', 'value': 558, 'label': 'Ramón Jarquin Gálvez', 'selected': False, 'index': '303', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 303), (None, [
    {'name': 'usuarios', 'value': 685, 'label': 'Ramón Mariaca Méndez', 'selected': False, 'index': '304', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 304), (None, [
    {'name': 'usuarios', 'value': 409, 'label': 'Raquel González García', 'selected': False, 'index': '305',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 305), (None, [
    {'name': 'usuarios', 'value': 453, 'label': 'Raúl Aguirre Gómez', 'selected': False, 'index': '306', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 306), (None, [
    {'name': 'usuarios', 'value': 489, 'label': 'Raul Cejudo Ruiz', 'selected': False, 'index': '307', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 307), (None, [
    {'name': 'usuarios', 'value': 464, 'label': 'René Arzuffi Barrera', 'selected': False, 'index': '308', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 308), (None, [
    {'name': 'usuarios', 'value': 600, 'label': 'Ricardo Nápoles', 'selected': False, 'index': '309', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 309), (None, [
    {'name': 'usuarios', 'value': 677, 'label': 'Ricardo Saucedo', 'selected': False, 'index': '310', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 310), (None, [
    {'name': 'usuarios', 'value': 439, 'label': 'Roberto Lindig', 'selected': False, 'index': '311', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 311), (None, [
    {'name': 'usuarios', 'value': 510, 'label': 'Roberto Alexander Fisher Ortíz', 'selected': False, 'index': '312',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 312), (None, [
    {'name': 'usuarios', 'value': 425, 'label': 'Rocío Aguirre', 'selected': False, 'index': '313', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 313), (None, [
    {'name': 'usuarios', 'value': 570, 'label': 'Rodrigo Liendo', 'selected': False, 'index': '314', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 314), (None, [
    {'name': 'usuarios', 'value': 661, 'label': 'Roger Guevara Hernández', 'selected': False, 'index': '315',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 315), (None, [
    {'name': 'usuarios', 'value': 691, 'label': 'Romina C. Spano', 'selected': False, 'index': '316', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 316), (None, [
    {'name': 'usuarios', 'value': 407, 'label': 'Rosa Rivas', 'selected': False, 'index': '317', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 317), (None, [
    {'name': 'usuarios', 'value': 586, 'label': 'Rosa María Molina Rojas', 'selected': False, 'index': '318',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 318), (None, [
    {'name': 'usuarios', 'value': 567, 'label': 'Rosario Langrave', 'selected': False, 'index': '319', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 319), (None, [
    {'name': 'usuarios', 'value': 395, 'label': 'Rosaura Páez Bistrain', 'selected': False, 'index': '320', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 320), (None, [
    {'name': 'usuarios', 'value': 416, 'label': 'Roser Manejo', 'selected': False, 'index': '321', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 321), (None, [
    {'name': 'usuarios', 'value': 550, 'label': 'Ruben Hernández Morales', 'selected': False, 'index': '322',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 322), (None, [
    {'name': 'usuarios', 'value': 607, 'label': 'S. Ortiz García', 'selected': False, 'index': '323', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 323), (None, [
    {'name': 'usuarios', 'value': 615, 'label': 'Sandra Pola Villaseñor', 'selected': False, 'index': '324',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 324), (None, [
    {'name': 'usuarios', 'value': 391, 'label': 'Sara Barrasa García', 'selected': False, 'index': '325', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 325), (None, [
    {'name': 'usuarios', 'value': 415, 'label': 'Sara Ortiz', 'selected': False, 'index': '326', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 326), (None, [
    {'name': 'usuarios', 'value': 366, 'label': 'Saray Bucio Mendoza', 'selected': False, 'index': '327', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 327), (None, [
    {'name': 'usuarios', 'value': 630, 'label': 'Saúl Álvarez Borrego', 'selected': False, 'index': '328', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 328), (None, [
    {'name': 'usuarios', 'value': 631, 'label': 'Selene Rangel Landa', 'selected': False, 'index': '329', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 329), (None, [
    {'name': 'usuarios', 'value': 650, 'label': 'Sergey Sedov', 'selected': False, 'index': '330', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 330), (None, [
    {'name': 'usuarios', 'value': 612, 'label': 'Sol Perez Jimenez', 'selected': False, 'index': '331', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 331), (None, [
    {'name': 'usuarios', 'value': 540, 'label': 'Solange Grimoldi', 'selected': False, 'index': '332', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 332), (None, [
    {'name': 'usuarios', 'value': 457, 'label': 'Sonia Altizer', 'selected': False, 'index': '333', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 333), (None, [
    {'name': 'usuarios', 'value': 443, 'label': 'Sophie Avila', 'selected': False, 'index': '334', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 334), (None, [
    {'name': 'usuarios', 'value': 494, 'label': 'Stéphane Couturier', 'selected': False, 'index': '335', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 335), (None, [
    {'name': 'usuarios', 'value': 472, 'label': 'Stephen Brush', 'selected': False, 'index': '336', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 336), (None, [
    {'name': 'usuarios', 'value': 613, 'label': 'Suzanne Pierce', 'selected': False, 'index': '337', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 337), (None, [
    {'name': 'usuarios', 'value': 482, 'label': 'T. Carlón Allende', 'selected': False, 'index': '338', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 338), (None, [
    {'name': 'usuarios', 'value': 555, 'label': 'Thomas J. Ihl', 'selected': False, 'index': '339', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 339), (None, [
    {'name': 'usuarios', 'value': 580, 'label': 'Tomás Martínez Saldaña', 'selected': False, 'index': '340',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 340), (None, [
    {'name': 'usuarios', 'value': 653, 'label': 'Tzitzi Sharhi Delgado', 'selected': False, 'index': '341', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 341), (None, [
    {'name': 'usuarios', 'value': 360, 'label': 'usr_st usr_st', 'selected': False, 'index': '342', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 342), (None, [
    {'name': 'usuarios', 'value': 481, 'label': 'V. Palamarczuk', 'selected': False, 'index': '343', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 343), (None, [
    {'name': 'usuarios', 'value': 667, 'label': 'V. Zamora Crescencio', 'selected': False, 'index': '344', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 344), (None, [
    {'name': 'usuarios', 'value': 547, 'label': 'V. M. Hernández Madrigal', 'selected': False, 'index': '345',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 345), (None, [
    {'name': 'usuarios', 'value': 519, 'label': 'Victoria Reyes García', 'selected': False, 'index': '346', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 346), (None, [
    {'name': 'usuarios', 'value': 592, 'label': 'Wendy Morales', 'selected': False, 'index': '347', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 347), (None, [
    {'name': 'usuarios', 'value': 672, 'label': 'Y. Calvillo García', 'selected': False, 'index': '348', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 348), (None, [
    {'name': 'usuarios', 'value': 579, 'label': 'Y. Martínez Ruíz', 'selected': False, 'index': '349', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 349), (None, [
    {'name': 'usuarios', 'value': 396, 'label': 'Yadira Mireya Méndez Lemus', 'selected': False, 'index': '350',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 350), (None, [
    {'name': 'usuarios', 'value': 683, 'label': 'Yair Merlín Uribe', 'selected': False, 'index': '351', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 351), (None, [
    {'name': 'usuarios', 'value': 450, 'label': 'Yameli Aguilar Duarte', 'selected': False, 'index': '352', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 352), (None, [
    {'name': 'usuarios', 'value': 378, 'label': 'Yan Gao', 'selected': False, 'index': '353', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 353), (None, [
    {'name': 'usuarios', 'value': 636, 'label': 'Yesenia Rodríguez López', 'selected': False, 'index': '354',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 354), (None, [
    {'name': 'usuarios', 'value': 639, 'label': 'Yessica Angélica Romero Bautista', 'selected': False, 'index': '355',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 355), (None, [
    {'name': 'usuarios', 'value': 364, 'label': 'yunsh yunsh', 'selected': False, 'index': '356', 'attrs': {},
     'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 356), (None, [
    {'name': 'usuarios', 'value': 495, 'label': 'Zoila Cárdenas Mendoza', 'selected': False, 'index': '357',
     'attrs': {}, 'type': 'select', 'template_name': 'widgets/w_select_option.html'}], 357)]
