from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from .agents import plan_responses
from .db import db
from .models import Lesson, User


main_bp = Blueprint("main", __name__)


def create_app() -> Flask:
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)
    db.init_app(app)
    app.register_blueprint(main_bp)

    @app.before_request
    def load_logged_in_user() -> None:
        g.user = None
        user_id = session.get("user_id")
        if user_id is not None:
            g.user = User.query.get(user_id)

    return app


def get_current_user() -> User | None:
    user_id = session.get("user_id")
    if not user_id:
        return None
    return User.query.get(user_id)


@main_bp.route("/")
def index():
    return redirect(url_for("main.chat"))


@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter((User.email == email) | (User.username == email)).first()
        if user and check_password_hash(user.password_hash, password):
            session.clear()
            session["user_id"] = user.id
            session["username"] = user.username
            return redirect(url_for("main.chat"))
        flash("Invalid credentials", "error")
    return render_template("auth/login.html")


@main_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        learning_language = request.form.get("learning_language")
        native_language = request.form.get("native_language")

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
            )
            db.session.add(user)
            db.session.commit()
            session.clear()
            session["user_id"] = user.id
            session["username"] = user.username
            return redirect(url_for("main.chat"))
    return render_template("auth/register.html")


@main_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out", "info")
    return redirect(url_for("main.login"))


@main_bp.route("/chat", methods=["GET", "POST"])
def chat():
    user = get_current_user()
    if not user:
        flash("Create an account to continue", "warning")
        return redirect(url_for("main.login"))

    lessons = Lesson.query.order_by(Lesson.created_at.desc()).all()
    selected_lesson = None
    lesson_id = request.values.get("lesson_id")
    if lesson_id:
        selected_lesson = Lesson.query.get(lesson_id)
    if not selected_lesson and lessons:
        selected_lesson = lessons[0]

    history = list(session.get("chat_history", []))
    if request.method == "POST":
        message = request.form.get("message", "").strip()
        if message:
            agents = [
                {"title": result.title, "message": result.message}
                for result in plan_responses(message, selected_lesson.title if selected_lesson else None)
            ]
            history.append(
                {
                    "lesson": selected_lesson.title if selected_lesson else "General",
                    "message": message,
                    "agents": agents,
                }
            )
            session["chat_history"] = history[-12:]
        else:
            flash("Ask something to trigger the language agents", "info")

    return render_template(
        "chat.html",
        lessons=lessons,
        selected_lesson=selected_lesson,
        user=user,
        history=history,
    )
