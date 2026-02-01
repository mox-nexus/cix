"""Output ports - what the domain needs from infrastructure."""

from memex.domain.ports._out.corpus import CorpusPort
from memex.domain.ports._out.source import SourceAdapterPort

__all__ = ["SourceAdapterPort", "CorpusPort"]
