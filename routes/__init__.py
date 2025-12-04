from routes.category_routes import create_category_blueprint
from routes.home_routes import home_bp
from routes.auth_routes import auth_bp
from utils.auth_utils import require_login
from routes.ads_routes import ads_bp  

def initialize_routes(app):
    # Middleware eliminado: la protección de rutas se gestiona en app.py

    # Registrar rutas de autenticación
    app.register_blueprint(auth_bp)

    # Registrar la ruta de inicio
    app.register_blueprint(home_bp)

    # Luego, dentro de initialize_routes o directamente en app.py:
    app.register_blueprint(ads_bp)

    # Categorías dinámicas
    categories = {
        "books": {
            "json_file": "data/books.json",
            "upload_folder": "static/uploads/books"
        },
        "stickers": {
            "json_file": "data/stickers.json",
            "upload_folder": "static/uploads/stickers"
        },
        "cojines": {
            "json_file": "data/cojines.json",
            "upload_folder": "static/uploads/cojines"
        }
    }

    for category, config in categories.items():
        blueprint = create_category_blueprint(
            category,
            config["json_file"],
            config["upload_folder"]
        )
        app.register_blueprint(blueprint)
