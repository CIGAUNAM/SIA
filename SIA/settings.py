"""
Configuración del SIA (Sistema de Información Académica).

Los valores sensibles o dependientes del entorno se leen de variables de
entorno o de un archivo `.env` (ver `.env.example`).
"""

from pathlib import Path

from decouple import Csv, config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='', cast=Csv())

INSTALLED_APPS = [
    # Unfold debe ir antes del admin; BasicAppConfig no reemplaza el sitio (usamos SIAAdminSite).
    'unfold.apps.BasicAppConfig',
    'unfold.contrib.simple_history',
    'SIA.apps.SIAAdminConfig',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'simple_history',

    'nucleo',
    'formacion_academica',
    'experiencia_profesional',
    'compromiso_institucional',
    'investigacion',
    'difusion_cientifica',
    'divulgacion_cientifica',
    'vinculacion',
    'movilidad_academica',
    'docencia',
    'formacion_recursos_humanos',
    'desarrollo_tecnologico',
    'distinciones',
    'formatos',
]

AUTH_USER_MODEL = 'nucleo.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

ROOT_URLCONF = 'SIA.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'SIA.wsgi.application'

# DB_ENGINE: 'postgresql' (producción) o 'sqlite' (desarrollo local / pruebas).
if config('DB_ENGINE', default='postgresql') == 'sqlite':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': config('DB_NAME', default=str(BASE_DIR / 'db.sqlite3')),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432'),
            'NAME': config('DB_NAME', default='sia'),
            'USER': config('DB_USER', default=''),
            'PASSWORD': config('DB_PASSWORD', default=''),
            'CONN_MAX_AGE': config('DB_CONN_MAX_AGE', default=60, cast=int),
        }
    }

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'es-mx'
LOCALE_PATHS = [BASE_DIR / 'locale']
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'
# Evidencias adjuntas: fuera de MEDIA_ROOT, se sirven solo mediante una vista con control de permisos.
PRIVATE_MEDIA_ROOT = Path(config('PRIVATE_MEDIA_ROOT', default=str(BASE_DIR / 'privado')))

LOGIN_URL = 'admin:login'

# Correo (recuperación de contraseña). Por defecto se imprime en la consola.
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='SIA <no-responder@localhost>')

# Nombre del país sede; se usa para distinguir producción nacional de internacional.
PAIS_SEDE = config('PAIS_SEDE', default='México')

if not DEBUG:
    SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=bool)
    CSRF_COOKIE_SECURE = SESSION_COOKIE_SECURE
    SECURE_CONTENT_TYPE_NOSNIFF = True

# Datos de la entidad que aparecen en el CV y en los formatos impresos.
ENTIDAD = {
    'nombre': config('ENTIDAD_NOMBRE', default='Centro de Investigaciones en Geografía Ambiental'),
    'siglas': config('ENTIDAD_SIGLAS', default='CIGA'),
    'director': config('ENTIDAD_DIRECTOR', default=''),
    'ciudad': config('ENTIDAD_CIUDAD', default='Morelia, Michoacán'),
    'direccion': config('ENTIDAD_DIRECCION', default=(
        'Antigua carretera a Pátzcuaro 8701, Col. Ex Hacienda de San José de la Huerta, C.P. 58190, '
        'Morelia, Michoacán, México')),
}

UNFOLD = {
    'SITE_TITLE': 'SIA',
    'SITE_HEADER': 'SIA',
    'SITE_SUBHEADER': 'Sistema de Información Académica',
    'SITE_SYMBOL': 'school',
    'SHOW_HISTORY': True,
    'SHOW_VIEW_ON_SITE': False,
    'DASHBOARD_CALLBACK': 'SIA.tablero.contexto_tablero',
    'SIDEBAR': {
        'show_search': True,
        'show_all_applications': False,
        'navigation': 'SIA.navegacion.menu',
    },
    'ACCOUNT': {
        'navigation': 'SIA.navegacion.enlaces_cuenta',
    },
    # Azul institucional
    'COLORS': {
        'primary': {
            '50': 'oklch(97% .014 254.604)',
            '100': 'oklch(93.2% .032 255.585)',
            '200': 'oklch(88.2% .059 254.128)',
            '300': 'oklch(80.9% .105 251.813)',
            '400': 'oklch(70.7% .165 254.624)',
            '500': 'oklch(62.3% .214 259.815)',
            '600': 'oklch(54.6% .245 262.881)',
            '700': 'oklch(48.8% .243 264.376)',
            '800': 'oklch(42.4% .199 265.638)',
            '900': 'oklch(37.9% .146 265.522)',
            '950': 'oklch(28.2% .091 267.935)',
        },
    },
}
