"""Driven ports - interfaces for what cix needs from external systems."""

from cix.ports.out.registry import RegistryPort
from cix.ports.out.repository import SourcePort
from cix.ports.out.scanner import ScannerPort
from cix.ports.out.target import TargetPort

__all__ = [
    "RegistryPort",
    "SourcePort",
    "ScannerPort",
    "TargetPort",
]
