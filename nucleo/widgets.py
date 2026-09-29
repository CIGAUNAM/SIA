"""Widgets propios del admin."""

import json

from django.urls import reverse_lazy
from unfold.widgets import UnfoldAdminTextInputWidget


class BuscarOrcidWidget(UnfoldAdminTextInputWidget):
    """Campo de ORCID con un botón que consulta ORCID (por el ORCID o, si está vacío, por el correo) y llena los
    campos vacíos del formulario. `destinos`: {'nombre' | 'email' | 'orcid': id del campo en el formulario}."""
    template_name = 'nucleo/widgets/orcid.html'

    def __init__(self, destinos, campo_correo=None, en_persona=False, attrs=None):
        self.destinos, self.campo_correo, self.en_persona = destinos, campo_correo, en_persona
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        contexto = super().get_context(name, value, attrs)
        contexto['orcid_url'] = reverse_lazy('admin:orcid')
        contexto['orcid_destinos'] = json.dumps(self.destinos)
        contexto['orcid_correo'] = self.campo_correo or ''
        contexto['orcid_en_persona'] = self.en_persona  # Al editar una persona, su propio ORCID no es "de otra".
        return contexto
