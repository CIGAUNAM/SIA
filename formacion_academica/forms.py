from SIA.widgets import *
from .models import *
from django.conf import settings
#from django_select2.views import AutoResponseView

from django_select2.forms import ModelSelect2Widget, Select2Widget, Select2MultipleWidget
from nucleo.models import Institucion
from SIA.widgets import wDateInput


class CursoEspecializacionForm(forms.ModelForm):
    nombre = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True, label='Nombre del curso', help_text='Nombre del curso de especializacion como aparece en la constancia del mismo')
    tipo = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}), choices=getattr(settings, 'CURSO_ESPECIALIZACION_TIPO', ), required=True)
    horas = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}), required=True, label='Número de horas')
    modalidad = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}), choices=getattr(settings, 'CURSO_ESPECIALIZACION_MODALIDAD', ), required=True, help_text='Modalidad help text')
    fecha_inicio = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    fecha_fin = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=False)

    institucion = forms.ModelChoiceField(
        required=False,
        queryset=InstitucionSimple.objects.all(),
        label="Institución",
        widget=ModelSelect2Widget(
            search_fields=['institucion_nombre__icontains'],
            queryset=InstitucionSimple.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )

    class Meta:
        model = CursoEspecializacion
        exclude = ['usuario', ]


class LicenciaturaForm(forms.ModelForm):
    titulo_obtenido = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)
    distincion_obtenida = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False)

    """
    carrera = forms.ModelChoiceField(
        required=False,
        queryset=ProgramaLicenciatura.objects.all(),
        label="Carrera",
        widget=ModelSelect2Widget(
            search_fields=['programalicenciatura_nombre__icontains'],
            queryset=ProgramaLicenciatura.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
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
    """
    institucion = forms.ModelChoiceField(
        required=False,
        queryset=InstitucionSimple.objects.all(),
        label="Institución",
        widget=ModelSelect2Widget(
            search_fields=['institucion_nombre__icontains'],
            queryset=InstitucionSimple.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    titulo_tesis = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)
    #fecha_inicio = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    #fecha_fin = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    fecha_grado = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)

    class Meta:
        model = Licenciatura
        exclude = ['usuario', ]


class MaestriaForm(forms.ModelForm):
    titulo_obtenido = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)
    distincion_obtenida = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False)

    """
    programa = forms.ModelChoiceField(
        queryset=ProgramaMaestria.objects.all(),
        label="ProgramaMaestria",
        widget=ModelSelect2Widget(
            search_fields=['programamaestria_nombre__icontains'],
            queryset=ProgramaMaestria.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
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
    """
    institucion = forms.ModelChoiceField(
        required=False,
        queryset=InstitucionSimple.objects.all(),
        label="Institución",
        widget=ModelSelect2Widget(
            search_fields=['institucion_nombre__icontains'],
            queryset=InstitucionSimple.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    titulo_tesis = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)
    #tesis_url = forms.URLField(widget=URLInput(attrs={'class': 'form-control pull-right'}), required=False)
    #fecha_inicio = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    #fecha_fin = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=False)
    fecha_grado = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=False)

    class Meta:
        model = Maestria
        exclude = ['usuario', ]


class DoctoradoForm(forms.ModelForm):
    titulo_obtenido = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)
    distincion_obtenida = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False)

    """
    programa = forms.ModelChoiceField(
        queryset=ProgramaDoctorado.objects.all(),
        label="ProgramaDoctorado",
        widget=ModelSelect2Widget(
            search_fields=['programadoctorado_nombre__icontains'],
            queryset=ProgramaDoctorado.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
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
    
    """
    institucion = forms.ModelChoiceField(
        required=False,
        queryset=InstitucionSimple.objects.all(),
        label="Institución",
        widget=ModelSelect2Widget(
            search_fields=['institucion_nombre__icontains'],
            queryset=InstitucionSimple.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    titulo_tesis = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)
    #tesis_url = forms.URLField(widget=URLInput(attrs={'class': 'form-control pull-right'}), required=False)
    #fecha_inicio = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    #fecha_fin = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=False)
    fecha_grado = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=False)

    class Meta:
        model = Doctorado
        exclude = ['usuario', ]


class PostDoctoradoForm(forms.ModelForm):
    titulo_proyecto = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True, label='Título de proyecto postdoctoral')

    tutor_responsable = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Tutor o investigador responsable",
        widget=ModelSelect2Widget(
            search_fields=['first_name__icontains', 'last_name__icontains', 'username__icontains'],
            queryset=User.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )

    institucion = forms.ModelChoiceField(
        required=False,
        queryset=InstitucionSimple.objects.all(),
        label="Institución",
        widget=ModelSelect2Widget(
            search_fields=['institucion_nombre__icontains'],
            queryset=InstitucionSimple.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    entidad_financiamiento = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        choices=(('', '-------'), ('CONACYT', 'CONACYT'), ('SRE', 'SRE'), ('DGAPA', 'DGAPA'), ('OTRA', 'Otra')),
        required=True)
    otra_entidad_financiamiento = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False, label='Financiamiento de otra entidad')
    fecha_inicio = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True, label='Fecha de inicio')
    fecha_fin = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=False, label='Fecha de finalización')

    class Meta:
        model = PostDoctorado
        exclude = ['usuario', ]