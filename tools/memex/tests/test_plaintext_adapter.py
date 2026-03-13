"""Tests for plaintext source adapter."""

from pathlib import Path

from memex.adapters._out.sources.plaintext import PlaintextAdapter


class TestPlaintextAdapter:
    def setup_method(self):
        self.adapter = PlaintextAdapter()

    def test_can_handle_markdown(self, tmp_path):
        f = tmp_path / "doc.md"
        f.write_text("# Hello")
        assert self.adapter.can_handle(f) is True

    def test_can_handle_txt(self, tmp_path):
        f = tmp_path / "notes.txt"
        f.write_text("some notes")
        assert self.adapter.can_handle(f) is True

    def test_can_handle_python(self, tmp_path):
        f = tmp_path / "script.py"
        f.write_text("print('hello')")
        assert self.adapter.can_handle(f) is True

    def test_cannot_handle_binary(self, tmp_path):
        f = tmp_path / "image.png"
        f.write_bytes(b"\x89PNG")
        assert self.adapter.can_handle(f) is False

    def test_cannot_handle_pdf_without_dep(self, tmp_path):
        """PDF requires pymupdf — should return False if not installed."""
        f = tmp_path / "doc.pdf"
        f.write_bytes(b"%PDF-1.4")
        # May or may not handle depending on whether pymupdf is installed
        # Just verify it doesn't crash
        self.adapter.can_handle(f)

    def test_source_kind(self):
        assert self.adapter.source_kind() == "plaintext"

    def test_ingest_plain_text(self, tmp_path):
        f = tmp_path / "notes.txt"
        f.write_text("This is a plain text file with enough content to be meaningful and pass the minimum fragment length check.")
        fragments = list(self.adapter.ingest(f))
        assert len(fragments) == 1
        assert fragments[0].role == "document"
        assert "plain text file" in fragments[0].content
        assert fragments[0].provenance.source_kind == "plaintext"

    def test_ingest_markdown_splits_by_heading(self, tmp_path):
        f = tmp_path / "doc.md"
        f.write_text(
            "# Introduction\n\n"
            "This is the introduction section with enough content to pass the minimum length requirement for fragment creation.\n\n"
            "## Methods\n\n"
            "This is the methods section with detailed description of approaches used in this study and their justification.\n\n"
            "## Results\n\n"
            "These are the results of the analysis including key findings and their statistical significance.\n"
        )
        fragments = list(self.adapter.ingest(f))
        assert len(fragments) == 3
        # Verify sections are captured
        contents = [f.content for f in fragments]
        assert any("Introduction" in c for c in contents)
        assert any("Methods" in c for c in contents)
        assert any("Results" in c for c in contents)

    def test_ingest_empty_file_yields_nothing(self, tmp_path):
        f = tmp_path / "empty.md"
        f.write_text("")
        fragments = list(self.adapter.ingest(f))
        assert len(fragments) == 0

    def test_ingest_idempotent_ids(self, tmp_path):
        """Same file produces same fragment IDs (stable hashing)."""
        f = tmp_path / "doc.md"
        f.write_text("This is content with enough text to pass the minimum fragment length check for the plaintext adapter.")
        ids_first = [frag.id for frag in self.adapter.ingest(f)]
        ids_second = [frag.id for frag in self.adapter.ingest(f)]
        assert ids_first == ids_second

    def test_ingest_skips_trivial_sections(self, tmp_path):
        f = tmp_path / "doc.md"
        f.write_text(
            "# Title\n\n"
            "Short.\n\n"  # Too short, should be skipped
            "## Real Section\n\n"
            "This section has enough content to be meaningful as a fragment and should be included in the output.\n"
        )
        fragments = list(self.adapter.ingest(f))
        # "Short." section should be skipped (< 50 chars)
        assert all("Short." not in f.content for f in fragments)

    def test_conversation_id_is_file_path(self, tmp_path):
        f = tmp_path / "doc.txt"
        f.write_text("Enough content here to create a fragment that meets the minimum length requirement for the adapter.")
        fragments = list(self.adapter.ingest(f))
        assert fragments[0].conversation_id == str(f.resolve())
