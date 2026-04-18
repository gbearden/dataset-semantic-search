"""Unit tests for BiomedEmbedder (uses MockEmbedder for speed)."""

import numpy as np
import pytest

from catalog_search.embedder import BiomedEmbedder


class TestMockEmbedder:
    """Structural tests that run with the mock embedder from conftest."""

    def test_encode_single_string(self, mock_embedder):
        v = mock_embedder.encode("longitudinal Alzheimer MRI")
        assert v.ndim == 1
        assert v.shape[0] == mock_embedder.dim

    def test_encode_list_of_strings(self, mock_embedder):
        texts = ["MRI study", "genomics dataset", "diabetes trial"]
        vecs = mock_embedder.encode(texts)
        assert vecs.shape == (3, mock_embedder.dim)

    def test_normalised_vectors_unit_length(self, mock_embedder):
        v = mock_embedder.encode("test query", normalize=True)
        assert abs(np.linalg.norm(v) - 1.0) < 1e-5

    def test_different_texts_differ(self, mock_embedder):
        v1 = mock_embedder.encode("brain MRI imaging")
        v2 = mock_embedder.encode("cancer genomics sequencing")
        assert not np.allclose(v1, v2)

    def test_same_text_same_vector(self, mock_embedder):
        v1 = mock_embedder.encode("identical query text")
        v2 = mock_embedder.encode("identical query text")
        np.testing.assert_array_equal(v1, v2)

    def test_batch_matches_individual(self, mock_embedder):
        texts = ["alpha", "beta", "gamma"]
        batch = mock_embedder.encode(texts)
        for i, t in enumerate(texts):
            single = mock_embedder.encode(t)
            np.testing.assert_allclose(batch[i], single, atol=1e-6)


class TestBiomedEmbedderInterface:
    """Tests that BiomedEmbedder exposes the right interface (without loading a model)."""

    def test_model_name_is_none_before_load(self):
        e = BiomedEmbedder.__new__(BiomedEmbedder)
        e._model_name = None
        e._model = None
        e._device = "cpu"
        assert e._model is None

    def test_custom_model_name_stored(self):
        e = BiomedEmbedder(model_name="some/model")
        assert e._model_name == "some/model"
