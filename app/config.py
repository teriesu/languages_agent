import os
from os import environ
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, "..", ".env"))  
class Config:
    SECRET_KEY = environ.get("FLASK_SECRET_KEY", "dev-secret")
    
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")
    
    if not SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_DATABASE_URI = "postgresql+psycopg://postgres:password@127.0.0.1:5433/langlearn_db"
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False