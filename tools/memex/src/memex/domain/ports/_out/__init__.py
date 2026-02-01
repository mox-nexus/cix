"""Output ports - what the domain needs from infrastructure."""

from memex.domain.ports._out.source import SourceAdapterPort
from memex.domain.ports._out.corpus import CorpusPort

__all__ = ["SourceAdapterPort", "CorpusPort"]
