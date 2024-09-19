from pathlib import Path
from environs import Env

env = Env()
env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env.str("SECRET_KEY", default="django-insecure-^qi19(+(oo-ere5b&$@275chw)k@7ob1)74aol5d$(k*)5kk5)")

DISCORD_BOT_PUBLIC_KEY = env("DISCORD_BOT_PUBLIC_KEY", default="")
DISCORD_APPLICATION_ID = env("DISCORD_APPLICATION_ID", default="")
DISCORD_BOT_TOKEN = env("DISCORD_BOT_TOKEN", default="")
DISCORD_BOT_CLIENT_SECRET = env("DISCORD_BOT_CLIENT_SECRET", default="")

DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = ["textable-todos.fly.dev"]
CSRF_TRUSTED_ORIGINS = ["https://textable-todos.fly.dev"]
if DEBUG:
    NGROK_DOMAIN = env("NGROK_DOMAIN")
    ALLOWED_HOSTS.extend(["localhost", "127.0.0.1", NGROK_DOMAIN])
    CSRF_TRUSTED_ORIGINS.append(f"https://{NGROK_DOMAIN}")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise',
    'django.contrib.staticfiles',

    "django_browser_reload",
    'tasks',
    'webhooks',
    'configs',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

ROOT_URLCONF = 'todo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'todo.wsgi.application'

DATABASES = {
    "default": env.dj_db_url("DATABASE_URL", default="sqlite:///db.sqlite3"),
}

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / ".staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'list'