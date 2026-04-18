#!/usr/bin/env python
"""
Build the FAISS index from the synthetic health dataset catalog.

Usage
-----
    python scripts/build_index.py [--index-dir indexes/] [--model MODEL] [--device cpu]

The script will:
  1. Load the 100-entry synthetic catalog from catalog_search.data_catalog.
  2. Optionally fetch real ClinicalTrials.gov records via the public API
     (pass --fetch-ct N to pull N studies).
  3. Embed every dataset with the biomedical sentence-transformer.
  4. Build and save a FAISS IndexFlatIP.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

# Allow running from repo root without installing the package
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from catalog_search.data_catalog import SYNTHETIC_CATALOG
from catalog_search.models import Dataset
from catalog_search.search import CatalogSearch

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


# ── Optional ClinicalTrials.gov fetcher ──────────────────────────────────────


def fetch_clinicaltrials(n: int = 50) -> list[Dataset]:
    """
    Pull up to *n* studies from the ClinicalTrials.gov v2 API (no auth required).

    Returns an empty list on network error so the build can continue
    with just the synthetic catalog.
    """
    import requests

    url = "https://clinicaltrials.gov/api/v2/studies"
    params = {
        "format": "json",
        "pageSize": min(n, 100),
        "fields": "NCTId,BriefTitle,BriefSummary,Condition,StudyType,Keyword",
        "query.term": "health",
    }
    logger.info("Fetching %d ClinicalTrials.gov records …", n)
    try:
        resp = requests.get(url, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except Exception as exc:
        logger.warning("ClinicalTrials.gov fetch failed: %s", exc)
        return []

    datasets: list[Dataset] = []
    for study in data.get("studies", []):
        proto = study.get("protocolSection", {})
        id_mod = proto.get("identificationModule", {})
        desc_mod = proto.get("descriptionModule", {})
        cond_mod = proto.get("conditionsModule", {})
        design_mod = proto.get("designModule", {})

        nct_id = id_mod.get("nctId", "")
        if not nct_id:
            continue
        datasets.append(
            Dataset(
                id=nct_id,
                title=id_mod.get("briefTitle", ""),
                description=desc_mod.get("briefSummary", ""),
                tags=cond_mod.get("keywords", []),
                conditions=cond_mod.get("conditions", []),
                source="ClinicalTrials.gov",
                study_type=design_mod.get("studyType", ""),
            )
        )

    logger.info("Retrieved %d studies from ClinicalTrials.gov", len(datasets))
    return datasets


# ── Main ─────────────────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(description="Build semantic search index for health datasets")
    parser.add_argument(
        "--index-dir",
        default="indexes/",
        help="Directory to write FAISS index (default: indexes/)",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Sentence-transformer model name (default: auto-select biomedical model)",
    )
    parser.add_argument(
        "--device",
        default="cpu",
        choices=["cpu", "cuda"],
        help="Torch device (default: cpu)",
    )
    parser.add_argument(
        "--fetch-ct",
        type=int,
        default=0,
        metavar="N",
        help="Fetch N real studies from ClinicalTrials.gov (0 = disabled)",
    )
    args = parser.parse_args()

    # ── Assemble corpus ─────────────────────────────────────────────────────
    datasets: list[Dataset] = list(SYNTHETIC_CATALOG)
    logger.info("Synthetic catalog: %d datasets", len(datasets))

    if args.fetch_ct > 0:
        real_studies = fetch_clinicaltrials(args.fetch_ct)
        datasets.extend(real_studies)

    logger.info("Total corpus size: %d datasets", len(datasets))

    # ── Build & save ────────────────────────────────────────────────────────
    engine = CatalogSearch.build(
        datasets=datasets,
        model_name=args.model,
        device=args.device,
        show_progress=True,
    )
    engine.save_index(args.index_dir)
    logger.info("Index saved to %s", args.index_dir)

    # ── Quick smoke test ────────────────────────────────────────────────────
    test_queries = [
        "longitudinal Alzheimer's MRI imaging datasets",
        "type 2 diabetes randomised controlled trial",
        "cancer genomics sequencing",
    ]
    print("\n── Quick smoke test ──")
    for q in test_queries:
        results = engine.search(q, top_k=3)
        print(f"\nQuery: {q!r}")
        for r in results:
            print(f"  [{r.rank}] ({r.method}, {r.score:.3f})  {r.dataset.id}: {r.dataset.title}")


if __name__ == "__main__":
    main()
