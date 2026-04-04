# Normalize Spec Reference

Normalize specs map API/CLI output fields to uniform output columns. Each entry is `output_column: "source.path|$transform"`.

## Path Syntax

Path resolution uses [glom](https://glom.readthedocs.io/) with our `*` list-map syntax on top.

| Pattern | Meaning | Example |
|---------|---------|---------|
| `field` | Direct access | `title` → `record["title"]` |
| `a.b.c` | Nested dotted path | `openAccessPdf.url` → `record["openAccessPdf"]["url"]` |
| `a.*.b` | List-map | `authors.*.name` → `[author["name"] for author in record["authors"]]` |
| `a.*.b.c` | Deep list-map | `authorships.*.author.display_name` |
| `a.*` | Bare list | `items.*` → the list itself |

Missing fields return `None` (no error).

### Examples from Real APIs

```yaml
# Semantic Scholar
title: title                          # direct
authors: "authors.*.name"             # list-map
pdf_url: "openAccessPdf.url"          # nested
citations: citationCount              # rename

# OpenAlex
title: display_name                   # rename
authors: "authorships.*.author.display_name"  # deep list-map
abstract: "abstract_inverted_index|$inverted_index"  # path + transform

# Zenodo
title: "metadata.title"              # nested
authors: "metadata.creators.*.name"  # nested + list-map
abstract: "metadata.description|$html2text"  # nested + transform

# arXiv (after xmltodict)
venue: "arxiv:primary_category.@term"  # XML attribute key
authors: "author.*.name"              # list-map
```

## Pipe Syntax

Append `|$transform` to apply a transform after path resolution:

```yaml
abstract: "metadata.description|$html2text"
#          ^^^^^^^^^^^^^^^^^^^^^ ^^^^^^^^^
#          path                   transform
```

The pipe is always `|` (no spaces required). Transform names start with `$`.

## Built-in Transforms

| Transform | Input | Output | Use case |
|-----------|-------|--------|----------|
| `$html2text` | HTML string | Plain text | Strip tags from API descriptions |
| `$inverted_index` | `{"word": [pos, ...]}` | Reconstructed text | OpenAlex abstract format |
| `$join` | `list` | `str` (comma-separated) | Flatten author lists to string |
| `$first` | `list` | First element or `None` | Extract first match from ripgrep |
| `$pdf2text` | File path string | Extracted text | PDF content extraction (pymupdf) |

### $html2text

Strips HTML tags, scripts, styles. Preserves paragraph breaks. Uses stdlib `html.parser`.

```yaml
description: "content|$html2text"
# "<p>A <b>bold</b> claim.</p>" → "A bold claim."
```

### $inverted_index

Reconstructs text from OpenAlex inverted index format where words map to position arrays.

```yaml
abstract: "abstract_inverted_index|$inverted_index"
# {"hello": [0], "world": [1]} → "hello world"
```

### $join

Joins list elements with `, ` separator.

```yaml
departments: "departments.*.name|$join"
# ["Engineering", "Platform"] → "Engineering, Platform"
```

### $first

Returns first element of a list, or `None` if empty.

```yaml
content: "data.lines.text|$first"
# ["matched line", "context"] → "matched line"
```

### $pdf2text

Extracts text from a PDF file path using pymupdf. Returns empty string if extraction fails.

```yaml
full_text: "pdf_path|$pdf2text"
```

## Response Formats

API collectors support different response formats via `response_format`:

| Format | Parser | Use case |
|--------|--------|----------|
| `json` (default) | `resp.json()` | Most REST APIs |
| `xml` | `xmltodict` with namespace handling | arXiv, PubMed |
| `html` | Raw text | Web pages (planned) |
| `text` | Raw text | Plain text APIs |

### XML Namespace Handling

arXiv responses use XML namespaces. The parser strips common namespaces and prefixes others:

```yaml
response_format: xml
# "http://www.w3.org/2005/Atom" → stripped (no prefix)
# "http://arxiv.org/schemas/atom" → "arxiv:" prefix
```

Access XML attributes with `@` prefix: `"arxiv:primary_category.@term"`.

## Extract Path

The `extract` field navigates to the record array before normalize specs apply:

```yaml
extract: "data"              # S2: response.data[...]
extract: "feed.entry"        # arXiv: response.feed.entry[...]
extract: "results"           # OpenAlex: response.results[...]
extract: "hits.hits"         # Zenodo: response.hits.hits[...]
```

Uses the same dotted-path resolution (via glom). If the extracted value is a single dict, it becomes `[dict]`. Non-dict items in lists are filtered out.
