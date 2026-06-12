import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Tuple, Optional
import streamlit as st
import pickle
import os


@st.cache_resource
def _load_embedding_model(model_name: str) -> SentenceTransformer:
    """Load the sentence-transformer model once and cache across reruns.

    Using st.cache_resource keeps the heavy model out of session_state so
    Streamlit never tries to pickle/copy it across script reruns — which
    would cause a segfault on macOS due to forked torch/OpenMP threads.
    """
    return SentenceTransformer(model_name)


# Module-level constant so every VectorStore instance shares one model
_EMBEDDING_MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"


class VectorStore:
    """Manages document embeddings with sentence-transformers and FAISS.

    IMPORTANT: The SentenceTransformer model is intentionally **not** stored
    as an instance attribute.  Storing it would mean Streamlit's session_state
    tries to pickle a torch model on every rerun, which causes segfaults on
    macOS.  Instead we fetch it from the cache each time we need it.
    """

    def __init__(self, api_key: str = None):
        """Initialize the vector store (lightweight — no model reference)."""
        # Trigger model download/cache on first call so the user sees progress
        _load_embedding_model(_EMBEDDING_MODEL_NAME)

        self.dimension: int = 768  # all-mpnet-base-v2 always produces 768-d
        self.index = faiss.IndexFlatL2(self.dimension)
        self.texts: List[str] = []
        self.metadata: List[dict] = []

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _get_model() -> SentenceTransformer:
        """Return the cached model (never stored on self)."""
        return _load_embedding_model(_EMBEDDING_MODEL_NAME)

    def _get_embeddings(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings with the sentence-transformers model."""
        try:
            model = self._get_model()
            embeddings = []

            batch_size = 100
            for i in range(0, len(texts), batch_size):
                batch = texts[i : i + batch_size]

                batch_embeddings = model.encode(
                    batch,
                    convert_to_numpy=True,
                    normalize_embeddings=True,
                )

                if batch_embeddings.ndim == 1:
                    batch_embeddings = batch_embeddings.reshape(1, -1)

                embeddings.extend(batch_embeddings.tolist())

            return np.array(embeddings, dtype=np.float32)

        except Exception as e:
            st.error(f"Error generating embeddings: {str(e)}")
            return np.array([])

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def add_documents(
        self, texts: List[str], metadata: Optional[List[dict]] = None
    ) -> bool:
        """Add document chunks to the vector store."""
        if not texts:
            return False

        try:
            with st.spinner("Creating embeddings with sentence-transformers…"):
                embeddings = self._get_embeddings(texts)

            if embeddings.size == 0:
                st.error("Failed to generate embeddings")
                return False

            self.index.add(embeddings)

            self.texts.extend(texts)
            if metadata:
                self.metadata.extend(metadata)
            else:
                self.metadata.extend(
                    [{"chunk_id": i + len(self.metadata)} for i in range(len(texts))]
                )

            st.success(f"Added {len(texts)} document chunks to vector store")
            return True

        except Exception as e:
            st.error(f"Error adding documents to vector store: {str(e)}")
            return False

    def search(self, query: str, k: int = 5) -> List[Tuple[str, float, dict]]:
        """Search for most relevant document chunks."""
        if self.index.ntotal == 0:
            return []

        try:
            model = self._get_model()
            query_embedding = model.encode(
                [query],
                convert_to_numpy=True,
                normalize_embeddings=True,
            )
            query_embedding = np.array(query_embedding, dtype=np.float32)

            distances, indices = self.index.search(
                query_embedding, min(k, self.index.ntotal)
            )

            results = []
            for distance, idx in zip(distances[0], indices[0]):
                if 0 <= idx < len(self.texts):
                    similarity = 1 / (1 + distance)
                    results.append(
                        (
                            self.texts[idx],
                            similarity,
                            self.metadata[idx] if idx < len(self.metadata) else {},
                        )
                    )

            return results

        except Exception as e:
            st.error(f"Error searching vector store: {str(e)}")
            return []

    def save(self, filepath: str) -> bool:
        """Save the vector store to disk."""
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)

            faiss.write_index(self.index, f"{filepath}.faiss")

            with open(f"{filepath}.pkl", "wb") as f:
                pickle.dump(
                    {
                        "texts": self.texts,
                        "metadata": self.metadata,
                        "dimension": self.dimension,
                    },
                    f,
                )

            return True
        except Exception as e:
            st.error(f"Error saving vector store: {str(e)}")
            return False

    def load(self, filepath: str) -> bool:
        """Load the vector store from disk."""
        try:
            if not os.path.exists(f"{filepath}.faiss") or not os.path.exists(
                f"{filepath}.pkl"
            ):
                return False

            self.index = faiss.read_index(f"{filepath}.faiss")

            with open(f"{filepath}.pkl", "rb") as f:
                data = pickle.load(f)
                self.texts = data["texts"]
                self.metadata = data["metadata"]
                self.dimension = data["dimension"]

            return True
        except Exception as e:
            st.error(f"Error loading vector store: {str(e)}")
            return False

    def clear(self) -> None:
        """Clear the vector store."""
        self.index = faiss.IndexFlatL2(self.dimension)
        self.texts = []
        self.metadata = []

    def get_stats(self) -> dict:
        """Get statistics about the vector store."""
        return {
            "total_chunks": len(self.texts),
            "index_size": self.index.ntotal,
            "dimension": self.dimension,
        }