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
#cur.execute("SELECT curso, tipo, horas, mes_ini, anio_ini, mes_fin, anio_fin, area, instituciones, idu FROM fa_especializacion")
#cur.execute("SELECT DISTINCT area FROM `fa_especializacion` ORDER BY `fa_especializacion`.`area` ASC ")
#cur.execute("SELECT carrera, area, institucion, tesis, anio_ini, mes_ini, anio_fin, mes_fin, grado_fin, grado_ini, idu FROM fa_licenciatura")
#cur.execute("SELECT area, area_wos, institucion, tesis, anio_ini, mes_ini, anio_fin, mes_fin, grado_fin, grado_ini, idu FROM fa_maestria")
#cur.execute("SELECT DISTINCT area, area_wos FROM fa_maestria ORDER BY area")
#cur.execute("SELECT DISTINCT area, area_wos FROM fa_doctorado ORDER BY area")
#cur.execute("SELECT area, institucion, tesis, anio_ini, mes_ini, anio_fin, mes_fin, grado_fin, grado_ini, idu FROM fa_doctorado")
cur.execute("SELECT titulo, ciudad_publi, casas_ed, estado, anio_pub, num_ed, pag_tot, isbn, vinculo, autores FROM ir_librosentidad")



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




articulos_investigacion_enprensa_data = [['Año', 'Mis artículos', 'Promedio por persona', 'Max por persona', 'Min por persona']]
for i in range(num_years):
    year = last_x_years[i]
    articulos_investigacion_enprensa_data.append([str(year)])

    total_articulos_cientificos_year_sum = ArticuloCientifico.objects.filter(fecha__year=year, status='EN_PRENSA').count()
    request_user_articulo_cientifico_year_sum = ArticuloCientifico.objects.filter(fecha__year=year, status='EN_PRENSA', usuarios=request.user).count()
    if not request_user_articulo_cientifico_year_sum:
        request_user_articulo_cientifico_year_sum = 0
    articulos_investigacion_enprensa_data[i + 1].append(request_user_articulo_cientifico_year_sum)

    users_with_articles_year_count = User.objects.filter(
        Q(articulo_cientifico_autores__fecha__year=year, articulo_cientifico_autores__status='EN_PRENSA') &
        ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
         (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
        Count('pk', distinct=True)).count()  # numero de usuarios activos en el año y con cursos en el año
    if users_with_articles_year_count == None:
        users_with_articles_year_count = 0
    if users_with_articles_year_count > 0:
        articulos_investigacion_enprensa_data[i + 1].append(
            round(total_articulos_cientificos_year_sum / users_with_articles_year_count, 2))
    else:
        articulos_investigacion_enprensa_data[i + 1].append(0)

    max_articulo_cientifico_year_user = User.objects.filter(
        Q(articulo_cientifico_autores__fecha__year=year, articulo_cientifico_autores__status='EN_PRENSA') &
        ((Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad__year__gt=year)) |
         (Q(ingreso_entidad__year__lte=year) & Q(egreso_entidad=None)))).annotate(
        Count('articulo_cientifico_autores')).aggregate(Max('articulo_cientifico_autores__count'))[
        'articulo_cientifico_autores__count__max']
    if max_articulo_cientifico_year_user == None:
        max_articulo_cientifico_year_user = 0
    articulos_investigacion_enprensa_data[i + 1].append(max_articulo_cientifico_year_user)

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


