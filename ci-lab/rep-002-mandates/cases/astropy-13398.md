---
id: astropy-13398
expectation: must_pass
rationale: Medium SWE-bench task — coordinate transformation. Tests deeper code understanding.
difficulty: medium
source: swebench-verified
repo: astropy/astropy
base_commit: "3832210580d516eb3e2eea31e00a023174e tried"
fail_to_pass:
  - "astropy/coordinates/tests/test_earth.py::test_itrs_topocentric"
pass_to_pass:
  - "astropy/coordinates/tests/test_earth.py"
---
Support topocentric ITRS frame for coordinate transformations.

Currently, converting an `EarthLocation` to ITRS gives a geocentric position, but there's no straightforward way to get a topocentric ITRS frame (i.e., ITRS centered at a specific location on Earth's surface).

This is needed for satellite tracking and ground-based observations where you want positions relative to an observer, not the Earth's center.

Add support for specifying an `obstime` and `location` in the ITRS frame to enable topocentric transformations, similar to how AltAz works.
