from langchain.agents import create_agent
from langchain_openai import ChatOpenAI


from app.agents.support.nodes.speach_evaluator.prompt import prompt_template


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)
booking_node = create_agent(
    model=llm,
    # tools=tools,
    system_prompt=prompt_template.format()
)