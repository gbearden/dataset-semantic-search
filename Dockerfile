# ── Build stage ───────────────────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Runtime stage ─────────────────────────────────────────────────────────────
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy source
COPY . .

# Install the catalog_search package
RUN pip install --no-cache-dir -e . --no-deps

# Pre-download the embedding model and build the FAISS index.
# Baking these into the image layer means cold starts are fast —
# the server loads pre-built artefacts rather than downloading at runtime.
RUN python scripts/build_index.py --index-dir indexes/

# HF Spaces requires port 7860
EXPOSE 7860

# Non-root user (HF Spaces security requirement)
RUN useradd -m -u 1000 appuser && chown -R appuser /app
USER appuser

CMD ["uvicorn", "catalog_search.api:app", "--host", "0.0.0.0", "--port", "7860"]
