from SIA.widgets import *
from . models import *
from django import forms
from django_select2.forms import Select2MultipleWidget

#

class ArbitrajePublicacionAcademicaForm(forms.ModelForm):
    descripcion = forms.CharField(widget=wTextarea, required=False)
    tipo = forms.ChoiceField(widget=Select3Widget, choices=getattr(settings, 'ARBITRAJE_ACADEMCICA__TIPO', ), required=True)
    revista = forms.ModelChoiceField(
        required=False,
        queryset=Revista.objects.all(),
        label="Revista",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    libro = forms.ModelChoiceField(
        required=False,
        queryset=Libro.objects.all(),
        label="Libro",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    capitulo_libro = forms.ModelChoiceField(
        required=False,
        queryset=CapituloLibroInvestigacion.objects.all(),
        label="Capitulo en Libro de Investigación",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    fecha_dictamen = forms.DateField(widget=wDateField, required=True)

    class Meta:
        model = ArbitrajePublicacionAcademica
        exclude = ['usuario', 'tags', ]
        widgets = {
            'indices': Select3MultipleWidget,
        }


class ArbitrajeProyectoInvestigacionForm(forms.ModelForm):
    fecha = forms.DateField(widget=wDateField, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    proyecto = forms.ModelChoiceField(
        queryset=Proyecto.objects.all(),
        label="Proyecto de Investigación",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )

    class Meta:
        model = ArbitrajeProyectoInvestigacion
        exclude = ['usuario', 'tags', ]


class ArbitrajeOtraActividadForm(forms.ModelForm):
    actividad = forms.CharField(widget=wTextInput, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    institucion = forms.ModelChoiceField(
        queryset=Institucion.objects.all(),
        label="Institución",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    dependencia = forms.ModelChoiceField(
        queryset=Dependencia.objects.all(),
        label="Dependencia",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            dependent_fields={'institucion': 'institucion'},
            max_results=500,
        )
    )
    fecha = forms.DateField(widget=wDateField, required=True)

    class Meta:
        model = ArbitrajeOtraActividad
        exclude = ['usuario', 'tags', ]


class RedAcademicaForm(forms.ModelForm):
    nombre = forms.CharField(widget=wTextInput, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    clasificacion = forms.ChoiceField(widget=Select3Widget, choices=getattr(settings, 'RED_ACADEMICA__CLASIFICACION', ), required=True)
    objetivos = forms.CharField(widget=wTextarea, required=True)
    fecha_constitucion = forms.DateField(widget=wDateField, required=True)
    vigente = forms.BooleanField(required=False)
    proyecto = forms.ModelChoiceField(
        queryset=Proyecto.objects.all(),
        label="Proyecto de Investigación",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )

    class Meta:
        model = RedAcademica
        exclude = ['tags', ]
        widgets = {
            'paises': Select3MultipleWidget,
            'usuarios': Select3MultipleWidget,
        }



class ConvenioEntidadNoAcademicaForm(forms.ModelForm):
    nombre = forms.CharField(widget=wTextInput, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    es_agradecimiento = forms.BooleanField(required=False)
    clasificacion_entidad = forms.ChoiceField(widget=Select3Widget, choices=getattr(settings, 'ENTIDAD_NO_ACADEMICA__CLASIFICACION', ), required=True)
    objetivos = forms.CharField(widget=wTextarea(attrs={'placeholder': 'Objetivos esperados o logrados con el convenio'}), required=True)
    fecha_inicio = forms.DateField(widget=wDateField, required=True)
    fecha_fin = forms.DateField(widget=wDateField, required=True)
    es_renovacion = forms.BooleanField(required=False)
    incluye_financiamiento = forms.BooleanField(required=False)
    institucion = forms.ModelChoiceField(
        queryset=Institucion.objects.all(),
        label="Institución",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    dependencia = forms.ModelChoiceField(
        queryset=Dependencia.objects.all(),
        label="Dependencia",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            dependent_fields={'institucion': 'institucion'},
            max_results=500,
        )
    )

    class Meta:
        model = ConvenioEntidadNoAcademica
        exclude = ['tags', ]
        widgets = {
            'usuarios': Select3MultipleWidget,
        }


class ServicioExternoEntidadNoAcademicaForm(forms.ModelForm):
    nombre_servicio = forms.CharField(widget=wTextInput, required=True, label='Nombre de servicio')
    clasificacion_servicio = forms.ModelChoiceField(
        queryset=ClasificacionServicio.objects.all(),
        label="Clasificacion de servicio",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            dependent_fields={'institucion': 'institucion'},
            max_results=500,
        )
    )
    descripcion = forms.CharField(widget=wTextarea, required=False)
    institucion = forms.ModelChoiceField(
        queryset=Institucion.objects.all(),
        label="Institución",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    dependencia = forms.ModelChoiceField(
        queryset=Dependencia.objects.all(),
        label="Dependencia",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            dependent_fields={'institucion': 'institucion'},
            max_results=500,
        )
    )
    clasificacion_entidad = forms.ChoiceField(widget=Select3Widget, choices=getattr(settings, 'ENTIDAD_NO_ACADEMICA__CLASIFICACION', ), required=True)
    fecha_inicio = forms.DateField(widget=wDateField, required=True)
    fecha_fin = forms.DateField(widget=wDateField, required=True)
    incluye_financiamiento = forms.BooleanField(required=False)

    class Meta:
        model = ServicioExternoEntidadNoAcademica
        exclude = ['usuario', 'tags', ]


class OtroProgramaVinculacionForm(forms.ModelForm):
    nombre = forms.CharField(widget=wTextInput, required=True)
    fecha = forms.DateField(widget=wDateField, required=True)
    tipo = forms.ChoiceField(widget=Select3Widget, choices=(('VINCULACION', 'Vinculación'), ('COLABORACION', 'Colaboración'), ('COOPERACION', 'Cooperación'), ('OTRO', 'Otro')), required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    resultados = forms.CharField(widget=wTextarea, required=False)
    institucion = forms.ModelChoiceField(
        queryset=Institucion.objects.all(),
        label="Institución",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    dependencia = forms.ModelChoiceField(
        queryset=Dependencia.objects.all(),
        label="Dependencia",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            dependent_fields={'institucion': 'institucion'},
            max_results=500,
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
            'nombre': wTextInput,
            'descripcion': wTextarea,
        }