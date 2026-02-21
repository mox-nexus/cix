---
id: interval-merging
expectation: must_pass
rationale: Classic algorithmic problem — tests sorting, edge cases, and correctness under iteration
difficulty: medium
test_cases:
  - input: "[[1,3],[2,6],[8,10],[15,18]]"
    expected: "[[1,6],[8,10],[15,18]]"
  - input: "[[1,4],[4,5]]"
    expected: "[[1,5]]"
  - input: "[]"
    expected: "[]"
  - input: "[[1,1]]"
    expected: "[[1,1]]"
  - input: "[[1,4],[0,4]]"
    expected: "[[0,4]]"
  - input: "[[1,4],[2,3]]"
    expected: "[[1,4]]"
  - input: "[[2,3],[4,5],[6,7],[8,9],[1,10]]"
    expected: "[[1,10]]"
  - input: "[[1,3],[0,2],[2,3],[4,6],[5,7]]"
    expected: "[[0,3],[4,7]]"
  - input: "[[1,10],[2,3],[4,5],[6,7]]"
    expected: "[[1,10]]"
  - input: "[[1,2],[3,4],[5,6]]"
    expected: "[[1,2],[3,4],[5,6]]"
  - input: "[[1,100]]"
    expected: "[[1,100]]"
  - input: "[[1,2],[2,3],[3,4],[4,5]]"
    expected: "[[1,5]]"
entry_point: merge
---
Write a function `merge(intervals: list[list[int]]) -> list[list[int]]` that merges all overlapping intervals and returns a list of the non-overlapping intervals that cover all the intervals in the input.

Example:
- Input: `[[1,3],[2,6],[8,10],[15,18]]`
- Output: `[[1,6],[8,10],[15,18]]`
- Explanation: Since intervals [1,3] and [2,6] overlap, merge them into [1,6].

Constraints:
- Each interval is `[start, end]` where `start <= end`
- The input list may be empty
- Intervals may be in any order
- Adjacent intervals (e.g., [1,4] and [4,5]) should be merged
