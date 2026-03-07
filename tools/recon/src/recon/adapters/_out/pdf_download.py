"""PDF download adapter — implements DownloadPort."""

from __future__ import annotations

from pathlib import Path

import httpx

from recon.domain.types import Paper

_UNPAYWALL_EMAIL = "mox.rnd@gmail.com"


class PdfDownloadAdapter:
    """DownloadPort implementation. Tries S2 OA → arXiv → Unpaywall."""

    def download(self, paper: Paper, output_dir: Path) -> Path | None:
        output_dir.mkdir(parents=True, exist_ok=True)
        pdf_path = output_dir / f"{paper.slug}.pdf"

        if pdf_path.exists():
            return pdf_path

        url = self._find_url(paper)
        if not url:
            return None

        try:
            with httpx.Client(follow_redirects=True, timeout=60) as client:
                resp = client.get(url)
                resp.raise_for_status()

                content_type = resp.headers.get("content-type", "")
                if "pdf" not in content_type and resp.content[:5] != b"%PDF-":
                    return None

                pdf_path.write_bytes(resp.content)
                return pdf_path
        except (httpx.HTTPError, OSError):
            return None

    def _find_url(self, paper: Paper) -> str | None:
        if paper.open_access_url:
            return paper.open_access_url
        if paper.arxiv_id:
            return f"https://arxiv.org/pdf/{paper.arxiv_id}"
        if paper.doi:
            return self._try_unpaywall(paper.doi)
        return None

    def _try_unpaywall(self, doi: str) -> str | None:
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.get(
                    f"https://api.unpaywall.org/v2/{doi}",
                    params={"email": _UNPAYWALL_EMAIL},
                )
                resp.raise_for_status()
                data = resp.json()
                best_oa = data.get("best_oa_location") or {}
                return best_oa.get("url_for_pdf")
        except (httpx.HTTPError, KeyError, ValueError):
            return None
