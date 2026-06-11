def test_vector_store_uses_huggingface_embedding_model(monkeypatch):
    import vector_store

    captured = {}

    class FakeTransformer:
        def __init__(self, model_name):
            captured['model_name'] = model_name

        def encode(self, texts, convert_to_numpy=True, normalize_embeddings=False):
            captured['texts'] = list(texts)
            return [[0.1, 0.2], [0.3, 0.4]]

    monkeypatch.setattr(vector_store, 'SentenceTransformer', FakeTransformer, raising=False)

    store = vector_store.VectorStore('dummy-key')

    assert store.embedding_model == 'sentence-transformers/all-mpnet-base-v2'
    assert captured['model_name'] == 'sentence-transformers/all-mpnet-base-v2'


def test_chat_handler_uses_requested_llm_name(monkeypatch):
    import chat_handler

    captured = {}

    monkeypatch.setenv('HUGGINGFACE_API_KEY', 'hf-test-key')

    class FakeClient:
        def __init__(self, model, token):
            captured['model'] = model
            captured['token'] = token

    monkeypatch.setattr(chat_handler, 'InferenceClient', FakeClient)

    chat_handler.ChatHandler(None)

    assert captured['model'] == 'meta-llama/Llama-3.1-8B-Instruct'
    assert captured['token'] == 'hf-test-key'
