from flask import Blueprint, render_template, request, redirect, url_for, session

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "palita" and password == "Viajes2024#":
            session["user"] = username
            return redirect(url_for("home.index"))  # Redirige al inicio
        else:
            return render_template("login.html", error="Usuario o contraseña inválidos")

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.pop("user", None)  # Elimina al usuario de la sesión
    return redirect(url_for("auth.login"))  # Redirige al login
