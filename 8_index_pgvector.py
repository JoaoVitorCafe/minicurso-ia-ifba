from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings

from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()

pdf_path = r".\pdfs\ACESSO À JUSTIÇA E INTELIGÊNCIA ARTIFICIAL.pdf"
loader = PyPDFLoader(pdf_path)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
chunks = text_splitter.split_documents(docs)

POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgres"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5433"
POSTGRES_DATABASE = "DB_IFBA"

conn_string = f"postgresql://{POSTGRES_USER}:{quote(POSTGRES_PASSWORD)}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"

COLLECTION_NAME = "COLLECTION_IFBA"

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

vector_store = PGVector(
    embeddings=embeddings,
    collection_name="COLLECTION_IFBA",
    connection=conn_string,
    use_jsonb=True,
)

ids = vector_store.add_documents(chunks, ids=[f"file_{i}" for i in range(len(chunks))])
print("IDs dos documentos adicionados: ", ids)

total_docs = vector_store.similarity_search(" ", k=99999)
print("Total de documentos encontrados: ", len(total_docs))


print("Primeiro documento encontrado: ", total_docs[0])

page_doc = vector_store.similarity_search(" ", k=99999, filter={"page": 1})
print("Documento da página 1: ", page_doc)

kwargs = {
    "filter": {"page": 1}
}