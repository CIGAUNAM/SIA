from django.contrib import admin

# Register your models here.

from . models import ArticuloDivulgacion, CapituloLibroDivulgacion, OrganizacionEventoDivulgacion, ParticipacionEventoDivulgacion, MedioDivulgacion, ProgramaRadioTelevisionInternet

admin.site.register(ArticuloDivulgacion)
#admin.site.register(LibroDivulgacion)
admin.site.register(CapituloLibroDivulgacion)
admin.site.register(OrganizacionEventoDivulgacion)
admin.site.register(ParticipacionEventoDivulgacion)
admin.site.register(MedioDivulgacion)
admin.site.register(ProgramaRadioTelevisionInternet)