from langchain.tools import tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

checkpointer = InMemorySaver()

from langchain.agents.middleware import PIIMiddleware, SummarizationMiddleware

@tool(description="Mock tool to simulate a tool call")
def mock_tool() -> str:
    return f"This is a mock tool call"

prompt = """
Você é um assistente que responde perguntas sobre conhecimentos gerais.
"""

agent = create_agent(
    model="openai:gpt-4.1-2025-04-14", # Modelo demonstrativo
    tools=[],
    system_prompt=prompt,
    middleware=[
        SummarizationMiddleware(
            model="openai:gpt-4o-mini",
            max_tokens_before_summary=200, # Ativa a sumarização quando o texto ultrapassa 200 tokens
            messages_to_keep=5, # Mantém os últimos 5 mensagens após a resumização
        ),
        PIIMiddleware("email", strategy="redact", apply_to_input=True),
    ],
    checkpointer=checkpointer
)

config = {"configurable": {"thread_id": "1"}}

while True:
    user_input = input("> : ")
    if user_input.lower() == "sair":
        break
    response = agent.invoke({
        "messages": [HumanMessage(content=user_input)]},
        config=config
    )
    print(response["messages"][-1].content)