from django.http.response import Http404, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy

from django.core import serializers

from nucleo.models import User

import datetime
from datetime import datetime

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
        #obj = get_object_or_404(User, username__iexact=request.user)
        obj = range(self.ten_years_ago, self.this_year)

        years_curso_especializacion = SIAYearModelCounter.objects.filter(model='CursoEspecializacion')




        obj = {}

        if request.user.is_authenticated:
            years_curso_especializacion = SIAYearModelCounter.objects.filter(model='CursoEspecializacion')
            years_curso_especializacion = years_curso_especializacion[years_curso_especializacion.count() - 11:]

            obj['curso_especializacion'] = {}


            for i in range(len(years_curso_especializacion)):
                try:
                    #obj['curso_especializacion'][str(years_curso_especializacion[i].year)] = round(years_curso_especializacion[i].counter / years_curso_especializacion[i].users.count(), 2)
                    obj['curso_especializacion'][str(years_curso_especializacion[i].year)] = str(years_curso_especializacion[i].counter) + " " + str(years_curso_especializacion[i].users.count())
                except ZeroDivisionError:
                    obj['curso_especializacion'][str(years_curso_especializacion[i].year)] = 0.0


        '''
        try:            
            # obtener los datos de las horas de cursos de especializacion por año de los ultimos 10 años del usuario
            for year in range(self.ten_years_ago, self.this_year+1):
                h = 0
                cursos_year = request.user.cursos_especializacion.filter(fecha_inicio__year=year)
                for i in cursos_year:
                    h += i.horas
                obj['mishorascursos-'+str(year)] = h
    
            horas_periodo_anual = {}
            usuarios_con_cursos = 0
    
            for year in range(self.ten_years_ago, self.this_year + 1):
                horas_periodo_anual['year'] = 0
    
    
            usuarios = User.objects.exclude(pk=request.user.pk)
            for usuario in usuarios:
                h = 0
    
                # paa cada usuario iterar los ultimos 10 años, y para cada año:
                for year in range(self.ten_years_ago, self.this_year + 1):
    
                    cursos_year = usuario.cursos_especializacion.filter(fecha_inicio__year=year)
                    for i in cursos_year:
                        h += i.horas
    
                    horas_periodo_anual['year'] = 0
    
                if h > 0:
                    usuarios_con_cursos += 1
                h = 0
        except:
            pass
        '''

"""



# devuelve la suma total de horas de cursos por año de todos los usuarios (que tengan cursos ese año)
c = CursoEspecializacion.objects.filter(fecha_inicio__year=2007).aggregate(year_users=Sum('horas'))
CursoEspecializacion.objects.filter(fecha_inicio__year=2007).aggregate(Sum('horas'))['horas__sum']


# cantidad de usuarios que tienen al menos un curso, por año.
u = User.objects.filter(cursos_especializacion__fecha_inicio__year=2007).annotate(Count('pk', distinct=True)).count()

# suma de horas por usuario por año
u = User.objects.filter(cursos_especializacion__fecha_inicio__year=2005).annotate(Sum('cursos_especializacion__horas'))

# usuario que tiene la mayor cantidad de horas en el año
u = User.objects.filter(cursos_especializacion__fecha_inicio__year=2005).annotate(Sum('cursos_especializacion__horas')).aggregate(Max('cursos_especializacion__horas__sum'))

# usuario que tiene la menor cantidad de horas en el año
u = User.objects.filter(cursos_especializacion__fecha_inicio__year=2005).annotate(Sum('cursos_especializacion__horas')).aggregate(Min('cursos_especializacion__horas__sum'))['cursos_especializacion__horas__sum__min']


"""





        return render(request, self.template_name,
                      {'aux': self.aux, 'obj': obj, 'active': 'detalle'}, )
