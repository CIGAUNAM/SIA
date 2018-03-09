"""
Django settings for SIA project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

DATA_DIR = os.path.dirname(os.path.dirname(__file__))

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'm-y6($7)(5vy-*e!2f6pqxt6%^jqrnu4!&tbm2($ku^5i@dtiz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '10.10.2.203', '10.1.11.2', '201.144.41.229']

STATUS_PUBLICACION = (('', '-------'), ('ENVIADO', 'Enviado'), ('ACEPTADO', 'Aceptado'), ('EN_PRENSA', 'En prensa'), ('PUBLICADO', 'Publicado'), ('OTRO', 'Otro'))
STATUS_PROYECTO = (('', '-------'), ('NUEVO', 'Nuevo'), ('EN_PROCESO', 'En proceso'), ('CONCLUIDO', 'Concluído'), ('OTRO', 'Otro'))
CLASIFICACION_PROYECTO = (('', '-------'), ('BASICO', 'Básico'), ('APLICADO', 'Aplicado'), ('DESARROLLO_TECNOLOGICO', 'Desarrollo tecnológico'),('INNOVACION', 'Innovación'), ('INVESTIGACION_FRONTERA', 'Investigación de frontera'), ('OTRA', 'Otra'))
ORGANIZACION_PROYECTO = (('', '-------'), ('INDIVIDUAL', 'Individual'), ('COLECTIVO', 'Colectivo'))
MODALIDAD_PROYECTO = (('', '-------'), ('DISCIPLINARIO', 'Disciplinario'), ('MULTIDISCIPLINARIO', 'Multidisciplinario'), ('INTERDISCIPLINARIO', 'Interisciplinario'), ('TRANSDISCIPLINARIO', 'Transdisciplinario'), ('OTRA', 'Otra'))
FINANCIAMIENTO_UNAM = (('', '-------'), ('ASIGNADO', 'Presupuesto asignado a la entidad'), ('CONCURSADO', 'Presupuesto concursado por la entidad'), ('AUTOGENERADO', 'Recursos autogenerados (extraordinarios)'), ('OTRO', 'Otro'))
FINANCIAMIENTO_EXTERNO = (('', '-------'), ('ESTATAL', 'Gubernamental Estatal'), ('FEDERAL', 'Gubernamental Federal'), ('LUCRATIVO', 'Privado lucrativo'), ('NO_LUCRATIVO', 'Privado no lucrativo'), ('EXTRANJERO', 'Recursos del extranjero'))
FINANCIAMIENTO_TIPO = (('', '-------'), ('UNAM', FINANCIAMIENTO_UNAM), ('Externo', FINANCIAMIENTO_EXTERNO))
CURSO_ESPECIALIZACION_TIPO = (('', '-------'), ('CURSO', 'Curso'), ('DIPLOMADO', 'Diplomado'), ('CERTIFICACION', 'Certificación'), ('OTRO', 'Otro'))
CURSO_ESPECIALIZACION_MODALIDAD = (('', '-------'), ('PRESENCIAL', 'Presencial'), ('EN_LINEA', 'En línea'), ('MIXTO', 'Mixto'), ('OTRO', 'Otro'))
CARGO__TIPO_CARGO = (('', '-------'), ('ACADEMICO', 'Académico'), ('ADMINISTRATIVO', 'Administrativo'))
EVENTO__AMBITO = (('', '-------'), ('INSTITUCIONAL', 'Institucional'), ('REGIONAL', 'Regional'), ('NACIONAL', 'Nacional'), ('INTERNACIONAL', 'Internacional'), ('OTRO', 'Otro'))
EVENTO__RESPONSABILIDAD = (('', '-------'), ('COORDINADOR', 'Coordinador general'), ('COMITE', 'Comité organizador'), ('AYUDANTE', 'Ayudante'), ('TECNICO', 'Apoyo técnico'), ('OTRO', 'Otro'))
RED_ACADEMICA__CLASIFICACION = (('', '-------'), ('LOCAL', 'Local'), ('REGIONAL', 'Regional'), ('NACIONAL', 'Nacional'), ('INTERNACIONAL', 'Internacional'), ('OTRO', 'Otro'))
CONVENIO_ENTIDAD_EXTERNA__CLASIFICACION = (('', '-------'), ('FEDERAL', 'Gubernamental federal'), ('ESTATAL', 'Gubernamental estatal'), ('MUNICIPAL', 'Gubernamental municipal'), ('PRIVADA', 'Sector privado'), ('NO_LUCRATIVA', 'Sector privado no lucrativo'), ('EXTRANJERA', 'Extranjero'))
ENTIDAD_CLASIFICACION = (('', '-------'), ('FEDERAL', 'Gubernamental federal'), ('ESTATAL', 'Gubernamental estatal'), ('MUNICIPAL', 'Gubernamental municipal'), ('PRIVADA', 'Sector privado'), ('NO_LUCRATIVA', 'Sector privado no lucrativo'))
DISTINCION__AMBITO = (('', '-------'), ('INSTITUCIONAL', 'Institucional'), ('REGIONAL', 'Regional'), ('NACIONAL', 'Nacional'), ('INTERNACIONAL', 'Internacional'), ('OTRO', 'Otro'))
NIVEL_ACADEMICO = (('', '-------'), ('LICENCIATURA', 'Licenciatura'), ('MAESTRIA', 'Maestría'), ('DOCTORADO', 'Doctorado'))
RESENA__TIPO = (('', '-------'), ('LIBRO', 'Libro'), ('ARTICULO', 'Artículo'))
ARBITRAJE_ACADEMICA__TIPO = (('', '-------'), ('ARTICULO', 'Artículo en revista'), ('LIBRO', 'Libro'))

# Application definition

INSTALLED_APPS = [

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.admin',

    'nucleo.apps.NucleoConfig',
    'formacion_academica.apps.FormacionAcademicaConfig',
    'experiencia_laboral.apps.ExperienciaLaboralConfig',
    'investigacion.apps.InvestigacionConfig',
    'difusion_cientifica.apps.DifusionCientificaConfig',
    'divulgacion_cientifica.apps.DivulgacionCientificaConfig',
    'vinculacion.apps.VinculacionConfig',
    'apoyo_institucional.apps.ApoyoInstitucionalConfig',
    'movilidad_academica.apps.MovilidadAcademicaConfig',
    'docencia.apps.DocenciaConfig',
    'formacion_recursos_humanos.apps.FormacionRecursosHumanosConfig',
    'desarrollo_tecnologico.apps.DesarrolloTecnologicoConfig',
    'distinciones.apps.DistincionesConfig',
    'formatos.apps.FormatoConfig',

    'rest_framework',
    'django_adminlte',
    'sortedm2m',
    'table',
    'django_select2',
    'graphos',

]

#MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
#MESSAGE_LEVEL = 'DEBUG'


AUTH_USER_MODEL = 'nucleo.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'SIA.urls'

'''
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
'''

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'SIA.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'CONN_MAX_AGE': 0,
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'NAME': 'sia',
        'PASSWORD': '',
        'PORT': '3306',
        'USER': 'root'
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(DATA_DIR, 'static')
MEDIA_ROOT = os.path.join(DATA_DIR, 'media')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static_custom'),
)



# TEMPLATE_DIRS = (
#    os.path.join(BASE_DIR, 'templates'),
# )

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters'
)

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = '/'

