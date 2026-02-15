# Embedding Models for Search (2026)

## Recommendation Matrix

| Use Case | Model | Dims | Speed | Quality | Cost |
|----------|-------|------|-------|---------|------|
| **Personal KB (recommended)** | Nomic Embed v1.5 | 768 | Good | Excellent | Free |
| Speed-critical | all-MiniLM-L6-v2 | 384 | 5x faster | Good | Free |
| Edge/mobile | E5-Small-v2 | 384 | Very fast | Good | Free |
| Best accuracy | Voyage-4-Large | 1024 | API latency | Best | $0.06-0.18/1M |
| Budget API | Gemini Embedding | 768 | API latency | Good | Free tier |

---

## Local Models (Recommended for Personal Use)

### Nomic Embed Text V1.5 (Primary Recommendation)

**Why:**
- First production-ready open-source MoE architecture
- Trained on 1.6B contrastive pairs
- 100+ languages, 8K token context
- Competitive with Voyage, beats OpenAI v3
- Apache 2.0 license

**Specs:**
- Dimensions: 1536 (can reduce to 768)
- Inference: ~50-100ms per query on CPU
- Model size: ~500MB

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("nomic-ai/nomic-embed-text-v1.5")
embedding = model.encode("your text here")
```

### all-MiniLM-L6-v2 (Speed Fallback)

**Why:**
- Most battle-tested
- 4-5x faster than full models
- Runs on edge devices
- Acceptable 5-10% quality tradeoff

**Specs:**
- Dimensions: 384
- Inference: ~5ms per query
- Throughput: 14K sentences/sec on CPU

```python
model = SentenceTransformer("all-MiniLM-L6-v2")
```

---

## API Models (When Quality Matters)

### Voyage-4-Large

**Why choose over OpenAI:**
- 8.2% better than Cohere Embed v4
- 14% better than OpenAI v3-Large
- Built by Stanford RAG researchers
- Lower latency than competitors

**Pricing:** $0.06-0.18 per 1M tokens (30-40% cheaper than OpenAI)

### OpenAI text-embedding-3

**When to use:** Enterprise with existing OpenAI integration

**Pricing:** $0.13 per 1M tokens

**Reality:** Outperformed by open-source on MTEB benchmarks

---

## Dimension Tradeoffs

| Dimension | Speed | Quality | Storage | Recommendation |
|-----------|-------|---------|---------|----------------|
| 384 | 5x faster | Good | 50% less | Mobile, real-time |
| **768** | 2x faster | Very good | 25% less | **Sweet spot** |
| 1024 | Baseline | Excellent | Baseline | Complex multilingual |
| 1536 | 0.8x slower | Marginal | +50% | Overkill for most |

**Evidence:** Quality curve flattens after 768. Going higher yields <5% improvement at 2x cost.

### Dimension Reduction

768-dim from Nomic retains 95%+ accuracy:

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "nomic-ai/nomic-embed-text-v1.5",
    truncate_dim=768  # Reduce from 1536
)
```

---

## Multi-Modal (Skip for Text-Only)

### When to Consider

- Research papers with figures
- Screenshot-heavy documentation
- Image + text retrieval

### Models

- **OpenCLIP ViT-G/H** — Community-maintained, reproducible
- **SigLIP 2** — Google DeepMind, improved objective
- **EVA-CLIP** — High-resolution fine-grained vision

### When to Skip Multimodal

- Requires 1024-4096 dimensions (3x+ storage)
- GPU infrastructure needed for reasonable latency
- 10-50x slower than text-only models
- Only needed if your corpus has significant image content

---

## Runtime: fastembed (ONNX) over sentence-transformers

**Prefer fastembed for local embedding.** ONNX runtime, no torch dependency.

| | sentence-transformers | fastembed (ONNX) |
|--|----------------------|------------------|
| Install size | ~2GB (torch) | ~285MB |
| Inference speed | Baseline | ~12x faster |
| Quality (nomic v1.5) | Baseline | cosine ~0.9999 |
| Dependency weight | Heavy (torch, transformers) | Light (onnxruntime) |

```python
from fastembed import TextEmbedding

model = TextEmbedding("nomic-ai/nomic-embed-text-v1.5", threads=2)

# Returns a generator — don't call list() in bulk paths
for embedding in model.embed(texts, batch_size=4):
    yield embedding.tolist()
```

---

## ONNX Resource Model

ONNX Runtime pads all sequences in a batch to max length, then allocates O(batch * seq_len^2) attention tensors. With real corpus text (avg ~2500 chars), default batch_size=256 can require ~90GB for 100 documents — instant SIGKILL.

### Two knobs

| Setting | Effect | Default | Guidance |
|---------|--------|---------|----------|
| `batch_size` | Docs per ONNX inference call. Peak RAM scales linearly. | 4 | Biggest lever for memory |
| `threads` | ONNX inter-op threads. Each allocates a memory arena. | 2 | Secondary lever |

### Resource profiles

| Profile | batch_size | threads | Peak RAM | Target |
|---------|-----------|---------|----------|--------|
| Conservative | 1-2 | 1 | ~2GB | 8GB machines, CI |
| Default | 4 | 2 | ~5GB | 16-64GB machines |
| Aggressive | 8 | 4 | ~10GB | 64GB+ with fast backfill |

