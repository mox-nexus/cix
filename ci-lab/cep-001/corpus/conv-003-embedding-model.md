# Embedding Model Selection

**Date**: 2025-02-01
**Participants**: user, claude

user: We need to pick an embedding model for memex semantic search. Options: OpenAI ada-002, Cohere embed-v3, nomic-embed-text-v1.5, or BGE-large.

claude: Key dimensions:
- **ada-002**: 1536-dim, cloud-only, $0.0001/1K tokens. Great quality but requires API calls.
- **Cohere embed-v3**: 1024-dim, cloud-only, comparable quality. Matryoshka support.
- **nomic-embed-text-v1.5**: 768-dim, runs locally via ONNX. Open-source, Matryoshka dimensions.
- **BGE-large**: 1024-dim, runs locally. Excellent MTEB scores.

user: Local inference is non-negotiable. We can't depend on cloud APIs for search — it needs to work offline.

claude: That narrows it to nomic and BGE. nomic-embed-text-v1.5 advantages:
- Matryoshka representations (can truncate dimensions for speed)
- ONNX + CoreML acceleration on macOS
- 768-dim is more storage-efficient than BGE's 1024
- Comparable MTEB scores to BGE-large

**Decision**: nomic-ai/nomic-embed-text-v1.5. Rationale: local inference, CoreML acceleration, Matryoshka flexibility, storage efficiency at 768 dimensions.

**Key fact**: At 768 dimensions with CoreML, encoding 1000 fragments takes approximately 4.2 seconds on M2.
