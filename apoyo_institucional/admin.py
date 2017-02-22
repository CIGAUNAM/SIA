from django.contrib import admin

# Register your models here.
from . models import Actividad, Comision, Representacion, CargoAcademicoAdministrativo, \
    RepresentanteAnteOrganoColegiado, ComisionAcademica, ApoyoTecnico, ApoyoOtraActividad
    #OrganoColegiado, ComisionEvaluacion

admin.site.register(Actividad)
admin.site.register(Comision)
admin.site.register(Representacion)
#admin.site.register(OrganoColegiado)
admin.site.register(CargoAcademicoAdministrativo)
admin.site.register(RepresentanteAnteOrganoColegiado)
admin.site.register(ComisionAcademica)
#admin.site.register(ComisionEvaluacion)
admin.site.register(ApoyoTecnico)
admin.site.register(ApoyoOtraActividad)



