from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from .db import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    learning_language = db.Column(db.Integer, db.ForeignKey("languages.id"), nullable=True)
    native_language = db.Column(db.Integer, db.ForeignKey("languages.id"), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    level_ll = db.Column(db.Integer, db.ForeignKey("levels.id"), nullable=True)

    lessons = relationship("Lesson", back_populates="owner")
    learning_language_obj = relationship("Languages", foreign_keys=[learning_language])
    native_language_obj = relationship("Languages", foreign_keys=[native_language])
    level_ll_obj = relationship("Levels", foreign_keys=[level_ll])

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

class Languages(db.Model):
    __tablename__ = "languages"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    contraction = db.Column(db.String(16), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"<Language {self.name}>"

class Levels(db.Model):
    __tablename__ = "levels"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self) -> str:
        return f"<Level {self.name}>"