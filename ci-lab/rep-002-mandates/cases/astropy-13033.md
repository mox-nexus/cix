---
id: astropy-13033
expectation: must_pass
rationale: Easy SWE-bench task — exception message fix. Tests minimal focused change.
difficulty: easy
source: swebench-verified
repo: astropy/astropy
base_commit: "298ccb478e6bf092953bca67a3d29dc6c35f6752"
fail_to_pass:
  - "astropy/timeseries/tests/test_common.py::test_empty_timeseries"
pass_to_pass:
  - "astropy/timeseries/tests/test_common.py"
---
TimeSeries required column check exception message is misleading.

When creating an empty TimeSeries, the exception message says:

```
ValueError: TimeSeries object is invalid - expected 'time' as the first column but found 'None'
```

The message "found 'None'" is confusing — the real issue is that the TimeSeries has no columns at all. The error message should distinguish between "wrong first column" and "no columns present."

Fix the exception message in the TimeSeries validation to be accurate when there are no columns.
