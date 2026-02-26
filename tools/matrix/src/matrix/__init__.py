"""Matrix: Component runtime for DAG execution.

Kind-agnostic. Components in, results out.
Also provides Agent protocol and AgentResponse for agent execution.
"""

from .composition.config import deep_merge, discover_sources, load_config
from .domain.compiler import CompilationError, DagCompiler
from .domain.config import Config, MatrixConfig
from .domain.orchestrator import Orchestrator
from .domain.ports._out.runtime import Agent
from .domain.registry import ComponentRegistry
from .domain.scheduler import DagScheduler
from .domain.types import AgentResponse, Artifact, Component, Construct, ContractError, TypedStruct


def configure_telemetry(**kwargs):
    """Configure OpenTelemetry SDK. Requires: uv add matrix[otel]"""
    from .composition.telemetry import configure_telemetry as _configure

    return _configure(**kwargs)


__all__ = [
    "Agent",
    "AgentResponse",
    "Artifact",
    "CompilationError",
    "Component",
    "ComponentRegistry",
    "Config",
    "configure_telemetry",
    "Construct",
    "ContractError",
    "DagCompiler",
    "DagScheduler",
    "MatrixConfig",
    "Orchestrator",
    "TypedStruct",
    "deep_merge",
    "discover_sources",
    "load_config",
]
