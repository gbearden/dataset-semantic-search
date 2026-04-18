"""Domain models for dataset catalog entries and search results."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class Dataset(BaseModel):
    """A single entry in the health dataset catalog."""

    id: str = Field(..., description="Unique identifier (e.g. NCT number, NIH grant ID)")
    title: str
    description: str
    tags: list[str] = Field(default_factory=list)
    modality: list[str] = Field(
        default_factory=list,
        description="Data modalities: imaging, genomics, EHR, survey, …",
    )
    conditions: list[str] = Field(default_factory=list)
    source: str = Field(default="", description="Data source (NIH, ClinicalTrials.gov, …)")
    study_type: str = Field(default="", description="observational | interventional | …")
    variables: list[str] = Field(default_factory=list)

    def searchable_text(self) -> str:
        """Concatenate all text fields into a single string for embedding/BM25."""
        parts = [
            self.title,
            self.description,
            " ".join(self.tags),
            " ".join(self.modality),
            " ".join(self.conditions),
            " ".join(self.variables),
        ]
        return " ".join(p for p in parts if p)


class SearchResult(BaseModel):
    """A ranked search result."""

    dataset: Dataset
    score: float = Field(..., description="Relevance score in [0, 1]")
    method: Literal["semantic", "bm25", "hybrid"] = "semantic"
    rank: int = Field(..., ge=1)

    @property
    def is_high_confidence(self) -> bool:
        return self.score >= 0.35
