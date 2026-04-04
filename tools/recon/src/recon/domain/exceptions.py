"""Recon domain exceptions."""


class ReconError(Exception):
    """Base for all recon errors."""


class ConfigError(ReconError):
    """Invalid configuration."""


class CollectionError(ReconError):
    """Collection failed."""
