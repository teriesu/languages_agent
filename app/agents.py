from dataclasses import dataclass
from typing import Iterable

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
