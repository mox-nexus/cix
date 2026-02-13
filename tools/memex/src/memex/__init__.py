"""Memex - Excavating Collaborative Intelligence Artifacts."""

import os
import warnings

# Suppress HuggingFace Hub noise. All models we use are public.
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
os.environ.setdefault("TQDM_DISABLE", "1")
warnings.filterwarnings("ignore", message=".*unauthenticated.*")
warnings.filterwarnings("ignore", message=".*HF_HUB_DISABLE_PROGRESS_BARS.*")

__version__ = "0.2.0-experimental"
__status__ = "experimental"  # stable, beta, experimental, deprecated
