"""
FastAPI application — serves the search UI and exposes the search API.

Endpoints
---------
GET  /                    → serves ui/index.html
GET  /api/search?q=...    → returns JSON search results
GET  /api/health          → health check

Run
---
    uvicorn catalog_search.api:app --reload --port 8000
"""

from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from catalog_search import CatalogSearch
from catalog_search.index import CatalogIndex

logger = logging.getLogger(__name__)

# ── Paths ────────────────────────────────────────────────────────────────────

_ROOT = Path(__file__).parent.parent.parent  # src/catalog_search/api.py → repo root
_INDEX_DIR = _ROOT / "indexes"
_UI_DIR = _ROOT / "ui"

# ── App ──────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Health Dataset Catalog Search",
    description="Semantic search for health dataset catalogs (PubMedBERT + FAISS + BM25)",
    version="0.1.0",
)

# ── Search engine (loaded once at startup) ───────────────────────────────────

_engine: CatalogSearch | None = None


@app.on_event("startup")
def _load_engine() -> None:
    global _engine
    if not CatalogIndex.exists(_INDEX_DIR):
        logger.warning(
            "No index found at %s — run `python scripts/build_index.py` first. "
            "Search will be unavailable until the index is built.",
            _INDEX_DIR,
        )
        return
    logger.info("Loading search engine from %s …", _INDEX_DIR)
    t0 = time.perf_counter()
    _engine = CatalogSearch.from_index(_INDEX_DIR)
    elapsed = time.perf_counter() - t0
    logger.info(
        "Search engine ready in %.1fs  (model=%s, corpus=%d)",
        elapsed,
        _engine.model_name,
        _engine.catalog_size,
    )


# ── Response models ───────────────────────────────────────────────────────────

class DatasetOut(BaseModel):
    id: str
    title: str
    description: str
    tags: list[str]
    modality: list[str]
    conditions: list[str]
    source: str
    study_type: str
    variables: list[str]


class SearchResultOut(BaseModel):
    rank: int
    score: float
    method: Literal["semantic", "bm25", "hybrid"]
    is_high_confidence: bool
    dataset: DatasetOut


class SearchResponse(BaseModel):
    query: str
    total: int
    elapsed_ms: float
    model: str
    results: list[SearchResultOut]


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "index_ready": _engine is not None,
        "model": _engine.model_name if _engine else None,
        "corpus_size": _engine.catalog_size if _engine else 0,
    }


@app.get("/api/search", response_model=SearchResponse)
def search(
    q: str = Query(..., min_length=1, description="Free-text search query"),
    top_k: int = Query(10, ge=1, le=50, description="Maximum results to return"),
    method: Literal["auto", "semantic", "bm25"] = Query(
        "auto", description="Force a search method or use auto (hybrid)"
    ),
):
    if _engine is None:
        raise HTTPException(
            status_code=503,
            detail="Search index not ready. Run `python scripts/build_index.py` first.",
        )

    t0 = time.perf_counter()
    force = None if method == "auto" else method
    results = _engine.search(q, top_k=top_k, force_method=force)
    elapsed_ms = (time.perf_counter() - t0) * 1000

    return SearchResponse(
        query=q,
        total=len(results),
        elapsed_ms=round(elapsed_ms, 1),
        model=_engine.model_name,
        results=[
            SearchResultOut(
                rank=r.rank,
                score=round(r.score, 4),
                method=r.method,
                is_high_confidence=r.is_high_confidence,
                dataset=DatasetOut(**r.dataset.model_dump()),
            )
            for r in results
        ],
    )


# ── Static UI ────────────────────────────────────────────────────────────────

@app.get("/", include_in_schema=False)
def serve_ui():
    index = _UI_DIR / "index.html"
    if not index.exists():
        raise HTTPException(status_code=404, detail="UI not found — check that ui/index.html exists.")
    return FileResponse(index)
