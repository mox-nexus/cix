"""Test helpers for matrix tests."""

from matrix import Construct, TypedStruct


class FakeComponent:
    """Minimal component for testing — satisfies the Component protocol."""

    def __init__(
        self,
        name: str,
        consumes: frozenset[str],
        produces: str,
        data=None,
    ):
        self.name = name
        self.consumes = consumes
        self.produces = produces
        self._data = data

    async def run(self, construct: Construct) -> TypedStruct:
        value = self._data if self._data is not None else f"{self.name}-output"
        return TypedStruct(type_url=self.produces, value=value)
