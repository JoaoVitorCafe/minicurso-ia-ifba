from urllib.parse import quote
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from urllib.parse import quote
from langchain_classic.indexes import SQLRecordManager, index
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgres"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5433"
POSTGRES_DATABASE = "DB_IFBA"

conn_string = f"postgresql://{POSTGRES_USER}:{quote(POSTGRES_PASSWORD)}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"

COLLECTION_NAME = "COLLECTION_IFBA"

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

pdf_path = r".\pdfs\ACESSO À JUSTIÇA E INTELIGÊNCIA ARTIFICIAL.pdf"
loader = PyPDFLoader(pdf_path)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
chunks = text_splitter.split_documents(docs)

vector_store = PGVector(
    embeddings=embeddings,
    collection_name=COLLECTION_NAME,
    connection=conn_string,
    use_jsonb=True,
)

CHAT_HISTORY_TABLE_NAME = "CHAT_HISTORY_IFBA"

namespace = f"pgvector/{COLLECTION_NAME}"
record_manager = SQLRecordManager(namespace, db_url=conn_string)
record_manager.create_schema()

results = index(
    chunks,
    record_manager,
    vector_store,
    cleanup="incremental",
    source_id_key="source",
)

print(results)
