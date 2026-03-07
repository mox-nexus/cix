"""pdftotext adapter — implements ConvertPort."""

from __future__ import annotations

import subprocess
from pathlib import Path


class PdftotextAdapter:
    """ConvertPort implementation via poppler's pdftotext."""

    def to_text(self, pdf_path: Path, output_dir: Path | None = None) -> Path | None:
        if not pdf_path.exists():
            return None

        out_dir = output_dir or pdf_path.parent
        out_dir.mkdir(parents=True, exist_ok=True)
        txt_path = out_dir / f"{pdf_path.stem}.txt"

        if self._run(pdf_path, txt_path, layout=True):
            return txt_path
        if self._run(pdf_path, txt_path, layout=False):
            return txt_path
        return None

    def _run(self, pdf_path: Path, txt_path: Path, *, layout: bool) -> bool:
        cmd = ["pdftotext"]
        if layout:
            cmd.append("-layout")
        cmd.extend([str(pdf_path), str(txt_path)])

        try:
            result = subprocess.run(cmd, capture_output=True, timeout=60)
            return result.returncode == 0 and txt_path.exists() and txt_path.stat().st_size > 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
