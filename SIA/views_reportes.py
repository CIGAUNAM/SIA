from django.http.response import Http404, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View

from formacion_academica.models import CursoEspecializacion
from investigacion.models import ArticuloCientifico, CapituloLibroInvestigacion, MapaArbitrado, InformeTecnico, ProyectoInvestigacion
from difusion_cientifica.models import MemoriaInExtenso, Resena, Traduccion, OrganizacionEventoAcademico, ParticipacionEventoAcademico
from divulgacion_cientifica.models import ArticuloDivulgacion, CapituloLibroDivulgacion, OrganizacionEventoDivulgacion, ParticipacionEventoDivulgacion, ProgramaRadioTelevisionInternet
from vinculacion.models import ArbitrajePublicacionAcademica, ArbitrajeProyectoInvestigacion, ArbitrajeOtraActividad, OtroProgramaVinculacion
from docencia.models import CursoDocenciaEscolarizado, CursoDocenciaExtracurricular, ArticuloDocencia, ProgramaEstudio
from desarrollo_tecnologico.models import DesarrolloTecnologico
from distinciones.models import DistincionAcademico, ParticipacionSociedadCientifica, DistincionAlumno
from vinculacion.models import ConvenioEntidadExterna, RedAcademica, ServicioExternoEntidadNoAcademica
from nucleo.models import User, Libro
from experiencia_laboral.models import ExperienciaLaboral, LineaInvestigacion, CapacidadPotencialidad
from formacion_academica.models import Doctorado, Maestria, Licenciatura, PostDoctorado
from apoyo_institucional.models import ComisionAcademica
from movilidad_academica.models import MovilidadAcademica
from formacion_recursos_humanos.models import DireccionTesis, AsesoriaEstudiante, SupervisionInvestigadorPostDoctoral, \
    DesarrolloGrupoInvestigacionInterno, ComiteTutoral, ComiteCandidaturaDoctoral
from apoyo_institucional.models import CargoAcademicoAdministrativo, RepresentacionOrganoColegiado, ComisionAcademica, ApoyoTecnico, ApoyoOtraActividad

from datetime import datetime
from django.db.models import Q, Max, Min, Count, Sum, Avg


