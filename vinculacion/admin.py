from django.contrib import admin

# Register your models here.

from . models import ArbitrajePublicacionAcademica, ArbitrajeProyectoInvestigacion, ArbitrajeOtraActividad, RedAcademica, \
    ConvenioEntidadExterna, ClasificacionServicio, ServicioExternoEntidadNoAcademica, OtroProgramaVinculacion

admin.site.register(ArbitrajePublicacionAcademica)
admin.site.register(ArbitrajeProyectoInvestigacion)
admin.site.register(ArbitrajeOtraActividad)
admin.site.register(RedAcademica)
admin.site.register(ConvenioEntidadExterna)
admin.site.register(ClasificacionServicio)
admin.site.register(ServicioExternoEntidadNoAcademica)
admin.site.register(OtroProgramaVinculacion)