import pytest

from chat_handler import ChatHandler
from vector_store import VectorStore


def test_vector_store_does_not_require_google_key(monkeypatch):
    monkeypatch.setenv("HUGGINGFACE_API_KEY", "hf-test-key")

    try:
        VectorStore(None)
    except ValueError as exc:
        pytest.fail(f"VectorStore should not require a Google key: {exc}")


def test_chat_handler_uses_huggingface_key(monkeypatch):
    captured = {}

    monkeypatch.setenv("HUGGINGFACE_API_KEY", "hf-test-key")

    class FakeClient:
        def __init__(self, model, token):
            captured["model"] = model
            captured["token"] = token

    monkeypatch.setattr("chat_handler.InferenceClient", FakeClient)

    ChatHandler(None)

    assert captured["model"] == "meta-llama/Llama-3.1-8B-Instruct"
    assert captured["token"] == "hf-test-key"
