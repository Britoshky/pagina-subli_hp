# config.py
import os

# Configuración del servidor de correo
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 587
MAIL_USERNAME = "britoshky@gmail.com"  # Reemplaza con tu correo
MAIL_PASSWORD = "tavm jyle wwro bfeb"  # Reemplaza con tu contraseña
MAIL_USE_TLS = True
MAIL_USE_SSL = False

# Configuración del remitente
MAIL_SENDER = "britoshky@gmail.com"

# Configuración de optimización
class Config:
    # Configuración básica de Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key_change_in_production'
    
    # Configuración de sesión
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    
    # Configuración de compresión
    COMPRESS_MIMETYPES = [
        'text/html', 'text/css', 'text/xml', 'application/json',
        'application/javascript', 'text/javascript', 'application/xml',
        'text/plain', 'image/svg+xml'
    ]
    COMPRESS_LEVEL = 6
    COMPRESS_MIN_SIZE = 500
    COMPRESS_REGISTER = True
    
    # Configuración de caché
    SEND_FILE_MAX_AGE_DEFAULT = 31536000  # 1 año
    
    # Configuración de subida de archivos
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB máximo
    UPLOAD_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    
    # Configuración de imágenes
    IMAGE_MAX_WIDTH = 800
    IMAGE_MAX_HEIGHT = 600
    IMAGE_QUALITY = 85
    WEBP_QUALITY = 80
    THUMBNAIL_SIZE = (150, 150)

class DevelopmentConfig(Config):
    DEBUG = True
    COMPRESS_DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    COMPRESS_DEBUG = False
    
    # Configuración adicional para producción
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

# Configuración por defecto
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
