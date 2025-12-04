from flask import session, redirect, url_for, request

def require_login(allowed_routes):
    """Middleware para proteger rutas correctamente."""

    # 1. Permitir rutas estáticas, imágenes, assets, etc.
    if request.path.startswith('/static/'):
        return None

    # 2. Permitir endpoints sin nombre (static, favicon, manifest, errores)
    if request.endpoint is None:
        return None

    # 3. Permitir rutas públicas
    if request.endpoint in allowed_routes:
        return None

    # 4. Si el usuario no está logueado → enviar a login
    if "user" not in session:
        return redirect(url_for("auth.login"))

    return None
