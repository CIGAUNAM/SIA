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
            #years_curso_especializacion = SIAYearModelCounter.objects.filter(model='CursoEspecializacion')
            #years_curso_especializacion = years_curso_especializacion[years_curso_especializacion.count() - 11:]

            num_years = 10
            last_x_years = []
            for i in range(datetime.now().year - num_years + 1, datetime.now().year + 1):
                last_x_years.append(i)

            active_users_per_last_x_year = []
            for i in range(datetime.now().year - num_years + 1, datetime.now().year + 1):
                u = User.objects.filter((Q(ingreso_entidad__year__lte=last_x_years[i]) & Q(egreso_entidad__year__gt=last_x_years[i])) |
                                        (Q(ingreso_entidad__year__lte=last_x_years[i]) & Q(egreso_entidad=None)))
                active_users_per_last_x_year.append(u.count())


            years_cursos_especializacion_dates = CursoEspecializacion.objects.dates('fecha_inicio', 'year', order='DESC')
            years_cursos_especializacion = []

            for i in reversed(years_cursos_especializacion_dates[:num_years]):
                years_cursos_especializacion.append(str(i.year))

            """
            for i in reversed(years_cursos_especializacion[:10]):
                c = CursoEspecializacion.objects.filter(fecha_inicio__year=i.year).aggregate(Sum('horas'))['horas__sum']
                print(i.year)  # Año
                obj['curso_especializacion'][str(i.year) + '__horas_sum'] = c
                print(c)
                u = User.objects.filter(cursos_especializacion__fecha_inicio__year=i.year).annotate(
                    Count('pk', distinct=True)).count()  # cantidad de usuarios que tienen al menos un curso, por año.
                obj['curso_especializacion'][str(i.year) + '__usuarios_sum'] = u
                print(u)
                if u > 0:
                    print(round(c / u, 2))
                    obj['curso_especializacion'][str(i.year) + '__horas_prom'] = round(c / u, 2)
                    h = None
                else:
                    obj['curso_especializacion'][str(i.year) + '__horas_prom'] = 0
                h = User.objects.filter(cursos_especializacion__fecha_inicio__year=i.year,
                                        cursos_especializacion__usuario=request.user).aggregate(
                    Sum('cursos_especializacion__horas'))['cursos_especializacion__horas__sum']  # horas del usuario en el año actual
                if not h:
                    h = 0
                print(h)
                obj['curso_especializacion'][str(i.year) + '__horas_usuario'] = h
                hM = User.objects.filter(cursos_especializacion__fecha_inicio__year=i.year).annotate(
                    Sum('cursos_especializacion__horas')).aggregate(Max('cursos_especializacion__horas__sum'))[
                    'cursos_especializacion__horas__sum__max']  # maximo de horas de un solo usuario
                print(hM)
                obj['curso_especializacion'][str(i.year) + '__horas_max'] = hM
                hm = User.objects.filter(cursos_especializacion__fecha_inicio__year=i.year).annotate(
                    Sum('cursos_especializacion__horas')).aggregate(Min('cursos_especializacion__horas__sum'))[
                    'cursos_especializacion__horas__sum__min']  # minimo
                print(hm)
                obj['curso_especializacion'][str(i.year) + '__horas_min'] = hm
            """

            #cursos_data = [['Año', 'Personas', 'Total horas', 'Mis horas', 'Promedio Horas', 'Max horas', 'Min horas']]
            cursos_data = [['Año', 'Mis horas', 'Promedio horas', 'Max horas', 'Min horas']]

            for i in range(num_years):
                year = years_cursos_especializacion[i]
                cursos_data.append([years_cursos_especializacion[i]])
                u = User.objects.filter(cursos_especializacion__fecha_inicio__year=year).annotate(
                    Count('pk', distinct=True)).count()
                #cursos_data[i + 1].append(u)
                th = CursoEspecializacion.objects.filter(fecha_inicio__year=year).aggregate(Sum('horas'))['horas__sum']
                #cursos_data[i + 1].append(th)
                hu = User.objects.filter(cursos_especializacion__fecha_inicio__year=year,
                                         cursos_especializacion__usuario=request.user).aggregate(
                    Sum('cursos_especializacion__horas'))['cursos_especializacion__horas__sum']
                if not hu:
                    hu = 0
                cursos_data[i + 1].append(hu)
                cursos_data[i + 1].append(round(th / u, 2))
                Mh = User.objects.filter(cursos_especializacion__fecha_inicio__year=year).annotate(
                    Sum('cursos_especializacion__horas')).aggregate(Max('cursos_especializacion__horas__sum'))[
                    'cursos_especializacion__horas__sum__max']
                cursos_data[i + 1].append(Mh)
                mh = User.objects.filter(cursos_especializacion__fecha_inicio__year=year).annotate(
                    Sum('cursos_especializacion__horas')).aggregate(Min('cursos_especializacion__horas__sum'))[
                    'cursos_especializacion__horas__sum__min']
                cursos_data[i + 1].append(mh)

            # obj['curso_especializacion'] = cursos_data
            data_source = SimpleDataSource(data=cursos_data)
            chart_cursos_especializacion = LineChart(data_source)
            context['chart_cursos_especializacion'] = chart_cursos_especializacion


            articulos_investigacion_data = [['Año', 'Total artículos', 'Mis artículos', 'Promedio artículos', 'Max artículos', 'Min artículos']]
            for i in range(num_years):
                year = last_x_years[i]
                articulos_investigacion_data.append([str(year)])
                u = User.objects.filter(articulo_cientifico_autores__fecha__year=year).annotate(
                    Count('pk', distinct=True)).count() # usuarios con articulo en el año
                if u == None:
                    u = 0

                ta = ArticuloCientifico.objects.filter(fecha__year=year).count()
                articulos_investigacion_data[i + 1].append(ta)  # numero de articulos en el año de todos los usuarios
                ma = ArticuloCientifico.objects.filter(fecha__year=year, usuarios=request.user).count()
                articulos_investigacion_data[i + 1].append(ma)  # numero de articulos del usuario
                cursos_data[i + 1].append(round(th / u, 2))



        print(articulos_investigacion_data)
        data_source = SimpleDataSource(data=articulos_investigacion_data)
        chart_articulos_investigacion = LineChart(data_source)
        context['chart_articulos_investigacion'] = chart_articulos_investigacion


        return render(request, self.template_name, context)



