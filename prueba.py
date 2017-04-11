import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SIA.settings")

django.setup()


from movilidad_academica.models import MovilidadAcademica
from django.core.serializers.python import Serializer


class MySer(Serializer):
    def get_dump_object9(self, obj):
        data = self._current
        if not self.selected_fields or 'ciudad' in self.selected_fields:
            data['ciudad'] = obj.dependencia.ciudad
        return data

    def getvalue(self):
        return super(Serializer, self).getvalue()

items = MovilidadAcademica.objects.filter(usuario=21, tipo='INVITACION')
print(type(items))
print(items)
jsons = Serializer.serialize('json', items)

