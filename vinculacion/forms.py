from SIA.widgets import *
from . models import *
from django import forms

#

class ArbitrajePublicacionAcademicaForm(forms.ModelForm):
    descripcion = forms.CharField(widget=wTextarea, required=False)
    revista = forms.ModelChoiceField(Revista.objects.all().order_by('nombre_revista'), widget=wSelectSingle, required=True)
    libro = forms.ModelChoiceField(Libro.objects.all().order_by('nombre_libro'), widget=wSelectSingle, required=True)
    capitulo_libro = forms.ModelChoiceField(CapituloLibroInvestigacion.objects.all().order_by('titulo'), widget=wSelectSingle, required=True)
    fecha_dictamen = forms.CharField(widget=wDateField, required=True)

    class Meta:
        model = ArbitrajePublicacionAcademica
        exclude = ['usuario', 'tags', ]


class ArbitrajeProyectoInvestigacionForm(forms.ModelForm):
    fecha = forms.CharField(widget=wDateField, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    proyecto = forms.ModelChoiceField(Proyecto.objects.all().order_by('nombre_proyecto'), widget=wSelectSingle, required=True)

    class Meta:
        model = ArbitrajeProyectoInvestigacion
        exclude = ['usuario', 'tags', ]


class ArbitrajeOtraActividadForm(forms.ModelForm):
    actividad = forms.CharField(widget=wCharField, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    dependencia = forms.ModelChoiceField(Dependencia.objects.all().order_by('dependencia'), widget=wSelectSingle, required=True)
    fecha = forms.CharField(widget=wDateField, required=True)

    class Meta:
        model = ArbitrajeOtraActividad
        exclude = ['usuario', 'tags', ]


class RedAcademicaForm(forms.ModelForm):
    nombre = forms.CharField(widget=wCharField, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    clasificacion = forms.ChoiceField(widget=wSelectSingle, choices=getattr(settings, 'RED_ACADEMICA__CLASIFICACION', ), required=True)
    objetivos = forms.CharField(widget=wTextarea, required=True)
    fecha_constitucion = forms.CharField(widget=wDateField, required=True)
    vigente = forms.BooleanField()

    class Meta:
        model = RedAcademica
        exclude = ['tags', ]


class ConvenioEntidadNoAcademicaForm(forms.ModelForm):
    nombre = forms.CharField(widget=wCharField, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    es_agradecimiento = forms.BooleanField()
    clasificacion = forms.ChoiceField(widget=wSelectSingle, choices=getattr(settings, 'ENTIDAD_NO_ACADEMICA__CLASIFICACION', ), required=True)
    objetivos = forms.CharField(widget=wTextarea, required=False)
    fecha_inicio = forms.CharField(widget=wDateField, required=True)
    fecha_fin = forms.CharField(widget=wDateField, required=True)
    es_renovacion = forms.BooleanField(required=False)
    incluye_financiamiento = forms.BooleanField()

    class Meta:
        model = ConvenioEntidadNoAcademica
        exclude = ['tags', ]


class ServicioExternoEntidadNoAcademicaForm(forms.ModelForm):
    nombre_servicio = forms.CharField(widget=wCharField, required=True)
    clasificacion_servicio = forms.ModelChoiceField(ClasificacionServicio.objects.all().order_by('nombre'), widget=wSelectSingle, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    dependencia = forms.ModelChoiceField(Dependencia.objects.all().order_by('dependencia'), widget=wSelectSingle, required=True)
    clasificacion_entidad = forms.ChoiceField(widget=wSelectSingle, choices=getattr(settings, 'ENTIDAD_NO_ACADEMICA__CLASIFICACION', ), required=True)
    fecha_inicio = forms.CharField(widget=wDateField, required=True)
    fecha_fin = forms.CharField(widget=wDateField, required=True)
    incluye_financiamiento = forms.BooleanField()

    class Meta:
        model = ServicioExternoEntidadNoAcademica
        exclude = ['usuario', 'tags', ]


class OtroProgramaVinculacionForm(forms.ModelForm):
    nombre = forms.CharField(widget=wCharField, required=True)
    fecha = forms.CharField(widget=wDateField, required=True)
    tipo = forms.ChoiceField(widget=wSelectSingle, choices=(('', '',), ('', '',), ('VINCULACION', 'Vinculación'), ('COLABORACION', 'Colaboración'), ('COOPERACION', 'Cooperación'), ('OTRO', 'Otro')), required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    resultados = forms.CharField(widget=wTextarea, required=False)

    class Meta:
        model = OtroProgramaVinculacion
        exclude = ['usuario', 'tags', ]