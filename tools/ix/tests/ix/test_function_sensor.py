"""Tests for FunctionTestSensor — runs code against test cases."""

from ix.domain.types import Trial
from ix.eval.sensors import FunctionTestSensor

MERGE_INTERVALS_CODE = """
def merge_intervals(intervals):
    if not intervals:
        return []
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1] = [merged[-1][0], max(merged[-1][1], end)]
        else:
            merged.append([start, end])
    return merged
"""

BROKEN_CODE = """
def merge_intervals(intervals):
    return intervals  # wrong — just returns input unchanged
"""

SYNTAX_ERROR_CODE = """
def merge_intervals(intervals)  # missing colon
    return []
"""

GROUND_TRUTH = {
    "merge-001": {
        "function_name": "merge_intervals",
        "test_cases": [
            {
                "input": [[[1, 3], [2, 6], [8, 10], [15, 18]]],
                "expected": [[1, 6], [8, 10], [15, 18]],
                "description": "standard overlap",
            },
            {
                "input": [[]],
                "expected": [],
                "description": "empty input",
            },
            {
                "input": [[[1, 4], [4, 5]]],
                "expected": [[1, 5]],
                "description": "touching intervals",
            },
        ],
    },
}


def _trial(probe_id: str, response: str, trial_index: int = 0) -> Trial:
    return Trial(probe_id=probe_id, trial_index=trial_index, response=response)


class TestFunctionTestSensor:
    def test_all_tests_pass(self):
        sensor = FunctionTestSensor(ground_truth=GROUND_TRUTH)
        result = sensor.sense(_trial("merge-001", MERGE_INTERVALS_CODE))

        assert len(result) == 1
        assert result[0].passed is True
        assert result[0].score == 1.0
        assert result[0].metrics["tests_passed"] == 3
        assert result[0].metrics["tests_total"] == 3

    def test_wrong_output_fails(self):
        sensor = FunctionTestSensor(ground_truth=GROUND_TRUTH)
        result = sensor.sense(_trial("merge-001", BROKEN_CODE))

        assert result[0].passed is False
        assert result[0].score < 1.0
        assert result[0].metrics["tests_failed"] > 0

    def test_syntax_error_fails(self):
        sensor = FunctionTestSensor(ground_truth=GROUND_TRUTH)
        result = sensor.sense(_trial("merge-001", SYNTAX_ERROR_CODE))

        assert result[0].passed is False
        assert "load error" in result[0].details

    def test_no_code_in_response(self):
        sensor = FunctionTestSensor(ground_truth=GROUND_TRUTH)
        result = sensor.sense(_trial("merge-001", ""))

        assert result[0].passed is False
        assert "no code" in result[0].details

    def test_missing_ground_truth(self):
        sensor = FunctionTestSensor(ground_truth={})
        result = sensor.sense(_trial("merge-001", MERGE_INTERVALS_CODE))

        assert result[0].passed is False
        assert "missing ground truth" in result[0].details

    def test_reading_carries_trial_identity(self):
        sensor = FunctionTestSensor(ground_truth=GROUND_TRUTH)
        result = sensor.sense(_trial("merge-001", MERGE_INTERVALS_CODE, trial_index=2))

        assert result[0].probe_id == "merge-001"
        assert result[0].trial_index == 2
        assert result[0].sensor_name == "function-test"

    def test_partial_pass_score(self):
        """Code that passes some but not all tests gets partial score."""
        # This code handles empty but fails on overlaps
        partial_code = """
def merge_intervals(intervals):
    if not intervals:
        return []
    return intervals  # no actual merging
"""
        sensor = FunctionTestSensor(ground_truth=GROUND_TRUTH)
        result = sensor.sense(_trial("merge-001", partial_code))

        assert result[0].passed is False
        assert 0.0 < result[0].score < 1.0
        assert result[0].metrics["tests_passed"] == 1  # empty input passes
        assert result[0].metrics["tests_failed"] == 2

    def test_exception_in_test_case(self):
        """Code that raises during execution is caught per test case."""
        raise_code = """
def merge_intervals(intervals):
    raise ValueError("boom")
"""
        sensor = FunctionTestSensor(ground_truth=GROUND_TRUTH)
        result = sensor.sense(_trial("merge-001", raise_code))

        assert result[0].passed is False
        assert result[0].score == 0.0
        assert "ValueError" in result[0].details
