from SIA.widgets import *
from .models import *
from django_select2.forms import Select2Widget, ModelSelect2Widget, ModelSelect2MultipleWidget, Select2MultipleWidget
from django.forms.widgets import DateTimeInput
from investigacion.models import ProyectoInvestigacion

class FormatoServicioTransporteForm(forms.ModelForm):
    uso = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
                            choices=(('', '-------'), ('DOCENCIA', 'Docencia'), ('INVESTIGACION', 'Investigaciòn')))
    #modalidad = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}), choices=getattr(settings, 'CURSO_ESPECIALIZACION_MODALIDAD', ), required=True, help_text='Modalidad help text')
    num_pasajeros = forms.IntegerField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}), label='Número de pasajeros')
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
    km_aprox = forms.IntegerField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}), label='Kilometros aproximados')
    gasto_casetas = forms.DecimalField(widget=NumberInput(attrs={'min': 0.0, 'class': 'form-control pull-right'}),
                                     label='Gasto en casetas')
    fecha_inicio = forms.DateTimeField(
        widget=DateTimeInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=True)
    fecha_fin = forms.DateTimeField(
        widget=DateTimeInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=True)
    salidas_diarias = forms.IntegerField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}), required=True,
                            label='Salidas diarias')
    tiempo_completo = forms.IntegerField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}), required=True,
                            label='Tiempo completo (días)')
    objetivo = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
                               required=False, label='Objetivos', help_text='')

    class Meta:
        model = FormatoServicioTransporte
        exclude = ['fecha', 'usuario', ]


class FormatoLicenciaGoceSueldoForm(forms.ModelForm):
    evento = forms.ModelChoiceField(
        required=True,
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
                               required=True, label='Importancia', help_text='')
    costo = forms.DecimalField(widget=NumberInput(attrs={'min': 0.0, 'class': 'form-control pull-right'}),
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
    presupuesto_personal = forms.DecimalField(widget=NumberInput(attrs={'min': 0.0, 'class': 'form-control pull-right'}),
                                     label='Presupuesto Personal')
    carta_invitacion = forms.BooleanField(label='Tiene carta de invitación', required=False)
    aceptacion_ponencia = forms.BooleanField(label='Aceptación de ponencia', required=False)
    otro = forms.BooleanField(label='Otro', required=False)
    otro_anexo = forms.CharField(label='Otro', widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False,
                                         help_text='Otro.')

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
    fecha_salida = forms.DateTimeField(
        widget=DateTimeInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=True)
    fecha_regreso = forms.DateTimeField(
        widget=DateTimeInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=True)
    actividades = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
                                  required=False, label='Actividades', help_text='')
    importe = forms.DecimalField(widget=NumberInput(attrs={'min': 0.0, 'class': 'form-control pull-right'}),
                                     label='Importe')
    num_acta = forms.IntegerField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}), label='Número de acta de consejo interno')
    nombre_cheque = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Nombre del cheque",
        widget=ModelSelect2Widget(
            search_fields=['first_name__icontains', 'last_name__icontains', 'username__icontains'],
            queryset=User.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    cargo_papiit = forms.BooleanField(required=False)
    cargo_conacyt = forms.BooleanField(required=False)
    cargo_papime = forms.BooleanField(required=False)
    cargo_ie = forms.BooleanField(required=False)
    cargo_po = forms.BooleanField(required=False)
    cargo_paep = forms.BooleanField(required=False)
    cargo_otro = forms.BooleanField(required=False)
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

    class Meta:
        model = FormatoPagoViatico
        exclude = ['fecha', 'usuario', ]
