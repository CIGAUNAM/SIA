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
cur.execute("SELECT titulo, revista, volumen, numeros, anio, issn, becarios AS status, electronica, autores_iimas, indices, pagina_i, pagina_f, doi FROM ir_articuloscientificos")



for i in cur:
    l = "('"
    l += i[0]  # titulo
    l += "', '"
    l += i[1]  # revista
    l += "', '"
    l += i[2]  # volumen
    l += "', '"
    l += i[3]  # numero
    l += "', "
    l += i[4]  # anio
    l += ", '"
    l += i[5]  # issn
    l += "', '"
    l += i[6]  # status
    l += "', '"
    l += i[7]  # electronica
    l += "', '"
    l += i[8]  # autores
    l += "', '"
    l += i[9]  # indices
    l += "', "
    l += i[10]  # pag i
    l += ", "
    l += i[11]  # pag f
    l += ", '"
    l += i[12]  # doi
    l += "'),"
    print(l)



cur.close()
conn.close()


