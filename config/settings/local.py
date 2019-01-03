from .base import *

SECRET_KEY = 'xH8C6GEsGiYZXRb9NjKFfysi1jNhAUKpuBnj2nABsGjPhCChM2'

DEBUG = True

ALLOWED_HOSTS = ['*']


MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'whitenoise.middleware.WhiteNoiseMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Email Backend

EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Google ReCaptcha

RECAPTCHA_SECRET_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'

RECAPTCHA_SITE_KEY = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'

# Twitter API

PUBLIC_API_KEY = '7V4vHQHWm9CK1T4hC1byZJJzp'

PRIVATE_KEY_KEY = 'G2ahiH1i1bbocGc6QYqUNB4pwh1jBO0KKBP7uhXsAVaziYaW6G'

PUBLIC_ACCESS_TOKEN = '1065652779857965057-iJ9wtbWwmLjRlgW3G8fbGJsvjYfKSa'

PRIVATE_ACCESS_TOKEN = 'qcpfz4QQmiM2DaKjd7DTTwJ1ponJz4J3OTy4XZJCJXSNb'

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

#STATIC_ROOT = "/home/cfedeploy/webapps/cfehome_static_root/"

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "live-static", "media")
