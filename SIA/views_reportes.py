from django.http.response import Http404, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View

from formacion_academica.models import CursoEspecializacion
from investigacion.models import ArticuloCientifico, CapituloLibroInvestigacion, MapaArbitrado, PublicacionTecnica, ProyectoInvestigacion
from difusion_cientifica.models import MemoriaInExtenso, OrganizacionEventoAcademico, ParticipacionEventoAcademico
from divulgacion_cientifica.models import ArticuloDivulgacion, CapituloLibroDivulgacion, OrganizacionEventoDivulgacion, ParticipacionEventoDivulgacion, ProgramaRadioTelevisionInternet
from vinculacion.models import ArbitrajePublicacionAcademica, OtraComision
from docencia.models import CursoDocenciaEscolarizado, CursoDocenciaExtracurricular, ArticuloDocencia, ProgramaEstudio
from desarrollo_tecnologico.models import DesarrolloTecnologico
from distinciones.models import DistincionAcademico, ParticipacionSociedadCientifica, DistincionAlumno
from vinculacion.models import ConvenioOtraEntidad, RedAcademica, ServicioAsesoriaExterna
from nucleo.models import User, Libro
from experiencia_profesional.models import ExperienciaProfesional, LineaInvestigacion, CapacidadPotencialidad
from formacion_academica.models import Doctorado, Maestria, Licenciatura, PostDoctorado
from compromiso_institucional.models import ComisionInstitucionalCIGA
from movilidad_academica.models import MovilidadAcademica
from formacion_recursos_humanos.models import DireccionTesis, AsesoriaEstudiante, SupervisionInvestigadorPostDoctoral, \
    DesarrolloGrupoInvestigacionInterno, ComiteTutoral, ComiteCandidaturaDoctoral
from compromiso_institucional.models import LaborDirectivaCoordinacion, RepresentacionOrganoColegiadoUNAM, ComisionInstitucionalCIGA, ApoyoTecnico, ApoyoOtraActividad

from datetime import datetime
from django.db.models import Q, Max, Min, Count, Sum, Avg


