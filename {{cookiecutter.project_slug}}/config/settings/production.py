# -*- coding: utf-8 -*-
"""
Production Configurations

- Use Amazon's S3 for storing static files and uploaded media
- Use mailgun to send emails
- Use Redis for cache
{% if cookiecutter.use_sentry_for_error_reporting == 'y' %}
- Use sentry for error logging
{% endif %}
{% if cookiecutter.use_opbeat == 'y' %}
- Use opbeat for error reporting
{% endif %}
"""
from __future__ import absolute_import, unicode_literals
from .common import *  # noqa

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Raises ImproperlyConfigured exception if DJANGO_SECRET_KEY not in os.environ
SECRET_KEY = env('DJANGO_SECRET_KEY')


# This ensures that Django will be able to detect a secure connection
# properly on Heroku.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# SECURITY CONFIGURATION
# ------------------------------------------------------------------------------
# See https://docs.djangoproject.com/en/1.9/ref/middleware/#module-django.middleware.security
# and https://docs.djangoproject.com/ja/1.9/howto/deployment/checklist/#run-manage-py-check-deploy

# set this to 60 seconds and then to 518400 when you can prove it works
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    'DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
    'DJANGO_SECURE_CONTENT_TYPE_NOSNIFF', default=True)
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SECURE_SSL_REDIRECT = env.bool('DJANGO_SECURE_SSL_REDIRECT', default=True)
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'

# SITE CONFIGURATION
# ------------------------------------------------------------------------------
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.6/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['{{cookiecutter.domain_name}}'])
# END SITE CONFIGURATION

# EMAIL
# ------------------------------------------------------------------------------
DEFAULT_FROM_EMAIL = env('DJANGO_DEFAULT_FROM_EMAIL',
                         default='{{cookiecutter.project_name}} <noreply@{{cookiecutter.domain_name}}>')
EMAIL_SUBJECT_PREFIX = env('DJANGO_EMAIL_SUBJECT_PREFIX', default='[{{cookiecutter.project_name}}] ')
SERVER_EMAIL = env('DJANGO_SERVER_EMAIL', default=DEFAULT_FROM_EMAIL)

# Anymail with Mailgun
INSTALLED_APPS += ("anymail", )
ANYMAIL = {
    "MAILGUN_API_KEY": env('DJANGO_MAILGUN_API_KEY'),
}
EMAIL_BACKEND = "anymail.backends.mailgun.MailgunBackend"

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See:
# https://docs.djangoproject.com/en/dev/ref/templates/api/#django.template.loaders.cached.Loader
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader', ]),
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['console'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'django.security.DisallowedHost': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

# Custom Admin URL, use {% raw %}{% url 'admin:index' %}{% endraw %}
ADMIN_URL = env('DJANGO_ADMIN_URL')

# Your production stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------
