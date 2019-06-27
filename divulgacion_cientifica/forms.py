from SIA.widgets import *
from . models import *
from nucleo.models import Libro as LibroDivulgacion, Editorial, Coleccion
from django import forms
from django_select2.forms import Select2MultipleWidget, Select2Widget, ModelSelect2Widget
from nucleo.models import Pais

#

class ArticuloDivulgacionForm(forms.ModelForm):
    titulo = forms.CharField(
        widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True, label='Título de artículo')
    status = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        choices=getattr(settings, 'STATUS_PUBLICACION_ARTICULO', ), required=True)
    url = forms.URLField(widget=URLInput(attrs={'class': 'form-control pull-right'}), required=False)
    solo_electronico = forms.BooleanField(required=False)
    revista_divulgacion = forms.ModelChoiceField(
        queryset=RevistaDivulgacion.objects.all(),
        label="Revista",
        widget=ModelSelect2Widget(
            search_fields=['revistadivulgacion_nombre__icontains'],
            queryset=RevistaDivulgacion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    fecha_enviado = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=False, label='Fecha de envío')
    fecha_aceptado = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=False, label='Fecha de aceptación')
    fecha_enprensa = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=False, label='Fecha de envío a prensa')
    fecha_publicado = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=False, label='Fecha de publicación')
    numero = forms.CharField(widget=NumberInput(attrs={'min': 0, 'class': 'form-control pull-right'}), required=False,
                             label='Número')
    pagina_inicio = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}),
                                    required=True, label='Número de página donde inicia')
    pagina_fin = forms.CharField(
        widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}),
        required=True, label='Número de página final')
    autores_todos = forms.CharField(
        widget=Textarea(attrs={'class': 'form-control', 'rows': '3',
                               'placeholder': 'Autores tal cual se reportan en el artículo, en el orden y forma.'}),
        label='Autores como se reportan en el artículo')

    class Meta:
        model = ArticuloDivulgacion
        exclude = []
        widgets = {
            "autores": wSortedSelect2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'agradecimientos': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class CapituloLibroDivulgacionForm(forms.ModelForm):
    titulo = forms.CharField(
        widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True, label='Título del capítulo')
    libro = forms.ModelChoiceField(
        queryset=Libro.objects.filter(tipo='DIVULGACION'),
        label="Libro",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Libro.objects.filter(tipo='DIVULGACION'),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    pagina_inicio = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}),
                                    required=True, label='Número de página donde inicia')
    pagina_fin = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}),
                                 required=True, label='Número de página final')
    autores_todos = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3',
                                                           'placeholder': 'Autores tal cual se reportan en el capítulo del libro, en el orden y forma.'}),
                                    required=False, label='Autores como se reportan en el capítulo del libro')


    class Meta:
        model = CapituloLibroDivulgacion
        exclude = ['usuario', ]
        widgets = {
            "autores": wSortedSelect2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class EventoDivulgacionForm(forms.ModelForm):
    eventodivulgacion_nombre = forms.CharField(widget=TextInput(
        attrs={'class': 'form-control pull-right', 'placeholder': 'Nombre del evento académico'}),
        required=True,
        label='Nombre del evento académico')
    eventodivulgacion_tipo = forms.ModelChoiceField(
        queryset=TipoEvento.objects.all(),
        label="Tipo de evento",
        widget=ModelSelect2Widget(
            search_fields=['tipoevento_nombre__icontains'],
            queryset=TipoEvento.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right',
                   'data-placeholder': 'Seleccione el tipo de evento'}
        )
    )
    eventodivulgacion_fecha_inicio = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=True, label='Fecha de inicio del evento.')
    eventodivulgacion_fecha_fin = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=True, label='Fecha de fin del evento.')
    eventodivulgacion_pais = forms.ModelChoiceField(
        queryset=Pais.objects.all(),
        label="País",
        widget=ModelSelect2Widget(
            search_fields=['pais_nombre__icontains'],
            queryset=Pais.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right',
                   'data-placeholder': 'Seleccione el pais donde se llevó a cabo el evento'}
        )
    )
    eventodivulgacion_ciudad = forms.CharField(widget=TextInput(
        attrs={'class': 'form-control pull-right', 'placeholder': 'Ciudad donde se llevó a cabo el evento académico'}),
        required=True,
        label='Ciudad donde se llevó a cabo el evento académico')
    eventodivulgacion_ambito = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        choices=(('', '-------'), ('NACIONAL', 'Nacional'), ('INTERNACIONAL', 'Internacional')))
    eventodivulgacion_numeroponentes = forms.IntegerField(
        widget=NumberInput(attrs={'min': 0, 'class': 'form-control pull-right'}),
        required=True, label='Número de ponentes', initial='0')
    eventodivulgacion_numeroasistentes = forms.IntegerField(
        widget=NumberInput(attrs={'min': 0, 'class': 'form-control pull-right'}),
        required=True, label='Número de asistentes', initial='0')


    class Meta:
        model = EventoDivulgacion
        exclude = ['eventodivulgacion_regverificado', 'eventodivulgacion_regfechacreado', 'eventodivulgacion_regfechaactualizado', 'eventodivulgacion_regusuario']
        widgets = {
        }



