"""
Evaluation tests — end-to-end relevance assertions.

These tests verify the acceptance criteria:
  - "MRI" returns imaging datasets
  - Semantic search finds datasets that don't share exact keywords with the query
  - Synonyms and related concepts work (e.g. "brain scan" → MRI datasets)
  - Top results are more relevant than lower results
  - Longitudinal Alzheimer's imaging queries find ADNI/OASIS
  - Cancer genomics queries find TCGA/genomics datasets
  - Precision@K ≥ threshold for standard queries

Tests requiring the real model are marked ``slow`` and ``evaluation``.
BM25-only evaluation tests run without model downloads.

Usage
-----
    pytest tests/test_evaluation.py -m "not slow"   # fast BM25 tests only
    pytest tests/test_evaluation.py -m evaluation   # all (needs model download)
"""

from __future__ import annotations

import pytest

from catalog_search.bm25 import BM25Index
from catalog_search.data_catalog import SYNTHETIC_CATALOG


# ── Helpers ──────────────────────────────────────────────────────────────────


def result_ids(results) -> list[str]:
    return [r.dataset.id for r in results]


def top_n_ids(results, n: int) -> set[str]:
    return {r.dataset.id for r in results[:n]}


def precision_at_k(results, relevant_ids: set[str], k: int) -> float:
    """Fraction of top-k results that are relevant."""
    top = results[:k]
    hits = sum(1 for r in top if r.dataset.id in relevant_ids)
    return hits / k if k > 0 else 0.0


# ── BM25 Evaluation (fast — no model needed) ─────────────────────────────────


class TestBM25Evaluation:
    """Keyword-level correctness on the full 100-entry synthetic catalog."""

    @pytest.fixture(scope="class")
    def bm25(self):
        return BM25Index(SYNTHETIC_CATALOG)

    def test_mri_returns_imaging_datasets(self, bm25):
        """'MRI' query must surface datasets that actually have MRI as a modality or tag."""
        hits = bm25.search("MRI imaging", top_k=5)
        mri_hits = [
            h for h in hits
            if "MRI" in h.dataset.modality
            or "MRI" in h.dataset.tags
            or "neuroimaging" in h.dataset.tags
        ]
        assert mri_hits, (
            f"No MRI dataset in top-5 BM25 results for 'MRI imaging'. "
            f"Got: {[(h.dataset.id, h.dataset.modality) for h in hits]}"
        )

    def test_alzheimers_query_finds_adni(self, bm25):
        hits = bm25.search("Alzheimer's disease longitudinal", top_k=5)
        ids = {h.dataset.id for h in hits}
        assert "ADNI-001" in ids or "OASIS-002" in ids, (
            f"Neither ADNI nor OASIS in top-5 for Alzheimer query: {ids}"
        )

    def test_cancer_genomics_finds_tcga(self, bm25):
        hits = bm25.search("cancer genomics RNA-seq mutation", top_k=5)
        ids = {h.dataset.id for h in hits}
        assert "TCGA-007" in ids, f"TCGA not in top-5 for cancer genomics query: {ids}"

    def test_diabetes_trial_finds_relevant_datasets(self, bm25):
        hits = bm25.search("diabetes randomised trial HbA1c", top_k=5)
        ids = {h.dataset.id for h in hits}
        diabetes_ids = {"ACCORD-014", "UKPDS-023", "DPPOS-024"}
        assert ids & diabetes_ids, f"No diabetes trial dataset in top-5: {ids}"

    def test_cardiovascular_cohort_found(self, bm25):
        hits = bm25.search("cardiovascular risk factors longitudinal cohort", top_k=5)
        ids = {h.dataset.id for h in hits}
        cardio_ids = {"FHS-011", "MESA-012", "ARIC-052"}
        assert ids & cardio_ids, f"No cardiovascular cohort in top-5: {ids}"

    def test_lung_ct_screening_found(self, bm25):
        hits = bm25.search("lung CT screening cancer", top_k=5)
        ids = {h.dataset.id for h in hits}
        assert "NLST-041" in ids or "TCIA-009" in ids, (
            f"No lung CT dataset in top-5: {ids}"
        )

    def test_ehr_icu_found(self, bm25):
        hits = bm25.search("ICU electronic health records critical care", top_k=5)
        ids = {h.dataset.id for h in hits}
        assert "MIMIC-019" in ids, f"MIMIC not in top-5 for ICU EHR query: {ids}"

    def test_no_empty_results_for_common_terms(self, bm25):
        """Guard: common medical terms must always return at least one result."""
        queries = [
            "MRI brain imaging",
            "cancer genomics",
            "diabetes mellitus treatment",
            "cardiovascular cohort",
            "lung respiratory",
            "genome sequencing",
            "pediatric children",
            "clinical trial randomised",
        ]
        for q in queries:
            hits = bm25.search(q, top_k=5)
            assert hits, f"Zero BM25 results for: {q!r}"

    def test_precision_at_3_for_mri_query(self, bm25):
        """At least 2 of the top-3 results for 'MRI scan' should be imaging datasets."""
        hits = bm25.search("MRI brain scan", top_k=3)
        imaging_modalities = {"MRI", "fMRI", "dMRI", "neuroimaging"}
        p = sum(
            1
            for h in hits
            if imaging_modalities & set(h.dataset.modality + h.dataset.tags)
        ) / max(len(hits), 1)
        assert p >= 0.5, f"Precision@3 for MRI scan query too low: {p:.2f}"


