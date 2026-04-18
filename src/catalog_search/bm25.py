"""
BM25 keyword search — used as a fallback when semantic confidence is low.
"""

from __future__ import annotations

import re
from typing import NamedTuple

from rank_bm25 import BM25Okapi

from .models import Dataset


def _tokenise(text: str) -> list[str]:
    """Lowercase and split on non-alphanumeric characters."""
    return [tok for tok in re.split(r"\W+", text.lower()) if tok]


class BM25Hit(NamedTuple):
    dataset: Dataset
    score: float  # raw BM25 score (not normalised)


class BM25Index:
    """Thin wrapper around rank-bm25's BM25Okapi."""

    def __init__(self, datasets: list[Dataset]) -> None:
        self._datasets = datasets
        corpus = [_tokenise(d.searchable_text()) for d in datasets]
        self._bm25 = BM25Okapi(corpus)

    def search(self, query: str, top_k: int = 10) -> list[BM25Hit]:
        tokens = _tokenise(query)
        if not tokens:
            return []
        scores = self._bm25.get_scores(tokens)
        # Sort descending; exclude zero-score documents
        ranked = sorted(
            ((score, i) for i, score in enumerate(scores) if score > 0),
            reverse=True,
        )
        return [
            BM25Hit(dataset=self._datasets[i], score=float(s))
            for s, i in ranked[:top_k]
        ]

    @property
    def max_possible_score(self) -> float:
        """A rough upper-bound used for normalisation (max observed idf * k1+1)."""
        # In practice we normalise in CatalogSearch rather than here
        return float(max(self._bm25.idf.values(), default=1.0)) * (
            self._bm25.k1 + 1
        )
