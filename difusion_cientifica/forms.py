from SIA.widgets import *
from . models import *

from django import forms

#

class MemoriaInExtensoForm(forms.ModelForm):
    titulo = forms.CharField(widget=wCharField, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    ciudad = forms.ModelChoiceField(Ciudad.objects.all().order_by('ciudad'), widget=wSelectSingle, required=True)
    fecha = forms.CharField(widget=wDateField, required=True)
    evento = forms.ModelChoiceField(Evento.objects.all().order_by('nombre_evento'), widget=wSelectSingle, required=True)
    pais_origen = forms.ModelChoiceField(Pais.objects.all().order_by('pais'), widget=wSelectSingle, required=True)
    pagina_inicio = forms.CharField(widget=wNumberField, required=True)
    pagina_fin = forms.CharField(widget=wNumberField, required=True)
    issn = forms.CharField(widget=wCharField, required=False)
    url = forms.CharField(widget=wCharField, required=False)  # corregir valiadr url

    class Meta:
        model = MemoriaInExtenso
        exclude = ['tags', ]


class PrologoLibroForm(forms.ModelForm):
    descripcion = forms.CharField(widget=wTextarea, required=False)
    libro = forms.ModelChoiceField(Libro.objects.all().order_by('nombre_libro'), widget=wSelectSingle, required=True)
    pagina_inicio = forms.CharField(widget=wNumberField, required=True)
    pagina_fin = forms.CharField(widget=wNumberField, required=True)
    url = forms.CharField(widget=wCharField, required=False)  # corregir valiadr url

    class Meta:
        model = PrologoLibro
        exclude = ['usuario', 'tags', ]


class ResenaForm(forms.ModelForm):
    titulo = forms.CharField(widget=wCharField, required=True)
    libro_resenado = forms.ModelChoiceField(Libro.objects.all().order_by('nombre_libro'), widget=wSelectSingle, required=True)
    revista_resenada = forms.ModelChoiceField(Revista.objects.all().order_by('nombre_revista'), widget=wSelectSingle, required=True)
    descripcion = forms.CharField(widget=wTextarea, required=False)
    libro_publica = forms.ModelChoiceField(Libro.objects.all().order_by('nombre_libro'), widget=wSelectSingle, required=True)
    revista_publica = forms.ModelChoiceField(Revista.objects.all().order_by('nombre_revista'), widget=wSelectSingle, required=True)
    pagina_inicio = forms.CharField(widget=wNumberField, required=True)
    pagina_fin = forms.CharField(widget=wNumberField, required=True)
    url = forms.CharField(widget=wCharField, required=False)  # corregir valiadr url

    class Meta:
        model = Resena
        exclude = ['usuario', 'tags', ]


class OrganizacionEventoAcademicoForm(forms.ModelForm):
    class Meta:
        model = OrganizacionEventoAcademico
        exclude = ['usuario', 'tags', ]


class ParticipacionEventoAcademicoForm(forms.ModelForm):
    class Meta:
        model = ParticipacionEventoAcademico
        exclude = ['usuario', 'tags', ]
