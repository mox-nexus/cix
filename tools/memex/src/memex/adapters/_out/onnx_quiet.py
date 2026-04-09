"""Suppress CoreML native stderr noise on macOS.

CoreML ONNX Runtime provider writes benign warnings to file descriptor 2
(not Python stderr — raw C fprintf). These include:
- "IsInputSupported: CoreML does not support shapes with dimension values of 0"
- "Context leak detected, msgtracer returned -1"

Both are harmless — unsupported ops fall back to CPU. But they pollute
terminal output. This module provides a context manager to silence them.
"""

import os
import sys
from contextlib import contextmanager

_IS_MACOS = sys.platform == "darwin"


@contextmanager
def suppress_native_stderr():
    """Redirect file descriptor 2 to /dev/null during ONNX operations.

    Only active on macOS (where CoreML provider emits native warnings).
    No-op on other platforms.
    """
    if not _IS_MACOS:
        yield
        return

    devnull = os.open(os.devnull, os.O_WRONLY)
    old_stderr = os.dup(2)
    try:
        os.dup2(devnull, 2)
        yield
    finally:
        os.dup2(old_stderr, 2)
        os.close(old_stderr)
        os.close(devnull)
