import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SIA.settings")

django.setup()

from datetime import datetime, date
from django.db import models
# from django.contrib.auth.models import AbstractUser
from django.conf import settings

# from autoslug import AutoSlugField
from nucleo.models import *
from compromiso_institucional.models import ComisionInstitucional, Representacion, LaborDirectivaCoordinacion, \
    RepresentacionOrganoColegiadoUNAM, ComisionInstitucionalCIGA, ApoyoTecnico, ApoyoOtraActividad
from desarrollo_tecnologico.models import TipoDesarrollo, Licencia, DesarrolloTecnologico
from difusion_cientifica.models import MemoriaInExtenso, Resena, OrganizacionEventoAcademico, \
    ParticipacionEventoAcademico

from formacion_academica.models import CursoEspecializacion, Licenciatura, Maestria, Doctorado, PostDoctorado
from experiencia_profesional.models import *


