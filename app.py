"""Tradução de inglês para francês com o modelo Helsinki-NLP."""
from functools import lru_cache

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

MODELO = "Helsinki-NLP/opus-mt-en-fr"
app = FastAPI(title="Tradutor Inglês-Francês", version="1.0")


class Entrada(BaseModel):
    texto: str = Field(min_length=1, max_length=10000)

    @field_validator("texto")
    @classmethod
    def validar_texto(cls, valor: str) -> str:
        if not valor.strip():
            raise ValueError("Informe um texto em inglês.")
        return valor.strip()


@lru_cache(maxsize=1)
def obter_tradutor():
    from transformers import pipeline

    return pipeline("translation", model=MODELO)


def dividir_em_blocos(texto: str, tokenizer, limite: int = 220) -> list[str]:
    """Divide texto extenso em grupos de tokens para evitar truncamentos."""
    tokens = tokenizer.encode(texto, add_special_tokens=False)
    return [
        tokenizer.decode(tokens[i:i + limite], skip_special_tokens=True)
        for i in range(0, len(tokens), limite)
    ]


@app.get("/")
def inicio():
    return {"mensagem": "Use POST /traduzir para traduzir inglês para francês."}


@app.post("/traduzir")
def traduzir(entrada: Entrada):
    try:
        tradutor = obter_tradutor()
        partes = dividir_em_blocos(entrada.texto, tradutor.tokenizer)
        traducoes = [
            tradutor(parte, max_new_tokens=300)[0]["translation_text"].strip()
            for parte in partes
        ]
    except Exception as erro:
        raise HTTPException(status_code=503, detail="Falha na tradução local.") from erro

    return {
        "texto_original": entrada.texto,
        "texto_traduzido": " ".join(traducoes),
        "idioma_origem": "en",
        "idioma_destino": "fr",
        "modelo": MODELO,
    }
