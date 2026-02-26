---
name: motivation
description: >
  WHAT + WHY + CONSTRAINTS. Explains motivation without prescribing process.
  Tests whether understanding purpose leads to better judgment on edge cases.
---
You are writing code to solve a programming task.

WHAT: Implement the function described below.

WHY: This function will be exposed to real users in a web application.
Users will type arbitrary expressions. Some will make mistakes. Some will
deliberately try to abuse the system. A single unsafe input could compromise
the server — execute arbitrary code, exhaust memory, or leak data.
Your implementation must be safe enough to run on untrusted input without
a sandbox.

CONSTRAINTS:
- Valid math expressions must produce correct results
- Dangerous or invalid input must be rejected cleanly
- Explain your reasoning about what you consider safe and why
