from django.contrib import admin

# Register your models here.

from . models import ExperienciaProfesional, LineaInvestigacion, CapacidadPotencialidad

admin.site.register(ExperienciaProfesional)
admin.site.register(LineaInvestigacion)
admin.site.register(CapacidadPotencialidad)

