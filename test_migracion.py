import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SIA.settings")

django.setup()

from datetime import datetime, date
from django.db import models
#from django.contrib.auth.models import AbstractUser
from django.conf import settings

#from autoslug import AutoSlugField

from formacion_academica.models import CursoEspecializacion, Licenciatura, Maestria, Doctorado, PostDoctorado
from experiencia_laboral.models import *

import uuid


from nucleo.models import ZonaPais, Pais, Estado, Ciudad, Institucion, Dependencia, User, Revista, Indice
from investigacion.models import *


import pymysql

conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='cigacurricula')
cur = conn.cursor()
cur.execute("SELECT titulo, tipo, clasificacion as indizado, revista, volumen, numeros, anio, issn, FROM ir_articuloscientificos")

for i in cur:
    print(i[0], i[1])