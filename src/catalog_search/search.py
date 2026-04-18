"""
CatalogSearch — the main entry point.

Strategy
--------
1. Embed the query with BiomedEmbedder.
2. Run FAISS semantic search.
3. If the top-1 cosine score < SEMANTIC_CONFIDENCE_THRESHOLD:
   - Run BM25 keyword search as fallback.
   - Return BM25 results if they beat the semantic set; otherwise blend.
4. Tag every result with the method used.

Confidence threshold is configurable (default 0.35).
"""

from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Sequence

import numpy as np

from .bm25 import BM25Index
from .embedder import BiomedEmbedder
from .index import CatalogIndex
from .models import Dataset, SearchResult

logger = logging.getLogger(__name__)

SEMANTIC_CONFIDENCE_THRESHOLD = 0.35


class CatalogSearch:
    """Hybrid semantic + BM25 search engine for a health dataset catalog."""

    def __init__(
        self,
        datasets: list[Dataset],
        embedder: BiomedEmbedder,
        catalog_index: CatalogIndex,
        confidence_threshold: float = SEMANTIC_CONFIDENCE_THRESHOLD,
    ) -> None:
        self._datasets = datasets
        self._embedder = embedder
        self._faiss = catalog_index
        self._bm25 = BM25Index(datasets)
        self._threshold = confidence_threshold

    # ── factory methods ──────────────────────────────────────────────────────

    @classmethod
    def build(
        cls,
        datasets: list[Dataset],
        model_name: str | None = None,
        device: str = "cpu",
        confidence_threshold: float = SEMANTIC_CONFIDENCE_THRESHOLD,
        show_progress: bool = True,
    ) -> "CatalogSearch":
        """Build a new index from a list of datasets.

        Parameters
        ----------
        datasets:
            The catalog to index.
        model_name:
            Sentence-transformer model name.  ``None`` uses the priority list
            in :mod:`catalog_search.embedder`.
        device:
            ``'cpu'`` or ``'cuda'``.
        """
        embedder = BiomedEmbedder(model_name=model_name, device=device)
        texts = [d.searchable_text() for d in datasets]
        logger.info("Embedding %d documents …", len(texts))
        t0 = time.perf_counter()
        vectors = embedder.encode(texts, show_progress=show_progress)
        elapsed = time.perf_counter() - t0
        logger.info("Embedding done in %.1fs  (model=%s)", elapsed, embedder.model_name)
        catalog_index = CatalogIndex(datasets, vectors)
        return cls(datasets, embedder, catalog_index, confidence_threshold)

    @classmethod
    def from_index(
        cls,
        index_dir: str | Path,
        model_name: str | None = None,
        device: str = "cpu",
        confidence_threshold: float = SEMANTIC_CONFIDENCE_THRESHOLD,
    ) -> "CatalogSearch":
        """Load a pre-built index from *index_dir*."""
        catalog_index = CatalogIndex.load(index_dir)
        embedder = BiomedEmbedder(model_name=model_name, device=device)
        return cls(
            catalog_index.datasets,
            embedder,
            catalog_index,
            confidence_threshold,
        )

    def save_index(self, index_dir: str | Path) -> None:
        """Persist the FAISS index and document store to *index_dir*."""
        self._faiss.save(index_dir)

    # ── search ───────────────────────────────────────────────────────────────

    def search(
        self,
        query: str,
        top_k: int = 10,
        force_method: str | None = None,
    ) -> list[SearchResult]:
        """Search the catalog.

        Parameters
        ----------
        query:
            Free-text natural language query.
        top_k:
            Maximum number of results to return.
        force_method:
            ``'semantic'`` | ``'bm25'`` | ``None`` (auto).

        Returns
        -------
        list[SearchResult]
            Ranked results with scores and method labels.
            Never returns an empty list as long as the catalog is non-empty.
        """
        if not query.strip():
            return []

        t0 = time.perf_counter()

        if force_method == "bm25":
            results = self._bm25_search(query, top_k)
        elif force_method == "semantic":
            results = self._semantic_search(query, top_k)
        else:
            results = self._hybrid_search(query, top_k)

        elapsed_ms = (time.perf_counter() - t0) * 1000
        logger.debug(
            "query=%r  method=%s  n=%d  top_score=%.3f  elapsed=%.1fms",
            query,
            results[0].method if results else "none",
            len(results),
            results[0].score if results else 0.0,
            elapsed_ms,
        )
        return results

    # ── internals ───────────────────────────────────────────────────────────

    def _hybrid_search(self, query: str, top_k: int) -> list[SearchResult]:
        """Run semantic first; fall back to BM25 when confidence is low."""
        sem_results = self._semantic_search(query, top_k)
        top_score = sem_results[0].score if sem_results else 0.0

        if top_score >= self._threshold:
            return sem_results

        # Low-confidence semantic — try BM25
        logger.debug(
            "Semantic top score %.3f < threshold %.3f — activating BM25 fallback",
            top_score,
            self._threshold,
        )
        bm25_results = self._bm25_search(query, top_k)

        if not bm25_results:
            # BM25 also found nothing: return semantic results as-is
            return sem_results

        # Tag all BM25 results as fallback and prefer them over low-confidence semantic
        for r in bm25_results:
            object.__setattr__(r, "method", "bm25")
        return bm25_results

    def _semantic_search(self, query: str, top_k: int) -> list[SearchResult]:
        q_vec = self._embedder.encode(query, normalize=True)
        hits = self._faiss.search(q_vec, top_k=top_k)
        return [
            SearchResult(
                dataset=hit.dataset,
                score=hit.score,
                method="semantic",
                rank=rank,
            )
            for rank, hit in enumerate(hits, start=1)
        ]

    def _bm25_search(self, query: str, top_k: int) -> list[SearchResult]:
        hits = self._bm25.search(query, top_k=top_k)
        if not hits:
            return []
        # Normalise BM25 scores to [0, 1] relative to the top hit
        max_score = hits[0].score if hits[0].score > 0 else 1.0
        return [
            SearchResult(
                dataset=hit.dataset,
                score=hit.score / max_score,
                method="bm25",
                rank=rank,
            )
            for rank, hit in enumerate(hits, start=1)
        ]

    # ── convenience ──────────────────────────────────────────────────────────

    @property
    def catalog_size(self) -> int:
        return len(self._datasets)

    @property
    def model_name(self) -> str:
        return self._embedder.model_name
