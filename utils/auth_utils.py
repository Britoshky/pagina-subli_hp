from flask import session, redirect, url_for, request

def login_user(username):
    """Inicia sesión del usuario"""
    session["user"] = username

def logout_user():
    """Cierra sesión del usuario"""
    session.pop("user", None)

def is_logged_in():
    """Verifica si el usuario está autenticado"""
    return "user" in session

def require_login(allowed_routes):
    """Middleware para proteger rutas"""
    # Permitir archivos estáticos sin autenticación
    if request.path.startswith('/static/'):
        return None
    if "user" not in session and request.endpoint not in allowed_routes:
        return redirect(url_for("auth.login"))
    return None
