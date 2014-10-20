"""
Django settings for notifsys project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEMPLATE_PATH = os.path.join(BASE_DIR,'templates')

STATIC_PATH=os.path.join(BASE_DIR,'static')

DATABASE_PATH=os.path.join(BASE_DIR,'listing.db')

LOGIN_URL='/listing/login/'
MEDIA_URL="/media/"
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')
TEMPLATE_DIRS=(
    #'/home/ht/projects/classifiedsystem/templates',

    TEMPLATE_PATH,
)



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'b1xmuuuy^%j(xt$-2v*&v@mip1qie4j1^1-x7!)r*3het@1hba'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'user_sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'listing',
    'djcelery',
   
)

MIDDLEWARE_CLASSES = (
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    'user_sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'notifsys.urls'

WSGI_APPLICATION = 'notifsys.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
# DATABASES = {
#    'default' : {
#       'ENGINE' : 'django_mongodb_engine',
#       'NAME' : 'django_db'
#    }
# }  
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DATABASE_PATH,
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql', 
#         'NAME': 'listing',
#         'USER': 'root',
#         'PASSWORD': 'ht',
#         'HOST': '127.0.0.1',   # Or an IP Address that your DB is hosted on
#         'PORT': '3306',
#     }
     
# }

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/


STATICFILES_DIRS=(
    STATIC_PATH,
)

SESSION_ENGINE = 'user_sessions.backends.db'
TEMPLATE_CONTEXT_PROCESSORS += ("django.core.context_processors.request",)

import djcelery
djcelery.setup_loader() 
BROKER_URL = 'amqp://myuser:1234@localhost:5672//' 
CELERY_IMPORTS = ('listing.task',)
