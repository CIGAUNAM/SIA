"""Formularios de cuenta: cada cuenta figura como una persona (nombre para mostrar y ORCID)."""

from django import forms
from django.utils.html import format_html
from unfold.forms import UserChangeForm as BaseUserChangeForm
from unfold.forms import UserCreationForm as BaseUserCreationForm
from unfold.widgets import UnfoldBooleanWidget, UnfoldAdminTextInputWidget

from .externos import ErrorServicio, nombre_orcid
from .models import Persona, User
from .nombres import formato_cita, normalizar_orcid
from .similitud import personas_parecidas


class CamposPersona(forms.Form):
    nombre_persona = forms.CharField(
        label='Nombre para mostrar', max_length=300, required=False, widget=UnfoldAdminTextInputWidget,
        help_text=f'{Persona._meta.get_field("nombre").help_text} Si lo dejas vacío, se toma de ORCID.')
    orcid = forms.CharField(label='ORCID', max_length=40, required=False, widget=UnfoldAdminTextInputWidget,
                            help_text='Formato 0000-0002-1825-0097. Una vez asignado, solo un administrador lo cambia.')

    #: Lo asigna el admin: los académicos no cambian un ORCID ya capturado ni su persona.
    administrador = False

    def clean_orcid(self):
        valor = self.cleaned_data['orcid'].strip()
        if valor and not normalizar_orcid(valor):
            raise forms.ValidationError('El ORCID debe tener el formato 0000-0000-0000-000X.')
        return normalizar_orcid(valor)

    def _nombre_desde_orcid(self, orcid):
        try:
            nombre = nombre_orcid(orcid)
        except ErrorServicio as error:
            self.add_error('nombre_persona', f'No se pudo consultar ORCID ({error}). Escribe el nombre.')
            return ''
        if not nombre:
            self.add_error('nombre_persona', 'Ese ORCID no tiene un nombre público. Escribe el nombre.')
        return nombre

    def _orcid_de_otra_persona(self, orcid, persona=None):
        otra = Persona.objects.filter(orcid=orcid).exclude(pk=getattr(persona, 'pk', None)).first()
        if otra is not None:
            self.add_error('orcid', f'Ese ORCID ya es de «{otra}».')
        return otra


class UserCreationForm(CamposPersona, BaseUserCreationForm):
    """Alta de cuenta: se elige una persona existente, se crea desde ORCID o con el nombre escrito."""
    confirmar_persona_nueva = forms.BooleanField(
        required=False, widget=forms.HiddenInput,
        label='Crear persona nueva', help_text='Ninguna de las personas parecidas es esta persona.')

    class Meta(BaseUserCreationForm.Meta):
        model = User
        fields = ('email', 'first_name', 'last_name', 'persona')
        field_classes = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['persona'].required = False
        self.fields['persona'].label = 'Persona existente'
        self.fields['persona'].help_text = ('Si ya figura en el catálogo (p. ej. como coautor), elígela aquí; '
                                            'si no, se crea con el ORCID o el nombre para mostrar.')

    def clean(self):
        datos = super().clean()
        persona, orcid, nombre = datos.get('persona'), datos.get('orcid'), datos.get('nombre_persona', '').strip()
        if persona is not None:
            if orcid and persona.orcid and persona.orcid != orcid:
                self.add_error('orcid', f'«{persona}» ya tiene otro ORCID ({persona.orcid}).')
            elif orcid:
                self._orcid_de_otra_persona(orcid, persona)
            self.persona_nueva = None
            return datos

        existente = Persona.objects.filter(orcid=orcid).first() if orcid else None
        if existente is not None:
            if existente.tiene_cuenta:
                self.add_error('orcid', f'Ese ORCID es de «{existente}», que ya tiene cuenta.')
            else:
                datos['persona'] = existente
            self.persona_nueva = None
            return datos

        if not nombre and orcid:
            nombre = self._nombre_desde_orcid(orcid)
        nombre = nombre or formato_cita(datos.get('first_name'), datos.get('last_name'))
        if not nombre:
            self.add_error('nombre_persona', 'Escribe el nombre para mostrar, un ORCID o el nombre y apellidos.')
            return datos
        similares = [p for p in personas_parecidas(Persona.objects.all(), nombre) if not p.tiene_cuenta]
        if similares and not datos.get('confirmar_persona_nueva'):
            self.fields['confirmar_persona_nueva'].widget = UnfoldBooleanWidget()
            self.add_error('persona', format_html(
                'Ya hay personas parecidas en el catálogo: {}. Si es alguna, elígela aquí; si no, marca abajo '
                '«Crear persona nueva».', '; '.join(f'«{p}» (núm. {p.pk})' for p in similares)))
        self.persona_nueva = Persona(nombre=nombre, orcid=orcid, verificado=True)
        return datos

    def save(self, commit=True):
        user = super().save(commit=False)
        persona = self.cleaned_data.get('persona')
        if persona is None:
            persona = self.persona_nueva
            persona.save()
        elif self.cleaned_data.get('orcid') and not persona.orcid:
            persona.orcid = self.cleaned_data['orcid']
            persona.save(update_fields=['orcid'])
        if self.cleaned_data.get('nombre_persona') and persona.nombre != self.cleaned_data['nombre_persona']:
            persona.nombre = self.cleaned_data['nombre_persona'].strip()
            persona.save(update_fields=['nombre'])
        user.persona = persona
        if commit:
            user.save()
            self.save_m2m()
        return user


class UserChangeForm(CamposPersona, BaseUserChangeForm):
    """Perfil: el nombre para mostrar y el ORCID se editan aquí y se guardan en la persona de la cuenta."""

    class Meta(BaseUserChangeForm.Meta):
        model = User
        field_classes = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        persona = self.instance.persona
        self.fields['nombre_persona'].initial = persona.nombre
        self.fields['orcid'].initial = persona.orcid
        if persona.orcid and not self.administrador:
            self.fields['orcid'].disabled = True
        if 'persona' in self.fields:
            self.fields['persona'].help_text = ('Cambiarla reasigna al académico la producción de otra persona. '
                                                'Al cambiarla no se guardan el nombre ni el ORCID de abajo.')

    def _persona_cambia(self):
        return 'persona' in self.changed_data

    def clean(self):
        datos = super().clean()
        if self._persona_cambia():
            return datos
        persona = self.instance.persona
        orcid = datos.get('orcid', '')
        if orcid:
            self._orcid_de_otra_persona(orcid, persona)
        if not datos.get('nombre_persona', '').strip():
            if orcid:
                datos['nombre_persona'] = self._nombre_desde_orcid(orcid)
            else:
                self.add_error('nombre_persona', 'Escribe el nombre para mostrar.')
        return datos

    def save(self, commit=True):
        user = super().save(commit=commit)
        if not self._persona_cambia():
            persona = user.persona
            persona.nombre = self.cleaned_data['nombre_persona'].strip()
            persona.orcid = self.cleaned_data.get('orcid', '')
            persona.save(update_fields=['nombre', 'orcid', 'actualizado'])
        return user
