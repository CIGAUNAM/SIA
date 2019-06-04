from django.contrib import admin

# Register your models here.

from . models import MemoriaInExtenso, OrganizacionEventoAcademico, ParticipacionEventoAcademico, EventoDifusion

admin.site.register(MemoriaInExtenso)
admin.site.register(OrganizacionEventoAcademico)
admin.site.register(ParticipacionEventoAcademico)
admin.site.register(EventoDifusion)