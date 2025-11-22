

# Configuração de chaves de API
from google.colab import userdata
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

pdf_path = "/content/TCC - João Vítor Café.pdf"
loader = PyPDFLoader(pdf_path)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
chunks = text_splitter.split_documents(docs)

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vector_store = Chroma(
    collection_name="langchain",
    embedding_function=embeddings,
    persist_directory="./chroma_db",
)

ids = vector_store.add_documents(chunks, ids=[f"file_{i}" for i in range(len(chunks))])
print("IDs dos documentos adicionados: ", ids)

# total_docs = vector_store.similarity_search(" ", k=99999)
# print("Total de documentos encontrados: ", len(total_docs))

# print("Primeiro documento encontrado: ", total_docs[0])