class OrganizacionEventoDivulgacionForm(forms.ModelForm):
    evento = forms.ModelChoiceField(
        queryset=EventoDivulgacion.objects.all(),
        label="Evento",
        widget=ModelSelect2Widget(
            search_fields=['eventodivulgacion_nombre__icontains'],
            queryset=EventoDivulgacion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    tipo_participacion = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        choices=(('', '-------'), ('COORDINADOR', 'Coordinador general'), ('COMITE_ORGANIZADOR', 'Comité organizador'),
                 ('APOYO_TECNICO', 'Apoyo técnico'), ('OTRO', 'Otro tipo de participaciòn')), required=True)
    tipo_participacion_otro = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}),
                                              required=False, label='Otro tipo de participación')

    class Meta:
        model = OrganizacionEventoDivulgacion
        exclude = ['usuario', ]


class ParticipacionEventoDivulgacionForm(forms.ModelForm):
    tipo = forms.ChoiceField(widget=Select2Widget(
        attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        choices=(('', '------'), ('PONENCIA', 'Ponencia'), ('POSTER', 'Poster')), required=True)
    titulo = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)
    evento_text = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True,
                                  label='Nombre del evento')
    lugar_evento = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True,
                                   label='Lugar del evento')
    autores_todos = forms.CharField(widget=Textarea(
        attrs={'class': 'form-control', 'rows': '3', 'placeholder': 'Autores como aparecen publicados.'}),
                                    required=False)
    institucion = forms.ModelChoiceField(
        required=True,
        queryset=InstitucionSimple.objects.all(),
        label="Institución",
        widget=ModelSelect2Widget(
            search_fields=['institucion_nombre__icontains'],
            queryset=InstitucionSimple.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )

    ambito = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
                               choices=getattr(settings, 'EVENTO__AMBITO', ), required=True)
    por_invitacion = forms.BooleanField(required=False, label='Participación por invitación')
    ponencia_magistral = forms.BooleanField(required=False, label='Ponencia Magistral')
    fecha = forms.DateField(widget=wDateInput(attrs={'data-provide': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True, label='Fecha de la participación en el evento.')

    class Meta:
        model = ParticipacionEventoDivulgacion
        exclude = []
        widgets = {
            'autores': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class ProgramaRadioTelevisionInternetForm(forms.ModelForm):
    tema = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)
    fecha = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=True)
    descripcion = forms.CharField(
        widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}), required=False)
    actividad = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        choices=(('PRODUCCION', 'Producción'), ('PARTICIPACION', 'Participación'), ('ENTREVISTA', 'Entrevista'),
                 ('OTRA', 'Otra')),
        required=True)
    medio_divulgacion_text = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)


    class Meta:
        model = ProgramaRadioTelevisionInternet
        exclude = ['usuario', ]


class LibroDivulgacionForm(forms.ModelForm):  # Posiblemente MANTENER, creo que estaba duplicado (borrar el otro)
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

    ciudad_text = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}))
    editorial_text = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}))
    coleccion_text = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False)

    status = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        choices=getattr(settings, 'STATUS_PUBLICACION', ), required=True)
    tipo_participacion = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        choices=(('', '-------'), ('AUTORIA', 'Autoría'), ('EDICION', 'Edición'), ('COORDINACION', 'Coordinación'),
                 ('COMPILACION', 'Compilación')), required=True)
    fecha = forms.DateField(widget=wDateInput(
        attrs={'style': 'width: 100%', 'data-provider': 'datepicker',
               'class': 'datepicker form-control pull-right'}),
        required=False)
    fecha_enviado = forms.DateField(widget=wDateInput(
        attrs={'style': 'width: 100%', 'data-provider': 'datepicker',
               'class': 'datepicker form-control pull-right'}),
        required=False)
    fecha_aceptado = forms.DateField(widget=wDateInput(
        attrs={'style': 'width: 100%', 'data-provider': 'datepicker',
               'class': 'datepicker form-control pull-right'}),
        required=False)
    fecha_enprensa = forms.DateField(widget=wDateInput(
        attrs={'style': 'width: 100%', 'data-provider': 'datepicker',
               'class': 'datepicker form-control pull-right'}),
        required=False)
    fecha_publicado = forms.DateField(widget=wDateInput(
        attrs={'style': 'width: 100%', 'data-provider': 'datepicker',
               'class': 'datepicker form-control pull-right'}),
        required=False)
    numero_edicion = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}))
    numero_paginas = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}))
    volumen = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False)
    isbn = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False)
    url = forms.URLField(widget=URLInput(attrs={'class': 'form-control pull-right'}), required=False)
    autores_todos = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3',
                                                           'placeholder': 'Autores tal cual se reportan en el artículo, en el orden y forma.'}),
                                    required=False, label='Autores como se reportan en el artículo')

    class Meta:
        model = LibroDivulgacion
        exclude = ['tipo', ]
        widgets = {
            "autores": wSortedSelect2MultipleWidget(
                attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            "editores": wSortedSelect2MultipleWidget(
                attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            "coordinadores": wSortedSelect2MultipleWidget(
                attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'compiladores': wSortedSelect2MultipleWidget(
                attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'agradecimientos': Select2MultipleWidget(
                attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }
