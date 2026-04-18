# dataset-semantic-search

Semantic search for health dataset catalogs.  
Enter a free-text query — the engine finds relevant datasets by *meaning*, not just keyword overlap.

```
Query: "memory loss cognitive decline aging study"

[1] 0.951  ADNI-001  Alzheimer's Disease Neuroimaging Initiative (ADNI)
[2] 0.934  OASIS-002 OASIS-3: Longitudinal Multimodal Neuroimaging Dataset
[3] 0.921  DIAN-095  Dominantly Inherited Alzheimer Network (DIAN)
```

## How it works

| Layer | Technology | Role |
|---|---|---|
| Embedding | `pritamdeka/S-PubMedBert-MS-MARCO` (PubMedBERT) | Encode queries and dataset metadata into semantic vectors |
| Vector search | FAISS `IndexFlatIP` | Exact cosine similarity over the vector index |
| Keyword fallback | BM25 (`rank-bm25`) | Activates automatically when semantic confidence is low |

Queries and data stay **entirely local** — no calls to external APIs.

## Quick start

**1. Install**

```bash
pip install -e ".[dev]"
```

**2. Build the index**

```bash
python scripts/build_index.py
```

This downloads the PubMedBERT model (~440 MB, once), embeds the catalog, and saves the FAISS index to `indexes/`.

To pull live studies from ClinicalTrials.gov on top of the built-in catalog:

```bash
python scripts/build_index.py --fetch-ct 100
```

**3. Search**

```python
from catalog_search import CatalogSearch

engine = CatalogSearch.from_index("indexes/")
results = engine.search("longitudinal Alzheimer's imaging datasets", top_k=5)

for r in results:
    print(r.rank, r.score, r.dataset.title)
```

**4. Explore interactively**

Open `notebooks/explore.ipynb` in VS Code (or Jupyter) for a guided tour of queries, score distributions, and side-by-side semantic vs BM25 comparisons.

## Project structure

```
src/catalog_search/
├── models.py        — Dataset + SearchResult types
├── data_catalog.py  — 100-entry synthetic health dataset corpus
├── embedder.py      — Sentence-transformer wrapper (biomedical model priority list)
├── bm25.py          — BM25 keyword search
├── index.py         — FAISS index: build, save, load, search
└── search.py        — CatalogSearch: hybrid engine with automatic BM25 fallback

scripts/
└── build_index.py   — Ingest → embed → save; optional ClinicalTrials.gov fetch

notebooks/
└── explore.ipynb    — Interactive exploration notebook (VS Code / Jupyter)

tests/
├── conftest.py          — MockEmbedder and shared fixtures
├── test_models.py       — Domain model unit tests
├── test_embedder.py     — Embedder interface tests
├── test_bm25.py         — BM25 correctness
├── test_index.py        — FAISS build / search / persistence
├── test_search.py       — Hybrid engine structure and fallback logic
├── test_data_catalog.py — Corpus integrity
└── test_evaluation.py   — End-to-end relevance tests (BM25 + semantic)
```

## Running tests

```bash
# Fast tests only — no model download needed
pytest -m "not slow"

# Full suite including semantic relevance tests (requires model)
pytest
```

Tests are split by speed:

- **Fast (72 tests):** use a `MockEmbedder` — run in ~0.1 s, no network needed
- **Slow/evaluation (15 tests):** use the real PubMedBERT model — run in ~5 s after first download

## Using your own catalog

See [CATALOG_GUIDE.md](CATALOG_GUIDE.md) for step-by-step instructions on replacing the built-in dataset catalog with your own data.

## Acceptance criteria met

- Free-text natural language queries return semantically relevant results
- Results ranked by relevance score (cosine similarity)
- Synonym and paraphrase support ("memory loss" → Alzheimer datasets, "brain scan" → MRI datasets)
- Automatic BM25 fallback when semantic confidence is low (`score < 0.35`)
- No query returns an empty result set without a fallback attempt
- Model runs locally — no data leaves the machine
- Search returns in < 2 seconds for standard queries

## License

[MIT](LICENSE)
