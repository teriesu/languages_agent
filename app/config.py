from os import environ

from dotenv import load_dotenv


load_dotenv()


class Config:
    SECRET_KEY = environ.get("FLASK_SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI = environ.get(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/langlearn",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
