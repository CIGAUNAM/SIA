from django.contrib import admin

# Register your models here.

from . models import ArbitrajePublicacionAcademica, OtraComisionArbitraje, RedAcademica, \
    ConvenioOtraEntidad, ServicioAsesoriaExterna, ComisionArbitraje

admin.site.register(ArbitrajePublicacionAcademica)
admin.site.register(OtraComisionArbitraje)
admin.site.register(RedAcademica)
admin.site.register(ConvenioOtraEntidad)
admin.site.register(ServicioAsesoriaExterna)
admin.site.register(ComisionArbitraje)