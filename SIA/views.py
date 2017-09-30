from django.http.response import Http404, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy

from django.core import serializers

from formacion_academica.models import CursoEspecializacion
from investigacion.models import ArticuloCientifico

from nucleo.models import User
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
                users_with_articles_year_count = User.objects.filter((Q(ingreso_entidad__year__lte=i) & Q(egreso_entidad__year__gt=i)) |
                                        (Q(ingreso_entidad__year__lte=i) & Q(egreso_entidad=None)))
                active_users_per_last_x_year.append(users_with_articles_year_count.count())

            #years_cursos_especializacion_dates = CursoEspecializacion.objects.dates('fecha_inicio', 'year', order='DESC')
            #years_cursos_especializacion = []

            #for i in reversed(years_cursos_especializacion_dates[:num_years]):
            #    years_cursos_especializacion.append(str(i.year))

            #cursos_data = [['Año', 'Personas', 'Total horas', 'Mis horas', 'Promedio Horas', 'Max horas', 'Min horas']]


            cursos_data = [['Año', 'Mis horas', 'Promedio horas', 'Max horas', 'Min horas']]

            for i in range(num_years):
                year = last_x_years[i]
                cursos_data.append([str(last_x_years[i])])

                users_with_articles_year_count = User.objects.filter(
                    Q(cursos_especializacion__fecha_inicio__year=year) &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
                if users_with_articles_year_count == None:
                    users_with_articles_year_count = 0

                total_course_hours_year_sum = CursoEspecializacion.objects.filter(fecha_inicio__year=year).filter((
                    (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) |
                    (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).aggregate(Sum('horas'))['horas__sum']
                if     total_course_hours_year_sum == None:
                        total_course_hours_year_sum = 0

                request_user_course_hours_year_sum = User.objects.filter(cursos_especializacion__fecha_inicio__year=year,
                    cursos_especializacion__usuario=request.user).aggregate(
                    Sum('cursos_especializacion__horas'))['cursos_especializacion__horas__sum']
                if not request_user_course_hours_year_sum:
                    request_user_course_hours_year_sum = 0
                cursos_data[i + 1].append(request_user_course_hours_year_sum)

                if users_with_articles_year_count == None:
                    users_with_articles_year_count = 0
                if users_with_articles_year_count > 0:
                    cursos_data[i + 1].append(round(total_course_hours_year_sum / users_with_articles_year_count, 2))
                else:
                    cursos_data[i + 1].append(round(0, 2))

                max_hours_year_user = User.objects.filter(cursos_especializacion__fecha_inicio__year=year).annotate(
                    Sum('cursos_especializacion__horas')).filter((
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                    (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).aggregate(Max('cursos_especializacion__horas__sum'))[
                    'cursos_especializacion__horas__sum__max']
                if max_hours_year_user == None:
                    max_hours_year_user = 0
                cursos_data[i + 1].append(max_hours_year_user)

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


            articulos_investigacion_data = [['Año', 'Total artículos', 'Mis artículos', 'Promedio artículos', 'Max artículos', 'Min artículos']]
            for i in range(num_years):
                year = last_x_years[i]
                articulos_investigacion_data.append([str(year)])

                u = ArticuloCientifico.objects.filter(fecha__year=year).count()
                articulos_investigacion_data[i + 1].append(u)

                users_with_articles_year_count = User.objects.filter(
                    Q(articulo_cientifico_autores__fecha__year=year, articulo_cientifico_autores__status='PUBLICADO') &
                    ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
                     (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
                    Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año

                if users_with_articles_year_count == None:
                    users_with_articles_year_count = 0

                ta = ArticuloCientifico.objects.filter(fecha__year=year).count()
                articulos_investigacion_data[i + 1].append(
                    users_with_articles_year_count)  # numero de articulos en el año de todos los usuarios
                ma = ArticuloCientifico.objects.filter(fecha__year=year, usuarios=request.user).count()
                articulos_investigacion_data[i + 1].append(ma)  # numero de articulos del usuario
                articulos_investigacion_data[i + 1].append(round(0, 2))



        print(articulos_investigacion_data)
        data_source = SimpleDataSource(data=articulos_investigacion_data)
        chart_articulos_investigacion = LineChart(data_source)
        context['chart_articulos_investigacion'] = chart_articulos_investigacion


        return render(request, self.template_name, context)



