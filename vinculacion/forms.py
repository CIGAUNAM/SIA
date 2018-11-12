from SIA.widgets import *
from . models import *
from django import forms
from django_select2.forms import Select2MultipleWidget, Select2Widget, ModelSelect2Widget
from investigacion.models import ProyectoInvestigacion

class ArbitrajePublicacionAcademicaForm(forms.ModelForm):
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}), required=False)
    tipo = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}), 
        choices=ARBITRAJE_ACADEMICO__TIPO, required=True)
    revista = forms.ModelChoiceField(
        required=False,
        queryset=Revista.objects.all(),
        label="Revista",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Revista.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    libro = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False, label='Libro')
    capitulo_libro = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False, label='Capítulo de libro')
    fecha_dictamen = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)

    class Meta:
        model = ArbitrajePublicacionAcademica
        exclude = ['usuario', ]


class ArbitrajeProyectoInvestigacionForm(forms.ModelForm):
    fecha = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}), required=False)
    convocatoria = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)
    dependencia = forms.ModelChoiceField(
        queryset=Dependencia.objects.all(),
        label="Dependencia",
        widget=ModelSelect2Widget(
            search_fields=['nombre_dependencia__icontains'],
            queryset=Dependencia.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )

    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model = ArbitrajeProyectoInvestigacion
        exclude = ['usuario', ]


class ArbitrajeOtraActividadForm(forms.ModelForm):
    actividad = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}), required=False)
    dependencia = forms.ModelChoiceField(
        queryset=Dependencia.objects.all(),
        label="Dependencia",
        widget=ModelSelect2Widget(
            search_fields=['nombre_dependencia__icontains'],
            queryset=Dependencia.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}            
        )
    )
    fecha = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)

    class Meta:
        model = ArbitrajeOtraActividad
        exclude = ['usuario', 'tags', ]


class RedAcademicaForm(forms.ModelForm):
    nombre = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}), required=False)
    ambito = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}), choices=getattr(settings, 'RED_ACADEMICA__CLASIFICACION', ), required=True)
    objetivos = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}), required=True)
    fecha_constitucion = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    fecha_fin = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=False)
    vigente = forms.BooleanField(required=False)
    proyecto = forms.ModelChoiceField(
        queryset=ProyectoInvestigacion.objects.all(),
        label="Proyecto de Investigación",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=ProyectoInvestigacion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )

    class Meta:
        model = RedAcademica
        exclude = []
        widgets = {
            'paises': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            "participantes": Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            "entidades": Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class ConvenioEntidadNoAcademicaForm(forms.ModelForm):
    nombre = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}), required=False)
    objetivos = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}), required=True)
    fecha_inicio = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    fecha_fin = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    es_renovacion = forms.BooleanField(required=False)
    entidades = forms.ModelMultipleChoiceField(
        queryset=Dependencia.objects.exclude(institucion_dependencia__clasificacion_institucion='ACADEMICA'),
        required=True,
        widget=Select2MultipleWidget(
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'})
        )

    class Meta:
        model = ConvenioEntidadExterna
        exclude = ['tags', ]
        widgets = {
            "participantes": Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            "financiamientos": Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class ServicioExternoEntidadNoAcademicaForm(forms.ModelForm):
    nombre_servicio = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True, label='Nombre de servicio')
    clasificacion_servicio = forms.ModelChoiceField(
        queryset=ClasificacionServicio.objects.all(),
        label="Clasificacion de servicio",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=ClasificacionServicio.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}), required=False)
    fecha_inicio = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    fecha_fin = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=False)
    incluye_financiamiento = forms.BooleanField(required=False)

    class Meta:
        model = ServicioExternoEntidadNoAcademica
        exclude = ['usuario', 'tags', ]
        widgets = {
            "financiamientos": Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            "entidades": Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class OtroProgramaVinculacionForm(forms.ModelForm):
    nombre = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)
    fecha = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    tipo = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}), choices=(('', 'Seleccionar un tipo de programa'), ('VINCULACION', 'Vinculación'), ('COLABORACION', 'Colaboración'), ('COOPERACION', 'Cooperación'), ('OTRO', 'Otro')), required=True)
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}), required=False)
    resultados = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}), required=False)
    dependencia = forms.ModelChoiceField(
        queryset=Dependencia.objects.all(),
        label="Dependencia",
        widget=ModelSelect2Widget(
            search_fields=['nombre_dependencia__icontains'],
            queryset=Dependencia.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )

    class Meta:
        model = OtroProgramaVinculacion
        exclude = ['usuario', 'tags', ]



class ClasificacionServicioForm(forms.ModelForm):
    class Meta:
        model = ClasificacionServicio
        exclude = []
        widgets = {
            'nombre_dependencia': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion_dependencia': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
        }