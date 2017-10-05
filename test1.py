import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SIA.settings")

django.setup()

from datetime import datetime, date
from django.db import models
from django.conf import settings

from formacion_academica.models import CursoEspecializacion, Licenciatura, Maestria, Doctorado, PostDoctorado
from experiencia_laboral.models import *

import uuid

from nucleo.models import ZonaPais, Pais, Estado, Ciudad, Institucion, Dependencia, User, Revista, Indice
from investigacion.models import *

import pymysql

conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='cigacurricula')
cur = conn.cursor()
# cur.execute("SELECT curso, tipo, horas, mes_ini, anio_ini, mes_fin, anio_fin, area, instituciones, idu FROM fa_especializacion")
# cur.execute("SELECT DISTINCT area FROM `fa_especializacion` ORDER BY `fa_especializacion`.`area` ASC ")
# cur.execute("SELECT carrera, area, institucion, tesis, anio_ini, mes_ini, anio_fin, mes_fin, grado_fin, grado_ini, idu FROM fa_licenciatura")
# cur.execute("SELECT area, area_wos, institucion, tesis, anio_ini, mes_ini, anio_fin, mes_fin, grado_fin, grado_ini, idu FROM fa_maestria")
# cur.execute("SELECT DISTINCT area, area_wos FROM fa_maestria ORDER BY area")
# cur.execute("SELECT DISTINCT area, area_wos FROM fa_doctorado ORDER BY area")
# cur.execute("SELECT area, institucion, tesis, anio_ini, mes_ini, anio_fin, mes_fin, grado_fin, grado_ini, idu FROM fa_doctorado")
cur.execute(
    "SELECT titulo, ciudad_publi, casas_ed, estado, anio_pub, num_ed, pag_tot, isbn, vinculo, autores FROM ir_librosentidad")

for i in cur:
    l = "['"
    l += i[0]  # titulo
    l += "', '"
    l += i[1]  # ciudad_publi
    l += "', '"
    l += i[2]  # casas_ed
    l += "', '"
    l += i[3]  # estado
    l += "', "
    l += i[4]  # anio_pub
    l += ", "
    l += i[5]  # num_ed
    l += ", "
    l += i[6]  # pag_tot
    l += ", '"
    l += i[7]  # isbn
    l += "', '"
    l += i[8]  # vinculo
    l += "', '"
    l += i[9]  # autores
    l += "'],"
    print(l)

    items_data = [['Año', 'Mis horas de docencia', 'Promedio horas', 'Max horas', 'Min horas']]
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

        total_hours_year_sum = CursoDocencia.objects.filter(fecha_inicio__year=year, tipo='EXTRACURRICULAR').filter((
            (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad__year__gt=year)) |
            (Q(usuario__ingreso_entidad__year__lte=year) & Q(usuario__egreso_entidad=None)))).aggregate(
            Sum('total_horas'))[
            'total_horas__sum']
        if total_hours_year_sum == None:
            total_hours_year_sum = 0

        request_user_years_year_sum = User.objects.filter(cursodocencia_usuario__fecha_inicio__year=year, cursodocencia_usuario__tipo='EXTRACURRICULAR',
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

        max_item_year_user = User.objects.filter(cursodocencia_usuario__fecha_inicio__year=year, cursodocencia_usuario__tipo='EXTRACURRICULAR').annotate(
            Sum('cursodocencia_usuario__horas')).filter((
            (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
            (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).aggregate(
            Max('cursodocencia_usuario__horas__sum'))[
            'cursodocencia_usuario__horas__sum__max']
        if max_item_year_user == None:
            max_item_year_user = 0
        items_data[i + 1].append(max_item_year_user)

        min_item_year_user = User.objects.filter(cursodocencia_usuario__fecha_inicio__year=year, cursodocencia_usuario__tipo='EXTRACURRICULAR').annotate(
            Sum('cursodocencia_usuario__horas')).filter((
            (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
            (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).aggregate(
            Min('cursodocencia_usuario__horas__sum'))[
            'cursodocencia_usuario__horas__sum__min']
        if not min_item_year_user:
            min_item_year_user = 0
        items_data[i + 1].append(min_item_year_user)

    data_source = SimpleDataSource(data=items_data)
    chart_cursodocencia_escolarizado = LineChart(data_source)
    context['chart_cursodocencia_escolarizado'] = chart_cursodocencia_escolarizado
