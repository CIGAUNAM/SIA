# -*- coding: utf-8 -*-

from django.http.response import Http404, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View

from formacion_academica.models import CursoEspecializacion
from investigacion.models import ArticuloCientifico, CapituloLibroInvestigacion, MapaArbitrado, PublicacionTecnica, ProyectoInvestigacion
from difusion_cientifica.models import MemoriaInExtenso, Resena, Traduccion, OrganizacionEventoAcademico, ParticipacionEventoAcademico
from divulgacion_cientifica.models import ArticuloDivulgacion, CapituloLibroDivulgacion, OrganizacionEventoDivulgacion, ParticipacionEventoDivulgacion, ProgramaRadioTelevisionInternet
from vinculacion.models import ArbitrajePublicacionAcademica
from docencia.models import CursoDocenciaEscolarizado, CursoDocenciaExtracurricular, ArticuloDocencia, ProgramaEstudio
from desarrollo_tecnologico.models import DesarrolloTecnologico
from distinciones.models import DistincionAcademico, ParticipacionComisionExpertos, ParticipacionSociedadCientifica, CitaPublicacion
from vinculacion.models import ConvenioEntidadExterna, RedAcademica, ServicioAsesoriaExterna
from nucleo.models import User, Libro
from experiencia_profesional.models import ExperienciaProfesional, LineaInvestigacion, CapacidadPotencialidad
from formacion_academica.models import Doctorado, Maestria, Licenciatura, PostDoctorado
from compromiso_institucional.models import ComisionInstitucionalCIGA
from movilidad_academica.models import MovilidadAcademica
from formacion_recursos_humanos.models import DireccionTesis, AsesoriaEstudiante, SupervisionInvestigadorPostDoctoral, \
    DesarrolloGrupoInvestigacionInterno, ComiteTutoral, ComiteCandidaturaDoctoral



from datetime import datetime
from django.db.models import Q, Max, Min, Count, Sum, Avg

from graphos.sources.simple import SimpleDataSource
from graphos.renderers.morris import LineChart, BarChart, DonutChart
from graphos.renderers.gchart import PieChart

from django.template.loader import get_template
from subprocess import Popen, PIPE
import tempfile
import os, sys

# Create your views here.

from graphos.renderers import gchart


class CustomGchart(gchart.LineChart):
    def get_template(self):
        return "demo/gchart_line.html"


