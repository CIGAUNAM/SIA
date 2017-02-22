from django.contrib import admin

# Register your models here.

from . models import ArbitrajePublicacionAcademica, ArbitrajeProyectoInvestigacion, ArbitrajeOtrasActividades, RedAcademica, \
    ConvenioEntidadNoAcademica, ClasificacionServicio, ServicioExternoEntidadNoAcademica, OtroProgramaVinculacion

admin.site.register(ArbitrajePublicacionAcademica)
admin.site.register(ArbitrajeProyectoInvestigacion)
admin.site.register(ArbitrajeOtrasActividades)
admin.site.register(RedAcademica)
admin.site.register(ConvenioEntidadNoAcademica)
admin.site.register(ClasificacionServicio)
admin.site.register(ServicioExternoEntidadNoAcademica)
admin.site.register(OtroProgramaVinculacion)