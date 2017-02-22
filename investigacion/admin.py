from django.contrib import admin

# Register your models here.
from . models import ArticuloCientifico, CapituloLibroInvestigacion, MapaArbitrado, InformeTecnico


admin.site.register(ArticuloCientifico)
admin.site.register(CapituloLibroInvestigacion)
admin.site.register(MapaArbitrado)
admin.site.register(InformeTecnico)