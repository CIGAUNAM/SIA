from django.http.response import Http404, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy

from django.core import serializers

from formacion_academica.models import CursoEspecializacion
from investigacion.models import ArticuloCientifico, CapituloLibroInvestigacion, MapaArbitrado, InformeTecnico
from difusion_cientifica.models import MemoriaInExtenso


from nucleo.models import User, Libro
from datetime import datetime
from django.db.models import Q, Max, Min, Count, Sum


from sia_stats.models import SIAYearModelCounter


from graphos.sources.simple import SimpleDataSource, BaseDataSource
from graphos.renderers.morris import LineChart, AreaChart
#from graphos.renderers.highcharts import LineChart


# Create your views here.




class Dashboard(View):
    form_class = None
    template_name = 'dashboard.html'
    aux = {}
    now = datetime.now()
    this_year = now.year
    ten_years_ago = now.year - 10

    def get(self, request):
        # obj = get_object_or_404(User, username__iexact=request.user)
        obj = range(self.ten_years_ago, self.this_year)

        years_curso_especializacion = SIAYearModelCounter.objects.filter(model='CursoEspecializacion')

        obj = {}
        context = {}

        if request.user.is_authenticated:
            num_years = 10
            last_x_years = []
            active_users_per_last_x_year = []

            for i in range(datetime.now().year - num_years + 1, datetime.now().year + 1):
                last_x_years.append(i)

            for i in last_x_years:
                users_with_cursos_especializacion_year_count = User.objects.filter((Q(ingreso_entidad__year__lte=i) & Q(egreso_entidad__year__gt=i)) |
                                        (Q(ingreso_entidad__year__lte=i) & Q(egreso_entidad=None)))
                active_users_per_last_x_year.append(users_with_cursos_especializacion_year_count.count())

            #years_cursos_especializacion_dates = CursoEspecializacion.objects.dates('fecha_inicio', 'year', order='DESC')
            #years_cursos_especializacion = []

            #for i in reversed(years_cursos_especializacion_dates[:num_years]):
            #    years_cursos_especializacion.append(str(i.year))

            #cursos_data = [['Año', 'Personas', 'Total horas', 'Mis horas', 'Promedio Horas', 'Max horas', 'Min horas']]


            cursos_data = [['Año', 'Mis horas', 'Promedio horas', 'Max horas', 'Min horas']]

            for i in range(num_years):
                year = last_x_years[i]
                cursos_data.append([str(last_x_years[i])])

                users_with_cursos_especializacion_year_count = User.objects.filter(
                    Q(cursos_especializacion__fecha_inicio__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_cursos_especializacion_year_count == None:
                    users_with_cursos_especializacion_year_count = 0

                total_course_hours_year_sum = CursoEspecializacion.objects.filter(fecha_inicio__year=year).filter((
                    (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) |
                    (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).aggregate(Sum('horas'))['horas__sum']
                if     total_course_hours_year_sum == None:
                        total_course_hours_year_sum = 0

                request_user_articulo_cientifico_enprensa_year_sum = User.objects.filter(cursos_especializacion__fecha_inicio__year=year,
                    cursos_especializacion__usuario=request.user).aggregate(
                    Sum('cursos_especializacion__horas'))['cursos_especializacion__horas__sum']
                if not request_user_articulo_cientifico_enprensa_year_sum:
                    request_user_articulo_cientifico_enprensa_year_sum = 0
                cursos_data[i + 1].append(request_user_articulo_cientifico_enprensa_year_sum)

                if users_with_cursos_especializacion_year_count == None:
                    users_with_cursos_especializacion_year_count = 0
                if users_with_cursos_especializacion_year_count > 0:
                    cursos_data[i + 1].append(round(total_course_hours_year_sum / users_with_cursos_especializacion_year_count, 2))
                else:
                    cursos_data[i + 1].append(round(0, 2))

                max_cursos_especializacion_year_user = User.objects.filter(cursos_especializacion__fecha_inicio__year=year).annotate(
                    Sum('cursos_especializacion__horas')).filter((
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).aggregate(Max('cursos_especializacion__horas__sum'))[
                    'cursos_especializacion__horas__sum__max']
                if max_cursos_especializacion_year_user == None:
                    max_cursos_especializacion_year_user = 0
                cursos_data[i + 1].append(max_cursos_especializacion_year_user)

                min_hours_year_user = User.objects.filter(cursos_especializacion__fecha_inicio__year=year).annotate(
                    Sum('cursos_especializacion__horas')).filter((
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).aggregate(Min('cursos_especializacion__horas__sum'))[
                    'cursos_especializacion__horas__sum__min']
                if not min_hours_year_user:
                    min_hours_year_user = 0
                cursos_data[i + 1].append(min_hours_year_user)

            data_source = SimpleDataSource(data=cursos_data)
            chart_cursos_especializacion = LineChart(data_source)
            context['chart_cursos_especializacion'] = chart_cursos_especializacion


            articulos_investigacion_publicados_data = [['Año', 'Mis artículos', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                articulos_investigacion_publicados_data.append([str(year)])

                total_articulos_cientificos_enprensa_year_sum = ArticuloCientifico.objects.filter(fecha__year=year,
                                                                                                  status='PUBLICADO').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                    Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()

                request_user_articulo_cientifico_enprensa_year_sum = ArticuloCientifico.objects.filter(fecha__year=year,
                                                                                              status='PUBLICADO',
                                                                                              usuarios=request.user).count()
                if not request_user_articulo_cientifico_enprensa_year_sum:
                    request_user_articulo_cientifico_enprensa_year_sum = 0
                articulos_investigacion_publicados_data[i + 1].append(request_user_articulo_cientifico_enprensa_year_sum)

                users_with_cursos_especializacion_year_count = User.objects.filter(
                    Q(articulo_cientifico_autores__fecha__year=year, articulo_cientifico_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_cursos_especializacion_year_count == None:
                    users_with_cursos_especializacion_year_count = 0

                if users_with_cursos_especializacion_year_count > 0:
                    articulos_investigacion_publicados_data[i + 1].append(
                        round(total_articulos_cientificos_enprensa_year_sum / users_with_cursos_especializacion_year_count, 2))
                else:
                    articulos_investigacion_publicados_data[i + 1].append(0)

                max_cursos_especializacion_year_user = User.objects.filter(
                    Q(articulo_cientifico_autores__fecha__year=year, articulo_cientifico_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('articulo_cientifico_autores')).aggregate(Max('articulo_cientifico_autores__count'))[
                    'articulo_cientifico_autores__count__max']
                if max_cursos_especializacion_year_user == None:
                    max_cursos_especializacion_year_user = 0
                articulos_investigacion_publicados_data[i + 1].append(max_cursos_especializacion_year_user)

                min_articulo_cientifico_year_user = User.objects.filter(
                    Q(articulo_cientifico_autores__fecha__year=year, articulo_cientifico_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('articulo_cientifico_autores')).aggregate(Min('articulo_cientifico_autores__count'))[
                    'articulo_cientifico_autores__count__min']
                if min_articulo_cientifico_year_user == None:
                    min_articulo_cientifico_year_user = 0
                articulos_investigacion_publicados_data[i + 1].append(min_articulo_cientifico_year_user)

            print(articulos_investigacion_publicados_data)
            data_source = SimpleDataSource(data=articulos_investigacion_publicados_data)
            chart_articulos_investigacion_publicados = LineChart(data_source)
            context['chart_articulos_investigacion_publicados'] = chart_articulos_investigacion_publicados

            articulos_investigacion_enprensa_data = [
                ['Año', 'Mis artículos', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                articulos_investigacion_enprensa_data.append([str(year)])

                total_articulos_cientificos_enprensa_year_sum = ArticuloCientifico.objects.filter(fecha__year=year,
                                                                                                  status='EN_PRENSA').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                    Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()

                request_user_articulo_cientifico_enprensa_year_sum = ArticuloCientifico.objects.filter(fecha__year=year,
                                                                                              status='EN_PRENSA',
                                                                                              usuarios=request.user).count()
                if not request_user_articulo_cientifico_enprensa_year_sum:
                    request_user_articulo_cientifico_enprensa_year_sum = 0
                articulos_investigacion_enprensa_data[i + 1].append(request_user_articulo_cientifico_enprensa_year_sum)

                users_with_cursos_especializacion_year_count = User.objects.filter(
                    Q(articulo_cientifico_autores__fecha__year=year, articulo_cientifico_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_cursos_especializacion_year_count == None:
                    users_with_cursos_especializacion_year_count = 0
                if users_with_cursos_especializacion_year_count > 0:
                    articulos_investigacion_enprensa_data[i + 1].append(
                        round(total_articulos_cientificos_enprensa_year_sum / users_with_cursos_especializacion_year_count, 2))
                else:
                    articulos_investigacion_enprensa_data[i + 1].append(0)

                max_cursos_especializacion_year_user = User.objects.filter(
                    Q(articulo_cientifico_autores__fecha__year=year, articulo_cientifico_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('articulo_cientifico_autores')).aggregate(Max('articulo_cientifico_autores__count'))[
                    'articulo_cientifico_autores__count__max']
                if max_cursos_especializacion_year_user == None:
                    max_cursos_especializacion_year_user = 0
                articulos_investigacion_enprensa_data[i + 1].append(max_cursos_especializacion_year_user)

                min_articulo_cientifico_year_user = User.objects.filter(
                    Q(articulo_cientifico_autores__fecha__year=year, articulo_cientifico_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('articulo_cientifico_autores')).aggregate(Min('articulo_cientifico_autores__count'))[
                    'articulo_cientifico_autores__count__min']
                if min_articulo_cientifico_year_user == None:
                    min_articulo_cientifico_year_user = 0
                articulos_investigacion_enprensa_data[i + 1].append(min_articulo_cientifico_year_user)

            print(articulos_investigacion_enprensa_data)
            data_source = SimpleDataSource(data=articulos_investigacion_enprensa_data)
            chart_articulos_investigacion_enprensa = LineChart(data_source)
            context['chart_articulos_investigacion_enprensa'] = chart_articulos_investigacion_enprensa

            articulos_investigacion_aceptado_data = [
                ['Año', 'Mis artículos', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                articulos_investigacion_aceptado_data.append([str(year)])

                total_articulos_cientificos_year_sum = ArticuloCientifico.objects.filter(fecha__year=year,
                                                                                         status='ACEPTADO').count()
                request_user_articulo_cientifico_year_sum = ArticuloCientifico.objects.filter(fecha__year=year,
                                                                                              status='ACEPTADO',
                                                                                              usuarios=request.user).count()
                if not request_user_articulo_cientifico_year_sum:
                    request_user_articulo_cientifico_year_sum = 0
                articulos_investigacion_aceptado_data[i + 1].append(request_user_articulo_cientifico_year_sum)

                users_with_cursos_especializacion_year_count = User.objects.filter(
                    Q(articulo_cientifico_autores__fecha__year=year, articulo_cientifico_autores__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_cursos_especializacion_year_count == None:
                    users_with_cursos_especializacion_year_count = 0
                if users_with_cursos_especializacion_year_count > 0:
                    articulos_investigacion_aceptado_data[i + 1].append(
                        round(total_articulos_cientificos_year_sum / users_with_cursos_especializacion_year_count, 2))
                else:
                    articulos_investigacion_aceptado_data[i + 1].append(0)

                max_cursos_especializacion_year_user = User.objects.filter(
                    Q(articulo_cientifico_autores__fecha__year=year, articulo_cientifico_autores__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('articulo_cientifico_autores')).aggregate(Max('articulo_cientifico_autores__count'))[
                    'articulo_cientifico_autores__count__max']
                if max_cursos_especializacion_year_user == None:
                    max_cursos_especializacion_year_user = 0
                articulos_investigacion_aceptado_data[i + 1].append(max_cursos_especializacion_year_user)

                min_articulo_cientifico_year_user = User.objects.filter(
                    Q(articulo_cientifico_autores__fecha__year=year, articulo_cientifico_autores__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('articulo_cientifico_autores')).aggregate(Min('articulo_cientifico_autores__count'))[
                    'articulo_cientifico_autores__count__min']
                if min_articulo_cientifico_year_user == None:
                    min_articulo_cientifico_year_user = 0
                articulos_investigacion_aceptado_data[i + 1].append(min_articulo_cientifico_year_user)

            print(articulos_investigacion_aceptado_data)
            data_source = SimpleDataSource(data=articulos_investigacion_aceptado_data)
            chart_articulos_investigacion_aceptado = LineChart(data_source)
            context['chart_articulos_investigacion_aceptado'] = chart_articulos_investigacion_aceptado






            libros_investigacion_publicado_data = [
                ['Año', 'Mis Libros', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                libros_investigacion_publicado_data.append([str(year)])

                total_libros_cientificos_year_sum = Libro.objects.filter(fecha__year=year, tipo='INVESTIGACION',
                                                                         es_libro_completo=True,
                                                                         status='PUBLICADO').count()
                request_user_libro_investigacion_year_sum = Libro.objects.filter(fecha__year=year, tipo='INVESTIGACION',
                                                                                 es_libro_completo=True,
                                                                                 status='PUBLICADO',
                                                                                 usuarios=request.user).count()
                if not request_user_libro_investigacion_year_sum:
                    request_user_libro_investigacion_year_sum = 0
                libros_investigacion_publicado_data[i + 1].append(request_user_libro_investigacion_year_sum)

                users_with_cursos_especializacion_year_count = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='INVESTIGACION',
                      libro_autores__es_libro_completo=True, libro_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_cursos_especializacion_year_count == None:
                    users_with_cursos_especializacion_year_count = 0
                if users_with_cursos_especializacion_year_count > 0:
                    libros_investigacion_publicado_data[i + 1].append(
                        round(total_libros_cientificos_year_sum / users_with_cursos_especializacion_year_count, 2))
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

            print(libros_investigacion_publicado_data)
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
                                                                         status='EN_PRENSA').count()
                request_user_libro_investigacion_year_sum = Libro.objects.filter(fecha__year=year, tipo='INVESTIGACION',
                                                                                 es_libro_completo=True,
                                                                                 status='EN_PRENSA',
                                                                                 usuarios=request.user).count()
                if not request_user_libro_investigacion_year_sum:
                    request_user_libro_investigacion_year_sum = 0
                libros_investigacion_enprensa_data[i + 1].append(request_user_libro_investigacion_year_sum)

                users_with_cursos_especializacion_year_count = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='INVESTIGACION',
                      libro_autores__es_libro_completo=True, libro_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_cursos_especializacion_year_count == None:
                    users_with_cursos_especializacion_year_count = 0
                if users_with_cursos_especializacion_year_count > 0:
                    libros_investigacion_enprensa_data[i + 1].append(
                        round(total_libros_cientificos_year_sum / users_with_cursos_especializacion_year_count, 2))
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

            print(libros_investigacion_enprensa_data)
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
                                                                         status='ACEPTADO').count()
                request_user_libro_investigacion_year_sum = Libro.objects.filter(fecha__year=year, tipo='INVESTIGACION',
                                                                                 es_libro_completo=True,
                                                                                 status='ACEPTADO',
                                                                                 usuarios=request.user).count()
                if not request_user_libro_investigacion_year_sum:
                    request_user_libro_investigacion_year_sum = 0
                libros_investigacion_aceptado_data[i + 1].append(request_user_libro_investigacion_year_sum)

                users_with_cursos_especializacion_year_count = User.objects.filter(
                    Q(libro_autores__fecha__year=year, libro_autores__tipo='INVESTIGACION',
                      libro_autores__es_libro_completo=True, libro_autores__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_cursos_especializacion_year_count == None:
                    users_with_cursos_especializacion_year_count = 0
                if users_with_cursos_especializacion_year_count > 0:
                    libros_investigacion_aceptado_data[i + 1].append(
                        round(total_libros_cientificos_year_sum / users_with_cursos_especializacion_year_count, 2))
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

            print(libros_investigacion_aceptado_data)
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
                    libro__es_libro_completo=False, libro__status='PUBLICADO').count()

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

            print(capitulos_libros_investigacion_publicado_data)
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
                    libro__es_libro_completo=False, libro__status='EN_PRENSA').count()

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

            print(capitulos_libros_investigacion_enprensa_data)
            data_source = SimpleDataSource(data=capitulos_libros_investigacion_enprensa_data)
            chart_capitulos_libros_investigacion = LineChart(data_source)
            context['chart_capitulos_libros_investigacion_enprensa'] = chart_capitulos_libros_investigacion



            capitulos_libros_investigacion_aceptado_data = [
                ['Año', 'Mis Capitulos en libros', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                capitulos_libros_investigacion_aceptado_data.append([str(year)])

                total_capitulos_libros_investigacion_year_sum = CapituloLibroInvestigacion.objects.filter(
                    libro__fecha__year=year, libro__tipo='INVESTIGACION',
                    libro__es_libro_completo=False, libro__status='ACEPTADO').count()

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

            print(capitulos_libros_investigacion_aceptado_data)
            data_source = SimpleDataSource(data=capitulos_libros_investigacion_aceptado_data)
            chart_capitulos_libros_investigacion = LineChart(data_source)
            context['chart_capitulos_libros_investigacion_aceptado'] = chart_capitulos_libros_investigacion

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

            print(items_data)
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

            print(items_data)
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

            print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_mapas_arbitrados_aceptados = LineChart(data_source)
            context['chart_mapas_arbitrados_aceptados'] = chart_mapas_arbitrados_aceptados

            items_data = [
                ['Año', 'Mis Informes Técnicos', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = InformeTecnico.objects.filter(fecha__year=year,
                                                                     status='PUBLICADO').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                        Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()

                request_user_items_year_sum = InformeTecnico.objects.filter(fecha__year=year,
                                                                            status='PUBLICADO',
                                                                            usuarios=request.user).count()
                if not request_user_items_year_sum:
                    request_user_items_year_sum = 0
                items_data[i + 1].append(request_user_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(informe_tecnico_autores__fecha__year=year, informe_tecnico_autores__status='PUBLICADO') &
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
                    Q(informe_tecnico_autores__fecha__year=year, informe_tecnico_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('informe_tecnico_autores')).aggregate(Max('informe_tecnico_autores__count'))[
                    'informe_tecnico_autores__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(informe_tecnico_autores__fecha__year=year, informe_tecnico_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('informe_tecnico_autores')).aggregate(Min('informe_tecnico_autores__count'))[
                    'informe_tecnico_autores__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(min_items_year_user)

            print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_informes_tecnicos_publicados = LineChart(data_source)
            context['chart_informes_tecnicos_publicados'] = chart_informes_tecnicos_publicados

            items_data = [
                ['Año', 'Mis Informes Técnicos', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = InformeTecnico.objects.filter(fecha__year=year,
                                                                     status='EN_PRENSA').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                        Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()

                request_user_items_year_sum = InformeTecnico.objects.filter(fecha__year=year,
                                                                            status='EN_PRENSA',
                                                                            usuarios=request.user).count()
                if not request_user_items_year_sum:
                    request_user_items_year_sum = 0
                items_data[i + 1].append(request_user_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(informe_tecnico_autores__fecha__year=year, informe_tecnico_autores__status='EN_PRENSA') &
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
                    Q(informe_tecnico_autores__fecha__year=year, informe_tecnico_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('informe_tecnico_autores')).aggregate(Max('informe_tecnico_autores__count'))[
                    'informe_tecnico_autores__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(informe_tecnico_autores__fecha__year=year, informe_tecnico_autores__status='EN_PRENSA') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('informe_tecnico_autores')).aggregate(Min('informe_tecnico_autores__count'))[
                    'informe_tecnico_autores__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(min_items_year_user)

            print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_informes_tecnicos_enprensa = LineChart(data_source)
            context['chart_informes_tecnicos_enprensa'] = chart_informes_tecnicos_enprensa

            items_data = [
                ['Año', 'Mis Informes Técnicos', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = InformeTecnico.objects.filter(fecha__year=year,
                                                                     status='ACEPTADO').filter(
                    ((Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year)) | (
                        Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None)))).count()

                request_user_items_year_sum = InformeTecnico.objects.filter(fecha__year=year,
                                                                            status='ACEPTADO',
                                                                            usuarios=request.user).count()
                if not request_user_items_year_sum:
                    request_user_items_year_sum = 0
                items_data[i + 1].append(request_user_items_year_sum)

                users_with_items_year_count = User.objects.filter(
                    Q(informe_tecnico_autores__fecha__year=year, informe_tecnico_autores__status='ACEPTADO') &
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
                    Q(informe_tecnico_autores__fecha__year=year, informe_tecnico_autores__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('informe_tecnico_autores')).aggregate(Max('informe_tecnico_autores__count'))[
                    'informe_tecnico_autores__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(max_items_year_user)

                min_items_year_user = User.objects.filter(
                    Q(informe_tecnico_autores__fecha__year=year, informe_tecnico_autores__status='ACEPTADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('informe_tecnico_autores')).aggregate(Min('informe_tecnico_autores__count'))[
                    'informe_tecnico_autores__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(min_items_year_user)

            print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_informes_tecnicos_aceptados = LineChart(data_source)
            context['chart_informes_tecnicos_aceptados'] = chart_informes_tecnicos_aceptados

            items_data = [
                ['Año', 'Mis Proyectos de investigación', 'Promedio por persona', 'Max por persona', 'Min por persona']]
            for i in range(num_years):
                year = last_x_years[i]
                items_data.append([str(year)])

                total_items_year_sum = Proyecto.objects.filter(tipo='INVESTIGACION').filter(
                    (Q(fecha_inicio__year__lte=year) & Q(fecha_fin__year__gt=year))
                    | (Q(fecha_inicio__year__lte=year) & Q(fecha_fin=None))).filter(
                    (Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad__year__gt=year))
                    | (Q(usuarios__ingreso_entidad__year__lte=year) & Q(usuarios__egreso_entidad=None))).count()

                request_user_items_year_sum = Proyecto.objects.filter(tipo='INVESTIGACION',
                                                                      usuarios=request.user).filter(
                    (Q(fecha_inicio__year__lte=year) & Q(fecha_fin__year__gt=year))
                    | (Q(fecha_inicio__year__lte=year) & Q(fecha_fin=None))).count()
                if not request_user_items_year_sum:
                    request_user_items_year_sum = 0
                items_data[i + 1].append(request_user_items_year_sum)

                users_with_items_year_count = User.objects.filter(proyecto_responsables__tipo='INVESTIGACION').filter(
                    (Q(fecha_inicio__year__lte=year) & Q(fecha_fin__year__gt=year))
                    | (Q(fecha_inicio__year__lte=year) & Q(fecha_fin=None))).filter(
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

                max_items_year_user = User.objects.filter(proyecto_responsables__tipo='INVESTIGACION').filter(
                    (Q(fecha_inicio__year__lte=year) & Q(fecha_fin__year__gt=year))
                    | (Q(fecha_inicio__year__lte=year) & Q(fecha_fin=None))
                ).filter(((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                          (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('proyecto_responsables')).aggregate(Max('proyecto_responsables__count'))[
                    'proyecto_responsables__count__max']
                if max_items_year_user == None:
                    max_items_year_user = 0
                items_data[i + 1].append(max_items_year_user)

                min_items_year_user = User.objects.filter(proyecto_responsables__tipo='INVESTIGACION').filter(
                    (Q(fecha_inicio__year__lte=year) & Q(fecha_fin__year__gt=year))
                    | (Q(fecha_inicio__year__lte=year) & Q(fecha_fin=None))
                ).filter(((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                          (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('proyecto_responsables')).aggregate(Min('proyecto_responsables__count'))[
                    'proyecto_responsables__count__min']
                if min_items_year_user == None:
                    min_items_year_user = 0
                items_data[i + 1].append(min_items_year_user)

            print(items_data)
            data_source = SimpleDataSource(data=items_data)
            chart_proyectos_investigacion = LineChart(data_source)
            context['chart_proyectos_investigacion'] = chart_proyectos_investigacion







        return render(request, self.template_name, context)



