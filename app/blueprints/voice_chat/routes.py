import io
import os

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
    jsonify,
)
from werkzeug.utils import secure_filename

from app.agents import transcribe_audio_in_memory
from app.db import db
from app.utilities import get_current_user

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, "uploaded_audio")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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

    saved_path = os.path.join(UPLOAD_FOLDER, filename)
    audio_file.seek(0)
    audio_file.save(saved_path)

    print(f"Received audio file: {filename} for lesson ID: {lesson_id}")
    print(f"Saved audio file to: {saved_path}")

    in_memory_audio = io.BytesIO(open(saved_path, "rb").read())
    in_memory_audio.name = filename

    try:
        user_text = transcribe_audio_in_memory(in_memory_audio, filename)
        print("Transcription result:", user_text)
        # 3. Preparar el estado inicial para LangGraph
        # Por ejemplo, si el usuario está practicando cómo pedir un café en alemán, 
        # aquí pasas la transcripción y el ID de la lección para recuperar el contexto.
        initial_state = {
            "messages": [("user", user_text)],
            "lesson_id": lesson_id
            # "language": "de" (si lo manejas en el estado)
        }
        
        # 4. Invocar tu agente (LangGraph)
        # config={"configurable": {"thread_id": "..."}} es útil si usas memoria en LangGraph
        # resultado_grafo = mi_grafo_de_estudio.invoke(initial_state)
        
        # Asumiendo que tu grafo devuelve un estado donde el último mensaje es del AI
        # respuesta_ia = resultado_grafo["messages"][-1].content

        # 5. Retornar al frontend
        return jsonify({
            "status": "success",
            "transcription": user_text,
            "ai_response": None
        }), 200

    except Exception as e:
        # Aquí puedes usar tu logger preferido
        print(f"Error procesando audio: {e}")
        return jsonify({"error": "Hubo un error procesando el audio."}), 500