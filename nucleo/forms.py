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
            'titulo_proyecto': TextInput(attrs={'class': 'form-control pull-right'}),
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
            'titulo_proyecto': TextInput(attrs={'class': 'form-control pull-right'}),
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
        exclude = ['usuario_creador', 'validado', 'fecha_creado', 'fecha_actualizado']
        widgets = {
            'titulo_proyecto': TextInput(attrs={'class': 'form-control pull-right'}),
        }


class InstitucionSimpleForm(forms.ModelForm):
    institucion_nombre = forms.CharField(widget=TextInput(
        attrs={'class': 'form-control pull-right', 'placeholder': 'Nombre de la institución y sus siglas entre parentesis (si oficialmente las tiene)'}),
        required=True, label='Nombre de la institución')
    institucion_pais = forms.ModelChoiceField(
        queryset=Pais.objects.all(),
        label="País",
        widget=ModelSelect2Widget(
            search_fields=['pais_nombre__icontains'],
            queryset=Pais.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right', 'data-placeholder': 'Seleccione el país donde se encuentra la institución'}
        )
    )
    institucion_ciudad = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True, label='Nombre de la institución')
    institucion_clasificacion = forms.ChoiceField(
        widget=Select2Widget(attrs={'class': 'form-control pull-right'}),
        choices=(('', '-------'), ('ACADEMICA', 'Académica'), ('FEDERAL', 'Gubernamental federal'),
                 ('ESTATAL', 'Gubernamental estatal'), ('MUNICIPAL', 'Gubernamental municipal'),
                 ('PRIVADA', 'Sector privado'), ('NO_LUCRATIVA', 'Sector privado no lucrativo')), required=True)
    institucion_perteneceunam = forms.BooleanField(required=False)
    institucion_subsistemaunam = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        choices=(
            ('', '-------'),
            ('DIFUSION_CULTURAL', 'Subsistema de Difusión Cultural'),
            ('ESTUDIOS_POSGRADO', 'Subsistema de Estudios de Posgrado'),
            ('HUMANIDADES', 'Subsistema de Humanidades'),
            ('INVESTIGACION_CIENTIFICA', 'Subsistema de Investigación Científica'),
            ('ESCUELAS', 'Facultades y Escuelas'),
            ('DESARROLLO_INSTITUCIONAL', 'Desarrollo Institucional')), required=False)

    class Meta:
        model = Institucion
        exclude = ['institucion_regverificado', 'institucion_regfechacreado', 'institucion_regfechaactualizado', 'institucion_regusuario']
        widgets = {
        }


class InstitucionForm(forms.ModelForm):
    pais_institucion = forms.ModelChoiceField(
        queryset=Pais.objects.all(),
        label="País",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Pais.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    clasificacion_institucion = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        choices=getattr(settings, 'ENTIDAD_CLASIFICACION', ), required=True)

    class Meta:
        model = Institucion
        exclude = ['usuario_creador', 'validado', 'fecha_creado', 'fecha_actualizado']
        widgets = {
            'nombre_institucion': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion_institucion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
        }


class DependenciaForm(forms.ModelForm):
    institucion_dependencia = forms.ModelChoiceField(
        queryset=Institucion.objects.all(),
        label="Institución",
        widget=ModelSelect2Widget(
            search_fields=['nombre_institucion__icontains'],
            queryset=Institucion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )

    subsistema_unam_dependencia = forms.TypedChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right', 'data-placeholder': 'Seleccione el subsistema de la UNAM al que pertenece, si no pertenece a ninguno de los listados no seleccionar ninguno'}),
                                        choices=(('', 'Seleccionar Subsistema UNAM'),
                                                 ('DIFUSION_CULTURAL', 'Subsistema de Difusión Cultural'),
                                                 ('ESTUDIOS_POSGRADO', 'Subsistema de Estudios de Posgrado'),
                                                 ('HUMANIDADES', 'Subsistema de Humanidades'),
                                                 ('INVESTIGACION_CIENTIFICA', 'Subsistema de Investigación Científica'),
                                                 ('ESCUELAS', 'Facultades y Escuelas'),
                                                 ('DESARROLLO_INSTITUCIONAL', 'Desarrollo Institucional')), required=False)

    class Meta:
        model = Dependencia
        exclude = ['usuario_creador', 'validado', 'fecha_creado', 'fecha_actualizado']
        widgets = {
            'nombre_dependencia': TextInput(attrs={'class': 'form-control pull-right', 'placeholder': 'Nombre de la dependencia y sus siglas entre parentesis (si oficialmente las tiene)'}),
            'ciudad_text_dependencia': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion_dependencia': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
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
            'titulo_proyecto': TextInput(attrs={'class': 'form-control pull-right'}),
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
            'titulo_proyecto': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
        }


