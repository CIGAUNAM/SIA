from django.contrib import admin

# Register your models here.

from . models import MemoriaInExtenso, Resena, OrganizacionEventoAcademico, ParticipacionEventoAcademico

admin.site.register(MemoriaInExtenso)
admin.site.register(Resena)
admin.site.register(OrganizacionEventoAcademico)
admin.site.register(ParticipacionEventoAcademico)