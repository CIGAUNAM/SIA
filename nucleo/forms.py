from .models import *
from django import forms
from django.core.exceptions import ValidationError
from django_select2.forms import Select2Widget, ModelSelect2Widget, ModelSelect2MultipleWidget, Select2MultipleWidget


from SIA.widgets import *

#





class PaisForm(forms.ModelForm):
    zona = forms.ModelChoiceField(
        queryset=ZonaPais.objects.all(),
        label="Zona",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=ZonaPais.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )

    class Meta:
        model = Pais
        exclude = []
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control pull-right'}),
            'nombre_extendido': TextInput(attrs={'class': 'form-control pull-right'}),
            'codigo': TextInput(attrs={'class': 'form-control pull-right'}),
        }


class EstadoForm(forms.ModelForm):
    pais = forms.ModelChoiceField(
        queryset=Pais.objects.all(),
        label="País",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Pais.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )

    class Meta:
        model = Estado
        exclude = []
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control pull-right'}),
        }


class CiudadForm(forms.ModelForm):
    estado = forms.ModelChoiceField(
        queryset=Estado.objects.all(),
        label="Estado",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Estado.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )

    class Meta:
        model = Ciudad
        exclude = []
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control pull-right'}),
        }


class InstitucionForm(forms.ModelForm):
    pais = forms.ModelChoiceField(
        queryset=Pais.objects.all(),
        label="País",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Pais.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )

    class Meta:
        model = Institucion
        exclude = []
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
        }


class DependenciaForm(forms.ModelForm):
    institucion = forms.ModelChoiceField(
        queryset=Institucion.objects.all(),
        label="Institución",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Institucion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    ciudad = forms.ModelChoiceField(
        queryset=Ciudad.objects.all(),
        label="Ciudad",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Ciudad.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    subsistema_unam = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
                                        choices=(('', 'Seleccionar Subsistema UNAM, si aplica '), ('DIFUSION_CULTURAL', 'Subsistema de Difusión Cultural'),
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
            'nombre': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
        }


class DepartamentoForm(forms.ModelForm):
    dependencia = forms.ModelChoiceField(
        queryset=Dependencia.objects.all(),
        label="Dependencia",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Dependencia.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )

    class Meta:
        model = Departamento
        exclude = []
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
        }


class CargoForm(forms.ModelForm):
    tipo_cargo = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}), 
        choices=(('', 'Seleccionar tipo de cargo'), ('ACADEMICO', 'Académico'), ('ADMINISTRATIVO', 'Administrativo'), 
                 ('OTRO', 'Otro')))

    class Meta:
        model = Cargo
        exclude = []
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
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
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=AreaConocimiento.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )

    class Meta:
        model = AreaEspecialidad
        exclude = []
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
        }


class ImpactoSocialForm(forms.ModelForm):
    class Meta:
        model = ImpactoSocial
        exclude = []
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
        }


# class ProgramaFinanciamientoForm(forms.ModelForm):
#    class Meta:
#        model = ProgramaFinanciamiento
#        exclude = []


class FinanciamientoForm(forms.ModelForm):
    tipo_financiamiento = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}), choices=getattr(settings, 'FINANCIAMIENTO_TIPO', ), )

    class Meta:
        model = Financiamiento
        exclude = []
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
            'dependencias_financiamiento': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class MetodologiaForm(forms.ModelForm):
    class Meta:
        model = Metodologia
        exclude = []
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
        }


class BecaForm(forms.ModelForm):
    class Meta:
        model = Beca
        exclude = []
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
        }


class ReconocimientoForm(forms.ModelForm):
    class Meta:
        model = Reconocimiento
        exclude = []
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
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
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=AreaConocimiento.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )

    class Meta:
        model = ProgramaLicenciatura
        exclude = []
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
        }


class ProgramaMaestriaForm(forms.ModelForm):
    area_conocimiento = forms.ModelChoiceField(
        queryset=AreaConocimiento.objects.all(),
        label="Area de conocimiento",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=AreaConocimiento.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )

    class Meta:
        model = ProgramaMaestria
        exclude = []
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
        }


