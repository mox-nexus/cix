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

## Production Patterns

### Batch Embedding for Ingest

```python
# Efficient batch processing
texts = [frag.content for frag in fragments]
embeddings = model.encode(
    texts,
    batch_size=32,
    show_progress_bar=True,
    convert_to_numpy=True
)
```

### Lazy Model Loading

```python
from functools import lru_cache

@lru_cache(maxsize=1)
def get_embedder():
    """Lazy load to avoid startup cost."""
    return SentenceTransformer("nomic-ai/nomic-embed-text-v1.5")
```

### Query-Time Embedding

```python
def search(query: str):
    embedder = get_embedder()
    query_embedding = embedder.encode(query)
    return corpus.semantic_search(query_embedding)
```

---

## What NOT to Do

| ❌ Anti-Pattern | ✅ Better |
|-----------------|-----------|
| OpenAI for personal KB | Nomic (free, local, comparable quality) |
| 1024+ dims for text | 768 dims (diminishing returns) |
| CLIP for text-only | Sentence transformers |
| Re-embed on every query | Cache query embeddings |
| Cohere for cost optimization | Voyage or Nomic |

---

## Sources

- [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)
- [Nomic Embed Announcement](https://blog.nomic.ai/posts/nomic-embed-text-v1)
- [Voyage-4 Model Family](https://blog.voyageai.com/2026/01/15/voyage-4/)
- [Best Open-Source Embedding Models](https://www.bentoml.com/blog/a-guide-to-open-source-embedding-models)
- [Embedding Dimension Tradeoffs](https://particula.tech/blog/embedding-dimensions-rag-vector-search)
