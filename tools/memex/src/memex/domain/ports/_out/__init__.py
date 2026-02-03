"""Output ports - what the domain needs from infrastructure."""

from memex.domain.ports._out.corpus import CorpusPort
from memex.domain.ports._out.embedding import EmbeddingPort
from memex.domain.ports._out.reranker import RerankerPort
from memex.domain.ports._out.source import SourceAdapterPort

__all__ = ["SourceAdapterPort", "CorpusPort", "EmbeddingPort", "RerankerPort"]
