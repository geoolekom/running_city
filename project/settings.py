import os
from configparser import ConfigParser

config = ConfigParser()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(BASE_DIR)

DEFAULT_CONFIG_PATH = os.path.join(BASE_DIR, "build", "conf", "project.conf")
CONFIG_PATH = os.environ.get("CONFIG_PATH", DEFAULT_CONFIG_PATH)

config.read(CONFIG_PATH)

DEBUG = config.getboolean("main", "DEBUG")
SECRET_KEY = config.get("main", "SECRET")

INTERNAL_IPS = ["127.0.0.1"]
ALLOWED_HOSTS = ["*"]

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "bootstrap4",
]

if DEBUG:
    DJANGO_APPS += [
        "debug_toolbar",
    ]

PROJECT_APPS = [
    "core.apps.CoreConfig",
    "quiz.apps.QuizConfig",
]

INSTALLED_APPS = PROJECT_APPS + DJANGO_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]

    DEBUG_TOOLBAR_PANELS = [
        "debug_toolbar.panels.versions.VersionsPanel",
        "debug_toolbar.panels.timer.TimerPanel",
        "debug_toolbar.panels.settings.SettingsPanel",
        "debug_toolbar.panels.headers.HeadersPanel",
        "debug_toolbar.panels.request.RequestPanel",
        "debug_toolbar.panels.sql.SQLPanel",
        "debug_toolbar.panels.staticfiles.StaticFilesPanel",
        "debug_toolbar.panels.templates.TemplatesPanel",
        "debug_toolbar.panels.cache.CachePanel",
        "debug_toolbar.panels.signals.SignalsPanel",
        "debug_toolbar.panels.logging.LoggingPanel",
        "debug_toolbar.panels.redirects.RedirectsPanel",
    ]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "debug": DEBUG,
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": config.get("database", "ENGINE"),
        "NAME": config.get("database", "NAME"),
        "USER": config.get("database", "USER"),
        "PASSWORD": config.get("database", "PASSWORD"),
        "HOST": config.get("database", "HOST"),
        "PORT": config.getint("database", "PORT"),
    }
}

LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(PROJECT_DIR, "static")

MEDIA_URL = "/media/"

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
