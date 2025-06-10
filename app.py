from flask import Flask
from flask_session import Session
from routes import initialize_routes
from utils.auth_utils import require_login
from tasks.scheduler import start_scheduler  # Importa el scheduler



app = Flask(__name__)

# Configuración de la sesión
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = "your_secret_key"  # Cambia por una clave segura
Session(app)

# Middleware para proteger rutas
@app.before_request
def check_auth():
    allowed_routes = ["auth.login", "auth.logout"]  # Rutas sin protección
    response = require_login(allowed_routes)
    if response:
        return response
@app.template_filter('format_currency')
def format_currency(value):
    """Convierte un número a formato de moneda con puntos como separador de miles."""
    return f"{int(value):,}".replace(",", ".")

# Inicializar rutas dinámicas
initialize_routes(app)


if __name__ == "__main__":
    # Ejecutar en el puerto 2000 y permitir acceso desde cualquier IP
    start_scheduler()  # Inicia el scheduler al levantar la app
    app.run(debug=True, host="0.0.0.0", port=2000)
