from . import voice_chat

from flask import (
    Flask,
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.agents import plan_responses
from app.db import db
from app.models import Lesson, User
from app.utilities import get_current_user

import os
from flask import jsonify # Añadir a las importaciones
from werkzeug.utils import secure_filename

@voice_chat.route("/", methods=["GET", "POST"])
def chat():
    
    return render_template(
        "voice_chat.html",
        lessons=None,
        selected_lesson=None,
        user=None,
        history=[None],
    )

@voice_chat.route("/process_audio", methods=["POST"])
def process_audio():
    if 'audio_file' not in request.files:
        return jsonify({"error": "The audio file is missing"}), 400
        
    audio_file = request.files['audio_file']
    lesson_id = request.form.get('lesson_id')
    
    if audio_file.filename == '':
        return jsonify({"error": "The audio file is empty"}), 400

    filename = secure_filename(audio_file.filename)
    filepath = os.path.join("/tmp", filename)
    audio_file.save(filepath)

    return jsonify({
        "status": "success",
        "message": "Audio received and processed correctly.",
        "lesson_id": lesson_id,    
    }), 200
