"""Recon domain — pure types and port definitions."""

from recon.domain.types import Paper, WebSource
from recon.domain.ports import SearchPort, DownloadPort, ConvertPort, WebSearchPort, WebFetchPort

__all__ = [
    "Paper",
    "WebSource",
    "SearchPort",
    "DownloadPort",
    "ConvertPort",
    "WebSearchPort",
    "WebFetchPort",
]
