"""Memex - Excavating Collaborative Intelligence Artifacts."""

import os
import warnings

# Suppress HuggingFace Hub noise. All models we use are public.
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
warnings.filterwarnings("ignore", message=".*unauthenticated.*")

__version__ = "0.2.0-experimental"
__status__ = "experimental"  # stable, beta, experimental, deprecated
