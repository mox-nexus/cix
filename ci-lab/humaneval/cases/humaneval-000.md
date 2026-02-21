---
id: humaneval-000
expectation: must_pass
rationale: First HumanEval problem — checks if list is sorted and has no duplicate max elements
difficulty: easy
source: openai/human-eval
entry_point: has_close_elements
---
from typing import List

def has_close_elements(numbers: List[float], threshold: float) -> bool:
    """Check if in given list of numbers, are any two numbers closer to each other than
    given threshold.
    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)
    False
    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)
    True
    """
