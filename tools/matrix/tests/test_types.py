"""Tests for Matrix types: Artifact, Construct, Component, TypedStruct."""

import pytest
from matrix import Artifact, Component, Construct, ContractError, TypedStruct


class TestArtifact:
    def test_create_stamps_id_and_timestamp(self):
        a = Artifact.create(type_url="test.v1/data", producer="probe", data="hello")
        assert a.type_url == "test.v1/data"
        assert a.producer == "probe"
        assert a.data == "hello"
        assert len(a.id) == 36  # UUID
        assert a.timestamp is not None

    def test_frozen(self):
        a = Artifact.create(type_url="test.v1/data", producer="probe", data="hello")
        with pytest.raises(Exception):
            a.data = "mutate"

    def test_unique_ids(self):
        a1 = Artifact.create(type_url="test.v1/x", producer="p", data=1)
        a2 = Artifact.create(type_url="test.v1/x", producer="p", data=2)
        assert a1.id != a2.id


class TestConstruct:
    def test_empty_creation(self):
        c = Construct()
        assert len(c) == 0
        assert c.kinds() == frozenset()
        assert c.ledger == ()

    def test_append_and_retrieve(self):
        c = Construct()
        a = Artifact.create(type_url="test.v1/data", producer="probe", data="hello")
        c.append(a)
        assert c["test.v1/data"] == "hello"

    def test_getitem_returns_last_data(self):
        c = Construct()
        a1 = Artifact.create(type_url="test.v1/data", producer="p", data="first")
        a2 = Artifact.create(type_url="test.v1/data", producer="p", data="second")
        c.append(a1)
        c.append(a2)
        assert c["test.v1/data"] == "second"

    def test_getitem_raises_on_missing(self):
        c = Construct()
        with pytest.raises(LookupError, match="No artifact for type_url 'missing'"):
            c["missing"]

    def test_error_message_shows_available(self):
        c = Construct()
        a = Artifact.create(type_url="test.v1/data", producer="p", data="hello")
        c.append(a)
        with pytest.raises(LookupError, match="test.v1/data"):
            c["missing"]

    def test_error_message_empty(self):
        c = Construct()
        with pytest.raises(LookupError, match=r"\(none\)"):
            c["missing"]

    def test_contains(self):
        c = Construct()
        assert "test.v1/data" not in c
        a = Artifact.create(type_url="test.v1/data", producer="p", data="hello")
        c.append(a)
        assert "test.v1/data" in c

    def test_kinds(self):
        c = Construct()
        c.append(Artifact.create(type_url="test.v1/a", producer="p", data=1))
        c.append(Artifact.create(type_url="test.v1/b", producer="p", data=2))
        assert c.kinds() == frozenset({"test.v1/a", "test.v1/b"})

    def test_len_counts_unique_types(self):
        c = Construct()
        assert len(c) == 0
        c.append(Artifact.create(type_url="test.v1/a", producer="p", data=1))
        assert len(c) == 1
        c.append(Artifact.create(type_url="test.v1/b", producer="p", data=2))
        assert len(c) == 2
        # Same type_url — len stays 2
        c.append(Artifact.create(type_url="test.v1/a", producer="p", data=3))
        assert len(c) == 2

    def test_query_returns_all_of_type(self):
        c = Construct()
        a1 = Artifact.create(type_url="test.v1/x", producer="p", data=1)
        a2 = Artifact.create(type_url="test.v1/x", producer="p", data=2)
        a3 = Artifact.create(type_url="test.v1/y", producer="p", data=3)
        c.append(a1)
        c.append(a2)
        c.append(a3)
        result = c.query("test.v1/x")
        assert len(result) == 2
        assert result[0].data == 1
        assert result[1].data == 2

    def test_query_empty(self):
        c = Construct()
        assert c.query("test.v1/missing") == []

    def test_last_returns_most_recent(self):
        c = Construct()
        c.append(Artifact.create(type_url="test.v1/x", producer="p", data="first"))
        c.append(Artifact.create(type_url="test.v1/x", producer="p", data="last"))
        assert c.last("test.v1/x").data == "last"

    def test_ledger_preserves_order(self):
        c = Construct()
        c.append(Artifact.create(type_url="test.v1/a", producer="p", data=1))
        c.append(Artifact.create(type_url="test.v1/b", producer="p", data=2))
        c.append(Artifact.create(type_url="test.v1/a", producer="p", data=3))
        ledger = c.ledger
        assert len(ledger) == 3
        assert [a.data for a in ledger] == [1, 2, 3]

    def test_data_any_type(self):
        """Construct stores any type — no type constraints on values."""
        c = Construct()
        for i, data in enumerate(("str", 42, 3.14, True, None, (1, 2), {"nested": True}, [1, 2])):
            c.append(Artifact.create(type_url=f"test.v1/kind.{i}", producer="p", data=data))
            assert c[f"test.v1/kind.{i}"] == data


