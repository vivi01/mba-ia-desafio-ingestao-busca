import os
from pydantic import SecretStr
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres.vectorstores import PGVector
from langchain_core.documents import Document

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")
PGVECTOR_URL = os.getenv("PGVECTOR_URL", "postgresql://postgres:postgres@localhost:5432/rag")
PGVECTOR_COLLECTION = os.getenv("PGVECTOR_COLLECTION", "pdf_chunks")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def ingest_pdf():
  if not PDF_PATH or not os.path.exists(PDF_PATH):
    print(f"PDF_PATH '{PDF_PATH}' is not set or file does not exist.")
    return

  docs = PyPDFLoader(str(PDF_PATH)).load()

  splits = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150,
    add_start_index=False
  ).split_documents(docs)

  if not splits:
    raise SystemExit(0)

  enriched = [
    Document(
      page_content=d.page_content,
      metadata={k: v for k, v in d.metadata.items() if v not in ("", None)}
    )
    for d in splits
  ]

  ids = [f"doc-{i}" for i in range(len(enriched))]

  embeddings = GoogleGenerativeAIEmbeddings(model="text-embedding-3-small")

  collection_name = os.getenv("PGVECTOR_COLLECTION") or "pdf_chunks"
  connection_url = os.getenv("PGVECTOR_URL") or "postgresql://postgres:postgres@localhost:5432/rag"

  store = PGVector(
    embeddings=embeddings,
    collection_name=collection_name,
    connection=connection_url,
    use_jsonb=True,
  )

  store.add_documents(documents=enriched, ids=ids)

if __name__ == "__main__":
    ingest_pdf()