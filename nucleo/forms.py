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
    estado = forms.ModelChoiceField(
        queryset=Estado.objects.all(),
        label="Estado",
        widget=ModelSelect2Widget(
            dependent_fields={'pais': 'pais'},
            search_fields=['nombre__icontains'],
            queryset=Estado.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    ciudad = forms.ModelChoiceField(
        queryset=Ciudad.objects.all(),
        label="Ciudad",
        widget=ModelSelect2Widget(
            dependent_fields={'estado': 'estado'},
            search_fields=['nombre__icontains'],
            queryset=Ciudad.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    clasificacion = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        choices=getattr(settings, 'ENTIDAD_CLASIFICACION', ), required=True)

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
            dependent_fields={'pais': 'pais'},
            search_fields=['nombre__icontains'],
            queryset=Estado.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    ciudad = forms.ModelChoiceField(
        queryset=Ciudad.objects.all(),
        label="Ciudad",
        widget=ModelSelect2Widget(
            dependent_fields={'estado': 'estado'},
            search_fields=['nombre__icontains'],
            queryset=Ciudad.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    clasificacion = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        choices=getattr(settings, 'ENTIDAD_CLASIFICACION', ), required=True)

    subsistema_unam = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
                                        choices=(('', 'Seleccionar Subsistema UNAM (sólo si se trata de una dependencia perteneciente a la UNAM)'), ('DIFUSION_CULTURAL', 'Subsistema de Difusión Cultural'),
                                                 ('ESTUDIOS_POSGRADO', 'Subsistema de Estudios de Posgrado'),
                                                 ('HUMANIDADES', 'Subsistema de Humanidades'),
                                                 ('INVESTIGACION_CIENTIFICA', 'Subsistema de Investigación Científica'),
                                                 ('ESCUELAS', 'Facultades y Escuelas'),
                                                 ('DESARROLLO_INSTITUCIONAL', 'Desarrollo Institucional'),
                                                 ('NO', 'No')), required=False)

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
    institucion = forms.ModelChoiceField(
        queryset=Institucion.objects.all(),
        label="Institución",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
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

    class Meta:
        model = Financiamiento
        exclude = []
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
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
    institucion = forms.ModelChoiceField(
        queryset=Institucion.objects.all(),
        label="Institución",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
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

class TipoCursoForm(forms.ModelForm):
    class Meta:
        model = TipoCurso
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
    tipo_publico = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)
    fecha_inicio = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True, label='Fecha de inicio')
    fecha_fin = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True, label='Fecha de fin')
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
            dependent_fields={'pais': 'pais'},
            search_fields=['nombre__icontains'],
            queryset=Estado.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    ciudad = forms.ModelChoiceField(
        queryset=Ciudad.objects.all(),
        label="Ciudad",
        widget=ModelSelect2Widget(
            dependent_fields={'estado': 'estado'},
            search_fields=['nombre__icontains'],
            queryset=Ciudad.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )

    class Meta:
        model = Evento
        exclude = []
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
            'entidades': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'ubicacion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
        }


class DistincionForm(forms.ModelForm):
    tipo = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}), 
        choices=(('', 'Seleccionar tipo de distinción'), ('PREMIO', 'Premio'), ('DISTINCION', 'Distinción'),
                 ('RECONOCIMIENTO', 'Reconocimiento'), ('MEDALLA', 'Medalla'), ('GUGGENHEIM', 'Beca Guggenheim'), 
                 ('HONORIS_CAUSA', 'Doctorado Honoris Causa'), ('OTRO', 'Otro')))
    ambito = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        choices=(('', '-------'), ('INSTITUCIONAL', 'Institucional'), ('REGIONAL', 'Regional'), ('NACIONAL', 'Nacional'), ('INTERNACIONAL', 'Internacional')))
    institucion = forms.ModelChoiceField(
        queryset=Institucion.objects.all(),
        label="Institución",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Institucion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )

    class Meta:
        model = Distincion
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
            dependent_fields={'pais': 'pais'},
            search_fields=['nombre__icontains'],
            queryset=Estado.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    ciudad = forms.ModelChoiceField(
        queryset=Ciudad.objects.all(),
        label="Ciudad",
        widget=ModelSelect2Widget(
            dependent_fields={'estado': 'estado'},
            search_fields=['nombre__icontains'],
            queryset=Ciudad.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
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


class Libro1Form(forms.ModelForm):
    tipo = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
                             choices=(('INVESTIGACION', 'Investigación'), ('DIVULGACION', 'Divulgación')))
    pais = forms.ModelChoiceField(
        queryset=Pais.objects.all(),
        label="Pais",
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
            search_fields=['nombre__icontains'],
            dependent_fields={'pais': 'pais'},
            queryset=Estado.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    ciudad = forms.ModelChoiceField(
        queryset=Ciudad.objects.all(),
        label="Ciudad",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            dependent_fields={'estado': 'estado'},
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
    status = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}), choices=getattr(settings, 'STATUS_PUBLICACION_LIBRO'))
    fecha = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True)
    numero_edicion = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}), required=True, label='Número de edición')
    numero_paginas = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}), required=True, label='Número de páginas')
    coleccion = forms.ModelChoiceField(
        required=False,
        queryset=Coleccion.objects.all(),
        label="Coleccion",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Coleccion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    arbitrado_pares = forms.BooleanField(required=False)

    class Meta:
        model = Libro
        exclude = []
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
            "autores": wSortedSelect2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
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
    issn_impreso = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False,
                                   label='ISSN impreso')
    issn_online = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False,
                                  label='ISSN online')

    class Meta:
        model = Revista
        exclude = []
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control pull-right'}),
            'nombre_abreviado_wos': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
            'url': TextInput(attrs={'class': 'form-control pull-right'}),
            'indices': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
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
                             choices=(('', '-------'), ('PERIODICO', 'Periódico'), ('RADIO', 'Radio'), ('TV', 'Televisión'), ('INTERNET', 'Internet'), ('OTRO', 'Otro')))
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
            dependent_fields={'pais': 'pais'},
            search_fields=['nombre__icontains'],
            queryset=Estado.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    ciudad = forms.ModelChoiceField(
        queryset=Ciudad.objects.all(),
        label="Ciudad",
        widget=ModelSelect2Widget(
            dependent_fields={'estado': 'estado'},
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


class PersonaForm(forms.ModelForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False)
    password = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False)
    first_name = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)
    last_name = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)

    class Meta:
        model = User
        exclude = []


class UserForm(forms.ModelForm):
    # username = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False)
    password = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False)
    first_name = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)
    last_name = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)


    class Meta:
        model = User
        exclude = []


class ProyectoInvestigacionArbitradoForm(forms.ModelForm):
    nombre = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False)
    fecha_inicio = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True, label='Fecha de inicio')
    fecha_fin = forms.DateField(widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=True, label='Fecha de fin')
    institucion = forms.ModelChoiceField(
        queryset=Institucion.objects.all(),
        label="Institución",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
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
    status = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
                               choices=getattr(settings, 'STATUS_PROYECTO'), required=True)

    class Meta:
        model = ProyectoInsvestigacionArbitrado
        exclude = []
        widgets = {
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
        }


class ConvocatoriaArbitrajeForm(forms.ModelForm):
    class Meta:
        model = ConvocatoriaArbitraje
        exclude = []
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
        }

