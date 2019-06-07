from django.contrib import admin

# Register your models here.

from . models import ArbitrajePublicacionAcademica, OtraComision, RedAcademica, \
    ConvenioOtraEntidad, ServicioAsesoriaExterna, ComisionVinculacion

admin.site.register(ArbitrajePublicacionAcademica)
admin.site.register(OtraComision)
admin.site.register(RedAcademica)
admin.site.register(ConvenioOtraEntidad)
admin.site.register(ServicioAsesoriaExterna)
admin.site.register(ComisionVinculacion)