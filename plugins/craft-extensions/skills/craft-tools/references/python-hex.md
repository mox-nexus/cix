# Python Hexagonal + Functional Patterns

Patterns for building Python tools with hexagonal architecture and functional streaming. Extracted from production use (memex, cix).

## Hexagonal Layout

```
src/tool/
├── domain/
│   ├── models.py              # Pydantic models, pure data
│   ├── services/              # Use case orchestration
│   └── ports/
│       └── _out/
│           ├── corpus.py      # Protocol — what we need
│           └── embedding.py   # Protocol — what we need
├── adapters/
│   ├── _in/
│   │   └── cli/               # Driving: Click/Rich CLI
│   └── _out/
│       ├── corpus/duckdb/     # Driven: DuckDB implementation
│       └── embedding/         # Driven: ONNX implementation
├── composition/
│   └── __init__.py            # Wiring root — only place that knows all adapters
└── config/
    └── settings.py            # Pydantic BaseSettings (TOML + env vars)
```

### Key rules

- **Ports are `typing.Protocol`** with `@runtime_checkable`. Not ABCs.
- **Domain imports nothing from adapters.** Ever.
- **Composition root** is the only file that imports both ports and adapters.
- **Settings flow through constructor injection**, not global state. Composition root reads settings, passes values to adapter constructors.
- **`_in` = driving** (CLI, API). **`_out` = driven** (DB, models, APIs).

### Port example

```python
from collections.abc import Iterator
from typing import Protocol, runtime_checkable

@runtime_checkable
class EmbeddingPort(Protocol):
    """One method is the primitive. Convenience derives from it."""

    def embed_stream(self, texts: Iterator[str]) -> Iterator[list[float]]:
        """1:1 streaming transform. Texts in, vectors out."""
        ...

    @property
    def dimensions(self) -> int: ...

# Convenience — free functions, not protocol requirements
def embed_one(port: EmbeddingPort, text: str) -> list[float]:
    return next(port.embed_stream(iter([text])))
```

### Composition root

```python
from functools import lru_cache
from tool.config.settings import get_settings

@lru_cache(maxsize=1)
def get_embedder() -> EmbeddingPort:
    from tool.adapters._out.embedding.fastembed import FastEmbedEmbedder
    s = get_settings()
    return FastEmbedEmbedder(
        onnx_batch_size=s.onnx_batch_size,
        onnx_threads=s.onnx_threads,
    )
```

### Lazy settings

```python
_settings: Settings | None = None

def get_settings() -> Settings:
    """Lazy — defers construction until first access.
    Allows CLI flags to set env vars before settings are built.
    """
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
```

---

## Functional Streaming

### The principle

Every `list()` on a generator is a dam in the river. If you don't need the reservoir, don't build the dam. Pipelines should be pipes, not chains of buckets.

### Core idioms

#### `iter(callable, sentinel)` — unfold

Python's built-in "unfold." Repeatedly calls the callable until it returns the sentinel.

```python
from itertools import chain

def fetch_batch():
    return db.execute("SELECT ... LIMIT 100").fetchall()

# Replaces: while (rows := fetch()):
rows = chain.from_iterable(iter(fetch_batch, []))
```

#### `itertools.batched` — chunking (Python 3.12+)

```python
from itertools import batched

# Process a stream in fixed-size chunks
for chunk in batched(all_texts, 4):
    model.embed(list(chunk))  # Only 4 in memory at a time
```

#### `chain.from_iterable` — flatten nested generators

```python
from itertools import chain

# Generator of generators → single flat stream
flat = chain.from_iterable(
    (process(item) for item in batch)
    for batch in batched(source, 100)
)
```

#### `map` — apply function to stream

```python
# Side-effectful map (write each, pass through)
written = map(write_to_db, embedded_pairs)
```

#### `tap` / `tap_every` — side effects on a stream

