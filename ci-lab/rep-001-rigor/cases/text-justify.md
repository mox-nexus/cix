---
id: text-justify
expectation: must_pass
rationale: String manipulation with tricky edge cases — tests precision under iteration
difficulty: hard
test_cases:
  - input: '{"words": ["This","is","an","example","of","text","justification."], "maxWidth": 16}'
    expected: '["This    is    an","example  of text","justification.  "]'
  - input: '{"words": ["What","must","be","acknowledgment","shall","be"], "maxWidth": 16}'
    expected: '["What   must   be","acknowledgment  ","shall be        "]'
  - input: '{"words": ["Science","is","what","we","understand","well","enough","to","explain","to","a","computer.","Art","is","everything","else","we","do"], "maxWidth": 20}'
    expected: '["Science  is  what we","understand      well","enough to explain to","a  computer.  Art is","everything  else  we","do                  "]'
  - input: '{"words": ["a"], "maxWidth": 1}'
    expected: '["a"]'
  - input: '{"words": ["a"], "maxWidth": 5}'
    expected: '["a    "]'
  - input: '{"words": ["a","b"], "maxWidth": 3}'
    expected: '["a b"]'
  - input: '{"words": ["Listen","to","many,","speak","to","a","few."], "maxWidth": 6}'
    expected: '["Listen","to    ","many, ","speak ","to   a","few.  "]'
entry_point: fullJustify
---
Write a function `fullJustify(words: list[str], maxWidth: int) -> list[str]` that formats text to be fully justified with each line exactly `maxWidth` characters.

Rules:
1. Pack as many words as possible per line. Pad with extra spaces when necessary so each line has exactly `maxWidth` characters.
2. Extra spaces between words should be distributed as evenly as possible. If the number of spaces doesn't divide evenly, the left slots get more spaces than the right.
3. The last line should be left-justified (no extra space between words) and padded with trailing spaces.
4. A line with only one word should be left-justified with trailing spaces.

Example:
- Input: `words = ["This","is","an","example","of","text","justification."]`, `maxWidth = 16`
- Output:
  ```
  "This    is    an"
  "example  of text"
  "justification.  "
  ```
