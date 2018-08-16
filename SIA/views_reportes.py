from django.http.response import Http404, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View

from formacion_academica.models import CursoEspecializacion
from investigacion.models import ArticuloCientifico, CapituloLibroInvestigacion, MapaArbitrado, InformeTecnico, ProyectoInvestigacion
from difusion_cientifica.models import MemoriaInExtenso, PrologoLibro, Resena, Traduccion, OrganizacionEventoAcademico, ParticipacionEventoAcademico
from divulgacion_cientifica.models import ArticuloDivulgacion, CapituloLibroDivulgacion, OrganizacionEventoDivulgacion, ParticipacionEventoDivulgacion, ProgramaRadioTelevisionInternet
from vinculacion.models import ArbitrajePublicacionAcademica, ArbitrajeProyectoInvestigacion
from docencia.models import CursoDocenciaEscolarizado, CursoDocenciaExtracurricular, ArticuloDocencia, ProgramaEstudio
from desarrollo_tecnologico.models import DesarrolloTecnologico
from distinciones.models import DistincionAcademico, ParticipacionComisionExpertos, ParticipacionSociedadCientifica, CitaPublicacion
from vinculacion.models import ConvenioEntidadExterna, RedAcademica, ServicioExternoEntidadNoAcademica
from nucleo.models import User, Libro
from experiencia_laboral.models import ExperienciaLaboral, LineaInvestigacion, CapacidadPotencialidad
from formacion_academica.models import Doctorado, Maestria, Licenciatura, PostDoctorado
from apoyo_institucional.models import ComisionAcademica
from movilidad_academica.models import MovilidadAcademica
from formacion_recursos_humanos.models import DireccionTesis, AsesoriaEstudiante, SupervisionInvestigadorPostDoctoral, \
    DesarrolloGrupoInvestigacionInterno, ComiteTutoral, ComiteCandidaturaDoctoral

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

    context['libros_investigacion_nacionales_publicados'] = Libro.objects.filter(tipo='INVESTIGACION', fecha__year=this_year, status='PUBLICADO').filter(Q(autores__isnull=False) | Q(editores__isnull=False) | Q(coordinadores__isnull=False)).filter(editorial__pais__nombre='México').distinct()
    context['libros_investigacion_nacionales_enprensa'] = Libro.objects.filter(tipo='INVESTIGACION', fecha__year=this_year, status='EN_PRENSA').filter(Q(autores__isnull=False) | Q(editores__isnull=False) | Q(coordinadores__isnull=False)).filter(editorial__pais__nombre='México').distinct()
    context['libros_investigacion_nacionales_aceptados'] = Libro.objects.filter(tipo='INVESTIGACION', fecha__year=this_year, status='ACEPTADO').filter(Q(autores__isnull=False) | Q(editores__isnull=False) | Q(coordinadores__isnull=False)).filter(editorial__pais__nombre='México').distinct()

    context['libros_investigacion_internacionales_publicados'] = Libro.objects.filter(tipo='INVESTIGACION', fecha__year=this_year, status='PUBLICADO').filter(Q(autores__isnull=False) | Q(editores__isnull=False) | Q(coordinadores__isnull=False)).exclude(editorial__pais__nombre='México').distinct()
    context['libros_investigacion_internacionales_enprensa'] = Libro.objects.filter(tipo='INVESTIGACION', fecha__year=this_year, status='EN_PRENSA').filter(Q(autores__isnull=False) | Q(editores__isnull=False) | Q(coordinadores__isnull=False)).exclude(editorial__pais__nombre='México').distinct()
    context['libros_investigacion_internacionales_aceptados'] = Libro.objects.filter(tipo='INVESTIGACION', fecha__year=this_year, status='ACEPTADO').filter(Q(autores__isnull=False) | Q(editores__isnull=False) | Q(coordinadores__isnull=False)).exclude(editorial__pais__nombre='México').distinct()

    context['capitulos_libros_investigacion_nacionales_publicados'] = CapituloLibroInvestigacion.objects.filter(libro__fecha__year=this_year, libro__status='PUBLICADO').filter(libro__editorial__pais__nombre='México').distinct()
    context['capitulos_libros_investigacion_nacionales_enprensa'] = CapituloLibroInvestigacion.objects.filter(libro__fecha__year=this_year, libro__status='EN_PRENSA').filter(libro__editorial__pais__nombre='México').distinct()
    context['capitulos_libros_investigacion_nacionales_enviados'] = CapituloLibroInvestigacion.objects.filter(libro__fecha__year=this_year, libro__status='ENVIADO').filter(libro__editorial__pais__nombre='México').distinct()

    context['capitulos_libros_investigacion_internacionales_publicados'] = CapituloLibroInvestigacion.objects.filter(libro__fecha__year=this_year, libro__status='PUBLICADO').exclude(libro__editorial__pais__nombre='México').distinct()
    context['capitulos_libros_investigacion_internacionales_enprensa'] = CapituloLibroInvestigacion.objects.filter(libro__fecha__year=this_year, libro__status='EN_PRENSA').exclude(libro__editorial__pais__nombre='México').distinct()
    context['capitulos_libros_investigacion_internacionales_enviados'] = CapituloLibroInvestigacion.objects.filter(libro__fecha__year=this_year, libro__status='ENVIADO').exclude(libro__editorial__pais__nombre='México').distinct()

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

    context['libros_divulgacion'] = Libro.objects.filter(tipo='DIVULGACION', fecha__year=this_year).filter(Q(autores__isnull=False) | Q(editores__isnull=False) | Q(coordinadores__isnull=False)).distinct()
    context['programas_radiotelevisioninternet'] = ProgramaRadioTelevisionInternet.objects.filter(fecha__year=this_year).distinct()
    context['resenas'] = Resena.objects.filter(fecha__year=this_year).distinct()

    context['proyectos_investigacion_papiit'] = ProyectoInvestigacion.objects.filter(fecha_inicio__year=this_year, financiamiento_papiit__isnull=False)
    context['proyectos_investigacion_papime'] = ProyectoInvestigacion.objects.filter(fecha_inicio__year=this_year, financiamiento_papime__isnull=False)


    def get(self, request):
        return render(request, self.template_name, self.context)
