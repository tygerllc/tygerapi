# Django settings for tygerapi project.

from os.path import abspath, dirname, basename, join

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ROOT_PATH = abspath(dirname(__file__))
PROJECT_NAME = basename(ROOT_PATH)

ADMINS = (
    # ('Tim Ogilvie', 'me@timogilvie.com'),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'dev.db',                       # sqlite3 path.
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': ''
    }
}

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/static/static.lawrence.com/static/"
MEDIA_ROOT = join(ROOT_PATH, 'media')

# URL that handles the static served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://static.lawrence.com/static/", "http://example.com/static/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/static/static.lawrence.com/static/"
#STATIC_ROOT = join(ROOT_PATH, 'static_files')

# URL prefix for static files.
# Example: "http://static.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    join(ROOT_PATH, 'static/'),
    # "/Users/me/Dropbox/Tyger/tygerapi/static",
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '=h#-u!=#ksgvr$sl)8(xewe5h&+7n4qhc)dj11vb*(nvtu20k*'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'api.middleware.ContentTypeMiddleware',
)

ROOT_URLCONF = 'tygerapi.urls'

TEMPLATE_DIRS = (
    join(ROOT_PATH, 'templates'),
    join(ROOT_PATH, 'challenge/templates'),
    join(ROOT_PATH, 'bench/templates'),
    join(ROOT_PATH, 'profiles'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.request",
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'challenge',
    'bench',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.markup',
    'tagging',
    'piston',
    'profiles',
    'misc',
    'south',
    'device',
    'api'
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Forces use of lowercase tags in tagging application
FORCE_LOWERCASE_TAGS = True
AUTH_PROFILE_MODULE = 'challenge.UserProfile'
LOGIN_REDIRECT_URL = '/challenge/'
LOGIN_URL = '/login/'
PISTON_DISPLAY_ERRORS = True

try:
    from local_settings import *
except:
    pass

