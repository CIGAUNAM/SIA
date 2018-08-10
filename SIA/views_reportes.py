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

    context['articulos_cientificos_nacionales_publicados'] = ArticuloCientifico.objects.filter(fecha__year=this_year, revista__pais__nombre='México', status='PUBLICADO')
    context['articulos_cientificos_nacionales_enprensa'] = ArticuloCientifico.objects.filter(fecha__year=this_year, revista__pais__nombre='México', status='EN_PRENSA')
    context['articulos_cientificos_nacionales_aceptado'] = ArticuloCientifico.objects.filter(fecha__year=this_year, revista__pais__nombre='México', status='ACEPTADO')
    context['articulos_cientificos_nacionales_enviado'] = ArticuloCientifico.objects.filter(fecha__year=this_year, revista__pais__nombre='México', status='ENVIADO')

    context['articulos_cientificos_internacionales_publicados'] = ArticuloCientifico.objects.filter(fecha__year=this_year, status='PUBLICADO').exclude(revista__pais__nombre='México')


    def get(self, request):
        return render(request, self.template_name, self.context)
