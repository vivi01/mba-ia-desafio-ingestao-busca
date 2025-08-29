from search import search_prompt


def main():
    print("Pergunte algo sobre o conteúdo do PDF (ou 'sair' para encerrar):")
    contexto = ""  # Placeholder: in real use, load context from vector DB
    while True:
        pergunta = input("Usuário: ")
        if pergunta.lower() == 'sair':
            break
        resposta = search_prompt(pergunta=pergunta)
        print("Assistente:", resposta)

if __name__ == "__main__":
    main()