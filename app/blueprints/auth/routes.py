from flask import (
    Flask,
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.agents.agents import plan_responses
from app.db import db
from app.models import Lesson, User
from app.utilities import get_current_user, get_supported_languages, get_possible_levels
from app.blueprints.voice_chat import voice_chat
from app.blueprints.main_chat import main_chat
from . import auth

@auth.route("/")
def index():
    return redirect(url_for("main_chat.chat"))


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter((User.email == email) | (User.username == email)).first()
        if user and check_password_hash(user.password_hash, password):
            session.clear()
            session["user_id"] = user.id
            session["username"] = user.username
            return redirect(url_for("main_chat.chat"))
        flash("Invalid credentials", "error")
    return render_template("login.html")


@auth.route("/register", methods=["GET", "POST"])
def register():
    
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        learning_language = request.form.get("learning_language")
        native_language = request.form.get("native_language")
        level_ll = request.form.get("level_ll")

        if not username or not email or not password:
            flash("Username, email, and password are required.", "error")
        elif User.query.filter((User.email == email) | (User.username == username)).first():
            flash("A user with that username or email already exists.", "error")
        else:
            user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password),
                learning_language=learning_language,
                native_language=native_language,
                level_ll=level_ll,
            )
            db.session.add(user)
            db.session.commit()
            session.clear()
            session["user_id"] = user.id
            session["username"] = user.username
            return redirect(url_for("main_chat.chat"))
    return render_template("register.html",
                           supported_languages=get_supported_languages(),
                           possible_levels=get_possible_levels()
                           )


@auth.route("/logout")
def logout():
    session.clear()
    flash("Logged out", "info")
    return redirect(url_for("auth.login"))