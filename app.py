from flask import Flask, request, send_from_directory, session, redirect, url_for
from flask_session import Session
from flask_compress import Compress
from routes import initialize_routes
from utils.auth_utils import is_logged_in
from tasks.scheduler import start_scheduler
import os

# --------------------------------------------------------
# INICIALIZACIÓN FLASK
# --------------------------------------------------------
app = Flask(
    __name__,
    static_folder="static",
    static_url_path="/static",
    template_folder="templates"
)

# Ruta forzada para servir archivos estáticos
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

# --------------------------------------------------------
# SESIONES
# --------------------------------------------------------
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = "your_secret_key"

Session(app)
Compress(app)

# --------------------------------------------------------
# AUTENTICACIÓN GLOBAL
# --------------------------------------------------------
PUBLIC_PATHS = [
    "/auth/login",
    "/auth/logout",
    "/favicon.ico"
]

@app.before_request
def global_auth():
    path = request.path

    # 1) Permitir SIEMPRE archivos estáticos
    if path.startswith("/static/"):
        return None

    # 2) Permitir rutas públicas
    if path in PUBLIC_PATHS:
        return None

    # 3) Permitir archivos sin endpoint (error handlers, etc.)
    if request.endpoint is None:
        return None

    # 4) Si no está logueado → login
    if not is_logged_in():
        return redirect(url_for("auth.login"))

# --------------------------------------------------------
# FORMATTERS Y UTILIDADES
# --------------------------------------------------------
@app.template_filter('format_currency')
def format_currency(value):
    return f"{int(value):,}".replace(",", ".")

@app.template_filter('versioned_url')
def versioned_url(file_path):
    from utils.compression_utils import get_versioned_url
    return get_versioned_url(file_path, app.static_folder)

@app.template_filter('minified_url')
def minified_url(file_path):
    if file_path.endswith(".css") and not file_path.endswith(".min.css"):
        minified_path = file_path.replace(".css", ".min.css")
        if os.path.exists(os.path.join(app.static_folder, minified_path.lstrip("/static/"))):
            return minified_path
    if file_path.endswith(".js") and not file_path.endswith(".min.js"):
        minified_path = file_path.replace(".js", ".min.js")
        if os.path.exists(os.path.join(app.static_folder, minified_path.lstrip("/static/"))):
            return minified_path
    return file_path

# --------------------------------------------------------
# HEADERS DE SEGURIDAD
# --------------------------------------------------------
@app.after_request
def after_request(response):
    if request.path.startswith("/static/"):
        response.headers["Cache-Control"] = "public, max-age=31536000"
        response.headers["Expires"] = "Thu, 31 Dec 2025 23:59:59 GMT"

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"

    return response

# --------------------------------------------------------
# MIDDLEWARE IMÁGENES + RUTAS
# --------------------------------------------------------
from utils.image_middleware import setup_image_optimization
setup_image_optimization(app)

initialize_routes(app)

# --------------------------------------------------------
# RUN SERVER
# --------------------------------------------------------
if __name__ == "__main__":
    start_scheduler()
    app.run(host="0.0.0.0", port=2000, debug=True)
