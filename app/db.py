from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .config import Config




def init_app(app: Flask | None = None) -> None:
    if app is None:
        app = Flask(__name__)
        app.config.from_object(Config)

    db.init_app(app)
    with app.app_context():
        db.create_all()


if __name__ == "__main__":
    init_app()
