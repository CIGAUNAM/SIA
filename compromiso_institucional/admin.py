from django.contrib import admin

# Register your models here.
from . models import ActividadApoyo, Comision, Representacion, LaborDirectivaCoordinacion, \
    RepresentacionOrganoColegiadoUNAM, ComisionInstitucionalCIGA, ApoyoTecnico, ApoyoOtraActividad
    #OrganoColegiado, ComisionEvaluacion

admin.site.register(ActividadApoyo)
admin.site.register(Comision)
admin.site.register(Representacion)
#admin.site.register(OrganoColegiado)
admin.site.register(LaborDirectivaCoordinacion)
admin.site.register(RepresentacionOrganoColegiadoUNAM)
admin.site.register(ComisionInstitucionalCIGA)
#admin.site.register(ComisionEvaluacion)
admin.site.register(ApoyoTecnico)
admin.site.register(ApoyoOtraActividad)



