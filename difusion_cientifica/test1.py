import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SIA.settings")

django.setup()

from datetime import datetime, date
from django.db import models
#from django.contrib.auth.models import AbstractUser
from django.conf import settings

from django.core.serializers.python import Serializer
from django.http.response import (Http404, HttpResponse)
from django.core import serializers
from django.views.generic import View


from difusion_cientifica.models import Resena
from nucleo.models import User

class MySerialiserResena(Serializer):
    def end_object(self, obj):

        if self._current['libro_resenado']:
            self._current['publicacion'] = obj.libro_resenado
        else:
            self._current['publicacion'] = obj.revista_resenada


        self.objects.append( self._current )

class ResenaJSON(View):
    def get(self, request):

        try:
            #usuarioid = User.objects.get(username=request.user.username).id
            usuarioid = request
            items = Resena.objects.filter(usuario=usuarioid)
            ser = MySerialiserResena()
            ser.end_object(items)
            json = serializers.serialize('json', items, use_natural_foreign_keys=True,
                                         fields=('titulo',))
            return HttpResponse(json, content_type='application/json')
        except:
            raise Http404

a = ResenaJSON()

a.get(21)

print(a)