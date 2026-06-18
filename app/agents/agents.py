import os
from dataclasses import dataclass
from dotenv import load_dotenv
from typing import Iterable
from langchain_openai import ChatOpenAI
from openai import OpenAI
from langsmith import traceable
from pydub import AudioSegment

import io

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@traceable(run_type="tool", name="Whisper_STT")
def transcribe_audio_in_memory(audio_bytes: io.BytesIO, filename: str) -> str:
    """Filtra un poco la señal de ruido de fondo y devuelve la transcripción."""
    
    audio_bytes.seek(0)
    audio = AudioSegment.from_file(audio_bytes)
    audio = audio.set_frame_rate(16000)
    audio_louder = audio

    louder_buffer = io.BytesIO()
    audio_louder.export(louder_buffer, format="webm")
    louder_buffer.seek(0)
    louder_buffer.name = filename 
    
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=louder_buffer,
        language="de"
    )
    return transcription.text

try:
    from langchain.chains import LLMChain
    from langchain.llms import OpenAI
except ImportError:  # pragma: no cover - placeholder imports for future wiring
    LLMChain = None  # type: ignore
    OpenAI = None  # type: ignore

try:
    from langgraph import LangGraph
except ImportError:  # pragma: no cover
    LangGraph = None  # type: ignore

try:
    from lagsmith import Lagsmith
except ImportError:  # pragma: no cover
    Lagsmith = None  # type: ignore


@dataclass
class AgentResult:
    title: str
    message: str


def _simple_prompt(prefix: str, user_input: str, lesson_title: str | None) -> str:
    base = f"[{prefix}]" + (f" Lesson: {lesson_title}." if lesson_title else "")
    return f"{base} User asked: {user_input}" if user_input else base


def review_agent(user_query: str, lesson_title: str | None) -> AgentResult:
    return AgentResult(
        title="Review",
        message=_simple_prompt("Review agent", user_query, lesson_title),
    )


def explanation_agent(user_query: str, lesson_title: str | None) -> AgentResult:
    return AgentResult(
        title="Explain",
        message=_simple_prompt("Explanation agent", user_query, lesson_title),
    )


def correction_agent(user_query: str, lesson_title: str | None) -> AgentResult:
    return AgentResult(
        title="Correction",
        message=_simple_prompt("Correction agent", user_query, lesson_title),
    )


def evaluation_agent(user_query: str, lesson_title: str | None) -> AgentResult:
    return AgentResult(
        title="Evaluation",
        message=_simple_prompt("Evaluation agent", user_query, lesson_title),
    )


def activity_agent(user_query: str, lesson_title: str | None) -> AgentResult:
    return AgentResult(
        title="Activity",
        message=_simple_prompt("Activity planner", user_query, lesson_title),
    )


def plan_responses(user_query: str, lesson_title: str | None) -> Iterable[AgentResult]:
    if not user_query:
        return []

    return [
        review_agent(user_query, lesson_title),
        explanation_agent(user_query, lesson_title),
        correction_agent(user_query, lesson_title),
        evaluation_agent(user_query, lesson_title),
        activity_agent(user_query, lesson_title),
    ]
