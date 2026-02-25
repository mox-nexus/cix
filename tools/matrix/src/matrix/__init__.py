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
from .domain.types import AgentResponse, Component, Construct

__all__ = [
    "Agent",
    "AgentResponse",
    "CompilationError",
    "Component",
    "ComponentRegistry",
    "Config",
    "Construct",
    "DagCompiler",
    "DagScheduler",
    "MatrixConfig",
    "Orchestrator",
    "deep_merge",
    "discover_sources",
    "load_config",
]
