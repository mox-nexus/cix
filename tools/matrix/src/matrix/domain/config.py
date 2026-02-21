"""Matrix config types — platform schema + composed config container.

MatrixConfig defines what the platform needs (runtime, storage).
Config[C] composes Matrix settings with a client-provided schema.
"""

from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

C = TypeVar("C", bound=BaseModel)


class RuntimeSettings(BaseModel):
    """Runtime adapter settings."""

    model_config = ConfigDict(frozen=True)

    model: str = "claude-sonnet-4-5-20250929"
    max_tokens: int = 2048


class MatrixConfig(BaseModel):
    """What Matrix needs to operate.

    Platform-level settings. Clients don't define these —
    Matrix owns this schema.
    """

    model_config = ConfigDict(frozen=True)

    runtime: RuntimeSettings = RuntimeSettings()


class Config(BaseModel, Generic[C]):  # noqa: UP046
    """Composed config: Matrix platform settings + client settings.

    Generic over C — the client provides its Pydantic model type.
    Matrix validates its own section, client section validated
    against the client-provided type.
    """

    model_config = ConfigDict(frozen=True)

    matrix: MatrixConfig = MatrixConfig()
    client: C