class Informe(View):
    template_name = 'informe.html'
    context = {}
    this_year=2018

    indices = (1, 3)

    context['articulos_cientificos_nacionales_publicados_isiscopus'] = ArticuloCientifico.objects.filter(fecha_publicado__year=this_year, revista__revista_pais__pais_nombre='México', status='PUBLICADO', revista__revista_indices__isnull=False).filter(revista__revista_indices__in=indices).distinct()
    context['articulos_cientificos_nacionales_publicados_otrosindices'] = ArticuloCientifico.objects.filter(fecha_publicado__year=this_year, revista__revista_pais__pais_nombre='México', status='PUBLICADO', revista__revista_indices__isnull=False).exclude(revista__revista_indices__in=indices).distinct()
    context['articulos_cientificos_nacionales_publicados_noindizado'] = ArticuloCientifico.objects.filter(fecha_publicado__year=this_year, revista__revista_pais__pais_nombre='México', status='PUBLICADO', revista__revista_indices__isnull=True).distinct()
    context['articulos_cientificos_nacionales_enprensa'] = ArticuloCientifico.objects.filter(fecha_enprensa__year=this_year, revista__revista_pais__pais_nombre='México', status='EN_PRENSA').distinct()
    context['articulos_cientificos_nacionales_aceptado'] = ArticuloCientifico.objects.filter(fecha_aceptado__year=this_year, revista__revista_pais__pais_nombre='México', status='ACEPTADO').distinct()
    context['articulos_cientificos_nacionales_enviado'] = ArticuloCientifico.objects.filter(fecha_enviado__year=this_year, revista__revista_pais__pais_nombre='México', status='ENVIADO').distinct()


    context['articulos_cientificos_internacionales_publicados_isiscopus'] = ArticuloCientifico.objects.filter(fecha_publicado__year=this_year, status='PUBLICADO', revista__revista_indices__isnull=False).filter(revista__revista_indices__in=indices).exclude(revista__revista_pais__pais_nombre='México').distinct()
    context['articulos_cientificos_internacionales_publicados_alumnos'] = ArticuloCientifico.objects.filter(fecha_publicado__year=this_year, status='PUBLICADO', alumnos__isnull=False).exclude(revista__revista_pais__pais_nombre='México').distinct()
    context['articulos_cientificos_internacionales_publicados_otrosindices'] = ArticuloCientifico.objects.filter(fecha_publicado__year=this_year, status='PUBLICADO', revista__revista_indices__isnull=False).exclude(revista__revista_indices__in=indices).exclude(revista__revista_pais__pais_nombre='México').distinct()
    context['articulos_cientificos_internacionales_publicados_noindizado'] = ArticuloCientifico.objects.filter(fecha_publicado__year=this_year, status='PUBLICADO', revista__revista_indices__isnull=True).exclude(revista__revista_pais__pais_nombre='México').distinct()
    context['articulos_cientificos_internacionales_enprensa'] = ArticuloCientifico.objects.filter(fecha_enprensa__year=this_year, status='EN_PRENSA').exclude(revista__revista_pais__pais_nombre='México').distinct()
    context['articulos_cientificos_internacionales_aceptado'] = ArticuloCientifico.objects.filter(fecha_aceptado__year=this_year, status='ACEPTADO').exclude(revista__revista_pais__pais_nombre='México').distinct()
    context['articulos_cientificos_internacionales_enviado'] = ArticuloCientifico.objects.filter(fecha_enviado__year=this_year, status='ENVIADO').exclude(revista__revista_pais__pais_nombre='México').distinct()

    context['articulos_cientificos_agradecimientos'] = ArticuloCientifico.objects.filter(
        Q(fecha_publicado__year=this_year) | Q(fecha_enprensa__year=this_year) | Q(fecha_aceptado__year=this_year)
        | Q(fecha_enviado__year=this_year)).filter(agradecimientos__isnull=False).distinct()

    context['libros_investigacion_nacionales_publicados'] = Libro.objects.filter(tipo='INVESTIGACION', fecha__year=this_year, status='PUBLICADO').filter(Q(autores__isnull=False) | Q(compiladores__isnull=False)).filter(pais__pais_nombre='México').distinct()
    context['libros_investigacion_nacionales_enprensa'] = Libro.objects.filter(tipo='INVESTIGACION', fecha__year=this_year, status='EN_PRENSA').filter(Q(autores__isnull=False) | Q(compiladores__isnull=False)).filter(pais__pais_nombre='México').distinct()
    context['libros_investigacion_nacionales_aceptados'] = Libro.objects.filter(tipo='INVESTIGACION', fecha__year=this_year, status='ACEPTADO').filter(Q(autores__isnull=False) | Q(compiladores__isnull=False)).filter(pais__pais_nombre='México').distinct()

    context['libros_investigacion_internacionales_publicados'] = Libro.objects.filter(tipo='INVESTIGACION', fecha__year=this_year, status='PUBLICADO').filter(Q(autores__isnull=False) | Q(compiladores__isnull=False)).exclude(pais__pais_nombre='México').distinct()
    context['libros_investigacion_internacionales_enprensa'] = Libro.objects.filter(tipo='INVESTIGACION', fecha__year=this_year, status='EN_PRENSA').filter(Q(autores__isnull=False) | Q(compiladores__isnull=False)).exclude(pais__pais_nombre='México').distinct()
    context['libros_investigacion_internacionales_aceptados'] = Libro.objects.filter(tipo='INVESTIGACION', fecha__year=this_year, status='ACEPTADO').filter(Q(autores__isnull=False) | Q(compiladores__isnull=False)).exclude(pais__pais_nombre='México').distinct()

    context['capitulos_libros_investigacion_nacionales_publicados'] = CapituloLibroInvestigacion.objects.filter(libro__fecha__year=this_year, libro__status='PUBLICADO').filter(libro__pais__pais_nombre='México').distinct()
    context['capitulos_libros_investigacion_nacionales_enprensa'] = CapituloLibroInvestigacion.objects.filter(libro__fecha__year=this_year, libro__status='EN_PRENSA').filter(libro__pais__pais_nombre='México').distinct()
    context['capitulos_libros_investigacion_nacionales_enviados'] = CapituloLibroInvestigacion.objects.filter(libro__fecha__year=this_year, libro__status='ENVIADO').filter(libro__pais__pais_nombre='México').distinct()

    context['capitulos_libros_investigacion_internacionales_publicados'] = CapituloLibroInvestigacion.objects.filter(libro__fecha__year=this_year, libro__status='PUBLICADO').exclude(libro__pais__pais_nombre='México').distinct()
    context['capitulos_libros_investigacion_internacionales_enprensa'] = CapituloLibroInvestigacion.objects.filter(libro__fecha__year=this_year, libro__status='EN_PRENSA').exclude(libro__pais__pais_nombre='México').distinct()
    context['capitulos_libros_investigacion_internacionales_enviados'] = CapituloLibroInvestigacion.objects.filter(libro__fecha__year=this_year, libro__status='ENVIADO').exclude(libro__pais__pais_nombre='México').distinct()

    context['mapas_arbitrados'] = MapaArbitrado.objects.filter(Q(fecha_publicado__year=this_year) | Q(fecha_enprensa__year=this_year) | Q(fecha_aceptado__year=this_year)
        | Q(fecha_enviado__year=this_year)).distinct()

    context['informes_tecnicos_accesso_publico_nacionales'] = PublicacionTecnica.objects.filter(Q(fecha_publicado__year=this_year) | Q(fecha_enprensa__year=this_year) | Q(fecha_aceptado__year=this_year)
        | Q(fecha_enviado__year=this_year)).filter(proyecto__institucion__institucion_pais__pais_nombre='México').distinct()
    context['informes_tecnicos_accesso_publico_internacionales'] = PublicacionTecnica.objects.filter(Q(fecha_publicado__year=this_year) | Q(fecha_enprensa__year=this_year) | Q(fecha_aceptado__year=this_year)
        | Q(fecha_enviado__year=this_year)).exclude(proyecto__institucion__institucion_pais__pais_nombre='México').distinct()

    ### context['articulos_inextenso_memorias_nacionales'] = MemoriaInExtenso.objects.filter(fecha__year=this_year).filter(pais__pais_nombre='México').distinct()
    ### context['articulos_inextenso_memorias_internacionales'] = MemoriaInExtenso.objects.filter(fecha__year=this_year).exclude(pais__pais_nombre='México').distinct()

    #context['articulos_divulgacion_nacionales_publicados'] = ArticuloDivulgacion.objects.filter(fecha__year=this_year, revista_divulgacion__revistadivulgacion_pais__pais_nombre='México', status='PUBLICADO').distinct()
    #context['articulos_divulgacion_nacionales_enprensa'] = ArticuloDivulgacion.objects.filter(fecha__year=this_year, revista_divulgacion__revistadivulgacion_pais__pais_nombre='México', status='EN_PRENSA').distinct()
    #context['articulos_divulgacion_nacionales_aceptado'] = ArticuloDivulgacion.objects.filter(fecha__year=this_year, revista_divulgacion__revistadivulgacion_pais__pais_nombre='México', status='ACEPTADO').distinct()
    #context['articulos_divulgacion_nacionales_enviado'] = ArticuloDivulgacion.objects.filter(fecha__year=this_year, revista_divulgacion__revistadivulgacion_pais__pais_nombre='México', status='ENVIADO').distinct()

    #context['articulos_divulgacion_internacionales_publicados'] = ArticuloDivulgacion.objects.filter(fecha__year=this_year, status='PUBLICADO').exclude(revista_divulgacion__revistadivulgacion_pais__pais_nombre='México').distinct()
    #context['articulos_divulgacion_internacionales_enprensa'] = ArticuloDivulgacion.objects.filter(fecha__year=this_year, status='EN_PRENSA').exclude(revista_divulgacion__revistadivulgacion_pais__pais_nombre='México').distinct()
    #context['articulos_divulgacion_internacionales_aceptado'] = ArticuloDivulgacion.objects.filter(fecha__year=this_year, status='ACEPTADO').exclude(revista_divulgacion__revistadivulgacion_pais__pais_nombre='México').distinct()
    #context['articulos_divulgacion_internacionales_enviado'] = ArticuloDivulgacion.objects.filter(fecha__year=this_year, status='ENVIADO').exclude(revista_divulgacion__revistadivulgacion_pais__pais_nombre='México').distinct()

    #context['articulos_divulgacion_agradecimientos'] = ArticuloDivulgacion.objects.filter(fecha__year=this_year, agradecimientos__isnull=False).distinct()

    context['libros_divulgacion'] = Libro.objects.filter(tipo='DIVULGACION', fecha__year=this_year).filter(Q(autores__isnull=False) | Q(compiladores__isnull=False)).distinct()
    context['programas_radiotelevisioninternet'] = ProgramaRadioTelevisionInternet.objects.filter(fecha__year=this_year).distinct()

    context['proyectos_investigacion_papiit'] = ProyectoInvestigacion.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).filter(tipo_financiamiento='PAPIIT').distinct()
    context['proyectos_investigacion_papime'] = ProyectoInvestigacion.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).filter(tipo_financiamiento='PAPIME').distinct()
    context['proyectos_investigacion_conacyt'] = ProyectoInvestigacion.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).filter(tipo_financiamiento='CONACYT').distinct()
    context['proyectos_investigacion_otros'] = ProyectoInvestigacion.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).filter(tipo_financiamiento='EXTRAORDINARIOS').distinct()
    context['proyectos_investigacion_sinfinanciamiento'] = ProyectoInvestigacion.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).filter(tipo_financiamiento='SIN_RECURSOS').distinct()
    context['participacion_eventos_academicos_nacionales_invitacion'] = ParticipacionEventoAcademico.objects.filter(fecha__year=this_year, por_invitacion=True).filter(pais__pais_nombre='México').distinct()
    context['participacion_eventos_academicos_nacionales_participacion'] = ParticipacionEventoAcademico.objects.filter(fecha__year=this_year, por_invitacion=False).filter(pais__pais_nombre='México').distinct()
    context['participacion_eventos_academicos_internacionales_invitacion'] = ParticipacionEventoAcademico.objects.filter(fecha__year=this_year, por_invitacion=True).exclude(pais__pais_nombre='México').distinct()
    context['participacion_eventos_academicos_internacionales_participacion'] = ParticipacionEventoAcademico.objects.filter(fecha__year=this_year, por_invitacion=False).exclude(pais__pais_nombre='México').distinct()

    context['organizacion_eventos_academicos'] = OrganizacionEventoAcademico.objects.filter(evento__eventodifusion_fecha_inicio__year=this_year).distinct()
    context['organizacion_eventos_divulgacion'] = OrganizacionEventoDivulgacion.objects.filter(evento2__fecha_inicio__year=this_year).distinct()
    context['participacion_eventos_divulgacion'] = ParticipacionEventoDivulgacion.objects.filter(evento__fecha_inicio__year=this_year).distinct()
    context['arbitrajes_publicaciones_academicas'] = ArbitrajePublicacionAcademica.objects.filter(fecha_dictamen__year=this_year).distinct()
    context['arbitrajes_otras_actividades'] = OtraComision.objects.filter(fecha_inicio__year=this_year).distinct()
    context['redes_academicas'] = RedAcademica.objects.filter(fecha_constitucion__year=this_year).distinct()
    context['servicios_externos_entidadesnoacademicas'] = ServicioAsesoriaExterna.objects.filter(fecha_inicio__year=this_year).distinct()
    # context['otros_programa_vinculacion'] = OtroProgramaVinculacion.objects.filter(fecha__year=this_year).distinct()
    context['sociedades_cientificas'] = ParticipacionSociedadCientifica.objects.filter(fecha_inicio__year=this_year).distinct()
    context['cargos_academicoadministrativos'] = LaborDirectivaCoordinacion.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).filter(institucion__id=1).distinct()
    context['representacion_organos_colegiados'] = RepresentacionOrganoColegiadoUNAM.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).distinct()
    context['comisiones_academicas'] = ComisionInstitucionalCIGA.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).distinct()
    # context['comisiones_academicas_evaluacion'] = ComisionInstitucionalCIGA.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).filter(es_evaluacion=True).distinct()
    context['apoyo_tecnico'] = ApoyoTecnico.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).distinct()
    context['otras_actividades_apoyo'] = ApoyoOtraActividad.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).distinct()
    context['invitados_nacionales'] = MovilidadAcademica.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).filter(tipo='INVITACION').filter(dependencia__institucion_dependencia__pais_institucion__pais_nombre='México').distinct()
    context['invitados_internacionales'] = MovilidadAcademica.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).filter(tipo='INVITACION').exclude(dependencia__institucion_dependencia__pais_institucion__pais_nombre='México').distinct()
    context['sabaticos'] = MovilidadAcademica.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).filter(tipo='SABATICO').distinct()
    context['docencia_licenciatura_unam'] = CursoDocenciaEscolarizado.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).filter(nivel='LICENCIATURA', nombramiento='TITULAR').filter(institucion2__id=1).distinct()
    context['docencia_licenciatura_otras'] = CursoDocenciaEscolarizado.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).filter(nivel='LICENCIATURA', nombramiento='TITULAR').exclude(institucion2__id=1).distinct()
    context['docencia_licenciatura_colaborador'] = CursoDocenciaEscolarizado.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).filter(nivel='LICENCIATURA', nombramiento='COLABORADOR').distinct()
    context['docencia_posgrado_ciga'] = CursoDocenciaEscolarizado.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).filter(nivel__in=['MAESTRIA', 'DOCTORADO']).filter(dependencia__id=4).distinct()
    context['docencia_posgrado_otros'] = CursoDocenciaEscolarizado.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).filter(nivel__in=['MAESTRIA', 'DOCTORADO']).exclude(dependencia__id=4).distinct()
    context['docencia_extracurriculares'] = CursoDocenciaExtracurricular.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).distinct()
    context['asesoria_estudiantes'] = AsesoriaEstudiante.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).distinct()
    context['direccion_tesis_licenciatura_terminadas'] = DireccionTesis.objects.filter(fecha_examen__year__lte=this_year, nivel_academico='LICENCIATURA', fecha_examen__year=this_year).distinct()
    context['direccion_tesis_maestria_terminadas'] = DireccionTesis.objects.filter(fecha_examen__year__lte=this_year, nivel_academico='MAESTRIA', fecha_examen__year=this_year).distinct()
    context['direccion_tesis_doctorado_terminadas'] = DireccionTesis.objects.filter(fecha_examen__year__lte=this_year, nivel_academico='DOCTORADO', fecha_examen__year=this_year).distinct()
    context['direccion_tesis_licenciatura_enproceso'] = DireccionTesis.objects.filter(fecha_examen__year__lte=this_year, nivel_academico='LICENCIATURA', fecha_examen__isnull=True).distinct()
    context['direccion_tesis_maestria_enproceso'] = DireccionTesis.objects.filter(fecha_examen__year__lte=this_year, nivel_academico='MAESTRIA', fecha_examen__isnull=True).distinct()
    context['direccion_tesis_doctorado_enproceso'] = DireccionTesis.objects.filter(fecha_examen__year__lte=this_year, nivel_academico='DOCTORADO', fecha_examen__isnull=True).distinct()
    context['comites_tutorales'] = ComiteTutoral.objects.filter((Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__year__gte=this_year)) | (Q(fecha_inicio__year__lte=this_year) & Q(fecha_fin__isnull=True))).exclude(fecha_inicio__year__lte=1990).distinct()
    context['comites_candidaturas_doctorales'] = ComiteCandidaturaDoctoral.objects.filter(fecha_defensa__year=this_year).distinct()
    context['productos_tecnologicos'] = DesarrolloTecnologico.objects.filter(fecha__year=this_year).distinct()
    context['productos_tecnologicos'] = DistincionAcademico.objects.filter(fecha__year=this_year).distinct()
    context['distincion_academicos'] = DistincionAcademico.objects.filter(fecha__year=this_year).distinct()
    context['distincion_alumnos'] = DistincionAlumno.objects.filter(fecha__year=this_year).distinct()


    def get(self, request):
        return render(request, self.template_name, self.context)