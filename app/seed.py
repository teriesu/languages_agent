"""Utilities to seed the immutable base data sets."""

from typing import Iterable

from .db import db
from .models import Languages, Levels


DEFAULT_LANGUAGES = [
    {"name": "English", "contraction": "en"},
    {"name": "Spanish", "contraction": "es"},
    {"name": "French", "contraction": "fr"},
    {"name": "Portuguese", "contraction": "pt"},
    {"name": "German", "contraction": "de"},
]

DEFAULT_LEVELS = [
    {"name": "A1", "description": "Knows a few phrases and needs structured guidance."},
    {"name": "A2", "description": "Can communicate in simple and routine tasks requiring a direct exchange of information."},
    {"name": "B1", "description": "Can understand and produce simple, routine texts."},
    {"name": "B2", "description": "Can express themselves fluently and spontaneously."},
    {"name": "C1", "description": "Can understand and express complex ideas with ease."},
    {"name": "C2", "description": "Has mastered the language and can communicate effortlessly."},
]


def _ensure_defaults(model, entries: Iterable[dict]) -> int:
    created = 0
    for entry in entries:
        name = entry["name"]
        if not model.query.filter_by(name=name).first():
            db.session.add(model(**entry))
            created += 1
    return created


def seed_base_data() -> tuple[int, int]:
    """Ensure the languages and levels tables contain the default records."""
    languages_created = _ensure_defaults(Languages, DEFAULT_LANGUAGES)
    levels_created = _ensure_defaults(Levels, DEFAULT_LEVELS)
    if languages_created or levels_created:
        db.session.commit()
    return languages_created, levels_created
