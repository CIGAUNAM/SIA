from django.contrib import admin

# Register your models here.

from .models import DistincionAcademico, DistincionAlumno

admin.site.register(DistincionAcademico)
admin.site.register(DistincionAlumno)