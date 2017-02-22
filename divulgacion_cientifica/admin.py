from django.contrib import admin

# Register your models here.

from . models import ArticuloDivulgacion, LibroDivulgacion, CapituloLibroDivulgacion, OrganizacionEvento, ParticipacionEvento, MedioDivulgacion, ProgramaRadioTelevisionInternet

admin.site.register(ArticuloDivulgacion)
admin.site.register(LibroDivulgacion)
admin.site.register(CapituloLibroDivulgacion)
admin.site.register(OrganizacionEvento)
admin.site.register(ParticipacionEvento)
admin.site.register(MedioDivulgacion)
admin.site.register(ProgramaRadioTelevisionInternet)