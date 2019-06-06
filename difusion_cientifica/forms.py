from SIA.widgets import *
from . models import *

from django import forms
from nucleo.models import Pais
from django_select2.forms import ModelSelect2Widget, Select2Widget

#

class MemoriaInExtensoForm(forms.ModelForm):
    nombre = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True, label='Título de memoria in extenso')
    evento_text = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True, label='Nombre del evento')
    lugar = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True, label='Lugar del evento')
    fecha = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        label='Fecha del evento donde se publicó la memoria.')
    pais = forms.ModelChoiceField(
        queryset=Pais.objects.all(),
        label="País",
        widget=ModelSelect2Widget(
            search_fields=['pais_nombre__icontains'],
            queryset=Pais.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right',
                   'data-placeholder': 'Seleccione el pais donde se llevó a cabo el evento.'}
        )
    )
    ciudad = forms.CharField(widget=TextInput(
        attrs={'class': 'form-control pull-right', 'placeholder': 'Ciudad donde se llevó a cabo el evento.'}),
        label='Ciudad donde se llevó a cabo el evento.')
    autores_todos = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': 'Autores como aparecen en la memoria'}),
                                  required=True)
    institucion = forms.ModelChoiceField(
        queryset=InstitucionSimple.objects.all(),
        label="Institución",
        widget=ModelSelect2Widget(
            search_fields=['institucion_nombre__icontains'],
            queryset=InstitucionSimple.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    pagina_inicio = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}),
                                    label='Número de página inicial')
    pagina_fin = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}),
                                 label='Número de página final')
    isbn = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False)
    url = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False)

    class Meta:
        model = MemoriaInExtenso
        exclude = []
        widgets = {
            'autores': wSortedSelect2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class EventoDifusionForm(forms.ModelForm):
    eventodifusion_nombre = forms.CharField(widget=TextInput(
        attrs={'class': 'form-control pull-right', 'placeholder': 'Nombre del evento académico'}),
        required=True,
        label='Nombre del evento académico')
    eventodifusion_tipo = forms.ModelChoiceField(
        queryset=TipoEvento.objects.all(),
        label="Tipo de evento",
        widget=ModelSelect2Widget(
            search_fields=['tipoevento_nombre__icontains'],
            queryset=TipoEvento.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right',
                   'data-placeholder': 'Seleccione el tipo de evento'}
        )
    )
    eventodifusion_fecha_inicio = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=True, label='Fecha de inicio del evento.')
    eventodifusion_fecha_fin = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=True, label='Fecha de fin del evento.')
    eventodifusion_pais = forms.ModelChoiceField(
        queryset=Pais.objects.all(),
        label="País",
        widget=ModelSelect2Widget(
            search_fields=['pais_nombre__icontains'],
            queryset=Pais.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right',
                   'data-placeholder': 'Seleccione el pais donde se llevó a cabo el evento'}
        )
    )
    eventodifusion_ciudad = forms.CharField(widget=TextInput(
        attrs={'class': 'form-control pull-right', 'placeholder': 'Ciudad donde se llevó a cabo el evento académico'}),
        required=True,
        label='Ciudad donde se llevó a cabo el evento académico')
    eventodifusion_ambito = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        choices=(('', '-------'), ('NACIONAL', 'Nacional'), ('INTERNACIONAL', 'Internacional')))
    eventodifusion_numeroponentes = forms.IntegerField(
        widget=NumberInput(attrs={'min': 0, 'class': 'form-control pull-right'}),
        required=True, label='Número de ponentes', initial='0')
    eventodifusion_numeroasistentes = forms.IntegerField(
        widget=NumberInput(attrs={'min': 0, 'class': 'form-control pull-right'}),
        required=True, label='Número de asistentes', initial='0')


    class Meta:
        model = EventoDifusion
        exclude = ['eventodifusion_regverificado', 'eventodifusion_regfechacreado', 'eventodifusion_regfechaactualizado', 'eventodifusion_regusuario']
        widgets = {
        }


class OrganizacionEventoAcademicoForm(forms.ModelForm):
    evento = forms.ModelChoiceField(
        queryset=EventoDifusion.objects.all(),
        label="Evento",
        widget=ModelSelect2Widget(
            search_fields=['eventodifusion_nombre__icontains'],
            queryset=EventoDifusion.objects.all(),
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
        model = OrganizacionEventoAcademico
        exclude = ['usuario', ]


class ParticipacionEventoAcademicoForm(forms.ModelForm):
    tipo = forms.ChoiceField(widget=Select2Widget(
        attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        choices=(('', '------'), ('PONENCIA', 'Ponencia'), ('POSTER', 'Poster')))

    titulo = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}))
    evento = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), label='Nombre del evento')
    lugar_evento = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), label='Lugar del evento')
    autores_todos = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': 'Autores como aparecen publicados.'}))
    ambito = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}), choices=getattr(settings, 'EVENTO__AMBITO', ))
    por_invitacion = forms.BooleanField(required=False, label='Participación por invitación')
    ponencia_magistral = forms.BooleanField(required=False, label='Ponencia Magistral')
    fecha = forms.DateField(widget=wDateInput(attrs={'data-provide': 'datepicker', 'class': 'datepicker form-control pull-right'}), label='Fecha de la participación en el evento.')
    institucion = forms.ModelChoiceField(
        queryset=InstitucionSimple.objects.all(),
        label="Institución",
        widget=ModelSelect2Widget(
            search_fields=['institucion_nombre__icontains'],
            queryset=InstitucionSimple.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    pais = forms.ModelChoiceField(
        queryset=Pais.objects.all(),
        label="País",
        widget=ModelSelect2Widget(
            search_fields=['pais_nombre__icontains'],
            queryset=Pais.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right',
                   'data-placeholder': 'Seleccione el pais donde se llevó a cabo el evento.'}
        )
    )
    ciudad = forms.CharField(widget=TextInput(
        attrs={'class': 'form-control pull-right', 'placeholder': 'Ciudad donde se llevó a cabo el evento.'}),
        label='Ciudad donde se llevó a cabo el evento.')

    class Meta:
        model = ParticipacionEventoAcademico
        exclude = []
        widgets = {
            'autores': wSortedSelect2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }
