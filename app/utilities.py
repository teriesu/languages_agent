from flask import (
    session,
)
from .models import User, Languages

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