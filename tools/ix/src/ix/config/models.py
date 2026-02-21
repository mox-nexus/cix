"""ix config model — client config for Matrix composition.

Provides platform-level defaults for ix experiments.
Per-experiment settings in experiment.yaml override these.
"""

from pydantic import BaseModel, ConfigDict


class IxConfig(BaseModel):
    """ix platform config.

    These are defaults. experiment.yaml overrides per-experiment.
    Matrix config (runtime.model, runtime.max_tokens) is separate.
    """

    model_config = ConfigDict(frozen=True)

    default_trials: int = 5
    default_sensor: str = "activation"
