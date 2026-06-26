from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from app.agents.support.nodes.speach_evaluator.prompt import prompt_template


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.45)


def evaluate_text(
    original_text: str,
    corrected_text: str,
    language_learning: str,
    language_native: str,
    level: str,
) -> str:
    chain = prompt_template | llm | StrOutputParser()
    response = chain.invoke(
        {
            "original_text": original_text,
            "corrected_text": corrected_text,
            "language_learning": language_learning,
            "language_native": language_native,
            "level": level,
        }
    )
    return response.strip()


__all__ = ["evaluate_text"]
