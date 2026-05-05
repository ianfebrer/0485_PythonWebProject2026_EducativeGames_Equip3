from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from config import USERS_FILE
from models.user import User
from storage.user_storage import UserStorage


auth_bp = Blueprint("auth", __name__)
storage = UserStorage(str(USERS_FILE))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Has d'omplir usuari i contrasenya.")
            return redirect(url_for("auth.register"))

        if storage.get_user(username):
            flash("Aquest nom d'usuari ja existeix.")
            return redirect(url_for("auth.register"))

        new_user = User(username=username, password=password)
        storage.add_user(new_user)

        flash("Registre completat amb exit! Ara pots iniciar sessio.")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = storage.get_user(username)
        if user and user.check_password(password):
            session["username"] = user.username
            return redirect(url_for("main.index"))

        flash("Usuari o contrasenya incorrectes.")
        return redirect(url_for("auth.login"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("main.index"))
