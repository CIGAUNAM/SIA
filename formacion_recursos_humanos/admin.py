from django.contrib import admin

# Register your models here.

from . models import AsesorEstancia, DireccionTesis, ComiteTutoral, ComiteCandidaturaDoctoral

admin.site.register(AsesorEstancia)
admin.site.register(DireccionTesis)
admin.site.register(ComiteTutoral)
admin.site.register(ComiteCandidaturaDoctoral)