class TestTypedStruct:
    def test_creation(self):
        ts = TypedStruct(type_url="test.v1/data", value="hello")
        assert ts.type_url == "test.v1/data"
        assert ts.value == "hello"

    def test_named_tuple(self):
        """TypedStruct is a NamedTuple — indexed and unpacked."""
        ts = TypedStruct(type_url="test.v1/x", value=42)
        assert ts[0] == "test.v1/x"
        assert ts[1] == 42
        type_url, value = ts
        assert type_url == "test.v1/x"
        assert value == 42

    def test_structural_compatibility(self):
        """Any 2-tuple with matching fields satisfies TypedStruct shape."""
        from collections import namedtuple

        External = namedtuple("External", ["type_url", "value"])
        ext = External(type_url="ext.v1/data", value="payload")
        assert ext.type_url == "ext.v1/data"
        assert ext.value == "payload"

    def test_immutable(self):
        ts = TypedStruct(type_url="test.v1/x", value="data")
        with pytest.raises(AttributeError):
            ts.type_url = "mutated"


class TestContractError:
    def test_is_exception(self):
        assert issubclass(ContractError, Exception)

    def test_message(self):
        err = ContractError("produces='X' but returned type_url='Y'")
        assert "X" in str(err)
        assert "Y" in str(err)


class TestComponent:
    def test_satisfies_protocol(self):
        class MyProbe:
            name = "my-probe"
            consumes: frozenset[str] = frozenset()
            produces = "probe.response"

            async def run(self, construct: Construct) -> TypedStruct:
                return TypedStruct(type_url="probe.response", value="Hello, world")

        assert isinstance(MyProbe(), Component)

    def test_with_dependencies(self):
        class MySensor:
            name = "my-sensor"
            consumes = frozenset({"probe.response"})
            produces = "sensor.grade"

            async def run(self, construct: Construct) -> TypedStruct:
                response = construct["probe.response"]
                return TypedStruct(type_url="sensor.grade", value=len(response) > 0)

        sensor = MySensor()
        assert isinstance(sensor, Component)
        assert sensor.consumes == frozenset({"probe.response"})

    def test_incomplete_rejects(self):
        class Incomplete:
            name = "test"
            # missing consumes, produces, run

        assert not isinstance(Incomplete(), Component)

    def test_dag_chain(self):
        """Three-node DAG: probe -> sensor -> scorer."""

        class Probe:
            name = "probe"
            consumes: frozenset[str] = frozenset()
            produces = "probe.response"

            async def run(self, construct: Construct) -> TypedStruct:
                return TypedStruct(type_url="probe.response", value="Response")

        class Sensor:
            name = "sensor"
            consumes = frozenset({"probe.response"})
            produces = "sensor.grade"

            async def run(self, construct: Construct) -> TypedStruct:
                response = construct["probe.response"]
                return TypedStruct(
                    type_url="sensor.grade",
                    value={"passed": len(response) > 10, "score": 0.95},
                )

        class Scorer:
            name = "scorer"
            consumes = frozenset({"sensor.grade"})
            produces = "scorer.verdict"

            async def run(self, construct: Construct) -> TypedStruct:
                grade = construct["sensor.grade"]
                return TypedStruct(
                    type_url="scorer.verdict",
                    value="pass" if grade["passed"] else "fail",
                )

        for cls in (Probe, Sensor, Scorer):
            assert isinstance(cls(), Component)


class TestLifecycle:
    """End-to-end: empty Construct -> enriched Construct via Artifacts."""

    def test_manual_enrichment(self):
        """Simulate what the engine will do (without the engine)."""
        construct = Construct()

        artifact = Artifact.create(type_url="probe.response", producer="probe", data="Hello, world")
        construct.append(artifact)

        assert construct["probe.response"] == "Hello, world"
        assert len(construct) == 1

    def test_multi_component_enrichment(self):
        """Simulate probe -> sensor -> scorer chain."""
        c = Construct()

        c.append(
            Artifact.create(
                type_url="probe.response",
                producer="probe",
                data="I can help with evals",
            )
        )
        c.append(
            Artifact.create(
                type_url="sensor.grade",
                producer="sensor",
                data={"passed": True, "score": 1.0},
            )
        )
        c.append(Artifact.create(type_url="scorer.verdict", producer="scorer", data="pass"))

        assert len(c) == 3
        assert c["scorer.verdict"] == "pass"
        assert c.kinds() == frozenset({"probe.response", "sensor.grade", "scorer.verdict"})

    def test_parallel_batch_simulation(self):
        """Simulate parallel components in same batch."""
        c = Construct()

        # Batch 1: probe runs alone
        c.append(Artifact.create(type_url="probe.response", producer="probe", data="response"))

        # Batch 2: sensor-a and sensor-b run in parallel
        c.append(Artifact.create(type_url="sensor.accuracy", producer="sensor-a", data=0.95))
        c.append(Artifact.create(type_url="sensor.latency", producer="sensor-b", data=42))

        assert len(c) == 3
        assert c["sensor.accuracy"] == 0.95
        assert c["sensor.latency"] == 42
