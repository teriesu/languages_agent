from . import voice_chat

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

@voice_chat.route("/", methods=["GET", "POST"])
def chat():
    
    return render_template(
        "voice_chat.html",
        lessons=None,
        selected_lesson=None,
        user=None,
        history=[None],
    )
