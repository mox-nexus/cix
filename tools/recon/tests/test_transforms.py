"""Tests for transforms — glom-based path resolution + normalize specs."""

from recon.application.transforms import (
    apply_normalize,
    first,
    html2text,
    inverted_index,
    join,
    resolve_path,
)


class TestHtml2Text:
    def test_basic(self):
        assert html2text("<p>Hello</p>") == "Hello"

    def test_strips_scripts(self):
        html = "<p>Keep</p><script>remove();</script><p>Also keep</p>"
        result = html2text(html)
        assert "Keep" in result
        assert "Also keep" in result
        assert "remove" not in result

    def test_empty(self):
        assert html2text("") == ""
        assert html2text(None) == ""


class TestInvertedIndex:
    def test_basic(self):
        idx = {"hello": [0], "world": [1]}
        assert inverted_index(idx) == "hello world"

    def test_repeated_words(self):
        idx = {"the": [0, 3], "cat": [1], "sat": [2]}
        assert inverted_index(idx) == "the cat sat the"

    def test_empty(self):
        assert inverted_index({}) == ""
        assert inverted_index(None) == ""


class TestJoin:
    def test_basic(self):
        assert join(["a", "b", "c"]) == "a, b, c"

    def test_empty(self):
        assert join([]) == ""
        assert join(None) == ""


class TestFirst:
    def test_basic(self):
        assert first([1, 2, 3]) == 1

    def test_empty(self):
        assert first([]) is None
        assert first(None) is None


class TestResolvePath:
    def test_direct(self):
        assert resolve_path({"title": "Test"}, "title") == "Test"

    def test_nested(self):
        data = {"openAccessPdf": {"url": "https://example.com/paper.pdf"}}
        assert resolve_path(data, "openAccessPdf.url") == "https://example.com/paper.pdf"

    def test_list_map(self):
        data = {"authors": [{"name": "Alice"}, {"name": "Bob"}]}
        assert resolve_path(data, "authors.*.name") == ["Alice", "Bob"]

    def test_deep_list_map(self):
        data = {
            "authorships": [
                {"author": {"display_name": "Alice"}},
                {"author": {"display_name": "Bob"}},
            ]
        }
        assert resolve_path(data, "authorships.*.author.display_name") == ["Alice", "Bob"]

    def test_missing_field(self):
        assert resolve_path({"a": 1}, "b") is None
        assert resolve_path({"a": 1}, "a.b") is None

    def test_none_data(self):
        assert resolve_path(None, "x") is None


class TestApplyNormalize:
    def test_s2_shape(self):
        """Simulates Semantic Scholar API response normalization."""
        raw = {
            "title": "Attention Is All You Need",
            "abstract": "The dominant...",
            "authors": [{"name": "Vaswani"}, {"name": "Shazeer"}],
            "year": 2017,
            "citationCount": 90000,
            "openAccessPdf": {"url": "https://arxiv.org/pdf/1706.03762"},
            "venue": "NeurIPS",
        }
        spec = {
            "title": "title",
            "abstract": "abstract",
            "authors": "authors.*.name",
            "year": "year",
            "citations": "citationCount",
            "pdf_url": "openAccessPdf.url",
            "venue": "venue",
        }
        result = apply_normalize(raw, spec)
        assert result["title"] == "Attention Is All You Need"
        assert result["authors"] == ["Vaswani", "Shazeer"]
        assert result["citations"] == 90000
        assert result["pdf_url"] == "https://arxiv.org/pdf/1706.03762"

    def test_openalex_shape(self):
        """Simulates OpenAlex API response normalization with $inverted_index."""
        raw = {
            "display_name": "Test Paper",
            "abstract_inverted_index": {"hello": [0], "world": [1]},
            "authorships": [{"author": {"display_name": "Alice"}}],
            "publication_year": 2024,
            "cited_by_count": 42,
        }
        spec = {
            "title": "display_name",
            "abstract": "abstract_inverted_index|$inverted_index",
            "authors": "authorships.*.author.display_name",
            "year": "publication_year",
            "citations": "cited_by_count",
        }
        result = apply_normalize(raw, spec)
        assert result["title"] == "Test Paper"
        assert result["abstract"] == "hello world"
        assert result["authors"] == ["Alice"]

    def test_zenodo_shape(self):
        """Simulates Zenodo normalization with $html2text."""
        raw = {
            "metadata": {
                "title": "Dataset",
                "description": "<p>A <b>dataset</b> for testing.</p>",
                "creators": [{"name": "Bob"}],
            },
        }
        spec = {
            "title": "metadata.title",
            "abstract": "metadata.description|$html2text",
            "authors": "metadata.creators.*.name",
        }
        result = apply_normalize(raw, spec)
        assert result["title"] == "Dataset"
        assert result["abstract"] == "A dataset for testing."
        assert result["authors"] == ["Bob"]

    def test_missing_transform(self):
        """Unknown transforms are silently skipped."""
        raw = {"x": "hello"}
        result = apply_normalize(raw, {"x": "x|$nonexistent"})
        assert result["x"] == "hello"


class TestPdf2Text:
    """Test $pdf2text transform via pymupdf (registered by CLI composition root)."""

    def test_roundtrip(self, tmp_path):
        """Create a PDF with pymupdf, extract text with $pdf2text."""
        import pymupdf
        from recon.adapters._in.cli import _pdf2text

        # Create a test PDF
        doc = pymupdf.open()
        page = doc.new_page()
        page.insert_text((72, 72), "Recon extraction test.", fontsize=14)
        pdf_path = tmp_path / "test.pdf"
        doc.save(str(pdf_path))
        doc.close()

        text = _pdf2text(str(pdf_path))
        assert "Recon extraction test." in text

    def test_missing_file(self):
        """Non-existent file returns empty string."""
        from recon.adapters._in.cli import _pdf2text

        assert _pdf2text("/nonexistent/file.pdf") == ""
