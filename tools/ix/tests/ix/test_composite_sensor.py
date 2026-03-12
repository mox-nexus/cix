"""Tests for CompositeSensor — combines multiple sensors into one.

Source: ix/eval/sensors.py
"""

import pytest
from ix.domain.ports import Sensor
from ix.domain.types import Reading, Trial
from ix.eval.sensors import CompositeSensor


class _CountingSensor:
    """Stub sensor that always passes and counts invocations."""

    def __init__(self, name: str):
        self._name = name
        self.call_count = 0

    @property
    def name(self) -> str:
        return self._name

    def measure(self, trial: Trial) -> list[Reading]:
        self.call_count += 1
        return [
            Reading(
                sensor_name=self._name,
                probe_id=trial.probe_id,
                trial_index=trial.trial_index,
                passed=True,
                score=1.0,
            )
        ]


class _MultiReadingSensor:
    """Stub sensor that returns multiple readings per trial."""

    @property
    def name(self) -> str:
        return "multi"

    def measure(self, trial: Trial) -> list[Reading]:
        return [
            Reading(
                sensor_name="multi",
                probe_id=trial.probe_id,
                trial_index=trial.trial_index,
                passed=True,
                score=1.0,
                details="check-a",
            ),
            Reading(
                sensor_name="multi",
                probe_id=trial.probe_id,
                trial_index=trial.trial_index,
                passed=False,
                score=0.0,
                details="check-b",
            ),
        ]


def _trial() -> Trial:
    return Trial(probe_id="test", trial_index=0, response="ok")


class TestCompositeSensor:
    def test_satisfies_sensor_protocol(self):
        composite = CompositeSensor([_CountingSensor("a")])
        assert isinstance(composite, Sensor)

    def test_name_joins_child_names(self):
        composite = CompositeSensor([_CountingSensor("alpha"), _CountingSensor("beta")])
        assert composite.name == "alpha+beta"

    def test_flattens_readings_from_all_sensors(self):
        s1 = _CountingSensor("s1")
        s2 = _CountingSensor("s2")
        composite = CompositeSensor([s1, s2])

        readings = composite.measure(_trial())

        assert len(readings) == 2
        assert readings[0].sensor_name == "s1"
        assert readings[1].sensor_name == "s2"

    def test_flattens_multi_reading_sensors(self):
        composite = CompositeSensor([_CountingSensor("single"), _MultiReadingSensor()])
        readings = composite.measure(_trial())
        assert len(readings) == 3  # 1 from single + 2 from multi

    def test_invokes_all_children(self):
        s1 = _CountingSensor("s1")
        s2 = _CountingSensor("s2")
        composite = CompositeSensor([s1, s2])

        composite.measure(_trial())
        composite.measure(_trial())

        assert s1.call_count == 2
        assert s2.call_count == 2

    def test_rejects_empty_sensor_list(self):
        with pytest.raises(ValueError, match="at least one"):
            CompositeSensor([])
