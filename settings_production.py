"""
Settings de Producción para PythonAnywhere
"""
from .settings import *
import os

# Seguridad
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = False
ALLOWED_HOSTS = [
    os.environ.get('DOMAIN'),
    f"{os.environ.get('DOMAIN')}.pythonanywhere.com",
    'www.' + os.environ.get('DOMAIN', '')
]

# Base de Datos PostgreSQL para producción
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Archivos Estáticos
STATIC_ROOT = '/home/tu-username/mysite/static/'
MEDIA_ROOT = '/home/tu-username/mysite/media/'

# Correo (PythonAnywhere tiene configuración especial)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.googlemail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True

# Seguridad adicional
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Sesiones
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
