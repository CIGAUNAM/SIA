from django.http.response import Http404, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy

from django.core import serializers

from formacion_academica.models import CursoEspecializacion
from investigacion.models import ArticuloCientifico, CapituloLibroInvestigacion, MapaArbitrado, InformeTecnico, ProyectoInvestigacion
from difusion_cientifica.models import MemoriaInExtenso, PrologoLibro, Resena, OrganizacionEventoAcademico, ParticipacionEventoAcademico
from divulgacion_cientifica.models import ArticuloDivulgacion, CapituloLibroDivulgacion, OrganizacionEventoDivulgacion, ParticipacionEventoDivulgacion, ProgramaRadioTelevisionInternet
from vinculacion.models import ArbitrajePublicacionAcademica, ArbitrajeProyectoInvestigacion
from docencia.models import CursoDocencia
from desarrollo_tecnologico.models import DesarrolloTecnologico
from distinciones.models import DistincionAcademico

from nucleo.models import User, Libro, Pais
from datetime import datetime
from django.db.models import Q, Max, Min, Count, Sum



from graphos.sources.simple import SimpleDataSource, BaseDataSource
from graphos.renderers.morris import LineChart, AreaChart, BarChart
#from graphos.renderers.highcharts import LineChart


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
                users_with_items_year_count = User.objects.filter((Q(ingreso_entidad__year__lte=i) & Q(egreso_entidad__year__gt=i)) |
                                        (Q(ingreso_entidad__year__lte=i) & Q(egreso_entidad=None)))
                active_users_per_last_x_year.append(users_with_items_year_count.count())

            #years_cursos_especializacion_dates = CursoEspecializacion.objects.dates('fecha_inicio', 'year', order='DESC')
            #years_cursos_especializacion = []

            #for i in reversed(years_cursos_especializacion_dates[:num_years]):
            #    years_cursos_especializacion.append(str(i.year))

            #cursos_data = [['Año', 'Personas', 'Total horas', 'Mis horas', 'Promedio Horas', 'Max horas', 'Min horas']]


            cursos_data = [['Año', 'Mis horas', 'Promedio horas', 'Max horas', 'Min horas']]
            for i in range(num_years):
                year = last_x_years[i]
                cursos_data.append([str(last_x_years[i])])

                users_with_items_year_count = User.objects.filter(
                    Q(cursos_especializacion__fecha_inicio__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0

                total_course_hours_year_sum = CursoEspecializacion.objects.filter(fecha_inicio__year=year).filter((
                    (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) |
                    (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).aggregate(Sum('horas'))['horas__sum']
                if     total_course_hours_year_sum == None:
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
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).aggregate(Max('cursos_especializacion__horas__sum'))[
                    'cursos_especializacion__horas__sum__max']
                if max_item_year_user == None:
                    max_item_year_user = 0
                cursos_data[i + 1].append(max_item_year_user)

                min_item_year_user = User.objects.filter(cursos_especializacion__fecha_inicio__year=year).annotate(
                    Sum('cursos_especializacion__horas')).filter((
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).aggregate(Min('cursos_especializacion__horas__sum'))[
                    'cursos_especializacion__horas__sum__min']
                if not min_item_year_user:
                    min_item_year_user = 0
                cursos_data[i + 1].append(min_item_year_user)

            data_source = SimpleDataSource(data=cursos_data)
            chart_cursos_especializacion = LineChart(data_source)
            context['chart_cursos_especializacion'] = chart_cursos_especializacion





            items_data = [['Año', 'Mis artículos de investigación', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_articulos_cientificos_enprensa_year_sum = ArticuloCientifico.objects.filter(fecha__year=year,
                                                                                                  status='PUBLICADO').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                    Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()

                request_user_item_year_sum = ArticuloCientifico.objects.filter(fecha__year=year,
                                                                                              status='PUBLICADO',
                                                                                              usuarios=request.user).count()
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

            #print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_articulos_investigacion_publicados = LineChart(data_source)
            context['chart_articulos_investigacion_publicados'] = chart_articulos_investigacion_publicados

            items_data = [['Año', 'Mis artículos de investigación', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_articulos_cientificos_enprensa_year_sum = ArticuloCientifico.objects.filter(fecha__year=year,
                                                                                                  status='EN_PRENSA').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                    Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()

                request_user_item_year_sum = ArticuloCientifico.objects.filter(fecha__year=year,
                                                                                              status='EN_PRENSA',
                                                                                              usuarios=request.user).count()
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

            #print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_articulos_investigacion_enprensa = LineChart(data_source)
            context['chart_articulos_investigacion_enprensa'] = chart_articulos_investigacion_enprensa

            items_data = [['Año', 'Mis artículos de investigación', 'Promedio por persona', 'Max por persona', 'Min por persona']]
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

            #print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_articulos_investigacion_aceptado = LineChart(data_source)
            context['chart_articulos_investigacion_aceptado'] = chart_articulos_investigacion_aceptado












            libros_investigacion_publicado_data = [
                ['Año', 'Mis Libros', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                libros_investigacion_publicado_data.append([str(year)])

                total_libros_cientificos_year_sum = Libro.objects.filter(fecha__year=year, tipo='INVESTIGACION',
                                                                         es_libro_completo=True,
                                                                         status='PUBLICADO').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                    Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()
                request_user_libro_investigacion_year_sum = Libro.objects.filter(fecha__year=year, tipo='INVESTIGACION',
                                                                                 es_libro_completo=True,
                                                                                 status='PUBLICADO',
                                                                                 usuarios=request.user).count()
                if not request_user_libro_investigacion_year_sum:
                    request_user_libro_investigacion_year_sum = 0
                libros_investigacion_publicado_data[i + 1].append(request_user_libro_investigacion_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='INVESTIGACION',
                      libro_autores__es_libro_completo=True, libro_autores__status='PUBLICADO') &
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
                      libro_autores__es_libro_completo=True, libro_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Max('libro_autores__count'))[
                    'libro_autores__count__max']
                if max_libro_investigacion_year_user == None:
                    max_libro_investigacion_year_user = 0
                libros_investigacion_publicado_data[i + 1].append(max_libro_investigacion_year_user)

                min_libro_investigacion_year_user = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='INVESTIGACION',
                      libro_autores__es_libro_completo=True, libro_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Min('libro_autores__count'))[
                    'libro_autores__count__min']
                if min_libro_investigacion_year_user == None:
                    min_libro_investigacion_year_user = 0
                libros_investigacion_publicado_data[i + 1].append(min_libro_investigacion_year_user)

            #print(libros_investigacion_publicado_data)
            data_source = SimpleDataSource(data=libros_investigacion_publicado_data)
            chart_libros_investigacion_publicado = LineChart(data_source)
            context['chart_libros_investigacion_publicado'] = chart_libros_investigacion_publicado


            libros_investigacion_enprensa_data = [
                ['Año', 'Mis Libros', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                libros_investigacion_enprensa_data.append([str(year)])

                total_libros_cientificos_year_sum = Libro.objects.filter(fecha__year=year, tipo='INVESTIGACION',
                                                                         es_libro_completo=True,
                                                                         status='EN_PRENSA').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                    Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()
                request_user_libro_investigacion_year_sum = Libro.objects.filter(fecha__year=year, tipo='INVESTIGACION',
                                                                                 es_libro_completo=True,
                                                                                 status='EN_PRENSA',
                                                                                 usuarios=request.user).count()
                if not request_user_libro_investigacion_year_sum:
                    request_user_libro_investigacion_year_sum = 0
                libros_investigacion_enprensa_data[i + 1].append(request_user_libro_investigacion_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='INVESTIGACION',
                      libro_autores__es_libro_completo=True, libro_autores__status='EN_PRENSA') &
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
                      libro_autores__es_libro_completo=True, libro_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Max('libro_autores__count'))[
                    'libro_autores__count__max']
                if max_libro_investigacion_year_user == None:
                    max_libro_investigacion_year_user = 0
                libros_investigacion_enprensa_data[i + 1].append(max_libro_investigacion_year_user)

                min_libro_investigacion_year_user = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='INVESTIGACION',
                      libro_autores__es_libro_completo=True, libro_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Min('libro_autores__count'))[
                    'libro_autores__count__min']
                if min_libro_investigacion_year_user == None:
                    min_libro_investigacion_year_user = 0
                libros_investigacion_enprensa_data[i + 1].append(min_libro_investigacion_year_user)

            #print(libros_investigacion_enprensa_data)
            data_source = SimpleDataSource(data=libros_investigacion_enprensa_data)
            chart_libros_investigacion_enprensa = LineChart(data_source)
            context['chart_libros_investigacion_enprensa'] = chart_libros_investigacion_enprensa

            libros_investigacion_aceptado_data = [
                ['Año', 'Mis Libros', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                libros_investigacion_aceptado_data.append([str(year)])

                total_libros_cientificos_year_sum = Libro.objects.filter(fecha__year=year, tipo='INVESTIGACION',
                                                                         es_libro_completo=True,
                                                                         status='ACEPTADO').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                    Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()
                request_user_libro_investigacion_year_sum = Libro.objects.filter(fecha__year=year, tipo='INVESTIGACION',
                                                                                 es_libro_completo=True,
                                                                                 status='ACEPTADO',
                                                                                 usuarios=request.user).count()
                if not request_user_libro_investigacion_year_sum:
                    request_user_libro_investigacion_year_sum = 0
                libros_investigacion_aceptado_data[i + 1].append(request_user_libro_investigacion_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='INVESTIGACION',
                      libro_autores__es_libro_completo=True, libro_autores__status='ACEPTADO') &
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
                      libro_autores__es_libro_completo=True, libro_autores__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Max('libro_autores__count'))[
                    'libro_autores__count__max']
                if max_libro_investigacion_year_user == None:
                    max_libro_investigacion_year_user = 0
                libros_investigacion_aceptado_data[i + 1].append(max_libro_investigacion_year_user)

                min_libro_investigacion_year_user = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='INVESTIGACION',
                      libro_autores__es_libro_completo=True, libro_autores__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Min('libro_autores__count'))[
                    'libro_autores__count__min']
                if min_libro_investigacion_year_user == None:
                    min_libro_investigacion_year_user = 0
                libros_investigacion_aceptado_data[i + 1].append(min_libro_investigacion_year_user)

            #print(libros_investigacion_aceptado_data)
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
                    libro__es_libro_completo=False, libro__status='PUBLICADO').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                    Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()

                request_user_capitulos_libros_investigacion_year_sum = CapituloLibroInvestigacion.objects.filter(
                    libro__fecha__year=year, libro__tipo='INVESTIGACION',
                    libro__es_libro_completo=False, libro__status='PUBLICADO',
                    libro__usuarios=request.user).count()
                if not request_user_capitulos_libros_investigacion_year_sum:
                    request_user_capitulos_libros_investigacion_year_sum = 0
                capitulos_libros_investigacion_publicado_data[i + 1].append(
                    request_user_capitulos_libros_investigacion_year_sum)

                users_with_capitulos_libros_investigacion_year_count = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='INVESTIGACION',
                      capitulo_libro_investigacion_autores__libro__es_libro_completo=False,
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
                      capitulo_libro_investigacion_autores__libro__es_libro_completo=False,
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
                      capitulo_libro_investigacion_autores__libro__es_libro_completo=False,
                      capitulo_libro_investigacion_autores__libro__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Min('libro_autores__count'))[
                    'libro_autores__count__min']
                if min_capitulos_libros_investigacion_year_user == None:
                    min_capitulos_libros_investigacion_year_user = 0
                capitulos_libros_investigacion_publicado_data[i + 1].append(
                    min_capitulos_libros_investigacion_year_user)

            #print(capitulos_libros_investigacion_publicado_data)
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
                    libro__es_libro_completo=False, libro__status='EN_PRENSA').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                    Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()

                request_user_capitulos_libros_investigacion_year_sum = CapituloLibroInvestigacion.objects.filter(
                    libro__fecha__year=year, libro__tipo='INVESTIGACION',
                    libro__es_libro_completo=False, libro__status='EN_PRENSA',
                    libro__usuarios=request.user).count()
                if not request_user_capitulos_libros_investigacion_year_sum:
                    request_user_capitulos_libros_investigacion_year_sum = 0
                capitulos_libros_investigacion_enprensa_data[i + 1].append(
                    request_user_capitulos_libros_investigacion_year_sum)

                users_with_capitulos_libros_investigacion_year_count = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='INVESTIGACION',
                      capitulo_libro_investigacion_autores__libro__es_libro_completo=False,
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
                      capitulo_libro_investigacion_autores__libro__es_libro_completo=False,
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
                      capitulo_libro_investigacion_autores__libro__es_libro_completo=False,
                      capitulo_libro_investigacion_autores__libro__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Min('libro_autores__count'))[
                    'libro_autores__count__min']
                if min_capitulos_libros_investigacion_year_user == None:
                    min_capitulos_libros_investigacion_year_user = 0
                capitulos_libros_investigacion_enprensa_data[i + 1].append(
                    min_capitulos_libros_investigacion_year_user)

            #print(capitulos_libros_investigacion_enprensa_data)
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
                    libro__es_libro_completo=False, libro__status='ACEPTADO').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                    Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()

                request_user_capitulos_libros_investigacion_year_sum = CapituloLibroInvestigacion.objects.filter(
                    libro__fecha__year=year, libro__tipo='INVESTIGACION',
                    libro__es_libro_completo=False, libro__status='ACEPTADO',
                    libro__usuarios=request.user).count()
                if not request_user_capitulos_libros_investigacion_year_sum:
                    request_user_capitulos_libros_investigacion_year_sum = 0
                capitulos_libros_investigacion_aceptado_data[i + 1].append(
                    request_user_capitulos_libros_investigacion_year_sum)

                users_with_capitulos_libros_investigacion_year_count = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='INVESTIGACION',
                      capitulo_libro_investigacion_autores__libro__es_libro_completo=False,
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
                      capitulo_libro_investigacion_autores__libro__es_libro_completo=False,
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
                      capitulo_libro_investigacion_autores__libro__es_libro_completo=False,
                      capitulo_libro_investigacion_autores__libro__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Min('libro_autores__count'))[
                    'libro_autores__count__min']
                if min_capitulos_libros_investigacion_year_user == None:
                    min_capitulos_libros_investigacion_year_user = 0
                capitulos_libros_investigacion_aceptado_data[i + 1].append(
                    min_capitulos_libros_investigacion_year_user)

            #print(capitulos_libros_investigacion_aceptado_data)
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
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                        Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()

                request_user_items_year_sum = MapaArbitrado.objects.filter(fecha__year=year,
                                                                           status='PUBLICADO',
                                                                           usuarios=request.user).count()
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

            #print(items_data)
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
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                        Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()

                request_user_items_year_sum = MapaArbitrado.objects.filter(fecha__year=year,
                                                                           status='EN_PRENSA',
                                                                           usuarios=request.user).count()
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

            #print(items_data)
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
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                        Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()

                request_user_items_year_sum = MapaArbitrado.objects.filter(fecha__year=year,
                                                                           status='ACEPTADO',
                                                                           usuarios=request.user).count()
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

            #print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_mapas_arbitrados_aceptados = LineChart(data_source)
            context['chart_mapas_arbitrados_aceptados'] = chart_mapas_arbitrados_aceptados







            items_data = [
                ['Año', 'Mis Informes Técnicos', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = InformeTecnico.objects.filter(fecha__year=year).filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                        Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()

                request_user_items_year_sum = InformeTecnico.objects.filter(fecha__year=year,
                                                                            usuarios=request.user).count()
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

            #print(items_data)
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
                    (Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year))
                    | (Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None))).count()

                request_user_items_year_sum = ProyectoInvestigacion.objects.filter(usuarios=request.user).filter(
                    (Q(fecha_inicio__year__lte=year) & Q(fecha_fin__year__gt=year))
                    | (Q(fecha_inicio__year__lte=year) & Q(fecha_fin=None))).count()
                if not request_user_items_year_sum:
                    request_user_items_year_sum = 0
                items_data[i + 1].append(request_user_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    (Q(proyecto_investigacion_responsables__fecha_inicio__year__lte=year) & Q(proyecto_investigacion_responsables__fecha_fin__year__gt=year))
                    | (Q(proyecto_investigacion_responsables__fecha_inicio__year__lte=year) & Q(proyecto_investigacion_responsables__fecha_fin=None))).filter(
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
                    (Q(proyecto_investigacion_responsables__fecha_inicio__year__lte=year) & Q(proyecto_investigacion_responsables__fecha_fin__year__gt=year))
                    | (Q(proyecto_investigacion_responsables__fecha_inicio__year__lte=year) & Q(proyecto_investigacion_responsables__fecha_fin=None))
                ).filter(((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                          (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('proyecto_investigacion_responsables')).aggregate(Max('proyecto_investigacion_responsables__count'))[
                    'proyecto_investigacion_responsables__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(max_items_year_user)

                min_items_year_user = User.objects.filter(
                    (Q(proyecto_investigacion_responsables__fecha_inicio__year__lte=year) & Q(proyecto_investigacion_responsables__fecha_fin__year__gt=year))
                    | (Q(proyecto_investigacion_responsables__fecha_inicio__year__lte=year) & Q(proyecto_investigacion_responsables__fecha_fin=None))
                ).filter(((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                          (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('proyecto_investigacion_responsables')).aggregate(Min('proyecto_investigacion_responsables__count'))[
                    'proyecto_investigacion_responsables__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(min_items_year_user)

            #print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_proyectos_investigacion = LineChart(data_source)
            context['chart_proyectos_investigacion'] = chart_proyectos_investigacion











            items_data = [
                ['Año', 'Mis Memorias in extenso', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = MemoriaInExtenso.objects.filter(fecha__year=year).filter(
                    (Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year))
                    | (Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None))).count()

                request_user_items_year_sum = MemoriaInExtenso.objects.filter(fecha__year=year, usuarios=request.user).count()
                if not request_user_items_year_sum:
                    request_user_items_year_sum = 0
                items_data[i + 1].append(request_user_items_year_sum)

                users_with_items_year_count = User.objects.filter(memoria_in_extenso_autores__fecha__year=year).filter(
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

                max_items_year_user = User.objects.filter(memoria_in_extenso_autores__fecha__year=year).filter(
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('memoria_in_extenso_autores')).aggregate(
                    Max('memoria_in_extenso_autores__count'))['memoria_in_extenso_autores__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(max_items_year_user)

                min_items_year_user = User.objects.filter(memoria_in_extenso_autores__fecha__year=year).filter(
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('memoria_in_extenso_autores')).aggregate(Min('memoria_in_extenso_autores__count'))[
                    'memoria_in_extenso_autores__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(min_items_year_user)

            #print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_memoria_in_extenso = LineChart(data_source)
            context['chart_memoria_in_extenso'] = chart_memoria_in_extenso




            items_data = [
                ['Año', 'Mis Prologos en libros', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = PrologoLibro.objects.filter(
                    libro__fecha__year=year, libro__tipo='INVESTIGACION',
                    libro__tiene_participacion_prologo=True, libro__status='PUBLICADO').filter(
                    ((Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) |
                     (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).count()

                request_user_items_year_sum = PrologoLibro.objects.filter(
                    libro__fecha__year=year, libro__tipo='INVESTIGACION',
                    libro__tiene_participacion_prologo=True, libro__status='PUBLICADO',
                    usuario=request.user).count()
                if not request_user_items_year_sum:
                    request_user_items_year_sum = 0
                items_data[i + 1].append(
                    request_user_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(prologo_libro_autor__libro__fecha__year=year,
                      prologo_libro_autor__libro__tipo='INVESTIGACION',
                      prologo_libro_autor__libro__tiene_participacion_prologo=True,
                      prologo_libro_autor__libro__status='PUBLICADO') &
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
                    Q(prologo_libro_autor__libro__fecha__year=year,
                      prologo_libro_autor__libro__tipo='INVESTIGACION',
                      prologo_libro_autor__libro__tiene_participacion_prologo=True,
                      prologo_libro_autor__libro__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('prologo_libro_autor')).aggregate(Max('prologo_libro_autor__count'))[
                    'prologo_libro_autor__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(
                    max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(prologo_libro_autor__libro__fecha__year=year,
                      prologo_libro_autor__libro__tipo='INVESTIGACION',
                      prologo_libro_autor__libro__tiene_participacion_prologo=True,
                      prologo_libro_autor__libro__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('prologo_libro_autor')).aggregate(Min('prologo_libro_autor__count'))[
                    'prologo_libro_autor__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(
                    min_items_year_user)

            #print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_prologo_libro_investigacion_publicado = LineChart(data_source)
            context['chart_prologo_libro_investigacion_publicado'] = chart_prologo_libro_investigacion_publicado

























            items_data = [
                ['Año', 'Mis Reseñas', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = Resena.objects.filter(fecha__year=year).filter(
                    ((Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) |
                     (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).count()

                request_user_items_year_sum = Resena.objects.filter(fecha__year=year, usuario=request.user).count()
                if not request_user_items_year_sum:
                    request_user_items_year_sum = 0
                items_data[i + 1].append(
                    request_user_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(resena_autor__fecha__year=year) &
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
                    Q(resena_autor__fecha__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('resena_autor')).aggregate(Max('resena_autor__count'))[
                    'resena_autor__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(
                    max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(resena_autor__fecha__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('resena_autor')).aggregate(Min('resena_autor__count'))[
                    'resena_autor__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(
                    min_items_year_user)

            #print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_resena = LineChart(data_source)
            context['chart_resena'] = chart_resena



            items_data = [['Año', 'Mis Organizaciones de eventos académicos', 'Promedio por persona', 'Max por persona',
                           'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = OrganizacionEventoAcademico.objects.filter(evento__fecha_inicio__year=year).filter(
                    ((Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) |
                     (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).count()

                request_user_items_year_sum = OrganizacionEventoAcademico.objects.filter(evento__fecha_inicio__year=year,
                                                                                         usuario=request.user).count()
                if not request_user_items_year_sum:
                    request_user_items_year_sum = 0
                items_data[i + 1].append(
                    request_user_items_year_sum)

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
                items_data[i + 1].append(
                    min_items_year_user)

            #print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_organizacioneventoacademico = LineChart(data_source)
            context['chart_organizacioneventoacademico'] = chart_organizacioneventoacademico



            items_data = [['Año', 'Mis Participaciones en eventos académicos', 'Promedio por persona', 'Max por persona',
                           'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = ParticipacionEventoAcademico.objects.filter(evento__fecha_inicio__year=year).filter(
                    ((Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) |
                     (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).count()

                request_user_items_year_sum = ParticipacionEventoAcademico.objects.filter(evento__fecha_inicio__year=year,
                                                                                         usuario=request.user).count()
                if not request_user_items_year_sum:
                    request_user_items_year_sum = 0
                items_data[i + 1].append(
                    request_user_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(participacioneventoacademico__evento__fecha_inicio__year=year) &
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
                    Q(participacioneventoacademico__evento__fecha_inicio__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('participacioneventoacademico')).aggregate(Max('participacioneventoacademico__count'))[
                    'participacioneventoacademico__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(
                    max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(organizacioneventoacademico__evento__fecha_inicio__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('participacioneventoacademico')).aggregate(Min('participacioneventoacademico__count'))[
                    'participacioneventoacademico__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(
                    min_items_year_user)

            #print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_participacioneventoacademico = LineChart(data_source)
            context['chart_participacioneventoacademico'] = chart_participacioneventoacademico






            items_data = [['Año', 'Mis artículos de divulgación', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = ArticuloDivulgacion.objects.filter(fecha__year=year, status='PUBLICADO').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                    Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()

                request_user_item_year_sum = ArticuloDivulgacion.objects.filter(fecha__year=year, status='PUBLICADO', usuarios=request.user).count()
                if not request_user_item_year_sum:
                    request_user_item_year_sum = 0
                items_data[i + 1].append(request_user_item_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(articulo_divulgacion_autores__fecha__year=year, articulo_divulgacion_autores__status='PUBLICADO') &
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
                    Q(articulo_divulgacion_autores__fecha__year=year, articulo_divulgacion_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('articulo_divulgacion_autores')).aggregate(Max('articulo_divulgacion_autores__count'))[
                    'articulo_divulgacion_autores__count__max']
                if max_item_year_user == None:
                    max_item_year_user = 0
                items_data[i + 1].append(max_item_year_user)

                min_articulo_cientifico_year_user = User.objects.filter(
                    Q(articulo_divulgacion_autores__fecha__year=year, articulo_divulgacion_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('articulo_divulgacion_autores')).aggregate(Min('articulo_divulgacion_autores__count'))[
                    'articulo_divulgacion_autores__count__min']
                if min_articulo_cientifico_year_user == None:
                    min_articulo_cientifico_year_user = 0
                items_data[i + 1].append(min_articulo_cientifico_year_user)

            #print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_articulo_divulgacion_publicados = LineChart(data_source)
            context['chart_articulo_divulgacion_publicados'] = chart_articulo_divulgacion_publicados


            items_data = [['Año', 'Mis artículos de divulgación', 'Promedio por persona', 'Max por persona', 'Min por persona']]
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
                if not request_user_item_year_sum:
                    request_user_item_year_sum = 0
                items_data[i + 1].append(request_user_item_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(articulo_divulgacion_autores__fecha__year=year, articulo_divulgacion_autores__status='EN_PRENSA') &
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
                    Q(articulo_divulgacion_autores__fecha__year=year, articulo_divulgacion_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('articulo_divulgacion_autores')).aggregate(Max('articulo_divulgacion_autores__count'))[
                    'articulo_divulgacion_autores__count__max']
                if max_item_year_user == None:
                    max_item_year_user = 0
                items_data[i + 1].append(max_item_year_user)

                min_articulo_cientifico_year_user = User.objects.filter(
                    Q(articulo_divulgacion_autores__fecha__year=year, articulo_divulgacion_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('articulo_divulgacion_autores')).aggregate(Min('articulo_divulgacion_autores__count'))[
                    'articulo_divulgacion_autores__count__min']
                if min_articulo_cientifico_year_user == None:
                    min_articulo_cientifico_year_user = 0
                items_data[i + 1].append(min_articulo_cientifico_year_user)

            #print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_articulo_divulgacion_enprensa = LineChart(data_source)
            context['chart_articulo_divulgacion_enprensa'] = chart_articulo_divulgacion_enprensa


            items_data = [['Año', 'Mis artículos de divulgación', 'Promedio por persona', 'Max por persona', 'Min por persona']]
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

            #print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_articulo_divulgacion_aceptados = LineChart(data_source)
            context['chart_articulo_divulgacion_aceptados'] = chart_articulo_divulgacion_aceptados


            items_data = [
                ['Año', 'Mis Libros de divulgación', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = Libro.objects.filter(fecha__year=year, tipo='DIVULGACION',
                                                            es_libro_completo=True,
                                                            status='PUBLICADO').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                        Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()
                request_user_items_year_sum = Libro.objects.filter(fecha__year=year, tipo='DIVULGACION',
                                                                   es_libro_completo=True,
                                                                   status='PUBLICADO',
                                                                   usuarios=request.user).count()
                if not request_user_items_year_sum:
                    request_user_items_year_sum = 0
                items_data[i + 1].append(request_user_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='DIVULGACION',
                      libro_autores__es_libro_completo=True, libro_autores__status='PUBLICADO') &
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
                      libro_autores__es_libro_completo=True, libro_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Max('libro_autores__count'))[
                    'libro_autores__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='DIVULGACION',
                      libro_autores__es_libro_completo=True, libro_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Min('libro_autores__count'))[
                    'libro_autores__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(min_items_year_user)

            #print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_libros_divulgacion_publicados = LineChart(data_source)
            context['chart_libros_divulgacion_publicados'] = chart_libros_divulgacion_publicados


            items_data = [
                ['Año', 'Mis Libros de divulgación', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = Libro.objects.filter(fecha__year=year, tipo='DIVULGACION',
                                                            es_libro_completo=True,
                                                            status='EN_PRENSA').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                        Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()
                request_user_items_year_sum = Libro.objects.filter(fecha__year=year, tipo='DIVULGACION',
                                                                   es_libro_completo=True,
                                                                   status='EN_PRENSA',
                                                                   usuarios=request.user).count()
                if not request_user_items_year_sum:
                    request_user_items_year_sum = 0
                items_data[i + 1].append(request_user_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='DIVULGACION',
                      libro_autores__es_libro_completo=True, libro_autores__status='EN_PRENSA') &
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
                      libro_autores__es_libro_completo=True, libro_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Max('libro_autores__count'))[
                    'libro_autores__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='DIVULGACION',
                      libro_autores__es_libro_completo=True, libro_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Min('libro_autores__count'))[
                    'libro_autores__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(min_items_year_user)

            #print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_libros_divulgacion_enprensa = LineChart(data_source)
            context['chart_libros_divulgacion_enprensa'] = chart_libros_divulgacion_enprensa

            libros_investigacion_aceptado_data = [
                ['Año', 'Mis Libros de divulgación', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                libros_investigacion_aceptado_data.append([str(year)])

                total_items_year_sum = Libro.objects.filter(fecha__year=year, tipo='DIVULGACION',
                                                            es_libro_completo=True,
                                                            status='ACEPTADO').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                        Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()
                request_user_items_year_sum = Libro.objects.filter(fecha__year=year, tipo='DIVULGACION',
                                                                   es_libro_completo=True,
                                                                   status='ACEPTADO',
                                                                   usuarios=request.user).count()
                if not request_user_items_year_sum:
                    request_user_items_year_sum = 0
                libros_investigacion_aceptado_data[i + 1].append(request_user_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='DIVULGACION',
                      libro_autores__es_libro_completo=True, libro_autores__status='ACEPTADO') &
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
                      libro_autores__es_libro_completo=True, libro_autores__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Max('libro_autores__count'))[
                    'libro_autores__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                libros_investigacion_aceptado_data[i + 1].append(max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='DIVULGACION',
                      libro_autores__es_libro_completo=True, libro_autores__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Min('libro_autores__count'))[
                    'libro_autores__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                libros_investigacion_aceptado_data[i + 1].append(min_items_year_user)

            #print(libros_investigacion_aceptado_data)
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
                    libro__es_libro_completo=False, libro__status='PUBLICADO').filter(
                    ((Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) | (
                        Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).count()

                request_user_items_year_sum = CapituloLibroDivulgacion.objects.filter(
                    libro__fecha__year=year, libro__tipo='DIVULGACION',
                    libro__es_libro_completo=False, libro__status='PUBLICADO',
                    libro__usuarios=request.user).count()
                if not request_user_items_year_sum:
                    request_user_items_year_sum = 0
                items_data[i + 1].append(
                    request_user_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='DIVULGACION',
                      capitulo_libro_investigacion_autores__libro__es_libro_completo=False,
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
                      capitulo_libro_investigacion_autores__libro__es_libro_completo=False,
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
                      capitulo_libro_investigacion_autores__libro__es_libro_completo=False,
                      capitulo_libro_investigacion_autores__libro__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Min('libro_autores__count'))[
                    'libro_autores__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(
                    min_items_year_user)

            #print(items_data)
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
                    libro__es_libro_completo=False, libro__status='EN_PRENSA').filter(
                    ((Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) | (
                        Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).count()

                request_user_items_year_sum = CapituloLibroDivulgacion.objects.filter(
                    libro__fecha__year=year, libro__tipo='DIVULGACION',
                    libro__es_libro_completo=False, libro__status='EN_PRENSA',
                    libro__usuarios=request.user).count()
                if not request_user_items_year_sum:
                    request_user_items_year_sum = 0
                capitulos_libros_investigacion_enprensa_data[i + 1].append(
                    request_user_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='DIVULGACION',
                      capitulo_libro_investigacion_autores__libro__es_libro_completo=False,
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
                      capitulo_libro_investigacion_autores__libro__es_libro_completo=False,
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
                      capitulo_libro_investigacion_autores__libro__es_libro_completo=False,
                      capitulo_libro_investigacion_autores__libro__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Min('libro_autores__count'))[
                    'libro_autores__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                capitulos_libros_investigacion_enprensa_data[i + 1].append(
                    min_items_year_user)

            #print(capitulos_libros_investigacion_enprensa_data)
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
                    libro__es_libro_completo=False, libro__status='ACEPTADO').filter(
                    ((Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) | (
                        Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).count()

                request_user_items_year_sum = CapituloLibroDivulgacion.objects.filter(
                    libro__fecha__year=year, libro__tipo='DIVULGACION',
                    libro__es_libro_completo=False, libro__status='ACEPTADO',
                    libro__usuarios=request.user).count()
                if not request_user_items_year_sum:
                    request_user_items_year_sum = 0
                items_data[i + 1].append(
                    request_user_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='DIVULGACION',
                      capitulo_libro_investigacion_autores__libro__es_libro_completo=False,
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
                      capitulo_libro_investigacion_autores__libro__es_libro_completo=False,
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
                      capitulo_libro_investigacion_autores__libro__es_libro_completo=False,
                      capitulo_libro_investigacion_autores__libro__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Min('libro_autores__count'))[
                    'libro_autores__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(
                    min_items_year_user)

            #print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_capitulos_libros_divulgacion_aceptados = LineChart(data_source)
            context['chart_capitulos_libros_divulgacion_aceptados'] = chart_capitulos_libros_divulgacion_aceptados





            items_data = [['Año', 'Mis Organizaciones de eventos de divulgación', 'Promedio por persona', 'Max por persona',
                           'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = OrganizacionEventoDivulgacion.objects.filter(evento__fecha_inicio__year=year).filter(
                    ((Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) |
                     (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).count()

                request_user_items_year_sum = OrganizacionEventoDivulgacion.objects.filter(evento__fecha_inicio__year=year,
                                                                                         usuario=request.user).count()
                if not request_user_items_year_sum:
                    request_user_items_year_sum = 0
                items_data[i + 1].append(
                    request_user_items_year_sum)

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
                items_data[i + 1].append(
                    min_items_year_user)

            #print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_organizacioneventodivulgacion = LineChart(data_source)
            context['chart_organizacioneventodivulgacion'] = chart_organizacioneventodivulgacion



            items_data = [['Año', 'Mis Participaciones en eventos de divulgación', 'Promedio por persona', 'Max por persona',
                           'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = ParticipacionEventoDivulgacion.objects.filter(evento__fecha_inicio__year=year).filter(
                    ((Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) |
                     (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).count()

                request_user_items_year_sum = ParticipacionEventoDivulgacion.objects.filter(evento__fecha_inicio__year=year,
                                                                                         usuario=request.user).count()
                if not request_user_items_year_sum:
                    request_user_items_year_sum = 0
                items_data[i + 1].append(
                    request_user_items_year_sum)

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
                items_data[i + 1].append(
                    min_items_year_user)

            #print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_participacioneventodivulgacion = LineChart(data_source)
            context['chart_participacioneventodivulgacion'] = chart_participacioneventodivulgacion




            items_data = [
                ['Año', 'Mis Participaciones en Programas de Radio, Television, Internet, etc.', 'Promedio por persona', 'Max por persona',
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

            #print(items_data)
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

            #print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_arbitrajepublicacionacademica = LineChart(data_source)
            context['chart_arbitrajepublicacionacademica'] = chart_arbitrajepublicacionacademica




            items_data = [
                ['Año', 'Mis Arbitrajes de Proyectos de investigación', 'Promedio por persona', 'Max por persona',
                 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = ArbitrajeProyectoInvestigacion.objects.filter(fecha__year=year).filter(
                    ((Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) |
                     (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).count()

                request_user_items_year_sum = ArbitrajeProyectoInvestigacion.objects.filter(fecha__year=year,
                                                                                            usuario=request.user).count()
                if not request_user_items_year_sum:
                    request_user_items_year_sum = 0
                items_data[i + 1].append(
                    request_user_items_year_sum)

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
                items_data[i + 1].append(
                    min_items_year_user)

            #print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_arbitrajeproyectoinvestigacion = LineChart(data_source)
            context['chart_arbitrajeproyectoinvestigacion'] = chart_arbitrajeproyectoinvestigacion



















            items_data = [['Año', 'Mis horas de docencia escolarizada', 'Promedio horas', 'Max horas', 'Min horas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(last_x_years[i])])

                users_with_items_year_count = User.objects.filter(
                    Q(cursodocencia_usuario__fecha_inicio__year=year, cursodocencia_usuario__tipo='ESCOLARIZADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0

                total_hours_year_sum = \
                CursoDocencia.objects.filter(fecha_inicio__year=year, tipo='ESCOLARIZADO').filter((
                    (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) |
                    (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).aggregate(
                    Sum('total_horas'))[
                    'total_horas__sum']
                if total_hours_year_sum == None:
                    total_hours_year_sum = 0

                request_user_years_year_sum = User.objects.filter(cursodocencia_usuario__fecha_inicio__year=year,
                                                                  cursodocencia_usuario__tipo='ESCOLARIZADO',
                                                                  cursodocencia_usuario__usuario=request.user).aggregate(
                    Sum('cursodocencia_usuario__total_horas'))['cursodocencia_usuario__total_horas__sum']
                if not request_user_years_year_sum:
                    request_user_years_year_sum = 0
                items_data[i + 1].append(request_user_years_year_sum)

                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(round(total_hours_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(round(0, 2))

                max_item_year_user = User.objects.filter(cursodocencia_usuario__fecha_inicio__year=year,
                                                         cursodocencia_usuario__tipo='ESCOLARIZADO').annotate(
                    Sum('cursodocencia_usuario__total_horas')).filter((
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).aggregate(
                    Max('cursodocencia_usuario__total_horas__sum'))[
                    'cursodocencia_usuario__total_horas__sum__max']
                if max_item_year_user == None:
                    max_item_year_user = 0
                items_data[i + 1].append(max_item_year_user)

                min_item_year_user = User.objects.filter(cursodocencia_usuario__fecha_inicio__year=year,
                                                         cursodocencia_usuario__tipo='ESCOLARIZADO').annotate(
                    Sum('cursodocencia_usuario__total_horas')).filter((
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).aggregate(
                    Min('cursodocencia_usuario__total_horas__sum'))[
                    'cursodocencia_usuario__total_horas__sum__min']
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
                    Q(cursodocencia_usuario__fecha_inicio__year=year, cursodocencia_usuario__tipo='EXTRACURRICULAR') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0

                total_hours_year_sum = \
                CursoDocencia.objects.filter(fecha_inicio__year=year, tipo='EXTRACURRICULAR').filter((
                    (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) |
                    (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).aggregate(
                    Sum('total_horas'))[
                    'total_horas__sum']
                if total_hours_year_sum == None:
                    total_hours_year_sum = 0

                request_user_years_year_sum = User.objects.filter(cursodocencia_usuario__fecha_inicio__year=year,
                                                                  cursodocencia_usuario__tipo='EXTRACURRICULAR',
                                                                  cursodocencia_usuario__usuario=request.user).aggregate(
                    Sum('cursodocencia_usuario__total_horas'))['cursodocencia_usuario__total_horas__sum']
                if not request_user_years_year_sum:
                    request_user_years_year_sum = 0
                items_data[i + 1].append(request_user_years_year_sum)

                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(round(total_hours_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(round(0, 2))

                max_item_year_user = User.objects.filter(cursodocencia_usuario__fecha_inicio__year=year,
                                                         cursodocencia_usuario__tipo='EXTRACURRICULAR').annotate(
                    Sum('cursodocencia_usuario__total_horas')).filter((
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).aggregate(
                    Max('cursodocencia_usuario__total_horas__sum'))[
                    'cursodocencia_usuario__total_horas__sum__max']
                if max_item_year_user == None:
                    max_item_year_user = 0
                items_data[i + 1].append(max_item_year_user)

                min_item_year_user = User.objects.filter(cursodocencia_usuario__fecha_inicio__year=year,
                                                         cursodocencia_usuario__tipo='EXTRACURRICULAR').annotate(
                    Sum('cursodocencia_usuario__total_horas')).filter((
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).aggregate(
                    Min('cursodocencia_usuario__total_horas__sum'))[
                    'cursodocencia_usuario__total_horas__sum__min']
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

                request_user_items_year_sum = DesarrolloTecnologico.objects.filter(fecha__year=year, autores=request.user).count()
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

            #print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_desarrollo_tecnologico = LineChart(data_source)
            context['chart_desarrollo_tecnologico'] = chart_desarrollo_tecnologico



            items_data = [
                ['Año', 'Mis distinciones', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = DistincionAcademico.objects.filter(fecha__year=year).filter(
                    ((Q(condecorados__ingreso_entidad__year__lte=year) & Q(
                        condecorados__egreso_entidad__year__gt=year)) |
                     (Q(condecorados__ingreso_entidad__year__lte=year) & Q(condecorados__egreso_entidad=None)))).count()

                request_user_items_year_sum = DistincionAcademico.objects.filter(fecha__year=year, condecorados=request.user).count()
                if not request_user_items_year_sum:
                    request_user_items_year_sum = 0
                items_data[i + 1].append(
                    request_user_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(distincion_academico_condecorados__fecha__year=year) &
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
                    Q(distincion_academico_condecorados__fecha__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('distincion_academico_condecorados')).aggregate(
                    Max('distincion_academico_condecorados__count'))[
                    'distincion_academico_condecorados__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(
                    max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(distincion_academico_condecorados__fecha__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('distincion_academico_condecorados')).aggregate(
                    Min('distincion_academico_condecorados__count'))[
                    'distincion_academico_condecorados__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(
                    min_items_year_user)

            #print(items_data)
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
                ['Año', 'Total artículos de investigación', 'Promedio por persona', 'Max por persona', 'Min por persona', 'Personas activas', 'Indexados']]
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
                ['Año', 'Total artículos de investigación', 'Promedio por persona', 'Max por persona', 'Min por persona', 'Personas activas']]
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
                ['Año', 'Total artículos de investigación', 'Promedio por persona', 'Max por persona', 'Min por persona', 'Personas activas']]
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
                ['Año', 'Total Libros', 'Promedio por persona', 'Max por persona', 'Min por persona', 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_libros_cientificos_year_sum = Libro.objects.filter(fecha__year=year, tipo='INVESTIGACION',
                                                                         es_libro_completo=True,
                                                                         status='PUBLICADO').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                        Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()
                request_user_libro_investigacion_year_sum = Libro.objects.filter(fecha__year=year, tipo='INVESTIGACION',
                                                                                 es_libro_completo=True,
                                                                                 status='PUBLICADO',
                                                                                 usuarios=request.user).count()
                if not total_libros_cientificos_year_sum:
                    total_libros_cientificos_year_sum = 0
                items_data[i + 1].append(total_libros_cientificos_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='INVESTIGACION',
                      libro_autores__es_libro_completo=True, libro_autores__status='PUBLICADO') &
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
                      libro_autores__es_libro_completo=True, libro_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Max('libro_autores__count'))[
                    'libro_autores__count__max']
                if max_libro_investigacion_year_user == None:
                    max_libro_investigacion_year_user = 0
                items_data[i + 1].append(max_libro_investigacion_year_user)

                min_libro_investigacion_year_user = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='INVESTIGACION',
                      libro_autores__es_libro_completo=True, libro_autores__status='PUBLICADO') &
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
                ['Año', 'Total Libros', 'Promedio por persona', 'Max por persona', 'Min por persona', 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_libros_cientificos_year_sum = Libro.objects.filter(fecha__year=year, tipo='INVESTIGACION',
                                                                         es_libro_completo=True,
                                                                         status='EN_PRENSA').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                        Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()
                request_user_libro_investigacion_year_sum = Libro.objects.filter(fecha__year=year, tipo='INVESTIGACION',
                                                                                 es_libro_completo=True,
                                                                                 status='EN_PRENSA',
                                                                                 usuarios=request.user).count()
                if not total_libros_cientificos_year_sum:
                    total_libros_cientificos_year_sum = 0
                items_data[i + 1].append(total_libros_cientificos_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='INVESTIGACION',
                      libro_autores__es_libro_completo=True, libro_autores__status='EN_PRENSA') &
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
                      libro_autores__es_libro_completo=True, libro_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Max('libro_autores__count'))[
                    'libro_autores__count__max']
                if max_libro_investigacion_year_user == None:
                    max_libro_investigacion_year_user = 0
                items_data[i + 1].append(max_libro_investigacion_year_user)

                min_libro_investigacion_year_user = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='INVESTIGACION',
                      libro_autores__es_libro_completo=True, libro_autores__status='EN_PRENSA') &
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
                ['Año', 'Total Libros', 'Promedio por persona', 'Max por persona', 'Min por persona', 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_libros_cientificos_year_sum = Libro.objects.filter(fecha__year=year, tipo='INVESTIGACION',
                                                                         es_libro_completo=True,
                                                                         status='ACEPTADO').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                        Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()
                request_user_libro_investigacion_year_sum = Libro.objects.filter(fecha__year=year, tipo='INVESTIGACION',
                                                                                 es_libro_completo=True,
                                                                                 status='ACEPTADO',
                                                                                 usuarios=request.user).count()
                if not total_libros_cientificos_year_sum:
                    total_libros_cientificos_year_sum = 0
                items_data[i + 1].append(total_libros_cientificos_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='INVESTIGACION',
                      libro_autores__es_libro_completo=True, libro_autores__status='ACEPTADO') &
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
                      libro_autores__es_libro_completo=True, libro_autores__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Max('libro_autores__count'))[
                    'libro_autores__count__max']
                if max_libro_investigacion_year_user == None:
                    max_libro_investigacion_year_user = 0
                items_data[i + 1].append(max_libro_investigacion_year_user)

                min_libro_investigacion_year_user = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='INVESTIGACION',
                      libro_autores__es_libro_completo=True, libro_autores__status='ACEPTADO') &
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
                ['Año', 'Total Capitulos en libros', 'Promedio por persona', 'Max por persona', 'Min por persona', 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_capitulos_libros_investigacion_year_sum = CapituloLibroInvestigacion.objects.filter(
                    libro__fecha__year=year, libro__tipo='INVESTIGACION',
                    libro__es_libro_completo=False, libro__status='PUBLICADO').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                        Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()

                request_user_capitulos_libros_investigacion_year_sum = CapituloLibroInvestigacion.objects.filter(
                    libro__fecha__year=year, libro__tipo='INVESTIGACION',
                    libro__es_libro_completo=False, libro__status='PUBLICADO',
                    libro__usuarios=request.user).count()

                if not total_capitulos_libros_investigacion_year_sum:
                    total_capitulos_libros_investigacion_year_sum = 0
                items_data[i + 1].append(total_capitulos_libros_investigacion_year_sum)

                users_with_capitulos_libros_investigacion_year_count = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='INVESTIGACION',
                      capitulo_libro_investigacion_autores__libro__es_libro_completo=False,
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
                      capitulo_libro_investigacion_autores__libro__es_libro_completo=False,
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
                      capitulo_libro_investigacion_autores__libro__es_libro_completo=False,
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
                ['Año', 'Total Capitulos en libros', 'Promedio por persona', 'Max por persona', 'Min por persona', 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_capitulos_libros_investigacion_year_sum = CapituloLibroInvestigacion.objects.filter(
                    libro__fecha__year=year, libro__tipo='INVESTIGACION',
                    libro__es_libro_completo=False, libro__status='EN_PRENSA').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                        Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()

                request_user_capitulos_libros_investigacion_year_sum = CapituloLibroInvestigacion.objects.filter(
                    libro__fecha__year=year, libro__tipo='INVESTIGACION',
                    libro__es_libro_completo=False, libro__status='EN_PRENSA',
                    libro__usuarios=request.user).count()

                if not total_capitulos_libros_investigacion_year_sum:
                    total_capitulos_libros_investigacion_year_sum = 0
                items_data[i + 1].append(
                    total_capitulos_libros_investigacion_year_sum)

                users_with_capitulos_libros_investigacion_year_count = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='INVESTIGACION',
                      capitulo_libro_investigacion_autores__libro__es_libro_completo=False,
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
                      capitulo_libro_investigacion_autores__libro__es_libro_completo=False,
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
                      capitulo_libro_investigacion_autores__libro__es_libro_completo=False,
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
                ['Año', 'Total Capitulos en libros', 'Promedio por persona', 'Max por persona', 'Min por persona', 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_capitulos_libros_investigacion_year_sum = CapituloLibroInvestigacion.objects.filter(
                    libro__fecha__year=year, libro__tipo='INVESTIGACION',
                    libro__es_libro_completo=False, libro__status='ACEPTADO').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                        Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()

                request_user_capitulos_libros_investigacion_year_sum = CapituloLibroInvestigacion.objects.filter(
                    libro__fecha__year=year, libro__tipo='INVESTIGACION',
                    libro__es_libro_completo=False, libro__status='ACEPTADO',
                    libro__usuarios=request.user).count()

                if not total_capitulos_libros_investigacion_year_sum:
                    total_capitulos_libros_investigacion_year_sum = 0
                items_data[i + 1].append(
                    total_capitulos_libros_investigacion_year_sum)

                users_with_capitulos_libros_investigacion_year_count = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='INVESTIGACION',
                      capitulo_libro_investigacion_autores__libro__es_libro_completo=False,
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
                      capitulo_libro_investigacion_autores__libro__es_libro_completo=False,
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
                      capitulo_libro_investigacion_autores__libro__es_libro_completo=False,
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
                ['Año', 'Total Mapas', 'Promedio por persona', 'Max por persona', 'Min por persona', 'Personas activas']]
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
                ['Año', 'Total Mapas', 'Promedio por persona', 'Max por persona', 'Min por persona', 'Personas activas']]
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
                ['Año', 'Total Mapas', 'Promedio por persona', 'Max por persona', 'Min por persona', 'Personas activas']]
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
                ['Año', 'Total Informes Técnicos', 'Promedio por persona', 'Max por persona', 'Min por persona', 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = InformeTecnico.objects.filter(fecha__year=year).filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                        Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()

                request_user_items_year_sum = InformeTecnico.objects.filter(fecha__year=year,
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
                ['Año', 'Total Proyectos de investigación', 'Promedio por persona', 'Max por persona', 'Min por persona', 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = ProyectoInvestigacion.objects.filter(tipo='INVESTIGACION').filter(
                    (Q(fecha_inicio__year__lte=year) & Q(fecha_fin__year__gt=year))
                    | (Q(fecha_inicio__year__lte=year) & Q(fecha_fin=None))).filter(
                    (Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year))
                    | (Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None))).count()

                request_user_items_year_sum = ProyectoInvestigacion.objects.filter(tipo='INVESTIGACION',
                                                                                   usuarios=request.user).filter(
                    (Q(fecha_inicio__year__lte=year) & Q(fecha_fin__year__gt=year))
                    | (Q(fecha_inicio__year__lte=year) & Q(fecha_fin=None))).count()
                if not total_items_year_sum:
                    total_items_year_sum = 0
                items_data[i + 1].append(total_items_year_sum)

                users_with_items_year_count = User.objects.filter(proyecto_investigacion_responsables__tipo='INVESTIGACION').filter(
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

                max_items_year_user = User.objects.filter(proyecto_investigacion_responsables__tipo='INVESTIGACION').filter(
                    (Q(proyecto_investigacion_responsables__fecha_inicio__year__lte=year) & Q(
                        proyecto_investigacion_responsables__fecha_fin__year__gt=year))
                    | (
                    Q(proyecto_investigacion_responsables__fecha_inicio__year__lte=year) & Q(proyecto_investigacion_responsables__fecha_fin=None))
                ).filter(((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                          (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('proyecto_investigacion_responsables')).aggregate(Max('proyecto_investigacion_responsables__count'))[
                    'proyecto_investigacion_responsables__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(max_items_year_user)

                min_items_year_user = User.objects.filter(proyecto_investigacion_responsables__tipo='INVESTIGACION').filter(
                    (Q(proyecto_investigacion_responsables__fecha_inicio__year__lte=year) & Q(
                        proyecto_investigacion_responsables__fecha_fin__year__gt=year))
                    | (
                    Q(proyecto_investigacion_responsables__fecha_inicio__year__lte=year) & Q(proyecto_investigacion_responsables__fecha_fin=None))
                ).filter(((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                          (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('proyecto_investigacion_responsables')).aggregate(Min('proyecto_investigacion_responsables__count'))[
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
                ['Año', 'Total Memorias in extenso', 'Promedio por persona', 'Max por persona', 'Min por persona', 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = MemoriaInExtenso.objects.filter(fecha__year=year).filter(
                    (Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year))
                    | (Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None))).count()

                request_user_items_year_sum = MemoriaInExtenso.objects.filter(fecha__year=year,
                                                                              usuarios=request.user).count()
                if not total_items_year_sum:
                    total_items_year_sum = 0
                items_data[i + 1].append(total_items_year_sum)

                users_with_items_year_count = User.objects.filter(memoria_in_extenso_autores__fecha__year=year).filter(
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

                max_items_year_user = User.objects.filter(memoria_in_extenso_autores__fecha__year=year).filter(
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('memoria_in_extenso_autores')).aggregate(
                    Max('memoria_in_extenso_autores__count'))['memoria_in_extenso_autores__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(max_items_year_user)

                min_items_year_user = User.objects.filter(memoria_in_extenso_autores__fecha__year=year).filter(
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
                ['Año', 'Total Prologos en libros', 'Promedio por persona', 'Max por persona', 'Min por persona', 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = PrologoLibro.objects.filter(
                    libro__fecha__year=year, libro__tipo='INVESTIGACION',
                    libro__tiene_participacion_prologo=True, libro__status='PUBLICADO').filter(
                    ((Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) |
                     (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).count()

                request_user_items_year_sum = PrologoLibro.objects.filter(
                    libro__fecha__year=year, libro__tipo='INVESTIGACION',
                    libro__tiene_participacion_prologo=True, libro__status='PUBLICADO',
                    usuario=request.user).count()

                if not total_items_year_sum:
                    total_items_year_sum = 0
                items_data[i + 1].append(total_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(prologo_libro_autor__libro__fecha__year=year,
                      prologo_libro_autor__libro__tipo='INVESTIGACION',
                      prologo_libro_autor__libro__tiene_participacion_prologo=True,
                      prologo_libro_autor__libro__status='PUBLICADO') &
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
                    Q(prologo_libro_autor__libro__fecha__year=year,
                      prologo_libro_autor__libro__tipo='INVESTIGACION',
                      prologo_libro_autor__libro__tiene_participacion_prologo=True,
                      prologo_libro_autor__libro__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('prologo_libro_autor')).aggregate(Max('prologo_libro_autor__count'))[
                    'prologo_libro_autor__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(
                    max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(prologo_libro_autor__libro__fecha__year=year,
                      prologo_libro_autor__libro__tipo='INVESTIGACION',
                      prologo_libro_autor__libro__tiene_participacion_prologo=True,
                      prologo_libro_autor__libro__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('prologo_libro_autor')).aggregate(Min('prologo_libro_autor__count'))[
                    'prologo_libro_autor__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(min_items_year_user)
                items_data[i + 1].append(users_with_items_year_count)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            hchart_prologo_libro_investigacion_publicado = LineChart(data_source)
            context['hchart_prologo_libro_investigacion_publicado'] = hchart_prologo_libro_investigacion_publicado

            items_data = [
                ['Año', 'Total Reseñas', 'Promedio por persona', 'Max por persona', 'Min por persona', 'Personas activas']]
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
                    Q(resena_autor__fecha__year=year) &
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
                    Q(resena_autor__fecha__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('resena_autor')).aggregate(Max('resena_autor__count'))[
                    'resena_autor__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(
                    max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(resena_autor__fecha__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('resena_autor')).aggregate(Min('resena_autor__count'))[
                    'resena_autor__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(min_items_year_user)
                items_data[i + 1].append(users_with_items_year_count)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            hchart_resena = LineChart(data_source)
            context['hchart_resena'] = hchart_resena

            items_data = [['Año', 'Total Organizaciones de eventos académicos', 'Promedio por persona', 'Max por persona',
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
                    Q(participacioneventoacademico__evento__fecha_inicio__year=year) &
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
                    Q(participacioneventoacademico__evento__fecha_inicio__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('participacioneventoacademico')).aggregate(Max('participacioneventoacademico__count'))[
                    'participacioneventoacademico__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(
                    max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(organizacioneventoacademico__evento__fecha_inicio__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('participacioneventoacademico')).aggregate(Min('participacioneventoacademico__count'))[
                    'participacioneventoacademico__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(min_items_year_user)
                items_data[i + 1].append(users_with_items_year_count)

            # print(items_data)
            data_source = SimpleDataSource(data=items_data)
            hchart_participacioneventoacademico = LineChart(data_source)
            context['hchart_participacioneventoacademico'] = hchart_participacioneventoacademico

            items_data = [
                ['Año', 'Total artículos de divulgación', 'Promedio por persona', 'Max por persona', 'Min por persona', 'Personas activas']]
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
                ['Año', 'Total artículos de divulgación', 'Promedio por persona', 'Max por persona', 'Min por persona', 'Personas activas']]
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
                ['Año', 'Total artículos de divulgación', 'Promedio por persona', 'Max por persona', 'Min por persona', 'Personas activas']]
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
                ['Año', 'Total Libros de divulgación', 'Promedio por persona', 'Max por persona', 'Min por persona', 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = Libro.objects.filter(fecha__year=year, tipo='DIVULGACION',
                                                            es_libro_completo=True,
                                                            status='PUBLICADO').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                        Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()
                request_user_items_year_sum = Libro.objects.filter(fecha__year=year, tipo='DIVULGACION',
                                                                   es_libro_completo=True,
                                                                   status='PUBLICADO',
                                                                   usuarios=request.user).count()
                if not total_items_year_sum:
                    total_items_year_sum = 0
                items_data[i + 1].append(total_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='DIVULGACION',
                      libro_autores__es_libro_completo=True, libro_autores__status='PUBLICADO') &
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
                      libro_autores__es_libro_completo=True, libro_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Max('libro_autores__count'))[
                    'libro_autores__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='DIVULGACION',
                      libro_autores__es_libro_completo=True, libro_autores__status='PUBLICADO') &
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
                ['Año', 'Total Libros de divulgación', 'Promedio por persona', 'Max por persona', 'Min por persona', 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = Libro.objects.filter(fecha__year=year, tipo='DIVULGACION',
                                                            es_libro_completo=True,
                                                            status='EN_PRENSA').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                        Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()
                request_user_items_year_sum = Libro.objects.filter(fecha__year=year, tipo='DIVULGACION',
                                                                   es_libro_completo=True,
                                                                   status='EN_PRENSA',
                                                                   usuarios=request.user).count()
                if not total_items_year_sum:
                    total_items_year_sum = 0
                items_data[i + 1].append(total_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='DIVULGACION',
                      libro_autores__es_libro_completo=True, libro_autores__status='EN_PRENSA') &
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
                      libro_autores__es_libro_completo=True, libro_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Max('libro_autores__count'))[
                    'libro_autores__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='DIVULGACION',
                      libro_autores__es_libro_completo=True, libro_autores__status='EN_PRENSA') &
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
                ['Año', 'Total Libros de divulgación', 'Promedio por persona', 'Max por persona', 'Min por persona', 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = Libro.objects.filter(fecha__year=year, tipo='DIVULGACION',
                                                            es_libro_completo=True,
                                                            status='ACEPTADO').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                        Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()
                request_user_items_year_sum = Libro.objects.filter(fecha__year=year, tipo='DIVULGACION',
                                                                   es_libro_completo=True,
                                                                   status='ACEPTADO',
                                                                   usuarios=request.user).count()
                if not total_items_year_sum:
                    total_items_year_sum = 0
                items_data[i + 1].append(total_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='DIVULGACION',
                      libro_autores__es_libro_completo=True, libro_autores__status='ACEPTADO') &
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
                      libro_autores__es_libro_completo=True, libro_autores__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('libro_autores')).aggregate(Max('libro_autores__count'))[
                    'libro_autores__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='DIVULGACION',
                      libro_autores__es_libro_completo=True, libro_autores__status='ACEPTADO') &
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
                    libro__es_libro_completo=False, libro__status='PUBLICADO').filter(
                    ((Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) | (
                        Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).count()

                request_user_items_year_sum = CapituloLibroDivulgacion.objects.filter(
                    libro__fecha__year=year, libro__tipo='DIVULGACION',
                    libro__es_libro_completo=False, libro__status='PUBLICADO',
                    libro__usuarios=request.user).count()

                if not total_items_year_sum:
                    total_items_year_sum = 0
                items_data[i + 1].append(
                    total_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='DIVULGACION',
                      capitulo_libro_investigacion_autores__libro__es_libro_completo=False,
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
                      capitulo_libro_investigacion_autores__libro__es_libro_completo=False,
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
                      capitulo_libro_investigacion_autores__libro__es_libro_completo=False,
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
                    libro__es_libro_completo=False, libro__status='EN_PRENSA').filter(
                    ((Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) | (
                        Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).count()

                request_user_items_year_sum = CapituloLibroDivulgacion.objects.filter(
                    libro__fecha__year=year, libro__tipo='DIVULGACION',
                    libro__es_libro_completo=False, libro__status='EN_PRENSA',
                    libro__usuarios=request.user).count()

                if not total_items_year_sum:
                    total_items_year_sum = 0
                items_data[i + 1].append(
                    total_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='DIVULGACION',
                      capitulo_libro_investigacion_autores__libro__es_libro_completo=False,
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
                      capitulo_libro_investigacion_autores__libro__es_libro_completo=False,
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
                      capitulo_libro_investigacion_autores__libro__es_libro_completo=False,
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
                    libro__es_libro_completo=False, libro__status='ACEPTADO').filter(
                    ((Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) | (
                        Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).count()

                request_user_items_year_sum = CapituloLibroDivulgacion.objects.filter(
                    libro__fecha__year=year, libro__tipo='DIVULGACION',
                    libro__es_libro_completo=False, libro__status='ACEPTADO',
                    libro__usuarios=request.user).count()

                if not total_items_year_sum:
                    total_items_year_sum = 0
                items_data[i + 1].append(total_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(capitulo_libro_investigacion_autores__libro__fecha__year=year,
                      capitulo_libro_investigacion_autores__libro__tipo='DIVULGACION',
                      capitulo_libro_investigacion_autores__libro__es_libro_completo=False,
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
                      capitulo_libro_investigacion_autores__libro__es_libro_completo=False,
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
                      capitulo_libro_investigacion_autores__libro__es_libro_completo=False,
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
                ['Año', 'Total Participaciones en Programas de Radio, Television, Internet, etc.', 'Promedio por persona',
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

            print(items_data)
            data_source = SimpleDataSource(data=items_data)
            hchart_arbitrajeproyectoinvestigacion = LineChart(data_source)
            context['hchart_arbitrajeproyectoinvestigacion'] = hchart_arbitrajeproyectoinvestigacion

            items_data = [['Año', 'Total horas de docencia escolarizada', 'Promedio horas', 'Max horas', 'Min horas', 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(last_x_years[i])])

                users_with_items_year_count = User.objects.filter(
                    Q(cursodocencia_usuario__fecha_inicio__year=year, cursodocencia_usuario__tipo='ESCOLARIZADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0

                total_hours_year_sum = \
                    CursoDocencia.objects.filter(fecha_inicio__year=year, tipo='ESCOLARIZADO').filter((
                        (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) |
                        (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).aggregate(
                        Sum('total_horas'))[
                        'total_horas__sum']
                if total_hours_year_sum == None:
                    total_hours_year_sum = 0

                request_user_years_year_sum = User.objects.filter(cursodocencia_usuario__fecha_inicio__year=year,
                                                                  cursodocencia_usuario__tipo='ESCOLARIZADO',
                                                                  cursodocencia_usuario__usuario=request.user).aggregate(
                    Sum('cursodocencia_usuario__total_horas'))['cursodocencia_usuario__total_horas__sum']

                if not total_hours_year_sum:
                    total_hours_year_sum = 0
                items_data[i + 1].append(total_hours_year_sum)

                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(round(total_hours_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(round(0, 2))

                max_item_year_user = User.objects.filter(cursodocencia_usuario__fecha_inicio__year=year,
                                                         cursodocencia_usuario__tipo='ESCOLARIZADO').annotate(
                    Sum('cursodocencia_usuario__total_horas')).filter((
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).aggregate(
                    Max('cursodocencia_usuario__total_horas__sum'))[
                    'cursodocencia_usuario__total_horas__sum__max']
                if max_item_year_user == None:
                    max_item_year_user = 0
                items_data[i + 1].append(max_item_year_user)

                min_item_year_user = User.objects.filter(cursodocencia_usuario__fecha_inicio__year=year,
                                                         cursodocencia_usuario__tipo='ESCOLARIZADO').annotate(
                    Sum('cursodocencia_usuario__total_horas')).filter((
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).aggregate(
                    Min('cursodocencia_usuario__total_horas__sum'))[
                    'cursodocencia_usuario__total_horas__sum__min']
                if not min_item_year_user:
                    min_item_year_user = 0
                items_data[i + 1].append(min_item_year_user)
                items_data[i + 1].append(users_with_items_year_count)

            data_source = SimpleDataSource(data=items_data)
            hchart_cursodocencia_escolarizado = LineChart(data_source)
            context['hchart_cursodocencia_escolarizado'] = hchart_cursodocencia_escolarizado

            items_data = [['Año', 'Total horas de docencia extracurricular', 'Promedio horas', 'Max horas', 'Min horas', 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(last_x_years[i])])

                users_with_items_year_count = User.objects.filter(
                    Q(cursodocencia_usuario__fecha_inicio__year=year, cursodocencia_usuario__tipo='EXTRACURRICULAR') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_items_year_count == None:
                    users_with_items_year_count = 0

                total_hours_year_sum = \
                    CursoDocencia.objects.filter(fecha_inicio__year=year, tipo='EXTRACURRICULAR').filter((
                        (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) |
                        (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).aggregate(
                        Sum('total_horas'))[
                        'total_horas__sum']
                if total_hours_year_sum == None:
                    total_hours_year_sum = 0

                request_user_years_year_sum = User.objects.filter(cursodocencia_usuario__fecha_inicio__year=year,
                                                                  cursodocencia_usuario__tipo='EXTRACURRICULAR',
                                                                  cursodocencia_usuario__usuario=request.user).aggregate(
                    Sum('cursodocencia_usuario__total_horas'))['cursodocencia_usuario__total_horas__sum']

                if not total_hours_year_sum:
                    total_hours_year_sum = 0
                items_data[i + 1].append(total_hours_year_sum)

                if users_with_items_year_count == None:
                    users_with_items_year_count = 0
                if users_with_items_year_count > 0:
                    items_data[i + 1].append(round(total_hours_year_sum / users_with_items_year_count, 2))
                else:
                    items_data[i + 1].append(round(0, 2))

                max_item_year_user = User.objects.filter(cursodocencia_usuario__fecha_inicio__year=year,
                                                         cursodocencia_usuario__tipo='EXTRACURRICULAR').annotate(
                    Sum('cursodocencia_usuario__total_horas')).filter((
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).aggregate(
                    Max('cursodocencia_usuario__total_horas__sum'))[
                    'cursodocencia_usuario__total_horas__sum__max']
                if max_item_year_user == None:
                    max_item_year_user = 0
                items_data[i + 1].append(max_item_year_user)

                min_item_year_user = User.objects.filter(cursodocencia_usuario__fecha_inicio__year=year,
                                                         cursodocencia_usuario__tipo='EXTRACURRICULAR').annotate(
                    Sum('cursodocencia_usuario__total_horas')).filter((
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).aggregate(
                    Min('cursodocencia_usuario__total_horas__sum'))[
                    'cursodocencia_usuario__total_horas__sum__min']
                if not min_item_year_user:
                    min_item_year_user = 0
                items_data[i + 1].append(min_item_year_user)
                items_data[i + 1].append(users_with_items_year_count)

            data_source = SimpleDataSource(data=items_data)
            hchart_cursodocencia_extracurricular = LineChart(data_source)
            context['hchart_cursodocencia_extracurricular'] = hchart_cursodocencia_extracurricular

            items_data = [
                ['Año', 'Total desarrollos tecnológicos', 'Promedio por persona', 'Max por persona', 'Min por persona', 'Personas activas']]
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
                ['Año', 'Total distinciones', 'Promedio por persona', 'Max por persona', 'Min por persona', 'Personas activas']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = DistincionAcademico.objects.filter(fecha__year=year).filter(
                    ((Q(condecorados__ingreso_entidad__year__lte=year) & Q(
                        condecorados__egreso_entidad__year__gt=year)) |
                     (Q(condecorados__ingreso_entidad__year__lte=year) & Q(condecorados__egreso_entidad=None)))).count()

                request_user_items_year_sum = DistincionAcademico.objects.filter(fecha__year=year,
                                                                                 condecorados=request.user).count()
                if not total_items_year_sum:
                    total_items_year_sum = 0
                items_data[i + 1].append(total_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(distincion_academico_condecorados__fecha__year=year) &
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
                    Q(distincion_academico_condecorados__fecha__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('distincion_academico_condecorados')).aggregate(
                    Max('distincion_academico_condecorados__count'))[
                    'distincion_academico_condecorados__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(max_items_year_user)
                items_data[i + 1].append(users_with_items_year_count)

                min_items_year_user = User.objects.filter(
                    Q(distincion_academico_condecorados__fecha__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('distincion_academico_condecorados')).aggregate(
                    Min('distincion_academico_condecorados__count'))[
                    'distincion_academico_condecorados__count__min']
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
                Q(fecha_fin__year=this_year - 2) | Q(fecha_fin__year=this_year - 1)).annotate(Count('pk', distinct=True)).count()

            # concluidos año anterior ingresos ext, internacionales:
            proy_pasty_conc_extint_tmp = ProyectoInvestigacion.objects.filter(
                financiamiento_conacyt__isnull=True, financiamiento_papiit__isnull=True).filter(
                Q(fecha_fin__year=this_year - 2) | Q(fecha_fin__year=this_year - 1))
            proy_pasty_conc_extint = 0
            for i in proy_pasty_conc_extint_tmp:
                print()
                paises = []
                for j in i.financiamientos.all():
                    if j.institucion.pais.nombre not in paises:
                        paises.append(j.institucion.pais.nombre)
                if 'México' in paises and len(paises) > 1 or 'México' not in paises and len(paises) > 0:
                    proy_pasty_conc_extint += 1
                    print(paises)









            # en proceso año anterior conacyt:
            proy_pasty_proc_conacyt = ProyectoInvestigacion.objects.filter(
                financiamiento_conacyt__isnull=False).filter(
                Q(fecha_inicio__year__lt=this_year - 1) & (Q(fecha_fin__year__gt=this_year - 1) | Q(fecha_fin=None))).count()

            # en proceso año anterior papiit:
            proy_pasty_proc_papiit = ProyectoInvestigacion.objects.filter(
                financiamiento_papiit__isnull=False).filter(
                Q(fecha_inicio__year__lt=this_year - 1) & (Q(fecha_fin__year__gt=this_year - 1) | Q(fecha_fin=None))).count()

            # en proceso año anterior ingresos ext, nacionales:
            proy_pasty_proc_extnal = ProyectoInvestigacion.objects.filter(
                financiamiento_conacyt__isnull=True, financiamiento_papiit__isnull=True).filter(
                Q(fecha_inicio__year__lt=this_year - 1) & (Q(fecha_fin__year__gt=this_year - 1) | Q(fecha_fin=None))).filter(
                Q(financiamientos__institucion__pais__nombre='México')).annotate(Count('pk', distinct=True)).count()

            # en proceso año anterior ingresos ext, internacionales:
            proy_pasty_proc_extint_tmp = ProyectoInvestigacion.objects.filter(
                financiamiento_conacyt__isnull=True, financiamiento_papiit__isnull=True).filter(
                Q(fecha_inicio__year__lt=this_year - 1) & (Q(fecha_fin__year__gt=this_year - 1) | Q(fecha_fin=None)))
            proy_pasty_proc_extint = 0
            for i in proy_pasty_proc_extint_tmp:
                print()
                paises = []
                for j in i.financiamientos.all():
                    if j.institucion.pais.nombre not in paises:
                        paises.append(j.institucion.pais.nombre)
                if 'México' in paises and len(paises) > 1 or 'México' not in paises and len(paises) > 0:
                    proy_pasty_proc_extint += 1
                    print(paises)










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
                print()
                paises = []
                for j in i.financiamientos.all():
                    if j.institucion.pais.nombre not in paises:
                        paises.append(j.institucion.pais.nombre)
                if 'México' in paises and len(paises) > 1 or 'México' not in paises and len(paises) > 0:
                    proy_thisy_conc_extint += 1
                    print(paises)






            # en proceso este año conacyt:
            proy_thisy_proc_conacyt = ProyectoInvestigacion.objects.filter(
                financiamiento_conacyt__isnull=False).filter(
                Q(fecha_inicio__year=this_year) & Q(fecha_fin=None)).count()

            # en proceso este año papiit:
            proy_thisy_proc_papiit = ProyectoInvestigacion.objects.filter(
                financiamiento_papiit__isnull=False).filter(
                Q(fecha_inicio__year=this_year) & Q(fecha_fin=None)).count()

            # en proceso este año ingresos ext, nacionales:
            proy_thisy_proc_extnal = ProyectoInvestigacion.objects.filter(
                financiamiento_conacyt__isnull=True, financiamiento_papiit__isnull=True).filter(
                Q(fecha_inicio__year=this_year) & Q(fecha_fin=None)).filter(
                Q(financiamientos__institucion__pais__nombre='México')).annotate(
                Count('pk', distinct=True)).count()

            # en proceso este año ingresos ext, internacionales:
            proy_thisy_proc_extint_tmp = ProyectoInvestigacion.objects.filter(
                financiamiento_conacyt__isnull=True, financiamiento_papiit__isnull=True).filter(
                Q(fecha_inicio__year=this_year) & Q(fecha_fin=None))
            proy_thisy_proc_extint = 0
            for i in proy_thisy_proc_extint_tmp:
                print()
                paises = []
                for j in i.financiamientos.all():
                    if j.institucion.pais.nombre not in paises:
                        paises.append(j.institucion.pais.nombre)
                if 'México' in paises and len(paises) > 1 or 'México' not in paises and len(paises) > 0:
                    proy_thisy_proc_extint += 1
                    print(paises)

            conc_pastyl = 'Concluidos ' + str(this_year - 2) + "-" + str(this_year - 1)
            proc_pastyl = 'En proceso ' + str(this_year - 2) + "-" + str(this_year - 1)
            conc_thisyl = 'Concluidos ' + str(this_year - 1) + "-" + str(this_year)
            proc_thisyl = 'En proceso ' + str(this_year - 1) + "-" + str(this_year)

            proyectos = [['Etiqueta', 'CONACYT',                'PAPIIT',               'Ext. Nacional', 'Ext. Internacional'],
                         [conc_pastyl, proy_pasty_conc_conacyt, proy_pasty_conc_papiit, proy_pasty_conc_extnal, proy_pasty_conc_extint],
                         [proc_pastyl, proy_pasty_proc_conacyt, proy_pasty_proc_papiit, proy_pasty_proc_extnal, proy_pasty_proc_extint],
                         [conc_thisyl, proy_thisy_conc_conacyt, proy_thisy_conc_papiit, proy_thisy_conc_extnal, proy_thisy_conc_extint],
                         [proc_thisyl, proy_thisy_proc_conacyt, proy_thisy_proc_papiit, proy_thisy_proc_extnal, proy_thisy_proc_extint],
                         ]

            data_source = SimpleDataSource(data=proyectos)
            chart_proyectos_investigacion = BarChart(data_source)
            context['chart_proyectos_investigacion'] = chart_proyectos_investigacion




            invest_en_proyectos_ant = User.objects.filter(tipo='INVESTIGADOR').filter(
                (Q(proyecto_investigacion_responsables__fecha_inicio__year=this_year - 2) | Q(
                    proyecto_investigacion_responsables__fecha_inicio__year=this_year - 1)) &
                Q(proyecto_investigacion_responsables__fecha_fin__year__gte=this_year - 2)).filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).count()

            invest_activos_ant = User.objects.filter(tipo='INVESTIGADOR').filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).count()

            invest_perc_ant = round(invest_en_proyectos_ant / invest_activos_ant, 2)

            invest_en_proyectos_act = User.objects.filter(tipo='INVESTIGADOR').filter(
                (Q(proyecto_investigacion_responsables__fecha_inicio__year=this_year - 1) | Q(
                    proyecto_investigacion_responsables__fecha_inicio__year=this_year)) &
                Q(proyecto_investigacion_responsables__fecha_fin__year__gte=this_year - 1)).filter(
                (Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad__year=this_year)) | (
                    Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad=None))).count()

            invest_activos_act = User.objects.filter(tipo='INVESTIGADOR').filter(
                (Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad__year=this_year)) | (
                    Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad=None))).count()

            invest_perc_act = round(invest_en_proyectos_act / invest_activos_act, 2)




            tecnicos_en_proyectos_ant = User.objects.filter(tipo='TECNICO').filter(
                (Q(proyecto_investigacion_responsables__fecha_inicio__year=this_year - 2) | Q(
                    proyecto_investigacion_responsables__fecha_inicio__year=this_year - 1)) &
                Q(proyecto_investigacion_responsables__fecha_fin__year__gte=this_year - 2)).filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).count()

            tecnicos_activos_ant = User.objects.filter(tipo='TECNICO').filter(
                (Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad__year__gte=this_year - 1)) | (
                    Q(ingreso_entidad__year__lte=this_year - 2) & Q(egreso_entidad=None))).count()

            tec_perc_ant = round(tecnicos_en_proyectos_ant / tecnicos_activos_ant, 2) * 100

            tecnicos_en_proyectos_act = User.objects.filter(tipo='TECNICO').filter(
                (Q(proyecto_investigacion_responsables__fecha_inicio__year=this_year - 1) | Q(
                    proyecto_investigacion_responsables__fecha_inicio__year=this_year)) &
                (Q(proyecto_investigacion_responsables__fecha_fin__year__gte=this_year - 1) |
                 Q(proyecto_investigacion_responsables__fecha_fin=None))).filter(
                    (Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad__year=this_year)) | (
                        Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad=None))).count()

            tecnicos_activos_act = User.objects.filter(tipo='TECNICO').filter(
                (Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad__year=this_year)) | (
                    Q(ingreso_entidad__year__lte=this_year - 1) & Q(egreso_entidad=None))).count()

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

            context['table_proyectos'] = {'invest_perc_ant': invest_perc_ant, 'invest_perc_act': invest_perc_act,
                                          'tec_perc_ant': tec_perc_ant, 'tec_perc_act': tec_perc_act,
                                          'proy_financiados_ant': proy_financiados_ant, 'proy_ant_perc': proy_ant_perc,
                                          'proy_financiados_act': proy_financiados_act, 'proy_act_perc': proy_act_perc,}







        return render(request, self.template_name, context)

