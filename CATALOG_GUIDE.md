# Replacing the Dataset Catalog

This guide explains how to swap the built-in 100-entry synthetic catalog for your own data.  
No changes to the search engine, embedder, or FAISS code are needed — only the catalog source.

---

## The only contract: the `Dataset` type

Every entry in your catalog must be a `Dataset` object, defined in
[`src/catalog_search/models.py`](src/catalog_search/models.py):

```python
from catalog_search.models import Dataset

Dataset(
    id          = "unique-string-id",       # required — must be unique across catalog
    title       = "Study or dataset name",  # required
    description = "Full abstract or summary text",  # required — carries most embedding weight
    tags        = ["MRI", "longitudinal"],  # free-form keywords
    modality    = ["MRI", "EHR", "genomics"],  # data collection modalities
    conditions  = ["Alzheimer's disease"],  # clinical conditions studied
    source      = "NIH NIA",               # data custodian / funding body
    study_type  = "observational",         # "observational" | "interventional" | ""
    variables   = ["MMSE", "hippocampal volume"],  # key measured variables
)
```

The `searchable_text()` method concatenates all fields into the string that is embedded
and BM25-indexed. The richer and more specific the fields, the better the retrieval quality.

---

## Step 1 — Write a loader function

Create a Python file that returns `list[Dataset]`.  
Below are templates for the most common sources.

### From a CSV file

```python
# my_loaders/from_csv.py
import csv
from catalog_search.models import Dataset

def load_from_csv(path: str) -> list[Dataset]:
    datasets = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            datasets.append(Dataset(
                id          = row["id"],
                title       = row["title"],
                description = row["description"],
                tags        = [t.strip() for t in row.get("tags", "").split(",") if t.strip()],
                modality    = [m.strip() for m in row.get("modality", "").split(",") if m.strip()],
                conditions  = [c.strip() for c in row.get("conditions", "").split(",") if c.strip()],
                source      = row.get("source", ""),
                study_type  = row.get("study_type", ""),
                variables   = [v.strip() for v in row.get("variables", "").split(",") if v.strip()],
            ))
    return datasets
```

Expected CSV columns:

| Column | Required | Notes |
|---|---|---|
| `id` | yes | Unique identifier |
| `title` | yes | |
| `description` | yes | |
| `tags` | no | Comma-separated |
| `modality` | no | Comma-separated |
| `conditions` | no | Comma-separated |
| `source` | no | |
| `study_type` | no | |
| `variables` | no | Comma-separated |

### From JSON

```python
# my_loaders/from_json.py
import json
from catalog_search.models import Dataset

def load_from_json(path: str) -> list[Dataset]:
    with open(path, encoding="utf-8") as f:
        records = json.load(f)  # expects a list of dicts
    return [Dataset(**record) for record in records]
```

### From the NIH Reporter API

```python
# my_loaders/from_nih_reporter.py
import requests
from catalog_search.models import Dataset

def load_from_nih_reporter(n: int = 100) -> list[Dataset]:
    url = "https://api.reporter.nih.gov/v2/projects/search"
    payload = {"criteria": {}, "offset": 0, "limit": min(n, 500)}
    resp = requests.post(url, json=payload, timeout=30)
    resp.raise_for_status()
    datasets = []
    for p in resp.json().get("results", []):
        datasets.append(Dataset(
            id          = p.get("core_project_num", p.get("appl_id", "")),
            title       = p.get("project_title", ""),
            description = p.get("abstract_text") or p.get("phr_text") or "",
            tags        = p.get("terms", "").split(";") if p.get("terms") else [],
            conditions  = [t["name"] for t in p.get("disease_spec_project_arr", [])],
            source      = "NIH Reporter",
            study_type  = "observational",
        ))
    return datasets
```

### From ClinicalTrials.gov (already built in)

`scripts/build_index.py` already includes `fetch_clinicaltrials()`.  
Pass `--fetch-ct N` when running the script to pull N live studies.

### From a FHIR ResearchStudy endpoint

