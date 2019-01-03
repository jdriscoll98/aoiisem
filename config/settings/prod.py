
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

DEBUG = True

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

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'db_name',
#         'USER': 'db_user',
#         'PASSWORD': 'db_user_password',
#         'HOST': '',
#         'PORT': '',
#     }
# }

db_from_env = dj_database_url.config(default='postgres://jhrculleivnrun:44e9949d06ffaa2fc0f7451e925c7ba5658f96e3f8214ce096b7b0240c1ca022@ec2-107-20-250-113.compute-1.amazonaws.com:5432/dciibotrihvmab', conn_max_age=600)
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
