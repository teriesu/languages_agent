from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from app.agents.support.nodes.speach_corrector.prompt import prompt_template


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.25)


def correct_text(user_text: str, language_learning: str, language_native: str, level: str) -> str:
    chain = prompt_template | llm | StrOutputParser()
    response = chain.invoke(
        {
            "user_text": user_text,
            "language_learning": language_learning,
            "language_native": language_native,
            "level": level,
        }
    )
    return response.strip()


__all__ = ["correct_text"]