```python
# my_loaders/from_fhir.py
import requests
from catalog_search.models import Dataset

def load_from_fhir(base_url: str) -> list[Dataset]:
    resp = requests.get(f"{base_url}/ResearchStudy?_format=json&_count=200", timeout=30)
    resp.raise_for_status()
    datasets = []
    for entry in resp.json().get("entry", []):
        r = entry["resource"]
        datasets.append(Dataset(
            id          = r["id"],
            title       = r.get("title", ""),
            description = r.get("description", ""),
            conditions  = [c["text"] for c in r.get("condition", [])],
            source      = base_url,
            study_type  = r.get("primaryPurpose", {}).get("text", ""),
        ))
    return datasets
```

---

## Step 2 — Wire it into the build script

Edit [`scripts/build_index.py`](scripts/build_index.py), replacing the default catalog import:

```python
# Remove or keep the synthetic catalog
# from catalog_search.data_catalog import SYNTHETIC_CATALOG

# Add your loader
from my_loaders.from_csv import load_from_csv

def main():
    # Option A — replace entirely
    datasets = load_from_csv("data/my_catalog.csv")

    # Option B — merge with synthetic catalog (useful during development)
    # from catalog_search.data_catalog import SYNTHETIC_CATALOG
    # datasets = list(SYNTHETIC_CATALOG) + load_from_csv("data/my_catalog.csv")

    engine = CatalogSearch.build(datasets=datasets, show_progress=True)
    engine.save_index("indexes/")
```

---

## Step 3 — Rebuild the index

```bash
python scripts/build_index.py
```

The embedder will re-encode every document and save a fresh FAISS index to `indexes/`.  
Indexing speed is roughly **50–100 documents/second** on CPU with the PubMedBERT model.

---

## Step 4 — Update the tests

Two test files reference catalog-specific IDs and domain assumptions.  
Update them to match your new data:

### `tests/test_data_catalog.py`

```python
# Update these to reflect your corpus
def test_has_at_least_100_entries(self):
    assert len(YOUR_CATALOG) >= YOUR_EXPECTED_COUNT

def test_imaging_datasets_present(self):
    imaging = [d for d in YOUR_CATALOG if "MRI" in d.modality]
    assert len(imaging) >= YOUR_EXPECTED_IMAGING_COUNT
```

### `tests/test_evaluation.py` — `TestBM25Evaluation`

Replace the expected-ID sets with IDs from your catalog:

```python
def test_mri_returns_imaging_datasets(self, bm25):
    hits = bm25.search("MRI imaging", top_k=5)
    mri_hits = [h for h in hits if "MRI" in h.dataset.modality]
    assert mri_hits  # modality check works regardless of specific IDs
```

### `tests/test_evaluation.py` — `TestSemanticEvaluation`

Update the `relevant_ids` sets in the batch table:

```python
TEST_QUERIES = [
    ("your query here", {"YOUR-ID-001", "YOUR-ID-002"}),
    ...
]
```

---

## Tips for better retrieval quality

**Write rich descriptions.** The description field carries the most weight in the embedding.
A one-line description will retrieve poorly; a full abstract will retrieve well.

**Use specific modality and condition values.** The `searchable_text()` method concatenates
all fields, so precise values in `modality` and `conditions` help both semantic and BM25 search.

**Normalise synonyms in tags.** If your catalog uses both "fMRI" and "functional MRI",
add both to `tags` so BM25 finds either.

**Tune the confidence threshold** if your domain is very different from biomedical literature.
The default is `0.35`; lower it to rely more on semantic results, raise it to fall back to
BM25 more aggressively:

```python
engine = CatalogSearch.build(datasets, confidence_threshold=0.30)
```

**Consider a domain-specific model.** The default model is `pritamdeka/S-PubMedBert-MS-MARCO`
(biomedical). For other domains, pass a different model name:

```python
engine = CatalogSearch.build(
    datasets,
    model_name="sentence-transformers/all-mpnet-base-v2",  # general-purpose
)
```

Other options worth evaluating:

| Domain | Suggested model |
|---|---|
| Biomedical (default) | `pritamdeka/S-PubMedBert-MS-MARCO` |
| Scientific literature | `allenai/scibert_scivocab_uncased` |
| General / fast | `sentence-transformers/all-MiniLM-L6-v2` |
| Multilingual | `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` |
