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


        # obj es donde se guarda la info de los datos
        obj = {}

        # obtener los datos de las horas de cursos de especializacion por año de los ultimos 10 años del usuario
        for year in range(self.ten_years_ago, self.this_year+1):
            h = 0
            c_year = request.user.cursos_especializacion.filter(fecha_inicio__year=year)
            for i in c_year:
                h += i.horas
            obj['mishorascursos-'+str(year)] = h

        usuarios_con_cursos = []
        for i in User.objects.all():
            if i.cursos_especializacion.filter(fecha_inicio__year=2015).count()



        return render(request, self.template_name,
                      {'aux': self.aux, 'obj': obj, 'active': 'detalle'}, )
