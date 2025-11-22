from langchain.agents.middleware import dynamic_prompt, ModelRequest
from langchain.agents import create_agent
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

vector_store = Chroma(
    collection_name="langchain",
    embedding_function=embeddings,
    persist_directory="./chroma_db",
)

llm = init_chat_model("gemini-2.5-flash-lite", model_provider="google_genai", temperature=0)

@dynamic_prompt
def prompt_with_context(request: ModelRequest) -> str:
    """Inject context into state messages."""
    last_query = request.state["messages"][-1].text
    retrieved_docs = vector_store.similarity_search(last_query)

    docs_content = "\n\n".join(doc.page_content for doc in retrieved_docs)

    system_message = SystemMessage(content=f"You are a helpful assistant. Use the following context in your response: {docs_content}")

    return system_message

agent = create_agent(llm, tools=[], middleware=[prompt_with_context])

query = "Faça um resumo dos À JUSTIÇA E INTELIGÊNCIA ARTIFICIAL?"

result = agent.invoke({"messages": [HumanMessage(query)]})
print(result["messages"][-1].content)