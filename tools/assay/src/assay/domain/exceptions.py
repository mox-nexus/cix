"""Domain exceptions for assay."""


class AssayError(Exception):
    """Base error type for assay."""


class MechanismError(AssayError):
    """A mechanism failed to produce a MechanismResult (timeout, parse failure)."""


class InquiryConfigError(AssayError):
    """Inquiry YAML is malformed or references missing files."""


class AdjudicationError(AssayError):
    """Adjudication could not be computed."""
