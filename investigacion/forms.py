from SIA.widgets import *

from .models import *
from nucleo.models import Libro as LibroInvestigacion
from nucleo.models import ProblemaNacionalConacyt

from django import forms

from django.conf import settings
from django_select2.forms import Select2Widget, ModelSelect2Widget, ModelSelect2MultipleWidget, Select2MultipleWidget


#

class ArticuloCientificoForm(forms.ModelForm):
    titulo = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True,
                             label='Título de artículo')

    status = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
                               choices=getattr(settings, 'STATUS_PUBLICACION_ARTICULO', ), required=True)
    solo_electronico = forms.BooleanField(required=False)
    url = forms.URLField(widget=URLInput(attrs={'class': 'form-control pull-right'}), required=False)
    fecha = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=False, label='Fecha')
    fecha_enviado = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=False, label='Fecha de envío')
    fecha_aceptado = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=False, label='Fecha de aceptación')
    fecha_enprensa = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=False, label='Fecha de envío a prensa')
    fecha_publicado = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=False, label='Fecha de publicación')
    revista = forms.ModelChoiceField(
        queryset=Revista.objects.all(),
        label="Revista",
        widget=ModelSelect2Widget(
            search_fields=['revista_nombre__icontains'],
            queryset=Revista.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    volumen = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False)
    numero = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False,
                             label='Número')
    pagina_inicio = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}),
                                    required=True, label='Número de página donde inicia')
    pagina_fin = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}),
                                 required=True, label='Número de página final')
    id_doi = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False,
                             label='ID DOI')

    factor_impacto = forms.DecimalField(max_digits=5, decimal_places=3,
                                        required=False,
                                        widget=TextInput(
                                            attrs={'min': 0, 'class': 'form-control pull-right', 'step': '0.001'}),
                                        label='Factor de impácto')
    proyecto = forms.ModelChoiceField(
        required=False,
        queryset=ProyectoInvestigacion.objects.all(),
        label="Proyecto de investigación",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=ProyectoInvestigacion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    autores_todos = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3',
                                                           'placeholder': 'Autores tal cual se reportan en el artículo, en el orden y forma.'}),
                                    required=False, label='Autores como se reportan en el artículo')

    class Meta:
        model = ArticuloCientifico
        exclude = []
        widgets = {
            'autores': wSortedSelect2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'alumnos': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'agradecimientos': Select2MultipleWidget(
                attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class CapituloLibroInvestigacionForm(forms.ModelForm):
    titulo = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True,
                             label='Título del capítulo')
    libro = forms.ModelChoiceField(
        queryset=LibroInvestigacion.objects.filter(tipo='INVESTIGACION'),
        label="Libro",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=LibroInvestigacion.objects.filter(tipo='INVESTIGACION'),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    pagina_inicio = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}),
                                    required=True, label='Número de página donde inicia')
    pagina_fin = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}),
                                 required=True, label='Número de página final')
    autores_todos = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3',
                                                           'placeholder': 'Autores tal cual se reportan en el capítulo del libro, en el orden y forma.'}),
                                    required=False, label='Autores como se reportan en el capítulo del libro')

    class Meta:
        model = CapituloLibroInvestigacion
        exclude = []
        widgets = {
            "autores": wSortedSelect2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class MapaArbitradoForm(forms.ModelForm):
    titulo = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True,
                             label='Título del mapa')
    status = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
                               choices=getattr(settings, 'STATUS_PUBLICACION', ), required=True)
    pais = forms.ModelChoiceField(
        required=True,
        queryset=Pais.objects.all(),
        label="Pais",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Pais.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )

    fecha = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=True, label='fecha')
    fecha_enviado = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=False, label='Fecha de envío')
    fecha_aceptado = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=False, label='Fecha de aceptación')
    fecha_enprensa = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=False, label='Fecha de envío a prensa')
    fecha_publicado = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=False, label='Fecha de publicación')
    numero_paginas = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}),
                                     required=True, label='Número de páginas')
    ciudad_text = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False,
                                  label='Ciudad')
    publicacion = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False,
                                  label='Libro o revista donde se publica')

    proyecto = forms.ModelChoiceField(
        required=False,
        queryset=ProyectoInvestigacion.objects.all(),
        label="Proyecto de investigación",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=ProyectoInvestigacion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    autores_todos = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3',
                                                           'placeholder': 'Autores tal cual se reportan en el capítulo del libro, en el orden y forma.'}),
                                    required=False, label='Autores como se reportan en el capítulo del libro')

    class Meta:
        model = MapaArbitrado
        exclude = []
        widgets = {
            "autores": wSortedSelect2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            "agradecimientos": wSortedSelect2MultipleWidget(
                attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class PublicacionTecnicaForm(forms.ModelForm):
    titulo = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
                                  required=False)
    tipo = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
                             choices=(('', '-------'), ('DESARROLLO_TECNOLOGICO', 'Desarrollo tecnológico terminado'),
                                      ('PROGRAMA_COMPUTO', 'Programa de cómputo especializado documentado'),
                                      ('BASE_DATOS',
                                       'Bases de datos geográficos, arbitradas por expertos, para apliciones Web'),
                                      ('NORMA_PATENTE', 'Normas y patentes'),
                                      ('INFORME_TECNICO',
                                       'Informes técnicos finales dirigidos a tomadores de decisiones'),
                                      ('PLAN_MANEJO',
                                       'Planes de manejo, ordenamiento, y gestión territorial, reconocidos oficialmente'),
                                      ('CARTA_REVISTA', 'Cartas en revistas de prestigio internacional'),
                                      ('TRADUCCION', 'Traducción de libros y revisiones técnicas')), required=True)
    status = forms.ChoiceField(widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
                               choices=getattr(settings, 'STATUS_PUBLICACION', ), required=True)
    fecha_enviado = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=False, label='Fecha de envío')
    fecha_aceptado = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=False, label='Fecha de aceptación')
    fecha_enprensa = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=False, label='Fecha de envío a prensa')
    fecha_publicado = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=False, label='Fecha de publicación')
    autores_todos = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3',
                                                           'placeholder': 'Autores tal cual se reportan en la publicación, en el orden y forma.'}),
                                    required=False, label='Autores como se reportan en la publicación')
    institucion = forms.ModelChoiceField(
        required=True,
        queryset=InstitucionSimple.objects.all(),
        label="Institución",
        widget=ModelSelect2Widget(
            search_fields=['institucion_nombre__icontains'],
            queryset=InstitucionSimple.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    url = forms.URLField(widget=URLInput(attrs={'class': 'form-control pull-right'}), required=False)
    proyecto = forms.ModelChoiceField(
        required=True,
        queryset=ProyectoInvestigacion.objects.all(),
        label="Proyecto de investigación",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=ProyectoInvestigacion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    es_publico = forms.BooleanField(required=False)
    cita = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3',
                                                  'placeholder': 'Cita completa del producto'}), required=False)

    class Meta:
        model = PublicacionTecnica
        exclude = []
        widgets = {
            'autores': wSortedSelect2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class ProyectoInvestigacionForm(forms.ModelForm):
    nombre = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True,
                             label='Nombre del proyecto')
    es_permanente = forms.BooleanField(required=False)
    fecha_inicio = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=True, label='Fecha de inicio')
    fecha_fin = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=False, label='Fecha de fin')
    institucion = forms.ModelChoiceField(
        queryset=InstitucionSimple.objects.all(),
        label="Institución",
        widget=ModelSelect2Widget(
            search_fields=['institucion_nombre__icontains'],
            queryset=InstitucionSimple.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
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
    tipo_financiamiento = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        choices=(('', '-------'), ('CONACYT', 'CONACYT'), ('PAPIIT', 'DGAPA-PAPIIT'), ('PAPIME', 'DGAPA-PAPIME'),
                 ('EXTRAORDINARIOS', 'Ingresos extraordinarios'), ('SIN_RECURSOS', 'Sin recursos en el CIGA (en colaboración con otras dependencias)')),
        required=True)
    financiamiento_extraordinario = forms.ModelChoiceField(
        queryset=Dependencia.objects.all(),
        required=False,
        label="Dependencia",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Dependencia.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    financiamiento_sin_recurso_ciga = forms.ModelChoiceField(
        queryset=Dependencia.objects.all(),
        required=False,
        label="Dependencia",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Dependencia.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    tematica_genero = forms.BooleanField(required=False)

    metodologias_text = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False,
                                        label='Metodologías')
    impacto_social_text = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False,
                                          label='Impacto social')
    num_alumnos_doctorado = forms.IntegerField(widget=NumberInput(attrs={'min': 0, 'class': 'form-control pull-right'}),
                                               required=True, label='Número de alumnos de doctorado', initial='0')
    num_alumnos_maestria = forms.IntegerField(widget=NumberInput(attrs={'min': 0, 'class': 'form-control pull-right'}),
                                              required=True, label='Número de alumnos de maestría', initial='0')
    num_alumnos_licenciatura = forms.IntegerField(
        widget=NumberInput(attrs={'min': 0, 'class': 'form-control pull-right'}), required=True,
        label='Número de alumnos de doctorado', initial='0')
    participantes_externos_text = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3',
                                                           'placeholder': 'Participantes externos (No adscritos al CIGA), separar cada participante por coma.'}),
                                    required=False, label='Autores como se reportan en la publicación')

    class Meta:
        model = ProyectoInvestigacion
        exclude = []
        widgets = {
            'descripcion': Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
            "responsables": wSortedSelect2MultipleWidget(
                attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'participantes': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'objetivos2030': Select2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'financiamiento_conacyt_clave': TextInput(attrs={'class': 'form-control pull-right'}),
            'financiamiento_conacyt_convocatoria': TextInput(attrs={'class': 'form-control pull-right'}),
            'financiamiento_papiit': TextInput(attrs={'class': 'form-control pull-right'}),
            'financiamiento_papime': TextInput(attrs={'class': 'form-control pull-right'}),
        }


class LibroInvestigacionForm(forms.ModelForm):  # Posiblemente MANTENER, creo que estaba duplicado (borrar el otro)
    nombre = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=True)
    descripcion = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': ''}),
                                  required=False)
    pais = forms.ModelChoiceField(
        queryset=Pais.objects.all(),
        label="Pais",
        widget=ModelSelect2Widget(
            search_fields=['nombre__icontains'],
            queryset=Pais.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )

    ciudad_text = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}))
    editorial_text = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}))
    coleccion_text = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False)

    status = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        choices=getattr(settings, 'STATUS_PUBLICACION', ), required=True)
    tipo_participacion = forms.ChoiceField(
        widget=Select2Widget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        choices=(('', '-------'), ('AUTORIA', 'Autoría'), ('EDICION', 'Edición'), ('COORDINACION', 'Coordinación'),
                 ('COMPILACION', 'Compilación')), required=True)
    fecha = forms.DateField(widget=wDateInput(
        attrs={'style': 'width: 100%', 'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=False)
    fecha_enviado = forms.DateField(widget=wDateInput(
        attrs={'style': 'width: 100%', 'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=False)
    fecha_aceptado = forms.DateField(widget=wDateInput(
        attrs={'style': 'width: 100%', 'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=False)
    fecha_enprensa = forms.DateField(widget=wDateInput(
        attrs={'style': 'width: 100%', 'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=False)
    fecha_publicado = forms.DateField(widget=wDateInput(
        attrs={'style': 'width: 100%', 'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=False)
    numero_edicion = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}))
    numero_paginas = forms.CharField(widget=NumberInput(attrs={'min': 1, 'class': 'form-control pull-right'}))
    volumen = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False)
    isbn = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False)
    url = forms.URLField(widget=URLInput(attrs={'class': 'form-control pull-right'}), required=False)
    autores_todos = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': '3',
                                                           'placeholder': 'Autores tal cual se reportan en el artículo, en el orden y forma.'}),
                                    required=False, label='Autores como se reportan en el artículo')

    class Meta:
        model = LibroInvestigacion
        exclude = ['tipo', ]
        widgets = {
            "autores": wSortedSelect2MultipleWidget(attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            "editores": wSortedSelect2MultipleWidget(
                attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            "coordinadores": wSortedSelect2MultipleWidget(
                attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'compiladores': wSortedSelect2MultipleWidget(
                attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
            'agradecimientos': Select2MultipleWidget(
                attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}),
        }


class ApoyoTecnicoInvestigacionForm(forms.ModelForm):
    actividad = forms.ModelChoiceField(
        queryset=ActividadApoyoTecnicoInvestigacion.objects.all(),
        label="Actividad de apoyo técnico a la investigación",
        widget=ModelSelect2Widget(
            search_fields=['actividadapoyotecnicoinvestigacion_nombre__icontains'],
            queryset=ActividadApoyoTecnicoInvestigacion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    actividad_otra = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False,
                                     label='Otra actividad', help_text='Otra actividad de apoyo a la investigación')
    fecha_inicio = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=True)
    fecha_fin = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=False)

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
        model = ApoyoTecnicoInvestigacion
        exclude = ['usuario', ]


class ApoyoTecnicoServicioForm(forms.ModelForm):
    actividad = forms.ModelChoiceField(
        queryset=ActividadApoyoTecnicoInvestigacion.objects.all(),
        label="Actividad de apoyo técnico a la investigación",
        widget=ModelSelect2Widget(
            search_fields=['actividadapoyotecnicoinvestigacion_nombre__icontains'],
            queryset=ActividadApoyoTecnicoInvestigacion.objects.all(),
            attrs={'style': 'width: 100%', 'class': 'form-control pull-right'}
        )
    )
    actividad_otra = forms.CharField(widget=TextInput(attrs={'class': 'form-control pull-right'}), required=False,
                                     label='Otra actividad', help_text='Otra actividad de apoyo a la investigación')
    fecha_inicio = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=True)
    fecha_fin = forms.DateField(
        widget=wDateInput(attrs={'data-provider': 'datepicker', 'class': 'datepicker form-control pull-right'}),
        required=False)

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
        model = ApoyoTecnicoServicio
        exclude = ['usuario', ]
