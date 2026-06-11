from flask import Flask, g, session

from .config import Config
from .db import db
from .models import User
from .routes import main_bp
from .blueprints.voice_chat import voice_chat
from .blueprints.main_chat import main_chat


def create_app() -> Flask:
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)
    db.init_app(app)
    app.register_blueprint(main_bp)
    app.register_blueprint(voice_chat)
    app.register_blueprint(main_chat)

    @app.before_request
    def load_current_user() -> None:
        g.user = None
        user_id = session.get("user_id")
        if user_id:
            g.user = User.query.get(user_id)

    return app


app = create_app()
