from flask import Blueprint

main_chat = Blueprint(
        'main_chat',
        __name__,
        url_prefix='/main_chat',
        template_folder='templates',
        static_folder='static',
)

from . import routes