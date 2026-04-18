"""
FAISS index management: build, save, load, and search.

Index type: ``IndexFlatIP`` (exact inner-product search).
Because embeddings are L2-normalised by BiomedEmbedder, inner product
equals cosine similarity.  No approximation is introduced for this corpus
size (≤ 100k entries); switch to IndexHNSWFlat for larger corpora.
"""

from __future__ import annotations

import json
import logging
import pickle
from pathlib import Path
from typing import NamedTuple

import faiss
import numpy as np

from .models import Dataset

logger = logging.getLogger(__name__)

_INDEX_FILE = "faiss.index"
_DOCS_FILE = "documents.pkl"
_META_FILE = "index_meta.json"


class IndexHit(NamedTuple):
    dataset: Dataset
    score: float  # cosine similarity in [-1, 1]; higher is better


class CatalogIndex:
    """Wraps a FAISS index together with the document store."""

    def __init__(self, datasets: list[Dataset], vectors: np.ndarray) -> None:
        if len(datasets) != vectors.shape[0]:
            raise ValueError(
                f"datasets ({len(datasets)}) and vectors ({vectors.shape[0]}) must have the same length"
            )
        self._datasets = datasets
        self._dim = vectors.shape[1]
        self._index = self._build_faiss(vectors)

    # ── build ────────────────────────────────────────────────────────────────

    @staticmethod
    def _build_faiss(vectors: np.ndarray) -> faiss.IndexFlatIP:
        dim = vectors.shape[1]
        index = faiss.IndexFlatIP(dim)
        # FAISS expects float32 row-major
        index.add(vectors.astype(np.float32))
        logger.info("FAISS index built: %d vectors, dim=%d", index.ntotal, dim)
        return index

    # ── persistence ──────────────────────────────────────────────────────────

    def save(self, directory: str | Path) -> None:
        d = Path(directory)
        d.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self._index, str(d / _INDEX_FILE))
        with open(d / _DOCS_FILE, "wb") as f:
            pickle.dump(self._datasets, f)
        meta = {"n": len(self._datasets), "dim": self._dim}
        with open(d / _META_FILE, "w") as f:
            json.dump(meta, f)
        logger.info("Index saved to %s (%d docs)", d, len(self._datasets))

    @classmethod
    def load(cls, directory: str | Path) -> "CatalogIndex":
        d = Path(directory)
        index = faiss.read_index(str(d / _INDEX_FILE))
        with open(d / _DOCS_FILE, "rb") as f:
            datasets: list[Dataset] = pickle.load(f)
        obj = cls.__new__(cls)
        obj._datasets = datasets
        obj._dim = index.d
        obj._index = index
        logger.info("Index loaded from %s (%d docs, dim=%d)", d, len(datasets), index.d)
        return obj

    @classmethod
    def exists(cls, directory: str | Path) -> bool:
        d = Path(directory)
        return (d / _INDEX_FILE).exists() and (d / _DOCS_FILE).exists()

    # ── search ───────────────────────────────────────────────────────────────

    def search(self, query_vector: np.ndarray, top_k: int = 10) -> list[IndexHit]:
        """Return up to *top_k* results sorted by descending cosine similarity."""
        q = query_vector.astype(np.float32).reshape(1, -1)
        scores, indices = self._index.search(q, min(top_k, self._index.ntotal))
        results: list[IndexHit] = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            results.append(IndexHit(dataset=self._datasets[idx], score=float(score)))
        return results

    # ── properties ───────────────────────────────────────────────────────────

    @property
    def size(self) -> int:
        return self._index.ntotal

    @property
    def dim(self) -> int:
        return self._dim

    @property
    def datasets(self) -> list[Dataset]:
        return list(self._datasets)
