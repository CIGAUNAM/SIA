from django.http.response import Http404, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy

from django.core import serializers

from nucleo.models import User

import datetime

# Create your views here.




class Dashboard(View):
    form_class = None
    template_name = 'dashboard.html'
    aux = {}
    now = datetime.datetime.now()
    this_year = now.year
    ten_years_ago = now.year - 10

    usuarios = User.objects.all()




    def get(self, request):
        #obj = get_object_or_404(User, username__iexact=request.user)
        obj = range(self.ten_years_ago, self.this_year)


        return render(request, self.template_name,
                      {'aux': self.aux, 'obj': obj, 'active': 'detalle'}, )
