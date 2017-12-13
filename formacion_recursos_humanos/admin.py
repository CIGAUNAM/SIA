from django.contrib import admin

# Register your models here.

from . models import AsesoriaEstudiante, DireccionTesis, ComiteTutoral, ComiteCandidaturaDoctoral

admin.site.register(AsesoriaEstudiante)
admin.site.register(DireccionTesis)
admin.site.register(ComiteTutoral)
admin.site.register(ComiteCandidaturaDoctoral)