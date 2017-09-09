from django.http.response import Http404, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy

from django.core import serializers

from nucleo.models import User

import datetime
from datetime import datetime

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



        obj = {}

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







        return render(request, self.template_name,
                      {'aux': self.aux, 'obj': obj, 'active': 'detalle'}, )
