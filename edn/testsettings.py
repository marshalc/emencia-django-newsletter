"""Settings for testing emencia"""

SITE_ID = 1

USE_I18N = False

ROOT_URLCONF = 'emencia.urls'

DATABASES = {'default': {'NAME': 'newsletter_tests.db', 'ENGINE': 'django.db.backends.sqlite3'}}

INSTALLED_APPS = ['django.contrib.contenttypes', 'django.contrib.sites', 'django.contrib.auth', 'tagging', 'emencia']