### Expose via settings, not CLI flags

The embedder adapter receives resource settings through constructor injection. Users configure via env vars or config files. Claude-as-operator reads the skill to diagnose and tune.

```python
# Settings (Pydantic)
onnx_batch_size: int = 4
onnx_threads: int = 2

# Composition root passes to adapter
FastEmbedEmbedder(onnx_batch_size=s.onnx_batch_size, onnx_threads=s.onnx_threads)
```

### Diagnosis

If an embedding process exits silently (SIGKILL, exit 137), it's OOM. Lower `batch_size` first, then `threads`.

### ONNX Padding Tax

ONNX pads all sequences in a batch to the **max length in that batch**. One outlier destroys the entire batch:

| Batch scenario | Attention tensor | Relative cost |
|---|---|---|
| 4 × 500 tokens (uniform) | 4 × 500² = 1M | 1x |
| 3 × 500 + 1 × 2000 (one long) | 4 × 2000² = 16M | 16x |
| 3 × 500 + 1 × 8192 (one extreme) | 4 × 8192² = 268M | **268x** |

**Sort by content length before batching.** This is the single highest-impact optimization for heterogeneous corpora. Similar-length documents in the same ONNX batch eliminate padding waste. Expected: 3-8x throughput improvement.

```python
# Pre-fetch IDs sorted by length — similar-length fragments batch together
ids = db.execute(
    "SELECT id FROM fragments WHERE embedding IS NULL ORDER BY LENGTH(content)"
).fetchall()
```

### ONNX Arena Growth

ONNX Runtime uses arena allocation. Arenas grow monotonically — every time a longer sequence is encountered, the arena expands and **never shrinks back**. This is C++ managed memory invisible to Python GC.

Over a 60K-fragment backfill with long-tail content distribution (median 778 chars, max 256K), RSS can grow from 5GB to 26GB purely from arena ratcheting.

**Mitigations (ranked):**
1. Sort by length (prevents arena from seeing outlier-mixed batches)
2. Truncate to model context window (~8K tokens for nomic) before embedding
3. ONNX session option `arena_extend_strategy = kSameAsRequested` (less over-allocation)

### Progressive Scan Degradation

Naively fetching unembedded rows with `WHERE embedding IS NULL LIMIT N` does a full scan. As backfill progresses, more rows have embeddings, so each scan skips more non-NULL rows. At 90% done, it scans 54K rows to find 100 NULLs.

Total work: O(n²/batch_size). **The run gets slower over time.**

**Fix:** Pre-fetch all unembedded IDs upfront (~2MB for 60K UUIDs), then cursor through by ID. O(n) total.

---

## Production Patterns

### Streaming Embedding (bulk paths)

fastembed's `embed()` returns a generator. Preserve it — don't call `list()`.

```python
# Stream: one vector at a time, numpy array GC'd after .tolist()
def embed_stream(self, texts: Iterator[str]) -> Iterator[list[float]]:
    for chunk in batched(texts, self._onnx_batch_size):
        for embedding in self._model.embed(list(chunk), batch_size=self._onnx_batch_size):
            yield embedding.tolist()
```

See `craft-tools:python-hex` reference for the full streaming pipeline pattern.

### Lazy Model Loading

```python
from functools import cached_property

@cached_property
def model(self):
    from fastembed import TextEmbedding
    return TextEmbedding(model_name=self._model_name, threads=self._onnx_threads)
```

### Query-Time Embedding

```python
def search(query: str):
    embedder = get_embedder()
    query_vec = next(embedder.embed_stream(iter([query])))
    return corpus.semantic_search(query_vec)
```

---

## What NOT to Do

| Anti-Pattern | Better |
|-------------|--------|
| OpenAI for personal KB | Nomic via fastembed (free, local, comparable quality) |
| 1024+ dims for text | 768 dims (diminishing returns after this) |
| `list()` on embed generator in bulk | `yield from` — stream and write each immediately |
| sentence-transformers (torch) | fastembed (ONNX) — 285MB vs 2GB, 12x faster |
| Default ONNX batch_size for bulk | Explicit batch_size=4, threads=2 via settings |
| Re-embed on every query | Cache query embeddings |
| Random batch ordering for ONNX | Sort by content length — 3-8x speedup from less padding |
| `WHERE col IS NULL LIMIT N` in loop | Pre-fetch IDs, cursor by ID — avoids O(n²) scan degradation |
| Low DuckDB memory_limit during HNSW build | Lift to 8GB for index construction, restore after |

---

## Sources

- [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)
- [Nomic Embed Announcement](https://blog.nomic.ai/posts/nomic-embed-text-v1)
- [Voyage-4 Model Family](https://blog.voyageai.com/2026/01/15/voyage-4/)
- [Best Open-Source Embedding Models](https://www.bentoml.com/blog/a-guide-to-open-source-embedding-models)
- [Embedding Dimension Tradeoffs](https://particula.tech/blog/embedding-dimensions-rag-vector-search)
