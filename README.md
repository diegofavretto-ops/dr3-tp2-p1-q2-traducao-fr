# Parte 1 - Questão 2: FastAPI com tradução EN-FR

API que recebe um texto em inglês e retorna sua tradução para o francês com o modelo Helsinki-NLP/opus-mt-en-fr da Hugging Face.

Este projeto faz parte do DR3/TP2 da disciplina **Desenvolvimento de Data-Driven Apps com Python**.

## O que foi usado

- **FastAPI** recebe o JSON.
- **transformers.pipeline("translation")** traduz o texto.
- **Tokenizer** ajuda a dividir textos maiores.

## 1. Preparar o ambiente

É recomendado utilizar **Python 3.11 ou 3.12**. No terminal, entre na pasta do projeto e execute:

**Windows (PowerShell):**

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Se `py -3.11` não estiver disponível, utilize `python -m venv .venv` com uma versão compatível.

**Linux/macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 2. Executar a API

```bash
uvicorn app:app --reload
```

Depois, acesse a documentação automática do FastAPI: **http://127.0.0.1:8000/docs**.

## 2.1. Exemplo de requisição

**POST** `http://127.0.0.1:8000/traduzir`

```json
{"texto": "Hello, my name is Maria. I like studying Python."}
```

A resposta contém `texto_traduzido`, `idioma_origem` (`en`) e `idioma_destino` (`fr`). Para textos longos, a aplicação divide a entrada em blocos de até 220 tokens e une as traduções. Isso evita descartar parte da entrada, mas pode reduzir a qualidade quando uma frase é dividida entre blocos.


## 3. Testar

```bash
pytest -q
```

Os testes automatizados usam **simulações (mocks)** para não baixar modelos nem gastar créditos. Para testar o modelo real, execute a aplicação e faça uma requisição pela página `/docs`.

## Observações

O código é um exercício didático. Os modelos locais precisam ser baixados antes da primeira tradução ou geração. A API da OpenAI exige uma chave válida e pode gerar cobrança. O tempo de resposta depende da máquina, do tamanho do texto e da conexão.

**Importante:** as saídas reais não foram inventadas nem medidas. Os testes usam simulações e verificam o processamento do JSON e das rotas.

**Compatibilidade:** este projeto fixa `transformers<5` em `requirements.txt`, porque a versão 5 removeu o pipeline `translation` utilizado no exercício. A versão 4 continua documentada em https://huggingface.co/docs/transformers/v4.57.1/en/main_classes/pipelines .
