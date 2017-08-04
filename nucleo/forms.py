from .models import *
from django import forms
from django.core.exceptions import ValidationError

from SIA.widgets import *
from django.forms import widgets

#


"""
class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        exclude = []

    def clean_tag(self):
        return self.cleaned_data['tag'].lower()
"""

"""
class ZonaPaisForm(forms.ModelForm):
    class Meta:
        model = ZonaPais
        exclude = []
"""


class PaisForm(forms.ModelForm):
    zona = forms.ModelChoiceField(
        queryset=ZonaPais.objects.all(),
        label="Zona",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )

    class Meta:
        model = Pais
        exclude = []
        widgets = {
            'nombre': wTextInput,
            'nombre_extendido': wTextInput,
            'codigo': wTextInput,
        }


class EstadoForm(forms.ModelForm):
    pais = forms.ModelChoiceField(
        queryset=Pais.objects.all(),
        label="País",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )

    class Meta:
        model = Estado
        exclude = []
        widgets = {
            'nombre': wTextInput,
        }


class CiudadForm(forms.ModelForm):
    estado = forms.ModelChoiceField(
        queryset=Estado.objects.all(),
        label="Estado",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )

    class Meta:
        model = Ciudad
        exclude = []
        widgets = {
            'nombre': wTextInput,
        }


class InstitucionForm(forms.ModelForm):
    pais = forms.ModelChoiceField(
        queryset=Pais.objects.all(),
        label="País",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )

    class Meta:
        model = Institucion
        exclude = []
        widgets = {
            'nombre': wTextInput,
            'descripcion': wTextarea,
        }


