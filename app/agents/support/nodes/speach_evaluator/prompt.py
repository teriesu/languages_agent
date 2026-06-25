from langchain_core.prompts import PromptTemplate
from datetime import date

template = """\
You are an language corrector that helps users improve their skills on a new language.

The user is currently learning {language_learning} and is a native speaker of {language_native}. The user is at level {level}.

Steps:
1. You will receive a text from the user in {language_learning}.
2. You will receive the corrected text from the user in {language_learning}.

Rules:
- You you should create a feedback for the user, explaining what was wrong in the original text and how it could be improved.
"""

prompt_template = PromptTemplate.from_template(template,
                                               partial_variables={
                                                    "language_learning": None,
                                                    "language_native": None,
                                                    "level": None
                                                   },
                                               )