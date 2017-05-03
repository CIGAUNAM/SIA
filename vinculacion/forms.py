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
    class Meta:
        model = ArbitrajeOtraActividad
        exclude = ['usuario', 'tags', ]


class RedAcademicaForm(forms.ModelForm):
    class Meta:
        model = RedAcademica
        exclude = ['tags', ]


class ConvenioEntidadNoAcademicaForm(forms.ModelForm):
    class Meta:
        model = ConvenioEntidadNoAcademica
        exclude = ['tags', ]


class ServicioExternoEntidadNoAcademicaForm(forms.ModelForm):
    class Meta:
        model = ServicioExternoEntidadNoAcademica
        exclude = ['usuario', 'tags', ]


class OtroProgramaVinculacionForm(forms.ModelForm):
    class Meta:
        model = OtroProgramaVinculacion
        exclude = ['usuario', 'tags', ]