"""Unit tests for domain models."""

import pytest

from catalog_search.models import Dataset, SearchResult


class TestDataset:
    def test_searchable_text_includes_title(self):
        d = Dataset(id="x", title="Brain MRI Study", description="Imaging data")
        assert "Brain MRI Study" in d.searchable_text()

    def test_searchable_text_includes_tags(self):
        d = Dataset(id="x", title="T", description="D", tags=["MRI", "Alzheimer"])
        text = d.searchable_text()
        assert "MRI" in text
        assert "Alzheimer" in text

    def test_searchable_text_includes_modality(self):
        d = Dataset(id="x", title="T", description="D", modality=["PET", "fMRI"])
        text = d.searchable_text()
        assert "PET" in text
        assert "fMRI" in text

    def test_searchable_text_includes_conditions(self):
        d = Dataset(id="x", title="T", description="D", conditions=["diabetes"])
        assert "diabetes" in d.searchable_text()

    def test_searchable_text_includes_variables(self):
        d = Dataset(id="x", title="T", description="D", variables=["HbA1c", "BMI"])
        text = d.searchable_text()
        assert "HbA1c" in text
        assert "BMI" in text

    def test_empty_lists_dont_crash(self):
        d = Dataset(id="x", title="", description="")
        text = d.searchable_text()
        assert isinstance(text, str)


class TestSearchResult:
    def _make(self, score: float) -> SearchResult:
        d = Dataset(id="x", title="T", description="D")
        return SearchResult(dataset=d, score=score, method="semantic", rank=1)

    def test_high_confidence_above_threshold(self):
        assert self._make(0.5).is_high_confidence is True

    def test_high_confidence_at_threshold(self):
        assert self._make(0.35).is_high_confidence is True

    def test_low_confidence_below_threshold(self):
        assert self._make(0.34).is_high_confidence is False

    def test_rank_must_be_positive(self):
        with pytest.raises(Exception):
            d = Dataset(id="x", title="T", description="D")
            SearchResult(dataset=d, score=0.5, method="semantic", rank=0)
