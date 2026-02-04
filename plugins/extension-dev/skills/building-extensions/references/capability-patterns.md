# Capability Patterns

Building tools and APIs with Collaborative Intelligence principles.

## CLI Design

### Progressive Disclosure

```
80% default path → zero flags, just works
20% power users → explicit flags, escape hatches
```

**Example (memex):**
```bash
# Default: hybrid search, auto-rerank
memex dig "where did I decide on auth?"

# Power: specific search mode
memex keyword "OAuth"
memex semantic "authentication patterns" --min-score 0.5

# Escape hatch: raw SQL
memex query "SELECT * FROM fragments WHERE..."
```

### The 80/20 Stack

| Layer | 80% (Default) | 20% (Power) |
|-------|---------------|-------------|
| Interface | Intent-driven | Explicit flags |
| Search | Hybrid (BM25 + semantic) | Mode-specific |
| Output | Human-readable | `--format json` |
| Control | Auto-best | Manual tuning |

### Command Design

| Principle | Implementation |
|-----------|----------------|
| **Verb-noun** | `memex dig`, `cix add` |
| **Predictable** | Same input → same output |
| **Dry-run** | `--dry-run` shows what would happen |
| **Confirm destructive** | `memex reset` requires `--yes` or interactive |

### Error Messages

```python
# Bad
print("Error: Invalid input")
sys.exit(1)

# Good
obs.error("Embedding dimension mismatch")
obs.info(f"Corpus has {corpus_dims}-dim, embedder produces {embedder_dims}-dim")
obs.info("Fix: Run 'memex reset' then re-ingest with new model")
```

---

## API Design

### Contract-First

Define ports as protocols, implement as adapters:

```python
class EmbeddingPort(Protocol):
    """Contract: text → vector"""
    def embed(self, text: str) -> list[float]: ...
    def embed_batch(self, texts: list[str]) -> list[list[float]]: ...

    @property
    def dimensions(self) -> int: ...
```

### Error Design

| Level | Purpose | Example |
|-------|---------|---------|
| **Domain errors** | Business logic | `EmbeddingDimensionMismatchError` |
| **Validation errors** | Input checking | `InvalidQueryError` |
| **Infrastructure errors** | External failures | `DatabaseConnectionError` |

```python
class EmbeddingDimensionMismatchError(Exception):
    """Raised when corpus dimensions don't match embedder."""

    def __init__(self, corpus_dim: int, embedder_dim: int):
        self.corpus_dim = corpus_dim
        self.embedder_dim = embedder_dim
        super().__init__(
            f"Corpus has {corpus_dim}-dim but embedder produces {embedder_dim}-dim. "
            f"Run 'memex reset' then re-ingest."
        )
```

### Fail Fast

Validate at construction, not runtime:

```python
# Composition root
def create_service(with_embedder: bool = False):
    embedder = get_embedder() if with_embedder else None
    corpus = DuckDBCorpus(path, embedding_dim=embedder.dimensions if embedder else None)

    # Fail fast: check at startup
    if embedder:
        corpus_dims = corpus.embedding_dimensions()
        if corpus_dims and corpus_dims != embedder.dimensions:
            raise EmbeddingDimensionMismatchError(corpus_dims, embedder.dimensions)
```

---

## Hexagonal Architecture

### Structure

```
tool/
├── src/tool/
│   ├── domain/           # Pure, no dependencies
│   │   ├── models.py
│   │   └── services/
│   ├── ports/            # Contracts
│   │   └── _out/
│   │       ├── corpus.py
│   │       └── embedding.py
│   ├── adapters/         # Implementations
│   │   ├── _in/          # Driving (CLI, API)
│   │   └── _out/         # Driven (DB, external)
│   └── composition/      # Wiring
│       └── __init__.py
```

### Dependency Flow

```
CLI (driving) → Service (domain) → Port (contract) → Adapter (driven)
     ↓                                                      ↓
  User intent                                         Infrastructure
```

### Composition Root

Single place for wiring:

```python
# composition/__init__.py
def create_service(with_embedder: bool = False) -> ExcavationService:
    embedder = get_embedder() if with_embedder else None
    corpus = DuckDBCorpus(settings.corpus_path, embedding_dim=embedder.dimensions)
    adapters = [ClaudeConversationsAdapter(), OpenAIConversationsAdapter()]
    return ExcavationService(corpus, adapters, embedder)
```

---

## Observability

### Structured Logging

```python
import structlog

log = structlog.get_logger()

def ingest(path: Path):
    log.info("ingest_started", path=str(path))

    try:
        count = service.ingest(path)
        log.info("ingest_completed", path=str(path), fragments=count)
    except Exception as e:
        log.error("ingest_failed", path=str(path), error=str(e))
        raise
```

### OTel for Tools

```python
from opentelemetry import trace

tracer = trace.get_tracer("memex")

def search(query: str):
    with tracer.start_as_current_span("search") as span:
        span.set_attribute("query", query[:100])

        results = service.search(query)

        span.set_attribute("result_count", len(results))
        span.set_attribute("success", True)
        return results
```

---

## Testing

### Port-Based Testing

```python
def test_search_returns_relevant_fragments(corpus_with_data):
    service = ExcavationService(corpus_with_data, [], None)

    results = service.keyword_search("authentication")

    assert len(results) > 0
    assert any("auth" in r.content.lower() for r in results)
```

### Fixture Composition

```python
@pytest.fixture
def corpus(tmp_path):
    corpus = DuckDBCorpus(tmp_path / "test.duckdb", embedding_dim=384)
    yield corpus
    corpus.close()

@pytest.fixture
def corpus_with_data(corpus, sample_fragments):
    corpus.store(sample_fragments)
    corpus.rebuild_fts_index()
    return corpus
```
