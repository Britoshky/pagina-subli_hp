from flask import session, redirect, url_for, request

def login_user(username):
    """Inicia sesión del usuario"""
    session["user"] = username

def logout_user():
    """Cierra sesión del usuario"""
    session.pop("user", None)

def is_logged_in():
    """Retorna True si el usuario está autenticado"""
    return "user" in session

def require_login(allowed_routes):
    """Middleware usado en versiones antiguas (ya no se usa para auth global)"""
    if request.path.startswith('/static/'):
        return None
    if request.endpoint in allowed_routes:
        return None
    if request.endpoint is None:
        return None
    if "user" not in session:
        return redirect(url_for("auth.login"))
    return None
