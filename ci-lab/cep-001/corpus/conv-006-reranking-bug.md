# Reranking Bug: Scores Inverted

**Date**: 2025-02-10
**Participants**: yza, claude

yza: Search results are weird — the most relevant results are at the bottom. Something's wrong with reranking.

claude: Let me check the reranking pipeline. The cross-encoder returns scores where higher = more relevant. But the sort is... ascending.

Found it. In `search.py` line 142:
```python
results.sort(key=lambda r: r.rerank_score)
```

Should be:
```python
results.sort(key=lambda r: r.rerank_score, reverse=True)
```

The BM25 + semantic scores were correct (higher = better), but after reranking, the sort order inverted everything.

yza: How long has this been broken?

claude: Since the reranking feature was added in commit `a3f7e21`. About 2 weeks. The initial search (without reranking) worked fine — this only affects the `--no-rerank=False` path (the default).

**Fix**: Added `reverse=True` to the reranking sort in `search.py:142`.

**Key fact**: The bug was in commit a3f7e21, and the cross-encoder model is Xenova/ms-marco-MiniLM-L-6-v2.
