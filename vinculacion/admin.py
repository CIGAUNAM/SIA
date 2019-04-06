from django.contrib import admin

# Register your models here.

from . models import ArbitrajePublicacionAcademica, OtraComision, RedAcademica, \
    ConvenioEntidadExterna, ServicioAsesoriaExterna, OtroProgramaVinculacion

admin.site.register(ArbitrajePublicacionAcademica)
admin.site.register(OtraComision)
admin.site.register(RedAcademica)
admin.site.register(ConvenioEntidadExterna)
admin.site.register(ServicioAsesoriaExterna)
admin.site.register(OtroProgramaVinculacion)