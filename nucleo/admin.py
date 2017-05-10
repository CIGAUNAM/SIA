from django.contrib import admin

# Register your models here.

from . models import Tag, ZonaPais, Pais, Estado, Ciudad, Institucion, Dependencia, Departamento, \
    User, AreaConocimiento, AreaEspecialidad, ImpactoSocial, Cargo, Financiamiento, \
    Metodologia, Beca, ProgramaLicenciatura, \
    ProgramaMaestria, ProgramaDoctorado, TipoEvento, Evento, ProblemaNacionalConacyt, Proyecto, Nombramiento, \
    TipoDocumento, Indice, Editorial, Coleccion, Libro, Revista, Asignatura

admin.site.register(Tag)
admin.site.register(ZonaPais)
admin.site.register(Pais)
admin.site.register(Estado)
admin.site.register(Ciudad)
admin.site.register(Institucion)
admin.site.register(Dependencia)
admin.site.register(Departamento)
admin.site.register(User)
admin.site.register(AreaConocimiento)
admin.site.register(AreaEspecialidad)
admin.site.register(ImpactoSocial)
admin.site.register(Cargo)
admin.site.register(Financiamiento)
admin.site.register(Metodologia)
admin.site.register(Beca)
admin.site.register(ProgramaLicenciatura)
admin.site.register(ProgramaMaestria)
admin.site.register(ProgramaDoctorado)
admin.site.register(TipoEvento)
admin.site.register(Evento)
admin.site.register(ProblemaNacionalConacyt)
admin.site.register(Proyecto)
admin.site.register(Nombramiento)


admin.site.register(TipoDocumento)
admin.site.register(Indice)
admin.site.register(Editorial)
admin.site.register(Coleccion)
admin.site.register(Libro)
admin.site.register(Revista)
admin.site.register(Asignatura)