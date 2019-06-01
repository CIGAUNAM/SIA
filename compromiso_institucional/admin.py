from django.contrib import admin

# Register your models here.
from . models import ActividadApoyo, ComisionInstitucional, Representacion, LaborDirectivaCoordinacion, \
    RepresentacionOrganoColegiadoUNAM, ComisionInstitucionalCIGA, ApoyoTecnico, ApoyoOtraActividad

admin.site.register(ActividadApoyo)
admin.site.register(ComisionInstitucional)
admin.site.register(Representacion)
admin.site.register(LaborDirectivaCoordinacion)
admin.site.register(RepresentacionOrganoColegiadoUNAM)
admin.site.register(ComisionInstitucionalCIGA)
admin.site.register(ApoyoTecnico)
admin.site.register(ApoyoOtraActividad)



