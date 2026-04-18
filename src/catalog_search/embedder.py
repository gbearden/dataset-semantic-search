"""
Sentence-transformer wrapper for biomedical embeddings.

Model priority:
  1. pritamdeka/S-PubMedBert-MS-MARCO  – PubMedBERT fine-tuned for semantic search
  2. allenai/scibert_scivocab_uncased   – SciBERT (general sci/bio vocabulary)
  3. sentence-transformers/all-MiniLM-L6-v2 – lightweight fallback
"""

from __future__ import annotations

import logging
from typing import Sequence

import numpy as np
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

# Ordered list: first model that loads successfully is used.
_MODEL_PRIORITY = [
    "pritamdeka/S-PubMedBert-MS-MARCO",
    "allenai/scibert_scivocab_uncased",
    "sentence-transformers/all-MiniLM-L6-v2",
]

_DEFAULT_BATCH = 64


class BiomedEmbedder:
    """Wraps a sentence-transformer model and exposes a single ``encode`` method."""

    def __init__(self, model_name: str | None = None, device: str = "cpu") -> None:
        self._model_name = model_name
        self._device = device
        self._model: SentenceTransformer | None = None

    # ── lazy load ───────────────────────────────────────────────────────────

    @property
    def model(self) -> SentenceTransformer:
        if self._model is None:
            self._model = self._load()
        return self._model

    def _load(self) -> SentenceTransformer:
        candidates = [self._model_name] if self._model_name else _MODEL_PRIORITY
        for name in candidates:
            try:
                logger.info("Loading embedding model: %s", name)
                m = SentenceTransformer(name, device=self._device)
                self._model_name = name
                dim = m.get_embedding_dimension() if hasattr(m, "get_embedding_dimension") else m.get_sentence_embedding_dimension()
                logger.info("Loaded: %s  (dim=%d)", name, dim)
                return m
            except Exception as exc:
                logger.warning("Could not load %s: %s", name, exc)
        raise RuntimeError(
            "No embedding model could be loaded. "
            "Ensure at least one of the following is downloadable: "
            + ", ".join(_MODEL_PRIORITY)
        )

    # ── public API ───────────────────────────────────────────────────────────

    @property
    def model_name(self) -> str:
        """Name of the model that was actually loaded (resolved after first call)."""
        _ = self.model  # trigger lazy load
        return self._model_name  # type: ignore[return-value]

    @property
    def dim(self) -> int:
        m = self.model
        if hasattr(m, "get_embedding_dimension"):
            return m.get_embedding_dimension()
        return m.get_sentence_embedding_dimension()

    def encode(
        self,
        texts: str | Sequence[str],
        batch_size: int = _DEFAULT_BATCH,
        normalize: bool = True,
        show_progress: bool = False,
    ) -> np.ndarray:
        """Encode text(s) → float32 array of shape (n, dim) or (dim,) for a single string.

        When ``normalize=True`` (default) vectors are L2-normalised so that
        inner-product == cosine similarity.
        """
        single = isinstance(texts, str)
        if single:
            texts = [texts]

        vectors = self.model.encode(
            list(texts),
            batch_size=batch_size,
            normalize_embeddings=normalize,
            show_progress_bar=show_progress,
            convert_to_numpy=True,
        )
        return vectors[0] if single else vectors  # type: ignore[return-value]