class ProgramaDoctoradoForm(forms.ModelForm):
    area_conocimiento = forms.ModelChoiceField(
        queryset=AreaConocimiento.objects.all(),
        label="Area de conocimiento",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=AreaConocimiento.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )

    class Meta:
        model = ProgramaDoctorado
        exclude = []
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
        }


class TipoEventoForm(forms.ModelForm):
    class Meta:
        model = TipoEvento
        exclude = []
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
        }


class EventoForm(forms.ModelForm):
    tipo = forms.ModelChoiceField(
        queryset=TipoEvento.objects.all(),
        label="Tipo de evento",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=TipoEvento.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    fecha_inicio = forms.CharField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True, label='Fecha de inicio')
    fecha_fin = forms.CharField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=False, label='Fecha de fin')

    class Meta:
        model = Evento
        exclude = []
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
            'dependencias': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'ubicacion': TextInput(attrs={'class': 'form-control pull-right'}),
        }


class DistincionForm(forms.ModelForm):
    tipo = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}), 
        choices=(('', 'Seleccionar tipo de distinción'), ('PREMIO', 'Premio'), ('DISTINCION', 'Distinción'),
                 ('RECONOCIMIENTO', 'Reconocimiento'), ('MEDALLA', 'Medalla'), ('GUGGENHEIM', 'Beca Guggenheim'), 
                 ('HONORIS_CAUSA', 'Doctorado Honoris Causa'), ('OTRO', 'Otro')))

    class Meta:
        model = Distincion
        exclude = []
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
        }


class ProyectoForm(forms.ModelForm):
    tipo = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}), 
        choices=(('', 'Seleccionar tipo de proyecto'), ('INVESTIGACION', 'Investigación'), ('OTRO', 'Otro')))
    es_permanente = forms.BooleanField(required=False)
    fecha_inicio = forms.CharField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), 
        required=True, label='Fecha de inicio')
    fecha_fin = forms.CharField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), 
        required=False, label='Fecha de fin')
    status = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}), 
        choices=getattr(settings, 'STATUS_PROYECTO'), required=True)
    clasificacion = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}), 
        choices=getattr(settings, 'CLASIFICACION_PROYECTO'), required=True)
    organizacion = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}), 
        choices=getattr(settings, 'ORGANIZACION_PROYECTO'), required=True)
    modalidad = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}), 
        choices=getattr(settings, 'MODALIDAD_PROYECTO'), required=True)
    tematica_genero = forms.BooleanField(required=False)
    problema_nacional_conacyt = forms.ModelChoiceField(
        queryset=ProblemaNacionalConacyt.objects.all(),
        label="Problema Nacional Conacyt",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
        ),
        required=False
    )

    class Meta:
        model = Proyecto
        exclude = []
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
            'descripcion_problema_nacional_conacyt': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
            'usuarios': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'participantes': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'dependencias': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'financiamientos': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'metodologias': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'especialidades': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'impactos_sociales': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'tecnicos': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'alumnos_doctorado': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'alumnos_maestria': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'alumnos_licenciatura': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class MemoriaForm(forms.ModelForm):
    class Meta:
        model = Memoria
        exclude = []
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
        }


class EditorialForm(forms.ModelForm):
    pais = forms.ModelChoiceField(
        queryset=Pais.objects.all(),
        label="País",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Pais.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    estado = forms.ModelChoiceField(
        queryset=Estado.objects.all(),
        label="Estado",
        widget=ModelSelect2Widget(
            dependent_fields={'pais_origen': 'pais'},
            search_fields=['nombre__icontains'],
        )
    )
    ciudad = forms.ModelChoiceField(
        queryset=Ciudad.objects.all(),
        label="Ciudad",
        widget=ModelSelect2Widget(
            dependent_fields={'estado': 'estado'},
            search_fields=['nombre__icontains'],
        )
    )

    class Meta:
        model = Editorial
        exclude = []
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
        }


class ColeccionForm(forms.ModelForm):
    class Meta:
        model = Coleccion
        exclude = []
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
        }