# ── Semantic Evaluation (requires model download) ────────────────────────────


@pytest.mark.slow
@pytest.mark.evaluation
class TestSemanticEvaluation:
    """
    End-to-end semantic relevance tests.

    These verify that the model finds semantically related datasets even when
    exact keywords are absent — the core value proposition of semantic search.
    """

    def test_mri_returns_imaging_datasets(self, real_search_engine):
        """Core acceptance criterion: 'MRI' → imaging datasets."""
        results = real_search_engine.search("MRI imaging", top_k=5)
        ids = {r.dataset.id for r in results}
        imaging_ids = {"ADNI-001", "OASIS-002", "HCP-003", "OAI-035", "ENIGMA-005",
                       "UK-BB-006", "MESA-012", "TCIA-009"}
        assert ids & imaging_ids, f"No imaging dataset in top-5 for 'MRI imaging': {ids}"

    def test_brain_scan_synonym_returns_mri_datasets(self, real_search_engine):
        """'brain scan' is a synonym — should still return neuroimaging datasets."""
        results = real_search_engine.search("brain scan neurological study", top_k=5)
        ids = {r.dataset.id for r in results}
        imaging_ids = {"ADNI-001", "OASIS-002", "HCP-003", "ABIDE-004", "ENIGMA-005"}
        assert ids & imaging_ids, (
            f"'brain scan' synonym failed — no MRI datasets in top-5: {ids}"
        )

    def test_memory_loss_returns_alzheimers_datasets(self, real_search_engine):
        """'memory loss cognitive decline' ~ Alzheimer's — semantic synonym test."""
        results = real_search_engine.search("memory loss cognitive decline aging study", top_k=5)
        ids = {r.dataset.id for r in results}
        alzheimer_ids = {"ADNI-001", "OASIS-002", "DIAN-095"}
        assert ids & alzheimer_ids, (
            f"'memory loss' synonym failed — no Alzheimer datasets in top-5: {ids}"
        )

    def test_longitudinal_alzheimers_imaging(self, real_search_engine):
        """Acceptance criterion verbatim: 'longitudinal Alzheimer's imaging datasets'."""
        results = real_search_engine.search("longitudinal Alzheimer's imaging datasets", top_k=5)
        ids = {r.dataset.id for r in results}
        expected = {"ADNI-001", "OASIS-002", "DIAN-095"}
        assert ids & expected, (
            f"'longitudinal Alzheimer's imaging' missed expected datasets: {ids}"
        )

    def test_heart_attack_synonym_returns_cardiovascular(self, real_search_engine):
        """'heart attack' → should surface MI/CVD-related datasets."""
        results = real_search_engine.search("heart attack myocardial infarction prevention", top_k=5)
        ids = {r.dataset.id for r in results}
        cardio_ids = {"FHS-011", "MESA-012", "ACCORD-014", "ARIC-052", "SPRINT-043"}
        assert ids & cardio_ids, (
            f"'heart attack' synonym failed — no CVD datasets in top-5: {ids}"
        )

    def test_blood_sugar_returns_diabetes_datasets(self, real_search_engine):
        """'blood sugar regulation' ~ diabetes — semantic synonym test."""
        results = real_search_engine.search("blood sugar regulation insulin resistance", top_k=5)
        ids = {r.dataset.id for r in results}
        diabetes_ids = {"ACCORD-014", "UKPDS-023", "DPPOS-024", "NHANES-022"}
        assert ids & diabetes_ids, (
            f"'blood sugar' synonym failed — no diabetes datasets in top-5: {ids}"
        )

    def test_dna_sequencing_returns_genomics(self, real_search_engine):
        """'DNA sequencing tumour' → genomics/cancer datasets."""
        results = real_search_engine.search("DNA sequencing tumour biopsy profiling", top_k=5)
        ids = {r.dataset.id for r in results}
        genomics_ids = {"TCGA-007", "ICGC-058", "GTEx-016", "1KG-018"}
        assert ids & genomics_ids, (
            f"'DNA sequencing' query missed genomics datasets: {ids}"
        )

    def test_gut_bacteria_returns_microbiome(self, real_search_engine):
        """'gut bacteria' ~ microbiome — semantic paraphrase test."""
        results = real_search_engine.search("gut bacteria bowel inflammation", top_k=5)
        ids = {r.dataset.id for r in results}
        assert "MICROBIOME-HMP-100" in ids, (
            f"'gut bacteria' semantic test failed — HMP not in top-5: {ids}"
        )

    def test_eye_retina_returns_retinal_imaging(self, real_search_engine):
        """'eye retina photographs' → retinal imaging datasets."""
        results = real_search_engine.search("eye retina photographs diabetic eye disease", top_k=5)
        ids = {r.dataset.id for r in results}
        retinal_ids = {"EYEPACS-037", "MAPLES-DR-038", "AREDS-057", "BIOBANK-RETINA-053"}
        assert ids & retinal_ids, (
            f"'eye retina' failed — no retinal datasets in top-5: {ids}"
        )

    def test_semantic_vs_exact_keyword_gap(self, real_search_engine):
        """
        Query 'neurodegeneration longitudinal cohort' does NOT contain 'MRI' or 'ADNI'
        but semantically should still surface ADNI/OASIS.
        """
        results = real_search_engine.search("neurodegeneration longitudinal cohort", top_k=10)
        ids = {r.dataset.id for r in results}
        assert "ADNI-001" in ids or "OASIS-002" in ids or "DIAN-095" in ids, (
            f"Semantic gap test failed — no AD datasets for 'neurodegeneration longitudinal': {ids}"
        )

    def test_all_results_have_positive_score(self, real_search_engine):
        results = real_search_engine.search("cancer treatment outcomes", top_k=10)
        assert all(r.score > 0 for r in results)

    def test_precision_at_5_alzheimers_imaging(self, real_search_engine):
        """At least 3 of top-5 results for Alzheimer MRI query should be imaging."""
        results = real_search_engine.search("Alzheimer MRI neuroimaging longitudinal", top_k=5)
        imaging_modalities = {"MRI", "PET", "fMRI", "neuroimaging"}
        hits = sum(
            1
            for r in results
            if imaging_modalities & set(r.dataset.modality + r.dataset.tags)
        )
        assert hits >= 3, (
            f"P@5 for Alzheimer MRI query: {hits}/5 imaging datasets "
            f"(expected ≥3). IDs: {result_ids(results)}"
        )

    def test_results_return_under_2_seconds(self, real_search_engine):
        """Acceptance criterion: search must complete within 2 seconds."""
        import time

        queries = [
            "longitudinal Alzheimer's imaging",
            "cancer genomics sequencing",
            "cardiovascular risk factors cohort",
            "diabetes type 2 randomised trial",
        ]
        for q in queries:
            t0 = time.perf_counter()
            real_search_engine.search(q, top_k=10)
            elapsed = time.perf_counter() - t0
            assert elapsed < 2.0, (
                f"Query {q!r} took {elapsed:.2f}s — exceeds 2-second limit"
            )

    def test_method_is_semantic_for_confident_results(self, real_search_engine):
        """Well-known queries should use semantic (high-confidence) method."""
        results = real_search_engine.search("Alzheimer's disease MRI longitudinal", top_k=5)
        # Top result should be semantic, not BM25 fallback
        assert results[0].method == "semantic", (
            f"Expected semantic method for confident query; got {results[0].method}"
        )

    def test_no_empty_results_for_any_query(self, real_search_engine):
        """Guard: every query returns at least one result."""
        queries = [
            "longitudinal Alzheimer's imaging datasets",
            "MRI returns imaging datasets",
            "type 2 diabetes clinical trial",
            "cancer genomics multi-omic",
            "wearable sensor heart rate monitoring",
            "paediatric brain development",
            "gut microbiome inflammatory bowel",
            "COVID-19 treatment randomised",
        ]
        for q in queries:
            results = real_search_engine.search(q, top_k=10)
            assert results, f"Empty result set for query: {q!r}"
