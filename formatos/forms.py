from SIA.widgets import *
from .models import *
from django_select2.forms import Select2Widget, ModelSelect2Widget, ModelSelect2MultipleWidget, Select2MultipleWidget
from django.forms.widgets import DateTimeInput
from investigacion.models import ProyectoInvestigacion

class FormatoServicioTransporteForm(forms.ModelForm):
    uso = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
                            choices=(('', '-------'), ('DOCENCIA', 'Docencia'), ('INVESTIGACION', 'Investigaciòn')))
    #modalidad = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}), choices=getattr(settings, 'CURSO_ESPECIALIZACION_MODALIDAD', ), required=True, help_text='Modalidad help text')
    num_pasajeros = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}), label='Número de pasajeros')
    tipo = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
                            choices=(('', '-------'), ('LOCAL', 'Local (dentro del área metropolitana)'), ('FORANEO', 'Foraneo (fuera del área metropolitana)')), label='Tipo de servicio')
    estado = forms.ModelChoiceField(
        required=False,
        queryset=Estado.objects.filter(pais__nombre='México'),
        label="Estado",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Estado.objects.filter(pais__nombre='México'),
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
    km_aprox = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}), label='Kilometros aproximados')
    gasto_casetas = forms.CharField(widget=NumberInput(attrs={'min': 0, 'class': 'form-control pull-right'}),
                                     label='Gasto en casetas')
    fecha_inicio = forms.DateTimeField(
        widget=DateTimeInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=True)
    fecha_fin = forms.DateTimeField(
        widget=DateTimeInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=True)
    salidas_diarias = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}), required=True,
                            label='Salidas diarias')
    tiempo_completo = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}), required=True,
                            label='Tiempo completo (días)')
    objetivo = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
                               required=False, label='Objetivos', help_text='')

    class Meta:
        model = FormatoServicioTransporte
        exclude = ['fecha', 'usuario', ]


class FormatoLicenciaGoceSueldoForm(forms.ModelForm):
    evento = forms.ModelChoiceField(
        required=False,
        queryset=Evento.objects.all(),
        label="Evento",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Evento.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    tipo_participacion = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True, label='Tipo de participación', help_text='Tipo de participación')
    fecha_inicio = forms.DateTimeField(
        widget=DateTimeInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=True)
    fecha_fin = forms.DateTimeField(
        widget=DateTimeInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=True)
    importancia = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
                               required=False, label='Importancia', help_text='')
    costo = forms.CharField(widget=NumberInput(attrs={'min': 0, 'class': 'form-control pull-right'}),
                                     label='Costo')
    proyecto = forms.ModelChoiceField(
        required=False,
        queryset=ProyectoInvestigacion.objects.all(),
        label="Proyecto de investigación",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=ProyectoInvestigacion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    presupuesto_personal = forms.CharField(widget=NumberInput(attrs={'min': 0, 'class': 'form-control pull-right'}),
                                     label='Presupuesto Personal')
    carta_invitacion = forms.BooleanField(label='Tiene carta de invitación', required=False)
    aceptacion_ponencia = forms.BooleanField(label='Aceptación de ponencia', required=False)
    otro = forms.BooleanField(label='Otro', required=False)

    class Meta:
        model = FormatoLicenciaGoceSueldo
        exclude = ['fecha', 'usuario', ]


class FormatoPagoViaticoForm(forms.ModelForm):
    evento = forms.ModelChoiceField(
        required=False,
        queryset=Evento.objects.all(),
        label="Evento",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Evento.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    tipo_participacion = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True, label='Tipo de participación', help_text='Tipo de participación')
    fecha_salida = forms.DateTimeField(
        widget=DateTimeInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=True)
    fecha_regreso = forms.DateTimeField(
        widget=DateTimeInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=True)

    class Meta:
        model = FormatoPagoViatico
        exclude = ['fecha', 'usuario', ]
