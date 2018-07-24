from django.contrib import admin

# Register your models here.

from . models import CursoDocenciaEscolarizado, CursoDocenciaExtracurricular

admin.site.register(CursoDocenciaEscolarizado)
admin.site.register(CursoDocenciaExtracurricular)