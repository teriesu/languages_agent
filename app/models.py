from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from .db import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    learning_language = db.Column(db.String(64), nullable=True)
    native_language = db.Column(db.String(64), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    lessons = relationship("Lesson", back_populates="owner")

    def __repr__(self) -> str:
        return f"<User {self.username}>"


class Lesson(db.Model):
    __tablename__ = "lessons"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120), nullable=False)
    language = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    owner = relationship("User", back_populates="lessons")
    concepts = relationship("Concept", back_populates="lesson", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Lesson {self.title} ({self.language})>"


class Concept(db.Model):
    __tablename__ = "concepts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey("lessons.id"), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    summary = db.Column(db.Text, nullable=True)
    vector = db.Column(ARRAY(db.Float), nullable=True, doc="Placeholder for pgvector embeddings")
    meta_data = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    lesson = relationship("Lesson", back_populates="concepts")

    def __repr__(self) -> str:
        return f"<Concept {self.title} in lesson {self.lesson_id}>"
