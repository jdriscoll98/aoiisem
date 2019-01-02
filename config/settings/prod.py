from .base import *

import json

from django.core.exceptions import ImproperlyConfigured
import dj_database_url

# JSON-based secrets module
with open(os.path.join(BASE_DIR, 'local-secrets.json')) as f:
	secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
	'''Get the secret variable or return explicit exception.'''
	try:
		return secrets[setting]
	except KeyError:
		error_msg = 'Set the {0} environment variable'.format(setting)
		raise ImproperlyConfigured(error_msg)

SECRET_KEY = get_secret('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'core',
	'website',
	'Application',
	'Employment',
	'House',
	'Scheduling',
	'SetUP',
]

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'data', 'db.sqlite3'),
	}
}
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

LOGIN_URL = 'core:login'
# Static Files

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Media Files

MEDIA_ROOT =  os.path.dirname(os.path.abspath(__file__))
MEDIA_URL = '/resumes/'
# Email Backend

EMAIL_HOST = 'smtp-relay.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Google ReCaptcha
