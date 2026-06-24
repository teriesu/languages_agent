import click

from flask import Flask, g, session

from .config import Config
from .db import init_app
from .models import User
from .routes import main_bp
from .blueprints.voice_chat import voice_chat
from .blueprints.main_chat import main_chat
from .blueprints.auth import auth
from .seed import seed_base_data


def create_app() -> Flask:
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)
    init_app(app)
    app.register_blueprint(main_bp)
    app.register_blueprint(voice_chat)
    app.register_blueprint(main_chat)
    app.register_blueprint(auth)

    @app.before_request
    def load_current_user() -> None:
        g.user = None
        user_id = session.get("user_id")
        if user_id:
            g.user = User.query.get(user_id)

    @app.cli.command("seed-db")
    def seed_db() -> None:
        """Insert the immutable language and level defaults."""
        languages_created, levels_created = seed_base_data()
        click.echo(
            f"seed-db: added {languages_created} language(s) and {levels_created} level(s)."
        )

    return app


app = create_app()
