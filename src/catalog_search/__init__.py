"""
catalog_search — semantic + BM25 hybrid search for health dataset catalogs.

Quick start
-----------
>>> from catalog_search.search import CatalogSearch
>>> engine = CatalogSearch.from_index("indexes/")
>>> results = engine.search("longitudinal Alzheimer's imaging datasets")
"""

from .models import Dataset, SearchResult
from .search import CatalogSearch

__all__ = ["Dataset", "SearchResult", "CatalogSearch"]