class Informe(View):
    template_name = 'informe.html'
    context = {}
    this_year=2018

    indices = (1, 3)

    context['articulos_cientificos_nacionales_publicados_isiscopus'] = ArticuloCientifico.objects.filter(fecha__year=this_year, revista__pais__nombre='México', status='PUBLICADO', revista__indices__isnull=False).filter(revista__indices__in=indices).distinct()
    context['articulos_cientificos_nacionales_publicados_otrosindices'] = ArticuloCientifico.objects.filter(fecha__year=this_year, revista__pais__nombre='México', status='PUBLICADO', revista__indices__isnull=False).exclude(revista__indices__in=indices).distinct()
    context['articulos_cientificos_nacionales_publicados_noindizado'] = ArticuloCientifico.objects.filter(fecha__year=this_year, revista__pais__nombre='México', status='PUBLICADO', revista__indices__isnull=True).distinct()
    context['articulos_cientificos_nacionales_enprensa'] = ArticuloCientifico.objects.filter(fecha__year=this_year, revista__pais__nombre='México', status='EN_PRENSA').distinct()
    context['articulos_cientificos_nacionales_aceptado'] = ArticuloCientifico.objects.filter(fecha__year=this_year, revista__pais__nombre='México', status='ACEPTADO').distinct()
    context['articulos_cientificos_nacionales_enviado'] = ArticuloCientifico.objects.filter(fecha__year=this_year, revista__pais__nombre='México', status='ENVIADO').distinct()


    context['articulos_cientificos_internacionales_publicados_isiscopus'] = ArticuloCientifico.objects.filter(fecha__year=this_year, status='PUBLICADO', revista__indices__isnull=False).filter(revista__indices__in=indices).exclude(revista__pais__nombre='México').distinct()
    context['articulos_cientificos_internacionales_publicados_alumnos'] = ArticuloCientifico.objects.filter(fecha__year=this_year, status='PUBLICADO', alumnos__isnull=False).exclude(revista__pais__nombre='México').distinct()
    context['articulos_cientificos_internacionales_publicados_otrosindices'] = ArticuloCientifico.objects.filter(fecha__year=this_year, status='PUBLICADO', revista__indices__isnull=False).exclude(revista__indices__in=indices).exclude(revista__pais__nombre='México').distinct()
    context['articulos_cientificos_internacionales_publicados_noindizado'] = ArticuloCientifico.objects.filter(fecha__year=this_year, status='PUBLICADO', revista__indices__isnull=True).exclude(revista__pais__nombre='México').distinct()
    context['articulos_cientificos_internacionales_enprensa'] = ArticuloCientifico.objects.filter(fecha__year=this_year, status='EN_PRENSA').exclude(revista__pais__nombre='México').distinct()
    context['articulos_cientificos_internacionales_aceptado'] = ArticuloCientifico.objects.filter(fecha__year=this_year, status='ACEPTADO').exclude(revista__pais__nombre='México').distinct()
    context['articulos_cientificos_internacionales_enviado'] = ArticuloCientifico.objects.filter(fecha__year=this_year, status='ENVIADO').exclude(revista__pais__nombre='México').distinct()

    context['articulos_cientificos_agradecimientos'] = ArticuloCientifico.objects.filter(fecha__year=this_year, agradecimientos__isnull=False).distinct()

    context['libros_investigacion_nacionales_publicados'] = Libro.objects.filter(tipo='INVESTIGACION', fecha__year=this_year, status='PUBLICADO').filter(Q(autores__isnull=False) | Q(coordinadores__isnull=False)).filter(pais__nombre='México').distinct()
    context['libros_investigacion_nacionales_enprensa'] = Libro.objects.filter(tipo='INVESTIGACION', fecha__year=this_year, status='EN_PRENSA').filter(Q(autores__isnull=False) | Q(coordinadores__isnull=False)).filter(pais__nombre='México').distinct()
    context['libros_investigacion_nacionales_aceptados'] = Libro.objects.filter(tipo='INVESTIGACION', fecha__year=this_year, status='ACEPTADO').filter(Q(autores__isnull=False) | Q(coordinadores__isnull=False)).filter(pais__nombre='México').distinct()

    context['libros_investigacion_internacionales_publicados'] = Libro.objects.filter(tipo='INVESTIGACION', fecha__year=this_year, status='PUBLICADO').filter(Q(autores__isnull=False) | Q(coordinadores__isnull=False)).exclude(pais__nombre='México').distinct()
    context['libros_investigacion_internacionales_enprensa'] = Libro.objects.filter(tipo='INVESTIGACION', fecha__year=this_year, status='EN_PRENSA').filter(Q(autores__isnull=False) | Q(coordinadores__isnull=False)).exclude(pais__nombre='México').distinct()
    context['libros_investigacion_internacionales_aceptados'] = Libro.objects.filter(tipo='INVESTIGACION', fecha__year=this_year, status='ACEPTADO').filter(Q(autores__isnull=False) | Q(coordinadores__isnull=False)).exclude(pais__nombre='México').distinct()

    context['capitulos_libros_investigacion_nacionales_publicados'] = CapituloLibroInvestigacion.objects.filter(libro__fecha__year=this_year, libro__status='PUBLICADO').filter(libro__pais__nombre='México').distinct()
    context['capitulos_libros_investigacion_nacionales_enprensa'] = CapituloLibroInvestigacion.objects.filter(libro__fecha__year=this_year, libro__status='EN_PRENSA').filter(libro__pais__nombre='México').distinct()
    context['capitulos_libros_investigacion_nacionales_enviados'] = CapituloLibroInvestigacion.objects.filter(libro__fecha__year=this_year, libro__status='ENVIADO').filter(libro__pais__nombre='México').distinct()

    context['capitulos_libros_investigacion_internacionales_publicados'] = CapituloLibroInvestigacion.objects.filter(libro__fecha__year=this_year, libro__status='PUBLICADO').exclude(libro__pais__nombre='México').distinct()
    context['capitulos_libros_investigacion_internacionales_enprensa'] = CapituloLibroInvestigacion.objects.filter(libro__fecha__year=this_year, libro__status='EN_PRENSA').exclude(libro__pais__nombre='México').distinct()
    context['capitulos_libros_investigacion_internacionales_enviados'] = CapituloLibroInvestigacion.objects.filter(libro__fecha__year=this_year, libro__status='ENVIADO').exclude(libro__pais__nombre='México').distinct()

    context['mapas_arbitrados'] = MapaArbitrado.objects.filter(fecha__year=this_year).distinct()

    context['informes_tecnicos_accesso_publico_nacionales'] = InformeTecnico.objects.filter(fecha__year=this_year).filter(proyecto__institucion__pais__nombre='México').distinct()
    context['informes_tecnicos_accesso_publico_internacionales'] = InformeTecnico.objects.filter(fecha__year=this_year).exclude(proyecto__institucion__pais__nombre='México').distinct()

    context['articulos_inextenso_memorias_nacionales'] = MemoriaInExtenso.objects.filter(evento__fecha_inicio__year=this_year).filter(evento__pais__nombre='México').distinct()
    context['articulos_inextenso_memorias_internacionales'] = MemoriaInExtenso.objects.filter(evento__fecha_inicio__year=this_year).exclude(evento__pais__nombre='México').distinct()

    context['articulos_divulgacion_nacionales_publicados'] = ArticuloDivulgacion.objects.filter(fecha__year=this_year, revista__pais__nombre='México', status='PUBLICADO').distinct()
    context['articulos_divulgacion_nacionales_enprensa'] = ArticuloDivulgacion.objects.filter(fecha__year=this_year, revista__pais__nombre='México', status='EN_PRENSA').distinct()
    context['articulos_divulgacion_nacionales_aceptado'] = ArticuloDivulgacion.objects.filter(fecha__year=this_year, revista__pais__nombre='México', status='ACEPTADO').distinct()
    context['articulos_divulgacion_nacionales_enviado'] = ArticuloDivulgacion.objects.filter(fecha__year=this_year, revista__pais__nombre='México', status='ENVIADO').distinct()

    context['articulos_divulgacion_internacionales_publicados'] = ArticuloDivulgacion.objects.filter(fecha__year=this_year, status='PUBLICADO').exclude(revista__pais__nombre='México').distinct()
    context['articulos_divulgacion_internacionales_enprensa'] = ArticuloDivulgacion.objects.filter(fecha__year=this_year, status='EN_PRENSA').exclude(revista__pais__nombre='México').distinct()
    context['articulos_divulgacion_internacionales_aceptado'] = ArticuloDivulgacion.objects.filter(fecha__year=this_year, status='ACEPTADO').exclude(revista__pais__nombre='México').distinct()
    context['articulos_divulgacion_internacionales_enviado'] = ArticuloDivulgacion.objects.filter(fecha__year=this_year, status='ENVIADO').exclude(revista__pais__nombre='México').distinct()

    context['articulos_divulgacion_agradecimientos'] = ArticuloDivulgacion.objects.filter(fecha__year=this_year, agradecimientos__isnull=False).distinct()

    context['libros_divulgacion'] = Libro.objects.filter(tipo='DIVULGACION', fecha__year=this_year).filter(Q(autores__isnull=False) | Q(coordinadores__isnull=False)).distinct()
    context['programas_radiotelevisioninternet'] = ProgramaRadioTelevisionInternet.objects.filter(fecha__year=this_year).distinct()
    context['resenas'] = Resena.objects.filter(fecha__year=this_year).distinct()



    context['proyectos_investigacion_papiit'] = ProyectoInvestigacion.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).filter(tipo_financiamiento='PAPIIT').distinct()
    context['proyectos_investigacion_papime'] = ProyectoInvestigacion.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).filter(tipo_financiamiento='PAPIME').distinct()
    context['proyectos_investigacion_conacyt'] = ProyectoInvestigacion.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).filter(tipo_financiamiento='CONACYT').distinct()
    context['proyectos_investigacion_otros'] = ProyectoInvestigacion.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).filter(tipo_financiamiento='EXTRAORDINARIOS').distinct()
    context['proyectos_investigacion_sinfinanciamiento'] = ProyectoInvestigacion.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).filter(tipo_financiamiento='SIN_RECURSOS').distinct()
    context['participacion_eventos_academicos_nacionales_invitacion'] = ParticipacionEventoAcademico.objects.filter(evento__fecha_inicio__year=this_year, por_invitacion=True).filter(evento__pais__nombre='México').distinct()
    context['participacion_eventos_academicos_nacionales_participacion'] = ParticipacionEventoAcademico.objects.filter(evento__fecha_inicio__year=this_year, por_invitacion=False).filter(evento__pais__nombre='México').distinct()
    context['participacion_eventos_academicos_internacionales_invitacion'] = ParticipacionEventoAcademico.objects.filter(evento__fecha_inicio__year=this_year, por_invitacion=True).exclude(evento__pais__nombre='México').distinct()
    context['participacion_eventos_academicos_internacionales_participacion'] = ParticipacionEventoAcademico.objects.filter(evento__fecha_inicio__year=this_year, por_invitacion=False).exclude(evento__pais__nombre='México').distinct()
    context['participacion_eventos_academicos_nacionales'] = ParticipacionEventoAcademico.objects.filter(evento__fecha_inicio__year=this_year).filter(evento__pais__nombre='México').distinct()
    context['participacion_eventos_academicos_internacionales'] = ParticipacionEventoAcademico.objects.filter(evento__fecha_inicio__year=this_year).exclude(evento__pais__nombre='México').distinct()

    context['organizacion_eventos_academicos'] = OrganizacionEventoAcademico.objects.filter(evento__fecha_inicio__year=this_year).distinct()
    context['organizacion_eventos_divulgacion'] = OrganizacionEventoDivulgacion.objects.filter(evento__fecha_inicio__year=this_year).distinct()
    context['participacion_eventos_divulgacion'] = ParticipacionEventoDivulgacion.objects.filter(evento__fecha_inicio__year=this_year).distinct()
    context['arbitrajes_publicaciones_academicas'] = ArbitrajePublicacionAcademica.objects.filter(fecha_dictamen__year=this_year).distinct()
    context['arbitrajes_proyectos_investigacion'] = ArbitrajeProyectoInvestigacion.objects.filter(fecha__year=this_year).distinct()
    context['arbitrajes_otras_actividades'] = ArbitrajeOtraActividad.objects.filter(fecha__year=this_year).distinct()
    context['redes_academicas'] = RedAcademica.objects.filter(fecha_constitucion__year=this_year).distinct()
    context['servicios_externos_entidadesnoacademicas'] = ServicioExternoEntidadNoAcademica.objects.filter(fecha_inicio__year=this_year).distinct()
    context['otros_programa_vinculacion'] = OtroProgramaVinculacion.objects.filter(fecha__year=this_year).distinct()
    context['sociedades_cientificas'] = ParticipacionSociedadCientifica.objects.filter(fecha_inicio__year=this_year).distinct()
    context['cargos_academicoadministrativos'] = CargoAcademicoAdministrativo.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).filter(dependencia__institucion__id=1).distinct()
    context['representacion_organos_colegiados'] = RepresentacionOrganoColegiado.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).distinct()
    context['comisiones_academicas'] = ComisionAcademica.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).filter(es_evaluacion=False).distinct()
    context['comisiones_academicas_evaluacion'] = ComisionAcademica.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).filter(es_evaluacion=True).distinct()
    context['apoyo_tecnico'] = ApoyoTecnico.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).distinct()
    context['otras_actividades_apoyo'] = ApoyoOtraActividad.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).distinct()
    context['invitados_nacionales'] = MovilidadAcademica.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).filter(tipo='INVITACION').filter(dependencia__pais__nombre='México').distinct()
    context['invitados_internacionales'] = MovilidadAcademica.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).filter(tipo='INVITACION').exclude(dependencia__pais__nombre='México').distinct()
    context['sabaticos'] = MovilidadAcademica.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).filter(tipo='SABATICO').distinct()
    context['docencia_licenciatura_unam'] = CursoDocenciaEscolarizado.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).filter(nivel='LICENCIATURA', nombramiento='TITULAR').filter(institucion__id=1).distinct()
    context['docencia_licenciatura_otras'] = CursoDocenciaEscolarizado.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).filter(nivel='LICENCIATURA', nombramiento='TITULAR').exclude(institucion__id=1).distinct()
    context['docencia_licenciatura_colaborador'] = CursoDocenciaEscolarizado.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).filter(nivel='LICENCIATURA', nombramiento='COLABORADOR').distinct()
    context['docencia_posgrado_ciga'] = CursoDocenciaEscolarizado.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).filter(nivel__in=['MAESTRIA', 'DOCTORADO']).filter(dependencia__id=4).distinct()
    context['docencia_posgrado_otros'] = CursoDocenciaEscolarizado.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).filter(nivel__in=['MAESTRIA', 'DOCTORADO']).exclude(dependencia__id=4).distinct()
    context['docencia_extracurriculares'] = CursoDocenciaExtracurricular.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).distinct()
    context['asesoria_estudiantes'] = AsesoriaEstudiante.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).distinct()
    context['direccion_tesis_licenciatura_terminadas'] = DireccionTesis.objects.filter(fecha_examen__year__lte=this_year, nivel_academico='LICENCIATURA', fecha_examen__year=this_year).distinct()
    context['direccion_tesis_maestria_terminadas'] = DireccionTesis.objects.filter(fecha_examen__year__lte=this_year, nivel_academico='MAESTRIA', fecha_examen__year=this_year).distinct()
    context['direccion_tesis_doctorado_terminadas'] = DireccionTesis.objects.filter(fecha_examen__year__lte=this_year, nivel_academico='DOCTORADO', fecha_examen__year=this_year).distinct()
    context['direccion_tesis_licenciatura_enproceso'] = DireccionTesis.objects.filter(nivel_academico='LICENCIATURA', fecha_examen__isnull=True).distinct()
    context['direccion_tesis_maestria_enproceso'] = DireccionTesis.objects.filter(nivel_academico='MAESTRIA', fecha_examen__isnull=True).distinct()
    context['direccion_tesis_doctorado_enproceso'] = DireccionTesis.objects.filter(nivel_academico='DOCTORADO', fecha_examen__isnull=True).distinct()
    context['comites_tutorales'] = ComiteTutoral.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).exclude(fecha_inicio__year__lte=1990).distinct()
    context['comites_candidaturas_doctorales'] = ComiteCandidaturaDoctoral.objects.filter(fecha_defensa__year=this_year).distinct()
    context['productos_tecnologicos'] = DesarrolloTecnologico.objects.filter(fecha__year=this_year).distinct()
    context['distincion_academicos'] = DistincionAcademico.objects.filter(fecha__year=this_year).distinct()
    context['distincion_alumnos'] = DistincionAlumno.objects.filter(fecha__year=this_year).distinct()





    def get(self, request):
        return render(request, self.template_name, self.context)

