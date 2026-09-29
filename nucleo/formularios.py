"""Formularios de cuenta: la cuenta se liga a su persona a partir del ORCID (o del nombre, si no tiene).

La relación interna es `User.persona`; en la interfaz solo se ven el ORCID y el nombre para mostrar.
"""

from django import forms
from unfold.forms import UserChangeForm as BaseUserChangeForm
from unfold.forms import UserCreationForm as BaseUserCreationForm
from unfold.widgets import UnfoldAdminRadioSelectWidget, UnfoldAdminTextInputWidget

from .externos import ErrorServicio, nombre_orcid, orcid_por_correo
from .fusion import resumen_referencias
from .models import Persona, User
from .nombres import formato_cita, normalizar_orcid
from .similitud import personas_parecidas
from .widgets import BuscarOrcidWidget

NUEVA = 'nueva'


def registros_de(persona):
    total = sum(resumen_referencias(persona).values())
    return 'sin registros' if not total else f'{total} registro{"s" if total != 1 else ""}'


class CamposPersona(forms.Form):
    orcid = forms.CharField(
        label='ORCID', max_length=40, required=False,
        widget=BuscarOrcidWidget({'orcid': 'id_orcid', 'nombre': 'id_nombre_persona'}, campo_correo='id_email'),
        help_text='Por ejemplo 0000-0002-1825-0097 o https://orcid.org/0000-0002-1825-0097. Con él se reconoce a la '
                  'persona en el catálogo y en las importaciones. Si falta, se busca en ORCID por el correo; el correo '
                  'solo se obtiene de ORCID si la persona lo hizo público ahí.')
    nombre_persona = forms.CharField(
        label='Nombre para mostrar', max_length=300, required=False, widget=UnfoldAdminTextInputWidget,
        help_text=f'{Persona._meta.get_field("nombre").help_text} Si lo dejas vacío, se toma de ORCID.')

    #: Lo asigna el admin (`get_form`): los académicos no cambian un ORCID ya capturado.
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


class UserCreationForm(CamposPersona, BaseUserCreationForm):
    """Alta: con el ORCID se encuentra o se crea la persona; si hay coautores parecidos, se pregunta si es alguno.

    `es_persona` solo se muestra (lo agrega el admin a la sección) cuando hay que preguntar: queda en `pregunta`.
    """
    es_persona = forms.CharField(label='¿Es alguna de estas personas?', required=False,
                                 widget=UnfoldAdminRadioSelectWidget)
    pregunta = ()

    class Meta(BaseUserCreationForm.Meta):
        model = User
        fields = ('email', 'first_name', 'last_name')
        field_classes = {}

    def clean(self):
        datos = super().clean()
        orcid, nombre = datos.get('orcid', ''), datos.get('nombre_persona', '').strip()
        self.persona = None
        self.orcid_encontrado = False
        if self.errors:
            return datos

        if not orcid:  # Quien publicó su correo en ORCID se encuentra sin capturar el ORCID.
            try:
                encontrado = orcid_por_correo(datos.get('email'))
            except ErrorServicio:
                encontrado = None
            if encontrado:
                orcid, nombre_orcid_encontrado = encontrado
                datos['orcid'], self.orcid_encontrado = orcid, True
                nombre = nombre or nombre_orcid_encontrado

        if orcid and (existente := Persona.objects.filter(orcid=orcid).first()):
            if existente.tiene_cuenta:
                self.add_error('orcid', f'Ese ORCID es de «{existente}», que ya tiene cuenta ({existente.usuario}).')
            self.persona = existente
            return datos

        nombre = nombre or (self._nombre_desde_orcid(orcid) if orcid else '')
        nombre = nombre or formato_cita(datos.get('first_name'), datos.get('last_name'))
        if not nombre:
            if 'nombre_persona' not in self.errors:
                self.add_error('nombre_persona', 'Escribe el ORCID, el nombre para mostrar o el nombre y apellidos.')
            return datos

        respuesta = datos.get('es_persona')
        candidatas = [p for p in personas_parecidas(Persona.objects.filter(usuario__isnull=True), nombre, limite=8)
                      if not (orcid and p.orcid)]
        if respuesta == NUEVA or not candidatas and not respuesta:
            correo = (datos.get('email') or '').strip().lower()
            correo = '' if correo.endswith('.invalid') else correo
            self.persona = Persona(nombre=nombre, orcid=orcid, email=correo, verificado=True)
        elif respuesta:
            self.persona = next((p for p in candidatas if str(p.pk) == respuesta), None)
            if self.persona is None:
                self.add_error('es_persona', 'Elige una de las opciones.')
        else:
            self.pregunta = ('es_persona',)
            self.fields['es_persona'].widget = UnfoldAdminRadioSelectWidget(choices=[
                *[(p.pk, f'{p} — {registros_de(p)}') for p in candidatas],
                (NUEVA, f'Ninguna: crear «{nombre}»')])
            self.add_error('es_persona', 'Ya hay personas parecidas en el catálogo (p. ej. como coautoras). Si es '
                                         'alguna, elígela para que la cuenta conserve su producción.')
        return datos

    def save(self, commit=True):
        user = super().save(commit=False)
        persona, orcid, nombre = self.persona, self.cleaned_data['orcid'], self.cleaned_data['nombre_persona'].strip()
        if orcid:
            persona.orcid = orcid
        if nombre:
            persona.nombre = nombre
        persona.save()
        user.persona = persona
        if commit:
            user.save()
            self.save_m2m()
        return user


