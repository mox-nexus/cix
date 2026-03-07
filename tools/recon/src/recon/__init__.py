"""Paper scout for craft-research.

Programmatic usage:

    from recon import ReconConfig, build_pipeline

    config = ReconConfig.web_preset("cognitive forcing functions", Path("sources/"))
    construct = await build_pipeline(config).run()
"""

from recon.config import ReconConfig, build_pipeline

__all__ = ["ReconConfig", "build_pipeline"]