class Dashboard(View):
    form_class = None
    template_name = 'dashboard.html'
    aux = {}
    now = datetime.now()
    this_year = now.year
    ten_years_ago = now.year - 10

    def get(self, request):
        context = {}

        if request.user.is_authenticated:
            num_years = 10
            last_x_years = []
            active_users_per_last_x_year = []

            for i in range(datetime.now().year - num_years + 1, datetime.now().year + 1):
                last_x_years.append(i)

            for i in last_x_years:
                users_with_items_year_count = User.objects.filter(
                    (Q(ingreso_entidad__year__lte=i) & Q(egreso_entidad__year__gt=i)) |
                    (Q(ingreso_entidad__year__lte=i) & Q(egreso_entidad=None)))
                active_users_per_last_x_year.append(users_with_items_year_count.count())

            # years_cursos_especializacion_dates = CursoEspecializacion.objects.dates('fecha_inicio', 'year', order='DESC')
            # years_cursos_especializacion = []

            # for i in reversed(years_cursos_especializacion_dates[:num_years]):
            #    years_cursos_especializacion.append(str(i.year))

            # cursos_data = [['Año', 'Personas', 'Total horas', 'Mis horas', 'Promedio Horas', 'Max horas', 'Min horas']]


            cursos_data = [['Año', 'Mis horas', 'Promedio horas', 'Max horas', 'Min horas']]
            for i in range(num_years):
                year = last_x_years[i]
                cursos_data.append([str(last_x_years[i])])

                users_with_items_year_count = User.objects.filter(
                    Q(cursos_especializacion__fecha_inicio__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0

                total_course_hours_year_sum = CursoEspecializacion.objects.filter(fecha_inicio__year=year).filter((
                    (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) |
                    (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).aggregate(
                    Sum('horas'))['horas__sum']
                if total_course_hours_year_sum == None:
                    total_course_hours_year_sum = 0

                request_user_item_year_sum = User.objects.filter(cursos_especializacion__fecha_inicio__year=year,
                                                                 cursos_especializacion__usuario=request.user).aggregate(
                    Sum('cursos_especializacion__horas'))['cursos_especializacion__horas__sum']
                if not request_user_item_year_sum:
                    request_user_item_year_sum = 0
                cursos_data[i + 1].append(request_user_item_year_sum)

                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    cursos_data[i + 1].append(round(total_course_hours_year_sum / users_with_items_year_count, 2))
                else:
                    cursos_data[i + 1].append(round(0, 2))

                max_item_year_user = User.objects.filter(cursos_especializacion__fecha_inicio__year=year).annotate(
                    Sum('cursos_especializacion__horas')).filter((
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).aggregate(
                    Max('cursos_especializacion__horas__sum'))[
                    'cursos_especializacion__horas__sum__max']
                if max_item_year_user == None:
                    max_item_year_user = 0
                cursos_data[i + 1].append(max_item_year_user)

                min_item_year_user = User.objects.filter(cursos_especializacion__fecha_inicio__year=year).annotate(
                    Sum('cursos_especializacion__horas')).filter((
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).aggregate(
                    Min('cursos_especializacion__horas__sum'))[
                    'cursos_especializacion__horas__sum__min']
                if not min_item_year_user:
                    min_item_year_user = 0
                cursos_data[i + 1].append(min_item_year_user)

            data_source = SimpleDataSource(data=cursos_data)
            chart_cursos_especializacion = LineChart(data_source)
            context['chart_cursos_especializacion'] = chart_cursos_especializacion

            items_data = [
                ['Año', 'Mis artículos de investigación', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_articulos_cientificos_enprensa_year_sum = ArticuloCientifico.objects.filter(fecha__year=year,
                                                                                                  status='PUBLICADO').filter(
                    ((Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad__year__gt=year)) | (
                        Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad=None)))).count()

                request_user_item_year_sum = ArticuloCientifico.objects.filter(fecha__year=year,
                                                                               status='PUBLICADO',
                                                                               autores=request.user).count()
                if not request_user_item_year_sum:
                    request_user_item_year_sum = 0
                items_data[i + 1].append(request_user_item_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(articulo_cientifico_autores__fecha__year=year, articulo_cientifico_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0

                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(total_articulos_cientificos_enprensa_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(0)

                max_item_year_user = User.objects.filter(
                    Q(articulo_cientifico_autores__fecha__year=year, articulo_cientifico_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('articulo_cientifico_autores')).aggregate(Max('articulo_cientifico_autores__count'))[
                    'articulo_cientifico_autores__count__max']
                if max_item_year_user == None:
                    max_item_year_user = 0
                items_data[i + 1].append(max_item_year_user)

                min_articulo_cientifico_year_user = User.objects.filter(
                    Q(articulo_cientifico_autores__fecha__year=year, articulo_cientifico_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('articulo_cientifico_autores')).aggregate(Min('articulo_cientifico_autores__count'))[
                    'articulo_cientifico_autores__count__min']
                if min_articulo_cientifico_year_user == None:
                    min_articulo_cientifico_year_user = 0
                items_data[i + 1].append(min_articulo_cientifico_year_user)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_articulos_investigacion_publicados = LineChart(data_source)
            context['chart_articulos_investigacion_publicados'] = chart_articulos_investigacion_publicados

            items_data = [
                ['Año', 'Mis artículos de investigación', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_articulos_cientificos_enprensa_year_sum = ArticuloCientifico.objects.filter(fecha__year=year,
                                                                                                  status='EN_PRENSA').filter(
                    ((Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad__year__gt=year)) | (
                        Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad=None)))).count()

                request_user_item_year_sum = ArticuloCientifico.objects.filter(fecha__year=year,
                                                                               status='EN_PRENSA',
                                                                               autores=request.user).count()
                if not request_user_item_year_sum:
                    request_user_item_year_sum = 0
                items_data[i + 1].append(request_user_item_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(articulo_cientifico_autores__fecha__year=year, articulo_cientifico_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(total_articulos_cientificos_enprensa_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(0)

                max_item_year_user = User.objects.filter(
                    Q(articulo_cientifico_autores__fecha__year=year, articulo_cientifico_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('articulo_cientifico_autores')).aggregate(Max('articulo_cientifico_autores__count'))[
                    'articulo_cientifico_autores__count__max']
                if max_item_year_user == None:
                    max_item_year_user = 0
                items_data[i + 1].append(max_item_year_user)

                min_articulo_cientifico_year_user = User.objects.filter(
                    Q(articulo_cientifico_autores__fecha__year=year, articulo_cientifico_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('articulo_cientifico_autores')).aggregate(Min('articulo_cientifico_autores__count'))[
                    'articulo_cientifico_autores__count__min']
                if min_articulo_cientifico_year_user == None:
                    min_articulo_cientifico_year_user = 0
                items_data[i + 1].append(min_articulo_cientifico_year_user)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_articulos_investigacion_enprensa = LineChart(data_source)
            context['chart_articulos_investigacion_enprensa'] = chart_articulos_investigacion_enprensa

            items_data = [
                ['Año', 'Mis artículos de investigación', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = ArticuloCientifico.objects.filter(fecha__year=year,
                                                                         status='ACEPTADO').filter(
                    ((Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad__year__gt=year)) | (
                        Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad=None)))).count()
                request_user_articulo_cientifico_year_sum = ArticuloCientifico.objects.filter(fecha__year=year,
                                                                                              status='ACEPTADO',
                                                                                              autores=request.user).count()
                if not request_user_articulo_cientifico_year_sum:
                    request_user_articulo_cientifico_year_sum = 0
                items_data[i + 1].append(request_user_articulo_cientifico_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(articulo_cientifico_autores__fecha__year=year, articulo_cientifico_autores__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(total_items_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(0)

                max_item_year_user = User.objects.filter(
                    Q(articulo_cientifico_autores__fecha__year=year, articulo_cientifico_autores__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('articulo_cientifico_autores')).aggregate(Max('articulo_cientifico_autores__count'))[
                    'articulo_cientifico_autores__count__max']
                if max_item_year_user == None:
                    max_item_year_user = 0
                items_data[i + 1].append(max_item_year_user)

                min_articulo_cientifico_year_user = User.objects.filter(
                    Q(articulo_cientifico_autores__fecha__year=year, articulo_cientifico_autores__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('articulo_cientifico_autores')).aggregate(Min('articulo_cientifico_autores__count'))[
                    'articulo_cientifico_autores__count__min']
                if min_articulo_cientifico_year_user == None:
                    min_articulo_cientifico_year_user = 0
                items_data[i + 1].append(min_articulo_cientifico_year_user)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_articulos_investigacion_aceptado = LineChart(data_source)
            context['chart_articulos_investigacion_aceptado'] = chart_articulos_investigacion_aceptado

            libros_investigacion_publicado_data = [
                ['Año', 'Mis Libros', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                libros_investigacion_publicado_data.append([str(year)])

                total_libros_cientificos_year_sum = Libro.objects.filter(fecha__year=year, tipo='INVESTIGACION',
                                                                         status='PUBLICADO').filter(
                    ((Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad__year__gt=year)) | (
                        Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad=None)))).count()
                request_user_libro_investigacion_year_sum = Libro.objects.filter(fecha__year=year, tipo='INVESTIGACION',
                                                                                 status='PUBLICADO',
                                                                                 autores=request.user).count()
                if not request_user_libro_investigacion_year_sum:
                    request_user_libro_investigacion_year_sum = 0
                libros_investigacion_publicado_data[i + 1].append(request_user_libro_investigacion_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='INVESTIGACION',
                      libro_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    libros_investigacion_publicado_data[i + 1].append(
                        round(total_libros_cientificos_year_sum / users_with_items_year_count, 2))
                else:
                    libros_investigacion_publicado_data[i + 1].append(0)

                max_libro_investigacion_year_user = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='INVESTIGACION',
                      libro_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Max('libro_autores__count'))[
                    'libro_autores__count__max']
                if max_libro_investigacion_year_user == None:
                    max_libro_investigacion_year_user = 0
                libros_investigacion_publicado_data[i + 1].append(max_libro_investigacion_year_user)

                min_libro_investigacion_year_user = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='INVESTIGACION',
                      libro_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Min('libro_autores__count'))[
                    'libro_autores__count__min']
                if min_libro_investigacion_year_user == None:
                    min_libro_investigacion_year_user = 0
                libros_investigacion_publicado_data[i + 1].append(min_libro_investigacion_year_user)

            # print(libros_investigacion_publicado_data)
            data_source = SimpleDataSource(data=libros_investigacion_publicado_data)
            chart_libros_investigacion_publicado = LineChart(data_source)
            context['chart_libros_investigacion_publicado'] = chart_libros_investigacion_publicado

            libros_investigacion_enprensa_data = [
                ['Año', 'Mis Libros', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                libros_investigacion_enprensa_data.append([str(year)])

                total_libros_cientificos_year_sum = Libro.objects.filter(fecha__year=year, tipo='INVESTIGACION',
                                                                         status='EN_PRENSA').filter(
                    ((Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad__year__gt=year)) | (
                        Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad=None)))).count()
                request_user_libro_investigacion_year_sum = Libro.objects.filter(fecha__year=year, tipo='INVESTIGACION',
                                                                                 status='EN_PRENSA',
                                                                                 autores=request.user).count()
                if not request_user_libro_investigacion_year_sum:
                    request_user_libro_investigacion_year_sum = 0
                libros_investigacion_enprensa_data[i + 1].append(request_user_libro_investigacion_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='INVESTIGACION',
                      libro_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    libros_investigacion_enprensa_data[i + 1].append(
                        round(total_libros_cientificos_year_sum / users_with_items_year_count, 2))
                else:
                    libros_investigacion_enprensa_data[i + 1].append(0)

                max_libro_investigacion_year_user = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='INVESTIGACION',
                      libro_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Max('libro_autores__count'))[
                    'libro_autores__count__max']
                if max_libro_investigacion_year_user == None:
                    max_libro_investigacion_year_user = 0
                libros_investigacion_enprensa_data[i + 1].append(max_libro_investigacion_year_user)

                min_libro_investigacion_year_user = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='INVESTIGACION',
                      libro_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Min('libro_autores__count'))[
                    'libro_autores__count__min']
                if min_libro_investigacion_year_user == None:
                    min_libro_investigacion_year_user = 0
                libros_investigacion_enprensa_data[i + 1].append(min_libro_investigacion_year_user)

            # print(libros_investigacion_enprensa_data)
            data_source = SimpleDataSource(data=libros_investigacion_enprensa_data)
            chart_libros_investigacion_enprensa = LineChart(data_source)
            context['chart_libros_investigacion_enprensa'] = chart_libros_investigacion_enprensa

            libros_investigacion_aceptado_data = [
                ['Año', 'Mis Libros', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                libros_investigacion_aceptado_data.append([str(year)])

                total_libros_cientificos_year_sum = Libro.objects.filter(fecha__year=year, tipo='INVESTIGACION',
                                                                         status='ACEPTADO').filter(
                    ((Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad__year__gt=year)) | (
                        Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad=None)))).count()
                request_user_libro_investigacion_year_sum = Libro.objects.filter(fecha__year=year, tipo='INVESTIGACION',
                                                                                 status='ACEPTADO',
                                                                                 autores=request.user).count()
                if not request_user_libro_investigacion_year_sum:
                    request_user_libro_investigacion_year_sum = 0
                libros_investigacion_aceptado_data[i + 1].append(request_user_libro_investigacion_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='INVESTIGACION',
                      libro_autores__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    libros_investigacion_aceptado_data[i + 1].append(
                        round(total_libros_cientificos_year_sum / users_with_items_year_count, 2))
                else:
                    libros_investigacion_aceptado_data[i + 1].append(0)

                max_libro_investigacion_year_user = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='INVESTIGACION',
                      libro_autores__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Max('libro_autores__count'))[
                    'libro_autores__count__max']
                if max_libro_investigacion_year_user == None:
                    max_libro_investigacion_year_user = 0
                libros_investigacion_aceptado_data[i + 1].append(max_libro_investigacion_year_user)

                min_libro_investigacion_year_user = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='INVESTIGACION',
                      libro_autores__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Min('libro_autores__count'))[
                    'libro_autores__count__min']
                if min_libro_investigacion_year_user == None:
                    min_libro_investigacion_year_user = 0
                libros_investigacion_aceptado_data[i + 1].append(min_libro_investigacion_year_user)

            # print(libros_investigacion_aceptado_data)
            data_source = SimpleDataSource(data=libros_investigacion_aceptado_data)
            chart_libros_investigacion_aceptados = LineChart(data_source)
            context['chart_libros_investigacion_aceptados'] = chart_libros_investigacion_aceptados

            capitulos_libros_investigacion_publicado_data = [
                ['Año', 'Mis Capitulos en libros', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                capitulos_libros_investigacion_publicado_data.append([str(year)])

                total_capitulos_libros_investigacion_year_sum = CapituloLibroInvestigacion.objects.filter(
                    libro__fecha__year=year, libro__tipo='INVESTIGACION',
                    libro__status='PUBLICADO').filter(
                    ((Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad__year__gt=year)) | (
                        Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad=None)))).count()

                request_user_capitulos_libros_investigacion_year_sum = CapituloLibroInvestigacion.objects.filter(
                    libro__fecha__year=year, libro__tipo='INVESTIGACION',
                    libro__status='PUBLICADO',
                    libro__autores=request.user).count()
                if not request_user_capitulos_libros_investigacion_year_sum:
                    request_user_capitulos_libros_investigacion_year_sum = 0
                capitulos_libros_investigacion_publicado_data[i + 1].append(
                    request_user_capitulos_libros_investigacion_year_sum)

                users_with_capitulos_libros_investigacion_year_count = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='INVESTIGACION',
                      capitulo_libro_investigacion_autores__libro__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_capitulos_libros_investigacion_year_count == None:
                    users_with_capitulos_libros_investigacion_year_count = 0
                if users_with_capitulos_libros_investigacion_year_count > 0:
                    capitulos_libros_investigacion_publicado_data[i + 1].append(
                        round(
                            total_capitulos_libros_investigacion_year_sum / users_with_capitulos_libros_investigacion_year_count,
                            2))
                else:
                    capitulos_libros_investigacion_publicado_data[i + 1].append(0)

                max_capitulos_libros_investigacion_year_user = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='INVESTIGACION',
                      capitulo_libro_investigacion_autores__libro__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Max('libro_autores__count'))[
                    'libro_autores__count__max']
                if max_capitulos_libros_investigacion_year_user == None:
                    max_capitulos_libros_investigacion_year_user = 0
                capitulos_libros_investigacion_publicado_data[i + 1].append(
                    max_capitulos_libros_investigacion_year_user)

                min_capitulos_libros_investigacion_year_user = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='INVESTIGACION',
                      capitulo_libro_investigacion_autores__libro__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Min('libro_autores__count'))[
                    'libro_autores__count__min']
                if min_capitulos_libros_investigacion_year_user == None:
                    min_capitulos_libros_investigacion_year_user = 0
                capitulos_libros_investigacion_publicado_data[i + 1].append(
                    min_capitulos_libros_investigacion_year_user)

            # print(capitulos_libros_investigacion_publicado_data)
            data_source = SimpleDataSource(data=capitulos_libros_investigacion_publicado_data)
            chart_capitulos_libros_investigacion_publicado = LineChart(data_source)
            context['chart_capitulos_libros_investigacion_publicado'] = chart_capitulos_libros_investigacion_publicado

            capitulos_libros_investigacion_enprensa_data = [
                ['Año', 'Mis Capitulos en libros', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                capitulos_libros_investigacion_enprensa_data.append([str(year)])

                total_capitulos_libros_investigacion_year_sum = CapituloLibroInvestigacion.objects.filter(
                    libro__fecha__year=year, libro__tipo='INVESTIGACION',
                    libro__status='EN_PRENSA').filter(
                    ((Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad__year__gt=year)) | (
                        Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad=None)))).count()

                request_user_capitulos_libros_investigacion_year_sum = CapituloLibroInvestigacion.objects.filter(
                    libro__fecha__year=year, libro__tipo='INVESTIGACION',
                    libro__status='EN_PRENSA',
                    libro__autores=request.user).count()
                if not request_user_capitulos_libros_investigacion_year_sum:
                    request_user_capitulos_libros_investigacion_year_sum = 0
                capitulos_libros_investigacion_enprensa_data[i + 1].append(
                    request_user_capitulos_libros_investigacion_year_sum)

                users_with_capitulos_libros_investigacion_year_count = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='INVESTIGACION',
                      capitulo_libro_investigacion_autores__libro__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_capitulos_libros_investigacion_year_count == None:
                    users_with_capitulos_libros_investigacion_year_count = 0
                if users_with_capitulos_libros_investigacion_year_count > 0:
                    capitulos_libros_investigacion_enprensa_data[i + 1].append(
                        round(
                            total_capitulos_libros_investigacion_year_sum / users_with_capitulos_libros_investigacion_year_count,
                            2))
                else:
                    capitulos_libros_investigacion_enprensa_data[i + 1].append(0)

                max_capitulos_libros_investigacion_year_user = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='INVESTIGACION',
                      capitulo_libro_investigacion_autores__libro__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Max('libro_autores__count'))[
                    'libro_autores__count__max']
                if max_capitulos_libros_investigacion_year_user == None:
                    max_capitulos_libros_investigacion_year_user = 0
                capitulos_libros_investigacion_enprensa_data[i + 1].append(
                    max_capitulos_libros_investigacion_year_user)

                min_capitulos_libros_investigacion_year_user = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='INVESTIGACION',
                      capitulo_libro_investigacion_autores__libro__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Min('libro_autores__count'))[
                    'libro_autores__count__min']
                if min_capitulos_libros_investigacion_year_user == None:
                    min_capitulos_libros_investigacion_year_user = 0
                capitulos_libros_investigacion_enprensa_data[i + 1].append(
                    min_capitulos_libros_investigacion_year_user)

            # print(capitulos_libros_investigacion_enprensa_data)
            data_source = SimpleDataSource(data=capitulos_libros_investigacion_enprensa_data)
            chart_capitulos_libros_investigacion_enprensa = LineChart(data_source)
            context['chart_capitulos_libros_investigacion_enprensa'] = chart_capitulos_libros_investigacion_enprensa

            capitulos_libros_investigacion_aceptado_data = [
                ['Año', 'Mis Capitulos en libros', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                capitulos_libros_investigacion_aceptado_data.append([str(year)])

                total_capitulos_libros_investigacion_year_sum = CapituloLibroInvestigacion.objects.filter(
                    libro__fecha__year=year, libro__tipo='INVESTIGACION',
                    libro__status='ACEPTADO').filter(
                    ((Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad__year__gt=year)) | (
                        Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad=None)))).count()

                request_user_capitulos_libros_investigacion_year_sum = CapituloLibroInvestigacion.objects.filter(
                    libro__fecha__year=year, libro__tipo='INVESTIGACION',
                    libro__status='ACEPTADO',
                    libro__autores=request.user).count()
                if not request_user_capitulos_libros_investigacion_year_sum:
                    request_user_capitulos_libros_investigacion_year_sum = 0
                capitulos_libros_investigacion_aceptado_data[i + 1].append(
                    request_user_capitulos_libros_investigacion_year_sum)

                users_with_capitulos_libros_investigacion_year_count = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='INVESTIGACION',
                      capitulo_libro_investigacion_autores__libro__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_capitulos_libros_investigacion_year_count == None:
                    users_with_capitulos_libros_investigacion_year_count = 0
                if users_with_capitulos_libros_investigacion_year_count > 0:
                    capitulos_libros_investigacion_aceptado_data[i + 1].append(
                        round(
                            total_capitulos_libros_investigacion_year_sum / users_with_capitulos_libros_investigacion_year_count,
                            2))
                else:
                    capitulos_libros_investigacion_aceptado_data[i + 1].append(0)

                max_capitulos_libros_investigacion_year_user = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='INVESTIGACION',
                      capitulo_libro_investigacion_autores__libro__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Max('libro_autores__count'))[
                    'libro_autores__count__max']
                if max_capitulos_libros_investigacion_year_user == None:
                    max_capitulos_libros_investigacion_year_user = 0
                capitulos_libros_investigacion_aceptado_data[i + 1].append(
                    max_capitulos_libros_investigacion_year_user)

                min_capitulos_libros_investigacion_year_user = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='INVESTIGACION',
                      capitulo_libro_investigacion_autores__libro__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Min('libro_autores__count'))[
                    'libro_autores__count__min']
                if min_capitulos_libros_investigacion_year_user == None:
                    min_capitulos_libros_investigacion_year_user = 0
                capitulos_libros_investigacion_aceptado_data[i + 1].append(
                    min_capitulos_libros_investigacion_year_user)

            # print(capitulos_libros_investigacion_aceptado_data)
            data_source = SimpleDataSource(data=capitulos_libros_investigacion_aceptado_data)
            chart_capitulos_libros_investigacion_aceptado = LineChart(data_source)
            context['chart_capitulos_libros_investigacion_aceptado'] = chart_capitulos_libros_investigacion_aceptado

            items_data = [
                ['Año', 'Mis Mapas', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = MapaArbitrado.objects.filter(fecha__year=year,
                                                                    status='PUBLICADO').filter(
                    ((Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad__year__gt=year)) | (
                        Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad=None)))).count()

                request_user_items_year_sum = MapaArbitrado.objects.filter(fecha__year=year,
                                                                           status='PUBLICADO',
                                                                           autores=request.user).count()
                if not request_user_items_year_sum:
                    request_user_items_year_sum = 0
                items_data[i + 1].append(request_user_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(mapa_arbitrado_autores__fecha__year=year, mapa_arbitrado_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0

                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(total_items_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(0)

                max_items_year_user = User.objects.filter(
                    Q(mapa_arbitrado_autores__fecha__year=year, mapa_arbitrado_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('mapa_arbitrado_autores')).aggregate(Max('mapa_arbitrado_autores__count'))[
                    'mapa_arbitrado_autores__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(mapa_arbitrado_autores__fecha__year=year, mapa_arbitrado_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('mapa_arbitrado_autores')).aggregate(Min('mapa_arbitrado_autores__count'))[
                    'mapa_arbitrado_autores__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(min_items_year_user)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_mapas_arbitrados_publicados = LineChart(data_source)
            context['chart_mapas_arbitrados_publicados'] = chart_mapas_arbitrados_publicados

            items_data = [
                ['Año', 'Mis Mapas', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = MapaArbitrado.objects.filter(fecha__year=year,
                                                                    status='EN_PRENSA').filter(
                    ((Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad__year__gt=year)) | (
                        Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad=None)))).count()

                request_user_items_year_sum = MapaArbitrado.objects.filter(fecha__year=year,
                                                                           status='EN_PRENSA',
                                                                           autores=request.user).count()
                if not request_user_items_year_sum:
                    request_user_items_year_sum = 0
                items_data[i + 1].append(request_user_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(mapa_arbitrado_autores__fecha__year=year, mapa_arbitrado_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0

                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(total_items_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(0)

                max_items_year_user = User.objects.filter(
                    Q(mapa_arbitrado_autores__fecha__year=year, mapa_arbitrado_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('mapa_arbitrado_autores')).aggregate(Max('mapa_arbitrado_autores__count'))[
                    'mapa_arbitrado_autores__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(mapa_arbitrado_autores__fecha__year=year, mapa_arbitrado_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('mapa_arbitrado_autores')).aggregate(Min('mapa_arbitrado_autores__count'))[
                    'mapa_arbitrado_autores__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(min_items_year_user)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_mapas_arbitrados_enprensa = LineChart(data_source)
            context['chart_mapas_arbitrados_enprensa'] = chart_mapas_arbitrados_enprensa

            items_data = [
                ['Año', 'Mis Mapas', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = MapaArbitrado.objects.filter(fecha__year=year,
                                                                    status='ACEPTADO').filter(
                    ((Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad__year__gt=year)) | (
                        Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad=None)))).count()

                request_user_items_year_sum = MapaArbitrado.objects.filter(fecha__year=year,
                                                                           status='ACEPTADO',
                                                                           autores=request.user).count()
                if not request_user_items_year_sum:
                    request_user_items_year_sum = 0
                items_data[i + 1].append(request_user_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(mapa_arbitrado_autores__fecha__year=year, mapa_arbitrado_autores__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0

                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(total_items_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(0)

                max_items_year_user = User.objects.filter(
                    Q(mapa_arbitrado_autores__fecha__year=year, mapa_arbitrado_autores__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('mapa_arbitrado_autores')).aggregate(Max('mapa_arbitrado_autores__count'))[
                    'mapa_arbitrado_autores__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(mapa_arbitrado_autores__fecha__year=year, mapa_arbitrado_autores__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('mapa_arbitrado_autores')).aggregate(Min('mapa_arbitrado_autores__count'))[
                    'mapa_arbitrado_autores__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(min_items_year_user)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_mapas_arbitrados_aceptados = LineChart(data_source)
            context['chart_mapas_arbitrados_aceptados'] = chart_mapas_arbitrados_aceptados

            items_data = [
                ['Año', 'Mis Informes Técnicos', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = PublicacionTecnica.objects.filter(fecha__year=year).filter(
                    ((Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad__year__gt=year)) | (
                        Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad=None)))).count()

                request_user_items_year_sum = PublicacionTecnica.objects.filter(fecha__year=year,
                                                                                autores=request.user).count()
                if not request_user_items_year_sum:
                    request_user_items_year_sum = 0
                items_data[i + 1].append(request_user_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(informe_tecnico_autores__fecha__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0

                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(total_items_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(0)

                max_items_year_user = User.objects.filter(
                    Q(informe_tecnico_autores__fecha__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('informe_tecnico_autores')).aggregate(Max('informe_tecnico_autores__count'))[
                    'informe_tecnico_autores__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(informe_tecnico_autores__fecha__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('informe_tecnico_autores')).aggregate(Min('informe_tecnico_autores__count'))[
                    'informe_tecnico_autores__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(min_items_year_user)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_informes_tecnicos = LineChart(data_source)
            context['chart_informes_tecnicos'] = chart_informes_tecnicos

            items_data = [
                ['Año', 'Mis Proyectos de investigación', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = ProyectoInvestigacion.objects.filter(
                    (Q(fecha_inicio__year__lte=year) & Q(fecha_fin__year__gt=year))
                    | (Q(fecha_inicio__year__lte=year) & Q(fecha_fin=None))).filter(
                    (Q(responsables__ingreso_entidad__year__lte=year) & Q(responsables__egreso_entidad__year__gt=year))
                    | (Q(responsables__ingreso_entidad__year__lte=year) & Q(responsables__egreso_entidad=None))).count()

                request_user_items_year_sum = ProyectoInvestigacion.objects.filter(responsables=request.user).filter(
                    (Q(fecha_inicio__year__lte=year) & Q(fecha_fin__year__gt=year))
                    | (Q(fecha_inicio__year__lte=year) & Q(fecha_fin=None))).count()
                if not request_user_items_year_sum:
                    request_user_items_year_sum = 0
                items_data[i + 1].append(request_user_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    (Q(proyecto_investigacion_responsables__fecha_inicio__year__lte=year) & Q(
                        proyecto_investigacion_responsables__fecha_fin__year__gt=year))
                    | (Q(proyecto_investigacion_responsables__fecha_inicio__year__lte=year) & Q(
                        proyecto_investigacion_responsables__fecha_fin=None))).filter(
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0

                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(total_items_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(0)

                max_items_year_user = User.objects.filter(
                    (Q(proyecto_investigacion_responsables__fecha_inicio__year__lte=year) & Q(
                        proyecto_investigacion_responsables__fecha_fin__year__gt=year))
                    | (Q(proyecto_investigacion_responsables__fecha_inicio__year__lte=year) & Q(
                        proyecto_investigacion_responsables__fecha_fin=None))
                ).filter(((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                          (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('proyecto_investigacion_responsables')).aggregate(
                    Max('proyecto_investigacion_responsables__count'))[
                    'proyecto_investigacion_responsables__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(max_items_year_user)

                min_items_year_user = User.objects.filter(
                    (Q(proyecto_investigacion_responsables__fecha_inicio__year__lte=year) & Q(
                        proyecto_investigacion_responsables__fecha_fin__year__gt=year))
                    | (Q(proyecto_investigacion_responsables__fecha_inicio__year__lte=year) & Q(
                        proyecto_investigacion_responsables__fecha_fin=None))
                ).filter(((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                          (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('proyecto_investigacion_responsables')).aggregate(
                    Min('proyecto_investigacion_responsables__count'))[
                    'proyecto_investigacion_responsables__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(min_items_year_user)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_proyectos_investigacion = LineChart(data_source)
            context['chart_proyectos_investigacion'] = chart_proyectos_investigacion

            items_data = [
                ['Año', 'Mis Reseñas', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = Resena.objects.filter(fecha__year=year).filter(
                    ((Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad__year__gt=year)) |
                     (Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad=None)))).count()

                request_user_items_year_sum = Resena.objects.filter(fecha__year=year, autores=request.user).count()
                if not request_user_items_year_sum:
                    request_user_items_year_sum = 0
                items_data[i + 1].append(
                    request_user_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(resena_autores__fecha__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(
                            total_items_year_sum / users_with_items_year_count,
                            2))
                else:
                    items_data[i + 1].append(0)

                max_items_year_user = User.objects.filter(
                    Q(resena_autores__fecha__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('resena_autores')).aggregate(Max('resena_autores__count'))[
                    'resena_autores__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(
                    max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(resena_autores__fecha__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('resena_autores')).aggregate(Min('resena_autores__count'))[
                    'resena_autores__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(
                    min_items_year_user)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_resena = LineChart(data_source)
            context['chart_resena'] = chart_resena



            items_data = [
                ['Año', 'Mis Participaciones en eventos académicos', 'Promedio por persona', 'Max por persona',
                 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = ParticipacionEventoAcademico.objects.filter(
                    evento__fecha_inicio__year=year).filter(
                    ((Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad__year__gt=year)) |
                     (Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad=None)))).count()

                request_user_items_year_sum = ParticipacionEventoAcademico.objects.filter(
                    evento__fecha_inicio__year=year,
                    autores=request.user).count()
                if not request_user_items_year_sum:
                    request_user_items_year_sum = 0
                items_data[i + 1].append(
                    request_user_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(participacion_evento_academico_autores__evento__fecha_inicio__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(total_items_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(0)

                max_items_year_user = User.objects.filter(
                    Q(participacion_evento_academico_autores__evento__fecha_inicio__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('participacion_evento_academico_autores')).aggregate(Max('participacion_evento_academico_autores__count'))[
                    'participacion_evento_academico_autores__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(
                    max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(participacion_evento_academico_autores__evento__fecha_inicio__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('participacion_evento_academico_autores')).aggregate(Min('participacion_evento_academico_autores__count'))[
                    'participacion_evento_academico_autores__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(
                    min_items_year_user)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_participacioneventoacademico = LineChart(data_source)
            context['chart_participacioneventoacademico'] = chart_participacioneventoacademico

            items_data = [
                ['Año', 'Mis artículos de divulgación', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = ArticuloDivulgacion.objects.filter(fecha__year=year, status='PUBLICADO').filter(
                    ((Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad__year__gt=year)) | (
                        Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad=None)))).count()

                request_user_item_year_sum = ArticuloDivulgacion.objects.filter(fecha__year=year, status='PUBLICADO',
                                                                                autores=request.user).count()
                if not request_user_item_year_sum:
                    request_user_item_year_sum = 0
                items_data[i + 1].append(request_user_item_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(articulo_divulgacion_autores__fecha__year=year,
                      articulo_divulgacion_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0

                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(total_items_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(0)

                max_item_year_user = User.objects.filter(
                    Q(articulo_divulgacion_autores__fecha__year=year,
                      articulo_divulgacion_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('articulo_divulgacion_autores')).aggregate(Max('articulo_divulgacion_autores__count'))[
                    'articulo_divulgacion_autores__count__max']
                if max_item_year_user == None:
                    max_item_year_user = 0
                items_data[i + 1].append(max_item_year_user)

                min_articulo_cientifico_year_user = User.objects.filter(
                    Q(articulo_divulgacion_autores__fecha__year=year,
                      articulo_divulgacion_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('articulo_divulgacion_autores')).aggregate(Min('articulo_divulgacion_autores__count'))[
                    'articulo_divulgacion_autores__count__min']
                if min_articulo_cientifico_year_user == None:
                    min_articulo_cientifico_year_user = 0
                items_data[i + 1].append(min_articulo_cientifico_year_user)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_articulo_divulgacion_publicados = LineChart(data_source)
            context['chart_articulo_divulgacion_publicados'] = chart_articulo_divulgacion_publicados

            items_data = [
                ['Año', 'Mis artículos de divulgación', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = ArticuloDivulgacion.objects.filter(fecha__year=year,
                                                                          status='EN_PRENSA').filter(
                    ((Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad__year__gt=year)) | (
                        Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad=None)))).count()

                request_user_item_year_sum = ArticuloDivulgacion.objects.filter(fecha__year=year,
                                                                                status='EN_PRENSA',
                                                                                autores=request.user).count()
                if not request_user_item_year_sum:
                    request_user_item_year_sum = 0
                items_data[i + 1].append(request_user_item_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(articulo_divulgacion_autores__fecha__year=year,
                      articulo_divulgacion_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(total_items_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(0)

                max_item_year_user = User.objects.filter(
                    Q(articulo_divulgacion_autores__fecha__year=year,
                      articulo_divulgacion_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('articulo_divulgacion_autores')).aggregate(Max('articulo_divulgacion_autores__count'))[
                    'articulo_divulgacion_autores__count__max']
                if max_item_year_user == None:
                    max_item_year_user = 0
                items_data[i + 1].append(max_item_year_user)

                min_articulo_cientifico_year_user = User.objects.filter(
                    Q(articulo_divulgacion_autores__fecha__year=year,
                      articulo_divulgacion_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('articulo_divulgacion_autores')).aggregate(Min('articulo_divulgacion_autores__count'))[
                    'articulo_divulgacion_autores__count__min']
                if min_articulo_cientifico_year_user == None:
                    min_articulo_cientifico_year_user = 0
                items_data[i + 1].append(min_articulo_cientifico_year_user)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_articulo_divulgacion_enprensa = LineChart(data_source)
            context['chart_articulo_divulgacion_enprensa'] = chart_articulo_divulgacion_enprensa

            items_data = [
                ['Año', 'Mis artículos de divulgación', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = ArticuloDivulgacion.objects.filter(fecha__year=year,
                                                                          status='ACEPTADO').filter(
                    ((Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad__year__gt=year)) | (
                        Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad=None)))).count()
                request_user_items_year_sum = ArticuloDivulgacion.objects.filter(fecha__year=year,
                                                                                 status='ACEPTADO',
                                                                                 autores=request.user).count()
                if not request_user_items_year_sum:
                    request_user_items_year_sum = 0
                items_data[i + 1].append(request_user_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(articulo_divulgacion_autores__fecha__year=year, articulo_divulgacion_autores__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(total_items_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(0)

                max_item_year_user = User.objects.filter(
                    Q(articulo_divulgacion_autores__fecha__year=year, articulo_divulgacion_autores__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('articulo_divulgacion_autores')).aggregate(Max('articulo_divulgacion_autores__count'))[
                    'articulo_divulgacion_autores__count__max']
                if max_item_year_user == None:
                    max_item_year_user = 0
                items_data[i + 1].append(max_item_year_user)

                min_articulo_cientifico_year_user = User.objects.filter(
                    Q(articulo_divulgacion_autores__fecha__year=year, articulo_divulgacion_autores__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('articulo_divulgacion_autores')).aggregate(Min('articulo_divulgacion_autores__count'))[
                    'articulo_divulgacion_autores__count__min']
                if min_articulo_cientifico_year_user == None:
                    min_articulo_cientifico_year_user = 0
                items_data[i + 1].append(min_articulo_cientifico_year_user)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_articulo_divulgacion_aceptados = LineChart(data_source)
            context['chart_articulo_divulgacion_aceptados'] = chart_articulo_divulgacion_aceptados

            items_data = [
                ['Año', 'Mis Libros de divulgación', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = Libro.objects.filter(fecha__year=year, tipo='DIVULGACION',
                                                            status='PUBLICADO').filter(
                    ((Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad__year__gt=year)) | (
                        Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad=None)))).count()
                request_user_items_year_sum = Libro.objects.filter(fecha__year=year, tipo='DIVULGACION',
                                                                   status='PUBLICADO',
                                                                   autores=request.user).count()
                if not request_user_items_year_sum:
                    request_user_items_year_sum = 0
                items_data[i + 1].append(request_user_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='DIVULGACION',
                      libro_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(total_items_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(0)

                max_items_year_user = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='DIVULGACION',
                      libro_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Max('libro_autores__count'))[
                    'libro_autores__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='DIVULGACION',
                      libro_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Min('libro_autores__count'))[
                    'libro_autores__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(min_items_year_user)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_libros_divulgacion_publicados = LineChart(data_source)
            context['chart_libros_divulgacion_publicados'] = chart_libros_divulgacion_publicados

            items_data = [
                ['Año', 'Mis Libros de divulgación', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = Libro.objects.filter(fecha__year=year, tipo='DIVULGACION',
                                                            status='EN_PRENSA').filter(
                    ((Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad__year__gt=year)) | (
                        Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad=None)))).count()
                request_user_items_year_sum = Libro.objects.filter(fecha__year=year, tipo='DIVULGACION',
                                                                   status='EN_PRENSA',
                                                                   autores=request.user).count()
                if not request_user_items_year_sum:
                    request_user_items_year_sum = 0
                items_data[i + 1].append(request_user_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='DIVULGACION',
                      libro_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(total_items_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(0)

                max_items_year_user = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='DIVULGACION',
                      libro_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Max('libro_autores__count'))[
                    'libro_autores__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='DIVULGACION',
                      libro_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Min('libro_autores__count'))[
                    'libro_autores__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(min_items_year_user)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_libros_divulgacion_enprensa = LineChart(data_source)
            context['chart_libros_divulgacion_enprensa'] = chart_libros_divulgacion_enprensa

            libros_investigacion_aceptado_data = [
                ['Año', 'Mis Libros de divulgación', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                libros_investigacion_aceptado_data.append([str(year)])

                total_items_year_sum = Libro.objects.filter(fecha__year=year, tipo='DIVULGACION',
                                                            status='ACEPTADO').filter(
                    ((Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad__year__gt=year)) | (
                        Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad=None)))).count()
                request_user_items_year_sum = Libro.objects.filter(fecha__year=year, tipo='DIVULGACION',
                                                                   status='ACEPTADO',
                                                                   autores=request.user).count()
                if not request_user_items_year_sum:
                    request_user_items_year_sum = 0
                libros_investigacion_aceptado_data[i + 1].append(request_user_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='DIVULGACION',
                      libro_autores__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    libros_investigacion_aceptado_data[i + 1].append(
                        round(total_items_year_sum / users_with_items_year_count, 2))
                else:
                    libros_investigacion_aceptado_data[i + 1].append(0)

                max_items_year_user = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='DIVULGACION',
                      libro_autores__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Max('libro_autores__count'))[
                    'libro_autores__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                libros_investigacion_aceptado_data[i + 1].append(max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='DIVULGACION',
                      libro_autores__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Min('libro_autores__count'))[
                    'libro_autores__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                libros_investigacion_aceptado_data[i + 1].append(min_items_year_user)

            # print(libros_investigacion_aceptado_data)
            data_source = SimpleDataSource(data=libros_investigacion_aceptado_data)
            chart_libros_divulgacion_aceptados = LineChart(data_source)
            context['chart_libros_divulgacion_aceptados'] = chart_libros_divulgacion_aceptados

            items_data = [
                ['Año', 'Mis Capitulos en libros de divulgación', 'Promedio por persona', 'Max por persona',
                 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = CapituloLibroDivulgacion.objects.filter(
                    libro__fecha__year=year, libro__tipo='DIVULGACION',
                    libro__status='PUBLICADO').filter(
                    ((Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) | (
                        Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).count()

                request_user_items_year_sum = CapituloLibroDivulgacion.objects.filter(
                    libro__fecha__year=year, libro__tipo='DIVULGACION',
                    libro__status='PUBLICADO',
                    libro__autores=request.user).count()
                if not request_user_items_year_sum:
                    request_user_items_year_sum = 0
                items_data[i + 1].append(
                    request_user_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='DIVULGACION',
                      capitulo_libro_investigacion_autores__libro__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(
                            total_items_year_sum / users_with_items_year_count,
                            2))
                else:
                    items_data[i + 1].append(0)

                max_items_year_user = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='DIVULGACION',
                      capitulo_libro_investigacion_autores__libro__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Max('libro_autores__count'))[
                    'libro_autores__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(
                    max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='DIVULGACION',
                      capitulo_libro_investigacion_autores__libro__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Min('libro_autores__count'))[
                    'libro_autores__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(
                    min_items_year_user)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_capitulos_libros_divulgacion_publicados = LineChart(data_source)
            context['chart_capitulos_libros_divulgacion_publicados'] = chart_capitulos_libros_divulgacion_publicados

            capitulos_libros_investigacion_enprensa_data = [
                ['Año', 'Mis Capitulos en libros de divulgación', 'Promedio por persona', 'Max por persona',
                 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                capitulos_libros_investigacion_enprensa_data.append([str(year)])

                total_items_year_sum = CapituloLibroDivulgacion.objects.filter(
                    libro__fecha__year=year, libro__tipo='DIVULGACION',
                    libro__status='EN_PRENSA').filter(
                    ((Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) | (
                        Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).count()

                request_user_items_year_sum = CapituloLibroDivulgacion.objects.filter(
                    libro__fecha__year=year, libro__tipo='DIVULGACION',
                    libro__status='EN_PRENSA',
                    libro__autores=request.user).count()
                if not request_user_items_year_sum:
                    request_user_items_year_sum = 0
                capitulos_libros_investigacion_enprensa_data[i + 1].append(
                    request_user_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='DIVULGACION',
                      capitulo_libro_investigacion_autores__libro__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    capitulos_libros_investigacion_enprensa_data[i + 1].append(
                        round(
                            total_items_year_sum / users_with_items_year_count,
                            2))
                else:
                    capitulos_libros_investigacion_enprensa_data[i + 1].append(0)

                max_items_year_user = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='DIVULGACION',
                      capitulo_libro_investigacion_autores__libro__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Max('libro_autores__count'))[
                    'libro_autores__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                capitulos_libros_investigacion_enprensa_data[i + 1].append(
                    max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='DIVULGACION',
                      capitulo_libro_investigacion_autores__libro__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Min('libro_autores__count'))[
                    'libro_autores__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                capitulos_libros_investigacion_enprensa_data[i + 1].append(
                    min_items_year_user)

            # print(capitulos_libros_investigacion_enprensa_data)
            data_source = SimpleDataSource(data=capitulos_libros_investigacion_enprensa_data)
            chart_capitulos_libros_divulgacion_enprensa = LineChart(data_source)
            context['chart_capitulos_libros_divulgacion_enprensa'] = chart_capitulos_libros_divulgacion_enprensa

            items_data = [
                ['Año', 'Mis Capitulos en libros de divulgación', 'Promedio por persona', 'Max por persona',
                 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = CapituloLibroDivulgacion.objects.filter(
                    libro__fecha__year=year, libro__tipo='DIVULGACION',
                    libro__status='ACEPTADO').filter(
                    ((Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) | (
                        Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).count()

                request_user_items_year_sum = CapituloLibroDivulgacion.objects.filter(
                    libro__fecha__year=year, libro__tipo='DIVULGACION',
                    libro__status='ACEPTADO',
                    libro__autores=request.user).count()
                if not request_user_items_year_sum:
                    request_user_items_year_sum = 0
                items_data[i + 1].append(
                    request_user_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='DIVULGACION',
                      capitulo_libro_investigacion_autores__libro__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(
                            total_items_year_sum / users_with_items_year_count,
                            2))
                else:
                    items_data[i + 1].append(0)

                max_items_year_user = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='DIVULGACION',
                      capitulo_libro_investigacion_autores__libro__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Max('libro_autores__count'))[
                    'libro_autores__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(
                    max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='DIVULGACION',
                      capitulo_libro_investigacion_autores__libro__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Min('libro_autores__count'))[
                    'libro_autores__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(
                    min_items_year_user)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_capitulos_libros_divulgacion_aceptados = LineChart(data_source)
            context['chart_capitulos_libros_divulgacion_aceptados'] = chart_capitulos_libros_divulgacion_aceptados


            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_organizacioneventodivulgacion = LineChart(data_source)
            context['chart_organizacioneventodivulgacion'] = chart_organizacioneventodivulgacion

            items_data = [
                ['Año', 'Mis Participaciones en eventos de divulgación', 'Promedio por persona', 'Max por persona',
                 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = ParticipacionEventoDivulgacion.objects.filter(
                    evento__fecha_inicio__year=year).filter(
                    ((Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad__year__gt=year)) |
                     (Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad=None)))).count()

                request_user_items_year_sum = ParticipacionEventoDivulgacion.objects.filter(
                    evento__fecha_inicio__year=year,
                    autores=request.user).count()
                if not request_user_items_year_sum:
                    request_user_items_year_sum = 0
                items_data[i + 1].append(
                    request_user_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(participacion_evento_divulgacion_autores__evento__fecha_inicio__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(total_items_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(0)

                max_items_year_user = User.objects.filter(
                    Q(participacion_evento_divulgacion_autores__evento__fecha_inicio__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('participacion_evento_divulgacion_autores')).aggregate(Max('participacion_evento_divulgacion_autores__count'))[
                    'participacion_evento_divulgacion_autores__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(
                    max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(participacion_evento_divulgacion_autores__evento__fecha_inicio__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('participacion_evento_divulgacion_autores')).aggregate(Min('participacion_evento_divulgacion_autores__count'))[
                    'participacion_evento_divulgacion_autores__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(
                    min_items_year_user)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_participacioneventodivulgacion = LineChart(data_source)
            context['chart_participacioneventodivulgacion'] = chart_participacioneventodivulgacion

            items_data = [
                ['Año', 'Mis Participaciones en Programas de Radio, Television, Internet, etc.', 'Promedio por persona',
                 'Max por persona',
                 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = ProgramaRadioTelevisionInternet.objects.filter(fecha__year=year).filter(
                    ((Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) |
                     (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).count()

                request_user_items_year_sum = ProgramaRadioTelevisionInternet.objects.filter(fecha__year=year,
                                                                                             usuario=request.user).count()
                if not request_user_items_year_sum:
                    request_user_items_year_sum = 0
                items_data[i + 1].append(
                    request_user_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(programaradiotelevisioninternet__fecha__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(total_items_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(0)

                max_items_year_user = User.objects.filter(
                    Q(programaradiotelevisioninternet__fecha__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('programaradiotelevisioninternet')).aggregate(Max('programaradiotelevisioninternet__count'))[
                    'programaradiotelevisioninternet__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(
                    max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(programaradiotelevisioninternet__fecha__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('programaradiotelevisioninternet')).aggregate(Min('programaradiotelevisioninternet__count'))[
                    'programaradiotelevisioninternet__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(
                    min_items_year_user)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_programaradiotelevisioninternet = LineChart(data_source)
            context['chart_programaradiotelevisioninternet'] = chart_programaradiotelevisioninternet

            items_data = [
                ['Año', 'Mis Arbitrajes de Publicaciones Academicas', 'Promedio por persona', 'Max por persona',
                 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = ArbitrajePublicacionAcademica.objects.filter(fecha_dictamen__year=year).filter(
                    ((Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) |
                     (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).count()

                request_user_items_year_sum = ArbitrajePublicacionAcademica.objects.filter(fecha_dictamen__year=year,
                                                                                           usuario=request.user).count()
                if not request_user_items_year_sum:
                    request_user_items_year_sum = 0
                items_data[i + 1].append(
                    request_user_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(arbitrajepublicacionacademica__fecha_dictamen__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(total_items_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(0)

                max_items_year_user = User.objects.filter(
                    Q(arbitrajepublicacionacademica__fecha_dictamen__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('arbitrajepublicacionacademica')).aggregate(Max('arbitrajepublicacionacademica__count'))[
                    'arbitrajepublicacionacademica__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(
                    max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(arbitrajepublicacionacademica__fecha_dictamen__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('arbitrajepublicacionacademica')).aggregate(Min('arbitrajepublicacionacademica__count'))[
                    'arbitrajepublicacionacademica__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(
                    min_items_year_user)


            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_arbitrajeproyectoinvestigacion = LineChart(data_source)
            context['chart_arbitrajeproyectoinvestigacion'] = chart_arbitrajeproyectoinvestigacion

            items_data = [['Año', 'Mis horas de docencia escolarizada', 'Promedio horas', 'Max horas', 'Min horas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(last_x_years[i])])

                users_with_items_year_count = User.objects.filter(
                    Q(curso_docencia_escolarizado_usuario__fecha_inicio__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0

                total_hours_year_sum = \
                    CursoDocenciaEscolarizado.objects.filter(fecha_inicio__year=year).filter((
                        (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) |
                        (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).aggregate(
                        Sum('total_horas'))[
                        'total_horas__sum']
                if total_hours_year_sum == None:
                    total_hours_year_sum = 0

                request_user_years_year_sum = User.objects.filter(curso_docencia_escolarizado_usuario__fecha_inicio__year=year,
                                                                  curso_docencia_escolarizado_usuario__usuario=request.user).aggregate(
                    Sum('curso_docencia_escolarizado_usuario__total_horas'))['curso_docencia_escolarizado_usuario__total_horas__sum']
                if not request_user_years_year_sum:
                    request_user_years_year_sum = 0
                items_data[i + 1].append(request_user_years_year_sum)

                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(round(total_hours_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(round(0, 2))

                max_item_year_user = User.objects.filter(curso_docencia_escolarizado_usuario__fecha_inicio__year=year).annotate(
                    Sum('curso_docencia_escolarizado_usuario__total_horas')).filter((
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).aggregate(
                    Max('curso_docencia_escolarizado_usuario__total_horas__sum'))[
                    'curso_docencia_escolarizado_usuario__total_horas__sum__max']
                if max_item_year_user == None:
                    max_item_year_user = 0
                items_data[i + 1].append(max_item_year_user)

                min_item_year_user = User.objects.filter(curso_docencia_escolarizado_usuario__fecha_inicio__year=year).annotate(
                    Sum('curso_docencia_escolarizado_usuario__total_horas')).filter((
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).aggregate(
                    Min('curso_docencia_escolarizado_usuario__total_horas__sum'))[
                    'curso_docencia_escolarizado_usuario__total_horas__sum__min']
                if not min_item_year_user:
                    min_item_year_user = 0
                items_data[i + 1].append(min_item_year_user)

            data_source = SimpleDataSource(data=items_data)
            chart_cursodocencia_escolarizado = LineChart(data_source)
            context['chart_cursodocencia_escolarizado'] = chart_cursodocencia_escolarizado

            items_data = [['Año', 'Mis horas de docencia extracurricular', 'Promedio horas', 'Max horas', 'Min horas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(last_x_years[i])])

                users_with_items_year_count = User.objects.filter(
                    Q(curso_docencia_extracurricular_usuario__fecha_inicio__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0

                total_hours_year_sum = \
                    CursoDocenciaExtracurricular.objects.filter(fecha_inicio__year=year).filter((
                        (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) |
                        (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).aggregate(
                        Sum('total_horas'))[
                        'total_horas__sum']
                if total_hours_year_sum == None:
                    total_hours_year_sum = 0

                request_user_years_year_sum = User.objects.filter(curso_docencia_extracurricular_usuario__fecha_inicio__year=year,
                                                                  curso_docencia_extracurricular_usuario__usuario=request.user).aggregate(
                    Sum('curso_docencia_extracurricular_usuario__total_horas'))['curso_docencia_extracurricular_usuario__total_horas__sum']
                if not request_user_years_year_sum:
                    request_user_years_year_sum = 0
                items_data[i + 1].append(request_user_years_year_sum)

                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(round(total_hours_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(round(0, 2))

                max_item_year_user = User.objects.filter(curso_docencia_extracurricular_usuario__fecha_inicio__year=year).annotate(
                    Sum('curso_docencia_extracurricular_usuario__total_horas')).filter((
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).aggregate(
                    Max('curso_docencia_extracurricular_usuario__total_horas__sum'))[
                    'curso_docencia_extracurricular_usuario__total_horas__sum__max']
                if max_item_year_user == None:
                    max_item_year_user = 0
                items_data[i + 1].append(max_item_year_user)

                min_item_year_user = User.objects.filter(curso_docencia_extracurricular_usuario__fecha_inicio__year=year).annotate(
                    Sum('curso_docencia_extracurricular_usuario__total_horas')).filter((
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).aggregate(
                    Min('curso_docencia_extracurricular_usuario__total_horas__sum'))[
                    'curso_docencia_extracurricular_usuario__total_horas__sum__min']
                if not min_item_year_user:
                    min_item_year_user = 0
                items_data[i + 1].append(min_item_year_user)

            data_source = SimpleDataSource(data=items_data)
            chart_cursodocencia_extracurricular = LineChart(data_source)
            context['chart_cursodocencia_extracurricular'] = chart_cursodocencia_extracurricular

            items_data = [
                ['Año', 'Mis desarrollos tecnológicos', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = DesarrolloTecnologico.objects.filter(fecha__year=year).filter(
                    ((Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad__year__gt=year)) |
                     (Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad=None)))).count()

                request_user_items_year_sum = DesarrolloTecnologico.objects.filter(fecha__year=year,
                                                                                   autores=request.user).count()
                if not request_user_items_year_sum:
                    request_user_items_year_sum = 0
                items_data[i + 1].append(
                    request_user_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(desarrollo_tecnologico_autores__fecha__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(
                            total_items_year_sum / users_with_items_year_count,
                            2))
                else:
                    items_data[i + 1].append(0)

                max_items_year_user = User.objects.filter(
                    Q(desarrollo_tecnologico_autores__fecha__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('desarrollo_tecnologico_autores')).aggregate(Max('desarrollo_tecnologico_autores__count'))[
                    'desarrollo_tecnologico_autores__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(
                    max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(desarrollo_tecnologico_autores__fecha__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('desarrollo_tecnologico_autores')).aggregate(Min('desarrollo_tecnologico_autores__count'))[
                    'desarrollo_tecnologico_autores__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(
                    min_items_year_user)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_desarrollo_tecnologico = LineChart(data_source)
            context['chart_desarrollo_tecnologico'] = chart_desarrollo_tecnologico

            items_data = [
                ['Año', 'Mis distinciones', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = DistincionAcademico.objects.filter(fecha__year=year).filter(
                    ((Q(usuario__ingreso_entidad__year__lte=year) & Q(
                        usuario__egreso_entidad__year__gt=year)) |
                     (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).count()

                request_user_items_year_sum = DistincionAcademico.objects.filter(fecha__year=year,
                                                                                 usuario=request.user).count()
                if not request_user_items_year_sum:
                    request_user_items_year_sum = 0
                items_data[i + 1].append(
                    request_user_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(distincion_academico_usuario__fecha__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(
                            total_items_year_sum / users_with_items_year_count,
                            2))
                else:
                    items_data[i + 1].append(0)

                max_items_year_user = User.objects.filter(
                    Q(distincion_academico_usuario__fecha__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('distincion_academico_usuario')).aggregate(
                    Max('distincion_academico_usuario__count'))[
                    'distincion_academico_usuario__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(
                    max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(distincion_academico_usuario__fecha__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('distincion_academico_usuario')).aggregate(
                    Min('distincion_academico_usuario__count'))[
                    'distincion_academico_usuario__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(
                    min_items_year_user)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_distincion_academicos = LineChart(data_source)
            context['chart_distincion_academicos'] = chart_distincion_academicos

        return render(request, self.template_name, context)


class ReporteHistorico(View):
    form_class = None
    template_name = 'historico.html'
    aux = {}
    now = datetime.now()
    this_year = now.year
    ten_years_ago = now.year - 10

    def get(self, request):
        context = {}

        if request.user.is_authenticated:
            num_years = 10
            last_x_years = []
            active_users_per_last_x_year = []

            for i in range(datetime.now().year - num_years + 1, datetime.now().year + 1):
                last_x_years.append(i)

            for i in last_x_years:
                users_with_items_year_count = User.objects.filter(
                    (Q(ingreso_entidad__year__lte=i) & Q(egreso_entidad__year__gt=i)) |
                    (Q(ingreso_entidad__year__lte=i) & Q(egreso_entidad=None)))
                active_users_per_last_x_year.append(users_with_items_year_count.count())

            cursos_data = [['Año', 'Total horas', 'Promedio horas', 'Max horas', 'Min horas', 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                cursos_data.append([str(last_x_years[i])])

                users_with_items_year_count = User.objects.filter(
                    Q(cursos_especializacion__fecha_inicio__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0

                total_course_hours_year_sum = CursoEspecializacion.objects.filter(fecha_inicio__year=year).filter((
                    (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) |
                    (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).aggregate(
                    Sum('horas'))['horas__sum']
                if total_course_hours_year_sum == None:
                    total_course_hours_year_sum = 0

                request_user_item_year_sum = User.objects.filter(cursos_especializacion__fecha_inicio__year=year,
                                                                 cursos_especializacion__usuario=request.user).aggregate(
                    Sum('cursos_especializacion__horas'))['cursos_especializacion__horas__sum']

                if not total_course_hours_year_sum:
                    total_course_hours_year_sum = 0
                cursos_data[i + 1].append(total_course_hours_year_sum)

                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    cursos_data[i + 1].append(round(total_course_hours_year_sum / users_with_items_year_count, 2))
                else:
                    cursos_data[i + 1].append(round(0, 2))

                max_item_year_user = User.objects.filter(cursos_especializacion__fecha_inicio__year=year).annotate(
                    Sum('cursos_especializacion__horas')).filter((
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).aggregate(
                    Max('cursos_especializacion__horas__sum'))[
                    'cursos_especializacion__horas__sum__max']
                if max_item_year_user == None:
                    max_item_year_user = 0
                cursos_data[i + 1].append(max_item_year_user)

                min_item_year_user = User.objects.filter(cursos_especializacion__fecha_inicio__year=year).annotate(
                    Sum('cursos_especializacion__horas')).filter((
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).aggregate(
                    Min('cursos_especializacion__horas__sum'))[
                    'cursos_especializacion__horas__sum__min']
                if not min_item_year_user:
                    min_item_year_user = 0
                cursos_data[i + 1].append(min_item_year_user)

                cursos_data[i + 1].append(users_with_items_year_count)

            data_source = SimpleDataSource(data=cursos_data)
            hchart_cursos_especializacion = LineChart(data_source)
            context['hchart_cursos_especializacion'] = hchart_cursos_especializacion

            items_data = [
                ['Año', 'Total artículos de investigación', 'Promedio por persona', 'Max por persona',
                 'Min por persona', 'Personas activas', 'Indexados']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = ArticuloCientifico.objects.filter(fecha__year=year, status='PUBLICADO').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                        Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()

                request_user_item_year_sum = ArticuloCientifico.objects.filter(fecha__year=year,
                                                                               status='PUBLICADO',
                                                                               usuarios=request.user).count()
                if not total_items_year_sum:
                    total_items_year_sum = 0
                items_data[i + 1].append(total_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(articulo_cientifico_autores__fecha__year=year, articulo_cientifico_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0

                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(total_items_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(0)

                max_item_year_user = User.objects.filter(
                    Q(articulo_cientifico_autores__fecha__year=year, articulo_cientifico_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('articulo_cientifico_autores')).aggregate(Max('articulo_cientifico_autores__count'))[
                    'articulo_cientifico_autores__count__max']
                if max_item_year_user == None:
                    max_item_year_user = 0
                items_data[i + 1].append(max_item_year_user)

                min_articulo_cientifico_year_user = User.objects.filter(
                    Q(articulo_cientifico_autores__fecha__year=year, articulo_cientifico_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('articulo_cientifico_autores')).aggregate(Min('articulo_cientifico_autores__count'))[
                    'articulo_cientifico_autores__count__min']
                if min_articulo_cientifico_year_user == None:
                    min_articulo_cientifico_year_user = 0
                items_data[i + 1].append(min_articulo_cientifico_year_user)
                items_data[i + 1].append(users_with_items_year_count)

                total_items_indexados_year_sum = ArticuloCientifico.objects.filter(fecha__year=year,
                                                                                   status='PUBLICADO').exclude(
                    Q(id_doi__isnull=True) & Q(indices__isnull=True)).filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                        Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()

                items_data[i + 1].append(total_items_indexados_year_sum)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            hchart_articulos_investigacion_publicados = LineChart(data_source)
            context['hchart_articulos_investigacion_publicados'] = hchart_articulos_investigacion_publicados

            items_data = [
                ['Año', 'Total artículos de investigación', 'Promedio por persona', 'Max por persona',
                 'Min por persona', 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = ArticuloCientifico.objects.filter(fecha__year=year,
                                                                         status='EN_PRENSA').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                        Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()

                request_user_item_year_sum = ArticuloCientifico.objects.filter(fecha__year=year,
                                                                               status='EN_PRENSA',
                                                                               usuarios=request.user).count()
                if not total_items_year_sum:
                    total_items_year_sum = 0
                items_data[i + 1].append(total_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(articulo_cientifico_autores__fecha__year=year, articulo_cientifico_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(total_items_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(0)

                max_item_year_user = User.objects.filter(
                    Q(articulo_cientifico_autores__fecha__year=year, articulo_cientifico_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('articulo_cientifico_autores')).aggregate(Max('articulo_cientifico_autores__count'))[
                    'articulo_cientifico_autores__count__max']
                if max_item_year_user == None:
                    max_item_year_user = 0
                items_data[i + 1].append(max_item_year_user)

                min_articulo_cientifico_year_user = User.objects.filter(
                    Q(articulo_cientifico_autores__fecha__year=year, articulo_cientifico_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('articulo_cientifico_autores')).aggregate(Min('articulo_cientifico_autores__count'))[
                    'articulo_cientifico_autores__count__min']
                if min_articulo_cientifico_year_user == None:
                    min_articulo_cientifico_year_user = 0
                items_data[i + 1].append(min_articulo_cientifico_year_user)
                items_data[i + 1].append(users_with_items_year_count)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            hchart_articulos_investigacion_enprensa = LineChart(data_source)
            context['hchart_articulos_investigacion_enprensa'] = hchart_articulos_investigacion_enprensa

            items_data = [
                ['Año', 'Total artículos de investigación', 'Promedio por persona', 'Max por persona',
                 'Min por persona', 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = ArticuloCientifico.objects.filter(fecha__year=year,
                                                                         status='ACEPTADO').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                        Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()
                request_user_articulo_cientifico_year_sum = ArticuloCientifico.objects.filter(fecha__year=year,
                                                                                              status='ACEPTADO',
                                                                                              usuarios=request.user).count()
                if not total_items_year_sum:
                    total_items_year_sum = 0
                items_data[i + 1].append(total_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(articulo_cientifico_autores__fecha__year=year, articulo_cientifico_autores__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(total_items_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(0)

                max_item_year_user = User.objects.filter(
                    Q(articulo_cientifico_autores__fecha__year=year, articulo_cientifico_autores__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('articulo_cientifico_autores')).aggregate(Max('articulo_cientifico_autores__count'))[
                    'articulo_cientifico_autores__count__max']
                if max_item_year_user == None:
                    max_item_year_user = 0
                items_data[i + 1].append(max_item_year_user)

                min_articulo_cientifico_year_user = User.objects.filter(
                    Q(articulo_cientifico_autores__fecha__year=year, articulo_cientifico_autores__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('articulo_cientifico_autores')).aggregate(Min('articulo_cientifico_autores__count'))[
                    'articulo_cientifico_autores__count__min']
                if min_articulo_cientifico_year_user == None:
                    min_articulo_cientifico_year_user = 0
                items_data[i + 1].append(min_articulo_cientifico_year_user)
                items_data[i + 1].append(users_with_items_year_count)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            hchart_articulos_investigacion_aceptado = LineChart(data_source)
            context['hchart_articulos_investigacion_aceptado'] = hchart_articulos_investigacion_aceptado

            items_data = [
                ['Año', 'Total Libros', 'Promedio por persona', 'Max por persona', 'Min por persona',
                 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_libros_cientificos_year_sum = Libro.objects.filter(fecha__year=year, tipo='INVESTIGACION',
                                                                         status='PUBLICADO').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                        Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()
                request_user_libro_investigacion_year_sum = Libro.objects.filter(fecha__year=year, tipo='INVESTIGACION',
                                                                                 status='PUBLICADO',
                                                                                 usuarios=request.user).count()
                if not total_libros_cientificos_year_sum:
                    total_libros_cientificos_year_sum = 0
                items_data[i + 1].append(total_libros_cientificos_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='INVESTIGACION',
                      libro_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(total_libros_cientificos_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(0)

                max_libro_investigacion_year_user = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='INVESTIGACION',
                      libro_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Max('libro_autores__count'))[
                    'libro_autores__count__max']
                if max_libro_investigacion_year_user == None:
                    max_libro_investigacion_year_user = 0
                items_data[i + 1].append(max_libro_investigacion_year_user)

                min_libro_investigacion_year_user = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='INVESTIGACION',
                      libro_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Min('libro_autores__count'))[
                    'libro_autores__count__min']
                if min_libro_investigacion_year_user == None:
                    min_libro_investigacion_year_user = 0
                items_data[i + 1].append(min_libro_investigacion_year_user)
                items_data[i + 1].append(users_with_items_year_count)

            # print(libros_investigacion_publicado_data)
            data_source = SimpleDataSource(data=items_data)
            hchart_libros_investigacion_publicado = LineChart(data_source)
            context['hchart_libros_investigacion_publicado'] = hchart_libros_investigacion_publicado

            items_data = [
                ['Año', 'Total Libros', 'Promedio por persona', 'Max por persona', 'Min por persona',
                 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_libros_cientificos_year_sum = Libro.objects.filter(fecha__year=year, tipo='INVESTIGACION',
                                                                         status='EN_PRENSA').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                        Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()
                request_user_libro_investigacion_year_sum = Libro.objects.filter(fecha__year=year, tipo='INVESTIGACION',
                                                                                 status='EN_PRENSA',
                                                                                 usuarios=request.user).count()
                if not total_libros_cientificos_year_sum:
                    total_libros_cientificos_year_sum = 0
                items_data[i + 1].append(total_libros_cientificos_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='INVESTIGACION',
                      libro_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(total_libros_cientificos_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(0)

                max_libro_investigacion_year_user = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='INVESTIGACION',
                      libro_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Max('libro_autores__count'))[
                    'libro_autores__count__max']
                if max_libro_investigacion_year_user == None:
                    max_libro_investigacion_year_user = 0
                items_data[i + 1].append(max_libro_investigacion_year_user)

                min_libro_investigacion_year_user = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='INVESTIGACION',
                      libro_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Min('libro_autores__count'))[
                    'libro_autores__count__min']
                if min_libro_investigacion_year_user == None:
                    min_libro_investigacion_year_user = 0
                items_data[i + 1].append(min_libro_investigacion_year_user)
                items_data[i + 1].append(users_with_items_year_count)

            # print(libros_investigacion_enprensa_data)
            data_source = SimpleDataSource(data=items_data)
            hchart_libros_investigacion_enprensa = LineChart(data_source)
            context['hchart_libros_investigacion_enprensa'] = hchart_libros_investigacion_enprensa

            items_data = [
                ['Año', 'Total Libros', 'Promedio por persona', 'Max por persona', 'Min por persona',
                 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_libros_cientificos_year_sum = Libro.objects.filter(fecha__year=year, tipo='INVESTIGACION',
                                                                         status='ACEPTADO').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                        Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()
                request_user_libro_investigacion_year_sum = Libro.objects.filter(fecha__year=year, tipo='INVESTIGACION',
                                                                                 status='ACEPTADO',
                                                                                 usuarios=request.user).count()
                if not total_libros_cientificos_year_sum:
                    total_libros_cientificos_year_sum = 0
                items_data[i + 1].append(total_libros_cientificos_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='INVESTIGACION',
                      libro_autores__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(total_libros_cientificos_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(0)

                max_libro_investigacion_year_user = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='INVESTIGACION',
                      libro_autores__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Max('libro_autores__count'))[
                    'libro_autores__count__max']
                if max_libro_investigacion_year_user == None:
                    max_libro_investigacion_year_user = 0
                items_data[i + 1].append(max_libro_investigacion_year_user)

                min_libro_investigacion_year_user = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='INVESTIGACION',
                      libro_autores__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Min('libro_autores__count'))[
                    'libro_autores__count__min']
                if min_libro_investigacion_year_user == None:
                    min_libro_investigacion_year_user = 0
                items_data[i + 1].append(min_libro_investigacion_year_user)
                items_data[i + 1].append(users_with_items_year_count)

            # print(libros_investigacion_aceptado_data)
            data_source = SimpleDataSource(data=items_data)
            hchart_libros_investigacion_aceptados = LineChart(data_source)
            context['hchart_libros_investigacion_aceptados'] = hchart_libros_investigacion_aceptados

            items_data = [
                ['Año', 'Total Capitulos en libros', 'Promedio por persona', 'Max por persona', 'Min por persona',
                 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_capitulos_libros_investigacion_year_sum = CapituloLibroInvestigacion.objects.filter(
                    libro__fecha__year=year, libro__tipo='INVESTIGACION',
                    libro__status='PUBLICADO').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                        Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()

                request_user_capitulos_libros_investigacion_year_sum = CapituloLibroInvestigacion.objects.filter(
                    libro__fecha__year=year, libro__tipo='INVESTIGACION',
                    libro__status='PUBLICADO',
                    libro__usuarios=request.user).count()

                if not total_capitulos_libros_investigacion_year_sum:
                    total_capitulos_libros_investigacion_year_sum = 0
                items_data[i + 1].append(total_capitulos_libros_investigacion_year_sum)

                users_with_capitulos_libros_investigacion_year_count = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='INVESTIGACION',
                      capitulo_libro_investigacion_autores__libro__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_capitulos_libros_investigacion_year_count == None:
                    users_with_capitulos_libros_investigacion_year_count = 0
                if users_with_capitulos_libros_investigacion_year_count > 0:
                    items_data[i + 1].append(
                        round(
                            total_capitulos_libros_investigacion_year_sum / users_with_capitulos_libros_investigacion_year_count,
                            2))
                else:
                    items_data[i + 1].append(0)

                max_capitulos_libros_investigacion_year_user = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='INVESTIGACION',
                      capitulo_libro_investigacion_autores__libro__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Max('libro_autores__count'))[
                    'libro_autores__count__max']
                if max_capitulos_libros_investigacion_year_user == None:
                    max_capitulos_libros_investigacion_year_user = 0
                items_data[i + 1].append(
                    max_capitulos_libros_investigacion_year_user)

                min_capitulos_libros_investigacion_year_user = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='INVESTIGACION',
                      capitulo_libro_investigacion_autores__libro__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Min('libro_autores__count'))[
                    'libro_autores__count__min']
                if min_capitulos_libros_investigacion_year_user == None:
                    min_capitulos_libros_investigacion_year_user = 0
                items_data[i + 1].append(min_capitulos_libros_investigacion_year_user)
                items_data[i + 1].append(users_with_capitulos_libros_investigacion_year_count)

            # print(capitulos_libros_investigacion_publicado_data)
            data_source = SimpleDataSource(data=items_data)
            hchart_capitulos_libros_investigacion_publicado = LineChart(data_source)
            context['hchart_capitulos_libros_investigacion_publicado'] = hchart_capitulos_libros_investigacion_publicado

            items_data = [
                ['Año', 'Total Capitulos en libros', 'Promedio por persona', 'Max por persona', 'Min por persona',
                 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_capitulos_libros_investigacion_year_sum = CapituloLibroInvestigacion.objects.filter(
                    libro__fecha__year=year, libro__tipo='INVESTIGACION',
                    libro__status='EN_PRENSA').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                        Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()

                request_user_capitulos_libros_investigacion_year_sum = CapituloLibroInvestigacion.objects.filter(
                    libro__fecha__year=year, libro__tipo='INVESTIGACION',
                    libro__status='EN_PRENSA',
                    libro__usuarios=request.user).count()

                if not total_capitulos_libros_investigacion_year_sum:
                    total_capitulos_libros_investigacion_year_sum = 0
                items_data[i + 1].append(
                    total_capitulos_libros_investigacion_year_sum)

                users_with_capitulos_libros_investigacion_year_count = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='INVESTIGACION',
                      capitulo_libro_investigacion_autores__libro__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_capitulos_libros_investigacion_year_count == None:
                    users_with_capitulos_libros_investigacion_year_count = 0
                if users_with_capitulos_libros_investigacion_year_count > 0:
                    items_data[i + 1].append(
                        round(
                            total_capitulos_libros_investigacion_year_sum / users_with_capitulos_libros_investigacion_year_count,
                            2))
                else:
                    items_data[i + 1].append(0)

                max_capitulos_libros_investigacion_year_user = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='INVESTIGACION',
                      capitulo_libro_investigacion_autores__libro__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Max('libro_autores__count'))[
                    'libro_autores__count__max']
                if max_capitulos_libros_investigacion_year_user == None:
                    max_capitulos_libros_investigacion_year_user = 0
                items_data[i + 1].append(
                    max_capitulos_libros_investigacion_year_user)

                min_capitulos_libros_investigacion_year_user = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='INVESTIGACION',
                      capitulo_libro_investigacion_autores__libro__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Min('libro_autores__count'))[
                    'libro_autores__count__min']
                if min_capitulos_libros_investigacion_year_user == None:
                    min_capitulos_libros_investigacion_year_user = 0
                items_data[i + 1].append(min_capitulos_libros_investigacion_year_user)
                items_data[i + 1].append(users_with_capitulos_libros_investigacion_year_count)

            # print(capitulos_libros_investigacion_enprensa_data)
            data_source = SimpleDataSource(data=items_data)
            hchart_capitulos_libros_investigacion_enprensa = LineChart(data_source)
            context['hchart_capitulos_libros_investigacion_enprensa'] = hchart_capitulos_libros_investigacion_enprensa

            items_data = [
                ['Año', 'Total Capitulos en libros', 'Promedio por persona', 'Max por persona', 'Min por persona',
                 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_capitulos_libros_investigacion_year_sum = CapituloLibroInvestigacion.objects.filter(
                    libro__fecha__year=year, libro__tipo='INVESTIGACION',
                    libro__status='ACEPTADO').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                        Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()

                request_user_capitulos_libros_investigacion_year_sum = CapituloLibroInvestigacion.objects.filter(
                    libro__fecha__year=year, libro__tipo='INVESTIGACION',
                    libro__status='ACEPTADO',
                    libro__usuarios=request.user).count()

                if not total_capitulos_libros_investigacion_year_sum:
                    total_capitulos_libros_investigacion_year_sum = 0
                items_data[i + 1].append(
                    total_capitulos_libros_investigacion_year_sum)

                users_with_capitulos_libros_investigacion_year_count = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='INVESTIGACION',
                      capitulo_libro_investigacion_autores__libro__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_capitulos_libros_investigacion_year_count == None:
                    users_with_capitulos_libros_investigacion_year_count = 0
                if users_with_capitulos_libros_investigacion_year_count > 0:
                    items_data[i + 1].append(
                        round(
                            total_capitulos_libros_investigacion_year_sum / users_with_capitulos_libros_investigacion_year_count,
                            2))
                else:
                    items_data[i + 1].append(0)

                max_capitulos_libros_investigacion_year_user = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='INVESTIGACION',
                      capitulo_libro_investigacion_autores__libro__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Max('libro_autores__count'))[
                    'libro_autores__count__max']
                if max_capitulos_libros_investigacion_year_user == None:
                    max_capitulos_libros_investigacion_year_user = 0
                items_data[i + 1].append(max_capitulos_libros_investigacion_year_user)
                items_data[i + 1].append(users_with_capitulos_libros_investigacion_year_count)

                min_capitulos_libros_investigacion_year_user = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='INVESTIGACION',
                      capitulo_libro_investigacion_autores__libro__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Min('libro_autores__count'))[
                    'libro_autores__count__min']
                if min_capitulos_libros_investigacion_year_user == None:
                    min_capitulos_libros_investigacion_year_user = 0
                items_data[i + 1].append(
                    min_capitulos_libros_investigacion_year_user)

            # print(capitulos_libros_investigacion_aceptado_data)
            data_source = SimpleDataSource(data=items_data)
            hchart_capitulos_libros_investigacion_aceptado = LineChart(data_source)
            context['hchart_capitulos_libros_investigacion_aceptado'] = hchart_capitulos_libros_investigacion_aceptado

            items_data = [
                ['Año', 'Total Mapas', 'Promedio por persona', 'Max por persona', 'Min por persona',
                 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = MapaArbitrado.objects.filter(fecha__year=year,
                                                                    status='PUBLICADO').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                        Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()

                request_user_items_year_sum = MapaArbitrado.objects.filter(fecha__year=year,
                                                                           status='PUBLICADO',
                                                                           usuarios=request.user).count()
                if not total_items_year_sum:
                    total_items_year_sum = 0
                items_data[i + 1].append(total_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(mapa_arbitrado_autores__fecha__year=year, mapa_arbitrado_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0

                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(total_items_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(0)

                max_items_year_user = User.objects.filter(
                    Q(mapa_arbitrado_autores__fecha__year=year, mapa_arbitrado_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('mapa_arbitrado_autores')).aggregate(Max('mapa_arbitrado_autores__count'))[
                    'mapa_arbitrado_autores__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(mapa_arbitrado_autores__fecha__year=year, mapa_arbitrado_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('mapa_arbitrado_autores')).aggregate(Min('mapa_arbitrado_autores__count'))[
                    'mapa_arbitrado_autores__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(min_items_year_user)
                items_data[i + 1].append(users_with_items_year_count)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            hchart_mapas_arbitrados_publicados = LineChart(data_source)
            context['hchart_mapas_arbitrados_publicados'] = hchart_mapas_arbitrados_publicados

            items_data = [
                ['Año', 'Total Mapas', 'Promedio por persona', 'Max por persona', 'Min por persona',
                 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = MapaArbitrado.objects.filter(fecha__year=year,
                                                                    status='EN_PRENSA').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                        Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()

                request_user_items_year_sum = MapaArbitrado.objects.filter(fecha__year=year,
                                                                           status='EN_PRENSA',
                                                                           usuarios=request.user).count()
                if not total_items_year_sum:
                    total_items_year_sum = 0
                items_data[i + 1].append(total_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(mapa_arbitrado_autores__fecha__year=year, mapa_arbitrado_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0

                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(total_items_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(0)

                max_items_year_user = User.objects.filter(
                    Q(mapa_arbitrado_autores__fecha__year=year, mapa_arbitrado_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('mapa_arbitrado_autores')).aggregate(Max('mapa_arbitrado_autores__count'))[
                    'mapa_arbitrado_autores__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(mapa_arbitrado_autores__fecha__year=year, mapa_arbitrado_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('mapa_arbitrado_autores')).aggregate(Min('mapa_arbitrado_autores__count'))[
                    'mapa_arbitrado_autores__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(min_items_year_user)
                items_data[i + 1].append(users_with_items_year_count)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            hchart_mapas_arbitrados_enprensa = LineChart(data_source)
            context['hchart_mapas_arbitrados_enprensa'] = hchart_mapas_arbitrados_enprensa

            items_data = [
                ['Año', 'Total Mapas', 'Promedio por persona', 'Max por persona', 'Min por persona',
                 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = MapaArbitrado.objects.filter(fecha__year=year,
                                                                    status='ACEPTADO').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                        Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()

                request_user_items_year_sum = MapaArbitrado.objects.filter(fecha__year=year,
                                                                           status='ACEPTADO',
                                                                           usuarios=request.user).count()
                if not total_items_year_sum:
                    total_items_year_sum = 0
                items_data[i + 1].append(total_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(mapa_arbitrado_autores__fecha__year=year, mapa_arbitrado_autores__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0

                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(total_items_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(0)

                max_items_year_user = User.objects.filter(
                    Q(mapa_arbitrado_autores__fecha__year=year, mapa_arbitrado_autores__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('mapa_arbitrado_autores')).aggregate(Max('mapa_arbitrado_autores__count'))[
                    'mapa_arbitrado_autores__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(mapa_arbitrado_autores__fecha__year=year, mapa_arbitrado_autores__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('mapa_arbitrado_autores')).aggregate(Min('mapa_arbitrado_autores__count'))[
                    'mapa_arbitrado_autores__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(min_items_year_user)
                items_data[i + 1].append(users_with_items_year_count)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            hchart_mapas_arbitrados_aceptados = LineChart(data_source)
            context['hchart_mapas_arbitrados_aceptados'] = hchart_mapas_arbitrados_aceptados

            items_data = [
                ['Año', 'Total Informes Técnicos', 'Promedio por persona', 'Max por persona', 'Min por persona',
                 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = PublicacionTecnica.objects.filter(fecha__year=year).filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                        Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()

                request_user_items_year_sum = PublicacionTecnica.objects.filter(fecha__year=year,
                                                                                usuarios=request.user).count()
                if not total_items_year_sum:
                    total_items_year_sum = 0
                items_data[i + 1].append(total_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(informe_tecnico_autores__fecha__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0

                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(total_items_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(0)

                max_items_year_user = User.objects.filter(
                    Q(informe_tecnico_autores__fecha__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('informe_tecnico_autores')).aggregate(Max('informe_tecnico_autores__count'))[
                    'informe_tecnico_autores__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(informe_tecnico_autores__fecha__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('informe_tecnico_autores')).aggregate(Min('informe_tecnico_autores__count'))[
                    'informe_tecnico_autores__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(min_items_year_user)
                items_data[i + 1].append(users_with_items_year_count)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            hchart_informes_tecnicos = LineChart(data_source)
            context['hchart_informes_tecnicos'] = hchart_informes_tecnicos

            items_data = [
                ['Año', 'Total Proyectos de investigación', 'Promedio por persona', 'Max por persona',
                 'Min por persona', 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = ProyectoInvestigacion.objects.filter(
                    (Q(fecha_inicio__year__lte=year) & Q(fecha_fin__year__gt=year))
                    | (Q(fecha_inicio__year__lte=year) & Q(fecha_fin=None))).filter(
                    (Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year))
                    | (Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None))).count()

                request_user_items_year_sum = ProyectoInvestigacion.objects.filter(usuarios=request.user).filter(
                    (Q(fecha_inicio__year__lte=year) & Q(fecha_fin__year__gt=year))
                    | (Q(fecha_inicio__year__lte=year) & Q(fecha_fin=None))).count()
                if not total_items_year_sum:
                    total_items_year_sum = 0
                items_data[i + 1].append(total_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    (Q(proyecto_investigacion_responsables__fecha_inicio__year__lte=year) & Q(
                        proyecto_investigacion_responsables__fecha_fin__year__gt=year))
                    | (Q(proyecto_investigacion_responsables__fecha_inicio__year__lte=year) & Q(
                        proyecto_investigacion_responsables__fecha_fin=None))).filter(
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0

                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(total_items_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(0)

                max_items_year_user = \
                    User.objects.filter(
                        (Q(proyecto_investigacion_responsables__fecha_inicio__year__lte=year) & Q(
                            proyecto_investigacion_responsables__fecha_fin__year__gt=year))
                        | (
                            Q(proyecto_investigacion_responsables__fecha_inicio__year__lte=year) & Q(
                                proyecto_investigacion_responsables__fecha_fin=None))
                    ).filter(((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                              (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                        Count('proyecto_investigacion_responsables')).aggregate(
                        Max('proyecto_investigacion_responsables__count'))[
                        'proyecto_investigacion_responsables__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(max_items_year_user)

                min_items_year_user = \
                    User.objects.filter(
                        (Q(proyecto_investigacion_responsables__fecha_inicio__year__lte=year) & Q(
                            proyecto_investigacion_responsables__fecha_fin__year__gt=year))
                        | (
                            Q(proyecto_investigacion_responsables__fecha_inicio__year__lte=year) & Q(
                                proyecto_investigacion_responsables__fecha_fin=None))
                    ).filter(((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                              (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                        Count('proyecto_investigacion_responsables')).aggregate(
                        Min('proyecto_investigacion_responsables__count'))[
                        'proyecto_investigacion_responsables__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(min_items_year_user)
                items_data[i + 1].append(users_with_items_year_count)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            hchart_proyectos_investigacion = LineChart(data_source)
            context['hchart_proyectos_investigacion'] = hchart_proyectos_investigacion

            items_data = [
                ['Año', 'Total Memorias in extenso', 'Promedio por persona', 'Max por persona', 'Min por persona',
                 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = MemoriaInExtenso.objects.filter(evento__fecha_inicio__year=year).filter(
                    (Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year))
                    | (Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None))).count()

                request_user_items_year_sum = MemoriaInExtenso.objects.filter(evento__fecha_inicio__year=year,
                                                                              usuarios=request.user).count()
                if not total_items_year_sum:
                    total_items_year_sum = 0
                items_data[i + 1].append(total_items_year_sum)

                users_with_items_year_count = User.objects.filter(memoria_in_extenso_autores__evento__fecha_inicio__year=year).filter(
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0

                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(total_items_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(0)

                max_items_year_user = User.objects.filter(memoria_in_extenso_autores__evento__fecha_inicio__year=year).filter(
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('memoria_in_extenso_autores')).aggregate(
                    Max('memoria_in_extenso_autores__count'))['memoria_in_extenso_autores__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(max_items_year_user)

                min_items_year_user = User.objects.filter(memoria_in_extenso_autores__evento__fecha_inicio__year=year).filter(
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('memoria_in_extenso_autores')).aggregate(Min('memoria_in_extenso_autores__count'))[
                    'memoria_in_extenso_autores__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(min_items_year_user)
                items_data[i + 1].append(users_with_items_year_count)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            hchart_memoria_in_extenso = LineChart(data_source)
            context['hchart_memoria_in_extenso'] = hchart_memoria_in_extenso



            items_data = [
                ['Año', 'Total Reseñas', 'Promedio por persona', 'Max por persona', 'Min por persona',
                 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = Resena.objects.filter(fecha__year=year).filter(
                    ((Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) |
                     (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).count()

                request_user_items_year_sum = Resena.objects.filter(fecha__year=year, usuario=request.user).count()

                if not total_items_year_sum:
                    total_items_year_sum = 0
                items_data[i + 1].append(
                    total_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(resena_autores__fecha__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(
                            total_items_year_sum / users_with_items_year_count,
                            2))
                else:
                    items_data[i + 1].append(0)

                max_items_year_user = User.objects.filter(
                    Q(resena_autores__fecha__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('resena_autores')).aggregate(Max('resena_autores__count'))[
                    'resena_autores__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(
                    max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(resena_autores__fecha__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('resena_autores')).aggregate(Min('resena_autores__count'))[
                    'resena_autores__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(min_items_year_user)
                items_data[i + 1].append(users_with_items_year_count)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            hchart_resena = LineChart(data_source)
            context['hchart_resena'] = hchart_resena

            items_data = [
                ['Año', 'Total Organizaciones de eventos académicos', 'Promedio por persona', 'Max por persona',
                 'Min por persona', 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = OrganizacionEventoAcademico.objects.filter(
                    evento__fecha_inicio__year=year).filter(
                    ((Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) |
                     (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).count()

                request_user_items_year_sum = OrganizacionEventoAcademico.objects.filter(
                    evento__fecha_inicio__year=year,
                    usuario=request.user).count()
                if not total_items_year_sum:
                    total_items_year_sum = 0
                items_data[i + 1].append(
                    total_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(organizacioneventoacademico__evento__fecha_inicio__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(total_items_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(0)

                max_items_year_user = User.objects.filter(
                    Q(organizacioneventoacademico__evento__fecha_inicio__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('organizacioneventoacademico')).aggregate(Max('organizacioneventoacademico__count'))[
                    'organizacioneventoacademico__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(
                    max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(organizacioneventoacademico__evento__fecha_inicio__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('organizacioneventoacademico')).aggregate(Min('organizacioneventoacademico__count'))[
                    'organizacioneventoacademico__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(min_items_year_user)
                items_data[i + 1].append(users_with_items_year_count)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            hchart_organizacioneventoacademico = LineChart(data_source)
            context['hchart_organizacioneventoacademico'] = hchart_organizacioneventoacademico

            items_data = [
                ['Año', 'Total Participaciones en eventos académicos', 'Promedio por persona', 'Max por persona',
                 'Min por persona', 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = ParticipacionEventoAcademico.objects.filter(
                    evento__fecha_inicio__year=year).filter(
                    ((Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) |
                     (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).count()

                request_user_items_year_sum = ParticipacionEventoAcademico.objects.filter(
                    evento__fecha_inicio__year=year,
                    usuario=request.user).count()

                if not total_items_year_sum:
                    total_items_year_sum = 0
                items_data[i + 1].append(
                    total_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(participacion_evento_academico_autores__evento__fecha_inicio__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(total_items_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(0)

                max_items_year_user = User.objects.filter(
                    Q(participacion_evento_academico_autores__evento__fecha_inicio__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('participacion_evento_academico_autores')).aggregate(Max('participacion_evento_academico_autores__count'))[
                    'participacion_evento_academico_autores__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(
                    max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(organizacioneventoacademico__evento__fecha_inicio__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('participacion_evento_academico_autores')).aggregate(Min('participacion_evento_academico_autores__count'))[
                    'participacion_evento_academico_autores__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(min_items_year_user)
                items_data[i + 1].append(users_with_items_year_count)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            hchart_participacioneventoacademico = LineChart(data_source)
            context['hchart_participacioneventoacademico'] = hchart_participacioneventoacademico

            items_data = [
                ['Año', 'Total artículos de divulgación', 'Promedio por persona', 'Max por persona', 'Min por persona',
                 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = ArticuloDivulgacion.objects.filter(fecha__year=year, status='PUBLICADO').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                        Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()

                request_user_item_year_sum = ArticuloDivulgacion.objects.filter(fecha__year=year, status='PUBLICADO',
                                                                                usuarios=request.user).count()
                if not total_items_year_sum:
                    total_items_year_sum = 0
                items_data[i + 1].append(total_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(articulo_divulgacion_autores__fecha__year=year,
                      articulo_divulgacion_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0

                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(total_items_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(0)

                max_item_year_user = User.objects.filter(
                    Q(articulo_divulgacion_autores__fecha__year=year,
                      articulo_divulgacion_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('articulo_divulgacion_autores')).aggregate(Max('articulo_divulgacion_autores__count'))[
                    'articulo_divulgacion_autores__count__max']
                if max_item_year_user == None:
                    max_item_year_user = 0
                items_data[i + 1].append(max_item_year_user)

                min_articulo_cientifico_year_user = User.objects.filter(
                    Q(articulo_divulgacion_autores__fecha__year=year,
                      articulo_divulgacion_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('articulo_divulgacion_autores')).aggregate(Min('articulo_divulgacion_autores__count'))[
                    'articulo_divulgacion_autores__count__min']
                if min_articulo_cientifico_year_user == None:
                    min_articulo_cientifico_year_user = 0
                items_data[i + 1].append(min_articulo_cientifico_year_user)
                items_data[i + 1].append(users_with_items_year_count)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            hchart_articulo_divulgacion_publicados = LineChart(data_source)
            context['hchart_articulo_divulgacion_publicados'] = hchart_articulo_divulgacion_publicados

            items_data = [
                ['Año', 'Total artículos de divulgación', 'Promedio por persona', 'Max por persona', 'Min por persona',
                 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = ArticuloDivulgacion.objects.filter(fecha__year=year,
                                                                          status='EN_PRENSA').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                        Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()

                request_user_item_year_sum = ArticuloDivulgacion.objects.filter(fecha__year=year,
                                                                                status='EN_PRENSA',
                                                                                usuarios=request.user).count()
                if not total_items_year_sum:
                    total_items_year_sum = 0
                items_data[i + 1].append(total_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(articulo_divulgacion_autores__fecha__year=year,
                      articulo_divulgacion_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(total_items_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(0)

                max_item_year_user = User.objects.filter(
                    Q(articulo_divulgacion_autores__fecha__year=year,
                      articulo_divulgacion_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('articulo_divulgacion_autores')).aggregate(Max('articulo_divulgacion_autores__count'))[
                    'articulo_divulgacion_autores__count__max']
                if max_item_year_user == None:
                    max_item_year_user = 0
                items_data[i + 1].append(max_item_year_user)

                min_articulo_cientifico_year_user = User.objects.filter(
                    Q(articulo_divulgacion_autores__fecha__year=year,
                      articulo_divulgacion_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('articulo_divulgacion_autores')).aggregate(Min('articulo_divulgacion_autores__count'))[
                    'articulo_divulgacion_autores__count__min']
                if min_articulo_cientifico_year_user == None:
                    min_articulo_cientifico_year_user = 0
                items_data[i + 1].append(min_articulo_cientifico_year_user)
                items_data[i + 1].append(users_with_items_year_count)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            hchart_articulo_divulgacion_enprensa = LineChart(data_source)
            context['hchart_articulo_divulgacion_enprensa'] = hchart_articulo_divulgacion_enprensa

            items_data = [
                ['Año', 'Total artículos de divulgación', 'Promedio por persona', 'Max por persona', 'Min por persona',
                 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = ArticuloDivulgacion.objects.filter(fecha__year=year,
                                                                          status='ACEPTADO').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                        Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()
                request_user_items_year_sum = ArticuloDivulgacion.objects.filter(fecha__year=year,
                                                                                 status='ACEPTADO',
                                                                                 usuarios=request.user).count()
                if not total_items_year_sum:
                    total_items_year_sum = 0
                items_data[i + 1].append(total_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(articulo_divulgacion_autores__fecha__year=year, articulo_divulgacion_autores__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(total_items_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(0)

                max_item_year_user = User.objects.filter(
                    Q(articulo_divulgacion_autores__fecha__year=year, articulo_divulgacion_autores__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('articulo_divulgacion_autores')).aggregate(Max('articulo_divulgacion_autores__count'))[
                    'articulo_divulgacion_autores__count__max']
                if max_item_year_user == None:
                    max_item_year_user = 0
                items_data[i + 1].append(max_item_year_user)

                min_articulo_cientifico_year_user = User.objects.filter(
                    Q(articulo_divulgacion_autores__fecha__year=year, articulo_divulgacion_autores__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('articulo_divulgacion_autores')).aggregate(Min('articulo_divulgacion_autores__count'))[
                    'articulo_divulgacion_autores__count__min']
                if min_articulo_cientifico_year_user == None:
                    min_articulo_cientifico_year_user = 0
                items_data[i + 1].append(min_articulo_cientifico_year_user)
                items_data[i + 1].append(users_with_items_year_count)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            hchart_articulo_divulgacion_aceptados = LineChart(data_source)
            context['hchart_articulo_divulgacion_aceptados'] = hchart_articulo_divulgacion_aceptados

            items_data = [
                ['Año', 'Total Libros de divulgación', 'Promedio por persona', 'Max por persona', 'Min por persona',
                 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = Libro.objects.filter(fecha__year=year, tipo='DIVULGACION',
                                                            status='PUBLICADO').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                        Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()
                request_user_items_year_sum = Libro.objects.filter(fecha__year=year, tipo='DIVULGACION',
                                                                   status='PUBLICADO',
                                                                   usuarios=request.user).count()
                if not total_items_year_sum:
                    total_items_year_sum = 0
                items_data[i + 1].append(total_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='DIVULGACION',
                      libro_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(total_items_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(0)

                max_items_year_user = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='DIVULGACION',
                      libro_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Max('libro_autores__count'))[
                    'libro_autores__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='DIVULGACION',
                      libro_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Min('libro_autores__count'))[
                    'libro_autores__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(min_items_year_user)
                items_data[i + 1].append(users_with_items_year_count)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            hchart_libros_divulgacion_publicados = LineChart(data_source)
            context['hchart_libros_divulgacion_publicados'] = hchart_libros_divulgacion_publicados

            items_data = [
                ['Año', 'Total Libros de divulgación', 'Promedio por persona', 'Max por persona', 'Min por persona',
                 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = Libro.objects.filter(fecha__year=year, tipo='DIVULGACION',
                                                            status='EN_PRENSA').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                        Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()
                request_user_items_year_sum = Libro.objects.filter(fecha__year=year, tipo='DIVULGACION',
                                                                   status='EN_PRENSA',
                                                                   usuarios=request.user).count()
                if not total_items_year_sum:
                    total_items_year_sum = 0
                items_data[i + 1].append(total_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='DIVULGACION',
                      libro_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(total_items_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(0)

                max_items_year_user = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='DIVULGACION',
                      libro_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Max('libro_autores__count'))[
                    'libro_autores__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='DIVULGACION',
                      libro_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Min('libro_autores__count'))[
                    'libro_autores__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(min_items_year_user)
                items_data[i + 1].append(users_with_items_year_count)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            hchart_libros_divulgacion_enprensa = LineChart(data_source)
            context['hchart_libros_divulgacion_enprensa'] = hchart_libros_divulgacion_enprensa

            items_data = [
                ['Año', 'Total Libros de divulgación', 'Promedio por persona', 'Max por persona', 'Min por persona',
                 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = Libro.objects.filter(fecha__year=year, tipo='DIVULGACION',
                                                            status='ACEPTADO').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                        Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()
                request_user_items_year_sum = Libro.objects.filter(fecha__year=year, tipo='DIVULGACION',
                                                                   status='ACEPTADO',
                                                                   usuarios=request.user).count()
                if not total_items_year_sum:
                    total_items_year_sum = 0
                items_data[i + 1].append(total_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='DIVULGACION',
                      libro_autores__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(total_items_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(0)

                max_items_year_user = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='DIVULGACION',
                      libro_autores__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Max('libro_autores__count'))[
                    'libro_autores__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='DIVULGACION',
                      libro_autores__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Min('libro_autores__count'))[
                    'libro_autores__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(min_items_year_user)
                items_data[i + 1].append(users_with_items_year_count)

            # print(libros_investigacion_aceptado_data)
            data_source = SimpleDataSource(data=items_data)
            hchart_libros_divulgacion_aceptados = LineChart(data_source)
            context['hchart_libros_divulgacion_aceptados'] = hchart_libros_divulgacion_aceptados

            items_data = [
                ['Año', 'Total Capitulos en libros de divulgación', 'Promedio por persona', 'Max por persona',
                 'Min por persona', 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = CapituloLibroDivulgacion.objects.filter(
                    libro__fecha__year=year, libro__tipo='DIVULGACION',
                    libro__status='PUBLICADO').filter(
                    ((Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) | (
                        Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).count()

                request_user_items_year_sum = CapituloLibroDivulgacion.objects.filter(
                    libro__fecha__year=year, libro__tipo='DIVULGACION',
                    libro__status='PUBLICADO',
                    libro__usuarios=request.user).count()

                if not total_items_year_sum:
                    total_items_year_sum = 0
                items_data[i + 1].append(
                    total_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='DIVULGACION',
                      capitulo_libro_investigacion_autores__libro__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(
                            total_items_year_sum / users_with_items_year_count,
                            2))
                else:
                    items_data[i + 1].append(0)

                max_items_year_user = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='DIVULGACION',
                      capitulo_libro_investigacion_autores__libro__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Max('libro_autores__count'))[
                    'libro_autores__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(
                    max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='DIVULGACION',
                      capitulo_libro_investigacion_autores__libro__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Min('libro_autores__count'))[
                    'libro_autores__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(min_items_year_user)
                items_data[i + 1].append(users_with_items_year_count)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            hchart_capitulos_libros_divulgacion_publicados = LineChart(data_source)
            context['hchart_capitulos_libros_divulgacion_publicados'] = hchart_capitulos_libros_divulgacion_publicados

            items_data = [
                ['Año', 'Total Capitulos en libros de divulgación', 'Promedio por persona', 'Max por persona',
                 'Min por persona', 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = CapituloLibroDivulgacion.objects.filter(
                    libro__fecha__year=year, libro__tipo='DIVULGACION',
                    libro__status='EN_PRENSA').filter(
                    ((Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) | (
                        Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).count()

                request_user_items_year_sum = CapituloLibroDivulgacion.objects.filter(
                    libro__fecha__year=year, libro__tipo='DIVULGACION',
                    libro__status='EN_PRENSA',
                    libro__usuarios=request.user).count()

                if not total_items_year_sum:
                    total_items_year_sum = 0
                items_data[i + 1].append(
                    total_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='DIVULGACION',
                      capitulo_libro_investigacion_autores__libro__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(
                            total_items_year_sum / users_with_items_year_count,
                            2))
                else:
                    items_data[i + 1].append(0)

                max_items_year_user = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='DIVULGACION',
                      capitulo_libro_investigacion_autores__libro__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Max('libro_autores__count'))[
                    'libro_autores__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(
                    max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='DIVULGACION',
                      capitulo_libro_investigacion_autores__libro__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Min('libro_autores__count'))[
                    'libro_autores__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(min_items_year_user)
                items_data[i + 1].append(users_with_items_year_count)

            # print(capitulos_libros_investigacion_enprensa_data)
            data_source = SimpleDataSource(data=items_data)
            hchart_capitulos_libros_divulgacion_enprensa = LineChart(data_source)
            context['hchart_capitulos_libros_divulgacion_enprensa'] = hchart_capitulos_libros_divulgacion_enprensa

            items_data = [
                ['Año', 'Total Capitulos en libros de divulgación', 'Promedio por persona', 'Max por persona',
                 'Min por persona', 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = CapituloLibroDivulgacion.objects.filter(
                    libro__fecha__year=year, libro__tipo='DIVULGACION',
                    libro__status='ACEPTADO').filter(
                    ((Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) | (
                        Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).count()

                request_user_items_year_sum = CapituloLibroDivulgacion.objects.filter(
                    libro__fecha__year=year, libro__tipo='DIVULGACION',
                    libro__status='ACEPTADO',
                    libro__usuarios=request.user).count()

                if not total_items_year_sum:
                    total_items_year_sum = 0
                items_data[i + 1].append(total_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='DIVULGACION',
                      capitulo_libro_investigacion_autores__libro__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(
                            total_items_year_sum / users_with_items_year_count,
                            2))
                else:
                    items_data[i + 1].append(0)

                max_items_year_user = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='DIVULGACION',
                      capitulo_libro_investigacion_autores__libro__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Max('libro_autores__count'))[
                    'libro_autores__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(
                    max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='DIVULGACION',
                      capitulo_libro_investigacion_autores__libro__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Min('libro_autores__count'))[
                    'libro_autores__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(min_items_year_user)
                items_data[i + 1].append(users_with_items_year_count)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            hchart_capitulos_libros_divulgacion_aceptados = LineChart(data_source)
            context['hchart_capitulos_libros_divulgacion_aceptados'] = hchart_capitulos_libros_divulgacion_aceptados

            items_data = [
                ['Año', 'Total Organizaciones de eventos de divulgación', 'Promedio por persona', 'Max por persona',
                 'Min por persona', 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = OrganizacionEventoDivulgacion.objects.filter(
                    evento__fecha_inicio__year=year).filter(
                    ((Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) |
                     (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).count()

                request_user_items_year_sum = OrganizacionEventoDivulgacion.objects.filter(
                    evento__fecha_inicio__year=year,
                    usuario=request.user).count()

                if not total_items_year_sum:
                    total_items_year_sum = 0
                items_data[i + 1].append(total_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(organizacioneventodivulgacion__evento__fecha_inicio__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(total_items_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(0)

                max_items_year_user = User.objects.filter(
                    Q(organizacioneventodivulgacion__evento__fecha_inicio__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('organizacioneventodivulgacion')).aggregate(Max('organizacioneventodivulgacion__count'))[
                    'organizacioneventodivulgacion__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(
                    max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(organizacioneventodivulgacion__evento__fecha_inicio__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('organizacioneventodivulgacion')).aggregate(Min('organizacioneventodivulgacion__count'))[
                    'organizacioneventodivulgacion__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(min_items_year_user)
                items_data[i + 1].append(users_with_items_year_count)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            hchart_organizacioneventodivulgacion = LineChart(data_source)
            context['hchart_organizacioneventodivulgacion'] = hchart_organizacioneventodivulgacion

            items_data = [
                ['Año', 'Total Participaciones en eventos de divulgación', 'Promedio por persona', 'Max por persona',
                 'Min por persona', 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = ParticipacionEventoDivulgacion.objects.filter(
                    evento__fecha_inicio__year=year).filter(
                    ((Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) |
                     (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).count()

                request_user_items_year_sum = ParticipacionEventoDivulgacion.objects.filter(
                    evento__fecha_inicio__year=year,
                    usuario=request.user).count()

                if not total_items_year_sum:
                    total_items_year_sum = 0
                items_data[i + 1].append(total_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(participacioneventodivulgacion__evento__fecha_inicio__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(total_items_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(0)

                max_items_year_user = User.objects.filter(
                    Q(participacioneventodivulgacion__evento__fecha_inicio__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('participacioneventodivulgacion')).aggregate(Max('participacioneventodivulgacion__count'))[
                    'participacioneventodivulgacion__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(
                    max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(participacioneventodivulgacion__evento__fecha_inicio__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('participacioneventodivulgacion')).aggregate(Min('participacioneventodivulgacion__count'))[
                    'participacioneventodivulgacion__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(min_items_year_user)
                items_data[i + 1].append(users_with_items_year_count)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            hchart_participacioneventodivulgacion = LineChart(data_source)
            context['hchart_participacioneventodivulgacion'] = hchart_participacioneventodivulgacion

            items_data = [
                ['Año', 'Total Participaciones en Programas de Radio, Television, Internet, etc.',
                 'Promedio por persona',
                 'Max por persona',
                 'Min por persona', 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = ProgramaRadioTelevisionInternet.objects.filter(fecha__year=year).filter(
                    ((Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) |
                     (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).count()

                request_user_items_year_sum = ProgramaRadioTelevisionInternet.objects.filter(fecha__year=year,
                                                                                             usuario=request.user).count()
                if not total_items_year_sum:
                    total_items_year_sum = 0
                items_data[i + 1].append(total_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(programaradiotelevisioninternet__fecha__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(total_items_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(0)

                max_items_year_user = User.objects.filter(
                    Q(programaradiotelevisioninternet__fecha__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('programaradiotelevisioninternet')).aggregate(Max('programaradiotelevisioninternet__count'))[
                    'programaradiotelevisioninternet__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(
                    max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(programaradiotelevisioninternet__fecha__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('programaradiotelevisioninternet')).aggregate(Min('programaradiotelevisioninternet__count'))[
                    'programaradiotelevisioninternet__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(min_items_year_user)
                items_data[i + 1].append(users_with_items_year_count)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            hchart_programaradiotelevisioninternet = LineChart(data_source)
            context['hchart_programaradiotelevisioninternet'] = hchart_programaradiotelevisioninternet

            items_data = [
                ['Año', 'Total Arbitrajes de Publicaciones Academicas', 'Promedio por persona', 'Max por persona',
                 'Min por persona', 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = ArbitrajePublicacionAcademica.objects.filter(fecha_dictamen__year=year).filter(
                    ((Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) |
                     (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).count()

                request_user_items_year_sum = ArbitrajePublicacionAcademica.objects.filter(fecha_dictamen__year=year,
                                                                                           usuario=request.user).count()
                if not total_items_year_sum:
                    total_items_year_sum = 0
                items_data[i + 1].append(
                    total_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(arbitrajepublicacionacademica__fecha_dictamen__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(total_items_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(0)

                max_items_year_user = User.objects.filter(
                    Q(arbitrajepublicacionacademica__fecha_dictamen__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('arbitrajepublicacionacademica')).aggregate(Max('arbitrajepublicacionacademica__count'))[
                    'arbitrajepublicacionacademica__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(
                    max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(arbitrajepublicacionacademica__fecha_dictamen__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('arbitrajepublicacionacademica')).aggregate(Min('arbitrajepublicacionacademica__count'))[
                    'arbitrajepublicacionacademica__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(min_items_year_user)
                items_data[i + 1].append(users_with_items_year_count)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            hchart_arbitrajepublicacionacademica = LineChart(data_source)
            context['hchart_arbitrajepublicacionacademica'] = hchart_arbitrajepublicacionacademica

            items_data = [
                ['Año', 'Total Arbitrajes de Proyectos de investigación', 'Promedio por persona', 'Max por persona',
                 'Min por persona', 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = ArbitrajeProyectoInvestigacion.objects.filter(fecha__year=year).filter(
                    ((Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) |
                     (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).count()

                request_user_items_year_sum = ArbitrajeProyectoInvestigacion.objects.filter(fecha__year=year,
                                                                                            usuario=request.user).count()
                if not total_items_year_sum:
                    total_items_year_sum = 0
                items_data[i + 1].append(total_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(arbitrajeproyectoinvestigacion__fecha__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(total_items_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(0)

                max_items_year_user = User.objects.filter(
                    Q(arbitrajeproyectoinvestigacion__fecha__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('arbitrajeproyectoinvestigacion')).aggregate(Max('arbitrajeproyectoinvestigacion__count'))[
                    'arbitrajeproyectoinvestigacion__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(
                    max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(arbitrajeproyectoinvestigacion__fecha__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('arbitrajeproyectoinvestigacion')).aggregate(Min('arbitrajeproyectoinvestigacion__count'))[
                    'arbitrajeproyectoinvestigacion__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(min_items_year_user)
                items_data[i + 1].append(users_with_items_year_count)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            hchart_arbitrajeproyectoinvestigacion = LineChart(data_source)
            context['hchart_arbitrajeproyectoinvestigacion'] = hchart_arbitrajeproyectoinvestigacion

            items_data = [['Año', 'Total horas de docencia escolarizada', 'Promedio horas', 'Max horas', 'Min horas',
                           'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(last_x_years[i])])

                users_with_items_year_count = User.objects.filter(
                    Q(curso_docencia_escolarizado_usuario__fecha_inicio__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0

                total_hours_year_sum = \
                    CursoDocenciaEscolarizado.objects.filter(fecha_inicio__year=year).filter((
                        (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) |
                        (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).aggregate(
                        Sum('total_horas'))[
                        'total_horas__sum']
                if total_hours_year_sum == None:
                    total_hours_year_sum = 0

                request_user_years_year_sum = User.objects.filter(curso_docencia_escolarizado_usuario__fecha_inicio__year=year,
                                                                  curso_docencia_escolarizado_usuario__usuario=request.user).aggregate(
                    Sum('curso_docencia_escolarizado_usuario__total_horas'))['curso_docencia_escolarizado_usuario__total_horas__sum']

                if not total_hours_year_sum:
                    total_hours_year_sum = 0
                items_data[i + 1].append(total_hours_year_sum)

                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(round(total_hours_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(round(0, 2))

                max_item_year_user = User.objects.filter(curso_docencia_escolarizado_usuario__fecha_inicio__year=year).annotate(
                    Sum('curso_docencia_escolarizado_usuario__total_horas')).filter((
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).aggregate(
                    Max('curso_docencia_escolarizado_usuario__total_horas__sum'))[
                    'curso_docencia_escolarizado_usuario__total_horas__sum__max']
                if max_item_year_user == None:
                    max_item_year_user = 0
                items_data[i + 1].append(max_item_year_user)

                min_item_year_user = User.objects.filter(curso_docencia_escolarizado_usuario__fecha_inicio__year=year).annotate(
                    Sum('curso_docencia_escolarizado_usuario__total_horas')).filter((
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).aggregate(
                    Min('curso_docencia_escolarizado_usuario__total_horas__sum'))[
                    'curso_docencia_escolarizado_usuario__total_horas__sum__min']
                if not min_item_year_user:
                    min_item_year_user = 0
                items_data[i + 1].append(min_item_year_user)
                items_data[i + 1].append(users_with_items_year_count)

            data_source = SimpleDataSource(data=items_data)
            hchart_cursodocencia_escolarizado = LineChart(data_source)
            context['hchart_cursodocencia_escolarizado'] = hchart_cursodocencia_escolarizado

            items_data = [['Año', 'Total horas de docencia extracurricular', 'Promedio horas', 'Max horas', 'Min horas',
                           'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(last_x_years[i])])

                users_with_items_year_count = User.objects.filter(
                    Q(curso_docencia_extracurricular_usuario__fecha_inicio__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0

                total_hours_year_sum = \
                    CursoDocenciaExtracurricular.objects.filter(fecha_inicio__year=year).filter((
                        (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) |
                        (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).aggregate(
                        Sum('total_horas'))[
                        'total_horas__sum']
                if total_hours_year_sum == None:
                    total_hours_year_sum = 0

                request_user_years_year_sum = User.objects.filter(curso_docencia_extracurricular_usuario__fecha_inicio__year=year,
                                                                  curso_docencia_extracurricular_usuario__usuario=request.user).aggregate(
                    Sum('curso_docencia_extracurricular_usuario__total_horas'))['curso_docencia_extracurricular_usuario__total_horas__sum']

                if not total_hours_year_sum:
                    total_hours_year_sum = 0
                items_data[i + 1].append(total_hours_year_sum)

                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(round(total_hours_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(round(0, 2))

                max_item_year_user = User.objects.filter(curso_docencia_extracurricular_usuario__fecha_inicio__year=year).annotate(
                    Sum('curso_docencia_extracurricular_usuario__total_horas')).filter((
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).aggregate(
                    Max('curso_docencia_extracurricular_usuario__total_horas__sum'))[
                    'curso_docencia_extracurricular_usuario__total_horas__sum__max']
                if max_item_year_user == None:
                    max_item_year_user = 0
                items_data[i + 1].append(max_item_year_user)

                min_item_year_user = User.objects.filter(curso_docencia_extracurricular_usuario__fecha_inicio__year=year).annotate(
                    Sum('curso_docencia_extracurricular_usuario__total_horas')).filter((
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).aggregate(
                    Min('curso_docencia_extracurricular_usuario__total_horas__sum'))[
                    'curso_docencia_extracurricular_usuario__total_horas__sum__min']
                if not min_item_year_user:
                    min_item_year_user = 0
                items_data[i + 1].append(min_item_year_user)
                items_data[i + 1].append(users_with_items_year_count)

            data_source = SimpleDataSource(data=items_data)
            hchart_cursodocencia_extracurricular = LineChart(data_source)
            context['hchart_cursodocencia_extracurricular'] = hchart_cursodocencia_extracurricular

            items_data = [
                ['Año', 'Total desarrollos tecnológicos', 'Promedio por persona', 'Max por persona', 'Min por persona',
                 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = DesarrolloTecnologico.objects.filter(fecha__year=year).filter(
                    ((Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad__year__gt=year)) |
                     (Q(autores__ingreso_entidad__year__lte=year) & Q(autores__egreso_entidad=None)))).count()

                request_user_items_year_sum = DesarrolloTecnologico.objects.filter(fecha__year=year,
                                                                                   autores=request.user).count()
                if not total_items_year_sum:
                    total_items_year_sum = 0
                items_data[i + 1].append(total_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(desarrollo_tecnologico_autores__fecha__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(
                            total_items_year_sum / users_with_items_year_count,
                            2))
                else:
                    items_data[i + 1].append(0)

                max_items_year_user = User.objects.filter(
                    Q(desarrollo_tecnologico_autores__fecha__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('desarrollo_tecnologico_autores')).aggregate(Max('desarrollo_tecnologico_autores__count'))[
                    'desarrollo_tecnologico_autores__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(
                    max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(desarrollo_tecnologico_autores__fecha__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('desarrollo_tecnologico_autores')).aggregate(Min('desarrollo_tecnologico_autores__count'))[
                    'desarrollo_tecnologico_autores__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(min_items_year_user)
                items_data[i + 1].append(users_with_items_year_count)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            hchart_desarrollo_tecnologico = LineChart(data_source)
            context['hchart_desarrollo_tecnologico'] = hchart_desarrollo_tecnologico

            items_data = [
                ['Año', 'Total distinciones', 'Promedio por persona', 'Max por persona', 'Min por persona',
                 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = DistincionAcademico.objects.filter(fecha__year=year).filter(
                    ((Q(usuario__ingreso_entidad__year__lte=year) & Q(
                        usuario__egreso_entidad__year__gt=year)) |
                     (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).count()

                request_user_items_year_sum = DistincionAcademico.objects.filter(fecha__year=year,
                                                                                 usuario=request.user).count()
                if not total_items_year_sum:
                    total_items_year_sum = 0
                items_data[i + 1].append(total_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(distincion_academico_usuario__fecha__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(
                        round(
                            total_items_year_sum / users_with_items_year_count,
                            2))
                else:
                    items_data[i + 1].append(0)

                max_items_year_user = User.objects.filter(
                    Q(distincion_academico_usuario__fecha__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('distincion_academico_usuario')).aggregate(
                    Max('distincion_academico_usuario__count'))[
                    'distincion_academico_usuario__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(max_items_year_user)
                items_data[i + 1].append(users_with_items_year_count)

                min_items_year_user = User.objects.filter(
                    Q(distincion_academico_usuario__fecha__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('distincion_academico_usuario')).aggregate(
                    Min('distincion_academico_usuario__count'))[
                    'distincion_academico_usuario__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(
                    min_items_year_user)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            hchart_distincion_academicos = LineChart(data_source)
            context['hchart_distincion_academicos'] = hchart_distincion_academicos

        return render(request, self.template_name, context)


class InformeActividades(View):
    form_class = None
    template_name = 'informe_actividades.html'
    aux = {}
    this_year = datetime.now().year

    def get(self, request):
        context = {}
        this_year = self.this_year

        if request.user.is_staff:

            # concluidos año anterior conacyt:
            proy_pasty_conc_conacyt = ProyectoInvestigacion.objects.filter(
                financiamiento_conacyt__isnull=False).filter(
                Q(fecha_fin__year=this_year - 2) | Q(fecha_fin__year=this_year - 1)).count()

            # concluidos año anterior papiit:
            proy_pasty_conc_papiit = ProyectoInvestigacion.objects.filter(
                financiamiento_papiit__isnull=False).filter(
                Q(fecha_fin__year=this_year - 2) | Q(fecha_fin__year=this_year - 1)).count()

            # concluidos año anterior ingresos ext, nacionales:
            proy_pasty_conc_extnal = ProyectoInvestigacion.objects.filter(
                financiamiento_conacyt__isnull=True, financiamiento_papiit__isnull=True).filter(
                Q(financiamientos__institucion__pais__nombre='México')).filter(
                Q(fecha_fin__year=this_year - 2) | Q(fecha_fin__year=this_year - 1)).annotate(
                Count('pk', distinct=True)).count()

            # concluidos año anterior ingresos ext, internacionales:
            proy_pasty_conc_extint_tmp = ProyectoInvestigacion.objects.filter(
                financiamiento_conacyt__isnull=True, financiamiento_papiit__isnull=True).filter(
                Q(fecha_fin__year=this_year - 2) | Q(fecha_fin__year=this_year - 1))
            proy_pasty_conc_extint = 0
            for i in proy_pasty_conc_extint_tmp:

                paises = []
                for j in i.financiamientos.all():
                    if j.institucion.pais.nombre not in paises:
                        paises.append(j.institucion.pais.nombre)
                if 'México' in paises and len(paises) > 1 or 'México' not in paises and len(paises) > 0:
                    proy_pasty_conc_extint += 1
                    # print(paises)

            # en proceso año anterior conacyt:
            proy_pasty_proc_conacyt = ProyectoInvestigacion.objects.filter(
                financiamiento_conacyt__isnull=False).filter(
                Q(fecha_fin__year__gt=this_year - 1) | Q(fecha_fin=None)).count()

            # en proceso año anterior papiit:
            proy_pasty_proc_papiit = ProyectoInvestigacion.objects.filter(
                financiamiento_papiit__isnull=False).filter(
                Q(fecha_fin__year__gt=this_year - 1) | Q(fecha_fin=None)).count()

            # en proceso año anterior ingresos ext, nacionales:
            proy_pasty_proc_extnal = ProyectoInvestigacion.objects.filter(
                financiamiento_conacyt__isnull=True, financiamiento_papiit__isnull=True).filter(
                Q(fecha_fin__year__gt=this_year - 1) | Q(fecha_fin=None)).filter(
                Q(financiamientos__institucion__pais__nombre='México')).annotate(Count('pk', distinct=True)).count()

            # en proceso año anterior ingresos ext, internacionales:
            proy_pasty_proc_extint_tmp = ProyectoInvestigacion.objects.filter(
                financiamiento_conacyt__isnull=True, financiamiento_papiit__isnull=True).filter(
                Q(fecha_fin__year__gt=this_year - 1) | Q(fecha_fin=None))
            proy_pasty_proc_extint = 0
            for i in proy_pasty_proc_extint_tmp:

                paises = []
                for j in i.financiamientos.all():
                    if j.institucion.pais.nombre not in paises:
                        paises.append(j.institucion.pais.nombre)
                if 'México' in paises and len(paises) > 1 or 'México' not in paises and len(paises) > 0:
                    proy_pasty_proc_extint += 1
                    # print(paises)

            # concluidos este año conacyt:
            proy_thisy_conc_conacyt = ProyectoInvestigacion.objects.filter(
                fecha_fin__year=this_year, financiamiento_conacyt__isnull=False).count()

            # concluidos este año papiit:
            proy_thisy_conc_papiit = ProyectoInvestigacion.objects.filter(
                fecha_fin__year=this_year, financiamiento_papiit__isnull=False).count()

            # concluidos este año ingresos ext, nacionales:
            proy_thisy_conc_extnal = ProyectoInvestigacion.objects.filter(
                fecha_fin__year=this_year, financiamiento_conacyt__isnull=True,
                financiamiento_papiit__isnull=True).filter(
                Q(financiamientos__institucion__pais__nombre='México')).annotate(
                Count('pk', distinct=True)).count()

            # concluidos este año ingresos ext, internacionales:
            proy_thisy_conc_extint_tmp = ProyectoInvestigacion.objects.filter(
                fecha_fin__year=this_year, financiamiento_conacyt__isnull=True,
                financiamiento_papiit__isnull=True)
            proy_thisy_conc_extint = 0
            for i in proy_thisy_conc_extint_tmp:

                paises = []
                for j in i.financiamientos.all():
                    if j.institucion.pais.nombre not in paises:
                        paises.append(j.institucion.pais.nombre)
                if 'México' in paises and len(paises) > 1 or 'México' not in paises and len(paises) > 0:
                    proy_thisy_conc_extint += 1
                    # print(paises)

            # en proceso este año conacyt:
            proy_thisy_proc_conacyt = ProyectoInvestigacion.objects.filter(
                financiamiento_conacyt__isnull=False, fecha_fin=None).count()

            # en proceso este año papiit:
            proy_thisy_proc_papiit = ProyectoInvestigacion.objects.filter(
                financiamiento_papiit__isnull=False, fecha_fin=None).count()

            # en proceso este año ingresos ext, nacionales:
            proy_thisy_proc_extnal = ProyectoInvestigacion.objects.filter(
                financiamiento_conacyt__isnull=True, financiamiento_papiit__isnull=True, fecha_fin=None).filter(
                Q(financiamientos__institucion__pais__nombre='México')).annotate(
                Count('pk', distinct=True)).count()

            # en proceso este año ingresos ext, internacionales:
            proy_thisy_proc_extint_tmp = ProyectoInvestigacion.objects.filter(
                financiamiento_conacyt__isnull=True, financiamiento_papiit__isnull=True, fecha_fin=None)
            proy_thisy_proc_extint = 0
            for i in proy_thisy_proc_extint_tmp:

                paises = []
                for j in i.financiamientos.all():
                    if j.institucion.pais.nombre not in paises:
                        paises.append(j.institucion.pais.nombre)
                if 'México' in paises and len(paises) > 1 or 'México' not in paises and len(paises) > 0:
                    proy_thisy_proc_extint += 1
                    # print(paises)

            conc_pastyl = 'Concluidos ' + str(this_year - 2) + "-" + str(this_year - 1)
            proc_pastyl = 'En proceso ' + str(this_year - 2) + "-" + str(this_year - 1)
            conc_thisyl = 'Concluidos ' + str(this_year - 1) + "-" + str(this_year)
            proc_thisyl = 'En proceso ' + str(this_year - 1) + "-" + str(this_year)

            proyectos = [['Etiqueta', 'CONACYT', 'PAPIIT', 'Ext. Nacional', 'Ext. Internacional'],
                         [conc_pastyl, proy_pasty_conc_conacyt, proy_pasty_conc_papiit, proy_pasty_conc_extnal,
                          proy_pasty_conc_extint],
                         [proc_pastyl, proy_pasty_proc_conacyt, proy_pasty_proc_papiit, proy_pasty_proc_extnal,
                          proy_pasty_proc_extint],
                         [conc_thisyl, proy_thisy_conc_conacyt, proy_thisy_conc_papiit, proy_thisy_conc_extnal,
                          proy_thisy_conc_extint],
                         [proc_thisyl, proy_thisy_proc_conacyt, proy_thisy_proc_papiit, proy_thisy_proc_extnal,
                          proy_thisy_proc_extint],
                         ]

            data_source = SimpleDataSource(data=proyectos)
            chart_proyectos_investigacion = BarChart(data_source)
            context['chart_proyectos_investigacion'] = chart_proyectos_investigacion

            invest_en_proyectos_ant = User.objects.filter(tipo='INVESTIGADOR').filter(
                Q(proyecto_investigacion_responsables__fecha_inicio__year__lte=this_year - 1) &
                (Q(proyecto_investigacion_responsables__fecha_fin__year__gte=this_year - 1) |
                 Q(proyecto_investigacion_responsables__fecha_fin=None))).filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).annotate(
                Count('pk', distinct=True)).count()

            invest_activos_ant = User.objects.filter(tipo='INVESTIGADOR').filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).annotate(
                Count('pk', distinct=True)).count()

            if invest_activos_ant == 0:
                invest_activos_ant = 0.001

            invest_perc_ant = round(invest_en_proyectos_ant / invest_activos_ant, 2)

            invest_en_proyectos_act = User.objects.filter(tipo='INVESTIGADOR').filter(
                Q(proyecto_investigacion_responsables__fecha_inicio__year__gte=this_year - 1) &
                (Q(proyecto_investigacion_responsables__fecha_fin__year__gte=this_year - 1) |
                 Q(proyecto_investigacion_responsables__fecha_fin=None))).filter(
                (Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad__year=this_year)) | (
                    Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad=None))).annotate(
                Count('pk', distinct=True)).count()

            invest_activos_act = User.objects.filter(tipo='INVESTIGADOR').filter(
                (Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad__year=this_year)) | (
                    Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad=None))).annotate(
                Count('pk', distinct=True)).count()

            if invest_activos_act == 0:
                invest_activos_act = 0.001
            invest_perc_act = round(invest_en_proyectos_act / invest_activos_act, 2)

            tecnicos_en_proyectos_ant = User.objects.filter(tipo='TECNICO').filter(
                Q(proyecto_investigacion_responsables__fecha_inicio__year__lte=this_year - 1) &
                (Q(proyecto_investigacion_responsables__fecha_fin__year__gte=this_year - 1) |
                 Q(proyecto_investigacion_responsables__fecha_fin=None))).filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).annotate(
                Count('pk', distinct=True)).count()

            tecnicos_activos_ant = User.objects.filter(tipo='TECNICO').filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).annotate(
                Count('pk', distinct=True)).count()

            if tecnicos_activos_ant == 0:
                tecnicos_activos_ant = 0.001

            tec_perc_ant = round(tecnicos_en_proyectos_ant / tecnicos_activos_ant, 2) * 100

            tecnicos_en_proyectos_act = User.objects.filter(tipo='TECNICO').filter(
                Q(proyecto_investigacion_responsables__fecha_inicio__year__gte=this_year - 1) &
                (Q(proyecto_investigacion_responsables__fecha_fin__year__gte=this_year - 1) |
                 Q(proyecto_investigacion_responsables__fecha_fin=None))).filter(
                (Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad__year=this_year)) | (
                    Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad=None))).annotate(
                Count('pk', distinct=True)).count()

            tecnicos_activos_act = User.objects.filter(tipo='TECNICO').filter(
                (Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad__year=this_year)) | (
                    Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad=None))).annotate(
                Count('pk', distinct=True)).count()

            if tecnicos_activos_act == 0:
                tecnicos_activos_act = 0.001

            tec_perc_act = round(tecnicos_en_proyectos_act / tecnicos_activos_act, 2) * 100

            proy_financiados_ant = ProyectoInvestigacion.objects.filter(
                Q(financiamientos__isnull=False) |
                Q(financiamiento_conacyt__isnull=False) |
                Q(financiamiento_papiit__isnull=False)).filter(
                (Q(fecha_inicio__year=this_year - 2) |
                 Q(fecha_inicio__year=this_year - 1)) &
                (Q(fecha_fin__year=this_year - 1) |
                 Q(fecha_fin__year=this_year))).annotate(
                Count('pk', distinct=True)).count()

            proy_financiados_act = ProyectoInvestigacion.objects.filter(
                Q(financiamientos__isnull=False) |
                Q(financiamiento_conacyt__isnull=False) |
                Q(financiamiento_papiit__isnull=False)).filter(
                (Q(fecha_inicio__year=this_year - 1) |
                 Q(fecha_inicio__year=this_year)) &
                (Q(fecha_fin__year=this_year) |
                 Q(fecha_fin=None))).annotate(
                Count('pk', distinct=True)).count()

            proy_tot_ant = ProyectoInvestigacion.objects.filter(
                (Q(fecha_inicio__year=this_year - 2) |
                 Q(fecha_inicio__year=this_year - 1)) &
                (Q(fecha_fin__year=this_year - 1) |
                 Q(fecha_fin__year=this_year))).annotate(
                Count('pk', distinct=True)).count()

            proy_tot_act = ProyectoInvestigacion.objects.filter(
                (Q(fecha_inicio__year=this_year - 1) |
                 Q(fecha_inicio__year=this_year)) &
                (Q(fecha_fin__year=this_year) |
                 Q(fecha_fin=None))).annotate(
                Count('pk', distinct=True)).count()
            try:
                proy_ant_perc = round(proy_financiados_ant / proy_tot_ant, 2) * 100
            except:
                proy_ant_perc = 0
            try:
                proy_act_perc = round(proy_financiados_act / proy_tot_act, 2) * 100
            except:
                proy_act_perc = 0

            context['this_year'] = this_year
            context['this_year_1'] = this_year - 1
            context['this_year_2'] = this_year - 2

            proyectos = [['Etiqueta', 'CONACYT', 'PAPIIT', 'Ext. Nacional', 'Ext. Internacional'],
                         [conc_pastyl, proy_pasty_conc_conacyt, proy_pasty_conc_papiit, proy_pasty_conc_extnal,
                          proy_pasty_conc_extint],
                         [proc_pastyl, proy_pasty_proc_conacyt, proy_pasty_proc_papiit, proy_pasty_proc_extnal,
                          proy_pasty_proc_extint],
                         [conc_thisyl, proy_thisy_conc_conacyt, proy_thisy_conc_papiit, proy_thisy_conc_extnal,
                          proy_thisy_conc_extint],
                         [proc_thisyl, proy_thisy_proc_conacyt, proy_thisy_proc_papiit, proy_thisy_proc_extnal,
                          proy_thisy_proc_extint],
                         ]

            context['table_proyectos'] = {'proy_pasty_conc_conacyt': proy_pasty_conc_conacyt,
                                          'proy_pasty_conc_papiit': proy_pasty_conc_papiit,
                                          'proy_pasty_conc_extnal': proy_pasty_conc_extnal,
                                          'proy_pasty_conc_extint': proy_pasty_conc_extint,
                                          'proy_thisy_conc_conacyt': proy_thisy_conc_conacyt,
                                          'proy_thisy_conc_papiit': proy_thisy_conc_papiit,
                                          'proy_thisy_conc_extnal': proy_thisy_conc_extnal,
                                          'proy_thisy_conc_extint': proy_thisy_conc_extint,
                                          'proy_thisy_proc_conacyt': proy_thisy_proc_conacyt,
                                          'proy_thisy_proc_papiit': proy_thisy_proc_papiit,
                                          'proy_thisy_proc_extnal': proy_thisy_proc_extnal,
                                          'proy_thisy_proc_extint': proy_thisy_proc_extint,
                                          'invest_perc_ant': invest_perc_ant, 'invest_perc_act': invest_perc_act,
                                          'tec_perc_ant': tec_perc_ant, 'tec_perc_act': tec_perc_act,
                                          'proy_financiados_ant': proy_financiados_ant, 'proy_ant_perc': proy_ant_perc,
                                          'proy_financiados_act': proy_financiados_act,
                                          'proy_act_perc': proy_act_perc, }

            proythisy_count = ProyectoInvestigacion.objects.filter(fecha_inicio__year__gte=this_year - 1).count()
            p_proythisy_count = ProyectoInvestigacion.objects.filter(fecha_inicio__year__gte=this_year - 2,
                                                                     fecha_fin__year__lte=this_year - 1).count()

            if proythisy_count == 0:
                proythisy_count = 0.001
            if p_proythisy_count == 0:
                p_proythisy_count = 0.001

            proymod_disc = ProyectoInvestigacion.objects.filter(modalidad='DISCIPLINARIO',
                                                                fecha_inicio__year__gte=this_year - 1).count()
            proymod_mult = ProyectoInvestigacion.objects.filter(modalidad='MULTIDISCIPLINARIO',
                                                                fecha_inicio__year__gte=this_year - 1).count()
            proymod_inter = ProyectoInvestigacion.objects.filter(modalidad='INTERDISCIPLINARIO',
                                                                 fecha_inicio__year__gte=this_year - 1).count()
            proymod_trans = ProyectoInvestigacion.objects.filter(modalidad='TRANSDISCIPLINARIO',
                                                                 fecha_inicio__year__gte=this_year - 1).count()

            proymod_discp = round(proymod_disc / proythisy_count * 100, 2)
            proymod_multp = round(proymod_mult / proythisy_count * 100, 2)
            proymod_interp = round(proymod_inter / proythisy_count * 100, 2)
            proymod_transp = round(proymod_trans / proythisy_count * 100, 2)

            proymod_data = [['Modalidad', 'Porcentaje'],
                            ['Disciplinario', proymod_discp],
                            ['Multidisciplinario', proymod_multp],
                            ['Interdisciplinario', proymod_interp],
                            ['Transdisciplinario', proymod_transp]
                            ]

            data_source = SimpleDataSource(data=proymod_data)
            chart_modalidad_proyectos = DonutChart(data_source)
            context['chart_modalidad_proyectos'] = chart_modalidad_proyectos

            p_proymod_disc = ProyectoInvestigacion.objects.filter(modalidad='DISCIPLINARIO',
                                                                  fecha_inicio__year__gte=this_year - 2,
                                                                  fecha_fin__year__lte=this_year - 1).count()
            p_proymod_mult = ProyectoInvestigacion.objects.filter(modalidad='MULTIDISCIPLINARIO',
                                                                  fecha_inicio__year__gte=this_year - 2,
                                                                  fecha_fin__year__lte=this_year - 1).count()
            p_proymod_inter = ProyectoInvestigacion.objects.filter(modalidad='INTERDISCIPLINARIO',
                                                                   fecha_inicio__year__gte=this_year - 2,
                                                                   fecha_fin__year__lte=this_year - 1).count()
            p_proymod_trans = ProyectoInvestigacion.objects.filter(modalidad='TRANSDISCIPLINARIO',
                                                                   fecha_inicio__year__gte=this_year - 2,
                                                                   fecha_fin__year__lte=this_year - 1).count()

            p_proymod_discp = round(p_proymod_disc / p_proythisy_count * 100, 2)
            p_proymod_multp = round(p_proymod_mult / p_proythisy_count * 100, 2)
            p_proymod_interp = round(p_proymod_inter / p_proythisy_count * 100, 2)
            p_proymod_transp = round(p_proymod_trans / p_proythisy_count * 100, 2)

            p_proymod_data = [['Modalidad', 'Porcentaje'],
                              ['Disciplinario', p_proymod_discp],
                              ['Multidisciplinario', p_proymod_multp],
                              ['Interdisciplinario', p_proymod_interp],
                              ['Transdisciplinario', p_proymod_transp]
                              ]

            data_source = SimpleDataSource(data=p_proymod_data)
            p_chart_modalidad_proyectos = DonutChart(data_source)
            context['p_chart_modalidad_proyectos'] = p_chart_modalidad_proyectos

            context['table_proyectos_modalidad'] = {'proymod_disc': proymod_disc,
                                                    'proymod_mult': proymod_mult,
                                                    'proymod_inter': proymod_inter,
                                                    'proymod_trans': proymod_trans,
                                                    'proymod_discp': proymod_discp,
                                                    'proymod_multp': proymod_multp,
                                                    'proymod_interp': proymod_interp,
                                                    'proymod_transp': proymod_transp,
                                                    'p_proymod_disc': p_proymod_disc,
                                                    'p_proymod_mult': p_proymod_mult,
                                                    'p_proymod_inter': p_proymod_inter,
                                                    'p_proymod_trans': p_proymod_trans,
                                                    'p_proymod_discp': p_proymod_discp,
                                                    'p_proymod_multp': p_proymod_multp,
                                                    'p_proymod_interp': p_proymod_interp,
                                                    'p_proymod_transp': p_proymod_transp,
                                                    }

            proyorg_ind = ProyectoInvestigacion.objects.filter(organizacion='INDIVIDUAL',
                                                               fecha_inicio__year__gte=this_year - 1).count()
            proyorg_col = ProyectoInvestigacion.objects.filter(organizacion='COLECTIVO',
                                                               fecha_inicio__year__gte=this_year - 1).count()
            proyorg_indp = round(proyorg_ind / proythisy_count * 100, 2)
            proyorg_colp = round(proyorg_col / proythisy_count * 100, 2)

            proymod_data = [['Organización', 'Porcentaje'],
                            ['Individual', proyorg_indp],
                            ['Colectivo', proyorg_colp]
                            ]

            data_source = SimpleDataSource(data=proymod_data)
            chart_organizacion_proyectos = DonutChart(data_source)
            context['chart_organizacion_proyectos'] = chart_organizacion_proyectos

            p_proyorg_ind = ProyectoInvestigacion.objects.filter(organizacion='INDIVIDUAL',
                                                                 fecha_inicio__year__gte=this_year - 2,
                                                                 fecha_fin__year__lte=this_year - 1).count()
            p_proyorg_col = ProyectoInvestigacion.objects.filter(organizacion='COLECTIVO',
                                                                 fecha_inicio__year__gte=this_year - 2,
                                                                 fecha_fin__year__lte=this_year - 1).count()
            p_proyorg_indp = round(p_proyorg_ind / p_proythisy_count * 100, 2)
            p_proyorg_colp = round(p_proyorg_col / p_proythisy_count * 100, 2)

            proymod_data = [['Organización', 'Porcentaje'],
                            ['Individual', p_proyorg_indp],
                            ['Colectivo', p_proyorg_colp]
                            ]

            data_source = SimpleDataSource(data=proymod_data)
            p_chart_organizacion_proyectos = DonutChart(data_source)
            context['p_chart_organizacion_proyectos'] = p_chart_organizacion_proyectos

            context['table_proyectos_organizacion'] = {'proyorg_ind': proyorg_ind,
                                                       'proyorg_col': proyorg_col,
                                                       'proyorg_indp': proyorg_indp,
                                                       'proyorg_colp': proyorg_colp,
                                                       'p_proyorg_ind': p_proyorg_ind,
                                                       'p_proyorg_col': p_proyorg_col,
                                                       'p_proyorg_indp': p_proyorg_indp,
                                                       'p_proyorg_colp': p_proyorg_colp,
                                                       }

            proygen_y = ProyectoInvestigacion.objects.filter(tematica_genero=True,
                                                             fecha_inicio__year__gte=this_year - 1).count()
            proygen_n = ProyectoInvestigacion.objects.filter(tematica_genero=False,
                                                             fecha_inicio__year__gte=this_year - 1).count()

            proygen_yp = round(proygen_y / proythisy_count * 100, 2)
            proygen_np = round(proygen_n / proythisy_count * 100, 2)

            proymod_data = [['Enfoque de género', 'Porcentaje'],
                            ['Si', proygen_yp],
                            ['No', proygen_np]
                            ]

            data_source = SimpleDataSource(data=proymod_data)
            chart_genero_proyectos = DonutChart(data_source)
            context['chart_genero_proyectos'] = chart_genero_proyectos

            p_proygen_y = ProyectoInvestigacion.objects.filter(tematica_genero=True,
                                                               fecha_inicio__year__gte=this_year - 2,
                                                               fecha_fin__year__lte=this_year - 1).count()
            p_proygen_n = ProyectoInvestigacion.objects.filter(tematica_genero=False,
                                                               fecha_inicio__year__gte=this_year - 2,
                                                               fecha_fin__year__lte=this_year - 1).count()

            p_proygen_yp = round(p_proygen_y / p_proythisy_count * 100, 2)
            p_proygen_np = round(p_proygen_n / p_proythisy_count * 100, 2)

            proymod_data = [['Enfoque de género', 'Porcentaje'],
                            ['Si', p_proygen_yp],
                            ['No', p_proygen_np]
                            ]

            data_source = SimpleDataSource(data=proymod_data)
            p_chart_genero_proyectos = DonutChart(data_source)
            context['p_chart_genero_proyectos'] = p_chart_genero_proyectos

            context['table_proyectos_genero'] = {'proygen_y': proygen_y,
                                                 'proygen_n': proygen_n,
                                                 'proygen_yp': proygen_yp,
                                                 'proygen_np': proygen_np,
                                                 'p_proygen_y': p_proygen_y,
                                                 'p_proygen_n': p_proygen_n,
                                                 'p_proygen_yp': p_proygen_yp,
                                                 'p_proygen_np': p_proygen_np,
                                                 }

            p_gestion_agua = ProyectoInvestigacion.objects.filter(
                problema_nacional_conacyt__nombre='Gestión integral del agua, seguridad hídrica y derecho del agua',
                fecha_inicio__year__gte=this_year - 2, fecha_fin__year__lte=this_year - 1).count()
            gestion_agua = ProyectoInvestigacion.objects.filter(
                problema_nacional_conacyt__nombre='Gestión integral del agua, seguridad hídrica y derecho del agua',
                fecha_inicio__year__gte=this_year - 1).count()

            p_mitigacion_cambio_climatico = ProyectoInvestigacion.objects.filter(
                problema_nacional_conacyt__nombre='Mitigación y adaptación al cambio climático',
                fecha_inicio__year__gte=this_year - 2, fecha_fin__year__lte=this_year - 1).count()
            mitigacion_cambio_climatico = ProyectoInvestigacion.objects.filter(
                problema_nacional_conacyt__nombre='Mitigación y adaptación al cambio climático',
                fecha_inicio__year__gte=this_year - 1).count()

            p_resiliencia_desastres_nt = ProyectoInvestigacion.objects.filter(
                problema_nacional_conacyt__nombre='Resiliencia frente a desastres naturales y tecnológicos',
                fecha_inicio__year__gte=this_year - 2, fecha_fin__year__lte=this_year - 1).count()
            resiliencia_desastres_nt = ProyectoInvestigacion.objects.filter(
                problema_nacional_conacyt__nombre='Resiliencia frente a desastres naturales y tecnológicos',
                fecha_inicio__year__gte=this_year - 1).count()

            p_aprovechamiento_ecosistemas = ProyectoInvestigacion.objects.filter(
                problema_nacional_conacyt__nombre='Aprovechamiento y protección de ecosistemas y de la biodiversidad',
                fecha_inicio__year__gte=this_year - 2, fecha_fin__year__lte=this_year - 1).count()
            aprovechamiento_ecosistemas = ProyectoInvestigacion.objects.filter(
                problema_nacional_conacyt__nombre='Aprovechamiento y protección de ecosistemas y de la biodiversidad',
                fecha_inicio__year__gte=this_year - 1).count()

            p_oceanos_aprovechamiento = ProyectoInvestigacion.objects.filter(
                problema_nacional_conacyt__nombre='Los océanos y su aprovechamiento',
                fecha_inicio__year__gte=this_year - 2, fecha_fin__year__lte=this_year - 1).count()
            oceanos_aprovechamiento = ProyectoInvestigacion.objects.filter(
                problema_nacional_conacyt__nombre='Los océanos y su aprovechamiento',
                fecha_inicio__year__gte=this_year - 1).count()

            p_alimentos_produccion = ProyectoInvestigacion.objects.filter(
                problema_nacional_conacyt__nombre='Alimentos y su producción',
                fecha_inicio__year__gte=this_year - 2, fecha_fin__year__lte=this_year - 1).count()
            alimentos_produccion = ProyectoInvestigacion.objects.filter(
                problema_nacional_conacyt__nombre='Alimentos y su producción',
                fecha_inicio__year__gte=this_year - 1).count()

            p_ciudades_desarrollo_urbano = ProyectoInvestigacion.objects.filter(
                problema_nacional_conacyt__nombre='Ciudades y desarrollo urbano',
                fecha_inicio__year__gte=this_year - 2, fecha_fin__year__lte=this_year - 1).count()
            ciudades_desarrollo_urbano = ProyectoInvestigacion.objects.filter(
                problema_nacional_conacyt__nombre='Ciudades y desarrollo urbano',
                fecha_inicio__year__gte=this_year - 1).count()

            p_conectividad_informatica = ProyectoInvestigacion.objects.filter(
                problema_nacional_conacyt__nombre='Conectividad informática y desarrollo de las tecnologías de la información, la comunicación y las telecomunicaciones',
                fecha_inicio__year__gte=this_year - 2, fecha_fin__year__lte=this_year - 1).count()
            conectividad_informatica = ProyectoInvestigacion.objects.filter(
                problema_nacional_conacyt__nombre='Conectividad informática y desarrollo de las tecnologías de la información, la comunicación y las telecomunicaciones',
                fecha_inicio__year__gte=this_year - 1).count()

            p_manufactura_alta_tecnologia = ProyectoInvestigacion.objects.filter(
                problema_nacional_conacyt__nombre='Manufactura de alta tecnología',
                fecha_inicio__year__gte=this_year - 2, fecha_fin__year__lte=this_year - 1).count()
            manufactura_alta_tecnologia = ProyectoInvestigacion.objects.filter(
                problema_nacional_conacyt__nombre='Manufactura de alta tecnología',
                fecha_inicio__year__gte=this_year - 1).count()

            p_consumo_sustentable_energia = ProyectoInvestigacion.objects.filter(
                problema_nacional_conacyt__nombre='Consumo sustentable de energía',
                fecha_inicio__year__gte=this_year - 2, fecha_fin__year__lte=this_year - 1).count()
            consumo_sustentable_energia = ProyectoInvestigacion.objects.filter(
                problema_nacional_conacyt__nombre='Consumo sustentable de energía',
                fecha_inicio__year__gte=this_year - 1).count()

            p_aprovechamiento_energias_renovables = ProyectoInvestigacion.objects.filter(
                problema_nacional_conacyt__nombre='Desarrollo y aprovechamiento de energías renovables limpias, conducta humana y prevención de adicciones',
                fecha_inicio__year__gte=this_year - 2, fecha_fin__year__lte=this_year - 1).count()
            aprovechamiento_energias_renovables = ProyectoInvestigacion.objects.filter(
                problema_nacional_conacyt__nombre='Desarrollo y aprovechamiento de energías renovables limpias, conducta humana y prevención de adicciones',
                fecha_inicio__year__gte=this_year - 1).count()

            p_enfermedades_emergentes = ProyectoInvestigacion.objects.filter(
                problema_nacional_conacyt__nombre='Enfermedades emergentes y de importancia nacional',
                fecha_inicio__year__gte=this_year - 2, fecha_fin__year__lte=this_year - 1).count()
            enfermedades_emergentes = ProyectoInvestigacion.objects.filter(
                problema_nacional_conacyt__nombre='Enfermedades emergentes y de importancia nacional',
                fecha_inicio__year__gte=this_year - 1).count()

            p_combate_pobreza = ProyectoInvestigacion.objects.filter(
                problema_nacional_conacyt__nombre='Combate a la pobreza y seguridad alimentaria',
                fecha_inicio__year__gte=this_year - 2, fecha_fin__year__lte=this_year - 1).count()
            combate_pobreza = ProyectoInvestigacion.objects.filter(
                problema_nacional_conacyt__nombre='Combate a la pobreza y seguridad alimentaria',
                fecha_inicio__year__gte=this_year - 1).count()

            p_migracion_humana = ProyectoInvestigacion.objects.filter(
                problema_nacional_conacyt__nombre='Migraciones y asentamientos humanos',
                fecha_inicio__year__gte=this_year - 2, fecha_fin__year__lte=this_year - 1).count()
            migracion_humana = ProyectoInvestigacion.objects.filter(
                problema_nacional_conacyt__nombre='Migraciones y asentamientos humanos',
                fecha_inicio__year__gte=this_year - 1).count()

            p_seguridad_ciudadana = ProyectoInvestigacion.objects.filter(
                problema_nacional_conacyt__nombre='Seguridad ciudadana',
                fecha_inicio__year__gte=this_year - 2, fecha_fin__year__lte=this_year - 1).count()
            seguridad_ciudadana = ProyectoInvestigacion.objects.filter(
                problema_nacional_conacyt__nombre='Seguridad ciudadana',
                fecha_inicio__year__gte=this_year - 1).count()

            p_gestion_conocimiento = ProyectoInvestigacion.objects.filter(
                problema_nacional_conacyt__nombre='Economía y gestión del conocimiento',
                fecha_inicio__year__gte=this_year - 2, fecha_fin__year__lte=this_year - 1).count()
            gestion_conocimiento = ProyectoInvestigacion.objects.filter(
                problema_nacional_conacyt__nombre='Economía y gestión del conocimiento',
                fecha_inicio__year__gte=this_year - 1).count()

            p_prevencion_riesgos_naturales = ProyectoInvestigacion.objects.filter(
                problema_nacional_conacyt__nombre='Prevención de riesgos naturales',
                fecha_inicio__year__gte=this_year - 2, fecha_fin__year__lte=this_year - 1).count()
            prevencion_riesgos_naturales = ProyectoInvestigacion.objects.filter(
                problema_nacional_conacyt__nombre='Prevención de riesgos naturales',
                fecha_inicio__year__gte=this_year - 1).count()

            p_proyectos_problemas_conacyt_count = ProyectoInvestigacion.objects.filter(
                problema_nacional_conacyt__isnull=False,
                fecha_inicio__year__gte=this_year - 2, fecha_fin__year__lte=this_year - 1).count()
            proyectos_problemas_conacyt_count = ProyectoInvestigacion.objects.filter(
                problema_nacional_conacyt__isnull=False,
                fecha_inicio__year__gte=this_year - 1).count()

            if p_proyectos_problemas_conacyt_count == 0:
                p_proyectos_problemas_conacyt_count = 0.001
            if proyectos_problemas_conacyt_count == 0:
                proyectos_problemas_conacyt_count = 0.001

            p_gestion_aguap = round(p_gestion_agua / p_proyectos_problemas_conacyt_count * 100, 2)
            p_mitigacion_cambio_climaticop = round(
                p_mitigacion_cambio_climatico / p_proyectos_problemas_conacyt_count * 100, 2)
            p_resiliencia_desastres_ntp = round(p_resiliencia_desastres_nt / p_proyectos_problemas_conacyt_count * 100,
                                                2)
            p_aprovechamiento_ecosistemasp = round(
                p_aprovechamiento_ecosistemas / p_proyectos_problemas_conacyt_count * 100, 2)
            p_oceanos_aprovechamientop = round(p_oceanos_aprovechamiento / p_proyectos_problemas_conacyt_count * 100, 2)
            p_alimentos_produccionp = round(p_alimentos_produccion / p_proyectos_problemas_conacyt_count * 100, 2)
            p_ciudades_desarrollo_urbanop = round(
                p_ciudades_desarrollo_urbano / p_proyectos_problemas_conacyt_count * 100, 2)
            p_conectividad_informaticap = round(p_conectividad_informatica / p_proyectos_problemas_conacyt_count * 100,
                                                2)
            p_manufactura_alta_tecnologiap = round(
                p_manufactura_alta_tecnologia / p_proyectos_problemas_conacyt_count * 100, 2)
            p_consumo_sustentable_energiap = round(
                p_consumo_sustentable_energia / p_proyectos_problemas_conacyt_count * 100, 2)
            p_aprovechamiento_energias_renovablesp = round(
                p_aprovechamiento_energias_renovables / p_proyectos_problemas_conacyt_count * 100, 2)
            p_enfermedades_emergentesp = round(p_enfermedades_emergentes / p_proyectos_problemas_conacyt_count * 100, 2)
            p_combate_pobrezap = round(p_combate_pobreza / p_proyectos_problemas_conacyt_count * 100, 2)
            p_migracion_humanap = round(p_migracion_humana / p_proyectos_problemas_conacyt_count * 100, 2)
            p_seguridad_ciudadanap = round(p_seguridad_ciudadana / p_proyectos_problemas_conacyt_count * 100, 2)
            p_gestion_conocimientop = round(p_gestion_conocimiento / p_proyectos_problemas_conacyt_count * 100, 2)
            p_prevencion_riesgos_naturalesp = round(
                p_prevencion_riesgos_naturales / p_proyectos_problemas_conacyt_count * 100, 2)

            gestion_aguap = round(gestion_agua / proyectos_problemas_conacyt_count * 100, 2)
            mitigacion_cambio_climaticop = round(mitigacion_cambio_climatico / proyectos_problemas_conacyt_count * 100,
                                                 2)
            resiliencia_desastres_ntp = round(resiliencia_desastres_nt / proyectos_problemas_conacyt_count * 100, 2)
            aprovechamiento_ecosistemasp = round(aprovechamiento_ecosistemas / proyectos_problemas_conacyt_count * 100,
                                                 2)
            oceanos_aprovechamientop = round(oceanos_aprovechamiento / proyectos_problemas_conacyt_count * 100, 2)
            alimentos_produccionp = round(alimentos_produccion / proyectos_problemas_conacyt_count * 100, 2)
            ciudades_desarrollo_urbanop = round(ciudades_desarrollo_urbano / proyectos_problemas_conacyt_count * 100, 2)
            conectividad_informaticap = round(conectividad_informatica / proyectos_problemas_conacyt_count * 100, 2)
            manufactura_alta_tecnologiap = round(manufactura_alta_tecnologia / proyectos_problemas_conacyt_count * 100,
                                                 2)
            consumo_sustentable_energiap = round(consumo_sustentable_energia / proyectos_problemas_conacyt_count * 100,
                                                 2)
            aprovechamiento_energias_renovablesp = round(
                aprovechamiento_energias_renovables / proyectos_problemas_conacyt_count * 100, 2)
            enfermedades_emergentesp = round(enfermedades_emergentes / proyectos_problemas_conacyt_count * 100, 2)
            combate_pobrezap = round(combate_pobreza / proyectos_problemas_conacyt_count * 100, 2)
            migracion_humanap = round(migracion_humana / proyectos_problemas_conacyt_count * 100, 2)
            seguridad_ciudadanap = round(seguridad_ciudadana / proyectos_problemas_conacyt_count * 100, 2)
            gestion_conocimientop = round(gestion_conocimiento / proyectos_problemas_conacyt_count * 100, 2)
            prevencion_riesgos_naturalesp = round(
                prevencion_riesgos_naturales / proyectos_problemas_conacyt_count * 100, 2)

            p_proyectos_problemas_conacyt_data = [['Problema nacional CONACYT', 'Porcentaje'],
                                                  ['Gestión integral del agua, seguridad hídrica y derecho del agua',
                                                   p_gestion_agua],
                                                  ['Mitigación y adaptación al cambio climático',
                                                   p_mitigacion_cambio_climatico],
                                                  ['Resiliencia frente a desastres naturales y tecnológicos',
                                                   p_resiliencia_desastres_nt],
                                                  ['Aprovechamiento y protección de ecosistemas y de la biodiversidad',
                                                   p_aprovechamiento_ecosistemas],
                                                  ['Los océanos y su aprovechamiento', p_oceanos_aprovechamiento],
                                                  ['Alimentos y su producción', p_alimentos_produccion],
                                                  ['Ciudades y desarrollo urbano', p_ciudades_desarrollo_urbano],
                                                  [
                                                      'Conectividad informática y desarrollo de las tecnologías de la información, la comunicación y las telecomunicaciones',
                                                      p_conectividad_informatica],
                                                  ['Manufactura de alta tecnología', p_manufactura_alta_tecnologia],
                                                  ['Consumo sustentable de energía', p_consumo_sustentable_energia],
                                                  [
                                                      'Desarrollo y aprovechamiento de energías renovables limpias, conducta humana y prevención de adicciones',
                                                      p_aprovechamiento_energias_renovables],
                                                  ['Enfermedades emergentes y de importancia nacional',
                                                   p_enfermedades_emergentes],
                                                  ['Combate a la pobreza y seguridad alimentaria', p_combate_pobreza],
                                                  ['Migraciones y asentamientos humanos', p_migracion_humana],
                                                  ['Seguridad ciudadana', p_seguridad_ciudadana],
                                                  ['Economía y gestión del conocimiento', p_gestion_conocimiento],
                                                  ['Prevención de riesgos naturales', p_prevencion_riesgos_naturales]
                                                  ]

            data_source = SimpleDataSource(data=p_proyectos_problemas_conacyt_data)
            p_chart_proyectos_problemas_conacyt = PieChart(data_source)
            context['p_chart_proyectos_problemas_conacyt'] = p_chart_proyectos_problemas_conacyt

            proyectos_problemas_conacyt_data = [['Problema nacional CONACYT', 'Porcentaje'],
                                                ['Gestión integral del agua, seguridad hídrica y derecho del agua',
                                                 gestion_agua],
                                                ['Mitigación y adaptación al cambio climático',
                                                 mitigacion_cambio_climatico],
                                                ['Resiliencia frente a desastres naturales y tecnológicos',
                                                 resiliencia_desastres_nt],
                                                ['Aprovechamiento y protección de ecosistemas y de la biodiversidad',
                                                 aprovechamiento_ecosistemas],
                                                ['Los océanos y su aprovechamiento', oceanos_aprovechamiento],
                                                ['Alimentos y su producción', alimentos_produccion],
                                                ['Ciudades y desarrollo urbano', ciudades_desarrollo_urbano],
                                                [
                                                    'Conectividad informática y desarrollo de las tecnologías de la información, la comunicación y las telecomunicaciones',
                                                    conectividad_informatica],
                                                ['Manufactura de alta tecnología', manufactura_alta_tecnologia],
                                                ['Consumo sustentable de energía', consumo_sustentable_energia],
                                                [
                                                    'Desarrollo y aprovechamiento de energías renovables limpias, conducta humana y prevención de adicciones',
                                                    aprovechamiento_energias_renovables],
                                                ['Enfermedades emergentes y de importancia nacional',
                                                 enfermedades_emergentes],
                                                ['Combate a la pobreza y seguridad alimentaria', combate_pobreza],
                                                ['Migraciones y asentamientos humanos', migracion_humana],
                                                ['Seguridad ciudadana', seguridad_ciudadana],
                                                ['Economía y gestión del conocimiento', gestion_conocimiento],
                                                ['Prevención de riesgos naturales', prevencion_riesgos_naturales]
                                                ]

            data_source = SimpleDataSource(data=proyectos_problemas_conacyt_data)
            chart_proyectos_problemas_conacyt = PieChart(data_source)
            context['chart_proyectos_problemas_conacyt'] = chart_proyectos_problemas_conacyt

            context['table_proyectos_problemas_conacyt'] = {
                'p_proyectos_problemas_conacyt_count': p_proyectos_problemas_conacyt_count,
                'proyectos_problemas_conacyt_count': proyectos_problemas_conacyt_count,
                'p_gestion_agua': p_gestion_agua,
                'p_mitigacion_cambio_climatico': p_mitigacion_cambio_climatico,
                'p_resiliencia_desastres_nt': p_resiliencia_desastres_nt,
                'p_aprovechamiento_ecosistemas': p_aprovechamiento_ecosistemas,
                'p_oceanos_aprovechamiento': p_oceanos_aprovechamiento,
                'p_alimentos_produccion': p_alimentos_produccion,
                'p_ciudades_desarrollo_urbano': p_ciudades_desarrollo_urbano,
                'p_conectividad_informatica': p_conectividad_informatica,
                'p_manufactura_alta_tecnologia': p_manufactura_alta_tecnologia,
                'p_consumo_sustentable_energia': p_consumo_sustentable_energia,
                'p_aprovechamiento_energias_renovables': p_aprovechamiento_energias_renovables,
                'p_enfermedades_emergentes': p_enfermedades_emergentes,
                'p_combate_pobreza': p_combate_pobreza,
                'p_migracion_humana': p_migracion_humana,
                'p_seguridad_ciudadana': p_seguridad_ciudadana,
                'p_gestion_conocimiento': p_gestion_conocimiento,
                'p_prevencion_riesgos_naturales': p_prevencion_riesgos_naturales,
                'gestion_agua': gestion_agua,
                'mitigacion_cambio_climatico': mitigacion_cambio_climatico,
                'resiliencia_desastres_nt': resiliencia_desastres_nt,
                'aprovechamiento_ecosistemas': aprovechamiento_ecosistemas,
                'oceanos_aprovechamiento': oceanos_aprovechamiento,
                'alimentos_produccion': alimentos_produccion,
                'ciudades_desarrollo_urbano': ciudades_desarrollo_urbano,
                'conectividad_informatica': conectividad_informatica,
                'manufactura_alta_tecnologia': manufactura_alta_tecnologia,
                'consumo_sustentable_energia': consumo_sustentable_energia,
                'aprovechamiento_energias_renovables': aprovechamiento_energias_renovables,
                'enfermedades_emergentes': enfermedades_emergentes,
                'combate_pobreza': combate_pobreza,
                'migracion_humana': migracion_humana,
                'seguridad_ciudadana': seguridad_ciudadana,
                'gestion_conocimiento': gestion_conocimiento,
                'prevencion_riesgos_naturales': prevencion_riesgos_naturales,
                'p_gestion_aguap': p_gestion_aguap,
                'p_mitigacion_cambio_climaticop': p_mitigacion_cambio_climaticop,
                'p_resiliencia_desastres_ntp': p_resiliencia_desastres_ntp,
                'p_aprovechamiento_ecosistemasp': p_aprovechamiento_ecosistemasp,
                'p_oceanos_aprovechamientop': p_oceanos_aprovechamientop,
                'p_alimentos_produccionp': p_alimentos_produccionp,
                'p_ciudades_desarrollo_urbanop': p_ciudades_desarrollo_urbanop,
                'p_conectividad_informaticap': p_conectividad_informaticap,
                'p_manufactura_alta_tecnologiap': p_manufactura_alta_tecnologiap,
                'p_consumo_sustentable_energiap': p_consumo_sustentable_energiap,
                'p_aprovechamiento_energias_renovablesp': p_aprovechamiento_energias_renovablesp,
                'p_enfermedades_emergentesp': p_enfermedades_emergentesp,
                'p_combate_pobrezap': p_combate_pobrezap,
                'p_migracion_humanap': p_migracion_humanap,
                'p_seguridad_ciudadanap': p_seguridad_ciudadanap,
                'p_gestion_conocimientop': p_gestion_conocimientop,
                'p_prevencion_riesgos_naturalesp': p_prevencion_riesgos_naturalesp,
                'gestion_aguap': gestion_aguap,
                'mitigacion_cambio_climaticop': mitigacion_cambio_climaticop,
                'resiliencia_desastres_ntp': resiliencia_desastres_ntp,
                'aprovechamiento_ecosistemasp': aprovechamiento_ecosistemasp,
                'oceanos_aprovechamientop': oceanos_aprovechamientop,
                'alimentos_produccionp': alimentos_produccionp,
                'ciudades_desarrollo_urbanop': ciudades_desarrollo_urbanop,
                'conectividad_informaticap': conectividad_informaticap,
                'manufactura_alta_tecnologiap': manufactura_alta_tecnologiap,
                'consumo_sustentable_energiap': consumo_sustentable_energiap,
                'aprovechamiento_energias_renovablesp': aprovechamiento_energias_renovablesp,
                'enfermedades_emergentesp': enfermedades_emergentesp,
                'combate_pobrezap': combate_pobrezap,
                'migracion_humanap': migracion_humanap,
                'seguridad_ciudadanap': seguridad_ciudadanap,
                'gestion_conocimientop': gestion_conocimientop,
                'prevencion_riesgos_naturalesp': prevencion_riesgos_naturalesp,
            }

            p_convenios_federales = ConvenioEntidadExterna.objects.filter(entidades__clasificacion='FEDERAL',
                                                                          fecha_inicio__year__gte=this_year - 2,
                                                                          fecha_fin__year__lte=this_year - 1).count()
            convenios_federales = ConvenioEntidadExterna.objects.filter(entidades__clasificacion='FEDERAL',
                                                                        fecha_inicio__year__gte=this_year - 1).count()

            p_convenios_estatales = ConvenioEntidadExterna.objects.filter(entidades__clasificacion='ESTATAL',
                                                                          fecha_inicio__year__gte=this_year - 2,
                                                                          fecha_fin__year__lte=this_year - 1).count()
            convenios_estatales = ConvenioEntidadExterna.objects.filter(entidades__clasificacion='ESTATAL',
                                                                        fecha_inicio__year__gte=this_year - 1).count()

            p_convenios_municipales = ConvenioEntidadExterna.objects.filter(entidades__clasificacion='MUNICIPAL',
                                                                            fecha_inicio__year__gte=this_year - 2,
                                                                            fecha_fin__year__lte=this_year - 1).count()
            convenios_municipales = ConvenioEntidadExterna.objects.filter(entidades__clasificacion='MUNICIPAL',
                                                                          fecha_inicio__year__gte=this_year - 1).count()

            p_convenios_privadas = ConvenioEntidadExterna.objects.filter(entidades__clasificacion='PRIVADA',
                                                                         fecha_inicio__year__gte=this_year - 2,
                                                                         fecha_fin__year__lte=this_year - 1).count()
            convenios_privadas = ConvenioEntidadExterna.objects.filter(entidades__clasificacion='PRIVADA',
                                                                       fecha_inicio__year__gte=this_year - 1).count()

            p_convenios_nolucrativas = ConvenioEntidadExterna.objects.filter(entidades__clasificacion='NO_LUCRATIVA',
                                                                             fecha_inicio__year__gte=this_year - 2,
                                                                             fecha_fin__year__lte=this_year - 1).count()
            convenios_nolucrativas = ConvenioEntidadExterna.objects.filter(entidades__clasificacion='NO_LUCRATIVA',
                                                                           fecha_inicio__year__gte=this_year - 1).count()

            p_convenios_extranjeras = ConvenioEntidadExterna.objects.filter(entidades__clasificacion='EXTRANJERA',
                                                                            fecha_inicio__year__gte=this_year - 2,
                                                                            fecha_fin__year__lte=this_year - 1).count()
            convenios_extranjeras = ConvenioEntidadExterna.objects.filter(entidades__clasificacion='EXTRANJERA',
                                                                          fecha_inicio__year__gte=this_year - 1).count()

            p_convenios_academicas = ConvenioEntidadExterna.objects.filter(entidades__clasificacion='ACADEMICA',
                                                                           fecha_inicio__year__gte=this_year - 2,
                                                                           fecha_fin__year__lte=this_year - 1).count()
            convenios_academicas = ConvenioEntidadExterna.objects.filter(entidades__clasificacion='ACADEMICA',
                                                                         fecha_inicio__year__gte=this_year - 1).count()

            p_convenios_externos_count = ConvenioEntidadExterna.objects.filter(fecha_inicio__year__gte=this_year - 2,
                                                                               fecha_fin__year__lte=this_year - 1).count()
            convenios_externos_count = ConvenioEntidadExterna.objects.filter(
                fecha_inicio__year__gte=this_year - 1).count()

            if p_convenios_externos_count == 0:
                p_convenios_externos_count = 0.001
            if convenios_externos_count == 0:
                convenios_externos_count = 0.001

            p_convenios_federalesp = round(p_convenios_federales / p_convenios_externos_count * 100, 2)
            convenios_federalesp = round(convenios_federales / convenios_externos_count * 100, 2)
            p_convenios_estatalesp = round(p_convenios_estatales / p_convenios_externos_count * 100, 2)
            convenios_estatalesp = round(convenios_estatales / convenios_externos_count * 100, 2)
            p_convenios_municipalesp = round(p_convenios_municipales / p_convenios_externos_count * 100, 2)
            convenios_municipalesp = round(convenios_municipales / convenios_externos_count * 100, 2)
            p_convenios_privadasp = round(p_convenios_privadas / p_convenios_externos_count * 100, 2)
            convenios_privadasp = round(convenios_privadas / convenios_externos_count * 100, 2)
            p_convenios_nolucrativasp = round(p_convenios_nolucrativas / p_convenios_externos_count * 100, 2)
            convenios_nolucrativasp = round(convenios_nolucrativas / convenios_externos_count * 100, 2)
            p_convenios_extranjerasp = round(p_convenios_extranjeras / p_convenios_externos_count * 100, 2)
            convenios_extranjerasp = round(convenios_extranjeras / convenios_externos_count * 100, 2)
            p_convenios_academicasp = round(p_convenios_academicas / p_convenios_externos_count * 100, 2)
            convenios_academicasp = round(convenios_academicas / convenios_externos_count * 100, 2)

            p_convenios_externos_data = [['Convenios con entidades externas', 'Porcentaje'],
                                         ['Gubernamental federal', p_convenios_federales],
                                         ['Gubernamental estatal', p_convenios_estatales],
                                         ['Gubernamental municipal', p_convenios_municipales],
                                         ['Sector privado', p_convenios_privadas],
                                         ['Sector privado no lucrativo', p_convenios_nolucrativas],
                                         ['Extranjero', p_convenios_extranjeras],
                                         ['Académica', p_convenios_academicas],
                                         ]

            convenios_externos_data = [['Convenios con entidades externas', 'Porcentaje'],
                                       ['Gubernamental federal', convenios_federales],
                                       ['Gubernamental estatal', convenios_estatales],
                                       ['Gubernamental municipal', convenios_municipales],
                                       ['Sector privado', convenios_privadas],
                                       ['Sector privado no lucrativo', convenios_nolucrativas],
                                       ['Extranjero', convenios_extranjeras],
                                       ['Académica', convenios_academicas],
                                       ]

            p_data_source = SimpleDataSource(data=p_convenios_externos_data)
            p_chart_convenios_externos = PieChart(p_data_source)
            context['p_chart_convenios_externos'] = p_chart_convenios_externos

            data_source = SimpleDataSource(data=convenios_externos_data)
            chart_convenios_externos = PieChart(data_source)
            context['chart_convenios_externos'] = chart_convenios_externos

            context['table_convenios_externos'] = {'p_convenios_externos_count': p_convenios_externos_count,
                                                   'convenios_externos_count': convenios_externos_count,

                                                   'p_convenios_federales': p_convenios_federales,
                                                   'p_convenios_estatales': p_convenios_estatales,
                                                   'p_convenios_municipales': p_convenios_municipales,
                                                   'p_convenios_privadas': p_convenios_privadas,
                                                   'p_convenios_nolucrativas': p_convenios_nolucrativas,
                                                   'p_convenios_extranjeras': p_convenios_extranjeras,
                                                   'p_convenios_academicas': p_convenios_academicas,
                                                   'convenios_federales': convenios_federales,
                                                   'convenios_estatales': convenios_estatales,
                                                   'convenios_municipales': convenios_municipales,
                                                   'convenios_privadas': convenios_privadas,
                                                   'convenios_nolucrativas': convenios_nolucrativas,
                                                   'convenios_extranjeras': convenios_extranjeras,
                                                   'convenios_academicas': convenios_academicas,

                                                   'p_convenios_federalesp': p_convenios_federalesp,
                                                   'p_convenios_estatalesp': p_convenios_estatalesp,
                                                   'p_convenios_municipalesp': p_convenios_municipalesp,
                                                   'p_convenios_privadasp': p_convenios_privadasp,
                                                   'p_convenios_nolucrativasp': p_convenios_nolucrativasp,
                                                   'p_convenios_extranjerasp': p_convenios_extranjerasp,
                                                   'p_convenios_academicasp': p_convenios_academicasp,
                                                   'convenios_federalesp': convenios_federalesp,
                                                   'convenios_estatalesp': convenios_estatalesp,
                                                   'convenios_municipalesp': convenios_municipalesp,
                                                   'convenios_privadasp': convenios_privadasp,
                                                   'convenios_nolucrativasp': convenios_nolucrativasp,
                                                   'convenios_extranjerasp': convenios_extranjerasp,
                                                   'convenios_academicasp': convenios_academicasp,
                                                   }

            p_investigadores_unam = ExperienciaProfesional.objects.filter(
                dependencia__nombre='Centro de Investigaciones en Geografía Ambiental (CIGA)',
                cargo__nombre='Investigador UNAM', fecha_inicio__year__gte=this_year - 2,
                fecha_inicio__year__lte=this_year - 1).count()

            p_investigadores_catedra = ExperienciaProfesional.objects.filter(
                dependencia__nombre='Centro de Investigaciones en Geografía Ambiental (CIGA)',
                cargo__nombre='Cátedras CONACYT', fecha_inicio__year__gte=this_year - 2,
                fecha_inicio__year__lte=this_year - 1).count()

            p_investigadores_postdoctoral = ExperienciaProfesional.objects.filter(
                dependencia__nombre='Centro de Investigaciones en Geografía Ambiental (CIGA)',
                cargo__nombre='Investigador Postdoctoral', fecha_inicio__year__gte=this_year - 2,
                fecha_inicio__year__lte=this_year - 1).count()

            p_investigadores_convenio = ExperienciaProfesional.objects.filter(
                dependencia__nombre='Centro de Investigaciones en Geografía Ambiental (CIGA)',
                cargo__nombre='Investigador por convenio', fecha_inicio__year__gte=this_year - 2,
                fecha_inicio__year__lte=this_year - 1).count()

            investigadores_unam = ExperienciaProfesional.objects.filter(
                dependencia__nombre='Centro de Investigaciones en Geografía Ambiental (CIGA)',
                cargo__nombre='Investigador UNAM', fecha_inicio__year__gte=this_year - 1).count()

            investigadores_catedra = ExperienciaProfesional.objects.filter(
                dependencia__nombre='Centro de Investigaciones en Geografía Ambiental (CIGA)',
                cargo__nombre='Cátedras CONACYT', fecha_inicio__year__gte=this_year - 1).count()

            investigadores_postdoctoral = ExperienciaProfesional.objects.filter(
                dependencia__nombre='Centro de Investigaciones en Geografía Ambiental (CIGA)',
                cargo__nombre='Investigador Postdoctoral', fecha_inicio__year__gte=this_year - 1).count()

            investigadores_convenio = ExperienciaProfesional.objects.filter(
                dependencia__nombre='Centro de Investigaciones en Geografía Ambiental (CIGA)',
                cargo__nombre='Investigador por convenio', fecha_inicio__year__gte=this_year - 1).count()

            p_investigadores_count = ExperienciaProfesional.objects.filter(
                dependencia__nombre='Centro de Investigaciones en Geografía Ambiental (CIGA)',
                fecha_inicio__year__gte=this_year - 2, fecha_inicio__year__lte=this_year - 1).count()
            investigadores_count = ExperienciaProfesional.objects.filter(
                dependencia__nombre='Centro de Investigaciones en Geografía Ambiental (CIGA)',
                fecha_inicio__year__gte=this_year - 1).count()

            if p_investigadores_count == 0:
                p_investigadores_count = 0.001

            if investigadores_count == 0:
                investigadores_count = 0.001

            p_investigadores_unamp = round(p_investigadores_unam / p_investigadores_count * 100, 2)
            investigadores_unamp = round(investigadores_unam / investigadores_count * 100, 2)
            p_investigadores_catedrap = round(p_investigadores_catedra / p_investigadores_count * 100, 2)
            investigadores_catedrap = round(investigadores_catedra / investigadores_count * 100, 2)
            p_investigadores_postdoctoralp = round(p_investigadores_postdoctoral / p_investigadores_count * 100, 2)
            investigadores_postdoctoralp = round(investigadores_postdoctoral / investigadores_count * 100, 2)
            p_investigadores_conveniop = round(p_investigadores_convenio / p_investigadores_count * 100, 2)
            investigadores_conveniop = round(investigadores_convenio / investigadores_count * 100, 2)

            p_investigadores_data = [['Investigadores', 'Porcentaje'],
                                     ['Investigadores UNAM', p_investigadores_unam],
                                     ['Cátedras CONACYT', p_investigadores_catedra],
                                     ['Investigador Postdoctoral', p_investigadores_postdoctoral],
                                     ['Investigador por convenio', p_investigadores_convenio],
                                     ]

            investigadores_data = [['Investigadores', 'Porcentaje'],
                                   ['Investigadores UNAM', investigadores_unam],
                                   ['Cátedras CONACYT', investigadores_catedra],
                                   ['Investigador Postdoctoral', investigadores_postdoctoral],
                                   ['Investigador por convenio', investigadores_convenio],
                                   ]

            p_data_source = SimpleDataSource(data=p_convenios_externos_data)
            p_chart_investigadores = PieChart(p_data_source)
            context['p_chart_investigadores'] = p_chart_investigadores

            data_source = SimpleDataSource(data=convenios_externos_data)
            chart_investigadores = PieChart(data_source)
            context['chart_investigadores'] = chart_investigadores

            context['table_investigadores'] = {'p_investigadores_count': p_investigadores_count,
                                               'investigadores_count': investigadores_count,
                                               'p_investigadores_unam': p_investigadores_unam,
                                               'p_investigadores_catedra': p_investigadores_catedra,
                                               'p_investigadores_postdoctoral': p_investigadores_postdoctoral,
                                               'p_investigadores_convenio': p_investigadores_convenio,
                                               'investigadores_unam': investigadores_unam,
                                               'investigadores_catedra': investigadores_catedra,
                                               'investigadores_postdoctoral': investigadores_postdoctoral,
                                               'investigadores_convenio': investigadores_convenio,

                                               'p_investigadores_unamp': p_investigadores_unamp,
                                               'p_investigadores_catedrap': p_investigadores_catedrap,
                                               'p_investigadores_postdoctoralp': p_investigadores_postdoctoralp,
                                               'p_investigadores_conveniop': p_investigadores_conveniop,
                                               'investigadores_unamp': investigadores_unamp,
                                               'investigadores_catedrap': investigadores_catedrap,
                                               'investigadores_postdoctoralp': investigadores_postdoctoralp,
                                               'investigadores_conveniop': investigadores_conveniop,
                                               }

            p_investigadores_asocA_tm = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Investigador Asociado A, Medio tiempo', ).filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year - 1)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            p_investigadores_asocB_tm = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Investigador Asociado B, Medio tiempo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year - 1)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            p_investigadores_asocC_tm = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Investigador Asociado C, Medio tiempo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year - 1)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            p_investigadores_asocA_tc = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Investigador Asociado A, Tiempo Completo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year - 1)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            p_investigadores_asocB_tc = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Investigador Asociado B, Tiempo Completo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year - 1)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            p_investigadores_asocC_tc = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Investigador Asociado C, Tiempo Completo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year - 1)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()

            p_investigadores_titA_tm = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Investigador Titular A, Medio tiempo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year - 1)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            p_investigadores_titB_tm = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Investigador Titular B, Medio tiempo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year - 1)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            p_investigadores_titC_tm = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Investigador Titular C, Medio tiempo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year - 1)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            p_investigadores_titA_tc = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Investigador Titular A, Tiempo Completo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year - 1)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            p_investigadores_titB_tc = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Investigador Titular B, Tiempo Completo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year - 1)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            p_investigadores_titC_tc = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Investigador Titular C, Tiempo Completo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year - 1)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()

            p_tecnicos_auxA_tm = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Técnico Académico Auxiliar A, Medio tiempo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year - 1)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            p_tecnicos_auxB_tm = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Técnico Académico Auxiliar B, Medio tiempo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year - 1)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            p_tecnicos_auxC_tm = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Técnico Académico Auxiliar C, Medio tiempo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year - 1)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            p_tecnicos_auxA_tc = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Técnico Académico Auxiliar A, Tiempo Completo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year - 1)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            p_tecnicos_auxB_tc = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Técnico Académico Auxiliar B, Tiempo Completo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year - 1)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            p_tecnicos_auxC_tc = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Técnico Académico Auxiliar C, Tiempo Completo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year - 1)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()

            p_tecnicos_asocA_tm = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Técnico Académico Asociado A, Medio tiempo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year - 1)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            p_tecnicos_asocB_tm = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Técnico Académico Asociado B, Medio tiempo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year - 1)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            p_tecnicos_asocC_tm = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Técnico Académico Asociado C, Medio tiempo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year - 1)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            p_tecnicos_asocA_tc = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Técnico Académico Asociado A, Tiempo Completo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year - 1)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            p_tecnicos_asocB_tc = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Técnico Académico Asociado B, Tiempo Completo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year - 1)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            p_tecnicos_asocC_tc = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Técnico Académico Asociado C, Tiempo Completo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year - 1)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()

            p_tecnicos_titA_tm = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Técnico Académico Titular A, Medio tiempo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year - 1)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            p_tecnicos_titB_tm = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Técnico Académico Titular B, Medio tiempo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year - 1)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            p_tecnicos_titC_tm = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Técnico Académico Titular C, Medio tiempo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year - 1)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            p_tecnicos_titA_tc = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Técnico Académico Titular A, Tiempo Completo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year - 1)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            p_tecnicos_titB_tc = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Técnico Académico Titular B, Tiempo Completo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year - 1)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            p_tecnicos_titC_tc = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Técnico Académico Titular C, Tiempo Completo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year - 1)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()

            #

            investigadores_asocA_tm = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Investigador Asociado A, Medio tiempo', ).filter(
                (Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad__year__gte=this_year)) | (
                    Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            investigadores_asocB_tm = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Investigador Asociado B, Medio tiempo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad__year__gte=this_year)) | (
                    Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            investigadores_asocC_tm = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Investigador Asociado C, Medio tiempo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad__year__gte=this_year)) | (
                    Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            investigadores_asocA_tc = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Investigador Asociado A, Tiempo Completo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad__year__gte=this_year)) | (
                    Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            investigadores_asocB_tc = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Investigador Asociado B, Tiempo Completo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad__year__gte=this_year)) | (
                    Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            investigadores_asocC_tc = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Investigador Asociado C, Tiempo Completo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad__year__gte=this_year)) | (
                    Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()

            investigadores_titA_tm = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Investigador Titular A, Medio tiempo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad__year__gte=this_year)) | (
                    Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            investigadores_titB_tm = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Investigador Titular B, Medio tiempo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad__year__gte=this_year)) | (
                    Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            investigadores_titC_tm = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Investigador Titular C, Medio tiempo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad__year__gte=this_year)) | (
                    Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            investigadores_titA_tc = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Investigador Titular A, Tiempo Completo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad__year__gte=this_year)) | (
                    Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            investigadores_titB_tc = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Investigador Titular B, Tiempo Completo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad__year__gte=this_year)) | (
                    Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            investigadores_titC_tc = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Investigador Titular C, Tiempo Completo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad__year__gte=this_year)) | (
                    Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()

            tecnicos_auxA_tm = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Técnico Académico Auxiliar A, Medio tiempo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad__year__gte=this_year)) | (
                    Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            tecnicos_auxB_tm = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Técnico Académico Auxiliar B, Medio tiempo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad__year__gte=this_year)) | (
                    Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            tecnicos_auxC_tm = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Técnico Académico Auxiliar C, Medio tiempo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad__year__gte=this_year)) | (
                    Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            tecnicos_auxA_tc = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Técnico Académico Auxiliar A, Tiempo Completo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad__year__gte=this_year)) | (
                    Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            tecnicos_auxB_tc = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Técnico Académico Auxiliar B, Tiempo Completo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad__year__gte=this_year)) | (
                    Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            tecnicos_auxC_tc = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Técnico Académico Auxiliar C, Tiempo Completo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad__year__gte=this_year)) | (
                    Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()

            tecnicos_asocA_tm = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Técnico Académico Asociado A, Medio tiempo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad__year__gte=this_year)) | (
                    Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            tecnicos_asocB_tm = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Técnico Académico Asociado B, Medio tiempo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad__year__gte=this_year)) | (
                    Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            tecnicos_asocC_tm = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Técnico Académico Asociado C, Medio tiempo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad__year__gte=this_year)) | (
                    Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            tecnicos_asocA_tc = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Técnico Académico Asociado A, Tiempo Completo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad__year__gte=this_year)) | (
                    Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            tecnicos_asocB_tc = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Técnico Académico Asociado B, Tiempo Completo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad__year__gte=this_year)) | (
                    Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            tecnicos_asocC_tc = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Técnico Académico Asociado C, Tiempo Completo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad__year__gte=this_year)) | (
                    Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()

            tecnicos_titA_tm = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Técnico Académico Titular A, Medio tiempo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad__year__gte=this_year)) | (
                    Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            tecnicos_titB_tm = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Técnico Académico Titular B, Medio tiempo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad__year__gte=this_year)) | (
                    Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            tecnicos_titC_tm = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Técnico Académico Titular C, Medio tiempo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad__year__gte=this_year)) | (
                    Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            tecnicos_titA_tc = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Técnico Académico Titular A, Tiempo Completo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad__year__gte=this_year)) | (
                    Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            tecnicos_titB_tc = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Técnico Académico Titular B, Tiempo Completo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad__year__gte=this_year)) | (
                    Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()
            tecnicos_titC_tc = User.objects.filter(
                experiencialaboral__nombramiento__nombre='Técnico Académico Titular C, Tiempo Completo').filter(
                (Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad__year__gte=this_year)) | (
                    Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()

            p_nom_investigadores_count = User.objects.filter(
                experiencialaboral__nombramiento__nombre__startswith='Investigador', ).filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year - 1)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()

            nom_investigadores_count = User.objects.filter(
                experiencialaboral__nombramiento__nombre__startswith='Investigador').filter(
                (Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad__year__gte=this_year)) | (
                    Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()

            p_nom_tecnicos_count = User.objects.filter(
                experiencialaboral__nombramiento__nombre__startswith='Técnico', ).filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year - 1)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()

            nom_tecnicos_count = User.objects.filter(
                experiencialaboral__nombramiento__nombre__startswith='Técnico').filter(
                (Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad__year__gte=this_year)) | (
                    Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True)).count()

            if p_nom_investigadores_count == 0:
                p_nom_investigadores_count = 0.001
            if nom_investigadores_count == 0:
                nom_investigadores_count = 0.001
            if p_nom_tecnicos_count == 0:
                p_nom_tecnicos_count = 0.001
            if nom_tecnicos_count == 0:
                nom_tecnicos_count = 0.001

            p_investigadores_asocA_tmp = round(p_investigadores_asocA_tm / p_nom_investigadores_count * 100, 2)
            p_investigadores_asocB_tmp = round(p_investigadores_asocB_tm / p_nom_investigadores_count * 100, 2)
            p_investigadores_asocC_tmp = round(p_investigadores_asocC_tm / p_nom_investigadores_count * 100, 2)
            p_investigadores_asocA_tcp = round(p_investigadores_asocA_tc / p_nom_investigadores_count * 100, 2)
            p_investigadores_asocB_tcp = round(p_investigadores_asocB_tc / p_nom_investigadores_count * 100, 2)
            p_investigadores_asocC_tcp = round(p_investigadores_asocC_tc / p_nom_investigadores_count * 100, 2)

            p_investigadores_titA_tmp = round(p_investigadores_titA_tm / p_nom_investigadores_count * 100, 2)
            p_investigadores_titB_tmp = round(p_investigadores_titB_tm / p_nom_investigadores_count * 100, 2)
            p_investigadores_titC_tmp = round(p_investigadores_titC_tm / p_nom_investigadores_count * 100, 2)
            p_investigadores_titA_tcp = round(p_investigadores_titA_tc / p_nom_investigadores_count * 100, 2)
            p_investigadores_titB_tcp = round(p_investigadores_titB_tc / p_nom_investigadores_count * 100, 2)
            p_investigadores_titC_tcp = round(p_investigadores_titC_tc / p_nom_investigadores_count * 100, 2)

            p_tecnicos_auxA_tmp = round(p_tecnicos_auxA_tm / p_nom_tecnicos_count * 100, 2)
            p_tecnicos_auxB_tmp = round(p_tecnicos_auxB_tm / p_nom_tecnicos_count * 100, 2)
            p_tecnicos_auxC_tmp = round(p_tecnicos_auxC_tm / p_nom_tecnicos_count * 100, 2)
            p_tecnicos_auxA_tcp = round(p_tecnicos_auxA_tc / p_nom_tecnicos_count * 100, 2)
            p_tecnicos_auxB_tcp = round(p_tecnicos_auxB_tc / p_nom_tecnicos_count * 100, 2)
            p_tecnicos_auxC_tcp = round(p_tecnicos_auxC_tc / p_nom_tecnicos_count * 100, 2)

            p_tecnicos_asocA_tmp = round(p_tecnicos_asocA_tm / p_nom_tecnicos_count * 100, 2)
            p_tecnicos_asocB_tmp = round(p_tecnicos_asocB_tm / p_nom_tecnicos_count * 100, 2)
            p_tecnicos_asocC_tmp = round(p_tecnicos_asocC_tm / p_nom_tecnicos_count * 100, 2)
            p_tecnicos_asocA_tcp = round(p_tecnicos_asocA_tc / p_nom_tecnicos_count * 100, 2)
            p_tecnicos_asocB_tcp = round(p_tecnicos_asocB_tc / p_nom_tecnicos_count * 100, 2)
            p_tecnicos_asocC_tcp = round(p_tecnicos_asocC_tc / p_nom_tecnicos_count * 100, 2)

            p_tecnicos_titA_tmp = round(p_tecnicos_titA_tm / p_nom_tecnicos_count * 100, 2)
            p_tecnicos_titB_tmp = round(p_tecnicos_titB_tm / p_nom_tecnicos_count * 100, 2)
            p_tecnicos_titC_tmp = round(p_tecnicos_titC_tm / p_nom_tecnicos_count * 100, 2)
            p_tecnicos_titA_tcp = round(p_tecnicos_titA_tc / p_nom_tecnicos_count * 100, 2)
            p_tecnicos_titB_tcp = round(p_tecnicos_titB_tc / p_nom_tecnicos_count * 100, 2)
            p_tecnicos_titC_tcp = round(p_tecnicos_titC_tc / p_nom_tecnicos_count * 100, 2)

            investigadores_asocA_tmp = round(investigadores_asocA_tm / nom_investigadores_count * 100, 2)
            investigadores_asocB_tmp = round(investigadores_asocB_tm / nom_investigadores_count * 100, 2)
            investigadores_asocC_tmp = round(investigadores_asocC_tm / nom_investigadores_count * 100, 2)
            investigadores_asocA_tcp = round(investigadores_asocA_tc / nom_investigadores_count * 100, 2)
            investigadores_asocB_tcp = round(investigadores_asocB_tc / nom_investigadores_count * 100, 2)
            investigadores_asocC_tcp = round(investigadores_asocC_tc / nom_investigadores_count * 100, 2)

            investigadores_titA_tmp = round(investigadores_titA_tm / nom_investigadores_count * 100, 2)
            investigadores_titB_tmp = round(investigadores_titB_tm / nom_investigadores_count * 100, 2)
            investigadores_titC_tmp = round(investigadores_titC_tm / nom_investigadores_count * 100, 2)
            investigadores_titA_tcp = round(investigadores_titA_tc / nom_investigadores_count * 100, 2)
            investigadores_titB_tcp = round(investigadores_titB_tc / nom_investigadores_count * 100, 2)
            investigadores_titC_tcp = round(investigadores_titC_tc / nom_investigadores_count * 100, 2)

            tecnicos_auxA_tmp = round(tecnicos_auxA_tm / nom_tecnicos_count * 100, 2)
            tecnicos_auxB_tmp = round(tecnicos_auxB_tm / nom_tecnicos_count * 100, 2)
            tecnicos_auxC_tmp = round(tecnicos_auxC_tm / nom_tecnicos_count * 100, 2)
            tecnicos_auxA_tcp = round(tecnicos_auxA_tc / nom_tecnicos_count * 100, 2)
            tecnicos_auxB_tcp = round(tecnicos_auxB_tc / nom_tecnicos_count * 100, 2)
            tecnicos_auxC_tcp = round(tecnicos_auxC_tc / nom_tecnicos_count * 100, 2)

            tecnicos_asocA_tmp = round(tecnicos_asocA_tm / nom_tecnicos_count * 100, 2)
            tecnicos_asocB_tmp = round(tecnicos_asocB_tm / nom_tecnicos_count * 100, 2)
            tecnicos_asocC_tmp = round(tecnicos_asocC_tm / nom_tecnicos_count * 100, 2)
            tecnicos_asocA_tcp = round(tecnicos_asocA_tc / nom_tecnicos_count * 100, 2)
            tecnicos_asocB_tcp = round(tecnicos_asocB_tc / nom_tecnicos_count * 100, 2)
            tecnicos_asocC_tcp = round(tecnicos_asocC_tc / nom_tecnicos_count * 100, 2)

            tecnicos_titA_tmp = round(tecnicos_titA_tm / nom_tecnicos_count * 100, 2)
            tecnicos_titB_tmp = round(tecnicos_titB_tm / nom_tecnicos_count * 100, 2)
            tecnicos_titC_tmp = round(tecnicos_titC_tm / nom_tecnicos_count * 100, 2)
            tecnicos_titA_tcp = round(tecnicos_titA_tc / nom_tecnicos_count * 100, 2)
            tecnicos_titB_tcp = round(tecnicos_titB_tc / nom_tecnicos_count * 100, 2)
            tecnicos_titC_tcp = round(tecnicos_titC_tc / nom_tecnicos_count * 100, 2)

            p_nom_investigadores_data = [['Investigadores', 'Porcentaje'],
                                         ['Investigadores asociados A, medio tiempo', p_investigadores_asocA_tm],
                                         ['Investigadores asociados B, medio tiempo', p_investigadores_asocB_tm],
                                         ['Investigadores asociados C, medio tiempo', p_investigadores_asocC_tm],
                                         ['Investigadores asociados A, tiempo completo', p_investigadores_asocA_tc],
                                         ['Investigadores asociados B, tiempo completo', p_investigadores_asocB_tc],
                                         ['Investigadores asociados C, tiempo completo', p_investigadores_asocC_tc],
                                         ['Investigadores titulares A, medio tiempo', p_investigadores_titA_tm],
                                         ['Investigadores titulares B, medio tiempo', p_investigadores_titB_tm],
                                         ['Investigadores titulares C, medio tiempo', p_investigadores_titC_tm],
                                         ['Investigadores titulares A, tiempo completo', p_investigadores_titA_tc],
                                         ['Investigadores titulares B, tiempo completo', p_investigadores_titB_tc],
                                         ['Investigadores titulares C, tiempo completo', p_investigadores_titC_tc],
                                         ]

            nom_investigadores_data = [['Investigadores', 'Porcentaje'],
                                       ['Investigadores asociados A, medio tiempo', investigadores_asocA_tm],
                                       ['Investigadores asociados B, medio tiempo', investigadores_asocB_tm],
                                       ['Investigadores asociados C, medio tiempo', investigadores_asocC_tm],
                                       ['Investigadores asociados A, tiempo completo', investigadores_asocA_tc],
                                       ['Investigadores asociados B, tiempo completo', investigadores_asocB_tc],
                                       ['Investigadores asociados C, tiempo completo', investigadores_asocC_tc],
                                       ['Investigadores titulares A, medio tiempo', investigadores_titA_tm],
                                       ['Investigadores titulares B, medio tiempo', investigadores_titB_tm],
                                       ['Investigadores titulares C, medio tiempo', investigadores_titC_tm],
                                       ['Investigadores titulares A, tiempo completo', investigadores_titA_tc],
                                       ['Investigadores titulares B, tiempo completo', investigadores_titB_tc],
                                       ['Investigadores titulares C, tiempo completo', investigadores_titC_tc],
                                       ]

            p_data_source = SimpleDataSource(data=p_nom_investigadores_data)
            p_chart_nom_investigadores = PieChart(p_data_source)
            context['p_chart_nom_investigadores'] = p_chart_nom_investigadores

            data_source = SimpleDataSource(data=nom_investigadores_data)
            chart_nom_investigadores = PieChart(data_source)
            context['chart_nom_investigadores'] = chart_nom_investigadores

            context['table_nom_investigadores'] = {'p_nom_investigadores_count': p_nom_investigadores_count,
                                                   'nom_investigadores_count': nom_investigadores_count,
                                                   'p_investigadores_asocA_tm': p_investigadores_asocA_tm,
                                                   'p_investigadores_asocB_tm': p_investigadores_asocB_tm,
                                                   'p_investigadores_asocC_tm': p_investigadores_asocC_tm,
                                                   'p_investigadores_asocA_tc': p_investigadores_asocA_tc,
                                                   'p_investigadores_asocB_tc': p_investigadores_asocB_tc,
                                                   'p_investigadores_asocC_tc': p_investigadores_asocC_tc,
                                                   'p_investigadores_titA_tm': p_investigadores_titA_tm,
                                                   'p_investigadores_titB_tm': p_investigadores_titB_tm,
                                                   'p_investigadores_titC_tm': p_investigadores_titC_tm,
                                                   'p_investigadores_titA_tc': p_investigadores_titA_tc,
                                                   'p_investigadores_titB_tc': p_investigadores_titB_tc,
                                                   'p_investigadores_titC_tc': p_investigadores_titC_tc,
                                                   'p_investigadores_asocA_tmp': p_investigadores_asocA_tmp,
                                                   'p_investigadores_asocB_tmp': p_investigadores_asocB_tmp,
                                                   'p_investigadores_asocC_tmp': p_investigadores_asocC_tmp,
                                                   'p_investigadores_asocA_tcp': p_investigadores_asocA_tcp,
                                                   'p_investigadores_asocB_tcp': p_investigadores_asocB_tcp,
                                                   'p_investigadores_asocC_tcp': p_investigadores_asocC_tcp,
                                                   'p_investigadores_titA_tmp': p_investigadores_titA_tmp,
                                                   'p_investigadores_titB_tmp': p_investigadores_titB_tmp,
                                                   'p_investigadores_titC_tmp': p_investigadores_titC_tmp,
                                                   'p_investigadores_titA_tcp': p_investigadores_titA_tcp,
                                                   'p_investigadores_titB_tcp': p_investigadores_titB_tcp,
                                                   'p_investigadores_titC_tcp': p_investigadores_titC_tcp,
                                                   'investigadores_asocA_tm': investigadores_asocA_tm,
                                                   'investigadores_asocB_tm': investigadores_asocB_tm,
                                                   'investigadores_asocC_tm': investigadores_asocC_tm,
                                                   'investigadores_asocA_tc': investigadores_asocA_tc,
                                                   'investigadores_asocB_tc': investigadores_asocB_tc,
                                                   'investigadores_asocC_tc': investigadores_asocC_tc,
                                                   'investigadores_titA_tm': investigadores_titA_tm,
                                                   'investigadores_titB_tm': investigadores_titB_tm,
                                                   'investigadores_titC_tm': investigadores_titC_tm,
                                                   'investigadores_titA_tc': investigadores_titA_tc,
                                                   'investigadores_titB_tc': investigadores_titB_tc,
                                                   'investigadores_titC_tc': investigadores_titC_tc,
                                                   'investigadores_asocA_tmp': investigadores_asocA_tmp,
                                                   'investigadores_asocB_tmp': investigadores_asocB_tmp,
                                                   'investigadores_asocC_tmp': investigadores_asocC_tmp,
                                                   'investigadores_asocA_tcp': investigadores_asocA_tcp,
                                                   'investigadores_asocB_tcp': investigadores_asocB_tcp,
                                                   'investigadores_asocC_tcp': investigadores_asocC_tcp,
                                                   'investigadores_titA_tmp': investigadores_titA_tmp,
                                                   'investigadores_titB_tmp': investigadores_titB_tmp,
                                                   'investigadores_titC_tmp': investigadores_titC_tmp,
                                                   'investigadores_titA_tcp': investigadores_titA_tcp,
                                                   'investigadores_titB_tcp': investigadores_titB_tcp,
                                                   'investigadores_titC_tcp': investigadores_titC_tcp
                                                   }

            p_nom_tecnicos_data = [['Técnicos', 'Porcentaje'],
                                   ['Técnicos auxiliares A, medio tiempo', p_tecnicos_auxA_tm],
                                   ['Técnicos auxiliares B, medio tiempo', p_tecnicos_auxB_tm],
                                   ['Técnicos auxiliares C, medio tiempo', p_tecnicos_auxC_tm],
                                   ['Técnicos auxiliares A, tiempo completo', p_tecnicos_auxA_tc],
                                   ['Técnicos auxiliares B, tiempo completo', p_tecnicos_auxB_tc],
                                   ['Técnicos auxiliares C, tiempo completo', p_tecnicos_auxC_tc],
                                   ['Técnicos asociados A, medio tiempo', p_tecnicos_asocA_tm],
                                   ['Técnicos asociados B, medio tiempo', p_tecnicos_asocB_tm],
                                   ['Técnicos asociados C, medio tiempo', p_tecnicos_asocC_tm],
                                   ['Técnicos asociados A, tiempo completo', p_tecnicos_asocA_tc],
                                   ['Técnicos asociados B, tiempo completo', p_tecnicos_asocB_tc],
                                   ['Técnicos asociados C, tiempo completo', p_tecnicos_asocC_tc],
                                   ['Técnicos titulares A, medio tiempo', p_tecnicos_titA_tm],
                                   ['Técnicos titulares B, medio tiempo', p_tecnicos_titB_tm],
                                   ['Técnicos titulares C, medio tiempo', p_tecnicos_titC_tm],
                                   ['Técnicos titulares A, tiempo completo', p_tecnicos_titA_tc],
                                   ['Técnicos titulares B, tiempo completo', p_tecnicos_titB_tc],
                                   ['Técnicos titulares C, tiempo completo', p_tecnicos_titC_tc],
                                   ]

            nom_tecnicos_data = [['Técnicos', 'Porcentaje'],
                                 ['Técnicos auxiliares A, medio tiempo', tecnicos_auxA_tm],
                                 ['Técnicos auxiliares B, medio tiempo', tecnicos_auxB_tm],
                                 ['Técnicos auxiliares C, medio tiempo', tecnicos_auxC_tm],
                                 ['Técnicos auxiliares A, tiempo completo', tecnicos_auxA_tc],
                                 ['Técnicos auxiliares B, tiempo completo', tecnicos_auxB_tc],
                                 ['Técnicos auxiliares C, tiempo completo', tecnicos_auxC_tc],
                                 ['Técnicos asociados A, medio tiempo', tecnicos_asocA_tm],
                                 ['Técnicos asociados B, medio tiempo', tecnicos_asocB_tm],
                                 ['Técnicos asociados C, medio tiempo', tecnicos_asocC_tm],
                                 ['Técnicos asociados A, tiempo completo', tecnicos_asocA_tc],
                                 ['Técnicos asociados B, tiempo completo', tecnicos_asocB_tc],
                                 ['Técnicos asociados C, tiempo completo', tecnicos_asocC_tc],
                                 ['Técnicos titulares A, medio tiempo', tecnicos_titA_tm],
                                 ['Técnicos titulares B, medio tiempo', tecnicos_titB_tm],
                                 ['Técnicos titulares C, medio tiempo', tecnicos_titC_tm],
                                 ['Técnicos titulares A, tiempo completo', tecnicos_titA_tc],
                                 ['Técnicos titulares B, tiempo completo', tecnicos_titB_tc],
                                 ['Técnicos titulares C, tiempo completo', tecnicos_titC_tc],
                                 ]

            p_data_source = SimpleDataSource(data=p_nom_tecnicos_data)
            p_chart_nom_tecnicos = PieChart(p_data_source)
            context['p_chart_nom_tecnicos'] = p_chart_nom_tecnicos
            print(p_nom_tecnicos_data)

            data_source = SimpleDataSource(data=nom_tecnicos_data)
            chart_nom_tecnicos = PieChart(data_source)
            context['chart_nom_tecnicos'] = chart_nom_tecnicos
            print(nom_tecnicos_data)

            context['table_nom_tecnicos'] = {'p_nom_tecnicos_count': p_nom_tecnicos_count,
                                             'nom_tecnicos_count': nom_tecnicos_count,
                                             'p_tecnicos_auxA_tm': p_tecnicos_auxA_tm,
                                             'p_tecnicos_auxB_tm': p_tecnicos_auxB_tm,
                                             'p_tecnicos_auxC_tm': p_tecnicos_auxC_tm,
                                             'p_tecnicos_auxA_tc': p_tecnicos_auxA_tc,
                                             'p_tecnicos_auxB_tc': p_tecnicos_auxB_tc,
                                             'p_tecnicos_auxC_tc': p_tecnicos_auxC_tc,
                                             'p_tecnicos_asocA_tm': p_tecnicos_asocA_tm,
                                             'p_tecnicos_asocB_tm': p_tecnicos_asocB_tm,
                                             'p_tecnicos_asocC_tm': p_tecnicos_asocC_tm,
                                             'p_tecnicos_asocA_tc': p_tecnicos_asocA_tc,
                                             'p_tecnicos_asocB_tc': p_tecnicos_asocB_tc,
                                             'p_tecnicos_asocC_tc': p_tecnicos_asocC_tc,
                                             'p_tecnicos_titA_tm': p_tecnicos_titA_tm,
                                             'p_tecnicos_titB_tm': p_tecnicos_titB_tm,
                                             'p_tecnicos_titC_tm': p_tecnicos_titC_tm,
                                             'p_tecnicos_titA_tc': p_tecnicos_titA_tc,
                                             'p_tecnicos_titB_tc': p_tecnicos_titB_tc,
                                             'p_tecnicos_titC_tc': p_tecnicos_titC_tc,
                                             'p_tecnicos_auxA_tmp': p_tecnicos_auxA_tmp,
                                             'p_tecnicos_auxB_tmp': p_tecnicos_auxB_tmp,
                                             'p_tecnicos_auxC_tmp': p_tecnicos_auxC_tmp,
                                             'p_tecnicos_auxA_tcp': p_tecnicos_auxA_tcp,
                                             'p_tecnicos_auxB_tcp': p_tecnicos_auxB_tcp,
                                             'p_tecnicos_auxC_tcp': p_tecnicos_auxC_tcp,
                                             'p_tecnicos_asocA_tmp': p_tecnicos_asocA_tmp,
                                             'p_tecnicos_asocB_tmp': p_tecnicos_asocB_tmp,
                                             'p_tecnicos_asocC_tmp': p_tecnicos_asocC_tmp,
                                             'p_tecnicos_asocA_tcp': p_tecnicos_asocA_tcp,
                                             'p_tecnicos_asocB_tcp': p_tecnicos_asocB_tcp,
                                             'p_tecnicos_asocC_tcp': p_tecnicos_asocC_tcp,
                                             'p_tecnicos_titA_tmp': p_tecnicos_titA_tmp,
                                             'p_tecnicos_titB_tmp': p_tecnicos_titB_tmp,
                                             'p_tecnicos_titC_tmp': p_tecnicos_titC_tmp,
                                             'p_tecnicos_titA_tcp': p_tecnicos_titA_tcp,
                                             'p_tecnicos_titB_tcp': p_tecnicos_titB_tcp,
                                             'p_tecnicos_titC_tcp': p_tecnicos_titC_tcp,
                                             'tecnicos_auxA_tm': tecnicos_auxA_tm,
                                             'tecnicos_auxB_tm': tecnicos_auxB_tm,
                                             'tecnicos_auxC_tm': tecnicos_auxC_tm,
                                             'tecnicos_auxA_tc': tecnicos_auxA_tc,
                                             'tecnicos_auxB_tc': tecnicos_auxB_tc,
                                             'tecnicos_auxC_tc': tecnicos_auxC_tc,
                                             'tecnicos_asocA_tm': tecnicos_asocA_tm,
                                             'tecnicos_asocB_tm': tecnicos_asocB_tm,
                                             'tecnicos_asocC_tm': tecnicos_asocC_tm,
                                             'tecnicos_asocA_tc': tecnicos_asocA_tc,
                                             'tecnicos_asocB_tc': tecnicos_asocB_tc,
                                             'tecnicos_asocC_tc': tecnicos_asocC_tc,
                                             'tecnicos_titA_tm': tecnicos_titA_tm,
                                             'tecnicos_titB_tm': tecnicos_titB_tm,
                                             'tecnicos_titC_tm': tecnicos_titC_tm,
                                             'tecnicos_titA_tc': tecnicos_titA_tc,
                                             'tecnicos_titB_tc': tecnicos_titB_tc,
                                             'tecnicos_titC_tc': tecnicos_titC_tc,
                                             'tecnicos_auxA_tmp': tecnicos_auxA_tmp,
                                             'tecnicos_auxB_tmp': tecnicos_auxB_tmp,
                                             'tecnicos_auxC_tmp': tecnicos_auxC_tmp,
                                             'tecnicos_auxA_tcp': tecnicos_auxA_tcp,
                                             'tecnicos_auxB_tcp': tecnicos_auxB_tcp,
                                             'tecnicos_auxC_tcp': tecnicos_auxC_tcp,
                                             'tecnicos_asocA_tmp': tecnicos_asocA_tmp,
                                             'tecnicos_asocB_tmp': tecnicos_asocB_tmp,
                                             'tecnicos_asocC_tmp': tecnicos_asocC_tmp,
                                             'tecnicos_asocA_tcp': tecnicos_asocA_tcp,
                                             'tecnicos_asocB_tcp': tecnicos_asocB_tcp,
                                             'tecnicos_asocC_tcp': tecnicos_asocC_tcp,
                                             'tecnicos_titA_tmp': tecnicos_titA_tmp,
                                             'tecnicos_titB_tmp': tecnicos_titB_tmp,
                                             'tecnicos_titC_tmp': tecnicos_titC_tmp,
                                             'tecnicos_titA_tcp': tecnicos_titA_tcp,
                                             'tecnicos_titB_tcp': tecnicos_titB_tcp,
                                             'tecnicos_titC_tcp': tecnicos_titC_tcp
                                             }

            p_edad_investigadores = User.objects.filter(
                experiencialaboral__nombramiento__nombre__startswith='Investigador', genero='M').filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year - 1)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True))

            p_edad_investigadores_sumy = 0
            p_edad_investigadores_sumc = 0

            for i in p_edad_investigadores:
                if i.fecha_nacimiento:
                    p_edad_investigadores_sumy += this_year - i.fecha_nacimiento.year
                    p_edad_investigadores_sumc += 1

            if p_edad_investigadores_sumc > 0:
                p_edad_investigadores = p_edad_investigadores_sumy / p_edad_investigadores_sumc
            else:
                p_edad_investigadores = 0

            p_edad_investigadoras = User.objects.filter(
                experiencialaboral__nombramiento__nombre__startswith='Investigador', genero='F').filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year - 1)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True))

            p_edad_investigadoras_sumy = 0
            p_edad_investigadoras_sumc = 0

            for i in p_edad_investigadoras:
                if i.fecha_nacimiento:
                    p_edad_investigadoras_sumy += this_year - i.fecha_nacimiento.year
                    p_edad_investigadoras_sumc += 1

            if p_edad_investigadoras_sumc > 0:
                p_edad_investigadoras = p_edad_investigadoras_sumy / p_edad_investigadoras_sumc
            else:
                p_edad_investigadoras = 0

            edad_investigadores = User.objects.filter(
                experiencialaboral__nombramiento__nombre__startswith='Investigador', genero='M').filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True))

            edad_investigadores_sumy = 0
            edad_investigadores_sumc = 0

            for i in edad_investigadores:
                if i.fecha_nacimiento:
                    edad_investigadores_sumy += this_year - i.fecha_nacimiento.year
                    edad_investigadores_sumc += 1

            if edad_investigadores_sumc > 0:
                edad_investigadores = edad_investigadores_sumy / edad_investigadores_sumc
            else:
                edad_investigadores = 0

            edad_investigadoras = User.objects.filter(
                experiencialaboral__nombramiento__nombre__startswith='Investigador', genero='F').filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True))

            edad_investigadoras_sumy = 0
            edad_investigadoras_sumc = 0

            for i in edad_investigadoras:
                if i.fecha_nacimiento:
                    edad_investigadoras_sumy += this_year - i.fecha_nacimiento.year
                    edad_investigadoras_sumc += 1

            if edad_investigadoras_sumc > 0:
                edad_investigadoras = edad_investigadoras_sumy / edad_investigadoras_sumc
            else:
                edad_investigadoras = 0

            #
            #



            p_edad_tecnicos = User.objects.filter(
                experiencialaboral__nombramiento__nombre__startswith='Técnico', genero='M').filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year - 1)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True))

            p_edad_tecnicos_sumy = 0
            p_edad_tecnicos_sumc = 0

            for i in p_edad_tecnicos:
                if i.fecha_nacimiento:
                    p_edad_tecnicos_sumy += this_year - i.fecha_nacimiento.year
                    p_edad_tecnicos_sumc += 1

            if p_edad_tecnicos_sumc > 0:
                p_edad_tecnicos = p_edad_tecnicos_sumy / p_edad_tecnicos_sumc
            else:
                p_edad_tecnicos = 0

            p_edad_tecnicas = User.objects.filter(
                experiencialaboral__nombramiento__nombre__startswith='Técnico', genero='F').filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year - 1)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 2) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True))

            p_edad_tecnicas_sumy = 0
            p_edad_tecnicas_sumc = 0

            for i in p_edad_tecnicas:
                if i.fecha_nacimiento:
                    p_edad_tecnicas_sumy += this_year - i.fecha_nacimiento.year
                    p_edad_tecnicas_sumc += 1

            if p_edad_tecnicas_sumc > 0:
                p_edad_tecnicas = p_edad_tecnicas_sumy / p_edad_tecnicas_sumc
            else:
                p_edad_tecnicas = 0

            edad_tecnicos = User.objects.filter(
                experiencialaboral__nombramiento__nombre__startswith='Técnico', genero='M').filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True))

            edad_tecnicos_sumy = 0
            edad_tecnicos_sumc = 0

            for i in edad_tecnicos:
                if i.fecha_nacimiento:
                    edad_tecnicos_sumy += this_year - i.fecha_nacimiento.year
                    edad_tecnicos_sumc += 1

            if edad_tecnicos_sumc > 0:
                edad_tecnicos = edad_tecnicos_sumy / edad_tecnicos_sumc
            else:
                edad_tecnicos = 0

            edad_tecnicas = User.objects.filter(
                experiencialaboral__nombramiento__nombre__startswith='Técnico', genero='F').filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).filter((Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin__year__gte=this_year)) | (Q(
                experiencialaboral__fecha_inicio__year__lte=this_year - 1) & Q(
                experiencialaboral__fecha_fin=None))).annotate(Count('pk', distinct=True))

            edad_tecnicas_sumy = 0
            edad_tecnicas_sumc = 0

            for i in edad_tecnicas:
                if i.fecha_nacimiento:
                    edad_tecnicas_sumy += this_year - i.fecha_nacimiento.year
                    edad_tecnicas_sumc += 1

            if edad_tecnicas_sumc > 0:
                edad_tecnicas = edad_tecnicas_sumy / edad_tecnicas_sumc
            else:
                edad_tecnicas = 0

            p_edad_investigadores_data = [['Investigadores', 'Porcentaje'],
                                          ['Investigadores', p_edad_investigadores],
                                          ['Investigadoras', p_edad_investigadoras],
                                          ]

            edad_investigadores_data = [['Investigadores', 'Porcentaje'],
                                        ['Investigadores', edad_investigadores],
                                        ['Investigadoras', edad_investigadoras],
                                        ]

            p_edad_tecnicos_data = [['Técnicos', 'Porcentaje'],
                                    ['Técnicos', p_edad_tecnicos],
                                    ['Técnicas', p_edad_tecnicas],
                                    ]

            edad_tecnicos_data = [['Investigadores', 'Porcentaje'],
                                  ['Técnicos', edad_tecnicos],
                                  ['Técnicas', edad_tecnicas],
                                  ]

            p_data_source = SimpleDataSource(data=p_edad_investigadores_data)
            p_chart_edad_investigadores = PieChart(p_data_source)
            context['p_chart_edad_investigadores'] = p_chart_edad_investigadores

            data_source = SimpleDataSource(data=edad_investigadores_data)
            chart_edad_investigadores = PieChart(data_source)
            context['chart_edad_investigadores'] = chart_edad_investigadores

            p_data_source = SimpleDataSource(data=p_edad_tecnicos_data)
            p_chart_edad_tecnicos = PieChart(p_data_source)
            context['p_chart_edad_tecnicos'] = p_chart_edad_tecnicos

            data_source = SimpleDataSource(data=edad_tecnicos_data)
            chart_edad_tecnicos = PieChart(data_source)
            context['chart_edad_tecnicos'] = chart_edad_tecnicos

            #
            #


            p_articulos_cientificos_int_indwos = ArticuloCientifico.objects.exclude(
                revista__pais__nombre='México').filter(
                fecha__year=this_year - 1).filter(
                Q(status='PUBLICADO') | Q(status='EN_PRENSA')).filter(
                Q(indices__nombre='Web of Science: SCI/SSCI/SCI-EX') | Q(indices__nombre='Scopus')).count()

            p_articulos_cientificos_int_indotros = ArticuloCientifico.objects.exclude(
                revista__pais__nombre='México').filter(
                fecha__year=this_year - 1).filter(
                Q(status='PUBLICADO') | Q(status='EN_PRENSA')).exclude(
                Q(indices__nombre='Web of Science: SCI/SSCI/SCI-EX') & Q(indices__nombre='Scopus') & Q(
                    indices__isnull=True)).count()

            p_articulos_cientificos_int_indno = ArticuloCientifico.objects.exclude(
                revista__pais__nombre='México').filter(
                fecha__year=this_year - 1).filter(
                Q(status='PUBLICADO') | Q(status='EN_PRENSA')).filter(
                indices__isnull=True).count()

            #
            p_articulos_cientificos_nal_indwos = ArticuloCientifico.objects.filter(
                revista__pais__nombre='México').filter(
                fecha__year=this_year - 1).filter(
                Q(status='PUBLICADO') | Q(status='EN_PRENSA')).filter(
                Q(indices__nombre='Web of Science: SCI/SSCI/SCI-EX') | Q(indices__nombre='Scopus')).count()

            p_articulos_cientificos_nal_indotros = ArticuloCientifico.objects.filter(
                revista__pais__nombre='México').filter(
                fecha__year=this_year - 1).filter(
                Q(status='PUBLICADO') | Q(status='EN_PRENSA')).exclude(
                Q(indices__nombre='Web of Science: SCI/SSCI/SCI-EX') & Q(indices__nombre='Scopus') & Q(
                    indices__isnull=True)).count()

            p_articulos_cientificos_nal_indno = ArticuloCientifico.objects.filter(
                revista__pais__nombre='México').filter(
                fecha__year=this_year - 1).filter(
                Q(status='PUBLICADO') | Q(status='EN_PRENSA')).filter(
                indices__isnull=True).count()

            #

            articulos_cientificos_int_indwos = ArticuloCientifico.objects.exclude(
                revista__pais__nombre='México').filter(
                fecha__year=this_year).filter(
                Q(status='PUBLICADO') | Q(status='EN_PRENSA')).filter(
                Q(indices__nombre='Web of Science: SCI/SSCI/SCI-EX') | Q(indices__nombre='Scopus')).count()

            articulos_cientificos_int_indotros = ArticuloCientifico.objects.exclude(
                revista__pais__nombre='México').filter(
                fecha__year=this_year).filter(
                Q(status='PUBLICADO') | Q(status='EN_PRENSA')).exclude(
                Q(indices__nombre='Web of Science: SCI/SSCI/SCI-EX') & Q(indices__nombre='Scopus') & Q(
                    indices__isnull=True)).count()

            articulos_cientificos_int_indno = ArticuloCientifico.objects.exclude(
                revista__pais__nombre='México').filter(
                fecha__year=this_year).filter(
                Q(status='PUBLICADO') | Q(status='EN_PRENSA')).filter(
                indices__isnull=True).count()

            #
            articulos_cientificos_nal_indwos = ArticuloCientifico.objects.filter(
                revista__pais__nombre='México').filter(
                fecha__year=this_year).filter(
                Q(status='PUBLICADO') | Q(status='EN_PRENSA')).filter(
                Q(indices__nombre='Web of Science: SCI/SSCI/SCI-EX') | Q(indices__nombre='Scopus')).count()

            articulos_cientificos_nal_indotros = ArticuloCientifico.objects.filter(
                revista__pais__nombre='México').filter(
                fecha__year=this_year).filter(
                Q(status='PUBLICADO') | Q(status='EN_PRENSA')).exclude(
                Q(indices__nombre='Web of Science: SCI/SSCI/SCI-EX') & Q(indices__nombre='Scopus') & Q(
                    indices__isnull=True)).count()

            articulos_cientificos_nal_indno = ArticuloCientifico.objects.filter(
                revista__pais__nombre='México').filter(
                fecha__year=this_year).filter(
                Q(status='PUBLICADO') | Q(status='EN_PRENSA')).filter(
                indices__isnull=True).count()

            articulos_cientificos_data = [['Etiqueta', 'Ind. WOS / Scopus', 'Otros indices', 'No indexadas'],
                                          [str(this_year-1) + ' Int.', p_articulos_cientificos_int_indwos, p_articulos_cientificos_int_indotros, p_articulos_cientificos_int_indno],
                                          [str(this_year) + ' Int.', articulos_cientificos_int_indwos, articulos_cientificos_int_indotros, articulos_cientificos_int_indno],
                                          [str(this_year-1) + ' Nal.', p_articulos_cientificos_nal_indwos, p_articulos_cientificos_nal_indotros, p_articulos_cientificos_nal_indno],
                                          [str(this_year) + ' Nal.', articulos_cientificos_nal_indwos, articulos_cientificos_nal_indotros, articulos_cientificos_nal_indno],
                                          ]

            data_source = SimpleDataSource(data=articulos_cientificos_data)
            chart_articulos_cientificos = BarChart(data_source)
            context['chart_articulos_cientificos'] = chart_articulos_cientificos

            p_avg_articulos_usuario = User.objects.filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gt=this_year - 1)) | (
                Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).filter(
                articulo_cientifico_autores__fecha__year=this_year - 1).filter(Q(articulo_cientifico_autores__status='PUBLICADO') & Q(articulo_cientifico_autores__status='EN_PRENSA')).annotate(Count('pk')).aggregate(Avg('pk__count'))[
                                                'pk__count__avg']
            if p_avg_articulos_usuario:
                p_avg_articulos_usuario = round(p_avg_articulos_usuario, 2)
            else:
                p_avg_articulos_usuario = 0


            avg_articulos_usuario = User.objects.filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gt=this_year - 1)) | (
                Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).filter(
                articulo_cientifico_autores__fecha__year=this_year).filter(Q(articulo_cientifico_autores__status='PUBLICADO') | Q(articulo_cientifico_autores__status='EN_PRENSA')).annotate(Count('pk')).aggregate(Avg('pk__count'))[
                                              'pk__count__avg']
            if avg_articulos_usuario:
                avg_articulos_usuario = round(avg_articulos_usuario, 2)
            else:
                avg_articulos_usuario = 0

            context['table_articulos_cientificos'] = {
                'p_articulos_cientificos_int_indwos': p_articulos_cientificos_int_indwos,
                'p_articulos_cientificos_int_indotros': p_articulos_cientificos_int_indotros,
                'p_articulos_cientificos_int_indno': p_articulos_cientificos_int_indno,
                'articulos_cientificos_int_indwos': articulos_cientificos_int_indwos,
                'articulos_cientificos_int_indotros': articulos_cientificos_int_indotros,
                'articulos_cientificos_int_indno': articulos_cientificos_int_indno,
                'p_articulos_cientificos_nal_indwos': p_articulos_cientificos_nal_indwos,
                'p_articulos_cientificos_nal_indotros': p_articulos_cientificos_nal_indotros,
                'p_articulos_cientificos_nal_indno': p_articulos_cientificos_nal_indno,
                'articulos_cientificos_nal_indwos': articulos_cientificos_nal_indwos,
                'articulos_cientificos_nal_indotros': articulos_cientificos_nal_indotros,
                'articulos_cientificos_nal_indno': articulos_cientificos_nal_indno,
                'p_avg_articulos_usuario': p_avg_articulos_usuario,
                'avg_articulos_usuario': avg_articulos_usuario,
                }


            #

            p_libros_nal = Libro.objects.filter(tipo='INVESTIGACION', pais__nombre='México', fecha__year__gte=this_year - 2,
                                                fecha__year__lte=this_year - 1).filter(Q(status='PUBLICADO') | Q(status='EN_PRENSA')).count()

            libros_nal = Libro.objects.filter(tipo='INVESTIGACION', pais__nombre='México', fecha__year__gte=this_year - 1,
                                                 fecha__year__lte=this_year).filter(Q(status='PUBLICADO') | Q(status='EN_PRENSA')).count()

            p_libros_intl = Libro.objects.filter(tipo='INVESTIGACION', fecha__year__gte=this_year - 2,
                                                fecha__year__lte=this_year - 1).exclude(pais__nombre='México').filter(Q(status='PUBLICADO') | Q(status='EN_PRENSA')).count()

            libros_intl = Libro.objects.filter(tipo='INVESTIGACION', fecha__year__gte=this_year - 1,
                                              fecha__year__lte=this_year).exclude(pais__nombre='México').filter(Q(status='PUBLICADO') | Q(status='EN_PRENSA')).count()


            p_capitulos_libros_nal = CapituloLibroInvestigacion.objects.filter(libro__pais__nombre='México', libro__fecha__year__gte=this_year - 2,
                                                                               libro__fecha__year__lte=this_year - 1).filter(Q(libro__status='PUBLICADO') | Q(libro__status='EN_PRENSA')).count()

            capitulos_libros_nal = CapituloLibroInvestigacion.objects.filter(libro__pais__nombre='México', libro__fecha__year__gte=this_year - 1,
                                                                             libro__fecha__year__lte=this_year).filter(Q(libro__status='PUBLICADO') | Q(libro__status='EN_PRENSA')).count()

            p_capitulos_libros_intl = CapituloLibroInvestigacion.objects.filter(libro__fecha__year__gte=this_year - 2,
                                                                                libro__fecha__year__lte=this_year - 1).exclude(libro__pais__nombre='México').filter(Q(libro__status='PUBLICADO') | Q(libro__status='EN_PRENSA')).count()

            capitulos_libros_intl = CapituloLibroInvestigacion.objects.filter(libro__fecha__year__gte=this_year - 1,
                                                                              libro__fecha__year__lte=this_year).exclude(libro__pais__nombre='México').filter(Q(libro__status='PUBLICADO') | Q(libro__status='EN_PRENSA')).count()


            #

            p_articulos_nal = ArticuloCientifico.objects.filter(revista__pais__nombre='México',
                                                                fecha__year__gte=this_year - 2,
                                                                fecha__year__lte=this_year - 1).filter(Q(status='PUBLICADO') & Q(status='EN_PRENSA')).count()

            articulos_nal = ArticuloCientifico.objects.filter(revista__pais__nombre='México',
                                                                             fecha__year__gte=this_year - 1,
                                                                             fecha__year__lte=this_year).filter(Q(status='PUBLICADO') & Q(status='EN_PRENSA')).count()

            p_articulos_intl = ArticuloCientifico.objects.filter(fecha__year__gte=this_year - 2,
                                                                                fecha__year__lte=this_year - 1).exclude(
                revista__pais__nombre='México').filter(Q(status='PUBLICADO') & Q(status='EN_PRENSA')).count()

            articulos_intl = ArticuloCientifico.objects.filter(fecha__year__gte=this_year - 1,
                                                                              fecha__year__lte=this_year).exclude(
                revista__pais__nombre='México').filter(Q(status='PUBLICADO') & Q(status='EN_PRENSA')).count()


            produccion_data = [['Etiqueta', 'Libros', 'Capitulos de libros', 'Artìculos'],

                           [str(this_year-2) + '-' + str(this_year-1) + ' Nal.', p_libros_nal, p_capitulos_libros_nal, p_articulos_nal],
                           [str(this_year-1) + '-' + str(this_year) + ' Nal.', libros_nal, capitulos_libros_nal, articulos_nal],
                           [str(this_year-2) + '-' + str(this_year-1) + ' Intl.', p_libros_intl, p_capitulos_libros_intl, p_articulos_intl],
                           [str(this_year-1) + '-' + str(this_year) + ' Intl.', libros_intl, capitulos_libros_intl, articulos_intl],
                           ]

            data_source = SimpleDataSource(data=produccion_data)
            chart_produccion  = BarChart(data_source)
            context['chart_produccion'] = chart_produccion

            #

            p_eventos_organizados = OrganizacionEventoAcademico.objects.filter(Q(evento__fecha_inicio__year__gte=this_year - 2) & Q(evento__fecha_fin__year__lte=this_year - 1))
            eventos_organizados = OrganizacionEventoAcademico.objects.filter(Q(evento__fecha_inicio__year__gte=this_year - 1) & Q(evento__fecha_fin__year__lte=this_year))

            eventos_organizados_data = [['Etiqueta', 'Eventos organizados'],
                                        [str(this_year - 2) + '-' + str(this_year - 1), p_eventos_organizados],
                                        [str(this_year - 1) + '-' + str(this_year), eventos_organizados],
                                        ]

            data_source = SimpleDataSource(data=eventos_organizados_data)
            chart_eventos_organizados = BarChart(data_source)
            context['chart_eventos_organizados'] = chart_eventos_organizados

            #

            p_asistencia_eventos_academicos_nal = ParticipacionEventoAcademico.objects.exclude(ambito='INTERNACIONAL').filter(
                Q(evento__fecha_inicio__year__gte=this_year - 2) & Q(evento__fecha_fin__year__lte=this_year - 1))
            asistencia_eventos_academicos_nal = OrganizacionEventoAcademico.objects.exclude(ambito='INTERNACIONAL').filter(
                Q(evento__fecha_inicio__year__gte=this_year - 1) & Q(evento__fecha_fin__year__lte=this_year))

            p_asistencia_eventos_academicos_intl = ParticipacionEventoAcademico.objects.filter(ambito='INTERNACIONAL').filter(
                Q(evento__fecha_inicio__year__gte=this_year - 2) & Q(evento__fecha_fin__year__lte=this_year - 1))
            asistencia_eventos_academicos_intl = OrganizacionEventoAcademico.objects.filter(ambito='INTERNACIONAL').filter(
                Q(evento__fecha_inicio__year__gte=this_year - 1) & Q(evento__fecha_fin__year__lte=this_year))

            asistencia_eventos_academicos_data = [['Etiqueta', 'Nacionales', 'Internacionales'],
                                        [str(this_year - 2) + '-' + str(this_year - 1), p_asistencia_eventos_academicos_nal, p_asistencia_eventos_academicos_intl],
                                        [str(this_year - 1) + '-' + str(this_year), asistencia_eventos_academicos_nal, asistencia_eventos_academicos_intl],
                                        ]

            data_source = SimpleDataSource(data=asistencia_eventos_academicos_data)
            chart_asistencia_eventos_academicos = BarChart(data_source)
            context['chart_asistencia_eventos_academicos'] = chart_asistencia_eventos_academicos

            p_disticion_academicos = DistincionAcademico.objects.filter(fecha__year__gte=this_year - 2, fecha__year__lte=this_year - 1)
            disticion_academicos = DistincionAcademico.objects.filter(fecha__year__gte=this_year - 1, fecha__year__lte=this_year)

            context['p_disticion_academicos'] = p_disticion_academicos
            context['disticion_academicos'] = disticion_academicos













        return render(request, self.template_name, context)



class CVInvestigadorLista(View):
    template_name = 'main3.html'
    this_year = datetime.now().year

    def get(self, request):
        context = {}
        this_year = self.this_year
        investigadoresUNAM = User.objects.filter(experiencialaboral__cargo__nombre='Investigador UNAM',
                                                 experiencialaboral__fecha_inicio__year__lte=this_year,
                                                 experiencialaboral__fecha_fin__isnull=True)
        investigadoresCONACYT = User.objects.filter(experiencialaboral__cargo__nombre='Investigador CONACYT',
                                                    experiencialaboral__fecha_inicio__year__lte=this_year,
                                                    experiencialaboral__fecha_fin__isnull=True)
        investigadoresInvitado = User.objects.filter(experiencialaboral__cargo__nombre='Investigador Invitado',
                                                     experiencialaboral__fecha_inicio__year__lte=this_year,
                                                     experiencialaboral__fecha_fin__isnull=True)

        context['investigadoresUNAM'] = investigadoresUNAM
        context['investigadoresCONACYT'] = investigadoresCONACYT
        context['investigadoresInvitado'] = investigadoresInvitado

        return render(request, self.template_name, context)


class WebPublicacionLista(View):
    template_name = 'web_publicaciones.html'
    this_year = datetime.now().year

    def get(self, request):
        context = {}
        this_year = self.this_year
        publicaciones = Libro.objects.filter(fecha__year=this_year).filter(Q(status='PUBLICADO') | Q(status='EN_PRENSA')).order_by('-fecha')

        context['publicaciones'] = publicaciones

        return render(request, self.template_name, context)


class WebPublicacionDetalle(View):
    template_name = 'web_publicaciones_detalle.html'
    this_year = datetime.now().year

    def get(self, request, pk):
        context = {}
        this_year = self.this_year
        publicacion = Libro.objects.get(pk=pk)

        context['publicacion'] = publicacion

        return render(request, self.template_name, context)


class WebArticuloLista(View):
    template_name = 'web_articulos.html'
    this_year = datetime.now().year

    def get(self, request):
        context = {}
        this_year = self.this_year
        articulos = ArticuloCientifico.objects.filter(fecha__year=this_year).filter(Q(status='PUBLICADO') | Q(status='EN_PRENSA')).order_by('-fecha')

        context['articulos'] = articulos

        return render(request, self.template_name, context)


class WebArticuloDetalle(View):
    template_name = 'web_articulos_detalle.html'
    this_year = datetime.now().year

    def get(self, request, pk):
        context = {}
        this_year = self.this_year
        articulo = ArticuloCientifico.objects.get(pk=pk)

        context['articulo'] = articulo

        return render(request, self.template_name, context)


class WebProyectoLista(View):
    template_name = 'web_proyectos.html'
    this_year = datetime.now().year

    def get(self, request):
        context = {}
        this_year = self.this_year
        proyectos = ProyectoInvestigacion.objects.filter(Q(fecha_inicio__year=this_year) | Q(fecha_fin=None) | Q(fecha_fin__year__gte=this_year)).order_by('-fecha_inicio')

        context['proyectos'] = proyectos

        return render(request, self.template_name, context)


class WebProyectoDetalle(View):
    template_name = 'web_proyectos_detalle.html'
    this_year = datetime.now().year

    def get(self, request, pk):
        context = {}
        proyecto = ProyectoInvestigacion.objects.get(pk=pk)
        context['proyecto'] = proyecto

        return render(request, self.template_name, context)


class CVInvestigadorDetalle(View):
    template_name = 'main4.html'
    this_year = datetime.now().year

    def get(self, request, pk):
        context = {}
        this_year = self.this_year
        usuario = User.objects.get(pk=pk)

        num_articulos = ArticuloCientifico.objects.filter(usuarios__pk=pk).filter(Q(fecha__year=this_year)).count()
        num_libros_investigacion = Libro.objects.filter(tipo='INVESTIGACION', usuarios__pk=pk).filter(Q(fecha__year=this_year)).count()
        num_proyectos_investigacion = ProyectoInvestigacion.objects.filter(usuarios__pk=pk).filter(Q(fecha_fin__year=this_year) | Q(fecha_fin=None)).count()
        doctorados = Doctorado.objects.filter(usuario=pk)
        maestrias = Maestria.objects.filter(usuario=pk)
        licenciaturas = Licenciatura.objects.filter(usuario=pk)
        cursos_especializacion = CursoEspecializacion.objects.filter(usuario=pk).order_by('-fecha_inicio')
        exp_prof_unam = ExperienciaProfesional.objects.filter(usuario=pk).filter(institucion__nombre='Universidad Nacional Autónoma de México (UNAM)', nombramiento__isnull=True).order_by('-fecha_inicio')
        exp_prof_unam_prom = ExperienciaProfesional.objects.filter(usuario=pk).filter(institucion__nombre='Universidad Nacional Autónoma de México (UNAM)', nombramiento__isnull=False).order_by('-fecha_inicio')

        exp_prof_ext = ExperienciaProfesional.objects.filter(usuario=pk).exclude(
            institucion__nombre='Universidad Nacional Autónoma de México (UNAM)').order_by('-fecha_inicio')
        lineas_investigacion = LineaInvestigacion.objects.filter(usuario=pk).order_by('-fecha_inicio')
        capacidades_potencialidades = CapacidadPotencialidad.objects.filter(usuario=pk).order_by('-fecha_inicio')
        articulos_indexadas_extranjeras = ArticuloCientifico.objects.filter(usuarios=pk, indices__isnull=False).exclude(revista__pais__nombre='México').filter(Q(status='PUBLICADO') | Q(status='EN_PRENSA')).order_by('-fecha')
        articulos_indexadas_mexicanas = ArticuloCientifico.objects.filter(usuarios=pk, indices__isnull=False).filter(revista__pais__nombre='México').filter(Q(status='PUBLICADO') | Q(status='EN_PRENSA')).order_by('-fecha')
        articulos_no_indexadas_extranjeras = ArticuloCientifico.objects.filter(usuarios=pk, indices__isnull=True).exclude(revista__pais__nombre='México').filter(Q(status='PUBLICADO') | Q(status='EN_PRENSA')).order_by('-fecha')
        articulos_no_indexadas_mexicanas = ArticuloCientifico.objects.filter(usuarios=pk, indices__isnull=True).filter(revista__pais__nombre='México').filter(Q(status='PUBLICADO') | Q(status='EN_PRENSA')).order_by('-fecha')
        libros_investigacion_editoriales_extranjeras = Libro.objects.filter(tipo='INVESTIGACION').filter(Q(usuarios=pk) | Q(editores=pk) | Q(coordinadores=pk)).exclude(editorial__pais__nombre='México').filter(Q(status='PUBLICADO') | Q(status='EN_PRENSA')).annotate(Count('pk', distinct=True)).order_by('-fecha')
        libros_investigacion_editoriales_mexicanas = Libro.objects.filter(tipo='INVESTIGACION').filter(Q(usuarios=pk) | Q(editores=pk) | Q(coordinadores=pk)).filter(editorial__pais__nombre='México').filter(Q(status='PUBLICADO') | Q(status='EN_PRENSA')).annotate(Count('pk', distinct=True)).order_by('-fecha')


        capitulos_libros_investigacion_editoriales_extranjeras = CapituloLibroInvestigacion.objects.filter(usuarios=pk, libro__tipo='INVESTIGACION').exclude(
            libro__pais__nombre='México').filter(Q(libro__status='PUBLICADO') | Q(libro__status='EN_PRENSA')).order_by('-libro__fecha')
        capitulos_libros_investigacion_editoriales_mexicanas = CapituloLibroInvestigacion.objects.filter(usuarios=pk, libro__tipo='INVESTIGACION').filter(
            libro__pais__nombre='México').filter(Q(libro__status='PUBLICADO') | Q(libro__status='EN_PRENSA')).order_by('-libro__fecha')

        mapas_publicaciones_extranjeras = MapaArbitrado.objects.filter(usuarios=pk).exclude(
            editorial__pais__nombre='México').filter(Q(status='PUBLICADO') | Q(status='EN_PRENSA')).order_by('-fecha')
        mapas_publicaciones_mexicanas = MapaArbitrado.objects.filter(usuarios=pk).filter(
            editorial__pais__nombre='México').filter(Q(status='PUBLICADO') | Q(status='EN_PRENSA')).order_by('-fecha')
        informes_tecnicos_mex = PublicacionTecnica.objects.filter(usuarios=pk).filter(proyecto__institucion__pais__nombre='México').order_by('-fecha')
        informes_tecnicos_intl = PublicacionTecnica.objects.filter(usuarios=pk).exclude(proyecto__institucion__pais__nombre='México').order_by('-fecha')
        articulos_divulgacion_mex = ArticuloDivulgacion.objects.filter(usuarios=pk).filter(revista__pais__nombre='México').filter(Q(status='PUBLICADO') | Q(status='EN_PRENSA')).order_by('-fecha')
        articulos_divulgacion_intl = ArticuloDivulgacion.objects.filter(usuarios=pk).filter(revista__pais__nombre='México').filter(Q(status='PUBLICADO') | Q(status='EN_PRENSA')).order_by('-fecha')

        libros_divulgacion_editoriales_extranjeras = Libro.objects.filter(usuarios=pk, tipo='DIVULGACION').exclude(pais__nombre='México').filter(Q(status='PUBLICADO') | Q(status='EN_PRENSA')).order_by('-fecha')
        libros_divulgacion_editoriales_mexicanas = Libro.objects.filter(usuarios=pk, tipo='DIVULGACION').filter(pais__nombre='México').filter(Q(status='PUBLICADO') | Q(status='EN_PRENSA')).order_by('-fecha')
        capitulos_libros_divulgacion_editoriales_extranjeras = CapituloLibroInvestigacion.objects.filter(usuarios=pk, libro__tipo='DIVULGACION').exclude(libro__pais__nombre='México').filter(Q(libro__status='PUBLICADO') | Q(libro__status='EN_PRENSA')).order_by('-fecha')
        capitulos_libros_divulgacion_editoriales_mexicanas = CapituloLibroInvestigacion.objects.filter(usuarios=pk, libro__tipo='DIVULGACION').filter(libro__pais__nombre='México').filter(Q(libro__status='PUBLICADO') | Q(libro__status='EN_PRENSA')).order_by('-fecha')
        resenas = Resena.objects.filter(usuario=pk).order_by('-fecha')
        material_medios = ProgramaRadioTelevisionInternet.objects.filter(usuario=pk).order_by('-fecha')
        participacion_proyectos_responsable = ProyectoInvestigacion.objects.filter(usuarios=pk).order_by('-fecha_inicio')
        participacion_proyectos_participante = ProyectoInvestigacion.objects.filter(participantes=pk).order_by('-fecha_inicio')
        ponente_eventos_academicos_nal_invitacion = ParticipacionEventoAcademico.objects.filter(usuario=pk, por_invitacion=True).filter(evento__pais__nombre='México').order_by('-evento__fecha_inicio')
        ponente_eventos_academicos_nal_participacion = ParticipacionEventoAcademico.objects.filter(usuario=pk, por_invitacion=False).filter(evento__pais__nombre='México').order_by('-evento__fecha_inicio')
        ponente_eventos_academicos_intl_invitacion = ParticipacionEventoAcademico.objects.filter(usuario=pk, por_invitacion=True).exclude(evento__pais__nombre='México').order_by('-evento__fecha_inicio')
        ponente_eventos_academicos_intl_participacion = ParticipacionEventoAcademico.objects.filter(usuario=pk, por_invitacion=False).exclude(evento__pais__nombre='México').order_by('-evento__fecha_inicio')

        organizacion_eventos_academicos_nacionales = OrganizacionEventoAcademico.objects.filter(usuario=pk).filter(evento__pais__nombre='México').order_by('-evento__fecha_inicio')
        organizacion_eventos_academicos_internacionales = OrganizacionEventoAcademico.objects.filter(usuario=pk).exclude(evento__pais__nombre='México').order_by('-evento__fecha_inicio')


        context['usuario'] = usuario
        context['num_articulos'] = num_articulos
        context['num_libros'] = num_libros_investigacion
        context['num_proyectos_investigacion'] = num_proyectos_investigacion

        context['doctorados'] = doctorados
        context['maestrias'] = maestrias
        context['licenciaturas'] = licenciaturas
        context['cursos_especializacion'] = cursos_especializacion
        context['exp_prof_unam'] = exp_prof_unam
        context['exp_prof_unam_prom'] = exp_prof_unam_prom
        context['exp_prof_ext'] = exp_prof_ext
        context['lineas_investigacion'] = lineas_investigacion
        context['capacidades_potencialidades'] = capacidades_potencialidades
        context['articulos_indexadas_extranjeras'] = articulos_indexadas_extranjeras
        context['articulos_indexadas_mexicanas'] = articulos_indexadas_mexicanas
        context['articulos_no_indexadas_extranjeras'] = articulos_no_indexadas_extranjeras
        context['articulos_no_indexadas_mexicanas'] = articulos_no_indexadas_mexicanas
        context['libros_investigacion_editoriales_mexicanas'] = libros_investigacion_editoriales_mexicanas
        context['libros_investigacion_editoriales_extranjeras'] = libros_investigacion_editoriales_extranjeras
        context['capitulos_libros_investigacion_editoriales_extranjeras'] = capitulos_libros_investigacion_editoriales_extranjeras
        context['capitulos_libros_investigacion_editoriales_mexicanas'] = capitulos_libros_investigacion_editoriales_mexicanas
        context['mapas_publicaciones_extranjeras '] = mapas_publicaciones_extranjeras
        context['mapas_publicaciones_mexicanas '] = mapas_publicaciones_mexicanas
        context['informes_tecnicos_mex'] = informes_tecnicos_mex
        context['informes_tecnicos_intl'] = informes_tecnicos_intl
        context['libros_divulgacion_editoriales_extranjeras'] = libros_divulgacion_editoriales_extranjeras
        context['libros_divulgacion_editoriales_mexicanas'] = libros_divulgacion_editoriales_mexicanas
        context['capitulos_libros_divulgacion_editoriales_extranjeras'] = capitulos_libros_divulgacion_editoriales_extranjeras
        context['capitulos_libros_divulgacion_editoriales_mexicanas'] = capitulos_libros_divulgacion_editoriales_mexicanas
        context['resenas'] = resenas

        context['participacion_proyectos_responsable'] = participacion_proyectos_responsable
        context['participacion_proyectos_participante'] = participacion_proyectos_participante
        context['ponente_eventos_academicos_nal_invitacion'] = ponente_eventos_academicos_nal_invitacion
        context['ponente_eventos_academicos_nal_participacion'] = ponente_eventos_academicos_nal_participacion
        context['ponente_eventos_academicos_intl_invitacion'] = ponente_eventos_academicos_intl_invitacion
        context['ponente_eventos_academicos_intl_participacion'] = ponente_eventos_academicos_intl_participacion
        context['organizacion_eventos_academicos_nacionales'] = organizacion_eventos_academicos_nacionales
        context['organizacion_eventos_academicos_internacionales'] = organizacion_eventos_academicos_internacionales



        return render(request, self.template_name, context)


class CVInvestigadorPDF(View):
    this_year = datetime.now().year

    def get(self, request, pk):
        context = {}
        this_year = self.this_year
        usuario = User.objects.get(pk=pk)

        num_articulos = ArticuloCientifico.objects.filter(usuarios__pk=pk).filter(Q(fecha__year=this_year)).count()
        num_libros_investigacion = Libro.objects.filter(tipo='INVESTIGACION', usuarios__pk=pk).filter(
            Q(fecha__year=this_year)).count()
        num_proyectos_investigacion = ProyectoInvestigacion.objects.filter(usuarios__pk=pk).filter(
            Q(fecha_fin__year=this_year) | Q(fecha_fin=None)).count()
        licenciaturas = Licenciatura.objects.filter(usuario=pk).order_by('-fecha_grado')
        maestrias = Maestria.objects.filter(usuario=pk).order_by('-fecha_grado')
        doctorados = Doctorado.objects.filter(usuario=pk).order_by('-fecha_grado')
        postdoctorados = PostDoctorado.objects.filter(usuario=pk).order_by('-fecha_fin')
        cursos_especializacion = CursoEspecializacion.objects.filter(usuario=pk).order_by('-fecha_inicio')
        exp_prof_unam = ExperienciaProfesional.objects.filter(usuario=pk).filter(
            institucion__nombre='Universidad Nacional Autónoma de México (UNAM)', nombramiento__isnull=True).order_by(
            '-fecha_inicio')
        exp_prof_unam_prom = ExperienciaProfesional.objects.filter(usuario=pk).filter(
            institucion__nombre='Universidad Nacional Autónoma de México (UNAM)', nombramiento__isnull=False).order_by(
            '-fecha_inicio')

        exp_prof_ext = ExperienciaProfesional.objects.filter(usuario=pk).exclude(
            institucion__nombre='Universidad Nacional Autónoma de México (UNAM)').order_by('-fecha_inicio')

        servicios_acad_admnvos = ExperienciaProfesional.objects.filter(usuario=pk).filter(
            institucion__nombre='Universidad Nacional Autónoma de México (UNAM)').exclude(cargo__tipo_cargo='OTRO').order_by(
            '-fecha_inicio')
        comisiones_institucionales = ComisionInstitucionalCIGA.objects.filter(usuario=pk).filter(institucion__nombre='Universidad Nacional Autónoma de México (UNAM)')

        lineas_investigacion = LineaInvestigacion.objects.filter(usuario=pk).order_by('-fecha_inicio')
        capacidades_potencialidades = CapacidadPotencialidad.objects.filter(usuario=pk).order_by('-fecha_inicio')

        articulos_indexadas_extranjeras = ArticuloCientifico.objects.filter(usuarios=pk, indices__isnull=False).exclude(
            revista__pais__nombre='México').filter(Q(status='PUBLICADO') | Q(status='EN_PRENSA')).annotate(Count('usuarios__pk', distinct=True)).order_by('-fecha')
        articulos_indexadas_mexicanas = ArticuloCientifico.objects.filter(usuarios=pk, indices__isnull=False).filter(
            revista__pais__nombre='México').filter(Q(status='PUBLICADO') | Q(status='EN_PRENSA')).annotate(Count('usuarios__pk', distinct=True)).order_by('-fecha')
        articulos_no_indexadas_extranjeras = ArticuloCientifico.objects.filter(usuarios=pk,
                                                                               indices__isnull=True).exclude(
            revista__pais__nombre='México').filter(Q(status='PUBLICADO') | Q(status='EN_PRENSA')).annotate(Count('usuarios__pk', distinct=True)).order_by('-fecha')
        articulos_no_indexadas_mexicanas = ArticuloCientifico.objects.filter(usuarios=pk, indices__isnull=True).filter(
            revista__pais__nombre='México').filter(Q(status='PUBLICADO') | Q(status='EN_PRENSA')).annotate(Count('usuarios__pk', distinct=True)).order_by('-fecha')

        libros_investigacion_editoriales_extranjeras = Libro.objects.filter(tipo='INVESTIGACION').filter(Q(usuarios=pk) | Q(editores=pk) | Q(coordinadores=pk)).exclude(editorial__pais__nombre='México').filter(Q(status='PUBLICADO') | Q(status='EN_PRENSA')).annotate(Count('pk', distinct=True)).order_by('-fecha')
        libros_investigacion_editoriales_mexicanas = Libro.objects.filter(tipo='INVESTIGACION').filter(Q(usuarios=pk) | Q(editores=pk) | Q(coordinadores=pk)).filter(editorial__pais__nombre='México').filter(Q(status='PUBLICADO') | Q(status='EN_PRENSA')).annotate(Count('pk', distinct=True)).order_by('-fecha')

        capitulos_libros_investigacion_editoriales_extranjeras = CapituloLibroInvestigacion.objects.filter(usuarios=pk,
                                                                                                           libro__tipo='INVESTIGACION').exclude(
            libro__editorial__pais__nombre='México').filter(Q(libro__status='PUBLICADO') | Q(libro__status='EN_PRENSA')).order_by(
            '-libro__fecha')
        capitulos_libros_investigacion_editoriales_mexicanas = CapituloLibroInvestigacion.objects.filter(usuarios=pk,
                                                                                                         libro__tipo='INVESTIGACION').filter(
            libro__editorial__pais__nombre='México').filter(Q(libro__status='PUBLICADO') | Q(libro__status='EN_PRENSA')).order_by(
            '-libro__fecha')

        memoriainextenso_extranjeras = MemoriaInExtenso.objects.filter(usuarios=pk).exclude(
            evento__pais__nombre='México').order_by('-evento__fecha_inicio')
        memoriainextenso_mexicanas = MemoriaInExtenso.objects.filter(usuarios=pk).filter(
            evento__pais__nombre='México').order_by('-evento__fecha_inicio')
        mapas_publicaciones_extranjeras = MapaArbitrado.objects.filter(usuarios=pk).exclude(
            editorial__pais__nombre='México').filter(Q(status='PUBLICADO') | Q(status='EN_PRENSA')).order_by('-fecha')
        mapas_publicaciones_mexicanas = MapaArbitrado.objects.filter(usuarios=pk).filter(
            editorial__pais__nombre='México').filter(Q(status='PUBLICADO') | Q(status='EN_PRENSA')).order_by('-fecha')
        informes_tecnicos_mex = PublicacionTecnica.objects.filter(usuarios=pk, es_publico=True).filter(
            proyecto__institucion__pais__nombre='México').order_by('-fecha')
        informes_tecnicos_intl = PublicacionTecnica.objects.filter(usuarios=pk, es_publico=True).exclude(
            proyecto__institucion__pais__nombre='México').order_by('-fecha')
        articulos_divulgacion_mex = ArticuloDivulgacion.objects.filter(usuarios=pk).filter(
            revista__pais__nombre='México').filter(Q(status='PUBLICADO') | Q(status='EN_PRENSA')).order_by('-fecha')
        articulos_divulgacion_intl = ArticuloDivulgacion.objects.filter(usuarios=pk).exclude(
            revista__pais__nombre='México').filter(Q(status='PUBLICADO') | Q(status='EN_PRENSA')).order_by('-fecha')

        libros_divulgacion_editoriales_extranjeras = Libro.objects.filter(usuarios=pk, tipo='DIVULGACION').exclude(pais__nombre='México').filter(Q(status='PUBLICADO') | Q(status='EN_PRENSA')).order_by('-fecha')

        libros_divulgacion_editoriales_mexicanas = Libro.objects.filter(
            usuarios=pk, tipo='DIVULGACION').filter(
            pais__nombre='México').filter(Q(status='PUBLICADO') | Q(status='EN_PRENSA')).order_by('-fecha')
        
        capitulos_libros_divulgacion_editoriales_extranjeras = CapituloLibroInvestigacion.objects.filter(usuarios=pk,
                                                                                                         libro__tipo='DIVULGACION').exclude(
            libro__pais__nombre='México').filter(Q(libro__status='PUBLICADO') | Q(libro__status='EN_PRENSA')).order_by(
            '-fecha')
        capitulos_libros_divulgacion_editoriales_mexicanas = CapituloLibroInvestigacion.objects.filter(usuarios=pk,
                                                                                                       libro__tipo='DIVULGACION').filter(
            libro__pais__nombre='México').filter(Q(libro__status='PUBLICADO') | Q(libro__status='EN_PRENSA')).order_by(
            '-fecha')
        resenas = Resena.objects.filter(usuario=pk).order_by('-fecha')
        traducciones = Traduccion.objects.filter(usuario=pk).order_by('-fecha')
        material_medios_produccion = ProgramaRadioTelevisionInternet.objects.filter(usuario=pk, actividad='PRODUCCION').order_by('-fecha')

        articulos_docencia = ArticuloDocencia.objects.filter(usuarios=pk).order_by('-fecha')
        libros_docencia = Libro.objects.filter(usuarios=pk, tipo='DOCENCIA').filter(Q(status='PUBLICADO') & Q(status='EN_PRENSA')).order_by('-fecha')
        programas_estudio_docencia = ProgramaEstudio.objects.filter(usuario=pk).order_by('-fecha')
        produccion_tecnologica = DesarrolloTecnologico.objects.filter(autores=pk).order_by('-fecha')

        participacion_proyectos_responsable = ProyectoInvestigacion.objects.filter(usuarios=pk).order_by('-fecha_inicio')
        participacion_proyectos_participante = ProyectoInvestigacion.objects.filter(participantes=pk).order_by('-fecha_inicio')

        ponente_eventos_academicos_nal_invitacion = ParticipacionEventoAcademico.objects.filter(usuario=pk,
                                                                                                por_invitacion=True).filter(
            evento__pais__nombre='México').order_by('-evento__fecha_inicio')
        ponente_eventos_academicos_nal_participacion = ParticipacionEventoAcademico.objects.filter(usuario=pk, por_invitacion=False).filter(evento__pais__nombre='México').order_by('-evento__fecha_inicio')
        ponente_eventos_academicos_intl_invitacion = ParticipacionEventoAcademico.objects.filter(usuario=pk, por_invitacion=True).exclude(evento__pais__nombre='México').order_by('-evento__fecha_inicio')
        ponente_eventos_academicos_intl_participacion = ParticipacionEventoAcademico.objects.filter(usuario=pk, por_invitacion=False).exclude(evento__pais__nombre='México').order_by('-evento__fecha_inicio')

        organizacion_eventos_academicos_nacionales = OrganizacionEventoAcademico.objects.filter(usuario=pk).filter(evento__pais__nombre='México').order_by('-evento__fecha_inicio')
        organizacion_eventos_academicos_internacionales = OrganizacionEventoAcademico.objects.filter(usuario=pk).exclude(evento__pais__nombre='México').order_by('-evento__fecha_inicio')

        participacion_comisiones_dictaminadoras_nacionales = ComisionInstitucionalCIGA.objects.filter(usuario=pk).filter(institucion__pais__nombre='México').order_by('-fecha_inicio')

        participacion_comisiones_dictaminadoras_internacionales = ComisionInstitucionalCIGA.objects.filter(usuario=pk).exclude(institucion__pais__nombre='México').order_by('-fecha_inicio')

        dictamenes_articulos_revistas_mexicanas = ArbitrajePublicacionAcademica.objects.filter(usuario=pk, tipo='ARTICULO').filter(articulo__revista__pais__nombre='México').order_by('-fecha_dictamen')
        dictamenes_articulos_revistas_extranjeras = ArbitrajePublicacionAcademica.objects.filter(usuario=pk, tipo='ARTICULO').exclude(articulo__revista__pais__nombre='México').order_by('-fecha_dictamen')
        dictamenes_libros_editoriales_mexicanas = ArbitrajePublicacionAcademica.objects.filter(usuario=pk, tipo='LIBRO').filter(libro__editorial__pais__nombre='México').order_by('-fecha_dictamen')
        dictamenes_libros_editoriales_extranjeras = ArbitrajePublicacionAcademica.objects.filter(usuario=pk, tipo='LIBRO').exclude(libro__editorial__pais__nombre='México').order_by('-fecha_dictamen')

        estancias_academicas = MovilidadAcademica.objects.filter(usuario=pk, tipo='ESTANCIA').order_by('-fecha_inicio')
        profesores_visitantes = MovilidadAcademica.objects.filter(usuario=pk, tipo='INVITACION').order_by('-fecha_inicio')
        sabaticos = MovilidadAcademica.objects.filter(usuario=pk, tipo='SABATICO').order_by('-fecha_inicio')
        participacion_redes_academicas = RedAcademica.objects.filter(usuarios=pk).order_by('-fecha_constitucion')
        convenios_entidades_externas = ConvenioEntidadExterna.objects.filter(usuarios=pk).order_by('-fecha_inicio')
        servicios_asesorias_externas = ServicioAsesoriaExterna.objects.filter(usuario=pk).order_by('-fecha_inicio')
        organizacion_eventos_divulgacion = OrganizacionEventoDivulgacion.objects.filter(usuario=pk).order_by('-evento__fecha_inicio')
        participacion_eventos_divulgacion = ParticipacionEventoDivulgacion.objects.filter(usuario=pk).order_by('-evento__fecha_inicio')

        cursos_extracurriculares_unam = CursoDocenciaExtracurricular.objects.filter(usuario=pk, institucion__nombre='Universidad Nacional Autónoma de México (UNAM)').order_by('-fecha_inicio')
        cursos_extracurriculares_nacionales = CursoDocenciaExtracurricular.objects.filter(usuario=pk, institucion__pais__nombre='México').exclude(institucion__nombre='Universidad Nacional Autónoma de México (UNAM)').order_by('-fecha_inicio')
        cursos_extracurriculares_internacionales = CursoDocenciaExtracurricular.objects.exclude(usuario=pk, institucion__pais__nombre='México').exclude(institucion__nombre='Universidad Nacional Autónoma de México (UNAM)').order_by('-fecha_inicio')
        cursos_escolarizados_licenciatura_titular = CursoDocenciaEscolarizado.objects.filter(usuario=pk, nombramiento='TITULAR').filter(nivel='LICENCIATURA').order_by('-fecha_inicio')
        cursos_escolarizados_licenciatura_colaborador = CursoDocenciaEscolarizado.objects.filter(usuario=pk, nombramiento='COLABORADOR').filter(nivel='LICENCIATURA').order_by('-fecha_inicio')
        cursos_escolarizados_posgrado_titular = CursoDocenciaEscolarizado.objects.filter(usuario=pk, nombramiento='TITULAR').exclude(nivel='LICENCIATURA').order_by('-fecha_inicio')
        cursos_escolarizados_posgrado_colaborador = CursoDocenciaEscolarizado.objects.filter(usuario=pk, nombramiento='COLABORADOR').exclude(nivel='LICENCIATURA').order_by('-fecha_inicio')

        tesis_dirigidas_licenciatura = DireccionTesis.objects.filter(usuarios=pk, nivel_academico='LICENCIATURA', fecha_examen__isnull=False).order_by('-fecha_examen')
        tesis_dirigidas_maestria = DireccionTesis.objects.filter(usuarios=pk, nivel_academico='MAESTRIA', fecha_examen__isnull=False).order_by('-fecha_examen')
        tesis_dirigidas_doctorado = DireccionTesis.objects.filter(usuarios=pk, nivel_academico='DOCTORADO', fecha_examen__isnull=False).order_by('-fecha_examen')

        tesis_proceso_licenciatura = DireccionTesis.objects.filter(usuarios=pk, nivel_academico='LICENCIATURA', fecha_examen__isnull=True).order_by('-fecha_examen')
        tesis_proceso_maestria = DireccionTesis.objects.filter(usuarios=pk, nivel_academico='MAESTRIA', fecha_examen__isnull=True).order_by('-fecha_examen')
        tesis_proceso_doctorado = DireccionTesis.objects.filter(usuarios=pk, nivel_academico='DOCTORADO', fecha_examen__isnull=True).order_by('-fecha_examen')

        asesorias_estudiantes = AsesoriaEstudiante.objects.filter(usuario=pk).filter(Q(tipo='ESTANCIA') | Q(tipo='PRACTICA')).order_by('-fecha_inicio')
        becarios_estudiantes = AsesoriaEstudiante.objects.filter(usuario=pk, tipo='BECARIO').order_by('-fecha_inicio')
        servicio_social_estudiantes = AsesoriaEstudiante.objects.filter(usuario=pk, tipo='SERVICIO_SOCIAL').order_by('-fecha_inicio')
        supervision_investigadores = SupervisionInvestigadorPostDoctoral.objects.filter(usuario=pk).order_by('-fecha_inicio')
        desarrollo_grupos_investigacion = DesarrolloGrupoInvestigacionInterno.objects.filter(usuarios=pk).order_by('-fecha_inicio')
        sinodales_tesis_licenciatura = ComiteTutoral.objects.filter(nivel_academico='LICENCIATURA', sinodales=pk, fecha_examen__isnull=False).order_by('-fecha_examen')
        comite_tutoral_maestria = ComiteTutoral.objects.filter(nivel_academico='MAESTRIA', asesores=pk, fecha_fin__isnull=False).order_by('-fecha_inicio')
        sinodales_tesis_maestria = ComiteTutoral.objects.filter(nivel_academico='MAESTRIA', sinodales=pk, fecha_examen__isnull=False).order_by('-fecha_examen')
        comite_tutoral_doctorado = ComiteTutoral.objects.filter(nivel_academico='DOCTORADO', asesores=pk, fecha_fin__isnull=False).order_by('-fecha_inicio')
        sinodales_tesis_doctorado = ComiteTutoral.objects.filter(nivel_academico='DOCTORADO', sinodales=pk, fecha_examen__isnull=False).order_by('-fecha_examen')
        participacion_candidaturas_doctorales = ComiteCandidaturaDoctoral.objects.filter(Q(asesores=pk) | Q(sinodales=pk)).order_by('-fecha_defensa')
        premios_nacionales = DistincionAcademico.objects.filter(usuario=pk, distincion__tipo='PREMIO').filter(institucion__nombre='México').order_by('-fecha')
        premios_internacionales = DistincionAcademico.objects.filter(usuario=pk, distincion__tipo='PREMIO').exclude(institucion__nombre='México').order_by('-fecha')
        reconocimientos_nacionales = DistincionAcademico.objects.filter(usuario=pk, distincion__tipo='RECONOCIMIENTO').filter(institucion__nombre='México').order_by('-fecha')
        reconocimientos_internacionales = DistincionAcademico.objects.filter(usuario=pk, distincion__tipo='RECONOCIMIENTO').exclude(institucion__nombre='México').order_by('-fecha')
        comisiones_expertos_nacionales = ParticipacionComisionExpertos.objects.filter(usuario=pk).filter(institucion__nombre='México').order_by('-fecha_inicio')
        comisiones_expertos_internacionales = ParticipacionComisionExpertos.objects.filter(usuario=pk).exclude(institucion__nombre='México').order_by('-fecha_inicio')

        participacion_sociedades_cientificas_nacionales = ParticipacionSociedadCientifica.objects.filter(usuario=pk).filter(ambito='NACIONAL').order_by('-fecha_inicio')
        participacion_sociedades_cientificas_internacionales = ParticipacionSociedadCientifica.objects.filter(usuario=pk).filter(ambito='INTERNACIONAL').order_by('-fecha_inicio')
        citas_publicaciones = CitaPublicacion.objects.filter(usuarios=pk)
        material_medios_presencia = ProgramaRadioTelevisionInternet.objects.filter(usuario=pk).exclude(actividad='PRODUCCION').order_by('-fecha')


        context['usuario'] = usuario
        context['num_articulos'] = num_articulos
        context['num_libros'] = num_libros_investigacion
        context['num_proyectos_investigacion'] = num_proyectos_investigacion
        context['licenciaturas'] = licenciaturas
        context['maestrias'] = maestrias
        context['doctorados'] = doctorados
        context['postdoctorados'] = postdoctorados
        context['cursos_especializacion'] = cursos_especializacion
        context['exp_prof_unam'] = exp_prof_unam
        context['exp_prof_unam_prom'] = exp_prof_unam_prom
        context['exp_prof_ext'] = exp_prof_ext
        context['servicios_acad_admnvos'] = servicios_acad_admnvos
        context['comisiones_institucionales'] = comisiones_institucionales
        context['lineas_investigacion'] = lineas_investigacion
        context['capacidades_potencialidades'] = capacidades_potencialidades
        context['articulos_indexadas_extranjeras'] = articulos_indexadas_extranjeras
        context['articulos_indexadas_mexicanas'] = articulos_indexadas_mexicanas
        context['articulos_no_indexadas_extranjeras'] = articulos_no_indexadas_extranjeras
        context['articulos_no_indexadas_mexicanas'] = articulos_no_indexadas_mexicanas
        context['libros_investigacion_editoriales_mexicanas'] = libros_investigacion_editoriales_mexicanas
        context['libros_investigacion_editoriales_extranjeras'] = libros_investigacion_editoriales_extranjeras
        context['capitulos_libros_investigacion_editoriales_extranjeras'] = capitulos_libros_investigacion_editoriales_extranjeras
        context['capitulos_libros_investigacion_editoriales_mexicanas'] = capitulos_libros_investigacion_editoriales_mexicanas
        context['memoriainextenso_extranjeras'] = memoriainextenso_extranjeras
        context['memoriainextenso_mexicanas'] = memoriainextenso_mexicanas
        context['mapas_publicaciones_extranjeras'] = mapas_publicaciones_extranjeras
        context['mapas_publicaciones_mexicanas'] = mapas_publicaciones_mexicanas
        context['informes_tecnicos_mex'] = informes_tecnicos_mex
        context['informes_tecnicos_intl'] = informes_tecnicos_intl
        context['articulos_divulgacion_mex'] = articulos_divulgacion_mex
        context['articulos_divulgacion_intl'] = articulos_divulgacion_intl
        context['libros_divulgacion_editoriales_extranjeras'] = libros_divulgacion_editoriales_extranjeras
        context['libros_divulgacion_editoriales_mexicanas'] = libros_divulgacion_editoriales_mexicanas
        context['capitulos_libros_divulgacion_editoriales_extranjeras'] = capitulos_libros_divulgacion_editoriales_extranjeras
        context['capitulos_libros_divulgacion_editoriales_mexicanas'] = capitulos_libros_divulgacion_editoriales_mexicanas
        context['resenas'] = resenas
        context['traducciones'] = traducciones
        context['material_medios_produccion'] = material_medios_produccion
        context['articulos_docencia'] = articulos_docencia
        context['libros_docencia'] = libros_docencia
        context['programas_estudio_docencia'] = programas_estudio_docencia
        context['produccion_tecnologica'] = produccion_tecnologica
        context['participacion_proyectos_responsable'] = participacion_proyectos_responsable
        context['participacion_proyectos_participante'] = participacion_proyectos_participante
        context['ponente_eventos_academicos_nal_invitacion'] = ponente_eventos_academicos_nal_invitacion
        context['ponente_eventos_academicos_nal_participacion'] = ponente_eventos_academicos_nal_participacion
        context['ponente_eventos_academicos_intl_invitacion'] = ponente_eventos_academicos_intl_invitacion
        context['ponente_eventos_academicos_intl_participacion'] = ponente_eventos_academicos_intl_participacion
        context['organizacion_eventos_academicos_nacionales'] = organizacion_eventos_academicos_nacionales
        context['organizacion_eventos_academicos_internacionales'] = organizacion_eventos_academicos_internacionales
        context['participacion_comisiones_dictaminadoras_nacionales'] = participacion_comisiones_dictaminadoras_nacionales
        context['participacion_comisiones_dictaminadoras_internacionales'] = participacion_comisiones_dictaminadoras_internacionales
        context['dictamenes_articulos_revistas_mexicanas'] = dictamenes_articulos_revistas_mexicanas
        context['dictamenes_articulos_revistas_extranjeras'] = dictamenes_articulos_revistas_extranjeras
        context['dictamenes_libros_editoriales_mexicanas'] = dictamenes_libros_editoriales_mexicanas
        context['dictamenes_libros_editoriales_extranjeras'] = dictamenes_libros_editoriales_extranjeras
        context['estancias_academicas'] = estancias_academicas
        context['profesores_visitantes'] = profesores_visitantes
        context['sabaticos'] = sabaticos
        context['participacion_redes_academicas'] = participacion_redes_academicas
        context['convenios_entidades_externas'] = convenios_entidades_externas
        context['servicios_asesorias_externas'] = servicios_asesorias_externas
        context['organizacion_eventos_divulgacion'] = organizacion_eventos_divulgacion
        context['participacion_eventos_divulgacion'] = participacion_eventos_divulgacion
        context['cursos_extracurriculares_unam'] = cursos_extracurriculares_unam
        context['cursos_extracurriculares_nacionales'] = cursos_extracurriculares_nacionales
        context['cursos_extracurriculares_internacionales'] = cursos_extracurriculares_internacionales
        context['cursos_escolarizados_licenciatura_titular'] = cursos_escolarizados_licenciatura_titular
        context['cursos_escolarizados_licenciatura_colaborador'] = cursos_escolarizados_licenciatura_colaborador
        context['cursos_escolarizados_posgrado_titular'] = cursos_escolarizados_posgrado_titular
        context['cursos_escolarizados_posgrado_colaborador'] = cursos_escolarizados_posgrado_colaborador
        context['tesis_dirigidas_licenciatura'] = tesis_dirigidas_licenciatura
        context['tesis_dirigidas_maestria'] = tesis_dirigidas_maestria
        context['tesis_dirigidas_doctorado'] = tesis_dirigidas_doctorado
        context['tesis_proceso_licenciatura'] = tesis_proceso_licenciatura
        context['tesis_proceso_maestria'] = tesis_proceso_maestria
        context['tesis_proceso_doctorado'] = tesis_proceso_doctorado

        context['asesorias_estudiantes'] = asesorias_estudiantes
        context['becarios_estudiantes'] = becarios_estudiantes
        context['servicio_social_estudiantes'] = servicio_social_estudiantes
        context['supervision_investigadores'] = supervision_investigadores
        context['desarrollo_grupos_investigacion'] = desarrollo_grupos_investigacion
        context['sinodales_tesis_licenciatura'] = sinodales_tesis_licenciatura
        context['comite_tutoral_maestria '] = comite_tutoral_maestria
        context['sinodales_tesis_maestria'] = sinodales_tesis_maestria
        context['comite_tutoral_doctorado'] = comite_tutoral_doctorado
        context['sinodales_tesis_doctorado'] = sinodales_tesis_doctorado
        context['participacion_candidaturas_doctorales'] = participacion_candidaturas_doctorales
        context['premios_nacionales'] = premios_nacionales
        context['premios_internacionales'] = premios_internacionales
        context['reconocimientos_nacionales'] = reconocimientos_nacionales
        context['reconocimientos_internacionales'] = reconocimientos_internacionales
        context['comisiones_expertos_nacionales'] = comisiones_expertos_nacionales
        context['comisiones_expertos_internacionales'] = comisiones_expertos_internacionales
        context['participacion_sociedades_cientificas_nacionales'] = participacion_sociedades_cientificas_nacionales
        context['participacion_sociedades_cientificas_internacionales'] = participacion_sociedades_cientificas_internacionales
        context['citas_publicaciones'] = citas_publicaciones
        context['material_medios_presencia'] = material_medios_presencia








        template = get_template('cv.tex')

        rendered_tpl = template.render(context).replace('&', '\&').encode('utf-8')

        print(template.render(context).replace('&', '\&'))

        with tempfile.TemporaryDirectory() as tempdir:
            for i in range(2):
                process = Popen(
                    ['pdflatex', '-output-directory', tempdir],
                    stdin=PIPE,
                    stdout=PIPE,
                )
                process.communicate(rendered_tpl)
            with open(os.path.join(tempdir, 'texput.pdf'), 'rb') as f:
                pdf = f.read()

        r = HttpResponse(content_type='application/pdf')
        r.write(pdf)
        return r