```python
from collections.abc import Callable, Iterator
from typing import TypeVar

T = TypeVar("T")

def tap(iterator: Iterator[T], fn: Callable[[T], None]) -> Iterator[T]:
    """Observe each element without consuming it."""
    for item in iterator:
        fn(item)
        yield item

def tap_every(iterator: Iterator[T], n: int, fn: Callable[[int], None]) -> Iterator[T]:
    """Side effect every n-th element. Counter is 1-based."""
    for i, item in enumerate(iterator, 1):
        yield item
        if i % n == 0:
            fn(i)
```

#### `sum(1 for _ in x)` — terminal consumer with count

```python
# Consume the entire pipeline, return count
updated = sum(1 for _ in pipeline)
```

#### `itertools.count` — stateless counter

```python
from itertools import count

counter = count(1)
# Use next(counter) instead of mutable `i += 1`
```

---

## Streaming Pipeline Pattern

### The shape

```
source → transform → sink → tap(side effects) → terminal
```

Each stage is a generator. Nothing materializes beyond its batch boundary.

### Example: embedding backfill

```python
from itertools import chain, count

def backfill(self, embedder: EmbeddingPort, fetch_size: int = 100,
             on_progress=None) -> int:
    total = self.count_pending()
    if total == 0:
        return 0

    self._drop_index()

    try:
        # Source: flat stream of (id, content) from DB
        rows = chain.from_iterable(iter(self._fetch_batch, []))

        # Transform: pair with embeddings (streaming, bounded)
        embedded = self._embed_rows(rows, embedder, fetch_size)

        # Sink: write each to DB (side effect, passthrough)
        pipeline = map(self._write_one, embedded)

        # Tap: checkpoint every 1000 writes
        pipeline = tap_every(pipeline, 1000, lambda _: self._checkpoint())

        # Tap: progress reporting
        if on_progress:
            c = count(1)
            pipeline = tap(pipeline, lambda _: on_progress(next(c), total))

        # Terminal: consume and count
        return sum(1 for _ in pipeline)
    finally:
        self._checkpoint()
        self._rebuild_index()
```

### The transform stage (zero accumulation)

```python
def _embed_rows(self, rows, embedder, batch_size):
    """Batch, unzip, embed, re-zip, flatten. Zero accumulation."""
    for batch in batched(rows, batch_size):
        ids, contents = zip(*batch)
        yield from zip(ids, embedder.embed_stream(iter(contents)))
```

At any point: one batch of ids (strings, cheap) + one ONNX inference (4 vectors). Nothing grows with corpus size.

### Memory model

| In flight | Size | Lifetime |
|-----------|------|----------|
| DB fetch buffer | `fetch_size` rows | One fetch cycle |
| `zip(*batch)` | `fetch_size` ids + contents | One batch |
| ONNX inference | `onnx_batch_size` vectors | One inference |
| Pipeline element | 1 `(id, embedding)` | Until write returns |
| Counter | 1 integer | Entire run |

Peak: O(fetch_size) + O(onnx_batch_size). Constant regardless of corpus size.

---

## Anti-patterns

| Anti-pattern | Fix |
|-------------|-----|
| `list()` on a generator in a bulk path | `yield from` or `chain.from_iterable` |
| `while True: ... break` | `iter(callable, sentinel)` or bounded `for` |
| Mutable counter (`i += 1`) in a loop | `enumerate()` or `itertools.count()` |
| Side effects mixed into iteration body | `tap()` / `tap_every()` as named stream operators |
| Port exposes 3 cardinalities (single/batch/stream) | Stream is the primitive; others are free functions |
| `executemany` with full batch | Single `execute` per item in streaming sink |
| `.tolist()` + list comprehension (double copy) | `yield embedding.tolist()` — convert and release immediately |

---

## ONNX-Specific

See `data-store:data-store` reference [`embedding-models.md`](../../../data-store/skills/data-store/references/embedding-models.md) for ONNX Runtime resource model, batch/thread tuning, and resource profiles.
