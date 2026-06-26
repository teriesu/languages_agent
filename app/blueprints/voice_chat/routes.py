import io
import os

from . import voice_chat

from flask import render_template, request, jsonify
from werkzeug.utils import secure_filename
from pydub import AudioSegment

from app.agents import transcribe_audio_in_memory
from app.agents.support.nodes.speach_corrector.node import correct_text
from app.agents.support.nodes.speach_evaluator.node import evaluate_text
from app.models import Lesson
from app.utilities import get_current_user, get_user_language_details

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, "uploaded_audio")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_AUDIO_EXTENSIONS = {".webm", ".mp3"}
ALLOWED_AUDIO_MIME_TYPES = {"audio/webm", "audio/mpeg", "audio/mp3", "video/webm"}

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
    if not filename:
        return jsonify({"error": "Invalid audio filename"}), 400

    extension = os.path.splitext(filename)[1].lower()
    content_type = (audio_file.mimetype or "").lower()

    if extension not in ALLOWED_AUDIO_EXTENSIONS:
        return jsonify({"error": "Only .webm and .mp3 files are supported."}), 400

    if content_type and content_type not in ALLOWED_AUDIO_MIME_TYPES:
        print(f"Unsupported audio format: {content_type}")
        return jsonify({"error": "Unsupported audio format."}), 400

    saved_path = os.path.join(UPLOAD_FOLDER, filename)
    audio_file.seek(0)
    audio_file.save(saved_path)

    try:
        with open(saved_path, "rb") as saved:
            file_bytes = saved.read()
    
        if extension == ".webm":
        
            audio_segment = AudioSegment.from_file(io.BytesIO(file_bytes), format="webm")
            
            in_memory_audio = io.BytesIO()
            audio_segment.export(in_memory_audio, format="wav")
            in_memory_audio.seek(0)
            
            filename_for_transcriber = filename.replace(extension, ".wav")
        else:
            
            in_memory_audio = io.BytesIO(file_bytes)
            filename_for_transcriber = filename

        user_language_details = get_user_language_details()
        ll_contraction = user_language_details.get("learning_language_contraction") if user_language_details else None
        language_learning = user_language_details.get("learning_language_name") if user_language_details else None
        language_native = user_language_details.get("native_language_name") if user_language_details else None
        level = user_language_details.get("level_name") if user_language_details else None


        in_memory_audio.name = filename_for_transcriber
        user_text = transcribe_audio_in_memory(in_memory_audio, filename, ll_contraction).strip()

        if not user_text:
            return jsonify({"error": "No speech detected in the audio."}), 400

        corrected_text = correct_text(user_text, language_learning, language_native, level)
        # feedback = evaluate_text(user_text, corrected_text, language_learning, language_native, level)
        feedback = "Feedback temporary disabled for costs, please check the corrected text."

        return jsonify({
            "status": "success",
            "transcription": user_text,
            "corrected_text": corrected_text,
            "feedback": feedback,
            "lesson_id": lesson_id,
        }), 200

    except Exception as e:
        print(f"Error processing audio: {e}")
        return jsonify({"error": "Hubo un error procesando el audio."}), 500

    finally:
        try:
            if os.path.exists(saved_path):
                os.remove(saved_path)
        except OSError:
            pass
