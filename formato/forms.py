from SIA.widgets import *
from .models import *
from django_select2.forms import Select2Widget, ModelSelect2Widget, ModelSelect2MultipleWidget, Select2MultipleWidget


class FormatoServicioTransporteForm(forms.ModelForm):
    fecha = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=True)
    uso = forms.ChoiceField(widget=Select2Widget(attrs={'class': 'form-control pull-right'}),
                            choices=(('', '-------'), ('DOCENCIA' 'Docencia'), ('INVESTIGACION', 'Investigaciòn')))
    num_pasajeros = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}), label='Número de pasajeros')
    tipo = forms.ChoiceField(widget=Select2Widget(attrs={'class': 'form-control pull-right'}),
                            choices=(('', '-------'), ('LOCAL', 'Local (dentro del área metropolitana)'), ('FORANEO', 'Foraneo (fuera del área metropolitana)')), label='Tipo de servicio')
    estado = forms.ModelChoiceField(
        required=False,
        queryset=Estado.objects.filter(pais__nombre='México'),
        label="Estado",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Estado.objects.filter(pais__nombre='México'),
            attrs={'class': 'form-control pull-right'}
        )
    )
    ciudad = forms.ModelChoiceField(
        queryset=Ciudad.objects.all(),
        label="Ciudad",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            dependent_fields={'estado': 'estado'},
            queryset=Ciudad.objects.all(),
            attrs={'class': 'form-control pull-right'}
        )
    )
    km_aprox = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}), label='Número de pasajeros')
    gasto_casetas = forms.CharField(widget=NumberInput(attrs={'min': 0, 'class': 'form-control pull-right'}),
                                     label='Gasto en casetas')
    fecha_inicio = forms.DateTimeField(
        widget=wDateTimeInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=True)
    fecha_fin = forms.DateTimeField(
        widget=wDateTimeInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=True)




