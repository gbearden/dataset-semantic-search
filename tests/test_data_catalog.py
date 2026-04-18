"""Tests for the synthetic catalog corpus."""

import pytest

from catalog_search.data_catalog import SYNTHETIC_CATALOG


class TestSyntheticCatalog:
    def test_has_at_least_100_entries(self):
        assert len(SYNTHETIC_CATALOG) >= 100

    def test_all_ids_unique(self):
        ids = [d.id for d in SYNTHETIC_CATALOG]
        assert len(ids) == len(set(ids)), "Duplicate dataset IDs found"

    def test_all_have_title_and_description(self):
        for d in SYNTHETIC_CATALOG:
            assert d.title.strip(), f"Empty title for {d.id}"
            assert d.description.strip(), f"Empty description for {d.id}"

    def test_imaging_datasets_present(self):
        imaging = [
            d for d in SYNTHETIC_CATALOG
            if any(m in d.modality for m in ["MRI", "CT", "PET", "X-ray", "fMRI"])
        ]
        assert len(imaging) >= 10, f"Expected ≥10 imaging datasets, got {len(imaging)}"

    def test_genomics_datasets_present(self):
        genomics = [
            d for d in SYNTHETIC_CATALOG
            if any(m in d.modality for m in ["genomics", "transcriptomics", "WGS"])
        ]
        assert len(genomics) >= 5

    def test_longitudinal_studies_present(self):
        longitudinal = [
            d for d in SYNTHETIC_CATALOG
            if "longitudinal" in d.tags or "longitudinal" in d.description.lower()
        ]
        assert len(longitudinal) >= 5

    def test_rct_datasets_present(self):
        rcts = [d for d in SYNTHETIC_CATALOG if d.study_type == "interventional"]
        assert len(rcts) >= 5

    def test_alzheimers_datasets_present(self):
        ad = [
            d for d in SYNTHETIC_CATALOG
            if "Alzheimer" in " ".join(d.tags + d.conditions + [d.title])
        ]
        assert len(ad) >= 2, f"Expected ≥2 Alzheimer datasets, got {len(ad)}"

    def test_searchable_text_non_empty(self):
        for d in SYNTHETIC_CATALOG:
            assert d.searchable_text().strip(), f"Empty searchable_text for {d.id}"
