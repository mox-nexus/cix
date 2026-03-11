#!/usr/bin/env python3
"""nexus — knowledge artifact manager.

A CLI tool with both --help and --skill output modes.
Used as the test fixture for the skill-vs-help experiment:
does an agent use a tool better when reading --skill vs --help?
"""

import sys

HELP_OUTPUT = """\
Usage: nexus [OPTIONS] COMMAND [ARGS]...

  nexus — knowledge artifact manager

Commands:
  excavate    Hybrid search (semantic + keyword fusion, RRF)
  locate      Exact match lookup by ID, path, or hash
  survey      Statistical overview and health check of corpus
  absorb      Ingest artifacts from files, directories, or streams
  connect     Create typed edges between artifacts
  trace       Follow a trail of connected artifacts

Options:
  --corpus PATH   Corpus path [default: .nexus/corpus.duckdb]
  --verbose       Enable debug logging
  --help          Show this message and exit

nexus excavate --help
  Usage: nexus excavate [OPTIONS] QUERY
  Options:
    --limit INT        Max results [default: 20]
    --source TEXT       Filter by source type
    --min-score FLOAT   Minimum relevance [default: 0.0]

nexus locate --help
  Usage: nexus locate [OPTIONS] IDENTIFIER
  Options:
    --by [id|path|hash]  Lookup method [default: id]
    --exact              Require exact match

nexus survey --help
  Usage: nexus survey [OPTIONS]
  Options:
    --format [table|json]  Output format [default: table]
    --section TEXT          Specific section to survey

nexus absorb --help
  Usage: nexus absorb [OPTIONS] SOURCE
  Options:
    --format [auto|json|csv|jsonl|md]  Input format [default: auto]
    --batch-size INT                    Docs per batch [default: 1000]
    --embed / --no-embed                Generate embeddings [default: embed]

nexus connect --help
  Usage: nexus connect [OPTIONS] SOURCE_ID TARGET_ID
  Options:
    --type [follows|similar|references|contradicts]  Edge type [default: references]
    --weight FLOAT  Edge weight [default: 1.0]
    --bidirectional  Create edge in both directions

nexus trace --help
  Usage: nexus trace [OPTIONS] START_ID
  Options:
    --depth INT      Max hops [default: 3]
    --edge-type TEXT  Filter by edge type
    --format [tree|flat|json]  Output format [default: tree]
"""

SKILL_OUTPUT = """\
# nexus — Knowledge Artifact Manager

## Capabilities

### excavate (search)
**When to use**: You need to FIND something but don't know exactly where it is
or what it's called. Works like a research assistant — understands meaning,
not just keywords. Best default when you're exploring.

**How it works**: Combines semantic understanding (embedding similarity) with
keyword matching (BM25), fused via Reciprocal Rank Fusion. Finds conceptually
related results even when wording differs.

**Example tasks**: "find discussions about auth decisions", "search for
performance-related conversations", "where did we talk about deployment?"

### locate (lookup)
**When to use**: You KNOW the specific artifact — you have its ID, file path,
or content hash. This is a direct lookup, not a search. Use when you need to
retrieve a specific known item, not discover unknown ones.

**How it works**: Direct index lookup by identifier. No ranking, no relevance
scoring — either finds the exact match or returns nothing.

**Example tasks**: "get artifact abc-123", "find the file at path/to/doc.md",
"look up hash 7f3a..."

### survey (overview)
**When to use**: You want to understand the STATE of the corpus — how many
artifacts, what types, what's embedded, what's not, health metrics. Use before
deciding what to do, not to find specific content.

**How it works**: Aggregates metadata across the corpus. No content search.

**Example tasks**: "how big is my corpus?", "what source types do I have?",
"are there un-embedded artifacts?"

### absorb (ingest)
**When to use**: You need to ADD new content to the corpus. Takes files,
directories, or streams and converts them into indexed artifacts.

**How it works**: Parses input format, chunks into artifacts, stores in
DuckDB, optionally generates embeddings. Idempotent — duplicate IDs are
safely ignored.

**Example tasks**: "import this JSON export", "add these markdown files",
"ingest the CSV data"

### connect (link)
**When to use**: You want to create an EXPLICIT relationship between two
artifacts. Different from search similarity — these are human-asserted
connections with typed semantics.

**Edge types**:
- `follows`: temporal sequence (A came after B)
- `similar`: conceptual similarity (human-asserted, not embedding)
- `references`: A cites or builds on B
- `contradicts`: A disagrees with B

**Example tasks**: "link these two discussions", "mark this as contradicting
that earlier decision", "connect the follow-up to the original"

### trace (navigate)
**When to use**: You want to FOLLOW connections from a starting point. Like
walking a graph — start at one artifact, see what it connects to, and keep
going. Good for understanding context and provenance.

**How it works**: Breadth-first traversal from start node, filtered by edge
type and depth. Shows the connected subgraph.

**Example tasks**: "what's connected to this decision?", "trace the history
of this design choice", "show me everything related to artifact X"
"""

if __name__ == "__main__":
    if len(sys.argv) < 2 or "--help" in sys.argv:
        print(HELP_OUTPUT)
    elif "--skill" in sys.argv:
        print(SKILL_OUTPUT)
    else:
        print(f"Unknown command: {' '.join(sys.argv[1:])}")
        print("Use --help or --skill for documentation")
        sys.exit(1)
