---
type: llm
name: 'expectations'
---

PASS if the reply meets every one of these:
- gives the 2026-11-01 error counts per service: auth 10, billing 12, search 13
- names ledger lock timeout and query timeout (7 each) as the most common messages
FAIL if any is missing or contradicted.
Length, detail, tone and confidence are not criteria: judge only whether each requirement is met.
Reference answer: auth 10, billing 12, search 13; most common ledger lock timeout (7) and query timeout (7).
