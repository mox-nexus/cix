#!/usr/bin/env python3
"""OpenAlex API recon sweeps for Stream C."""

import json
import time
import urllib.request
import urllib.parse
import sys

OUTPUT_DIR = "/Users/yza.vyas/mox/products/cix-memex-next-lance/research/stream-c-landscape/data/sweep-1"

QUERIES = [
    {
        "file": "openalex-c1-rag-survey.jsonl",
        "search": '"retrieval augmented generation" survey',
        "filter": "publication_year:2022-2026",
    },
    {
        "file": "openalex-c1-memory-agents.jsonl",
        "search": '"memory augmented" "large language model" agent',
        "filter": "publication_year:2022-2026",
    },
    {
        "file": "openalex-c1-memgpt.jsonl",
        "search": 'MemGPT OR Letta OR "hierarchical memory" "language model"',
        "filter": "publication_year:2022-2026",
    },
    {
        "file": "openalex-c2-hybrid-retrieval.jsonl",
        "search": '"hybrid retrieval" dense sparse',
        "filter": "publication_year:2022-2026",
    },
    {
        "file": "openalex-c2-contextual-retrieval.jsonl",
        "search": '"contextual retrieval" OR "context-aware retrieval" language model',
        "filter": "publication_year:2022-2026",
    },
    {
        "file": "openalex-c2-reranking.jsonl",
        "search": '"cross-encoder" reranking retrieval',
        "filter": "publication_year:2022-2026",
    },
    {
        "file": "openalex-c3-vector-db.jsonl",
        "search": '"vector database" OR "vector search" benchmark',
        "filter": "publication_year:2022-2026",
    },
    {
        "file": "openalex-c3-embeddings.jsonl",
        "search": 'embedding model "text retrieval" benchmark MTEB',
        "filter": "publication_year:2022-2026",
    },
    {
        "file": "openalex-c4-pkm.jsonl",
        "search": '"personal knowledge management" OR "personal information management" tool',
        "filter": "publication_year:2018-2026",
    },
    {
        "file": "openalex-c1-conversational-memory.jsonl",
        "search": '"conversational memory" OR "dialogue memory" system',
        "filter": "publication_year:2022-2026",
    },
]


def reconstruct_abstract(inverted_index):
    """Reconstruct abstract text from OpenAlex inverted index format."""
    if not inverted_index:
        return None
    word_positions = []
    for word, positions in inverted_index.items():
        for pos in positions:
            word_positions.append((pos, word))
    word_positions.sort(key=lambda x: x[0])
    return " ".join(w for _, w in word_positions)


def extract_work(work):
    """Extract relevant fields from an OpenAlex work record."""
    first_author = None
    if work.get("authorships") and len(work["authorships"]) > 0:
        author_info = work["authorships"][0].get("author", {})
        first_author = author_info.get("display_name")

    abstract = reconstruct_abstract(work.get("abstract_inverted_index"))

    return {
        "id": work.get("id"),
        "title": work.get("title"),
        "publication_year": work.get("publication_year"),
        "cited_by_count": work.get("cited_by_count"),
        "first_author": first_author,
        "doi": work.get("doi"),
        "abstract": abstract,
    }


def run_query(query_spec):
    """Run a single OpenAlex query and save results."""
    params = {
        "search": query_spec["search"],
        "per_page": "50",
        "sort": "cited_by_count:desc",
        "filter": query_spec["filter"],
        "mailto": "yza.vyas@gmail.com",
    }
    url = "https://api.openalex.org/works?" + urllib.parse.urlencode(params)

    print(f"  Query: {query_spec['search'][:60]}...")
    print(f"  URL: {url[:120]}...")

    req = urllib.request.Request(url, headers={"User-Agent": "CIX-Memex-Research/1.0 (mailto:yza.vyas@gmail.com)"})

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"  ERROR: {e}")
        return 0

    results = data.get("results", [])
    total = data.get("meta", {}).get("count", 0)

    outpath = f"{OUTPUT_DIR}/{query_spec['file']}"
    with open(outpath, "w") as f:
        for work in results:
            record = extract_work(work)
            f.write(json.dumps(record) + "\n")

    print(f"  Total available: {total}, saved: {len(results)}")
    return len(results)


def main():
    print("=== OpenAlex Recon Sweeps: Stream C ===\n")
    summary = []

    for i, q in enumerate(QUERIES, 1):
        print(f"[{i}/{len(QUERIES)}] {q['file']}")
        count = run_query(q)
        summary.append({"file": q["file"], "search": q["search"], "filter": q["filter"], "results_saved": count})
        if i < len(QUERIES):
            time.sleep(0.5)  # polite rate limiting
        print()

    # Write meta.yaml
    meta_path = f"{OUTPUT_DIR}/meta.yaml"
    with open(meta_path, "w") as f:
        f.write("# Stream C Landscape Recon — Sweep 1\n")
        f.write(f"# Collected: 2026-04-13\n")
        f.write(f"# Source: OpenAlex API (https://api.openalex.org/works)\n")
        f.write(f"# Sort: cited_by_count:desc\n")
        f.write(f"# Per page: 50\n\n")
        f.write("sweeps:\n")
        for s in summary:
            f.write(f"  - file: {s['file']}\n")
            f.write(f"    search: \"{s['search']}\"\n")
            f.write(f"    filter: \"{s['filter']}\"\n")
            f.write(f"    results_saved: {s['results_saved']}\n")
        f.write(f"\ntotal_files: {len(summary)}\n")
        total_records = sum(s["results_saved"] for s in summary)
        f.write(f"total_records: {total_records}\n")

    print(f"Done. {len(summary)} queries, {sum(s['results_saved'] for s in summary)} total records.")
    print(f"Meta written to {meta_path}")


if __name__ == "__main__":
    main()
