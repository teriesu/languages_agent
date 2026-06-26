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
from .db import db
from .models import Lesson, User
from .utilities import get_current_user
from .blueprints.voice_chat import voice_chat
from .blueprints.main_chat import main_chat
from .blueprints.auth import auth


main_bp = Blueprint("main", __name__)


def create_app() -> Flask:
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)
    db.init_app(app)
    app.register_blueprint(main_bp)
    app.register_blueprint(voice_chat)
    app.register_blueprint(main_chat)
    app.register_blueprint(auth)

    @app.before_request
    def load_logged_in_user() -> None:
        g.user = None
        user_id = session.get("user_id")
        if user_id is not None:
            g.user = User.query.get(user_id)

    return app