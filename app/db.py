from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Importación local para romper el ciclo
    from .db import db, init_app
    db.init_app(app)
    
    return app


# if __name__ == "__main__":
#     init_app()