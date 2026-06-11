from flask import Blueprint

voice_chat = Blueprint(
        'voice_chat',
        __name__,
        url_prefix='/voice_chat',
        template_folder='templates',
        static_folder='static',
)

from . import routes