from pydantic import SecretStr
PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

import os
from dotenv import load_dotenv
from langchain_postgres.vectorstores import PGVector
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

PG_CONN_STRING = os.getenv("PGVECTOR_URL", "postgresql://postgres:postgres@localhost:5432/rag")
COLLECTION_NAME = os.getenv("PGVECTOR_COLLECTION", "pdf_chunks")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
EMBEDDING_MODEL = os.getenv("OPENAI_MODEL", "text-embedding-3-small")

def search_prompt(pergunta=None):
  if not pergunta:
    return PROMPT_TEMPLATE.format(contexto="", pergunta="")

  # Retrieve relevant context from vector DB
  if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is not set in the environment.")

  embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL, google_api_key=SecretStr(GOOGLE_API_KEY))

  vectorstore = PGVector(
      collection_name=COLLECTION_NAME,
      connection=PG_CONN_STRING,
      embeddings=embeddings
  )
  # Search for top 10 relevant chunks with scores
  results = vectorstore.similarity_search_with_score(pergunta, k=10)
  contexto = "\n".join([doc.page_content for doc, score in results]) if results else ""

  if not contexto.strip():
    return 'Não tenho informações necessárias para responder sua pergunta.'

  prompt = PROMPT_TEMPLATE.format(contexto=contexto, pergunta=pergunta)
  # In a real implementation, LLM call would go here
  return prompt