from django.contrib import admin

# Register your models here.
from . models import ActividadApoyo, Comision, Representacion, CargoAcademicoAdministrativo, \
    RepresentacionOrganoColegiado, ComisionAcademica, ApoyoTecnico, ApoyoOtraActividad
    #OrganoColegiado, ComisionEvaluacion

admin.site.register(ActividadApoyo)
admin.site.register(Comision)
admin.site.register(Representacion)
#admin.site.register(OrganoColegiado)
admin.site.register(CargoAcademicoAdministrativo)
admin.site.register(RepresentacionOrganoColegiado)
admin.site.register(ComisionAcademica)
#admin.site.register(ComisionEvaluacion)
admin.site.register(ApoyoTecnico)
admin.site.register(ApoyoOtraActividad)



