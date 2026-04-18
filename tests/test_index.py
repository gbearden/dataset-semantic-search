"""Unit tests for CatalogIndex (FAISS wrapper)."""

import tempfile
from pathlib import Path

import numpy as np
import pytest

from catalog_search.index import CatalogIndex
from catalog_search.models import Dataset


def _make_vectors(n: int, dim: int, seed: int = 42) -> np.ndarray:
    rng = np.random.default_rng(seed)
    v = rng.standard_normal((n, dim)).astype(np.float32)
    # L2-normalise
    norms = np.linalg.norm(v, axis=1, keepdims=True)
    return v / norms


def _make_datasets(n: int) -> list[Dataset]:
    return [Dataset(id=f"DS-{i:03d}", title=f"Dataset {i}", description=f"Desc {i}") for i in range(n)]


class TestCatalogIndexBuild:
    def test_size_equals_n(self):
        n = 10
        ds = _make_datasets(n)
        vecs = _make_vectors(n, 32)
        idx = CatalogIndex(ds, vecs)
        assert idx.size == n

    def test_dim_stored_correctly(self):
        ds = _make_datasets(5)
        vecs = _make_vectors(5, 64)
        idx = CatalogIndex(ds, vecs)
        assert idx.dim == 64

    def test_mismatched_lengths_raise(self):
        with pytest.raises(ValueError, match="same length"):
            CatalogIndex(_make_datasets(3), _make_vectors(4, 16))


class TestCatalogIndexSearch:
    def test_returns_top_k_results(self, small_index):
        q = np.random.default_rng(0).standard_normal(small_index.dim).astype(np.float32)
        q /= np.linalg.norm(q)
        hits = small_index.search(q, top_k=3)
        assert len(hits) == 3

    def test_results_sorted_descending(self, small_index):
        q = np.random.default_rng(1).standard_normal(small_index.dim).astype(np.float32)
        q /= np.linalg.norm(q)
        hits = small_index.search(q, top_k=5)
        scores = [h.score for h in hits]
        assert scores == sorted(scores, reverse=True)

    def test_self_query_returns_itself_first(self, small_catalog, mock_embedder):
        """Embedding a document and querying should return that document as rank-1."""
        target = small_catalog[0]
        texts = [d.searchable_text() for d in small_catalog]
        vecs = mock_embedder.encode(texts)
        idx = CatalogIndex(small_catalog, vecs)
        q = mock_embedder.encode(target.searchable_text())
        hits = idx.search(q, top_k=5)
        assert hits[0].dataset.id == target.id

    def test_top_k_capped_at_corpus_size(self, small_index):
        q = np.random.default_rng(2).standard_normal(small_index.dim).astype(np.float32)
        q /= np.linalg.norm(q)
        hits = small_index.search(q, top_k=1000)
        # Should not exceed corpus size
        assert len(hits) <= small_index.size


class TestCatalogIndexPersistence:
    def test_save_and_reload(self, small_catalog, mock_embedder):
        texts = [d.searchable_text() for d in small_catalog]
        vecs = mock_embedder.encode(texts)
        idx = CatalogIndex(small_catalog, vecs)

        with tempfile.TemporaryDirectory() as tmp:
            idx.save(tmp)
            assert CatalogIndex.exists(tmp)
            loaded = CatalogIndex.load(tmp)

        assert loaded.size == idx.size
        assert loaded.dim == idx.dim
        # Dataset ids should match
        orig_ids = {d.id for d in idx.datasets}
        loaded_ids = {d.id for d in loaded.datasets}
        assert orig_ids == loaded_ids

    def test_exists_returns_false_on_empty_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            assert not CatalogIndex.exists(tmp)
