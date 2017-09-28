from django.http.response import Http404, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy

from django.core import serializers

from formacion_academica.models import CursoEspecializacion

from nucleo.models import User
from datetime import datetime
from django.db.models import Max, Min, Count, Sum

from sia_stats.models import SIAYearModelCounter


from graphos.sources.simple import SimpleDataSource
#from graphos.renderers.morris import LineChart, AreaChart
from graphos.renderers.highcharts import LineChart


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

            years_cursos_especializacion_dates = CursoEspecializacion.objects.dates('fecha_inicio', 'year', order='DESC')
            years_cursos_especializacion = []

            for i in reversed(years_cursos_especializacion_dates[:10]):
                years_cursos_especializacion.append(i.year)

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

            cursos_data = [['Año', 'Personas', 'Total horas', 'Mis horas', 'Promedio Horas', 'Max horas', 'Min horas']]
            print(years_cursos_especializacion)

            for i in range(10):
                year = years_cursos_especializacion[i]
                cursos_data.append([years_cursos_especializacion[i]])
                u = User.objects.filter(cursos_especializacion__fecha_inicio__year=year).annotate(
                    Count('pk', distinct=True)).count()
                cursos_data[i + 1].append(u)
                th = CursoEspecializacion.objects.filter(fecha_inicio__year=year).aggregate(Sum('horas'))['horas__sum']
                cursos_data[i + 1].append(th)
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



        return render(request, self.template_name, context)