class LibroForm(forms.ModelForm):
    tipo = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
                             choices=(('INVESTIGACION', 'Investigación'), ('DIVULGACION', 'Divulgación')))
    ciudad = forms.ModelChoiceField(
        queryset=Ciudad.objects.all(),
        label="Ciudad",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Ciudad.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    editorial = forms.ModelChoiceField(
        queryset=Editorial.objects.all(),
        label="Editorial",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Editorial.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    status = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}), choices=getattr(settings, 'STATUS_PUBLICACION'))
    fecha = forms.CharField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    numero_edicion = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}), required=True, label='Número de edición')
    numero_paginas = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}), required=True, label='Número de páginas')
    coleccion = forms.ModelChoiceField(
        queryset=Coleccion.objects.all(),
        label="Colección",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Coleccion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    es_libro_completo = forms.BooleanField(required=False)

    class Meta:
        model = Libro
        exclude = []
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
            'usuarios': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'editores': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'coordinadores': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'volumen': TextInput(attrs={'class': 'form-control pull-right'}),
            'isbn': TextInput(attrs={'class': 'form-control pull-right'}),
            'url': TextInput(attrs={'class': 'form-control pull-right'}),
        }


class RevistaForm(forms.ModelForm):
    pais = forms.ModelChoiceField(
        queryset=Pais.objects.all(),
        label="Editorial",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Pais.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    factor_impacto = forms.CharField(widget=NumberInput(attrs={'min': 0, 'class': 'form-control pull-right'}),
                                     label='Factor de impácto')

    class Meta:
        model = Revista
        exclude = []
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control pull-right'}),
            'nombre_abreviado_wos': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
            'url': TextInput(attrs={'class': 'form-control pull-right'}),
        }


class AsignaturaForm(forms.ModelForm):
    class Meta:
        model = Asignatura
        exclude = []
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
        }


class MedioDivulgacionForm(forms.ModelForm):
    tipo = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
                             choices=(('PERIODICO', 'Periódico'), ('RADIO', 'Radio'), ('TV', 'Televisión'), ('INTERNET', 'Internet'), ('OTRO', 'Otro')))
    ciudad = forms.ModelChoiceField(
        queryset=Ciudad.objects.all(),
        label="Ciudad",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Ciudad.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )

    class Meta:
        model = MedioDivulgacion
        exclude = []
        widgets = {
            'nombre_medio': TextInput(attrs={'class': 'form-control pull-right'}),
            'canal': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
        }


class UserForm(forms.ModelForm):
    """
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}), required=False, label='Semblanza')
    tipo = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}), choices=(
        ('INVESTIGADOR', 'Investigador'), ('ADMINISTRATIVO', 'Administrativo'), ('TECNICO', 'Técnico'),
        ('OTRO', 'Otro')),
                             required=True)
    fecha_nacimiento = forms.CharField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True, label='Fecha de nacimiento')
    pais_origen = forms.ModelChoiceField(
        queryset=Pais.objects.all(),
        label="País de origen",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
        )
    )
    estado = forms.ModelChoiceField(
        queryset=Estado.objects.all(),
        label="Estado",
        widget=ModelSelect2Widget(
            dependent_fields={'pais_origen': 'pais'},
            search_fields=['nombre__icontains'],
        )
    )
    ciudad = forms.ModelChoiceField(
        queryset=Ciudad.objects.all(),
        label="Ciudad",
        widget=ModelSelect2Widget(
            dependent_fields={'estado': 'estado'},
            search_fields=['nombre__icontains'],
        )
    )
    """

    class Meta:
        model = User
        exclude = []
        """
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control pull-right'}),
            'last_name': TextInput(attrs={'class': 'form-control pull-right'}),
            'username': TextInput(attrs={'class': 'form-control pull-right'}),
            'email': wEmailField,
            'rfc': TextInput(attrs={'class': 'form-control pull-right'}),
            'telefono': TextInput(attrs={'class': 'form-control pull-right'}),
            'celular': TextInput(attrs={'class': 'form-control pull-right'}),
        }
        """