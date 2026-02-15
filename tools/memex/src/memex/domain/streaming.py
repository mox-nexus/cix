"""Functional streaming operators for generator pipelines.

Domain-agnostic. No infrastructure dependencies.
These are the building blocks for source -> transform -> sink -> tap -> terminal pipelines.
"""

from collections.abc import Callable, Iterator


def tap[T](iterator: Iterator[T], fn: Callable[[T], None]) -> Iterator[T]:
    """Observe each element without consuming it.

    Applies fn as a side effect, then yields the element unchanged.
    """
    for item in iterator:
        fn(item)
        yield item


def tap_every[T](iterator: Iterator[T], n: int, fn: Callable[[int], None]) -> Iterator[T]:
    """Side effect every n-th element. Counter is 1-based.

    Yields every element; calls fn(i) only when i % n == 0.
    """
    for i, item in enumerate(iterator, 1):
        yield item
        if i % n == 0:
            fn(i)
