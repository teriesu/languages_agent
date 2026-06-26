from flask import (
    session,
)
from .models import db, User, Languages, Levels
from sqlalchemy.orm import aliased

def get_current_user() -> User | None:
    user_id = session.get("user_id")
    if not user_id:
        return None
    return User.query.get(user_id)

def get_supported_languages() -> list[list[str]]:
    return [[lang.id, lang.name] for lang in Languages.query.all()]

def get_possible_levels() -> list[list[str]]:
    from .models import Levels
    return [[level.id, level.name, level.description] for level in Levels.query.all()]

def get_user_language_details() -> dict | None:
    user_id = session.get("user_id")
    if not user_id:
        return None

    lang_learning = aliased(Languages, name="lang_learning")
    lang_native = aliased(Languages, name="lang_native")
    level_ll = aliased(Levels, name="level_ll")  # Alias para los niveles

    result = (
        db.session.query(
            User.username,
            lang_learning.name.label("learning_language_name"),
            lang_native.name.label("native_language_name"),
            lang_learning.contraction.label("learning_language_contraction"),
            level_ll.name.label("level_name")
        )
        .join(lang_learning, User.learning_language == lang_learning.id)
        .join(lang_native, User.native_language == lang_native.id)
        .join(level_ll, User.level_ll == level_ll.id)
        .filter(User.id == user_id)
        .first()
    )

    if not result:
        return None

    return {
        "username": result.username,
        "learning_language_name": result.learning_language_name,
        "native_language_name": result.native_language_name,
        "learning_language_contraction": result.learning_language_contraction,
        "level_name": result.level_name
    }