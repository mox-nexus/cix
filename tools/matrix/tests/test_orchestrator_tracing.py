"""Tests for Orchestrator OTel tracing — verifies spans are emitted."""

import pytest
from matrix import ContractError, Orchestrator, TypedStruct
from matrix_helpers import FakeComponent
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

# Single provider for the test module — OTel only allows set_tracer_provider once.
_exporter = InMemorySpanExporter()
_provider = TracerProvider()
_provider.add_span_processor(SimpleSpanProcessor(_exporter))
trace.set_tracer_provider(_provider)


@pytest.fixture(autouse=True)
def _clear_spans():
    _exporter.clear()
    yield
    _exporter.clear()


def _spans():
    return _exporter.get_finished_spans()


def _spans_named(name: str):
    return [s for s in _spans() if s.name == name]


class TestDagSpan:
    async def test_dag_run_span_emitted(self):
        probe = FakeComponent("probe", frozenset(), "probe.response")
        orch = Orchestrator([probe])
        await orch.run()

        assert len(_spans_named("matrix.dag.run")) == 1

    async def test_artifact_count_attribute(self):
        probe = FakeComponent("probe", frozenset(), "probe.response")
        sensor = FakeComponent("sensor", frozenset({"probe.response"}), "sensor.grade")

        orch = Orchestrator([probe, sensor])
        await orch.run()

        dag_span = _spans_named("matrix.dag.run")[0]
        assert dag_span.attributes["matrix.dag.artifact_count"] == 2

    async def test_empty_dag(self):
        orch = Orchestrator([])
        await orch.run()

        dag_span = _spans_named("matrix.dag.run")[0]
        assert dag_span.attributes["matrix.dag.artifact_count"] == 0


class TestComponentSpans:
    async def test_component_spans_emitted(self):
        probe = FakeComponent("probe", frozenset(), "probe.response")
        sensor = FakeComponent("sensor", frozenset({"probe.response"}), "sensor.grade")

        orch = Orchestrator([probe, sensor])
        await orch.run()

        comp_spans = _spans_named("matrix.component.run")
        assert len(comp_spans) == 2

        names = {s.attributes["matrix.component.name"] for s in comp_spans}
        assert names == {"probe", "sensor"}

    async def test_component_attributes(self):
        probe = FakeComponent("probe", frozenset(), "probe.response")
        orch = Orchestrator([probe])
        await orch.run()

        comp_span = _spans_named("matrix.component.run")[0]
        assert comp_span.attributes["matrix.component.name"] == "probe"
        assert comp_span.attributes["matrix.component.produces"] == "probe.response"


class TestSpanHierarchy:
    async def test_component_is_child_of_dag(self):
        probe = FakeComponent("probe", frozenset(), "probe.response")
        orch = Orchestrator([probe])
        await orch.run()

        dag_span = _spans_named("matrix.dag.run")[0]
        comp_span = _spans_named("matrix.component.run")[0]

        assert comp_span.parent.span_id == dag_span.context.span_id


class TestErrorTracing:
    async def test_component_error_recorded(self):
        class FailComponent:
            name = "fail"
            consumes: frozenset[str] = frozenset()
            produces = "fail.output"

            async def run(self, construct):
                raise ValueError("boom")

        orch = Orchestrator([FailComponent()])
        with pytest.raises(ValueError, match="boom"):
            await orch.run()

        comp_spans = _spans_named("matrix.component.run")
        assert len(comp_spans) == 1
        assert comp_spans[0].status.status_code == trace.StatusCode.ERROR

    async def test_contract_error_recorded(self):
        class MismatchComponent:
            name = "liar"
            consumes: frozenset[str] = frozenset()
            produces = "declared.type"

            async def run(self, construct):
                return TypedStruct(type_url="actual.type", value="data")

        orch = Orchestrator([MismatchComponent()])
        with pytest.raises(ContractError):
            await orch.run()

        comp_spans = _spans_named("matrix.component.run")
        assert len(comp_spans) == 1
        assert comp_spans[0].status.status_code == trace.StatusCode.ERROR


class TestNoOpSafety:
    async def test_orchestrator_works_regardless_of_tracing(self):
        probe = FakeComponent("probe", frozenset(), "probe.response")
        orch = Orchestrator([probe])
        construct = await orch.run()

        assert len(construct) == 1
        assert construct["probe.response"] is not None
