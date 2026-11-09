from fastapi.testclient import TestClient

import app as modulo

cliente = TestClient(modulo.app)


class TokenizerFalso:
    def encode(self, texto, add_special_tokens=False):
        return list(texto)

    def decode(self, tokens, skip_special_tokens=True):
        return "".join(tokens)


class TradutorFalso:
    tokenizer = TokenizerFalso()

    def __call__(self, texto, **kwargs):
        return [{"translation_text": "Bonjour"}]


def test_traducao_json(monkeypatch):
    monkeypatch.setattr(modulo, "obter_tradutor", lambda: TradutorFalso())
    resposta = cliente.post("/traduzir", json={"texto": "Hello"})
    assert resposta.status_code == 200
    assert resposta.json()["texto_traduzido"] == "Bonjour"
    assert resposta.json()["idioma_destino"] == "fr"


def test_divisao_de_texto_longo():
    partes = modulo.dividir_em_blocos("a" * 500, TokenizerFalso(), 220)
    assert len(partes) == 3
    assert "".join(partes) == "a" * 500


def test_entrada_vazia():
    assert cliente.post("/traduzir", json={"texto": ""}).status_code == 422
