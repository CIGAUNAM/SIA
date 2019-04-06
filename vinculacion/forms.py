from SIA.widgets import *
from . models import *
from django import forms
from django_select2.forms import Select2MultipleWidget,Select2Widget, ModelSelect2Widget
from investigacion.models import ProyectoInvestigacion, LibroInvestigacion, CapituloLibroInvestigacion

ARBITRAJE_ACADEMICO__TIPO = getattr(settings, 'ARBITRAJE_ACADEMICA__TIPO',
                                    (('', '-------'), ('ARTICULO', 'Artículo en revista'), ('LIBRO', 'Libro'), ('CAPITULO_LIBRO', 'Capítulo de libro')))
#

class ArbitrajePublicacionAcademicaForm(forms.ModelForm):
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




class OtraComisionForm(forms.ModelForm):
    comision = forms.ModelChoiceField(
        queryset=ComisionVinculacion.objects.all(),
        label="Comisión",
        widget=ModelSelect2Widget(
            search_fields=['comisionvinculacion_nombre__icontains'],
            queryset=ComisionVinculacion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    comision_otra = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)
    institucion2 = forms.ModelChoiceField(
        queryset=Institucion.objects.all(),
        label="Institución",
        widget=ModelSelect2Widget(
            search_fields=['nombre_institucion__icontains'],
            queryset=Institucion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    dependencia = forms.ModelChoiceField(
        queryset=Dependencia.objects.all(),
        label="Dependencia",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            dependent_fields={'institucion': 'institucion'},
            queryset=Dependencia.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}            
        )
    )
    fecha_inicio = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    fecha_fin = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)

    class Meta:
        model = OtraComision
        exclude = ['usuario', ]


class RedAcademicaForm(forms.ModelForm):
    nombre = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)
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


class ConvenioOtraEntidadForm(forms.ModelForm):
    nombre = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)
    entidades = forms.ModelMultipleChoiceField(
        queryset=Dependencia.objects.all(),
        required=True,
        widget=Select2MultipleWidget(
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'})
        )
    objetivos = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}), required=True)
    fecha_inicio = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    fecha_fin = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    es_renovacion = forms.BooleanField(required=False)

    financiamiento_text = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)
    proyecto = forms.ModelChoiceField(
        queryset=ProyectoInvestigacion.objects.all(),
        label="Proyecto de investigación",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=ProyectoInvestigacion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )

    class Meta:
        model = ConvenioOtraEntidad
        exclude = []
        widgets = {
            "participantes": Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class ServicioAsesoriaExternaForm(forms.ModelForm):
    nombre_servicio = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True, label='Nombre de servicio')
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}), required=False)
    fecha_inicio = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    fecha_fin = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=False)

    institucion = forms.ModelChoiceField(
        queryset=InstitucionSimple.objects.all(),
        label="Proyecto de investigación",
        widget=ModelSelect2Widget(
            search_fields=['institucion_nombre__icontains'],
            queryset=InstitucionSimple.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    financiamiento_text = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True, label='Nombre de servicio')


    class Meta:
        model = ServicioAsesoriaExterna
        exclude = ['usuario', ]