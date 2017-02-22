from django.contrib import admin

# Register your models here.

from . models import ExperienciaLaboral, LineaInvestigacion, CapacidadPotencialidad

admin.site.register(ExperienciaLaboral)
admin.site.register(LineaInvestigacion)
admin.site.register(CapacidadPotencialidad)