class NombramientoForm(forms.ModelForm):
    class Meta:
        model = Nombramiento
        exclude = []


class AreaEspecialidadForm(forms.ModelForm):
    area_conocimiento = forms.ModelChoiceField(
        queryset=AreaConocimiento.objects.all(),
        label="Area de conocimiento",
        widget=ModelSelect2Widget(
            search_fields=['areaconocimiento_nombre__icontains'],
            queryset=AreaConocimiento.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )

    class Meta:
        model = AreaEspecialidad
        exclude = []
        widgets = {
            'titulo_proyecto': TextInput(attrs={'class': 'form-control pull-right'}),
        }


class ImpactoSocialForm(forms.ModelForm):
    class Meta:
        model = ImpactoSocial
        exclude = []
        widgets = {
            'titulo_proyecto': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
        }


class FinanciamientoForm(forms.ModelForm):
    tipo_financiamiento = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}), choices=getattr(settings, 'FINANCIAMIENTO_TIPO', ), )
    institucion = forms.ModelChoiceField(
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

    class Meta:
        model = Financiamiento
        exclude = []
        widgets = {
            'titulo_proyecto': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
        }


class MetodologiaForm(forms.ModelForm):
    class Meta:
        model = Metodologia
        exclude = []
        widgets = {
            'titulo_proyecto': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
        }


class BecaForm(forms.ModelForm):
    institucion = forms.ModelChoiceField(
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
    class Meta:
        model = Beca
        exclude = []
        widgets = {
            'titulo_proyecto': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
        }


class ReconocimientoForm(forms.ModelForm):
    class Meta:
        model = Reconocimiento
        exclude = []
        widgets = {
            'titulo_proyecto': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
        }




class ProgramaLicenciaturaForm(forms.ModelForm):
    programalicenciatura_areaconocimiento = forms.ModelChoiceField(
        queryset=AreaConocimiento.objects.all(),
        label="Area de conocimiento",
        widget=ModelSelect2Widget(
            search_fields=['areaconocimiento_nombre__icontains'],
            queryset=AreaConocimiento.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )

    class Meta:
        model = ProgramaLicenciatura
        exclude = ['programalicenciatura_regverificado', 'programalicenciatura_regfechacreado', 'programalicenciatura_regfechaactualizado', 'programalicenciatura_regusuario']
        widgets = {
            'programalicenciatura_nombre': TextInput(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class ProgramaMaestriaForm(forms.ModelForm):
    programamaestria_areaconocimiento = forms.ModelChoiceField(
        queryset=AreaConocimiento.objects.all(),
        label="Area de conocimiento",
        widget=ModelSelect2Widget(
            search_fields=['areaconocimiento_nombre__icontains'],
            queryset=AreaConocimiento.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )

    class Meta:
        model = ProgramaMaestria
        exclude = ['programamaestria_regverificado', 'programamaestria_regfechacreado', 'programamaestria_regfechaactualizado', 'programamaestria_regusuario']
        widgets = {
            'programamaestria_nombre': TextInput(attrs={'class': 'form-control pull-right'}),
        }


class ProgramaDoctoradoForm(forms.ModelForm):
    programadoctorado_areaconocimiento = forms.ModelChoiceField(
        queryset=AreaConocimiento.objects.all(),
        label="Area de conocimiento",
        widget=ModelSelect2Widget(
            search_fields=['areaconocimiento_nombre__icontains'],
            queryset=AreaConocimiento.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )

    class Meta:
        model = ProgramaDoctorado
        exclude = ['programadoctorado_regverificado', 'programadoctorado_regfechacreado', 'programadoctorado_regfechaactualizado', 'programadoctorado_regusuario']
        widgets = {
            'programadoctorado_nombre': TextInput(attrs={'class': 'form-control pull-right'}),
        }


class TipoEventoForm(forms.ModelForm):
    class Meta:
        model = TipoEvento
        exclude = []
        widgets = {
            'titulo_proyecto': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
        }

class TipoCursoForm(forms.ModelForm):
    class Meta:
        model = TipoCurso
        exclude = []
        widgets = {
            'titulo_proyecto': TextInput(attrs={'class': 'form-control pull-right'}),
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
            'titulo_proyecto': TextInput(attrs={'class': 'form-control pull-right'}),
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
            search_fields=['nombre_institucion__icontains'],
            queryset=Institucion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )

    class Meta:
        model = Distincion
        exclude = []
        widgets = {
            'titulo_proyecto': TextInput(attrs={'class': 'form-control pull-right'}),
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
            'titulo_proyecto': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
        }


class ColeccionForm(forms.ModelForm):
    class Meta:
        model = Coleccion
        exclude = []
        widgets = {
            'titulo_proyecto': TextInput(attrs={'class': 'form-control pull-right'}),
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
    status = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}), choices=getattr(settings, 'STATUS_PUBLICACION'))
    fecha = forms.DateField(widget=wDateInput(attrs={'style': 'width: 100%', 'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=False)
    fecha_enviado = forms.DateField(widget=wDateInput(attrs={'style': 'width: 100%', 'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=False)
    fecha_aceptado = forms.DateField(widget=wDateInput(attrs={'style': 'width: 100%', 'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=False)
    fecha_enprensa = forms.DateField(widget=wDateInput(attrs={'style': 'width: 100%', 'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=False)
    fecha_publicado = forms.DateField(widget=wDateInput(attrs={'style': 'width: 100%', 'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}), required=False)
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
            'titulo_proyecto': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
            "autores": wSortedSelect2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'compiladores': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'volumen': TextInput(attrs={'class': 'form-control pull-right'}),
            'isbn': TextInput(attrs={'class': 'form-control pull-right'}),
            'url': TextInput(attrs={'class': 'form-control pull-right'}),
        }


class RevistaForm(forms.ModelForm):
    revista_pais = forms.ModelChoiceField(
        queryset=Pais.objects.all(),
        label="País",
        widget=ModelSelect2Widget(
            search_fields=['pais_nombre__icontains'],
            queryset=Pais.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    revista_issn_impreso = forms.CharField(widget=TextInput(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}), required=False,
                                   label='ISSN impreso')
    revista_issn_online = forms.CharField(widget=TextInput(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}), required=False,
                                  label='ISSN online')

    class Meta:
        model = Revista
        exclude = ['revista_regverificado', 'revista_regfechacreado', 'revista_regfechaactualizado', 'revista_regusuario']

        widgets = {
            'revista_nombre': TextInput(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'revista_nombreabreviadowos': TextInput(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'revista_descripcion': Textarea(attrs={'style': 'width: 100%', 'class': 'form-control', 'rows': '3', 'placeholder': ''}),
            'revista_indices': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class AsignaturaForm(forms.ModelForm):
    class Meta:
        model = Asignatura
        exclude = []
        widgets = {
            'titulo_proyecto': TextInput(attrs={'class': 'form-control pull-right'}),
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
            'titulo_proyecto': TextInput(attrs={'class': 'form-control pull-right'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
        }

