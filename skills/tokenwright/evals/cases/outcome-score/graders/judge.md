---
type: llm
name: 'expectations'
---

PASS if the reply meets every one of these:
- names reading logs/app.log whole (about 3,000 lines) as the main cost
- says it was read three times, or that the second and third reads repeated the first
- suggests searching the log (grep for ERROR) or reading only a range instead
FAIL if any is missing or contradicted.
Length, detail, tone and confidence are not criteria: judge only whether each requirement is met.
Reference answer: the three whole reads of logs/app.log are nearly all the cost; one grep for ERROR (2 hits) would have done.
