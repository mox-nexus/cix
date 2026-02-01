"""Excavation service - use case orchestration.

Orchestrates ingestion and search through ports (Burner).
Uses domain types only, no infrastructure leakage.
"""

from collections.abc import Callable
from pathlib import Path

from memex.domain.models import Fragment
from memex.domain.ports._out.corpus import CorpusPort
from memex.domain.ports._out.source import SourceAdapterPort


class ExcavationService:
    """Orchestrates excavation use cases.

    Connects source adapters to corpus storage through ports.
    """

    def __init__(
        self,
        corpus: CorpusPort,
        source_adapters: list[SourceAdapterPort],
    ):
        self.corpus = corpus
        self.source_adapters = source_adapters

    def ingest(
        self,
        path: Path,
        on_progress: Callable[[int], None] | None = None,
    ) -> int:
        """Ingest a file into the corpus.

        Returns count of fragments stored.
        """
        adapter = self._find_adapter(path)
        if not adapter:
            raise ValueError(f"No adapter found for {path}")

        # Count fragments for progress reporting
        fragment_count = 0

        def counting_generator():
            nonlocal fragment_count
            for fragment in adapter.ingest(path):
                fragment_count += 1
                yield fragment

        # Store fragments (adapter yields Iterator[Fragment])
        stored = self.corpus.store(counting_generator())

        if on_progress:
            on_progress(fragment_count)

        return stored

    def search(self, query: str, limit: int = 20) -> list[Fragment]:
        """Search the corpus."""
        return self.corpus.search(query, limit)

    def find_conversation(self, conversation_id: str) -> list[Fragment]:
        """Get all fragments in a conversation."""
        return self.corpus.find_by_conversation(conversation_id)

    def stats(self) -> dict:
        """Get corpus statistics."""
        return self.corpus.stats()

    def schema(self) -> dict:
        """Get corpus schema."""
        return self.corpus.schema()

    def available_sources(self) -> list[str]:
        """List available source adapters."""
        return [adapter.source_kind() for adapter in self.source_adapters]

    def get_source_skill(self, source_kind: str) -> str | None:
        """Get skill documentation for a source adapter."""
        for adapter in self.source_adapters:
            if adapter.source_kind() == source_kind:
                return adapter.skill()
        return None

    def get_corpus_skill(self) -> str:
        """Get skill documentation for the corpus."""
        return self.corpus.skill()

    def _find_adapter(self, path: Path) -> SourceAdapterPort | None:
        for adapter in self.source_adapters:
            if adapter.can_handle(path):
                return adapter
        return None