class DependenciaForm(forms.ModelForm):
    institucion = forms.ModelChoiceField(
        queryset=Institucion.objects.all(),
        label="Institución",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    ciudad = forms.ModelChoiceField(
        queryset=Ciudad.objects.all(),
        label="Ciudad",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    subsistema_unam = forms.ChoiceField(widget=Select3Widget,
                                        choices=(('DIFUSION_CULTURAL', 'Subsistema de Difusión Cultural'),
                                                 ('ESTUDIOS_POSGRADO', 'Subsistema de Estudios de Posgrado'),
                                                 ('HUMANIDADES', 'Subsistema de Humanidades'),
                                                 ('INVESTIGACION_CIENTIFICA', 'Subsistema de Investigación Científica'),
                                                 ('ESCUELAS', 'Facultades y Escuelas'),
                                                 ('DESARROLLO_INSTITUCIONAL', 'Desarrollo Institucional'),
                                                 ('NO', 'No')), required=True)

    class Meta:
        model = Dependencia
        exclude = []
        widgets = {
            'nombre': wTextInput,
            'descripcion': wTextarea,
        }


class DepartamentoForm(forms.ModelForm):
    dependencia = forms.ModelChoiceField(
        queryset=Dependencia.objects.all(),
        label="Dependencia",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )

    class Meta:
        model = Departamento
        exclude = []
        widgets = {
            'nombre': wTextInput,
            'descripcion': wTextarea,
        }


class CargoForm(forms.ModelForm):
    tipo_cargo = forms.ChoiceField(widget=Select3Widget, choices=(
        ('ACADEMICO', 'Académico'), ('ADMINISTRATIVO', 'Administrativo'), ('OTRO', 'Otro')))

    class Meta:
        model = Cargo
        exclude = []
        widgets = {
            'nombre': wTextInput,
            'descripcion': wTextarea,
        }


class NombramientoForm(forms.ModelForm):
    class Meta:
        model = Nombramiento
        exclude = []


class AreaConocimientoForm(forms.ModelForm):
    class Meta:
        model = AreaConocimiento
        exclude = []


class AreaEspecialidadForm(forms.ModelForm):
    area_conocimiento = forms.ModelChoiceField(
        queryset=AreaConocimiento.objects.all(),
        label="Area de conocimiento",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )

    class Meta:
        model = AreaEspecialidad
        exclude = []
        widgets = {
            'nombre': wTextInput,
            'descripcion': wTextarea,
        }


class ImpactoSocialForm(forms.ModelForm):
    class Meta:
        model = ImpactoSocial
        exclude = []
        widgets = {
            'nombre': wTextInput,
            'descripcion': wTextarea,
        }


# class ProgramaFinanciamientoForm(forms.ModelForm):
#    class Meta:
#        model = ProgramaFinanciamiento
#        exclude = []


class FinanciamientoForm(forms.ModelForm):
    tipo_financiamiento = forms.ChoiceField(widget=Select3Widget, choices=getattr(settings, 'FINANCIAMIENTO_TIPO', ), )

    class Meta:
        model = Financiamiento
        exclude = []
        widgets = {
            'nombre': wTextInput,
            'descripcion': wTextarea,
            'dependencias_financiamiento': Select3MultipleWidget,
        }


class MetodologiaForm(forms.ModelForm):
    class Meta:
        model = Metodologia
        exclude = []
        widgets = {
            'nombre': wTextInput,
            'descripcion': wTextarea,
        }


class BecaForm(forms.ModelForm):
    class Meta:
        model = Beca
        exclude = []
        widgets = {
            'nombre': wTextInput,
            'descripcion': wTextarea,
        }


class ReconocimientoForm(forms.ModelForm):
    class Meta:
        model = Reconocimiento
        exclude = []
        widgets = {
            'nombre': wTextInput,
            'descripcion': wTextarea,
        }


"""
class TesisForm(forms.ModelForm):
    class Meta:
        model = DireccionTesis
        exclude = []
"""


class ProgramaLicenciaturaForm(forms.ModelForm):
    area_conocimiento = forms.ModelChoiceField(
        queryset=AreaConocimiento.objects.all(),
        label="Area de conocimiento",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )

    class Meta:
        model = ProgramaLicenciatura
        exclude = []
        widgets = {
            'nombre': wTextInput,
            'descripcion': wTextarea,
        }


class ProgramaMaestriaForm(forms.ModelForm):
    area_conocimiento = forms.ModelChoiceField(
        queryset=AreaConocimiento.objects.all(),
        label="Area de conocimiento",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )

    class Meta:
        model = ProgramaMaestria
        exclude = []
        widgets = {
            'nombre': wTextInput,
            'descripcion': wTextarea,
        }


class ProgramaDoctoradoForm(forms.ModelForm):
    area_conocimiento = forms.ModelChoiceField(
        queryset=AreaConocimiento.objects.all(),
        label="Area de conocimiento",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )

    class Meta:
        model = ProgramaDoctorado
        exclude = []
        widgets = {
            'nombre': wTextInput,
            'descripcion': wTextarea,
        }


class TipoEventoForm(forms.ModelForm):
    class Meta:
        model = TipoEvento
        exclude = []
        widgets = {
            'nombre': wTextInput,
            'descripcion': wTextarea,
        }


class EventoForm(forms.ModelForm):
    tipo = forms.ModelChoiceField(
        queryset=TipoEvento.objects.all(),
        label="Tipo de evento",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    fecha_inicio = forms.DateField(widget=wDateField, required=True, label='Fecha de inicio')
    fecha_fin = forms.DateField(widget=wDateField, required=False, label='Fecha de fin')

    class Meta:
        model = Evento
        exclude = []
        widgets = {
            'nombre': wTextInput,
            'descripcion': wTextarea,
            'dependencias': Select3MultipleWidget,
            'ubicacion': wTextInput,
        }


class DistincionForm(forms.ModelForm):
    tipo = forms.ChoiceField(widget=Select3Widget, choices=(
        ('PREMIO', 'Premio'), ('DISTINCION', 'Distinción'), ('RECONOCIMIENTO', 'Reconocimiento'),
        ('MEDALLA', 'Medalla'), ('GUGGENHEIM', 'Beca Guggenheim'), ('HONORIS_CAUSA', 'Doctorado Honoris Causa'),
        ('OTRO', 'Otro')))

    class Meta:
        model = Distincion
        exclude = []
        widgets = {
            'nombre': wTextInput,
            'descripcion': wTextarea,
        }


class ProyectoForm(forms.ModelForm):
    tipo = forms.ChoiceField(widget=Select3Widget, choices=(('INVESTIGACION', 'Investigación'), ('OTRO', 'Otro')))
    es_permanente = forms.BooleanField(required=False)
    fecha_inicio = forms.DateField(widget=wDateField, required=True, label='Fecha de inicio')
    fecha_fin = forms.DateField(widget=wDateField, required=False, label='Fecha de fin')
    status = forms.ChoiceField(widget=Select3Widget, choices=getattr(settings, 'STATUS_PROYECTO'), required=True)
    clasificacion = forms.ChoiceField(widget=Select3Widget, choices=getattr(settings, 'CLASIFICACION_PROYECTO'),
                                      required=True)
    organizacion = forms.ChoiceField(widget=Select3Widget, choices=getattr(settings, 'ORGANIZACION_PROYECTO'),
                                     required=True)
    modalidad = forms.ChoiceField(widget=Select3Widget, choices=getattr(settings, 'MODALIDAD_PROYECTO'), required=True)
    tematica_genero = forms.BooleanField(required=False)
    problema_nacional_conacyt = forms.ModelChoiceField(
        queryset=ProblemaNacionalConacyt.objects.all(),
        label="Problema Nacional Conacyt",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        ),
        required=False
    )

    class Meta:
        model = Proyecto
        exclude = []
        widgets = {
            'nombre': wTextInput,
            'descripcion': wTextarea,
            'descripcion_problema_nacional_conacyt': wTextarea,
            'usuarios': Select3MultipleWidget,
            'participantes': Select3MultipleWidget,
            'dependencias': Select3MultipleWidget,
            'financiamientos': Select3MultipleWidget,
            'metodologias': Select3MultipleWidget,
            'especialidades': Select3MultipleWidget,
            'impactos_sociales': Select3MultipleWidget,
            'tecnicos': Select3MultipleWidget,
            'alumnos_doctorado': Select3MultipleWidget,
            'alumnos_maestria': Select3MultipleWidget,
            'alumnos_licenciatura': Select3MultipleWidget,
        }


class MemoriaForm(forms.ModelForm):
    class Meta:
        model = Memoria
        exclude = []
        widgets = {
            'nombre': wTextInput,
            'descripcion': wTextarea,
        }


class EditorialForm(forms.ModelForm):
    pais = forms.ModelChoiceField(
        queryset=Pais.objects.all(),
        label="País",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )

    class Meta:
        model = Editorial
        exclude = []
        widgets = {
            'nombre': wTextInput,
            'descripcion': wTextarea,
        }


class ColeccionForm(forms.ModelForm):
    class Meta:
        model = Coleccion
        exclude = []
        widgets = {
            'nombre': wTextInput,
            'descripcion': wTextarea,
        }


class LibroForm(forms.ModelForm):
    tipo = forms.ChoiceField(widget=Select3Widget,
                             choices=(('INVESTIGACION', 'Investigación'), ('DIVULGACION', 'Divulgación')))
    ciudad = forms.ModelChoiceField(
        queryset=Ciudad.objects.all(),
        label="Ciudad",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    editorial = forms.ModelChoiceField(
        queryset=Editorial.objects.all(),
        label="Editorial",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    status = forms.ChoiceField(widget=Select3Widget, choices=getattr(settings, 'STATUS_PUBLICACION'))
    fecha = forms.DateField(widget=wDateField, required=True)
    numero_edicion = forms.CharField(widget=wNumberInput, required=True, label='Número de edición')
    numero_paginas = forms.CharField(widget=wNumberInput, required=True, label='Número de páginas')
    coleccion = forms.ModelChoiceField(
        queryset=Coleccion.objects.all(),
        label="Colección",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )

    class Meta:
        model = Libro
        exclude = []
        widgets = {
            'nombre': wTextInput,
            'descripcion': wTextarea,
            'usuarios': Select3MultipleWidget,
            'editores': Select3MultipleWidget,
            'coordinadores': Select3MultipleWidget,
            'volumen': wTextInput,
            'isbn': wTextInput,
            'url': wURLInput,
        }


class RevistaForm(forms.ModelForm):
    editorial = forms.ModelChoiceField(
        queryset=Editorial.objects.all(),
        label="Editorial",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )

    class Meta:
        model = Revista
        exclude = []
        widgets = {
            'nombre': wTextInput,
            'descripcion': wTextarea,
            'url': wURLInput,
        }


class AsignaturaForm(forms.ModelForm):
    class Meta:
        model = Asignatura
        exclude = []
        widgets = {
            'nombre': wTextInput,
            'descripcion': wTextarea,
        }


class MedioDivulgacionForm(forms.ModelForm):
    tipo = forms.ChoiceField(widget=Select3Widget,
                             choices=(('PERIODICO', 'Periódico'), ('RADIO', 'Radio'), ('TV', 'Televisión'),
                                      ('INTERNET', 'Internet'), ('OTRO', 'Otro')))
    ciudad = forms.ModelChoiceField(
        queryset=Ciudad.objects.all(),
        label="Ciudad",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )

    class Meta:
        model = MedioDivulgacion
        exclude = []
        widgets = {
            'nombre_medio': wTextInput,
            'canal': wTextInput,
            'descripcion': wTextarea,
        }


class UserForm(forms.ModelForm):
    pais_origen = forms.ModelChoiceField(
        queryset=Pais.objects.all(),
        label="País de origen",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    pais = forms.ModelChoiceField(
        queryset=Pais.objects.all(),
        label="País",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
        )
    )
    estado = forms.ModelChoiceField(
        queryset=Estado.objects.all(),
        label="Estado",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            dependent_fields={'pais': 'pais'},
        )
    )
    ciudad = forms.ModelChoiceField(
        queryset=Ciudad.objects.all(),
        label="Ciudad",
        widget=ModelSelect3Widget(
            search_fields=['nombre__icontains'],
            dependent_fields={'estado': 'estado'},
        )
    )

    class Meta:
        model = User
        exclude = ['date_joined', 'is_staff', 'is_active', 'last_login', 'is_superuser', 'groups', 'user_permissions']

        widgets = {
            'first_name': wTextInput,
            'last_name': wTextInput,
            'username': wTextInput,
            'email': wEmailInput,

            'password': wPasswordInput,
            'descripcion': wTextarea,
            'fecha_nacimiento': wDateField,
            'rfc': wTextInput,
            'direccion': wTextInput,
            'direccion_continuacion': wTextInput,
            'telefono': wTextInput,
            'celular': wTextInput,
            'sni': wNoNegativeNumberField,
            'url': wURLInput,
            'pride': wTextInput,
            'ingreso_unam': wDateField,
            'ingreso_entidad': wDateField,
        }