class UserChangeForm(CamposPersona, BaseUserChangeForm):
    """Perfil: el ORCID y el nombre para mostrar se guardan en la persona de la cuenta.

    Si un administrador captura un ORCID que ya tiene otra persona sin cuenta (p. ej. un coautor importado),
    es la misma persona: se fusiona con la de la cuenta, que conserva toda la producción.
    """

    class Meta(BaseUserChangeForm.Meta):
        model = User
        field_classes = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        persona = self.instance.persona
        self.fields['nombre_persona'].initial = persona.nombre
        self.fields['orcid'].initial = persona.orcid
        self.fields['orcid'].help_text = self.fields['orcid'].help_text.replace(' Si falta, se busca en ORCID por el correo.', '')
        if persona.orcid and not self.administrador:
            self.fields['orcid'].disabled = True
            self.fields['orcid'].help_text = 'Para corregirlo, pídelo a un administrador.'
        if 'persona' in self.fields:
            self.fields['persona'].help_text = (
                'Solo para corregir una liga equivocada: la cuenta pasa a figurar como otra persona y deja la '
                'producción de la actual. Al cambiarla no se guardan el ORCID ni el nombre de arriba.')
        self.fusionada = None

    def _persona_cambia(self):
        return 'persona' in self.changed_data

    def clean(self):
        datos = super().clean()
        if self._persona_cambia() or self.errors:
            return datos
        persona = self.instance.persona
        orcid = datos.get('orcid', '')
        otra = Persona.objects.filter(orcid=orcid).exclude(pk=persona.pk).first() if orcid else None
        if otra is not None:
            if otra.tiene_cuenta:
                self.add_error('orcid', f'Ese ORCID es de la cuenta {otra.usuario}.')
            elif not self.administrador:
                self.add_error('orcid', f'Ese ORCID ya está en el catálogo como «{otra}». Pide a un administrador '
                                        'que lo ligue a tu cuenta.')
            else:
                self.fusionada = otra
        if not datos.get('nombre_persona', '').strip():
            if orcid:
                datos['nombre_persona'] = self._nombre_desde_orcid(orcid)
            else:
                self.add_error('nombre_persona', 'Escribe el nombre para mostrar.')
        return datos

    def save(self, commit=True):
        from .fusion import fusionar

        user = super().save(commit=commit)
        if not self._persona_cambia():
            persona = user.persona
            if self.fusionada is not None:
                self.resumen_fusion = f'«{self.fusionada}» ({registros_de(self.fusionada)})'
                fusionar(persona, [self.fusionada])
            persona.nombre = self.cleaned_data['nombre_persona'].strip()
            persona.orcid = self.cleaned_data.get('orcid', '')
            persona.save(update_fields=['nombre', 'orcid', 'actualizado'])
        return user
