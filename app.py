from flask import Flask, request
from flask_session import Session
from flask_compress import Compress
from routes import initialize_routes
from utils.auth_utils import require_login
from tasks.scheduler import start_scheduler  # Importa el scheduler
import os



app = Flask(__name__, static_folder="static", template_folder="templates")

# Configuración de la sesión
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = "your_secret_key"  # Cambia por una clave segura

# Configuración de compresión
app.config['COMPRESS_MIMETYPES'] = [
    'text/html', 'text/css', 'text/xml', 'application/json',
    'application/javascript', 'text/javascript', 'application/xml',
    'text/plain', 'image/svg+xml'
]
app.config['COMPRESS_LEVEL'] = 6
app.config['COMPRESS_MIN_SIZE'] = 500

# Configurar caché para archivos estáticos
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # 1 año para archivos estáticos

Session(app)
Compress(app)

# Middleware para proteger rutas
@app.before_request
def check_auth():
    # Permitir archivos estáticos
    if request.path.startswith('/static/'):
        return None

    allowed_routes = ["auth.login", "auth.logout"]  # Rutas sin protección
    response = require_login(allowed_routes)
    if response:
        return response
@app.template_filter('format_currency')
def format_currency(value):
    """Convierte un número a formato de moneda con puntos como separador de miles."""
    return f"{int(value):,}".replace(",", ".")

@app.template_filter('versioned_url')
def versioned_url(file_path):
    """Genera URLs con versión para cache busting."""
    from utils.compression_utils import get_versioned_url
    return get_versioned_url(file_path, app.static_folder)

@app.template_filter('minified_url')
def minified_url(file_path):
    """Convierte URLs de archivos CSS/JS a sus versiones minificadas."""
    if file_path.endswith('.css') and not file_path.endswith('.min.css'):
        minified_path = file_path.replace('.css', '.min.css')
        # Verificar si existe el archivo minificado
        full_path = os.path.join(app.static_folder, minified_path.lstrip('/static/'))
        if os.path.exists(full_path):
            return minified_path
    elif file_path.endswith('.js') and not file_path.endswith('.min.js'):
        minified_path = file_path.replace('.js', '.min.js')
        # Verificar si existe el archivo minificado
        full_path = os.path.join(app.static_folder, minified_path.lstrip('/static/'))
        if os.path.exists(full_path):
            return minified_path
    return file_path

# Headers de seguridad y rendimiento
@app.after_request
def after_request(response):
    # Cache headers para archivos estáticos
    if request.path.startswith('/static/'):
        response.headers['Cache-Control'] = 'public, max-age=31536000'  # 1 año
        response.headers['Expires'] = 'Thu, 31 Dec 2025 23:59:59 GMT'
    
    # Headers de seguridad
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    return response

# Configurar middleware de optimización de imágenes
from utils.image_middleware import setup_image_optimization
setup_image_optimization(app)

# Inicializar rutas dinámicas
initialize_routes(app)


if __name__ == "__main__":
    # Ejecutar en el puerto 2000 y permitir acceso desde cualquier IP
    start_scheduler()  # Inicia el scheduler al levantar la app
    app.run(debug=True, host="0.0.0.0", port=2000)
