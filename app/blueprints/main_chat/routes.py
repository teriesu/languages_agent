from . import main_chat

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

from app.agents import plan_responses
from app.db import db
from app.models import Lesson, User
from app.utilities import get_current_user

@main_chat.route("/", methods=["GET", "POST"])
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
