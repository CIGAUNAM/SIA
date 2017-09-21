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

        if request.user.is_authenticated:
            years_curso_especializacion = SIAYearModelCounter.objects.filter(model='CursoEspecializacion')
            years_curso_especializacion = years_curso_especializacion[years_curso_especializacion.count() - 11:]

            obj['curso_especializacion'] = {}

            years_cursos_especializacion = CursoEspecializacion.objects.dates('fecha_inicio', 'year', order='DESC')

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
                        Sum('cursos_especializacion__horas'))[
                        'cursos_especializacion__horas__sum']  # horas del usuario en el año actual
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
                print()

        return render(request, self.template_name,
                      {'aux': self.aux, 'obj': obj, 'active': 'detalle'}, )



