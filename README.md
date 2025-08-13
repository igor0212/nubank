# Como executar a main?

Para chamar o método main no prompt (terminal), execute o comando abaixo a partir da raiz do projeto:

    python -m src.main.main

Depois, cole as listas JSON (uma por linha) e pressione Ctrl+D (Linux/Mac) ou Ctrl+Z seguido de Enter (Windows) para finalizar a entrada.


# Como executar os testes unitários?

Execute a partir da raiz do projeto:

Para rodar todos os testes:

    python -m unittest discover -s src/test -p "*.py"

Para rodar um teste específico:

    python -m src.test.service.OperationServiceTest

