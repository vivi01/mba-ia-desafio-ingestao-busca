# Desafio MBA Engenharia de Software com IA - Full Cycle

## Visão Geral
Este projeto realiza ingestão de documentos PDF e busca semântica via chat CLI, utilizando LangChain, PostgreSQL com pgVector e embeddings Gemini.

## Requisitos
- Python 3.10+
- Docker e Docker Compose
- Chave de API Google Gemini (defina em `.env`)

## Setup do Ambiente
1. Clone o repositório e acesse a pasta do projeto.
2. Crie e ative o ambiente virtual:
	- Windows: `python -m venv venv && venv\Scripts\activate`
	- Unix: `python3 -m venv venv && source venv/bin/activate`
3. Instale as dependências:
	- `pip install -r requirements.txt`
4. Configure o arquivo `.env` com:
	- `PDF_PATH=document.pdf`
	- `GOOGLE_API_KEY=...` (sua chave Gemini)
	- `PGVECTOR_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag`
	- `PGVECTOR_COLLECTION=pdf_chunks`
	- `OPENAI_MODEL=text-embedding-3-small`

## Subindo o Banco de Dados
```
docker compose up -d
```
O banco ficará disponível em `localhost:5432` (user: postgres, senha: postgres, db: rag).

## Ingestão do PDF
```
python src/ingest.py
```
O PDF será dividido em chunks de 1000 caracteres (overlap 150), vetorizado e armazenado no banco vetorial.

## Chat CLI (Busca Semântica)
```
python src/chat.py
```
Digite sua pergunta e o sistema buscará os 10 trechos mais relevantes no banco, montará o prompt e retornará a resposta baseada apenas no PDF.

## Arquitetura
- `src/ingest.py`: Ingestão do PDF, chunking, embeddings e armazenamento vetorial.
- `src/search.py`: Busca semântica, montagem do prompt e fallback.
- `src/chat.py`: Interface de chat via terminal.
- `docker-compose.yml`: Banco PostgreSQL com pgVector.

## Observações
- O sistema responde apenas com base no PDF. Se a resposta não estiver no contexto, retorna: "Não tenho informações necessárias para responder sua pergunta."
- Prompt e regras seguem o template do desafio.

## Exemplo de Uso
Pergunta: Qual o faturamento da Empresa SuperTechIABrazil?
Resposta: O faturamento foi de 10 milhões de reais.

Pergunta: Quantos clientes temos em 2024?
Resposta: Não tenho informações necessárias para responder sua pergunta.