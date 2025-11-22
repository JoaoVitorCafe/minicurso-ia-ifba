from langchain.agents.middleware import dynamic_prompt, ModelRequest
from langchain.agents import create_agent
from langchain_openai import OpenAIEmbeddings
from langchain.chat_models import init_chat_model

from langchain_postgres import PGVector
from langgraph.checkpoint.postgres import PostgresSaver

from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgres"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5433"
POSTGRES_DATABASE = "DB_IFBA"

conn_string = f"postgresql://{POSTGRES_USER}:{quote(POSTGRES_PASSWORD)}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"

vector_store = PGVector(
    embeddings=embeddings,
    collection_name="COLLECTION_IFBA",
    connection=conn_string,
    use_jsonb=True,
)

llm = init_chat_model("gemini-2.5-flash-lite", model_provider="google_genai", temperature=0)

@dynamic_prompt
def prompt_with_context(request: ModelRequest) -> str:
    """Inject context into state messages."""
    last_query = request.state["messages"][-1].text
    retrieved_docs = vector_store.similarity_search(last_query)

    docs_content = "\n\n".join(doc.page_content for doc in retrieved_docs)

    system_message = (
        "You are a helpful assistant. Use the following context in your response:"
        f"\n\n{docs_content}"
    )

    return system_message


query = "Qual foi a minha pergunta anterior?"
# query = "Faça um resumo dos À JUSTIÇA E INTELIGÊNCIA ARTIFICIAL?"

with PostgresSaver.from_conn_string(conn_string) as checkpointer:
    checkpointer.setup() # auto create tables in PostgresSql
    agent = create_agent(
        llm,
        [],
        middleware=[prompt_with_context],
        checkpointer=checkpointer,  
    )

    result = agent.invoke(
        {"messages": {"role": "user", "content": f"{query}"}},
        {"configurable": {"thread_id": "3"}},  
    )

    print(result["messages"][-1].content)
