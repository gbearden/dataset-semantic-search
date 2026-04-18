"""Unit tests for BM25 keyword search."""

import pytest

from catalog_search.bm25 import BM25Index, _tokenise
from catalog_search.models import Dataset


class TestTokenise:
    def test_lowercases(self):
        assert "mri" in _tokenise("MRI")

    def test_splits_on_non_alpha(self):
        tokens = _tokenise("type-2 diabetes")
        assert "type" in tokens
        assert "2" in tokens
        assert "diabetes" in tokens

    def test_empty_string(self):
        assert _tokenise("") == []

    def test_removes_empty_tokens(self):
        assert "" not in _tokenise("a  b")


class TestBM25Index:
    @pytest.fixture()
    def index(self, small_catalog):
        return BM25Index(small_catalog)

    def test_exact_keyword_match_returns_result(self, index):
        hits = index.search("MRI neuroimaging", top_k=5)
        assert len(hits) > 0
        ids = [h.dataset.id for h in hits]
        assert "TEST-IMG-001" in ids

    def test_top_ranked_is_most_relevant(self, index):
        """The imaging dataset should rank above diabetes for 'MRI brain'."""
        hits = index.search("MRI brain imaging", top_k=5)
        assert hits[0].dataset.id == "TEST-IMG-001"

    def test_empty_query_returns_empty(self, index):
        assert index.search("", top_k=5) == []

    def test_nonsense_query_returns_empty_or_partial(self, index):
        hits = index.search("xyzzy frobnicate qqqqqq", top_k=5)
        # BM25 returns 0-score docs as absent — should be empty
        assert all(h.score > 0 for h in hits)

    def test_scores_positive(self, index):
        hits = index.search("diabetes HbA1c trial", top_k=5)
        assert all(h.score > 0 for h in hits)

    def test_diabetes_query_finds_diabetes_dataset(self, index):
        hits = index.search("diabetes glycaemic control HbA1c", top_k=3)
        ids = [h.dataset.id for h in hits]
        assert "TEST-DIA-004" in ids

    def test_cardiovascular_query_finds_cardio_dataset(self, index):
        hits = index.search("ECG blood pressure cardiovascular cohort", top_k=3)
        ids = [h.dataset.id for h in hits]
        assert "TEST-CVD-003" in ids
